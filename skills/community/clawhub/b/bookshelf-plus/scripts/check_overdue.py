#!/usr/bin/env python3
"""
逾期檢查腳本
由 Cron Job 每日呼叫，檢查逾期書籍並輸出提醒訊息
"""

import sys
import json
import datetime
import argparse
import urllib.request
import urllib.parse

NOTION_KEY = ""
DATABASE_ID = ""


def notion_headers():
    return {
        "Authorization": f"Bearer {NOTION_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }


def check_overdue() -> list:
    """查詢所有在借書籍，區分即將到期 / 已逾期"""
    import urllib.request

    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)

    # 查詢在借狀態的書籍
    body = json.dumps({
        "page_size": 100,
        "filter": {
            "property": "標籤",
            "multi_select": {"contains": "在借"}
        }
    }).encode()

    req = urllib.request.Request(url, data=body, headers=notion_headers(), method="POST")
    with urllib.request.urlopen(req, timeout=15) as r:
        data = json.loads(r.read())

    overdue_list = []
    due_soon_list = []

    for page in data.get("results", []):
        props = page["properties"]
        title = props.get("名稱", {}).get("title", [{}])[0].get("plain_text", "未知書名")
        borrowed_by = props.get("借出給", {}).get("rich_text", [{}])[0].get("plain_text", "")
        due_date_str = props.get("預定還日", {}).get("date", {}).get("start", "")

        if not due_date_str:
            continue

        try:
            due_date = datetime.date.fromisoformat(due_date_str)
        except ValueError:
            continue

        if due_date < today:
            days_late = (today - due_date).days
            overdue_list.append({
                "title": title,
                "borrowed_by": borrowed_by,
                "due_date": due_date_str,
                "days_overdue": days_late,
            })
        elif due_date == tomorrow:
            due_soon_list.append({
                "title": title,
                "borrowed_by": borrowed_by,
                "due_date": due_date_str,
            })

    return overdue_list, due_soon_list


def main():
    parser = argparse.ArgumentParser(description="逾期書籍檢查")
    parser.add_argument("--api-key", required=True, help="Notion API Key")
    parser.add_argument("--database-id", required=True, help="Notion Database ID")
    parser.add_argument("--format", choices=["json", "text"], default="text")
    args = parser.parse_args()

    global NOTION_KEY, DATABASE_ID
    NOTION_KEY = args.api_key
    DATABASE_ID = args.database_id

    overdue, due_soon = check_overdue()

    today = datetime.date.today().isoformat()

    result = {
        "check_date": today,
        "overdue_count": len(overdue),
        "due_soon_count": len(due_soon),
        "overdue": overdue,
        "due_soon": due_soon,
    }

    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(1 if overdue else 0)

    # text 格式（預設，人類可讀）
    print(f"📚 逾期檢查報告（{today}）\n")

    if overdue:
        print(f"⚠️  逾期書籍（共 {len(overdue)} 本）：")
        for i, b in enumerate(overdue, 1):
            print(f"  {i}. 《{b['title']}》")
            print(f"     借給：{b['borrowed_by']}｜原定還日：{b['due_date']}｜逾期 {b['days_overdue']} 天")
        print()

    if due_soon:
        print(f"⏰ 明日到期（共 {len(due_soon)} 本）：")
        for i, b in enumerate(due_soon, 1):
            print(f"  {i}. 《{b['title']}》借給 {b['borrowed_by']}")
        print()

    if not overdue and not due_soon:
        print("✅ 目前沒有逾期或即將到期的書籍，書庫狀態良好！")

    # exit code：若有逾期則返回 1，供 Cron 判斷是否發出通知
    sys.exit(1 if overdue else 0)


if __name__ == "__main__":
    main()
