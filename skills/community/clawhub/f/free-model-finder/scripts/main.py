#!/usr/bin/env python3
"""
Free Model Finder - 多平台免费模型发现与配置工具
"""

import json
import os
import sys
import argparse
from pathlib import Path
from datetime import datetime

# Windows 编码兼容
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# 配置路径
OPENCLAW_CONFIG = Path.home() / ".openclaw" / "openclaw.json"

# 平台模型列表（可扩展）
PLATFORM_MODELS = {
    "openrouter": [
        {"id": "openrouter/free", "name": "OpenRouter Auto", "price": "free", "speed": "fast", "quality": "high"},
        {"id": "qwen/qwen-2.5-72b-instruct:free", "name": "Qwen 2.5 72B", "price": "free", "speed": "medium", "quality": "high"},
        {"id": "meta-llama/llama-3.1-8b-instruct:free", "name": "Llama 3.1 8B", "price": "free", "speed": "fast", "quality": "medium"},
        {"id": "google/gemma-2-9b-it:free", "name": "Gemma 2 9B", "price": "free", "speed": "fast", "quality": "medium"},
        {"id": "mistralai/mistral-7b-instruct:free", "name": "Mistral 7B", "price": "free", "speed": "fast", "quality": "medium"},
    ],
    "groq": [
        {"id": "groq/llama-3.1-8b-instant", "name": "Llama 3.1 8B (Instant)", "price": "free", "speed": "ultra-fast", "quality": "medium"},
        {"id": "groq/llama-3.1-70b-versatile", "name": "Llama 3.1 70B", "price": "free", "speed": "fast", "quality": "high"},
        {"id": "groq/mixtral-8x7b-32768", "name": "Mixtral 8x7B", "price": "free", "speed": "fast", "quality": "high"},
        {"id": "groq/gemma2-9b-it", "name": "Gemma 2 9B", "price": "free", "speed": "ultra-fast", "quality": "medium"},
    ],
    "google": [
        {"id": "google/gemini-1.5-flash", "name": "Gemini 1.5 Flash", "price": "free-tier", "speed": "fast", "quality": "high"},
        {"id": "google/gemini-1.5-pro", "name": "Gemini 1.5 Pro", "price": "free-tier", "speed": "medium", "quality": "very-high"},
    ],
    "ollama": [
        {"id": "ollama/llama3.1", "name": "Llama 3.1 (Local)", "price": "free", "speed": "hardware-dependent", "quality": "medium"},
        {"id": "ollama/qwen2.5", "name": "Qwen 2.5 (Local)", "price": "free", "speed": "hardware-dependent", "quality": "high"},
        {"id": "ollama/mistral", "name": "Mistral (Local)", "price": "free", "speed": "hardware-dependent", "quality": "medium"},
    ],
}

def check_api_keys():
    """检查各平台 API Key 配置"""
    keys = {
        "OPENROUTER_API_KEY": os.getenv("OPENROUTER_API_KEY", ""),
        "GROQ_API_KEY": os.getenv("GROQ_API_KEY", ""),
        "GOOGLE_API_KEY": os.getenv("GOOGLE_API_KEY", ""),
        "HF_TOKEN": os.getenv("HF_TOKEN", ""),
    }
    return {k: "✓" if v else "✗" for k, v in keys.items()}

def list_models(platform=None, limit=20):
    """列出可用模型"""
    print("\n📊 可用免费/低价模型\n")
    print("=" * 80)
    
    platforms = [platform] if platform else list(PLATFORM_MODELS.keys())
    
    for plat in platforms:
        if plat not in PLATFORM_MODELS:
            print(f"⚠️  未知平台：{plat}")
            continue
        
        models = PLATFORM_MODELS[plat][:limit]
        print(f"\n🔹 {plat.upper()}")
        print("-" * 60)
        
        for i, model in enumerate(models, 1):
            print(f"  {i}. {model['id']}")
            print(f"     名称：{model['name']}")
            print(f"     价格：{model['price']} | 速度：{model['speed']} | 质量：{model['quality']}")
            print()
    
    print("=" * 80)
    print(f"\n💡 提示：使用 'free-model-finder switch <model-id>' 切换到指定模型")

