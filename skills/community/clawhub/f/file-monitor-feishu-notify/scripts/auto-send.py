#!/usr/bin/env python3
"""
自动发送通知
监控 .pending_notify.md 文件，有新内容立即通过 OpenClaw 发送
"""

import os
import sys
import time
import json
import subprocess
from pathlib import Path
from datetime import datetime

# 加载配置
SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent  # skills/file-monitor
CONFIG_FILE = SKILL_DIR / 'config.json'
config = json.load(open(CONFIG_FILE, 'r', encoding='utf-8'))

# 文件路径配置（相对于 skill 目录，自包含）
NOTIFY_FILE = SKILL_DIR / config.get('notify_file', '.data/.pending_notify.md')
LOG_FILE = SKILL_DIR / config.get('log_file', 'logs/auto-send.log')
CHECK_INTERVAL = config.get('check_interval', 2)

# 飞书配置
FEISHU_APP_ID = config['feishu']['app_id']
FEISHU_APP_SECRET = config['feishu']['app_secret']
FEISHU_CHAT_ID = config['feishu']['chat_id']

def log(message):
    """写入日志"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_line = f"[{timestamp}] {message}\n"
    print(log_line, end='', flush=True)
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(log_line)
    except:
        pass

def send_via_feishu(content):
    """直接调用飞书 API 发送消息"""
    import urllib.request
    import urllib.error
    
    # 飞书应用配置（从 config.json 读取）
    APP_ID = FEISHU_APP_ID
    APP_SECRET = FEISHU_APP_SECRET
    CHAT_ID = FEISHU_CHAT_ID
    
    try:
        log(f"  [INFO] 开始获取 token")
        
        # 1. 获取 access_token
        token_url = 'https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal'
        token_data = json.dumps({
            'app_id': APP_ID,
            'app_secret': APP_SECRET
        }).encode('utf-8')
        
        token_req = urllib.request.Request(token_url, data=token_data)
        token_req.add_header('Content-Type', 'application/json')
        
        with urllib.request.urlopen(token_req, timeout=10) as resp:
            token_result = json.loads(resp.read().decode('utf-8'))
        
        if token_result.get('code') != 0:
            log(f"  [ERR] Token 失败：{token_result.get('msg')}")
            return False
        
        access_token = token_result['app_access_token']
        
        # 2. 发送消息
        msg_url = 'https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id'
        msg_data = json.dumps({
            'receive_id': CHAT_ID,
            'msg_type': 'text',
            'content': json.dumps({'text': content})
        }).encode('utf-8')
        
        msg_req = urllib.request.Request(msg_url, data=msg_data)
        msg_req.add_header('Content-Type', 'application/json')
        msg_req.add_header('Authorization', f'Bearer {access_token}')
        
        with urllib.request.urlopen(msg_req, timeout=10) as resp:
            msg_result = json.loads(resp.read().decode('utf-8'))
        
        if msg_result.get('code') == 0:
            log(f"  [OK] 已发送到飞书群聊")
            return True
        else:
            log(f"  [ERR] 发送失败：{msg_result.get('msg')}")
            return False
            
    except urllib.error.HTTPError as e:
        log(f"  [ERR] HTTP 错误：{e.code} - {e.reason}")
        log(f"  [ERR] 响应内容：{e.read().decode('utf-8') if e.fp else 'N/A'}")
        return False
    except urllib.error.URLError as e:
        log(f"  [ERR] 网络错误：{e.reason}")
        return False
    except Exception as e:
        log(f"  [ERR] 未知错误：{type(e).__name__} - {e}")
        return False

def check_and_send():
    """检查并发送通知"""
    if not NOTIFY_FILE.exists():
        return
    
    content = NOTIFY_FILE.read_text(encoding='utf-8')
    
    # 检查是否是空模板
    if '当前没有待发送的通知' in content or len(content.strip()) < 50:
        return
    
    # 提取文件信息
    file_match = None
    for line in content.split('\n'):
        if '**文件**' in line or '文件名' in line:
            file_match = line
            break
    
    if not file_match:
        return
    
    log(f"\n[发现新通知] {file_match.strip()}")
    
    # 发送消息
    if send_via_feishu(content):
        log(f"  [OK] 已发送到群聊")
        
        # 清空通知文件（强制刷新到磁盘）
        try:
            with open(NOTIFY_FILE, 'w', encoding='utf-8') as f:
                f.write("# 待发送通知\n\n_当前没有待发送的通知_\n")
                f.flush()
                os.fsync(f.fileno())  # 强制刷新到磁盘
            log(f"  [OK] 通知文件已清空（已强制写入）")
        except Exception as e:
            log(f"  [ERR] 清空通知文件失败：{e}")
    else:
        log(f"  [WARN] 发送失败，下次重试")

def main():
    log("=" * 50)
    log("[SEND] 自动发送器 (实时)")
    log("=" * 50)
    log(f"监控文件：{NOTIFY_FILE}")
    log(f"检查间隔：{CHECK_INTERVAL}秒")
    log(f"发送方式：飞书 API")
    log("=" * 50)
    log("按 Ctrl+C 停止\n")
    
    while True:
        try:
            check_and_send()
        except Exception as e:
            log(f"[ERR] {e}")
        
        time.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
    main()
