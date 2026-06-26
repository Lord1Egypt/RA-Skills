#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置管理工具 - 检查、备份、恢复和迁移配置

功能：
1. 检查配置是否存在
2. 自动备份现有配置
3. 从其他来源恢复配置（环境变量、多维表格等）
4. 新用户引导创建配置
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime

SKILL_DIR = Path(__file__).parent.parent
CONFIG_FILE = SKILL_DIR / "config.json"
CONFIG_BACKUP = SKILL_DIR / ".config.backup.json"
ENV_FILE = SKILL_DIR / ".env"


def print_header(text: str):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")


def print_success(text: str):
    print(f"✅ {text}")


def print_warning(text: str):
    print(f"⚠️  {text}")


def print_error(text: str):
    print(f"❌ {text}")


def load_existing_config() -> dict:
    """加载现有配置（如果有）"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def backup_config():
    """备份现有配置"""
    if CONFIG_FILE.exists():
        import shutil
        shutil.copy2(CONFIG_FILE, CONFIG_BACKUP)
        print_success(f"配置已备份：{CONFIG_BACKUP}")
        return True
    return False


def restore_config():
    """从备份恢复配置"""
    if CONFIG_BACKUP.exists():
        import shutil
        shutil.copy2(CONFIG_BACKUP, CONFIG_FILE)
        print_success(f"配置已恢复：{CONFIG_FILE}")
        return True
    return False


def check_env_config() -> dict:
    """从环境变量读取配置"""
    config = {}
    
    bitable_token = os.environ.get('BITABLE_APP_TOKEN')
    table_id = os.environ.get('BITABLE_TABLE_ID')
    
    if bitable_token and table_id:
        config['bitable'] = {
            'app_token': bitable_token,
            'table_id': table_id
        }
        print_success("从环境变量读取到 Bitable 配置")
    
    return config


def search_feishu_bitable():
    """
    搜索飞书多维表格，帮助用户选择或创建
    
    注意：此功能需要飞书 API 支持
    """
    print_warning("自动搜索多维表格功能需要飞书 API 支持")
    print("建议手动配置：")
    print("1. 打开飞书多维表格")
    print("2. 复制表格 URL 中的 token")
    print("3. 运行配置向导")
    return None


def create_guide_config():
    """引导用户创建配置"""
    print_header("🔧 Article Workflow 配置向导")
    
    print("欢迎使用文章分析工作流！")
    print("首次使用需要配置飞书多维表格。\n")
    
    # 检查环境变量
    env_config = check_env_config()
    if env_config:
        print("\n✅ 检测到环境变量配置，是否使用？")
        print("   是 (y) / 否 (n) / 手动输入 (m)")
        choice = input("请选择：").strip().lower()
        if choice == 'y':
            return env_config
    
    # 检查是否有现有配置
    existing = load_existing_config()
    if existing.get('bitable'):
        print("\n✅ 检测到现有配置：")
        print(f"   App Token: {existing['bitable']['app_token'][:10]}...")
        print(f"   Table ID: {existing['bitable']['table_id']}")
        print("\n是否保留现有配置？")
        print("   是 (y) / 否 (n) / 更新 (u)")
        choice = input("请选择：").strip().lower()
        if choice == 'y':
            return existing
    
    # 引导手动输入
    print("\n📝 请输入配置信息：")
    print("\n1. 打开飞书多维表格（文章知识库）")
    print("2. 从 URL 复制 token")
    print("   示例 URL: https://xxx.feishu.cn/base/FOKgbCL2FarkSusBCRkcz4JZnad")
    print("   Token: FOKgbCL2FarkSusBCRkcz4JZnad\n")
    
    app_token = input("请输入 Bitable App Token: ").strip()
    table_id = input("请输入 Table ID (可选，默认第一个表): ").strip()
    
    if not app_token:
        print_error("App Token 不能为空")
        sys.exit(1)
    
    config = {
        "bitable": {
            "app_token": app_token,
            "table_id": table_id or "auto"
        },
        "workflow": {
            "check_interval_hours": 6,
            "batch_limit": 10,
            "enable_quality_score": True,
            "enable_url_dedup": True
        },
        "paths": {
            "data": "./data",
            "logs": "./logs"
        }
    }
    
    return config


def save_config(config: dict):
    """保存配置到文件"""
    # 备份现有配置
    if CONFIG_FILE.exists():
        backup_config()
    
    # 保存新配置
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print_success(f"配置已保存：{CONFIG_FILE}")
    
    # 设置权限（仅所有者可读写）
    os.chmod(CONFIG_FILE, 0o600)


def merge_config(new_config: dict, existing_config: dict) -> dict:
    """
    合并配置，保留用户自定义设置
    
    规则：
    1. 敏感信息（bitable token）优先保留现有配置
    2. 新增配置项使用新配置
    3. 用户自定义设置保留
    """
    merged = existing_config.copy()
    
    # 递归合并
    for key, value in new_config.items():
        if key == 'bitable' and 'bitable' in merged:
            # Bitable 配置保留现有的（敏感信息）
            if existing_config['bitable'].get('app_token'):
                merged['bitable']['app_token'] = existing_config['bitable']['app_token']
            if existing_config['bitable'].get('table_id'):
                merged['bitable']['table_id'] = existing_config['bitable']['table_id']
        elif isinstance(value, dict) and key in merged and isinstance(merged[key], dict):
            merged[key] = merge_config(value, merged[key])
        else:
            merged[key] = value
    
    return merged


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法：")
        print("  python config_manager.py check      # 检查配置")
        print("  python config_manager.py backup     # 备份配置")
        print("  python config_manager.py restore    # 恢复配置")
        print("  python config_manager.py guide      # 配置向导")
        print("  python config_manager.py merge      # 合并配置（升级时）")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "check":
        print_header("📋 配置检查")
        
        if CONFIG_FILE.exists():
            print_success(f"配置文件存在：{CONFIG_FILE}")
            config = load_existing_config()
            if config.get('bitable'):
                print_success("Bitable 配置：已配置")
                print(f"   App Token: {config['bitable']['app_token'][:10]}...")
                print(f"   Table ID: {config['bitable']['table_id']}")
            else:
                print_warning("Bitable 配置：未配置")
        else:
            print_warning("配置文件不存在")
            print("\n建议运行配置向导：")
            print("  python config_manager.py guide")
    
    elif command == "backup":
        print_header("💾 备份配置")
        if backup_config():
            print_success("备份完成")
        else:
            print_warning("无现有配置可备份")
    
    elif command == "restore":
        print_header("🔄 恢复配置")
        if restore_config():
            print_success("恢复完成")
        else:
            print_warning("无备份可恢复")
    
    elif command == "guide":
        print_header("🔧 配置向导")
        config = create_guide_config()
        save_config(config)
        print("\n✨ 配置完成！现在可以开始使用文章分析工作流了。")
    
    elif command == "merge":
        print_header("🔀 合并配置")
        
        # 读取新配置（从 config.example.json 或参数）
        example_file = SKILL_DIR / "config.example.json"
        if not example_file.exists():
            print_error("未找到示例配置文件")
            sys.exit(1)
        
        with open(example_file, 'r', encoding='utf-8') as f:
            new_config = json.load(f)
        
        # 加载现有配置
        existing_config = load_existing_config()
        
        if not existing_config:
            print_warning("无现有配置，直接创建新配置")
            save_config(new_config)
        else:
            # 合并配置
            merged = merge_config(new_config, existing_config)
            save_config(merged)
            print_success("配置合并完成")
            print("   保留了现有敏感信息（Bitable Token）")
            print("   更新了新增配置项")
    
    else:
        print_error(f"未知命令：{command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