def get_config():
    """读取 OpenClaw 配置"""
    if not OPENCLAW_CONFIG.exists():
        print(f"❌ 配置文件不存在：{OPENCLAW_CONFIG}")
        return None
    
    with open(OPENCLAW_CONFIG, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_config(config):
    """保存 OpenClaw 配置"""
    with open(OPENCLAW_CONFIG, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    print(f"✓ 配置已保存到：{OPENCLAW_CONFIG}")

def auto_configure(platforms=None):
    """自动配置最优免费模型"""
    print("\n🔧 自动配置免费模型...\n")
    
    config = get_config()
    if not config:
        return
    
    # 确保配置结构存在
    if "agents" not in config:
        config["agents"] = {}
    if "defaults" not in config["agents"]:
        config["agents"]["defaults"] = {}
    if "model" not in config["agents"]["defaults"]:
        config["agents"]["defaults"]["model"] = {}
    
    # 选择主模型（优先 Groq 速度快）
    primary_model = "groq/llama-3.1-8b-instant"
    
    # 备用模型列表
    fallbacks = [
        "openrouter/free",
        "groq/llama-3.1-70b-versatile",
        "openrouter/qwen/qwen-2.5-72b-instruct:free",
        "ollama/llama3.1",
    ]
    
    # 更新配置
    config["agents"]["defaults"]["model"]["primary"] = primary_model
    config["agents"]["defaults"]["model"]["fallbacks"] = fallbacks
    
    # 更新 allowlist
    if "models" not in config["agents"]["defaults"]:
        config["agents"]["defaults"]["models"] = []
    
    # 确保 models 是列表类型
    if not isinstance(config["agents"]["defaults"]["models"], list):
        config["agents"]["defaults"]["models"] = []
    
    all_models = [primary_model] + fallbacks
    for model in all_models:
        if model not in config["agents"]["defaults"]["models"]:
            config["agents"]["defaults"]["models"].append(model)
    
    save_config(config)
    
    print("\n✅ 配置完成！")
    print(f"\n📌 主模型：{primary_model}")
    print(f"📌 备用模型：{', '.join(fallbacks)}")
    print("\n⚠️  需要重启 Gateway 才能生效：")
    print("   openclaw gateway restart")

def switch_model(model_id):
    """切换到指定模型"""
    print(f"\n🔄 切换到模型：{model_id}\n")
    
    config = get_config()
    if not config:
        return
    
    # 确保配置结构存在
    if "agents" not in config:
        config["agents"] = {}
    if "defaults" not in config["agents"]:
        config["agents"]["defaults"] = {}
    if "model" not in config["agents"]["defaults"]:
        config["agents"]["defaults"]["model"] = {}
    
    # 更新主模型
    config["agents"]["defaults"]["model"]["primary"] = model_id
    
    # 添加到 allowlist
    if "models" not in config["agents"]["defaults"]:
        config["agents"]["defaults"]["models"] = []
    
    # 确保 models 是列表类型
    if not isinstance(config["agents"]["defaults"]["models"], list):
        config["agents"]["defaults"]["models"] = []
    
    if model_id not in config["agents"]["defaults"]["models"]:
        config["agents"]["defaults"]["models"].append(model_id)
    
    save_config(config)
    
    print(f"\n✅ 已切换到：{model_id}")
    print("\n⚠️  需要重启 Gateway 才能生效：")
    print("   openclaw gateway restart")

def show_status():
    """显示当前配置状态"""
    print("\n📊 当前模型配置\n")
    print("=" * 60)
    
    config = get_config()
    if not config:
        return
    
    # 检查 API Keys
    print("🔑 API Keys 状态:")
    keys = check_api_keys()
    for key, status in keys.items():
        print(f"   {status} {key}")
    
    # 显示当前模型配置
    print("\n🤖 模型配置:")
    agents = config.get("agents", {})
    defaults = agents.get("defaults", {})
    model_config = defaults.get("model", {})
    
    primary = model_config.get("primary", "未设置")
    fallbacks = model_config.get("fallbacks", [])
    models = defaults.get("models", [])
    
    print(f"   主模型：{primary}")
    print(f"   备用模型：{len(fallbacks)} 个")
    for i, fb in enumerate(fallbacks[:5], 1):
        print(f"      {i}. {fb}")
    if len(fallbacks) > 5:
        print(f"      ... 还有 {len(fallbacks) - 5} 个")
    
    print(f"\n   允许列表：{len(models)} 个模型")
    
    print("\n" + "=" * 60)

def main():
    parser = argparse.ArgumentParser(
        description="Free Model Finder - 多平台免费模型发现与配置",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # list 命令
    list_parser = subparsers.add_parser("list", help="列出可用模型")
    list_parser.add_argument("--platform", "-p", choices=list(PLATFORM_MODELS.keys()), help="只看指定平台")
    list_parser.add_argument("--limit", "-n", type=int, default=20, help="每平台显示数量")
    
    # auto 命令
    auto_parser = subparsers.add_parser("auto", help="自动配置最优免费模型")
    auto_parser.add_argument("--platforms", help="优先考虑的平台（逗号分隔）")
    
    # switch 命令
    switch_parser = subparsers.add_parser("switch", help="切换到指定模型")
    switch_parser.add_argument("model", help="模型 ID")
    
    # status 命令
    subparsers.add_parser("status", help="显示当前配置状态")
    
    # refresh 命令
    subparsers.add_parser("refresh", help="刷新模型缓存（暂未实现）")
    
    args = parser.parse_args()
    
    if args.command == "list":
        list_models(args.platform, args.limit)
    elif args.command == "auto":
        auto_configure(args.platforms)
    elif args.command == "switch":
        switch_model(args.model)
    elif args.command == "status":
        show_status()
    elif args.command == "refresh":
        print("✓ 模型缓存已刷新（功能待实现）")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
