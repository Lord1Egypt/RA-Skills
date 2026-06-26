#!/usr/bin/env python3
"""
安全添加 Discord 配置到 openclaw.json 的脚本

使用方法:
1. 设置环境变量:
   export DISCORD_BOT_TOKEN="your_token"
   export DISCORD_USER_ID="your_user_id"
   export DISCORD_SERVER_ID="your_server_id"

2. 运行脚本:
   python3 add_discord_config.py

或直接传入参数:
   python3 add_discord_config.py --token "your_token" --user-id "123" --server-id "456"
"""

import json
import os
import sys
import argparse
import tempfile
import shutil
from datetime import datetime

def load_config(config_path):
    """加载 openclaw.json 配置"""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"错误: 配置文件不存在: {config_path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"错误: 配置文件 JSON 格式错误: {e}")
        sys.exit(1)

def save_config(config_path, data):
    """保存配置到文件，先写入临时文件再移动"""
    # 创建备份
    backup_path = f"{config_path}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    shutil.copy2(config_path, backup_path)
    print(f"✅ 已创建备份: {backup_path}")
    
    # 写入临时文件
    temp_fd, temp_path = tempfile.mkstemp(suffix='.json', dir=os.path.dirname(config_path))
    try:
        with os.fdopen(temp_fd, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        # 移动临时文件到目标位置
        shutil.move(temp_path, config_path)
        print(f"✅ 配置已更新: {config_path}")
        
    except Exception as e:
        # 清理临时文件
        if os.path.exists(temp_path):
            os.unlink(temp_path)
        print(f"错误: 写入配置失败: {e}")
        sys.exit(1)

def add_discord_config(config_data, token, use_env_ref=True):
    """添加 Discord 配置到 channels 部分"""
    
    # 确保 channels 部分存在
    if 'channels' not in config_data:
        config_data['channels'] = {}
    
    # Discord 配置
    discord_config = {
        "enabled": True,
        "streaming": True,
        "footer": {
            "elapsed": True,
            "status": True
        },
        "accounts": {
            "default": {
                "dmPolicy": "open",
                "allowFrom": ["*"]
            }
        }
    }
    
    # Token 配置方式
    if use_env_ref:
        # 使用环境变量引用 (推荐)
        discord_config["token"] = {
            "source": "env",
            "provider": "default",
            "id": "DISCORD_BOT_TOKEN"
        }
        print("ℹ 使用环境变量引用 token: DISCORD_BOT_TOKEN")
    else:
        # 直接嵌入 token (不推荐，仅用于测试)
        discord_config["token"] = token
        print("⚠ 警告: 直接嵌入 token，建议使用环境变量方式")
    
    # 添加到 channels
    config_data['channels']['discord'] = discord_config
    
    return config_data

def validate_config(config_data):
    """验证配置格式"""
    try:
        # 检查 channels 部分
        if 'channels' not in config_data:
            print("❌ 错误: 配置缺少 channels 部分")
            return False
        
        # 检查 discord 配置
        if 'discord' not in config_data['channels']:
            print("❌ 错误: 配置缺少 discord 部分")
            return False
        
        discord_config = config_data['channels']['discord']
        
        # 检查必要字段
        required_fields = ['enabled', 'token']
        for field in required_fields:
            if field not in discord_config:
                print(f"❌ 错误: discord 配置缺少 {field} 字段")
                return False
        
        # 检查 token 格式
        token_config = discord_config['token']
        if isinstance(token_config, dict):
            if 'source' not in token_config:
                print("❌ 错误: token 配置缺少 source 字段")
                return False
        
        print("✅ 配置验证通过")
        return True
        
    except Exception as e:
        print(f"❌ 配置验证失败: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='添加 Discord 配置到 openclaw.json')
    parser.add_argument('--config', default='~/.openclaw/openclaw.json', 
                       help='openclaw.json 路径 (默认: ~/.openclaw/openclaw.json)')
    parser.add_argument('--token', help='Discord bot token')
    parser.add_argument('--user-id', help='Discord 用户 ID')
    parser.add_argument('--server-id', help='Discord 服务器 ID')
    parser.add_argument('--env-ref', action='store_true', default=True,
                       help='使用环境变量引用 token (默认)')
    parser.add_argument('--direct-token', action='store_false', dest='env_ref',
                       help='直接嵌入 token (不推荐)')
    
    args = parser.parse_args()
    
    # 展开路径
    config_path = os.path.expanduser(args.config)
    
    print(f"📁 配置文件: {config_path}")
    
    # 获取 token
    token = args.token
    if not token:
        token = os.environ.get('DISCORD_BOT_TOKEN')
    
    if not token:
        print("❌ 错误: 未提供 Discord bot token")
        print("请通过以下方式之一提供 token:")
        print("  1. 设置环境变量: export DISCORD_BOT_TOKEN=\"your_token\"")
        print("  2. 命令行参数: --token \"your_token\"")
        sys.exit(1)
    
    # 获取用户ID和服务器ID (仅用于信息显示)
    user_id = args.user_id or os.environ.get('DISCORD_USER_ID', '未设置')
    server_id = args.server_id or os.environ.get('DISCORD_SERVER_ID', '未设置')
    
    print(f"🔑 Token 已获取: {'*' * 20}{token[-4:] if len(token) > 4 else ''}")
    print(f"👤 用户 ID: {user_id}")
    print(f"🏢 服务器 ID: {server_id}")
    
    # 加载配置
    print("\n📖 加载当前配置...")
    config_data = load_config(config_path)
    
    # 检查是否已存在 discord 配置
    if 'channels' in config_data and 'discord' in config_data['channels']:
        print("⚠ 警告: 配置中已存在 discord 部分")
        response = input("是否覆盖现有配置? (y/N): ")
        if response.lower() != 'y':
            print("操作已取消")
            sys.exit(0)
    
    # 添加 discord 配置
    print("\n🔧 添加 Discord 配置...")
    config_data = add_discord_config(config_data, token, args.env_ref)
    
    # 验证配置
    print("\n🔍 验证配置格式...")
    if not validate_config(config_data):
        print("❌ 配置验证失败，操作已取消")
        sys.exit(1)
    
    # 确认操作
    print("\n⚠ 确认操作")
    print("将修改以下配置:")
    print(json.dumps(config_data['channels']['discord'], indent=2, ensure_ascii=False))
    
    response = input("\n确认修改配置? (y/N): ")
    if response.lower() != 'y':
        print("操作已取消")
        sys.exit(0)
    
    # 保存配置
    print("\n💾 保存配置...")
    save_config(config_path, config_data)
    
    # 后续步骤提示
    print("\n🎉 Discord 配置已添加!")
    print("\n📋 后续步骤:")
    print("1. 确保环境变量已设置:")
    print("   export DISCORD_BOT_TOKEN=\"your_token\"")
    if args.env_ref:
        print("   (已配置为使用环境变量)")
    
    print("\n2. 重启 OpenClaw gateway:")
    print("   openclaw gateway restart")
    
    print("\n3. 检查服务状态:")
    print("   openclaw gateway status")
    
    print("\n4. 配对机器人:")
    print("   在 Discord 中发送: /pair")
    print("   或通过其他渠道发送配对指令")
    
    print("\n5. 验证连接:")
    print("   检查 Discord 机器人是否在线")
    print("   发送测试消息验证功能")

if __name__ == '__main__':
    main()