#!/usr/bin/env python3
"""
企业 AI 助手一键部署脚本
用途：快速配置飞书 + OpenClaw 集成
"""

import os
import sys
import json
import argparse
from pathlib import Path

def check_dependencies():
    """检查依赖是否安装"""
    try:
        import lark
        print("✅ lark 已安装")
    except ImportError:
        print("❌ lark 未安装，正在安装...")
        os.system("pip install lark")

    try:
        import openclaw
        print("✅ openclaw 已安装")
    except ImportError:
        print("❌ openclaw 未安装，正在安装...")
        os.system("pip install openclaw")

def create_config(app_id, app_secret, model="deepseek-chat"):
    """创建配置文件"""
    config = {
        "feishu": {
            "app_id": app_id,
            "app_secret": app_secret,
            "encrypt_key": "",
            "verification_token": ""
        },
        "openclaw": {
            "model": model,
            "api_key": "${OPENCLAW_API_KEY}",
            "base_url": "https://api.openclaw.ai/v1"
        },
        "skills": [
            "smart-reply",
            "meeting-assistant",
            "approval-bot"
        ]
    }
    
    config_path = Path("config.json")
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ 配置文件已创建: {config_path}")
    return config_path

def create_skills_dir():
    """创建技能目录"""
    skills_dir = Path("skills")
    skills_dir.mkdir(exist_ok=True)
    
    # 智能回复技能
    smart_reply = {
        "name": "smart-reply",
        "description": "智能回复 - 自动回答常见问题",
        "triggers": ["@机器人"],
        "actions": [
            {"type": "llm", "prompt": "你是企业AI助手，用简洁专业的中文回答问题。"}
        ]
    }
    
    with open(skills_dir / "smart-reply.json", "w") as f:
        json.dump(smart_reply, f, indent=2, ensure_ascii=False)
    
    print(f"✅ 技能目录已创建: {skills_dir}")

def print_next_steps():
    """打印下一步指引"""
    print("""
╔════════════════════════════════════════════════════════════╗
║                 🎉 部署配置完成！                           ║
╠════════════════════════════════════════════════════════════╣
║  下一步：                                                  ║
║  1. 设置环境变量: export OPENCLAW_API_KEY=your_key        ║
║  2. 运行机器人: python bot.py                             ║
║  3. 在飞书群中 @机器人 测试                               ║
║                                                            ║
║  需要帮助？                                                ║
║  - 微信: OpenClawCN                                       ║
║  - Discord: https://discord.gg/clawd                      ║
╚════════════════════════════════════════════════════════════╝
""")

def main():
    parser = argparse.ArgumentParser(description="企业 AI 助手一键部署")
    parser.add_argument("--app-id", required=True, help="飞书应用 ID")
    parser.add_argument("--app-secret", required=True, help="飞书应用密钥")
    parser.add_argument("--model", default="deepseek-chat", help="AI 模型")
    args = parser.parse_args()
    
    print("🚀 开始部署企业 AI 助手...")
    
    check_dependencies()
    create_config(args.app_id, args.app_secret, args.model)
    create_skills_dir()
    print_next_steps()

if __name__ == "__main__":
    main()