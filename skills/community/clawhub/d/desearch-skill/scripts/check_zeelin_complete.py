#!/usr/bin/env python3
"""
Zeelin 任务完成检查脚本
"""

import os
import json
import requests
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
REPORTS_DIR = os.path.join(SKILL_DIR, "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

CONFIG_FILE = os.path.expanduser("~/.openclaw/zeelin-config.json")
STATUS_FILE = os.path.join(REPORTS_DIR, "zeelin-research-status.json")
NOTIFIED_FILE = os.path.join(REPORTS_DIR, "zeelin-last-notified.json")

def get_api_key():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            config = json.load(f)
            return config.get("api_key")
    return None

def check_current_session():
    api_key = get_api_key()
    if not api_key:
        return
    
    if not os.path.exists(STATUS_FILE):
        return
    
    with open(STATUS_FILE) as f:
        status = json.load(f)
    
    session_id = status.get("session_id")
    query = status.get("query", "")
    
    if not session_id:
        return
    
    # 检查是否已通知过
    if os.path.exists(NOTIFIED_FILE):
        with open(NOTIFIED_FILE) as f:
            notified = json.load(f)
        if notified.get("session_id") == session_id:
            return
    
    # 直接检查API状态
    try:
        url = "https://desearch.zeelin.cn/api/conversation/status"
        headers = {"x-api-key": api_key}
        params = {"sessionId": session_id}
        response = requests.get(url, headers=headers, params=params, timeout=30)
        data = response.json()
        
        if data.get("code") != 200:
            return
        
        api_data = data.get("data", {})
        api_status = api_data.get("status")
        md_url = api_data.get("mdUrl", "")
        
        if api_status == 2 and md_url:
            progress = status.get("progress", "")
            output_file = None
            if "完成:" in progress:
                output_file = progress.split("完成:")[1].strip()
                if not os.path.exists(output_file):
                    output_file = None
            
            if not output_file:
                r = requests.get(md_url, timeout=60)
                if r.status_code == 200:
                    safe_query = "".join(c for c in query if c.isalnum() or c in " -_")[:20]
                    output_file = f"{REPORTS_DIR}/zeelin_{safe_query}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
                    with open(output_file, "w", encoding="utf-8") as f:
                        f.write(r.text)
            
            if output_file:
                print(f"🎉 研究任务已完成！\n\n主题：{query}\n文件：{output_file}")
                
                # 记录已通知
                with open(NOTIFIED_FILE, "w") as f:
                    json.dump({"session_id": session_id, "query": query}, f, ensure_ascii=False)
                return
                
    except:
        pass

if __name__ == "__main__":
    check_current_session()
