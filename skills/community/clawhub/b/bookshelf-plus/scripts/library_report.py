#!/usr/bin/env python3
"""
書庫健康報告腳本
查詢 Notion 並生成 Markdown / JSON 格式的書庫統計報告
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


def fetch_all_books() -> list:
    """取得所有書籍記錄"""
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    body = json.dumps({"page_size": 100}).encode()
    req = urllib.request.Request(url, data=body, headers=notion_headers(), method="POST")
    with urllib.request.urlopen(req, timeout=15) as r:
        data = json.loads(r.read())
    return data.get("results", [])


def parse_book(page: dict) -> dict:
    """解析單筆書籍頁面屬性"""
    props = page["properties"]
    return {
        "title": props.get("名稱", {}).get("title", [{}])[0].get("plain_text", ""),
        "author": props.get("作者", {}).get("rich_text", [{}])[0].get("plain_text", ""),
        "isbn": props.get("ISBN", {}).get("rich_text", [{}])[0].get("plain_text", ""),
        "category": props.get("分類", {}).get("select", {}).get("name", ""),
        "tags": [t["name"] for t in props.get("標籤", {}).get("multi_select", [])],
        "borrowed_by": props.get("借出給", {}).get("rich_text", [{}])[0].get("plain_text", ""),
        "borrowed_date": props.get("借出日期", {}).get("date", {}).get("start", ""),
        "due_date": props.get("預定還日", {}).get("date", {}).get("start", ""),
        "pages_read": props.get("閱讀頁數", {}).get("number", 0) or 0,
        "total_pages": props.get("總頁數", {}).get("number", 0) or 0,
        "location": props.get("所在位置", {}).get("rich_text", [{}])[0].get("plain_text", ""),
        "language": props.get("語言", {}).get("select", {}).get("name", ""),
        "publish_year": props.get("出版年份", {}).get("number", 0) or 0,
    }


def generate_report(books: list, format: str = "markdown") -> str:
    today = datetime.date.today()
    total = len(books)

    # Tag 統計
    tag_counts = {"已讀": 0, "待讀": 0, "在借": 0, "閱讀中": 0, "逾期": 0, "新書": 0}
    category_counts = {}
    language_counts = {}
    borrow_count = {}  # 書名: 借出次數
    overdue_books = []

    for b in books:
        tags = b["tags"]
        for t in tag_counts:
            if t in tags:
                tag_counts[t] += 1
        cat = b["category"]
        if cat:
            category_counts[cat] = category_counts.get(cat, 0) + 1
        lang = b["language"]
        if lang:
            language_counts[lang] = language_counts.get(lang, 0) + 1
        if b["borrowed_by"]:
            key = b["title"]
            borrow_count[key] = borrow_count.get(key, 0) + 1
        if "逾期" in tags:
            overdue_books.append(b)

    # 最常被借出的書
    top_borrowed = sorted(borrow_count.items(), key=lambda x: x[1], reverse=True)[:3]

    # 計算閱讀進度
    books_with_progress = [b for b in books if b["total_pages"] > 0]
    avg_progress = 0
    if books_with_progress:
        avg_progress = sum(b["pages_read"] / b["total_pages"] * 100 for b in books_with_progress) / len(books_with_progress)

    if format == "json":
        return json.dumps({
            "report_date": today.isoformat(),
            "total_books": total,
            "tag_counts": tag_counts,
            "category_counts": category_counts,
            "language_counts": language_counts,
            "overdue_books": overdue_books,
            "top_borrowed": [{"title": t, "count": c} for t, c in top_borrowed],
            "average_reading_progress": round(avg_progress, 1),
        }, ensure_ascii=False, indent=2)

    # Markdown 格式
    md = f"""📚 書庫健康報告（{today.isoformat()}）

---

📖 **總藏書：{total} 本**

| 狀態 | 數量 | 佔比 |
|------|------|------|
| 已讀 | {tag_counts['已讀']} | {tag_counts['已讀']/total*100:.0f}% |
| 待讀 | {tag_counts['待讀']} | {tag_counts['待讀']/total*100:.0f}% |
| 閱讀中 | {tag_counts['閱讀中']} | {tag_counts['閱讀中']/total*100:.0f}% |
| 在借 | {tag_counts['在借']} | {tag_counts['在借']/total*100:.0f}% |
| 逾期 | {tag_counts['逾期']} | {tag_counts['逾期']/total*100:.0f}% |

"""

    if category_counts:
        md += "**📚 分類分布**\n\n"
        for cat, cnt in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
            md += f"- {cat}：{cnt} 本\n"
        md += "\n"

    if language_counts:
        md += "**🌐 語言分布**\n\n"
        for lang, cnt in sorted(language_counts.items(), key=lambda x: x[1], reverse=True):
            md += f"- {lang}：{cnt} 本\n"
        md += "\n"

    if overdue_books:
        md += "⚠️ **逾期書籍**\n\n"
        for b in overdue_books:
            md += f"- 《{b['title']}》— 借給 {b['borrowed_by']}（逾期）\n"
        md += "\n"

    if top_borrowed:
        md += f"🏆 **借出率冠軍**（被借出次數最多）\n\n"
        for i, (title, cnt) in enumerate(top_borrowed, 1):
            md += f"{i}. 《{title}》— 已借出 {cnt} 次\n"
        md += "\n"

    if books_with_progress:
        md += f"📈 **平均閱讀進度：{avg_progress:.1f}%**（共 {len(books_with_progress)} 本有進度記錄）\n"

    return md


def main():
    parser = argparse.ArgumentParser(description="書庫健康報告")
    parser.add_argument("--api-key", required=True, help="Notion API Key")
    parser.add_argument("--database-id", required=True, help="Notion Database ID")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--output", "-o", help="輸出檔案路徑（選填）")
    args = parser.parse_args()

    global NOTION_KEY, DATABASE_ID
    NOTION_KEY = args.api_key
    DATABASE_ID = args.database_id

    books = [parse_book(p) for p in fetch_all_books()]
    report = generate_report(books, args.format)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"✅ 報告已儲存：{args.output}")
    else:
        print(report)


if __name__ == "__main__":
    main()
