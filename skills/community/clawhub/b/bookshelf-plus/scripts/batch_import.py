#!/usr/bin/env python3
"""
批量入庫腳本
從 CSV 檔案批量匯入書籍至 Notion
CSV 格式：書名,作者,ISBN,分類,標籤,總頁數,語言,所在位置
"""

import sys
import json
import csv
import argparse
import urllib.request
import urllib.parse

try:
    import pandas as pd
except ImportError:
    pd = None  # 不用 pandas 也可運行，只用標準 csv


NOTION_KEY = ""
DATABASE_ID = ""


def notion_headers():
    return {
        "Authorization": f"Bearer {NOTION_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }


def create_book_page(book: dict) -> dict | None:
    """在 Notion 建立一本書的頁面"""
    url = "https://api.notion.com/v1/pages"
    properties = {
        "名稱": {"title": [{"text": {"content": book.get("書名", "未知書名")}}]},
    }

    if book.get("作者"):
        properties["作者"] = {"rich_text": [{"text": {"content": book["作者"]}}]}
    if book.get("ISBN"):
        properties["ISBN"] = {"rich_text": [{"text": {"content": book["ISBN"]}}]}
    if book.get("分類"):
        properties["分類"] = {"select": {"name": book["分類"]}}
    if book.get("標籤"):
        properties["標籤"] = {"multi_select": [{"name": t} for t in book["標籤"].split(",")]}
    if book.get("總頁數"):
        try:
            properties["總頁數"] = {"number": int(book["總頁數"])}
        except ValueError:
            pass
    if book.get("語言"):
        properties["語言"] = {"select": {"name": book["語言"]}}
    if book.get("所在位置"):
        properties["所在位置"] = {"rich_text": [{"text": {"content": book["所在位置"]}}]}

    body = json.dumps({
        "parent": {"database_id": DATABASE_ID},
        "properties": properties,
    }).encode()

    req = urllib.request.Request(url, data=body, headers=notion_headers(), method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            result = json.loads(r.read())
            return result
    except urllib.error.HTTPError as e:
        error_body = json.loads(e.read())
        return {"error": error_body.get("message", str(e))}


def read_csv(csv_path: str) -> list[dict]:
    """讀取 CSV 檔案"""
    if pd:
        df = pd.read_csv(csv_path)
        return df.to_dict("records")
    else:
        records = []
        with open(csv_path, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                records.append(row)
        return records


def main():
    parser = argparse.ArgumentParser(description="CSV 批量入庫")
    parser.add_argument("--csv", required=True, help="CSV 檔案路徑")
    parser.add_argument("--api-key", required=True, help="Notion API Key")
    parser.add_argument("--database-id", required=True, help="Notion Database ID")
    parser.add_argument("--dry-run", action="store_true", help="試運行（不實際寫入）")
    args = parser.parse_args()

    global NOTION_KEY, DATABASE_ID
    NOTION_KEY = args.api_key
    DATABASE_ID = args.database_id

    try:
        books = read_csv(args.csv)
    except FileNotFoundError:
        print(f"找不到 CSV 檔案：{args.csv}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"讀取 CSV 失敗：{e}", file=sys.stderr)
        sys.exit(1)

    print(f"📚 準備匯入 {len(books)} 本書...\n")

    success_count = 0
    error_count = 0

    for i, book in enumerate(books, 1):
        title = book.get("書名", f"未知-{i}")
        print(f"  [{i}/{len(books)}] {title}...", end=" ")

        if args.dry_run:
            print("✅（dry-run）")
            success_count += 1
            continue

        result = create_book_page(book)

        if result and "error" not in result:
            print("✅")
            success_count += 1
        else:
            error_msg = result.get("error", "未知錯誤") if result else "建立失敗"
            print(f"❌ {error_msg}")
            error_count += 1

    print(f"\n✅ 匯入完成：成功 {success_count} 本，失敗 {error_count} 本")
    if args.dry_run:
        print("💡 以上為試運行結果，加上 --dry-run 參數才會實際寫入")

    sys.exit(1 if error_count else 0)


if __name__ == "__main__":
    main()
