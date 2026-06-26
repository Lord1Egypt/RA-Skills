#!/usr/bin/env python3
"""Beauty Image 技能健康检查"""
import sys
import os
import json
from pathlib import Path

# 自动定位skill根目录 (scripts/../)
base_dir = Path(__file__).resolve().parent.parent

# 检查脚本是否存在
for script_name in ["generate_image.py", "generate_image_v2.py", "generate_image_v3.py"]:
    script_path = base_dir / "scripts" / script_name
    if script_path.exists():
        print(f"✅ {script_name}")
    else:
        print(f"❌ {script_name} 不存在：{script_path}")

# 检查 SKILL.md
skill_md = base_dir / "SKILL.md"
if not skill_md.exists():
    print(f"❌ SKILL.md 不存在：{skill_md}")
    sys.exit(1)
else:
    print("✅ SKILL.md")

# 检查 API Key 配置
print("\n--- API Key 检查 ---")

dashscope_key = os.environ.get('DASHSCOPE_API_KEY', '')
if dashscope_key:
    print("✅ DASHSCOPE_API_KEY 已配置 (通义万相)")
else:
    print("⚠️ DASHSCOPE_API_KEY 未设置")
    print("   获取地址: https://dashscope.console.aliyun.com/apiKey")

ark_key = os.environ.get('ARK_API_KEY', '') or os.environ.get('VOLC_API_KEY', '')
if ark_key:
    print("✅ ARK_API_KEY 已配置 (Seedream)")
else:
    print("⚠️ ARK_API_KEY 未设置 (Seedream引擎不可用)")
    print("   获取地址: https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey")

deepseek_key = os.environ.get('DEEPSEEK_API_KEY', '')
if deepseek_key:
    print("✅ DEEPSEEK_API_KEY 已配置 (LLM意图解析)")
else:
    print("ℹ️ DEEPSEEK_API_KEY 未设置 (可选, 用于--use-llm深度意图解析)")

# 检查 openclaw.json 配置
config_path = Path.home() / ".openclaw" / "openclaw.json"
if config_path.exists():
    try:
        with open(config_path) as f:
            config = json.load(f)
        providers = config.get("models", {}).get("providers", {})
        if providers.get("wanxiang", {}).get("apiKey"):
            print("✅ openclaw.json: wanxiang provider 已配置")
        for name in ["ark", "volcengine", "doubao"]:
            if providers.get(name, {}).get("apiKey"):
                print(f"✅ openclaw.json: {name} provider 已配置")
                break
    except Exception:
        pass

if not dashscope_key and not ark_key:
    print("\n⚠️ 至少需要配置一个 API Key 才能使用图片生成功能")
    print("   推荐: 设置 DASHSCOPE_API_KEY (免费额度较多)")
else:
    print("\n✅ OK - beauty-image 就绪")

print("   支持的引擎: wanx (万相), seedream4, seedream5")
print("   支持的模型: wan2.6-t2i, wan2.5-t2i-preview, doubao-seedream-4/5")
