#!/usr/bin/env python3
import json
import os
import sys
from datetime import datetime

# 读取配置
SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_FILE = os.path.join(SCRIPT_DIR, 'config.json')
DEFAULT_DATA_DIR = os.path.join(SCRIPT_DIR, 'practice-data')

def get_config():
    """读取配置文件"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}

def get_data_dir():
    """获取数据目录"""
    config = get_config()
    data_dir = config.get('data', {}).get('baseDir', DEFAULT_DATA_DIR)
    # 相对路径转绝对路径
    if not os.path.isabs(data_dir):
        data_dir = os.path.join(SCRIPT_DIR, data_dir)
    return data_dir

DATA_DIR = get_data_dir()
config = get_config()
DEFAULT_USER_NAME = config.get('user', {}).get('name', '朋友')
DEFAULT_LEARNING_GOAL = config.get('user', {}).get('learningGoal', '日常英语口语对话')
MONTH_FILE = os.path.join(DATA_DIR, datetime.now().strftime("%Y-%m") + ".json")

def load_data():
    """加载当月数据"""
    os.makedirs(DATA_DIR, exist_ok=True)
    if os.path.exists(MONTH_FILE):
        with open(MONTH_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        return {
            "version": "1.0",
            "lastUpdated": datetime.now().isoformat(),
            "month": datetime.now().strftime("%Y-%m"),
            "user": {"name": DEFAULT_USER_NAME, "learningGoal": DEFAULT_LEARNING_GOAL},
            "vocabulary": {"totalCount": 0, "words": []},
            "errors": {"totalCount": 0, "grammar": [], "pronunciation": [], "wordChoice": []},
            "goodExpressions": {"totalCount": 0, "expressions": []},
            "dailyRecords": {},
            "statistics": {
                "totalPracticeDays": 0,
                "totalVocabulary": 0,
                "totalErrors": 0,
                "totalGoodExpressions": 0,
                "streak": 0
            }
        }

def save_data(data):
    """保存数据"""
    data["lastUpdated"] = datetime.now().isoformat()
    with open(MONTH_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_vocabulary(word, meaning, example):
    """添加词汇"""
    data = load_data()
    vid = f"v{len(data['vocabulary']['words']) + 1:03d}"
    data['vocabulary']['words'].append({
        "id": vid,
        "word": word,
        "meaning": meaning,
        "example": example,
        "learnedDate": datetime.now().strftime("%Y-%m-%d"),
        "reviewCount": 0
    })
    data['vocabulary']['totalCount'] += 1
    data['statistics']['totalVocabulary'] += 1
    save_data(data)
    return f"已添加词汇: {word}"

def add_error(error_text, correct_text, category):
    """添加错误"""
    data = load_data()
    cat_key = "grammar"  # 默认归类为语法错误
    if "发音" in category or "pronunciation" in category.lower():
        cat_key = "pronunciation"
    elif "用词" in category or "word" in category.lower():
        cat_key = "wordChoice"
    
    eid = f"e{len(data['errors'][cat_key]) + 1:03d}"
    data['errors'][cat_key].append({
        "id": eid,
        "error": error_text,
        "correct": correct_text,
        "category": category,
        "times": 1,
        "firstDate": datetime.now().strftime("%Y-%m-%d"),
        "lastDate": datetime.now().strftime("%Y-%m-%d")
    })
    data['errors']['totalCount'] += 1
    data['statistics']['totalErrors'] += 1
    save_data(data)
    return f"已记录错误: {error_text} -> {correct_text}"

def add_good_expression(expression, meaning, category):
    """添加好表达"""
    data = load_data()
    gid = f"g{len(data['goodExpressions']['expressions']) + 1:03d}"
    data['goodExpressions']['expressions'].append({
        "id": gid,
        "expression": expression,
        "meaning": meaning,
        "category": category,
        "learnedDate": datetime.now().strftime("%Y-%m-%d")
    })
    data['goodExpressions']['totalCount'] += 1
    data['statistics']['totalGoodExpressions'] += 1
    save_data(data)
    return f"已记录好表达: {expression}"

def add_push_record(records_json):
    """添加推送记录 - 传入JSON字符串或列表"""
    data = load_data()
    
    # 初始化 pushRecords
    if 'pushRecords' not in data:
        data['pushRecords'] = []
    
    # 解析输入
    if isinstance(records_json, str):
        try:
            records = json.loads(records_json)
        except:
            records = json.loads(records_json.replace("'", '"'))
    else:
        records = records_json
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 检查今天是否已有记录，有则覆盖
    for i, rec in enumerate(data['pushRecords']):
        if rec.get('date') == today:
            data['pushRecords'][i] = {"date": today, "records": records}
            break
    else:
        data['pushRecords'].append({"date": today, "records": records})
    
    save_data(data)
    return f"已记录推送内容: {len(records)} 条"

def get_monthly_summary():
    """获取月度总结"""
    data = load_data()
    stats = data.get('statistics', {})
    vocab = data.get('vocabulary', {})
    errors = data.get('errors', {})
    good_expr = data.get('goodExpressions', {})
    
    summary = f"""📊 {data.get('month', datetime.now().strftime('%Y-%m'))} 月度总结

🗓️ 练习天数: {stats.get('totalPracticeDays', 0)} 天
📚 新学词汇: {stats.get('totalVocabulary', 0)} 个
❌ 错误次数: {stats.get('totalErrors', 0)} 次
✨ 好表达: {stats.get('totalGoodExpressions', 0)} 个

📖 词汇列表:
"""
    for w in vocab.get('words', [])[:5]:
        summary += f"  • {w['word']} - {w['meaning']}\n"
    if len(vocab.get('words', [])) > 5:
        summary += f"  ... 还有 {len(vocab['words']) - 5} 个\n"
    
    return summary

# 命令行接口
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: update-english-data.py <命令> [参数]")
        print("命令:")
        print("  push <json数组>         # 记录推送内容")
        print("  vocab <单词> <中文意思> <例句>")
        print("  error <错误句子> <正确句子> <分类>")
        print("  good <好表达> <中文意思> <分类>")
        print("  summary")
        sys.exit(1)
    
    cmd = sys.argv[1]
    if cmd == "vocab" and len(sys.argv) >= 5:
        print(add_vocabulary(sys.argv[2], sys.argv[3], sys.argv[4]))
    elif cmd == "error" and len(sys.argv) >= 5:
        print(add_error(sys.argv[2], sys.argv[3], sys.argv[4]))
    elif cmd == "good" and len(sys.argv) >= 5:
        print(add_good_expression(sys.argv[2], sys.argv[3], sys.argv[4]))
    elif cmd == "summary":
        print(get_monthly_summary())
    elif cmd == "push" and len(sys.argv) >= 3:
        print(add_push_record(' '.join(sys.argv[2:])))
    else:
        print("无效命令")
        sys.exit(1)
