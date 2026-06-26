"""
Rice phenotype prediction model architectures.
Two variants: GeneMMOE (genotype-only, multi-task) and EnvMMOE (genotype+environment, single-task).
"""
import torch
import torch.nn as nn
import torch.nn.functional as F


class GeneResidualMLP(nn.Module):
    """ResidualMLP for genotype-only models (negative_slope=0.01)."""
    def __init__(self, dim, hidden, drop=0.2):
        super().__init__()
        self.fc1 = nn.Linear(dim, hidden)
        self.fc2 = nn.Linear(hidden, dim)
        self.bn1 = nn.BatchNorm1d(hidden)
        self.drop = nn.Dropout(drop)
        self.act = nn.LeakyReLU(inplace=True)

    def forward(self, x):
        h = self.drop(self.act(self.bn1(self.fc1(x))))
        return self.act(x + self.fc2(h))


class GeneMMOE(nn.Module):
    """Multi-gate Mixture-of-Experts for genotype-only prediction (10 tasks)."""
    def __init__(self, input_dim, task_num, num_experts=6, expert_dim=256,
                 tower_dims=(256, 128), drop=0.25):
        super().__init__()
        self.task_num = task_num
        self.input_bn = nn.BatchNorm1d(input_dim)
        self.shared = nn.Sequential(
            nn.Linear(input_dim, expert_dim), nn.LeakyReLU(inplace=True)
        )
        self.experts = nn.ModuleList(
            [GeneResidualMLP(expert_dim, expert_dim, drop) for _ in range(num_experts)]
        )
        self.gates = nn.ModuleList(
            [nn.Linear(expert_dim, num_experts) for _ in range(task_num)]
        )
        self.towers = nn.ModuleList([
            nn.Sequential(
                nn.Linear(expert_dim, tower_dims[0]), nn.LeakyReLU(inplace=True), nn.Dropout(drop),
                nn.Linear(tower_dims[0], tower_dims[1]), nn.LeakyReLU(inplace=True), nn.Dropout(drop),
                nn.Linear(tower_dims[1], 1)
            ) for _ in range(task_num)
        ])

    def forward(self, x):
        x = self.input_bn(x)
        h = self.shared(x)
        expert_outs = torch.stack([E(h) for E in self.experts], dim=2)
        outs = []
        for t in range(self.task_num):
            w = F.softmax(self.gates[t](h), dim=-1).unsqueeze(-1)
            m = torch.bmm(expert_outs, w).squeeze(-1)
            outs.append(self.towers[t](m).squeeze(-1))
        return outs


class EnvResidualMLP(nn.Module):
    """ResidualMLP for environment models (negative_slope=0.1)."""
    def __init__(self, dim, hidden, drop=0.3):
        super().__init__()
        self.fc1 = nn.Linear(dim, hidden)
        self.fc2 = nn.Linear(hidden, dim)
        self.bn1 = nn.BatchNorm1d(hidden)
        self.drop = nn.Dropout(drop)
        self.act = nn.LeakyReLU(0.1)

    def forward(self, x):
        h = self.act(self.bn1(self.fc1(x)))
        h = self.drop(h)
        return self.act(x + self.fc2(h))


class EnvMMOE(nn.Module):
    """MMoE for environment+genotype prediction (single task per model)."""
    def __init__(self, input_dim, task_num=1, num_experts=6, expert_dim=256,
                 tower_dims=(256, 128), drop=0.3):
        super().__init__()
        self.task_num = task_num
        self.input_bn = nn.BatchNorm1d(input_dim)
        self.shared = nn.Sequential(
            nn.Linear(input_dim, expert_dim), nn.LeakyReLU()
        )
        self.experts = nn.ModuleList(
            [EnvResidualMLP(expert_dim, expert_dim, drop) for _ in range(num_experts)]
        )
        self.gates = nn.ModuleList(
            [nn.Linear(expert_dim, num_experts) for _ in range(task_num)]
        )
        self.towers = nn.ModuleList([
            nn.Sequential(
                nn.Linear(expert_dim, tower_dims[0]), nn.LeakyReLU(), nn.Dropout(drop),
                nn.Linear(tower_dims[0], tower_dims[1]), nn.LeakyReLU(), nn.Dropout(drop),
                nn.Linear(tower_dims[1], 1)
            ) for _ in range(task_num)
        ])

    def forward(self, x):
        x = torch.nan_to_num(x)
        x = self.input_bn(x)
        h = self.shared(x)
        expert_outs = torch.stack([E(h) for E in self.experts], dim=2)
        outputs = []
        for t in range(self.task_num):
            g = F.softmax(self.gates[t](h), dim=-1).unsqueeze(-1)
            m = torch.bmm(expert_outs, g).squeeze(-1)
            outputs.append(self.towers[t](m).squeeze(-1))
        return outputs
