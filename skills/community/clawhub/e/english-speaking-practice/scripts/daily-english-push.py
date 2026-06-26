#!/usr/bin/env python3
"""
每日英语知识推送 - AI 生成
"""
import json
import os
import subprocess
from datetime import datetime

# 读取配置
SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_FILE = os.path.join(SCRIPT_DIR, 'config.json')
DEFAULT_DATA_DIR = os.path.join(SCRIPT_DIR, 'practice-data')

def get_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}

def get_data_dir():
    config = get_config()
    data_dir = config.get('data', {}).get('baseDir', DEFAULT_DATA_DIR)
    if not os.path.isabs(data_dir):
        data_dir = os.path.join(SCRIPT_DIR, data_dir)
    return data_dir

DATA_DIR = get_data_dir()
LOG_FILE = os.path.join(DATA_DIR, "push-log.json")
TODAY = datetime.now().strftime("%Y-%m-%d")
MONTH_FILE = os.path.join(DATA_DIR, datetime.now().strftime("%Y-%m") + ".json")

# 从配置读取 API 信息和推送目标
config = get_config()
api_config = config.get('api', {})
API_URL = api_config.get('url', '')
API_KEY = api_config.get('apiKey', '')
MODEL = api_config.get('model', 'glm-5')

push_config = config.get('push', {})
TARGET_USER_ID = push_config.get('targetUserId', '')
PUSH_CHANNEL = push_config.get('channel', 'feishu')
PUSH_ENABLED = push_config.get('enabled', False)

# 检查推送是否启用
if not PUSH_ENABLED:
    print("推送已禁用")
    exit(0)

# 检查今天是否已推送
if os.path.exists(LOG_FILE):
    with open(LOG_FILE) as f:
        log_data = json.load(f)
        if log_data.get("lastPushDate") == TODAY:
            print("今天已推送")
            exit(0)

# 更丰富的 prompt
prompt = """生成 5 条日常英语口语知识。

每条必须包含：
1. phrase - 英文句子/短语
2. meaning - 中文翻译
3. usage - 详细用法说明（1-2句话）

要求：
- 简单实用，适合日常对话
- 用法说明要包含使用场景和注意事项
- 不要重复

输出 JSON 数组格式：
[
  {"phrase": "I could use a coffee", "meaning": "我正好需要一杯咖啡", "usage": "当你感到疲惫想喝点东西时可以说，相当于 'I want a coffee' 但更地道"},
  ...
]

只输出 JSON，不要其他内容。"""

cmd = [
    "curl", "-s", API_URL,
    "-H", f"Authorization: Bearer {API_KEY}",
    "-H", "Content-Type: application/json",
    "-d", json.dumps({
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1000
    })
]

result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

try:
    data = json.loads(result.stdout)
    content = data.get('choices', [{}])[0].get('message', {}).get('content', '')
    
    start = content.find('[')
    end = content.rfind(']') + 1
    if start >= 0 and end > start:
        tips = json.loads(content[start:end])
    else:
        tips = json.loads(content)
except Exception as e:
    print(f"解析失败: {e}")
    tips = [
        {"phrase": "Got it, thanks!", "meaning": "明白了，谢谢！", "usage": "表示理解并感谢，常用于对话结束时"},
        {"phrase": "Sounds good to me", "meaning": "听起来不错", "usage": "表示同意对方的建议或提议"},
        {"phrase": "Take your time", "meaning": "慢慢来，不着急", "usage": "告诉对方不要着急，慢慢来"},
        {"phrase": "No problem", "meaning": "不客气/没问题", "usage": "回应感谢，或表示这不算事"},
        {"phrase": "I'm just kidding", "meaning": "我在开玩笑啦", "usage": "说完笑话后表示刚才是在开玩笑"},
    ]

tips = tips[:5]

# 构建消息
message = "📚 每日英语知识\n\n"
for i, tip in enumerate(tips, 1):
    message += f"{i}. **{tip.get('phrase', '')}**\n   📖 {tip.get('meaning', '')}\n   💡 {tip.get('usage', '')}\n\n"

# 记录到 JSON
os.makedirs(DATA_DIR, exist_ok=True)
if os.path.exists(MONTH_FILE):
    with open(MONTH_FILE, 'r', encoding='utf-8') as f:
        month_data = json.load(f)
else:
    month_data = {
        "month": datetime.now().strftime("%Y-%m"),
        "pushRecords": [],
        "vocabulary": {"totalCount": 0, "words": []},
        "errors": {"totalCount": 0, "grammar": [], "pronunciation": [], "wordChoice": []},
        "goodExpressions": {"totalCount": 0, "expressions": []},
        "statistics": {"totalPracticeDays": 0}
    }

if "pushRecords" not in month_data:
    month_data["pushRecords"] = []

today_found = False
for i, record in enumerate(month_data["pushRecords"]):
    if record.get("date") == TODAY:
        month_data["pushRecords"][i] = {"date": TODAY, "records": tips}
        today_found = True
        break

if not today_found:
    month_data["pushRecords"].append({
        "date": TODAY,
        "records": tips
    })

with open(MONTH_FILE, 'w', encoding='utf-8') as f:
    json.dump(month_data, f, ensure_ascii=False, indent=2)

with open(LOG_FILE, 'w') as f:
    json.dump({"lastPushDate": TODAY}, f)

# 发送消息
send_cmd = ["openclaw", "agent", "--channel", PUSH_CHANNEL, "--to", TARGET_USER_ID, "--message", message, "--deliver"]
subprocess.run(send_cmd, capture_output=True)

print(f"已推送 5 条知识（包含翻译和用法）")
