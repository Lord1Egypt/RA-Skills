#!/usr/bin/env python3
"""
KAN Health — 检查KAN健康状态
Morgana守护者 — 精神(Shén) + 爱(Ài)
"""

import os
import sys
import json
import argparse
import torch
import torch.nn as nn

# KAN结构配置
KAN_STRUCTURE = {
    "stc": {"path": "/media/ezekiel/Morgana/stc_watchdog/models/stc_kan_model.pth", "agent": "morgana", "role": "STC — Emotional Tension"},
    "syn": {"path": "/media/ezekiel/Morgana/syn_watchdog/models/syn_kan_model.pth", "agent": "morgana", "role": "SYN — Spatial/Environmental"},
    "flx": {"path": "/media/ezekiel/Morgana/flx_watchdog/models/flx_kan_model.pth", "agent": "morgana", "role": "FLX — Message Fluidity"},
    "w7": {"path": "/media/ezekiel/Morgana/w7_watchdog/models/w7_kan_model.pth", "agent": "morgana", "role": "W7 — Wellbeing"},
    "vls": {"path": "/media/ezekiel/Ezekiel/vls_watchdog/models/vls_kan_model.pth", "agent": "ezeziel", "role": "VLS — Logic Validation"},
    "abs": {"path": "/media/ezekiel/Ezekiel/abs_watchdog/models/abs_kan_model.pth", "agent": "ezeziel", "role": "ABS — Architecture"},
    "clw": {"path": "/media/ezekiel/Merlin/.openclaw/skills/axiomata-cluster-guardian/models/clw_kan_model.pth", "agent": "merlin", "role": "CLW — Cluster Guardian"},
    "ics": {"path": "/media/ezekiel/Merlin/ics_watchdog/models/ics_kan_model.pth", "agent": "merlin", "role": "ICS — Integrity"},
    "skill_kan": {"path": "/media/ezekiel/Merlin/deep_memory/models/skill_kan.pt", "agent": "merlin", "role": "SKILL — Skill Evaluator"},
    "eval_kan": {"path": "/media/ezekiel/Morgana/skills/axioma-skill-evaluator-v3/models/eval_kan.pt", "agent": "morgana", "role": "EVAL — Eval KAN"},
    "t_kan": {"path": "/media/ezekiel/Merlin/cognitive_raffinery/models/raffinery_kan.pt", "agent": "merlin", "role": "T-KAN — Temporal"},
    "research_kan": {"path": "/media/ezekiel/Morgana/autoresearch/models/research_kan_latest.pth", "agent": "morgana", "role": "RESEARCH — AutoResearch"},
    "akep": {"path": "/media/ezekiel/Merlin/model_output/akep_v2_trained.pt", "agent": "merlin", "role": "AKEP — Knowledge Enhancement"},
}


class KANLayer(nn.Module):
    """单层KAN — B-spline基函数"""
    def __init__(self, in_features, out_features, grid_size=5, k=3):
        super().__init__()
        self.in_features = in_features
        self.out_features = out_features
        self.grid_size = grid_size
        self.k = k
        self.base_weight = nn.Parameter(torch.randn(out_features, in_features) * 0.1)
        self.spline_weight = nn.Parameter(torch.randn(out_features, in_features, grid_size) * 0.1)
        
    def forward(self, x):
        base = torch.nn.functional.silu(torch.matmul(x, self.base_weight.T))
        spline = torch.matmul(x, self.spline_weight.unsqueeze(0).expand(x.size(0), -1, -1))
        spline = torch.sum(spline, dim=-1)
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


