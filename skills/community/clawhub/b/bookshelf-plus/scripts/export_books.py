#!/usr/bin/env python3
"""
書庫匯出腳本
支援 CSV / Markdown / 報告 格式匯出
"""

import sys
import json
import csv
import argparse
import urllib.request
import datetime

NOTION_KEY = ""
DATABASE_ID = ""


def notion_headers():
    return {
        "Authorization": f"Bearer {NOTION_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }


def fetch_all_books() -> list:
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    body = json.dumps({"page_size": 100}).encode()
    req = urllib.request.Request(url, data=body, headers=notion_headers(), method="POST")
    with urllib.request.urlopen(req, timeout=15) as r:
        data = json.loads(r.read())
    return data.get("results", [])


def parse_book(page: dict) -> dict:
    props = page["properties"]
    return {
        "書名": props.get("名稱", {}).get("title", [{}])[0].get("plain_text", ""),
        "作者": props.get("作者", {}).get("rich_text", [{}])[0].get("plain_text", ""),
        "ISBN": props.get("ISBN", {}).get("rich_text", [{}])[0].get("plain_text", ""),
        "分類": props.get("分類", {}).get("select", {}).get("name", ""),
        "標籤": ",".join([t["name"] for t in props.get("標籤", {}).get("multi_select", [])]),
        "借出給": props.get("借出給", {}).get("rich_text", [{}])[0].get("plain_text", ""),
        "借出日期": props.get("借出日期", {}).get("date", {}).get("start", ""),
        "預定還日": props.get("預定還日", {}).get("date", {}).get("start", ""),
        "歸還日期": props.get("歸還日期", {}).get("date", {}).get("start", ""),
        "總頁數": props.get("總頁數", {}).get("number", 0) or 0,
        "所在位置": props.get("所在位置", {}).get("rich_text", [{}])[0].get("plain_text", ""),
        "語言": props.get("語言", {}).get("select", {}).get("name", ""),
        "出版年份": props.get("出版年份", {}).get("number", 0) or 0,
    }


def export_csv(books: list, output_path: str):
    if not books:
        print("沒有書籍可匯出", file=sys.stderr)
        sys.exit(1)
    fieldnames = ["書名", "作者", "ISBN", "分類", "標籤", "借出給", "借出日期", "預定還日", "歸還日期", "總頁數", "所在位置", "語言", "出版年份"]
    with open(output_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(books)
    print(f"✅ CSV 已匯出：{output_path}（共 {len(books)} 本）")


def export_markdown(books: list, output_path: str):
    today = datetime.date.today().isoformat()
    lines = [f"# 📚 書庫書單（{today}）\n", f"共 {len(books)} 本\n\n"]
    # 分組：先按分類，再按書名排序
    by_category = {}
    for b in books:
        cat = b["分類"] or "未分類"
        by_category.setdefault(cat, []).append(b)
    for cat, cat_books in sorted(by_category.items()):
        lines.append(f"## 📂 {cat}（{len(cat_books)} 本）\n")
        for b in sorted(cat_books, key=lambda x: x["書名"]):
            lines.append(f"- **{b['書名']}** — {b['作者'] or '未知作者'}")
            if b["ISBN"]:
                lines[-1] += f" ｜ ISBN: {b['ISBN']}"
            if b["借出給"]:
                lines[-1] += f" ｜ 👤 借給 {b['借出給']}"
            if "在借" in b["標籤"]:
                lines[-1] += " 📖"
            lines.append("")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ Markdown 已匯出：{output_path}（共 {len(books)} 本）")


def export_report(books: list, output_path: str):
    import sys, os
    scripts_dir = os.path.dirname(os.path.abspath(__file__))
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    import importlib
    mod = importlib.import_module("library_report")
    report = mod.generate_report([mod.parse_book(p) for p in books], "markdown")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"✅ 書庫報告已匯出：{output_path}")


def main():
    parser = argparse.ArgumentParser(description="書庫匯出")
    parser.add_argument("--api-key", required=True, help="Notion API Key")
    parser.add_argument("--database-id", required=True, help="Notion Database ID")
    parser.add_argument("--format", choices=["csv", "md", "markdown", "report"], default="csv")
    parser.add_argument("--output", "-o", required=True, help="輸出檔案路徑")
    args = parser.parse_args()

    global NOTION_KEY, DATABASE_ID
    NOTION_KEY = args.api_key
    DATABASE_ID = args.database_id

    pages = fetch_all_books()
    books = [parse_book(p) for p in pages]

    fmt = args.format
    if fmt in ("md", "markdown"):
        export_markdown(books, args.output)
    elif fmt == "report":
        export_report(pages, args.output)
    else:
        export_csv(books, args.output)


if __name__ == "__main__":
    main()
