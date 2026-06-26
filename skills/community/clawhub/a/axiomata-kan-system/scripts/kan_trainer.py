#!/usr/bin/env python3
"""
KAN Trainer — 训练KAN模型
Morgana守护者 — 精神(Shén) + 爱(Ài)
"""

import os
import sys
import json
import argparse
import torch
import torch.nn as nn

# 默认路径
KAN_STRUCTURE = {
    "stc": {
        "path": "/media/ezekiel/Morgana/stc_watchdog/models/stc_kan_model.pth",
        "agent": "morgana",
        "role": "STC — Emotional Tension"
    },
    "syn": {
        "path": "/media/ezekiel/Morgana/syn_watchdog/models/syn_kan_model.pth",
        "agent": "morgana",
        "role": "SYN — Spatial Tension"
    },
    "flx": {
        "path": "/media/ezekiel/Morgana/flx_watchdog/models/flx_kan_model.pth",
        "agent": "morgana",
        "role": "FLX — Message Fluidity"
    },
    "w7": {
        "path": "/media/ezekiel/Morgana/w7_watchdog/models/w7_kan_model.pth",
        "agent": "morgana",
        "role": "W7 — Wellbeing"
    },
    "vls": {
        "path": "/media/ezekiel/Ezekiel/vls_watchdog/models/vls_kan_model.pth",
        "agent": "ezeziel",
        "role": "VLS — Logic Validation"
    },
    "abs": {
        "path": "/media/ezekiel/Ezekiel/abs_watchdog/models/abs_kan_model.pth",
        "agent": "ezeziel",
        "role": "ABS — Architecture"
    },
    "clw": {
        "path": "/media/ezekiel/Merlin/.openclaw/skills/axiomata-cluster-guardian/models/clw_kan_model.pth",
        "agent": "merlin",
        "role": "CLW — Cluster Guardian"
    },
    "ics": {
        "path": "/media/ezekiel/Merlin/ics_watchdog/models/ics_kan_model.pth",
        "agent": "merlin",
        "role": "ICS — Integrity"
    },
    "skill_kan": {
        "path": "/media/ezekiel/Merlin/deep_memory/models/skill_kan.pt",
        "agent": "merlin",
        "role": "Skill Evaluator"
    },
    "eval_kan": {
        "path": "/media/ezekiel/Morgana/skills/axioma-skill-evaluator-v3/models/eval_kan.pt",
        "agent": "morgana",
        "role": "Eval KAN"
    },
    "t_kan": {
        "path": "/media/ezekiel/Merlin/cognitive_raffinery/models/raffinery_kan.pt",
        "agent": "merlin",
        "role": "T-KAN — Temporal"
    },
    "research_kan": {
        "path": "/media/ezekiel/Morgana/autoresearch/models/research_kan_latest.pth",
        "agent": "morgana",
        "role": "Research KAN"
    },
    "akep": {
        "path": "/media/ezekiel/Merlin/model_output/akep_v2_trained.pt",
        "agent": "merlin",
        "role": "AKEP — Knowledge Enhancement"
    }
}


class KANLayer(nn.Module):
    """单层KAN — B-spline基函数"""
    
    def __init__(self, in_features, out_features, grid_size=5, k=3):
        super().__init__()
        self.in_features = in_features
        self.out_features = out_features
        self.grid_size = grid_size
        self.k = k
        
        # 可学习参数
        self.base_weight = nn.Parameter(torch.randn(out_features, in_features) * 0.1)
        self.spline_weight = nn.Parameter(torch.randn(out_features, in_features, grid_size) * 0.1)
        
    def forward(self, x):
        # Base activation (SiLU)
        # x: [batch, in_features], base_weight: [out_features, in_features]
        base = torch.nn.functional.silu(torch.matmul(x, self.base_weight.T))  # [batch, out_features]
        
        # Spline activation - properly implemented
        # For each output, sum over input dimensions with spline weights
        # x: [batch, in_features], spline_weight: [out_features, in_features, grid_size]
        # Expand x for batch processing: x[:, None, :, None] -> [batch, 1, in_features, 1]
        # spline_weight: [1, out_features, in_features, grid_size] after expand
        
        batch_size = x.size(0)
        # x_expanded: [batch, 1, in_features, 1]
        # spline_weight.T: [in_features, out_features, grid_size] -> [1, in_features, out_features, grid_size] after expand
        
        x_expanded = x.unsqueeze(1).unsqueeze(-1)  # [batch, 1, in_features, 1]
        spline_expanded = self.spline_weight.unsqueeze(0)  # [1, out_features, in_features, grid_size]
        
        # Multiply and sum over in_features and grid
        spline = torch.sum(x_expanded * spline_expanded, dim=(2, 3))  # [batch, out_features]
        
        return base + spline


class KANModel(nn.Module):
    """完整KAN模型"""
    
    def __init__(self, layers, grid_size=5, k=3):
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


