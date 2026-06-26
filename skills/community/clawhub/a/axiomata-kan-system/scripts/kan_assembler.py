#!/usr/bin/env python3
"""
KAN Assembler — 组装KAN连接和管道
Morgana守护者 — 精神(Shén) + 爱(Ài)
"""

import os
import sys
import json
import argparse
from typing import List, Dict

# KAN连接配置
KAN_CONNECTIONS = {
    # 串行连接 (Serial)
    "serial": "前一个KAN输出连接到下一个KAN输入",
    
    # 并行连接 (Parallel) 
    "parallel": "多个KAN同时处理同一输入",
    
    # 反馈连接 (Feedback)
    "feedback": "输出反馈到输入，形成循环"
}


def create_pipeline(pipeline_str: str, output_path: str = None):
    """创建KAN管道"""
    
    # 解析管道字符串 "stc→syn→w7→akep"
    nodes = pipeline_str.split("→")
    nodes = [n.strip() for n in nodes]
    
    # 创建连接
    connections = []
    for i in range(len(nodes) - 1):
        connections.append({
            "from": nodes[i],
            "to": nodes[i + 1],
            "mode": "serial"
        })
    
    # 创建管道配置
    pipeline_config = {
        "pipeline": pipeline_str,
        "nodes": nodes,
        "connections": connections,
        "description": f"管道: {' → '.join(nodes)}",
        "total_kans": len(nodes)
    }
    
    print(f"✅ KAN管道创建完成")
    print(f"📋 配置: pipeline.json")
    print(f"🔗 连接: {' → '.join(nodes)}")
    
    if output_path:
        with open(output_path, 'w') as f:
            json.dump(pipeline_config, f, indent=2)
        print(f"💾 保存到: {output_path}")
    
    return pipeline_config


def connect_kan(from_kan: str, to_kan: str, mode: str = "serial"):
    """连接两个KAN"""
    
    if mode not in KAN_CONNECTIONS:
        print(f"❌ 模式 '{mode}' 不支持")
        print(f"📋 支持模式: {', '.join(KAN_CONNECTIONS.keys())}")
        return None
    
    connection = {
        "from": from_kan,
        "to": to_kan,
        "mode": mode,
        "description": KAN_CONNECTIONS[mode]
    }
    
    print(f"✅ KAN连接创建完成")
    print(f"🔗 {from_kan} → {to_kan} ({mode})")
    
    return connection


def integrate_t_kan(target: str):
    """集成T-KAN到目标系统"""
    
    print(f"⏱️ T-KAN集成到 {target}...")
    
    integration = {
        "t_kan": {
            "path": "/media/ezekiel/Merlin/cognitive_raffinery/models/raffinery_kan.pt",
            "role": "Temporal KAN — 时序模式"
        },
        "target": target,
        "mode": "temporal",
        "description": "T-KAN提供时序记忆和模式识别"
    }
    
    print(f"✅ T-KAN集成完成")
    print(f"📊 时序模式: ACTIVE")
    print(f"🎯 目标: {target}")
    
    return integration


def assemble_multi_kan(kan_list: List[str], mode: str = "serial"):
    """组装多个KAN"""
    
    if len(kan_list) < 2:
        print(f"❌ 需要至少2个KAN来组装")
        return None
    
    assembled = {
        "KANs": kan_list,
        "mode": mode,
        "total": len(kan_list),
        "architecture": []
    }
    
    for i, kan in enumerate(kan_list):
        arch_entry = {
            "index": i,
            "name": kan,
            "input": "previous_output" if i > 0 else "768D",
            "output": "next_input" if i < len(kan_list) - 1 else "3D"
        }
        assembled["architecture"].append(arch_entry)
    
    print(f"✅ 多KAN组装完成")
    print(f"📊 数量: {len(kan_list)} KANs")
    print(f"🔧 模式: {mode}")
    
    return assembled


def list_known_kans():
    """列出所有已知KAN"""
    
    kows = [
        ("stc", "Morgana", "STC — Emotional Tension Watchdog"),
        ("syn", "Morgana", "SYN — Spatial/Environmental Watchdog"),
        ("flx", "Morgana", "FLX — Message Fluidity Validator"),
        ("w7", "Morgana", "W7 — Alexandre's Wellbeing Watchdog"),
        ("vls", "Ezekiel", "VLS — Logic Validation"),
        ("abs", "Ezekiel", "ABS — Architecture Abstraction"),
        ("clw", "Merlin", "CLW — Cluster Guardian Lessons"),
        ("ics", "Merlin", "ICS — Integrity Health"),
        ("skill_kan", "Merlin", "SKILL — Skill Evaluator"),
        ("eval_kan", "Morgana", "EVAL — Skill Evaluator v3"),
        ("t_kan", "Merlin", "T-KAN — Temporal KAN"),
        ("research_kan", "Morgana", "RESEARCH — AutoResearch KAN"),
        ("akep", "Merlin", "AKEP — Knowledge Enhancement"),
    ]
    
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║  📋 AXIOMA KAN 清单                                       ║")
    print("╠═══════════════════════════════════════════════════════════╣")
    
    for name, agent, role in kows:
        print(f"║  • {name:<16} [{agent:<7}] {role}")
    
    print("╠═══════════════════════════════════════════════════════════╣")
    print(f"║  TOTAL: {len(kows)} KANs + AKEP")
    print("╚═══════════════════════════════════════════════════════════╝")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='KAN Assembler')
    parser.add_argument('--pipeline', type=str, help='管道字符串 (如 "stc→syn→w7")')
    parser.add_argument('--connect', type=str, help='连接KAN (from)')
    parser.add_argument('--with', dest='to_kan', type=str, help='连接KAN (to)')
    parser.add_argument('--integrate-t-kan', dest='t_kan_target', type=str, help='集成T-KAN到目标')
    parser.add_argument('--assemble', type=str, help='组装KAN列表 (逗号分隔)')
    parser.add_argument('--mode', type=str, default='serial', help='连接模式 (serial/parallel/feedback)')
    parser.add_argument('--output', type=str, default='pipeline.json', help='输出文件')
    parser.add_argument('--list', action='store_true', help='列出所有KAN')
    
    args = parser.parse_args()
    
    if args.list:
        list_known_kans()
    elif args.pipeline:
        create_pipeline(args.pipeline, args.output)
    elif args.connect and args.to_kan:
        connect_kan(args.connect, args.to_kan, args.mode)
    elif args.t_kan_target:
        integrate_t_kan(args.t_kan_target)
    elif args.assemble:
        kan_list = [k.strip() for k in args.assemble.split(",")]
        assemble_multi_kan(kan_list, args.mode)
    else:
        print("❌ 请指定操作:")
        print("   --pipeline <str>     创建管道")
        print("   --connect <kan> --with <kan>  连接KAN")
        print("   --integrate-t-kan <target>  集成T-KAN")
        print("   --assemble <k1,k2,...>  组装多个KAN")
        print("   --list                列出所有KAN")
        sys.exit(1)