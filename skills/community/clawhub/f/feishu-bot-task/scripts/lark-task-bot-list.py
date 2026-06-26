#!/usr/bin/env python3
"""
lark-task-bot-list.py
Bot身份查询自己负责的任务列表（使用v1 API）
直接调用飞书v1任务接口，绕过lark-cli封装的v2接口对bot的身份限制
"""

import sys
import json
import urllib.request
import urllib.parse
import os

# 从环境变量读取飞书应用凭证（OpenClaw飞书插件会自动注入）
APP_ID = os.environ.get("FEISHU_APP_ID", "")
APP_SECRET = os.environ.get("FEISHU_APP_SECRET", "")

if not APP_ID or not APP_SECRET:
    print(json.dumps({"code": 1, "msg": "Missing FEISHU_APP_ID or FEISHU_APP_SECRET in environment"}, ensure_ascii=False))
    sys.exit(1)

def get_tenant_token():
    """获取tenant_access_token"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    data = json.dumps({"app_id": APP_ID, "app_secret": APP_SECRET}).encode()
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as resp:
        result = json.load(resp)
    return result.get("tenant_access_token", "")

def list_bot_tasks(token, page_size=20, page_token=""):
    """调用v1接口获取bot自己作为负责人的任务"""
    base_url = "https://open.feishu.cn/open-apis/task/v1/tasks"
    params = {"page_size": page_size}
    if page_token:
        params["page_token"] = page_token
    
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req) as resp:
        return json.load(resp)

def main():
    # 获取token
    token = get_tenant_token()
    if not token:
        print(json.dumps({"code": 1, "msg": "Failed to get tenant_access_token"}, ensure_ascii=False))
        sys.exit(1)
    
    all_tasks = []
    page_token = ""
    
    # 分页获取所有任务
    while True:
        result = list_bot_tasks(token, page_size=20, page_token=page_token)
        if result.get("code") != 0:
            print(json.dumps(result, ensure_ascii=False))
            sys.exit(1)
        
        data = result.get("data", {})
        items = data.get("items", [])
        all_tasks.extend(items)
        
        has_more = data.get("has_more", False)
        if not has_more:
            break
        page_token = data.get("page_token", "")
        if not page_token:
            break
    
    # 输出完整结果
    print(json.dumps({
        "code": 0,
        "data": {
            "items": all_tasks,
            "total": len(all_tasks)
        }
    }, ensure_ascii=False))

if __name__ == "__main__":
    main()