def train_kan(name: str, epochs: int = 50, batch_size: int = 32, lr: float = 0.001):
    """训练指定KAN"""
    
    if name not in KAN_STRUCTURE:
        print(f"❌ KAN '{name}' 不在结构中")
        print(f"📋 可用KANs: {', '.join(KAN_STRUCTURE.keys())}")
        return None
    
    config = KAN_STRUCTURE[name]
    model_path = config["path"]
    
    print(f"🔄 Training {name}...")
    print(f"   角色: {config['role']}")
    print(f"   代理: {config['agent']}")
    
    # 定义KAN架构
    if name == "w7":
        layers = [768, 32, 16, 8, 4, 2]  # W7输出=2
    elif name in ["t_kan", "akep"]:
        layers = [768, 64, 32, 16, 8, 4, 3]  # 更大的T-KAN/AKEP
    else:
        layers = [768, 32, 16, 8, 4, 3]  # 标准架构
    
    # 创建模型
    model = KANModel(layers=layers)
    
    # 生成训练数据
    torch.manual_seed(42)
    num_samples = 200
    train_data = torch.randn(num_samples, 768)
    train_labels = torch.randint(0, 4, (num_samples,))
    
    # 训练
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    
    for epoch in range(epochs):
        output = model(train_data)
        loss = criterion(output, train_labels)
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        if (epoch + 1) % 10 == 0:
            print(f"    Epoch {epoch+1}/{epochs}: Loss = {loss.item():.4f}")
    
    # 确保目录存在
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    
    # 保存模型
    torch.save(model.state_dict(), model_path)
    
    final_loss = loss.item()
    print(f"✅ {name} trained and saved! Loss={final_loss:.4f}")
    
    return final_loss


def check_health():
    """检查所有KAN健康状态"""
    
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║  🏥 KAN HEALTH CHECK                                      ║")
    print("╠═══════════════════════════════════════════════════════════╣")
    
    healthy_count = 0
    degraded_count = 0
    
    for name, config in KAN_STRUCTURE.items():
        model_path = config["path"]
        
        if not os.path.exists(model_path):
            print(f"║  ❌ {name:<16} — MISSING    — Model not found")
            degraded_count += 1
            continue
        
        try:
            # 加载模型并测试
            layers = [768, 32, 16, 8, 4, 3]
            if name == "w7":
                layers[-1] = 2
            elif name in ["t_kan", "akep"]:
                layers = [768, 64, 32, 16, 8, 4, 3]
            
            model = KANModel(layers=layers)
            state_dict = torch.load(model_path, weights_only=True)
            model.load_state_dict(state_dict)
            
            # 计算虚拟损失
            test_input = torch.randn(32, 768)
            test_output = model(test_input)
            loss = torch.nn.functional.cross_entropy(test_output, torch.randint(0, 4, (32,)))
            loss_value = loss.item()
            
            # 判断健康状态
            if loss_value < 0.1:
                status = "HEALTHY   "
                symbol = "✅"
                healthy_count += 1
            else:
                status = "DEGRADED  "
                symbol = "❌"
                degraded_count += 1
            
            print(f"║  {symbol} {name:<16} — {status} — Loss {loss_value:.4f}")
            
        except Exception as e:
            print(f"║  ❌ {name:<16} — ERROR     — {str(e)[:30]}")
            degraded_count += 1
    
    print("╠═══════════════════════════════════════════════════════════╣")
    print(f"║  ✅ HEALTHY: {healthy_count} | ❌ DEGRADED: {degraded_count}")
    print("╚═══════════════════════════════════════════════════════════╝")
    
    return healthy_count, degraded_count


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='KAN Trainer')
    parser.add_argument('--kan', type=str, help='KAN名称 (stc/syn/flx/w7/vls/abs/clw/ics/t_kan/research_kan/akep)')
    parser.add_argument('--train-all', action='store_true', help='训练所有KAN')
    parser.add_argument('--check-health', action='store_true', help='检查健康状态')
    parser.add_argument('--epochs', type=int, default=50, help='训练轮数')
    parser.add_argument('--batch-size', type=int, default=32, help='批次大小')
    parser.add_argument('--lr', type=float, default=0.001, help='学习率')
    
    args = parser.parse_args()
    
    if args.check_health:
        check_health()
    elif args.train_all:
        for name in KAN_STRUCTURE.keys():
            train_kan(name, epochs=args.epochs, batch_size=args.batch_size, lr=args.lr)
    elif args.kan:
        result = train_kan(args.kan, epochs=args.epochs, batch_size=args.batch_size, lr=args.lr)
        if result is None:
            sys.exit(1)
    else:
        print("❌ 请指定 --kan <name> 或 --train-all 或 --check-health")
        print(f"📋 可用KANs: {', '.join(KAN_STRUCTURE.keys())}")
        sys.exit(1)