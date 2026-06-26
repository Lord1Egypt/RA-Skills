#!/usr/bin/env python3
"""
Echo Seed Telegram Bot 启动脚本

通过 OpenClaw 的 message 工具与 Telegram 交互
"""

import sys
import time
from pathlib import Path
from datetime import datetime

# 添加项目根目录到路径
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from echo_telegram import process_message

# 日志目录
LOG_DIR = ROOT_DIR / 'logs'
LOG_DIR.mkdir(parents=True, exist_ok=True)

# 消息队列文件
MESSAGE_QUEUE = LOG_DIR / 'telegram_message_queue.json'
REPLY_QUEUE = LOG_DIR / 'telegram_reply_queue.json'


def log_message(message, level='INFO'):
    """记录日志"""
    timestamp = datetime.now().isoformat()
    log_file = LOG_DIR / f'bot_{datetime.now().strftime("%Y%m%d")}.log'
    
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"[{timestamp}] [{level}] {message}\n")


def poll_messages():
    """轮询消息队列（简化版本）"""
    log_message("Bot 启动，等待消息...")
    
    last_check = None
    
    while True:
        try:
            # 检查消息队列文件
            if MESSAGE_QUEUE.exists():
                import json
                
                with open(MESSAGE_QUEUE, 'r', encoding='utf-8') as f:
                    message_data = json.load(f)
                
                # 处理消息
                text = message_data.get('text', '')
                user_id = message_data.get('user_id')
                message_id = message_data.get('message_id')
                
                log_message(f"收到消息：{text[:50]}...")
                
                # 处理并生成回复
                reply = process_message(text, user_id)
                
                log_message(f"回复：{reply[:50]}...")
                
                # 写入回复队列
                reply_data = {
                    'message_id': message_id,
                    'reply': reply,
                    'timestamp': datetime.now().isoformat()
                }
                
                with open(REPLY_QUEUE, 'w', encoding='utf-8') as f:
                    json.dump(reply_data, f, ensure_ascii=False, indent=2)
                
                # 删除已处理的消息
                MESSAGE_QUEUE.unlink()
            
            # 等待 1 秒
            time.sleep(1)
            
        except KeyboardInterrupt:
            log_message("Bot 停止", 'WARN')
            break
        except Exception as e:
            log_message(f"错误：{e}", 'ERROR')
            time.sleep(5)


if __name__ == '__main__':
    print("🤖 Echo Seed Telegram Bot 启动中...")
    print(f"📂 项目根目录：{ROOT_DIR}")
    print(f"📝 日志目录：{LOG_DIR}")
    print("💬 等待 Telegram 消息...\n")
    
    log_message("Bot 启动")
    
    try:
        poll_messages()
    except Exception as e:
        print(f"❌ Bot 错误：{e}")
        log_message(f"Bot 崩溃：{e}", 'ERROR')
