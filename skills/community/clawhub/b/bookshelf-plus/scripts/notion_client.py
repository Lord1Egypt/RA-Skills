#!/usr/bin/env python3
"""
Notion CRUD 腳本（Bookshelf Plus 版）
支援：新增書籍、查詢、更新欄位、刪除、統計
"""

import sys
import json
import argparse
import urllib.request
import urllib.parse
import urllib.error


NOTION_KEY = ""
DATABASE_ID = ""


def notion_headers():
    return {
        "Authorization": f"Bearer {NOTION_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }


def notion_url(path: str) -> str:
    return f"https://api.notion.com/v1{path}"


def api_post(path: str, body: dict):
    data = json.dumps(body).encode()
    req = urllib.request.Request(
        notion_url(path), data=data,
        headers=notion_headers(), method="POST"
    )
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())


def api_patch(path: str, body: dict):
    data = json.dumps(body).encode()
    req = urllib.request.Request(
        notion_url(path), data=data,
        headers=notion_headers(), method="PATCH"
    )
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())


def api_get(path: str):
    req = urllib.request.Request(
        notion_url(path),
        headers=notion_headers(), method="GET"
    )
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())


# ── 工具函式 ────────────────────────────────────────────

def make_title(text: str):
    return {"title": [{"text": {"content": text[:2000]}}]}

def make_text(text: str):
    return {"rich_text": [{"text": {"content": text[:2000]}}]}

def make_select(name: str):
    return {"select": {"name": name}} if name else {"select": None}

def make_multi_select(names: list):
    return {"multi_select": [{"name": n} for n in names if n]}

def make_date(date_str: str):
    return {"date": {"start": date_str}} if date_str else {"date": None}

def make_number(n: int | float):
    return {"number": n} if n else {"number": 0}


def search_pages(query: str, filter_object=True) -> list:
    body = {"query": query, "page_size": 10}
    if filter_object:
        body["filter"] = {"property": "object", "value": "page"}
    result = api_post("/search", body)
    return result.get("results", [])


# ── 命令 ────────────────────────────────────────────────

def cmd_add(args):
    global NOTION_KEY, DATABASE_ID
    NOTION_KEY = args.api_key or NOTION_KEY
    DATABASE_ID = args.database_id or DATABASE_ID

    if not NOTION_KEY or not DATABASE_ID:
        print("錯誤：缺少 --api-key 或 --database-id", file=sys.stderr)
        sys.exit(1)

    properties = {
        "名稱": make_title(args.title),
    }
    if args.author:
        properties["作者"] = make_text(args.author)
    if args.isbn:
        properties["ISBN"] = make_text(args.isbn)
    if args.category:
        properties["分類"] = make_select(args.category)
    if args.tags:
        properties["標籤"] = make_multi_select(args.tags.split(","))
    if args.total_pages:
        properties["總頁數"] = make_number(int(args.total_pages))
    if args.location:
        properties["所在位置"] = make_text(args.location)
    if args.language:
        properties["語言"] = make_select(args.language)
    if args.cover_url:
        properties["封面圖"] = make_text(args.cover_url)
    if args.notes:
        properties["備註"] = make_text(args.notes)

    result = api_post("/pages", {
        "parent": {"database_id": DATABASE_ID},
        "properties": properties,
    })

    page_id = result.get("id", "")
    title = result.get("properties", {}).get("名稱", {}).get("title", [{}])[0].get("plain_text", args.title)
    print(json.dumps({"status": "success", "page_id": page_id, "title": title}, ensure_ascii=False, indent=2))


def cmd_search(args):
    global NOTION_KEY, DATABASE_ID
    NOTION_KEY = args.api_key or NOTION_KEY
    DATABASE_ID = args.database_id or DATABASE_ID

    pages = search_pages(args.query)
    if not pages:
        print(json.dumps({"status": "not_found", "query": args.query}, ensure_ascii=False))
        sys.exit(1)

    books = []
    for p in pages:
        props = p["properties"]
        books.append({
            "id": p["id"],
            "title": props.get("名稱", {}).get("title", [{}])[0].get("plain_text", ""),
            "author": props.get("作者", {}).get("rich_text", [{}])[0].get("plain_text", ""),
            "isbn": props.get("ISBN", {}).get("rich_text", [{}])[0].get("plain_text", ""),
            "category": props.get("分類", {}).get("select", {}).get("name", ""),
            "tags": [t["name"] for t in props.get("標籤", {}).get("multi_select", [])],
            "borrowed_by": props.get("借出給", {}).get("rich_text", [{}])[0].get("plain_text", ""),
        })
    print(json.dumps({"status": "success", "count": len(books), "books": books}, ensure_ascii=False, indent=2))


