#!/usr/bin/env python3
"""
检查 OpenClaw 配置中的 SlonAide 设置
"""

import os
import json
import sys

def check_openclaw_config():
    """检查 OpenClaw 配置"""
    config_paths = [
        os.path.expanduser("~/.openclaw/openclaw.json"),
        os.path.expanduser("~/.openclaw/config.json"),
        "/etc/openclaw/config.json"
    ]
    
    config_found = False
    config_data = None
    
    for path in config_paths:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                    config_found = True
                    print(f"✅ 找到配置文件: {path}")
                    break
            except Exception as e:
                print(f"⚠️ 读取配置文件失败 {path}: {e}")
    
    if not config_found:
        print("❌ 未找到 OpenClaw 配置文件")
        return None
    
    return config_data

def check_slonaide_config(config_data):
    """检查 SlonAide 配置"""
    print("\n" + "=" * 60)
    print("检查 SlonAide 配置")
    print("=" * 60)
    
    # 检查插件配置
    plugins = config_data.get('plugins', {}).get('entries', {})
    slonaide_config = plugins.get('slonaide', {})
    
    if not slonaide_config:
        print("❌ 未找到 SlonAide 插件配置")
        return False
    
    enabled = slonaide_config.get('enabled', False)
    config = slonaide_config.get('config', {})
    api_key = config.get('apiKey')
    base_url = config.get('baseUrl', 'https://api.aidenote.cn')
    
    print(f"插件状态: {'✅ 已启用' if enabled else '❌ 未启用'}")
    print(f"API Key: {'✅ 已配置' if api_key else '❌ 未配置'}")
    print(f"Base URL: {base_url}")
    
    if api_key:
        # 检查 API Key 格式
        if api_key.startswith('sk-'):
            print(f"API Key 格式: ✅ 正确 (以 'sk-' 开头)")
        else:
            print(f"API Key 格式: ⚠️ 可能不正确 (应以 'sk-' 开头)")
        
        # 显示部分信息（保护隐私）
        if len(api_key) > 10:
            masked_key = f"{api_key[:10]}...{api_key[-4:]}"
            print(f"API Key (脱敏): {masked_key}")
    
    # 检查技能配置（旧版本可能在这里）
    skills = config_data.get('skills', {}).get('entries', {})
    old_slonaide_config = skills.get('slonaide', {})
    
    if old_slonaide_config:
        print("\n⚠️ 发现旧版技能配置 (skills.entries.slonaide):")
        print("建议迁移到新版插件配置 (plugins.entries.slonaide)")
    
    return bool(api_key)

def check_environment():
    """检查环境变量"""
    print("\n" + "=" * 60)
    print("检查环境变量")
    print("=" * 60)
    
    env_vars = ['SLONAIDE_API_KEY', 'OPENCLAW_SLONAIDE_API_KEY']
    found_vars = []
    
    for var in env_vars:
        value = os.environ.get(var)
        if value:
            found_vars.append((var, value))
    
    if found_vars:
        print("✅ 找到环境变量:")
        for var, value in found_vars:
            if len(value) > 10:
                masked = f"{value[:10]}...{value[-4:]}"
                print(f"  {var}: {masked}")
            else:
                print(f"  {var}: {value}")
    else:
        print("ℹ️ 未找到相关环境变量")
    
    return len(found_vars) > 0

def generate_config_example():
    """生成配置示例"""
    print("\n" + "=" * 60)
    print("配置示例")
    print("=" * 60)
    
    example = {
        "plugins": {
            "entries": {
                "slonaide": {
                    "enabled": True,
                    "config": {
                        "apiKey": "sk-你的API密钥",
                        "baseUrl": "https://api.aidenote.cn"
                    }
                }
            }
        }
    }
    
    print("在 ~/.openclaw/openclaw.json 中添加:")
    print(json.dumps(example, indent=2, ensure_ascii=False))
    
    print("\n配置命令:")
    print('openclaw config set slonaide.apiKey "sk-你的API密钥"')
    print('openclaw config set slonaide.baseUrl "https://api.aidenote.cn"')
    print('openclaw config set slonaide.enabled true')

def main():
    print("🔍 SlonAide 配置检查工具")
    print("版本: 2.0.0")
    print()
    
    # 检查配置
    config_data = check_openclaw_config()
    
    if config_data:
        config_ok = check_slonaide_config(config_data)
        env_ok = check_environment()
        
        print("\n" + "=" * 60)
        print("检查结果")
        print("=" * 60)
        
        if config_ok:
            print("✅ SlonAide 配置正确")
            print("\n下一步:")
            print("1. 重启 OpenClaw: openclaw gateway restart")
            print("2. 测试连接: 在 OpenClaw 中使用 'slonaide_test_connection'")
        else:
            print("❌ SlonAide 配置不完整")
            generate_config_example()
    else:
        generate_config_example()
    
    print("\n💡 提示:")
    print("• 获取 API Key: 访问 https://h5.slonaide.cn/")
    print("• 详细文档: 查看 SKILL.md")
    print("• 问题反馈: GitHub Issues")

if __name__ == "__main__":
    main()