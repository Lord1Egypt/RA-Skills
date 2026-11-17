#!/usr/bin/env python3
"""
借還生命週期管理腳本
用法：
  borrow  --isbn/--title  --borrower  --due-date  [--api-key] [--database-id]
  return  --isbn/--title  [--api-key] [--database-id]
  list    [--status all|borrowed|returned]  [--api-key] [--database-id]
"""

import sys
import json
import argparse
import datetime

try:
    from notion_client import AsyncNotion, NotionClient
except ImportError:
    print("請先安裝依賴：pip3 install notion-client", file=sys.stderr)
    sys.exit(1)


NOTION_KEY = ""
DATABASE_ID = ""


def notion_headers():
    return {
        "Authorization": f"Bearer {NOTION_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }


def search_book(query: str) -> dict | None:
    """在 Notion 中搜尋書籍"""
    import urllib.request

    url = "https://api.notion.com/v1/search"
    body = json.dumps({"query": query, "filter": {"property": "object", "value": "page"}}).encode()
    req = urllib.request.Request(url, data=body, headers=notion_headers(), method="POST")
    with urllib.request.urlopen(req, timeout=15) as r:
        data = json.loads(r.read())
    results = data.get("results", [])
    if not results:
        return None
    return results[0]


def update_page(page_id: str, properties: dict) -> bool:
    """更新 Notion Page 屬性"""
    import urllib.request

    url = f"https://api.notion.com/v1/pages/{page_id}"
    body = json.dumps({"properties": properties}).encode()
    req = urllib.request.Request(url, data=body, headers=notion_headers(), method="PATCH")
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.status == 200


def cmd_borrow(args):
    global NOTION_KEY, DATABASE_ID
    NOTION_KEY = args.api_key or NOTION_KEY
    DATABASE_ID = args.database_id or DATABASE_ID

    if not NOTION_KEY or not DATABASE_ID:
        print("錯誤：請提供 --api-key 和 --database-id", file=sys.stderr)
        sys.exit(1)

    # 搜尋書籍
    query = args.isbn or args.title
    page = search_book(query)
    if not page:
        print(f"找不到書籍：{query}", file=sys.stderr)
        sys.exit(1)

    page_id = page["id"]
    title = page["properties"].get("名稱", {}).get("title", [{}])[0].get("plain_text", query)

    # 組合更新屬性
    due_date = args.due_date or (datetime.date.today() + datetime.timedelta(days=30)).isoformat()
    borrowed_date = args.borrowed_date or datetime.date.today().isoformat()

    properties = {
        "借出給": {"rich_text": [{"text": {"content": args.borrower}}]},
        "借出日期": {"date": {"start": borrowed_date}},
        "預定還日": {"date": {"start": due_date}},
    }

    # 更新 Tags：移除「在借」，確保有
    tags_resp = search_book(query)
    current_tags = tags_resp["properties"].get("Tags", {}).get("multi_select", [])
    current_tag_names = [t["name"] for t in current_tags]
    if "在借" not in current_tag_names:
        new_tags = current_tag_names + ["在借"]
        properties["標籤"] = {"multi_select": [{"name": t} for t in new_tags]}

    success = update_page(page_id, properties)

    if success:
        print(json.dumps({
            "status": "success",
            "action": "borrow",
            "book": title,
            "borrower": args.borrower,
            "borrowed_date": borrowed_date,
            "due_date": due_date,
        }, ensure_ascii=False, indent=2))
    else:
        print(json.dumps({"status": "error", "message": "更新失敗"}, ensure_ascii=False))
        sys.exit(1)


def cmd_return(args):
    global NOTION_KEY, DATABASE_ID
    NOTION_KEY = args.api_key or NOTION_KEY
    DATABASE_ID = args.database_id or DATABASE_ID

    if not NOTION_KEY or not DATABASE_ID:
        print("錯誤：請提供 --api-key 和 --database-id", file=sys.stderr)
        sys.exit(1)

    query = args.isbn or args.title
    page = search_book(query)
    if not page:
        print(f"找不到書籍：{query}", file=sys.stderr)
        sys.exit(1)

    page_id = page["id"]
    title = page["properties"].get("名稱", {}).get("title", [{}])[0].get("plain_text", query)

    today = datetime.date.today().isoformat()

    # 檢查是否逾期
    due_date_str = page["properties"].get("預定還日", {}).get("date", {}).get("start", "")
    is_overdue = False
    if due_date_str:
        due = datetime.date.fromisoformat(due_date_str)
        is_overdue = today > due_date_str

    properties = {
        "歸還日期": {"date": {"start": today}},
    }

    # 移除「在借」標籤
    tags_resp = search_book(query)
    current_tags = tags_resp["properties"].get("Tags", {}).get("multi_select", [])
    current_tag_names = [t["name"] for t in current_tags]
    new_tag_names = [t for t in current_tag_names if t != "在借"]
    if is_overdue:
        new_tag_names = [t for t in new_tag_names if t != "逾期"]
        new_tag_names.append("逾期")
    properties["標籤"] = {"multi_select": [{"name": t} for t in new_tag_names]}

    success = update_page(page_id, properties)

    if success:
        print(json.dumps({
            "status": "success",
            "action": "return",
            "book": title,
            "returned_date": today,
            "overdue": is_overdue,
        }, ensure_ascii=False, indent=2))
    else:
        print(json.dumps({"status": "error", "message": "更新失敗"}, ensure_ascii=False))
        sys.exit(1)


def cmd_list(args):
    global NOTION_KEY, DATABASE_ID
    NOTION_KEY = args.api_key or NOTION_KEY
    DATABASE_ID = args.database_id or DATABASE_ID

    if not NOTION_KEY or not DATABASE_ID:
        print("錯誤：請提供 --api-key 和 --database-id", file=sys.stderr)
        sys.exit(1)

    import urllib.request

    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    body = json.dumps({"page_size": 100}).encode()
    req = urllib.request.Request(url, data=body, headers=notion_headers(), method="POST")
    with urllib.request.urlopen(req, timeout=15) as r:
        data = json.loads(r.read())

    results = data.get("results", [])
    books = []
    for page in results:
        props = page["properties"]
        tags = [t["name"] for t in props.get("標籤", {}).get("multi_select", [])]
        title = props.get("名稱", {}).get("title", [{}])[0].get("plain_text", "")
        author = props.get("作者", {}).get("rich_text", [{}])[0].get("plain_text", "")
        borrowed_by = props.get("借出給", {}).get("rich_text", [{}])[0].get("plain_text", "")
        borrowed_date = props.get("借出日期", {}).get("date", {}).get("start", "")
        due_date = props.get("預定還日", {}).get("date", {}).get("start", "")

        if args.status == "borrowed" and "在借" not in tags:
            continue
        if args.status == "returned" and "在借" in tags:
            continue

        books.append({
            "title": title,
            "author": author,
            "tags": tags,
            "borrowed_by": borrowed_by,
            "borrowed_date": borrowed_date,
            "due_date": due_date,
        })

    print(json.dumps({"status": "success", "count": len(books), "books": books}, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description="借還生命週期管理")
    sub = parser.add_subparsers(dest="cmd")

    p_borrow = sub.add_parser("borrow", help="借出書籍")
    p_borrow.add_argument("--isbn", help="ISBN")
    p_borrow.add_argument("--title", help="書名")
    p_borrow.add_argument("--borrower", required=True, help="借書人")
    p_borrow.add_argument("--due-date", help="預定還日 YYYY-MM-DD")
    p_borrow.add_argument("--borrowed-date", help="借出日 YYYY-MM-DD")
    p_borrow.add_argument("--api-key", default="", help="Notion API Key")
    p_borrow.add_argument("--database-id", default="", help="Notion Database ID")

    p_return = sub.add_parser("return", help="歸還書籍")
    p_return.add_argument("--isbn", help="ISBN")
    p_return.add_argument("--title", help="書名")
    p_return.add_argument("--api-key", default="", help="Notion API Key")
    p_return.add_argument("--database-id", default="", help="Notion Database ID")

    p_list = sub.add_parser("list", help="列出借出中的書")
    p_list.add_argument("--status", choices=["all", "borrowed", "returned"], default="borrowed")
    p_list.add_argument("--api-key", default="", help="Notion API Key")
    p_list.add_argument("--database-id", default="", help="Notion Database ID")

    args = parser.parse_args()

    if args.cmd == "borrow":
        cmd_borrow(args)
    elif args.cmd == "return":
        cmd_return(args)
    elif args.cmd == "list":
        cmd_list(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
