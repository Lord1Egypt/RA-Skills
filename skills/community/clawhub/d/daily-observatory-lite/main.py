#!/usr/bin/env python3
"""
Daily-Observatory Lite
每日自動健康檢查 + 情緒追蹤 + 主動預警
"""

import json
import os
import sys
from datetime import datetime

# Import modules
from system_health import check_system_health
from emotion_tracker import analyze_emotion_trend
from todo_watcher import check_todo_alerts
from pusher import send_telegram_message

def load_config():
    """載入設定檔"""
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_report(config):
    """生成每日報告"""
    report = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "time": datetime.now().strftime("%H:%M"),
        "system_health": {},
        "emotion_trend": {},
        "todo_alerts": {},
        "summary": ""
    }
    
    # 1. 系統健康檢查
    if config["modules"]["system_health"]:
        report["system_health"] = check_system_health()
    
    # 2. 情緒追蹤
    if config["modules"]["emotion_tracking"]:
        report["emotion_trend"] = analyze_emotion_trend()
    
    # 3. 待辦預警
    if config["modules"]["todo_alerts"]:
        report["todo_alerts"] = check_todo_alerts()
    
    # 4. 生成摘要
    report["summary"] = generate_summary(report)
    
    return report

def generate_summary(report):
    """生成摘要"""
    issues = []
    
    # 系統問題
    if report["system_health"].get("gateway_status") != "running":
        issues.append("系統正常")
    
    # 情緒異常
    if report["emotion_trend"].get("trend") == "下降":
        issues.append("情緒下降")
    
    # 待辦卡住
    p0_stuck = report["todo_alerts"].get("p0_stuck", 0)
    p1_stuck = report["todo_alerts"].get("p1_stuck", 0)
    if p0_stuck > 0:
        issues.append(f"{p0_stuck} 個 P0 任務卡住")
    if p1_stuck > 0:
        issues.append(f"{p1_stuck} 個 P1 任務卡住")
    
    if not issues:
        return "🌟 今日一切正常，保持節奏！"
    else:
        return f"⚠️ 需要注意：{', '.join(issues)}"

def format_message(report):
    """格式化訊息"""
    date = report["date"]
    time = report["time"]
    
    # 系統健康
    system = report["system_health"]
    gateway = system.get("gateway_status", "unknown")
    memory = system.get("memory_status", "unknown")
    
    # 情緒
    emotion = report["emotion_trend"]
    today_score = emotion.get("today_score", 0)
    trend = emotion.get("trend", "→")
    
    # 待辦
    todo = report["todo_alerts"]
    p0_stuck = todo.get("p0_stuck", 0)
    p1_stuck = todo.get("p1_stuck", 0)
    
    # 建議時間
    is_morning = time < "12:00"
    emoji = "🌅" if is_morning else "🌙"
    title = "早安日誌" if is_morning else "晚安日誌"
    
    message = f"""
{emoji} Daily-Observatory Lite · {date} {title}

✅ 系統健康
├─ Gateway: {gateway}
└─ 記憶結構: {memory}

😐 情緒溫度
├─ 今日: {today_score}
└─ 趨勢: {trend}

⚠️ 待辦預警
├─ P0 卡住: {p0_stuck} 個
└─ P1 卡住: {p1_stuck} 個

💡 建議: {report["summary"]}
"""
    
    return message.strip()

def main():
    """主程式"""
    # 載入設定
    config = load_config()
    
    # 生成報告
    report = generate_report(config)
    
    # 格式化訊息
    message = format_message(report)
    
    # 儲存報告
    report_path = os.path.join(
        os.path.dirname(__file__),
        "memory",
        f"{report['date']}-daily.md"
    )
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(message)
    
    # 推播到 Telegram
    if config["channels"]["telegram"]:
        chat_id = config["channels"]["telegram_chat_id"]
        if chat_id != "YOUR_CHAT_ID":
            send_telegram_message(chat_id, message)
        else:
            print("⚠️  請設定 telegram_chat_id")
    
    # 輸出到終端
    print(message)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