def check_kan_health(name: str, verbose: bool = False):
    """检查指定KAN的健康状态"""
    
    if name not in KAN_STRUCTURE:
        print(f"❌ KAN '{name}' 不在结构中")
        return None
    
    config = KAN_STRUCTURE[name]
    model_path = config["path"]
    
    if not os.path.exists(model_path):
        if verbose:
            print(f"❌ {name}: 模型文件不存在 — {model_path}")
        return None
    
    try:
        # 确定layers配置
        if name == "w7":
            layers = [768, 32, 16, 8, 4, 2]
        elif name in ["t_kan", "akep"]:
            layers = [768, 64, 32, 16, 8, 4, 3]
        else:
            layers = [768, 32, 16, 8, 4, 3]
        
        # 创建模型
        model = KANModel(layers=layers)
        
        # 加载权重 - 处理不同的格式
        state_dict = torch.load(model_path, weights_only=True)
        
        # 处理嵌套的state_dict (某些模型保存格式)
        if "model_state_dict" in state_dict:
            state_dict = state_dict["model_state_dict"]
        
        model.load_state_dict(state_dict)
        model.eval()
        
        # 计算虚拟损失
        torch.manual_seed(42)
        test_input = torch.randn(32, 768)
        
        with torch.no_grad():
            test_output = model(test_input)
        
        # 使用随机标签计算损失
        num_classes = layers[-1] if layers[-1] <= 10 else 4
        test_labels = torch.randint(0, num_classes, (32,))
        loss = nn.CrossEntropyLoss()(test_output, test_labels)
        loss_value = loss.item()
        
        # 判断健康状态
        if loss_value < 0.1:
            status = "HEALTHY"
            symbol = "✅"
        elif loss_value < 0.3:
            status = "WATCH"
            symbol = "🟡"
        elif loss_value < 0.5:
            status = "DEGRADED"
            symbol = "🟠"
        else:
            status = "CRITICAL"
            symbol = "🔴"
        
        if verbose:
            print(f"{symbol} {name}: Loss={loss_value:.4f} | Status={status} | Agent={config['agent']}")
        
        return {
            "name": name,
            "loss": loss_value,
            "status": status,
            "agent": config["agent"],
            "role": config["role"],
            "path": model_path
        }
        
    except Exception as e:
        if verbose:
            print(f"❌ {name}: ERROR — {str(e)[:50]}")
        return None


def check_all_health():
    """检查所有KAN健康状态"""
    
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║  🏥 KAN HEALTH CHECK                                      ║")
    print("╠═══════════════════════════════════════════════════════════╣")
    
    results = []
    for name in KAN_STRUCTURE.keys():
        result = check_kan_health(name, verbose=False)
        if result:
            results.append(result)
            # Color by status
            if result["loss"] < 0.1:
                symbol = "✅"
            elif result["loss"] < 0.3:
                symbol = "🟡"
            elif result["loss"] < 0.5:
                symbol = "🟠"
            else:
                symbol = "🔴"
            
            print(f"║  {symbol} {result['name']:<16} — {result['status']:<10} — Loss {result['loss']:.4f} [{result['agent']}]")
    
    # Summary
    healthy = sum(1 for r in results if r["loss"] < 0.1)
    watch = sum(1 for r in results if 0.1 <= r["loss"] < 0.3)
    degraded = sum(1 for r in results if r["loss"] >= 0.3)
    
    print("╠═══════════════════════════════════════════════════════════╣")
    print(f"║  ✅ HEALTHY: {healthy} | 🟡 WATCH: {watch} | 🟠 DEGRADED: {degraded}")
    print("╚═══════════════════════════════════════════════════════════╝")
    
    return results


def get_recommendations():
    """获取KAN健康建议"""
    
    results = check_all_health()
    recommendations = []
    
    for r in results:
        if r["loss"] >= 0.1:
            recommendations.append({
                "kan": r["name"],
                "action": "retrain",
                "command": f"python3 /media/ezekiel/Axioma Projects/Morgana-Projects/autoresearch/kan_auto_task.py --train {r['name']}",
                "priority": "HIGH" if r["loss"] >= 0.3 else "MEDIUM"
            })
    
    return recommendations


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='KAN Health Check')
    parser.add_argument('--kan', type=str, help='KAN名称')
    parser.add_argument('--all', action='store_true', help='检查所有KAN')
    parser.add_argument('--verbose', action='store_true', help='详细输出')
    parser.add_argument('--recommendations', action='store_true', help='显示建议')
    
    args = parser.parse_args()
    
    if args.all or (not args.kan and not args.recommendations):
        check_all_health()
    elif args.kan:
        result = check_kan_health(args.kan, verbose=args.verbose)
        if result is None:
            sys.exit(1)
    elif args.recommendations:
        recs = get_recommendations()
        if not recs:
            print("✅ 所有KAN都健康，无需建议")
        else:
            print("╔═══════════════════════════════════════════════════════════╗")
            print("║  💡 KAN HEALTH RECOMMENDATIONS                            ║")
            print("╠═══════════════════════════════════════════════════════════╣")
            for rec in recs:
                print(f"║  🟠 {rec['kan']}: {rec['command']}")
            print("╚═══════════════════════════════════════════════════════════╝")
    else:
        print("❌ 请指定 --kan <name> 或 --all")
        sys.exit(1)