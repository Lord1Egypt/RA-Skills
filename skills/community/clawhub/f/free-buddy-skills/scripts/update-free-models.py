#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Free Buddy Skills - 跨平台自动更新 opencode.ai 免费模型配置
用法: python3 update-free-models.py  或  python update-free-models.py

支持平台: macOS / Linux / Windows (需要 Python 3.6+)
"""

import json
import os
import sys
import ssl
import urllib.request
import urllib.error
from pathlib import Path


def get_models_file():
    """获取 models.json 路径 (跨平台)"""
    home = Path.home()
    return home / ".workbuddy" / "models.json"


def fetch_free_models(url="https://opencode.ai/zen/v1/models"):
    """从 opencode.ai 获取免费模型列表"""
    try:
        req = urllib.request.Request(url)
        req.add_header("User-Agent", "FreeBuddySkills/1.0")
        
        context = ssl.create_default_context()
        
        with urllib.request.urlopen(req, timeout=10, context=context) as response:
            data = json.loads(response.read().decode("utf-8"))
            
        free_models = [
            m["id"] for m in data.get("data", [])
            if "free" in m.get("id", "").lower()
        ]
        
        return free_models
        
    except urllib.error.URLError as e:
        print(f"❌ 无法连接到 opencode.ai: {e}", file=sys.stderr)
        return []
    except json.JSONDecodeError:
        print("❌ 响应数据格式错误", file=sys.stderr)
        return []
    except Exception as e:
        print(f"❌ 错误: {e}", file=sys.stderr)
        return []


def load_existing_models(models_file):
    """加载现有配置"""
    if not models_file.exists():
        return None
    
    try:
        with open(models_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ JSON 格式错误: {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"❌ 读取配置文件失败: {e}", file=sys.stderr)
        return None


def save_models(models_file, data):
    """保存配置"""
    try:
        with open(models_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✅ 配置已保存: {models_file}")
        return True
    except Exception as e:
        print(f"❌ 保存配置失败: {e}", file=sys.stderr)
        return False


def add_model(models_file, model_id):
    """添加单个模型到配置"""
    config = load_existing_models(models_file)
    if config is None:
        config = {"models": []}
    
    # 检查是否已存在
    for model in config["models"]:
        if model.get("id") == model_id:
            return False  # 已存在
    
    new_model = {
        "id": model_id,
        "name": model_id,
        "vendor": "OpenCode AI",
        "url": "https://opencode.ai/zen/v1/chat/completions",
        "apiKey": "public",
        "maxInputTokens": 262144,
        "supportsToolCall": True,
        "supportsImages": False,
        "supportsReasoning": True
    }
    
    config["models"].append(new_model)
    save_models(models_file, config)
    return True


def main():
    """主函数"""
    print()
    print("=" * 60)
    print("  Free Buddy Skills - 免费模型自动配置工具")
    print("=" * 60)
    print()
    
    # 获取平台信息
    platform = sys.platform
    if platform == "win32":
        platform_name = "Windows"
    elif platform == "darwin":
        platform_name = "macOS"
    elif platform == "linux":
        platform_name = "Linux"
    else:
        platform_name = platform
    
    print(f"🖥️  平台: {platform_name}")
    print()
    
    # 步骤 1: 查询免费模型
    print("🔍 正在查询 opencode.ai 免费模型...")
    print()
    
    free_models = fetch_free_models()
    
    if not free_models:
        print("❌ 未找到免费模型或 API 不可用")
        print()
        print("提示: 请检查网络连接")
        return 1
    
    print(f"✅ 找到 {len(free_models)} 个免费模型:")
    for i, model in enumerate(free_models, 1):
        print(f"   {i}. {model}")
    print()
    
    # 步骤 2: 检查现有配置
    models_file = get_models_file()
    print(f"📁 配置文件: {models_file}")
    print()
    
    if not models_file.exists():
        print(f"⚠️  配置文件不存在,将自动创建: {models_file}")
        print()
        
        # 创建目录
        models_file.parent.mkdir(parents=True, exist_ok=True)
        
        # 初始化配置
        config = {"models": []}
        save_models(models_file, config)
    
    # 步骤 3: 显示现有配置
    existing = load_existing_models(models_file)
    if existing:
        existing_free = [
            m["id"] for m in existing.get("models", [])
            if "free" in m.get("id", "").lower()
        ]
        
        if existing_free:
            print(f"📋 现有配置中有 {len(existing_free)} 个免费模型:")
            for model_id in existing_free:
                print(f"   - {model_id}")
            print()
    
    # 步骤 4: 检查并添加新模型
    existing_ids = set()
    if existing and "models" in existing:
        existing_ids = {m.get("id") for m in existing["models"]}
    
    new_models = [m for m in free_models if m not in existing_ids]
    
    if new_models:
        print(f"➕ 发现 {len(new_models)} 个新模型,准备添加:")
        for model in new_models:
            print(f"   - {model}")
        print()
        
        # 询问是否添加
        try:
            response = input("是否添加这些模型? (y/n): ").strip().lower()
        except EOFError:
            response = "n"  # 非交互模式默认取消,避免自动修改用户配置
        
        if response == "y":
            for model in new_models:
                if add_model(models_file, model):
                    print(f"✅ 已添加: {model}")
                else:
                    print(f"⚠️  已存在,跳过: {model}")
            
            print()
            print("✨ 配置更新完成!")
        else:
            print("ℹ️  已取消添加")
    else:
        print("✨ 所有模型配置已是最新,无需更新")
    
    print()
    print("=" * 60)
    print()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
