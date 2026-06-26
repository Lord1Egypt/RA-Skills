#!/usr/bin/env python3
"""
钉钉插件安装和配置脚本

用法:
    python install_dingtalk.py --client-id <clientId> --client-secret <clientSecret>
    
可选参数:
    --robot-code <robotCode>     机器人 code
    --corp-id <corpId>           企业 corpId
    --agent-id <agentId>         应用 agentId
    --card-template-id <id>      卡片模板 ID
    --card-template-key <key>    卡片模板内容变量
    --message-type <type>        消息类型：markdown 或 card (默认：markdown)
    --skip-restart               跳过 gateway 重启
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path


def run_command(cmd, description):
    """执行命令并输出结果"""
    print(f"\n🔧 {description}...")
    # 将命令字符串转换为列表形式以避免 shell 注入
    if isinstance(cmd, str):
        cmd = cmd.split()
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ 失败：{result.stderr}")
        return False
    if result.stdout:
        print(result.stdout)
    return True


def patch_config(client_id, client_secret, config_path, **kwargs):
    """更新 OpenClaw 配置文件"""
    print(f"\n📝 更新配置文件：{config_path}")
    
    # 读取现有配置
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"❌ 配置文件不存在：{config_path}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ 配置文件 JSON 格式错误：{e}")
        return False
    
    # 配置钉钉通道
    dingtalk_config = {
        "enabled": True,
        "clientId": client_id,
        "clientSecret": client_secret,
        "dmPolicy": "open",
        "groupPolicy": "open",
        "showThinking": True,
        "thinkingMessage": "🤔 思考中，请稍候...",
        "debug": False,
        "messageType": kwargs.get('message_type', 'markdown'),
        "allowFrom": ["*"]
    }
    
    # 添加可选参数
    if kwargs.get('robot_code'):
        dingtalk_config["robotCode"] = kwargs['robot_code']
    if kwargs.get('corp_id'):
        dingtalk_config["corpId"] = kwargs['corp_id']
    if kwargs.get('agent_id'):
        dingtalk_config["agentId"] = kwargs['agent_id']
    if kwargs.get('card_template_id') and kwargs.get('message_type') == 'card':
        dingtalk_config["cardTemplateId"] = kwargs['card_template_id']
    if kwargs.get('card_template_key') and kwargs.get('message_type') == 'card':
        dingtalk_config["cardTemplateKey"] = kwargs['card_template_key']
    
    # 更新配置
    config.setdefault('channels', {})
    config['channels']['dingtalk'] = dingtalk_config
    
    # 确保插件已启用
    config.setdefault('plugins', {})
    config['plugins']['enabled'] = True
    if 'allow' not in config['plugins']:
        config['plugins']['allow'] = []
    if 'dingtalk' not in config['plugins']['allow']:
        config['plugins']['allow'].append('dingtalk')
    config['plugins'].setdefault('entries', {})
    config['plugins']['entries']['dingtalk'] = {"enabled": True}
    
    # 写回配置
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print("✅ 配置已更新")
    return True


def restart_gateway():
    """重启 Gateway"""
    print("\n🔄 重启 Gateway...")
    result = subprocess.run(
        ["openclaw", "gateway", "restart"],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print(f"❌ 重启失败：{result.stderr}")
        return False
    print("✅ Gateway 重启成功")
    return True


def main():
    parser = argparse.ArgumentParser(description='钉钉插件安装和配置工具')
    parser.add_argument('--client-id', required=True, help='钉钉应用 Client ID')
    parser.add_argument('--client-secret', required=True, help='钉钉应用 Client Secret')
    parser.add_argument('--robot-code', help='机器人 Code')
    parser.add_argument('--corp-id', help='企业 Corp ID')
    parser.add_argument('--agent-id', help='应用 Agent ID')
    parser.add_argument('--card-template-id', help='卡片模板 ID (仅 card 模式)')
    parser.add_argument('--card-template-key', help='卡片模板内容变量 (仅 card 模式)')
    parser.add_argument('--message-type', choices=['markdown', 'card'], default='markdown',
                        help='消息类型 (默认：markdown)')
    parser.add_argument('--skip-restart', action='store_true', help='跳过 gateway 重启')
    parser.add_argument('--config-path', default=str(Path.home() / '.openclaw' / 'openclaw.json'),
                        help='OpenClaw 配置文件路径')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("📦 钉钉插件安装配置工具")
    print("=" * 60)
    
    # 安装插件
    if not run_command(
        ["openclaw", "plugins", "install", "@soimy/dingtalk"],
        "安装钉钉插件"
    ):
        print("⚠️ 插件可能已安装，继续配置...")
    
    # 更新配置
    if not patch_config(
        args.client_id,
        args.client_secret,
        args.config_path,
        robot_code=args.robot_code,
        corp_id=args.corp_id,
        agent_id=args.agent_id,
        card_template_id=args.card_template_id,
        card_template_key=args.card_template_key,
        message_type=args.message_type
    ):
        sys.exit(1)
    
    # 重启 Gateway
    if not args.skip_restart:
        if not restart_gateway():
            sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✅ 钉钉插件安装配置完成！")
    print("=" * 60)
    print("\n下一步:")
    print("1. 在钉钉开放平台配置机器人")
    print("2. 将机器人添加到群聊或私聊")
    print("3. 开始使用！")


if __name__ == '__main__':
    main()
