#!/usr/bin/env python3
import os
import json
import requests
from datetime import datetime

APP_ID = "cli_a92b19fbc278dbd6"
APP_SECRET = "WFsYhmcEZnRjL4c1ClotIeHhoq5568Sp"

CHATS = [
    ("oc_60c795e2e04eefc3d09eb49da4df15a5", "养虾乐园🦞"),
    ("oc_3cc1c4abbc093b180cb0b75e40bb6e1b", "🦞龙虾聚会")
]

def get_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    resp = requests.post(url, json={"app_id": APP_ID, "app_secret": APP_SECRET})
    return resp.json().get("tenant_access_token")

def extract_text(content):
    if not content:
        return ""
    try:
        if content.startswith("["):
            data = json.loads(content)
            if isinstance(data, list) and len(data) > 0:
                text_data = data[0]
                if isinstance(text_data, list):
                    result = ""
                    for item in text_data:
                        if item.get("tag") == "text":
                            result += item.get("text", "")
                    return result
        elif content.startswith("{"):
            data = json.loads(content)
            return data.get("text", "")
        else:
            return content
    except:
        return content[:200] if content else ""
    return ""

def get_messages(chat_id, token):
    url = "https://open.feishu.cn/open-apis/im/v1/messages"
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "container_id": chat_id,
        "container_id_type": "chat",
        "page_size": 100
    }
    
    resp = requests.get(url, headers=headers, params=params)
    data = resp.json()
    
    if data.get("code") != 0:
        print(f"Error: {data.get('msg')}")
        return []
    
    messages = []
    for msg in data.get("data", {}).get("items", []):
        if msg.get("msg_type") == "system":
            continue
        
        content = msg.get("body", {}).get("content", "")
        text = extract_text(content)
        
        if len(text) > 5:
            messages.append({
                "time": datetime.fromtimestamp(int(msg.get("create_time", 0)) / 1000).strftime("%Y-%m-%d %H:%M"),
                "content": text[:500]
            })
    
    return messages

def analyze_messages(messages, chat_name):
    if not messages:
        return None
    
    analysis = {
        "chat": chat_name,
        "message_count": len(messages),
        "insights": [],
        "recommendations": []
    }
    
    all_content = " ".join([m["content"] for m in messages]).lower()
    
    insights_map = {
        "科技领袖追踪需求": ["@sama", "@elonmusk", "科技圈", "大佬", "vc", "投资人"],
        "Agent稳定性问题": ["失灵", "连接", "无响应", "卡住"],
        "内容创作需求": ["简报", "整理", "文章", "生成"],
        "新用户引导": ["你是谁", "介绍", "怎么"],
        "产品发布": ["大会", "发布", "上线", "app", "web"]
    }
    
    for insight, keywords in insights_map.items():
        if any(kw in all_content for kw in keywords):
            analysis["insights"].append(insight)
    
    return analysis

def main():
    token = get_token()
    if not token:
        print("Failed to get token")
        return
    
    analyses = []
    for chat_id, chat_name in CHATS:
        messages = get_messages(chat_id, token)
        analysis = analyze_messages(messages, chat_name)
        if analysis:
            analyses.append(analysis)
    
    if not analyses:
        print("No messages to analyze")
        return
    
    # Generate report
    report = []
    report.append("📚 飞书群学习报告")
    report.append(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report.append(f"分析群聊: {len(analyses)} 个\n")
    
    for analysis in analyses:
        report.append(f"📌 {analysis['chat']}")
        report.append(f"   消息数: {analysis['message_count']}")
        if analysis['insights']:
            report.append(f"   发现: {', '.join(analysis['insights'])}")
        report.append("")
    
    print("\n".join(report))
    
    # Save to memory
    memory_dir = os.path.expanduser("~/.openclaw/workspace/memory")
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = os.path.join(memory_dir, f"{today}.md")
    
    entry = f"\n## 🕐 {datetime.now().strftime('%H:%M')} - 群学习分析\n\n"
    for analysis in analyses:
        entry += f"### {analysis['chat']}\n"
        entry += f"- 消息数: {analysis['message_count']}\n"
        if analysis['insights']:
            entry += f"- 发现: {', '.join(analysis['insights'])}\n"
        entry += "\n"
    
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(entry)
    
    print(f"已保存到 {log_file}")

if __name__ == "__main__":
    main()
