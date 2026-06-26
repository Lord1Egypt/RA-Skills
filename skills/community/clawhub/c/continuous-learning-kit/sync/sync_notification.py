# -*- coding: utf-8 -*-
import json
import sys
import os
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# 添加路径
sys.path.insert(0, 'C:/Users/18625/.openclaw/workspace/skills/mempalace')
from mempalace.mcp_server import handle_request

# 加载配置
def load_config():
    """加载配置"""
    config_path = 'C:/Users/18625/.openclaw/workspace/skills/continuous-learning/config/dream_config.json'
    default_queue = "C:/Users/18625/.openclaw/workspace/.notification_queue.json"

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            notification_config = config.get('notification', {})
            return {
                'queue_file': os.path.join(
                    os.path.dirname(config_path),
                    notification_config.get('queue_file', '.notification_queue.json')
                ),
                'to': notification_config.get('to', '')
            }
    except:
        return {
            'queue_file': default_queue,
            'to': ''
        }

NOTIFICATION_CONFIG = load_config()

def queue_notification(message):
    """将通知存入队列"""
    try:
        notifications = []

        queue_file = NOTIFICATION_CONFIG['queue_file']
        to_user = NOTIFICATION_CONFIG.get('to', '')

        if os.path.exists(queue_file):
            with open(queue_file, 'r', encoding='utf-8') as f:
                notifications = json.load(f)

        notification_item = {
            'message': message,
            'timestamp': datetime.now().isoformat()
        }

        if to_user:
            notification_item['to'] = to_user

        notifications.append(notification_item)

        with open(queue_file, 'w', encoding='utf-8') as f:
            json.dump(notifications, f, ensure_ascii=False, indent=2)

        print(f"[通知] 已加入发送队列")
        return True
    except Exception as e:
        print(f"[通知] 队列写入失败: {e}")
        return False

if __name__ == '__main__':
    start_time = datetime.now()
    print(f"[SYNC] 开始同步 - {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

    date_str = datetime.now().strftime('%Y-%m-%d')
    entry_text = f"SESSION:{date_str} 今日聊天已经自动同步到MemPalace 定时任务执行时间 {start_time.strftime('%H:%M:%S')}"

    # 执行同步
    req = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "mempalace_diary_write",
            "arguments": {
                "agent_name": "小麦",
                "entry": entry_text,
                "topic": "daily_summary"
            }
        }
    }

    result = handle_request(req)

    if 'result' in result:
        content = result['result']['content'][0]['text']
        data = json.loads(content)

        if data.get('success'):
            print(f"[SYNC] 同步成功")
            print(f"  条目ID: {data.get('entry_id')}")

            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            # 队列通知
            message = f"""✅ 今日聊天已同步到MemPalace

📅 日期: {date_str}
🕒 时间: {start_time.strftime('%H:%M:%S')}
⏱️ 耗时: {duration:.2f}秒

条目ID: {data.get('entry_id', 'unknown')}
"""
            queue_notification(message)

        else:
            print(f"[SYNC] 同步失败")
            queue_notification(f"❌ 同步失败: {data}")
    else:
        print(f"[SYNC] 错误: {result}")