def cmd_update(args):
    global NOTION_KEY, DATABASE_ID
    NOTION_KEY = args.api_key or NOTION_KEY
    DATABASE_ID = args.database_id or DATABASE_ID

    if not args.page_id and args.title:
        pages = search_pages(args.title)
        if pages:
            args.page_id = pages[0]["id"]
        else:
            print(f"找不到書籍：{args.title}", file=sys.stderr)
            sys.exit(1)

    properties = {}
    if args.author is not None:
        properties["作者"] = make_text(args.author)
    if args.isbn is not None:
        properties["ISBN"] = make_text(args.isbn)
    if args.category is not None:
        properties["分類"] = make_select(args.category) if args.category else {"select": None}
    if args.tags is not None:
        properties["標籤"] = make_multi_select(args.tags.split(",")) if args.tags else {"multi_select": []}
    if args.pages_read is not None:
        properties["閱讀頁數"] = make_number(int(args.pages_read))
    if args.total_pages is not None:
        properties["總頁數"] = make_number(int(args.total_pages))
    if args.location is not None:
        properties["所在位置"] = make_text(args.location)
    if args.notes is not None:
        properties["備註"] = make_text(args.notes)

    if not properties:
        print("錯誤：未提供任何要更新的欄位", file=sys.stderr)
        sys.exit(1)

    result = api_patch(f"/pages/{args.page_id}", {"properties": properties})
    print(json.dumps({"status": "success", "page_id": result.get("id", "")}, ensure_ascii=False))


def cmd_stats(args):
    global NOTION_KEY, DATABASE_ID
    NOTION_KEY = args.api_key or NOTION_KEY
    DATABASE_ID = args.database_id or DATABASE_ID

    result = api_post(f"/databases/{DATABASE_ID}/query", {"page_size": 100})
    pages = result.get("results", [])

    stats = {
        "total": len(pages),
        "categories": {},
        "tags": {},
        "borrowed": 0,
    }

    for p in pages:
        props = p["properties"]
        cat = props.get("分類", {}).get("select", {}).get("name", "")
        if cat:
            stats["categories"][cat] = stats["categories"].get(cat, 0) + 1
        tags = [t["name"] for t in props.get("標籤", {}).get("multi_select", [])]
        for t in tags:
            stats["tags"][t] = stats["tags"].get(t, 0) + 1
        if "在借" in tags:
            stats["borrowed"] += 1

    print(json.dumps({"status": "success", "stats": stats}, ensure_ascii=False, indent=2))


def cmd_delete(args):
    """Archive（軟刪除）書籍頁面"""
    global NOTION_KEY
    NOTION_KEY = args.api_key or NOTION_KEY

    if not args.page_id:
        print("錯誤：需提供 --page-id", file=sys.stderr)
        sys.exit(1)

    result = api_patch(f"/pages/{args.page_id}", {"archived": True})
    print(json.dumps({"status": "archived", "page_id": result.get("id", "")}, ensure_ascii=False))


# ── CLI 主體 ────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Notion 書籍管理 CRUD")
    parser.add_argument("--api-key", default="", help="Notion Integration Token")
    parser.add_argument("--database-id", default="", help="Notion Database ID")
    sub = parser.add_subparsers(dest="cmd")

    # add
    p = sub.add_parser("add", help="新增書籍")
    p.add_argument("--title", required=True, help="書名")
    p.add_argument("--author", default="", help="作者")
    p.add_argument("--isbn", default="", help="ISBN")
    p.add_argument("--category", default="", help="分類")
    p.add_argument("--tags", default="", help="標籤（逗號分隔）")
    p.add_argument("--total-pages", dest="total_pages", default="", help="總頁數")
    p.add_argument("--location", default="", help="所在位置")
    p.add_argument("--language", default="", help="語言")
    p.add_argument("--cover-url", dest="cover_url", default="", help="封面圖 URL")
    p.add_argument("--notes", default="", help="備註")

    # search
    sub.add_parser("search", help="搜尋書籍").add_argument("query", help="搜尋關鍵字")

    # update
    p = sub.add_parser("update", help="更新書籍")
    p.add_argument("--page-id", dest="page_id", default="", help="Page ID")
    p.add_argument("--title", default="", help="書名（用於查詢）")
    p.add_argument("--author", default=None, help="作者")
    p.add_argument("--isbn", default=None, help="ISBN")
    p.add_argument("--category", default=None, help="分類（空=清除）")
    p.add_argument("--tags", default=None, help="標籤（逗號分隔，空=清除）")
    p.add_argument("--pages-read", dest="pages_read", default=None, help="已讀頁數")
    p.add_argument("--total-pages", dest="total_pages", default=None, help="總頁數")
    p.add_argument("--location", default=None, help="所在位置")
    p.add_argument("--notes", default=None, help="備註")

    # stats
    sub.add_parser("stats", help="統計")

    # delete
    p = sub.add_parser("delete", help="刪除（Archive）書籍")
    p.add_argument("--page-id", dest="page_id", required=True, help="Page ID")

    args = parser.parse_args()

    if args.cmd == "add":
        cmd_add(args)
    elif args.cmd == "search":
        cmd_search(args)
    elif args.cmd == "update":
        cmd_update(args)
    elif args.cmd == "stats":
        cmd_stats(args)
    elif args.cmd == "delete":
        cmd_delete(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
