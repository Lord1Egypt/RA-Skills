#!/usr/bin/env python3
"""
API Cockpit - Multi-Platform Notifier
Supports: Telegram, Discord, Slack, Feishu, QQ, DingTalk
"""

import os
import sys
import json
import requests
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(SCRIPT_DIR, '..', 'config', 'notify.json')

def load_config():
    """Load notification config"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {
        "telegram": {"enabled": False, "bot_token": "", "chat_id": ""},
        "discord": {"enabled": False, "webhook_url": ""},
        "slack": {"enabled": False, "webhook_url": ""},
        "feishu": {"enabled": False, "webhook_url": ""},
        "qq": {"enabled": False, "webhook_url": ""},
        "dingtalk": {"enabled": False, "webhook_url": ""}
    }

def save_config(config):
    """Save notification config"""
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

def send_telegram(bot_token, chat_id, message):
    """Send via Telegram"""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
    r = requests.post(url, json=data, timeout=10)
    return r.status_code == 200

def send_discord(webhook_url, message):
    """Send via Discord webhook"""
    data = {"content": message}
    r = requests.post(webhook_url, json=data, timeout=10)
    return r.status_code in [200, 204]

def send_slack(webhook_url, message):
    """Send via Slack webhook"""
    data = {"text": message}
    r = requests.post(webhook_url, json=data, timeout=10)
    return r.status_code in [200, 204]

def send_feishu(webhook_url, message):
    """Send via Feishu webhook"""
    data = {"msg_type": "text", "content": {"text": message}}
    r = requests.post(webhook_url, json=data, timeout=10)
    return r.status_code == 200

def send_dingtalk(webhook_url, message):
    """Send via DingTalk webhook"""
    data = {"msgtype": "text", "text": {"content": message}}
    r = requests.post(webhook_url, json=data, timeout=10)
    return r.status_code == 200

def send_qq(webhook_url, message):
    """Send via QQ webhook (go-cqhttp style)"""
    # QQ uses go-cqhttp HTTP API
    data = {
        "message_type": "private",
        "message": message
    }
    r = requests.post(webhook_url, json=data, timeout=10)
    return r.status_code == 200

def notify(message, title="API Cockpit", platforms=None):
    """Send notification to configured platforms"""
    config = load_config()
    results = {}
    
    if platforms is None:
        platforms = [k for k, v in config.items() if v.get('enabled')]
    
    full_message = f"*{title}*\n{message}"
    
    for platform in platforms:
        if platform not in config or not config[platform].get('enabled'):
            continue
        
        try:
            if platform == 'telegram':
                ok = send_telegram(
                    config['telegram']['bot_token'],
                    config['telegram']['chat_id'],
                    full_message
                )
            elif platform == 'discord':
                ok = send_discord(config['discord']['webhook_url'], full_message)
            elif platform == 'slack':
                ok = send_slack(config['slack']['webhook_url'], full_message)
            elif platform == 'feishu':
                ok = send_feishu(config['feishu']['webhook_url'], full_message)
            elif platform == 'dingtalk':
                ok = send_dingtalk(config['dingtalk']['webhook_url'], full_message)
            elif platform == 'qq':
                ok = send_qq(config['qq']['webhook_url'], full_message)
            else:
                ok = False
            
            results[platform] = "✅" if ok else "❌"
        except Exception as e:
            results[platform] = f"❌ {e}"
    
    return results

def test(platforms=None):
    """Test all or specific platforms"""
    results = notify("🔔 Test message from API Cockpit", "Test", platforms)
    for platform, status in results.items():
        print(f"{platform}: {status}")
    return results

def main():
    """CLI entry point"""
    if len(sys.argv) < 2:
        print("Usage: notifier.py [test|config|send]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'test':
        test()
    elif command == 'config':
        config = load_config()
        print(json.dumps(config, indent=2))
    elif command == 'send':
        if len(sys.argv) < 3:
            print("Usage: notifier.py send <message>")
            sys.exit(1)
        results = notify(sys.argv[2])
        print(json.dumps(results, indent=2))
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == '__main__':
    main()
