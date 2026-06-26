#!/usr/bin/env python3
"""
🕐 CRON KAN TRAINER
===================
Trains the Cron Evaluator KAN

Architecture: 16 → 32 → 16 → 8 → 4 → 3
Input: 16 features (cron quality metrics)
Output: 3 classes (BAD=0, OK=1, GOOD=2)
"""

import os
import json
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import numpy as np
from pathlib import Path

MODEL_DIR = "/mnt/Morgana/skills/cron-evaluator/models"
DATA_DIR = "/mnt/Morgana/skills/cron-evaluator/data"
os.makedirs(MODEL_DIR, exist_ok=True)


class CronKANNet(nn.Module):
    """KAN for cron quality prediction - 16→32→16→8→4→3"""
    
    def __init__(self, input_dim=16, output_dim=3):
        super().__init__()
        
        self.layers = nn.ModuleList([
            nn.Linear(input_dim, 32),
            nn.Linear(32, 16),
            nn.Linear(16, 8),
            nn.Linear(8, 4),
            nn.Linear(4, output_dim)
        ])
        
        self.bn_layers = nn.ModuleList([
            nn.BatchNorm1d(32),
            nn.BatchNorm1d(16),
            nn.BatchNorm1d(8),
            nn.BatchNorm1d(4)
        ])
        
        self.activation = nn.ReLU()
        self.dropout = nn.Dropout(0.1)
        self.output_activation = nn.Sigmoid()
    
    def forward(self, x):
        for i, layer in enumerate(self.layers[:-1]):
            x = layer(x)
            x = self.bn_layers[i](x)
            x = self.activation(x)
            x = self.dropout(x)
        
        x = self.layers[-1](x)
        return self.output_activation(x)


class CronDataset(Dataset):
    def __init__(self, data):
        self.features = torch.tensor([d["features"] for d in data], dtype=torch.float32)
        self.labels = torch.tensor([d["label"] for d in data], dtype=torch.long)
    
    def __len__(self):
        return len(self.labels)
    
    def __getitem__(self, idx):
        return self.features[idx], self.labels[idx]


def train_kan(epochs=500, batch_size=8, lr=0.001):
    """Train the Cron KAN"""
    
    print("=" * 60)
    print("TRAINING CRON KAN (16→32→16→8→4→3)")
    print("=" * 60)
    
    # Load training data
    with open(f"{DATA_DIR}/cron_training.json", 'r') as f:
        data = json.load(f)
    
    print(f"\n📊 Training samples: {len(data)}")
    
    dataset = CronDataset(data)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
    
    # Model
    model = CronKANNet(input_dim=16, output_dim=3)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=150, gamma=0.5)
    
    # Training
    print("\n🚀 Training...")
    for epoch in range(epochs):
        model.train()
        total_loss = 0
        correct = 0
        total = 0
        
        for batch_features, batch_labels in dataloader:
            optimizer.zero_grad()
            outputs = model(batch_features)
            loss = criterion(outputs, batch_labels)
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
            _, predicted = torch.max(outputs, 1)
            total += batch_labels.size(0)
            correct += (predicted == batch_labels).sum().item()
        
        scheduler.step()
        
        if (epoch + 1) % 100 == 0:
            accuracy = 100 * correct / total
            print(f"   Epoch {epoch+1}/{epochs} - Loss: {total_loss/len(dataloader):.4f} - Acc: {accuracy:.1f}%")
    
    # Save
    model_path = f"{MODEL_DIR}/cron_kan.pt"
    torch.save({
        'model_state_dict': model.state_dict(),
        'architecture': '16→32→16→8→4→3',
        'input_dim': 16,
        'output_dim': 3,
        'training_samples': len(data),
        'epochs': epochs
    }, model_path)
    
    print(f"\n✅ Model saved to: {model_path}")
    
    # Test
    print("\n🧪 Testing...")
    model.eval()
    with torch.no_grad():
        test_input = torch.randn(1, 16)
        test_output = model(test_input)
        print(f"   Output shape: {test_output.shape}")
        print(f"   Output: {test_output}")
    
    return model


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=500)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--lr", type=float, default=0.001)
    args = parser.parse_args()
    
    train_kan(epochs=args.epochs, batch_size=args.batch_size, lr=args.lr)
