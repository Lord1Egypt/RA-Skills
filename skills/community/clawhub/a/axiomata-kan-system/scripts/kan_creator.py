#!/usr/bin/env python3
"""
KAN Creator — 创建新的KAN概念和骨架
Morgana守护者 — 精神(Shén) + 爱(Ài)
"""

import os
import sys
import json
import argparse

# 默认配置
DEFAULT_CONFIG = {
    "input_size": 768,
    "hidden_size": 32,
    "output_size": 3,
    "grid_size": 5,
    "k": 3,
    "layers": [768, 32, 16, 8, 4, 3],
    "activation": "silu",
    "loss_function": "cross_entropy",
    "optimizer": "adam",
    "learning_rate": 0.001,
    "batch_size": 32,
    "epochs": 50,
    "train_samples": 200,
    "num_classes": 4
}


def create_kan(name: str, role: str, agent: str, output_size: int = 3, input_size: int = 768):
    """创建新的KAN概念"""
    
    base_path = f"/media/ezekiel/Morgana/skills/axioma-kan-system"
    
    # 创建目录结构
    kan_dir = os.path.join(base_path, name)
    models_dir = os.path.join(kan_dir, "models")
    data_dir = os.path.join(kan_dir, "data")
    scripts_dir = os.path.join(kan_dir, "scripts")
    
    for d in [kan_dir, models_dir, data_dir, scripts_dir]:
        os.makedirs(d, exist_ok=True)
    
    # 创建配置
    config = DEFAULT_CONFIG.copy()
    config["name"] = name
    config["role"] = role
    config["agent"] = agent
    config["output_size"] = output_size
    config["input_size"] = input_size
    # Adjust layers for output_size
    config["layers"][-1] = output_size
    
    config_path = os.path.join(kan_dir, "config.json")
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    # 创建KAN模型类
    model_code = f'''#!/usr/bin/env python3
"""
{name}_kan.py — KAN模型定义
角色: {role}
代理: {agent}
"""

import torch
import torch.nn as nn
from typing import List


class KANLayer(nn.Module):
    """单层KAN"""
    
    def __init__(self, in_features, out_features, grid_size=5, k=3):
        super().__init__()
        self.in_features = in_features
        self.out_features = out_features
        self.grid_size = grid_size
        self.k = k
        
        # B-spline基函数参数
        self.base_weight = nn.Parameter(torch.randn(out_features, in_features))
        self.spline_weight = nn.Parameter(torch.randn(out_features, in_features, grid_size))
        
    def forward(self, x):
        # 基激活
        base = torch.nn.functional.silu(torch.matmul(x, self.base_weight.T))
        
        # Spline激活
        spline = torch.matmul(x, self.spline_weight)
        
        return base + spline


class KANModel(nn.Module):
    """完整KAN模型: {name}"""
    
    def __init__(self, layers: List[int] = {layers}, grid_size=5, k=3):
        super().__init__()
        self.layers_list = layers
        
        self.kan_layers = nn.ModuleList([
            KANLayer(layers[i], layers[i+1], grid_size, k)
            for i in range(len(layers) - 1)
        ])
        
    def forward(self, x):
        for layer in self.kan_layers:
            x = layer(x)
        return x
    
    def get_activations(self, x):
        """获取所有层激活"""
        activations = [x]
        for layer in self.kan_layers:
            x = layer(x)
            activations.append(x)
        return activations


def create_kan_{name}(config_path: str = None):
    """创建KAN模型"""
    if config_path:
        import json
        with open(config_path, 'r') as f:
            config = json.load(f)
        layers = config.get('layers', {layers})
    else:
        layers = {layers}
    
    return KANModel(layers=layers)


if __name__ == "__main__":
    model = create_kan_{name}()
    print(f"✅ {name} KAN创建完成")
    print(f"   参数: {{sum(p.numel() for p in model.parameters()):,}}")
'''.format(name=name, layers=str(DEFAULT_CONFIG["layers"]))
    
    model_path = os.path.join(scripts_dir, f"{name}_kan.py")
    with open(model_path, 'w') as f:
        f.write(model_code)
    
    # 创建训练脚本
    train_code = f'''#!/usr/bin/env python3
"""
{name}_train.py — 训练{name} KAN
"""

import torch
import torch.nn as nn
from {name}_kan import create_kan_{name}
import json
import os


def train_{name}(epochs=50, batch_size=32):
    """训练{name} KAN"""
    
    # 加载配置
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    # 创建模型
    model = create_kan_{name}(config_path)
    
    # 生成训练数据
    train_data = torch.randn(config['train_samples'], config['input_size'])
    train_labels = torch.randint(0, config['num_classes'], (config['train_samples'],))
    
    # 训练循环
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=config['learning_rate'])
    
    for epoch in range(epochs):
        # Forward
        output = model(train_data)
        loss = criterion(output, train_labels)
        
        # Backward
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        if (epoch + 1) % 10 == 0:
            print(f"Epoch {{epoch+1}}/{epochs}: Loss = {{loss.item():.4f}}")
    
    # 保存模型
    model_dir = os.path.join(os.path.dirname(__file__), '..', 'models')
    os.makedirs(model_dir, exist_ok=True)
    torch.save(model.state_dict(), os.path.join(model_dir, f'{name}_kan.pt'))
    
    print(f"✅ {{name}} KAN训练完成")
    return loss.item()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--epochs', type=int, default=50)
    parser.add_argument('--batch-size', type=int, default=32)
    args = parser.parse_args()
    
    train_{name}(epochs=args.epochs, batch_size=args.batch_size)
'''
    
    train_path = os.path.join(scripts_dir, f"{name}_train.py")
    with open(train_path, 'w') as f:
        f.write(train_code)
    
    print(f"✅ KAN概念 '{name}' 创建完成")
    print(f"📁 目录: {kan_dir}")
    print(f"📋 配置: {config_path}")
    print(f"🧠 模型: {model_path}")
    print(f"🏋️ 训练: {train_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='创建KAN概念')
    parser.add_argument('--name', required=True, help='KAN名称')
    parser.add_argument('--role', required=True, help='KAN角色描述')
    parser.add_argument('--agent', required=True, help='所属代理(morgana/ezeziel/merlin)')
    parser.add_argument('--output-size', type=int, default=3, help='输出维度')
    parser.add_argument('--input-size', type=int, default=768, help='输入维度')
    
    args = parser.parse_args()
    
    create_kan(args.name, args.role, args.agent, args.output_size, args.input_size)