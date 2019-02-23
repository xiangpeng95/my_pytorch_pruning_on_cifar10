import torch
import torch.nn as nn

import torch.nn.functional as F

from .layers import bn

class LeNet(nn.Module):
    def __init__(self, alpha=0.001):
        super(LeNet, self).__init__()
        self.alpha = alpha
        self.prune = False # change this to true when you want to remove channels
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.bn1   = bn.BatchNorm2dEx(6)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.bn2   = bn.BatchNorm2dEx(16)
        self.fc1   = nn.Linear(16*5*5, 120)
        self.fc2   = nn.Linear(120, 84)
        self.fc3   = nn.Linear(84, 10)

    def forward(self, x):
        out = F.relu(self.bn1(self.conv1(x), self.conv1.weight))
        out = F.max_pool2d(out, 2)
        out = F.relu(self.bn2(self.conv2(out), self.conv2.weight))
        out = F.max_pool2d(out, 2)
        out = out.view(out.size(0), -1)
        out = F.relu(self.fc1(out))
        out = F.relu(self.fc2(out))
        out = self.fc3(out)
        return out



class LeNetCompressed(nn.Module):
    def __init__(self, channels=[]):
        super(LeNetCompressed, self).__init__()
        print(channels)

        self.conv1 = nn.Conv2d(3, channels[0], 5)
        self.bn1   = nn.BatchNorm2d(channels[0])
        self.conv2 = nn.Conv2d(channels[0], channels[1], 5)
        self.bn2   = nn.BatchNorm2d(channels[1])
        self.fc1   = nn.Linear(channels[1]*5*5, 120)
        self.fc2   = nn.Linear(120, 84)
        self.fc3   = nn.Linear(84, 10)


    def forward(self, x):
        out = F.relu(self.bn1(self.conv1(x)))
        out = F.max_pool2d(out, 2)
        out = F.relu(self.bn2(self.conv2(out)))
        out = F.max_pool2d(out, 2)
        out = out.view(out.size(0), -1)
        out = F.relu(self.fc1(out))
        out = F.relu(self.fc2(out))
        out = self.fc3(out)
        return out
