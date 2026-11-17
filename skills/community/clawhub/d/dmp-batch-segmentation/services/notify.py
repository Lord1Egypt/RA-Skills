#!/usr/bin/env python3
"""
通用通知模块
支持多种通知方式：企业微信、钉钉、飞书、邮件、本地文件
"""

import json
import os
import urllib.request
import urllib.parse
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from datetime import datetime

# 配置文件路径
CONFIG_FILE = Path(__file__).parent / "notify_config.json"

def load_notify_config():
    """加载通知配置"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"enabled": [], "webhooks": {}, "email": {}, "local": {}}

def save_notify_config(config):
    """保存通知配置"""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

def send_wechat_webhook(message, webhook_url):
    """发送企业微信机器人通知"""
    try:
        data = {
            "msgtype": "text",
            "text": {
                "content": message
            }
        }
        req = urllib.request.Request(
            webhook_url,
            data=json.dumps(data).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result.get('errcode') == 0
    except Exception as e:
        print(f"企业微信通知失败: {e}")
        return False

def send_dingtalk_webhook(message, webhook_url):
    """发送钉钉机器人通知"""
    try:
        data = {
            "msgtype": "text",
            "text": {
                "content": message
            }
        }
        req = urllib.request.Request(
            webhook_url,
            data=json.dumps(data).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result.get('errcode') == 0
    except Exception as e:
        print(f"钉钉通知失败: {e}")
        return False

def send_feishu_webhook(message, webhook_url):
    """发送飞书机器人通知"""
    try:
        data = {
            "msg_type": "text",
            "content": {
                "text": message
            }
        }
        req = urllib.request.Request(
            webhook_url,
            data=json.dumps(data).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result.get('code') == 0
    except Exception as e:
        print(f"飞书通知失败: {e}")
        return False

def send_email(message, email_config):
    """发送邮件通知"""
    try:
        msg = MIMEMultipart()
        msg['From'] = email_config['from']
        msg['To'] = email_config['to']
        msg['Subject'] = email_config.get('subject', 'DMP任务通知')
        
        msg.attach(MIMEText(message, 'plain', 'utf-8'))
        
        server = smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port'])
        server.starttls()
        server.login(email_config['username'], email_config['password'])
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"邮件通知失败: {e}")
        return False

def save_local_notification(message, local_config):
    """保存本地通知"""
    try:
        log_file = local_config.get('log_file', str(Path(__file__).parent / 'notifications.log'))
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] {message}\n")
        return True
    except Exception as e:
        print(f"本地通知失败: {e}")
        return False

def send_notification(message, task_info=None):
    """发送通知（根据配置选择通知方式）"""
    config = load_notify_config()
    
    enabled = config.get('enabled', [])
    
    if not enabled:
        # 如果没有配置任何通知方式，只保存到本地
        save_local_notification(message, config.get('local', {}))
        return
    
    results = {}
    
    # 企业微信
    if 'wechat' in enabled:
        webhook_url = config.get('webhooks', {}).get('wechat')
        if webhook_url:
            results['wechat'] = send_wechat_webhook(message, webhook_url)
    
    # 钉钉
    if 'dingtalk' in enabled:
        webhook_url = config.get('webhooks', {}).get('dingtalk')
        if webhook_url:
            results['dingtalk'] = send_dingtalk_webhook(message, webhook_url)
    
    # 飞书
    if 'feishu' in enabled:
        webhook_url = config.get('webhooks', {}).get('feishu')
        if webhook_url:
            results['feishu'] = send_feishu_webhook(message, webhook_url)
    
    # 邮件
    if 'email' in enabled:
        email_config = config.get('email', {})
        if email_config:
            results['email'] = send_email(message, email_config)
    
    # 本地文件（始终保存）
    results['local'] = save_local_notification(message, config.get('local', {}))
    
    return results

def setup_wechat(webhook_url):
    """配置企业微信通知"""
    config = load_notify_config()
    config.setdefault('webhooks', {})['wechat'] = webhook_url
    if 'wechat' not in config.get('enabled', []):
        config.setdefault('enabled', []).append('wechat')
    save_notify_config(config)
    print("✅ 企业微信通知已配置")

def setup_dingtalk(webhook_url):
    """配置钉钉通知"""
    config = load_notify_config()
    config.setdefault('webhooks', {})['dingtalk'] = webhook_url
    if 'dingtalk' not in config.get('enabled', []):
        config.setdefault('enabled', []).append('dingtalk')
    save_notify_config(config)
    print("✅ 钉钉通知已配置")

def setup_feishu(webhook_url):
    """配置飞书通知"""
    config = load_notify_config()
    config.setdefault('webhooks', {})['feishu'] = webhook_url
    if 'feishu' not in config.get('enabled', []):
        config.setdefault('enabled', []).append('feishu')
    save_notify_config(config)
    print("✅ 飞书通知已配置")

def setup_email(smtp_server, smtp_port, username, password, to_email):
    """配置邮件通知"""
    config = load_notify_config()
    config['email'] = {
        'smtp_server': smtp_server,
        'smtp_port': smtp_port,
        'username': username,
        'password': password,
        'from': username,
        'to': to_email,
        'subject': 'DMP任务通知'
    }
    if 'email' not in config.get('enabled', []):
        config.setdefault('enabled', []).append('email')
    save_notify_config(config)
    print("✅ 邮件通知已配置")

def show_config():
    """显示当前配置"""
    config = load_notify_config()
    print(json.dumps(config, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法:")
        print("  python notify.py setup-wechat <webhook_url>")
        print("  python notify.py setup-dingtalk <webhook_url>")
        print("  python notify.py setup-feishu <webhook_url>")
        print("  python notify.py setup-email <smtp_server> <smtp_port> <username> <password> <to_email>")
        print("  python notify.py config")
        print("  python notify.py test <message>")
        sys.exit(1)
    
    action = sys.argv[1]
    
    if action == "setup-wechat" and len(sys.argv) >= 3:
        setup_wechat(sys.argv[2])
    
    elif action == "setup-dingtalk" and len(sys.argv) >= 3:
        setup_dingtalk(sys.argv[2])
    
    elif action == "setup-feishu" and len(sys.argv) >= 3:
        setup_feishu(sys.argv[2])
    
    elif action == "setup-email" and len(sys.argv) >= 7:
        setup_email(sys.argv[2], int(sys.argv[3]), sys.argv[4], sys.argv[5], sys.argv[6])
    
    elif action == "config":
        show_config()
    
    elif action == "test" and len(sys.argv) >= 3:
        result = send_notification(sys.argv[2])
        print(f"通知结果: {result}")
    
    else:
        print("未知命令")
