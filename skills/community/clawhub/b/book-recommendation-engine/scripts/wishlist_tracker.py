#!/usr/bin/env python3
"""
wishlist_tracker.py — 想讀書單追蹤器
自動追蹤：價格變化、出版狀態、評分消長、待讀順位
"""

import sys
import json
import re
import argparse
import urllib.request
import urllib.parse
from pathlib import Path
from datetime import datetime, timedelta

DATA_DIR = Path.home() / ".bookshelf-plus" / "recommendations"
DATA_DIR.mkdir(parents=True, exist_ok=True)
WISHLIST_FILE = DATA_DIR / "wishlist.json"


# ── Wishlist Storage ─────────────────────────────────────────────────────────

def _load() -> dict:
    if WISHLIST_FILE.exists():
        return json.loads(WISHLIST_FILE.read_text(encoding="utf-8"))
    return {"books": [], "updated": ""}


def _save(data: dict):
    data["updated"] = datetime.now().isoformat()
    WISHLIST_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


# ── Book Entry ───────────────────────────────────────────────────────────────

def _book(id: str, title: str, author: str = "",
          price: float = 0, priority: int = 0,
          status: str = "want", isbn: str = "",
          notes: str = "", source: str = "",
          added_date: str = "", url: str = "",
          tags: list = None) -> dict:
    return {
        "id": id,
        "title": title,
        "author": author,
        "price": price,
        "currency": "TWD",
        "priority": priority,     # 1=低 2=中 3=高 4=立刻買
        "status": status,         # want / ordered / arrived / read
        "isbn": isbn,
        "notes": notes,
        "source": source,         # kinunya / books.com.tw / taaze / eslite
        "added_date": added_date or datetime.now().date().isoformat(),
        "price_history": [],
        "url": url,
        "rating": 0,
        "tags": [],
    }


# ── Price Fetchers ───────────────────────────────────────────────────────────

def _fetch(url: str) -> str:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception:
        return ""


def _extract_price_kinokuniya(isbn: str) -> float | None:
    url = f"https://www.books.com.tw/product/{isbn}"
    html = _fetch(url)
    if not html:
        return None
    m = re.search(r'<span class="price">.*?([\d,]+)</span>', html, re.DOTALL)
    if m:
        return float(m.group(1).replace(",", ""))
    return None


def _extract_price_taaze(isbn: str) -> float | None:
    url = f"https://www.taaze.tw/products/{isbn}.html"
    html = _fetch(url)
    if not html:
        return None
    m = re.search(r'(\d[\d,]+)\s*元', html)
    if m:
        return float(m.group(1).replace(",", ""))
    return None


# ── Operations ──────────────────────────────────────────────────────────────

def add_book(title: str, author: str = "", isbn: str = "",
             price: float = 0, priority: int = 2,
             notes: str = "", tags: list = None,
             url: str = "") -> str:
    data = _load()
    book_id = isbn or (title[:15] + "_" + datetime.now().strftime("%m%d"))
    # Already in list?
    for b in data["books"]:
        if b["id"] == book_id or (isbn and b.get("isbn") == isbn):
            return f"⚠️  「{title}」已在想讀清單中"
    book = _book(book_id, title, author, price, priority,
                 isbn=isbn, notes=notes, url=url,
                 tags=tags or [])
    data["books"].append(book)
    _save(data)
    return f"✅ 已加入想讀清單：《{title}》"


def remove_book(book_id: str) -> str:
    data = _load()
    before = len(data["books"])
    data["books"] = [b for b in data["books"] if b["id"] != book_id]
    if len(data["books"]) == before:
        return f"❌ 找不到：{book_id}"
    _save(data)
    return f"✅ 已移除"


def mark_received(book_id: str) -> str:
    data = _load()
    for b in data["books"]:
        if b["id"] == book_id:
            b["status"] = "arrived"
            _save(data)
            return f"✅ 已標記為「已到貨」：《{b['title']}》"
    return f"❌ 找不到：{book_id}"


def mark_read(book_id: str, rating: int = 0) -> str:
    data = _load()
    for b in data["books"]:
        if b["id"] == book_id:
            b["status"] = "read"
            b["rating"] = rating
            _save(data)
            stars = "⭐" * rating if rating else ""
            return f"✅ 已標記為「已讀」：《{b['title']}》{stars}"
    return f"❌ 找不到：{book_id}"


def reorder_priority(book_id: str, new_priority: int) -> str:
    data = _load()
    for b in data["books"]:
        if b["id"] == book_id:
            b["priority"] = max(1, min(4, new_priority))
            _save(data)
            return f"✅ 優先順序已更新：《{b['title']}》（{b['priority']}/4）"
    return f"❌ 找不到：{book_id}"


def check_prices() -> str:
    data = _load()
    want_books = [b for b in data["books"] if b["status"] == "want" and b.get("isbn")]
    if not want_books:
        return "📭 目前沒有待追蹤的 ISBN 書籍"

    lines = ["\n💰 價格追蹤：\n"]
    changed = 0
    for b in want_books[:10]:  # 每次最多查 10 本
        isbn = b.get("isbn", "")
        old_price = b.get("price", 0) or 0
        new_price = _extract_price_taaze(isbn) or _extract_price_kinokuniya(isbn) or old_price
        if new_price and new_price != old_price:
            b["price_history"].append({"date": datetime.now().date().isoformat(),
                                        "price": new_price})
            b["price"] = new_price
            if new_price < old_price:
                lines.append(f"  🔻 {b['title']}：{old_price} → {new_price} 元（降價了！）")
            else:
                lines.append(f"  🔺 {b['title']}：{old_price} → {new_price} 元")
            changed += 1
    if changed:
        _save(data)
        lines.append(f"\n✅ 已更新 {changed} 本的價格")
    else:
        lines.append("  目前價格無變化")

    return "\n".join(lines)


def list_wishlist(filter_status: str = None) -> str:
    data = _load()
    books = data["books"]

    if filter_status:
        books = [b for b in books if b.get("status") == filter_status]

    if not books:
        return "📭 想讀清單為空"

    # Sort by priority desc
    books = sorted(books, key=lambda b: -b["priority"])

    status_icon = {"want": "📋", "ordered": "📦", "arrived": "✅", "read": "📖"}
    priority_label = {1:"低", 2:"中", 3:"高", 4:"立"}

    lines = [f"\n📚 想讀清單（共 {len(books)} 本）\n"]
    lines.append("─" * 50)

    for b in books:
        icon = status_icon.get(b.get("status","want"), "📋")
        pri  = priority_label.get(b.get("priority",2), "中")
        price = b.get("price", 0)
        price_str = f"💰 {price:.0f}元" if price else ""
        stars = "⭐" * int(b.get("rating",0))
        lines.append(
            f"\n{icon} [{b['id'][:12]}] 《{b['title']}》"
        )
        if b.get("author"): lines.append(f"   作者：{b['author']}")
        if price_str: lines.append(f"   {price_str}")
        lines.append(f"   優先：{pri}　狀態：{b.get('status','want')}")
        if stars: lines.append(f"   評分：{stars}")
        if b.get("notes"): lines.append(f"   📝 {b['notes']}")

    return "\n".join(lines)


def export_wishlist(out_path: Path) -> Path:
    data = _load()
    out_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    return out_path


# ── CLI ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="📚 想讀書單追蹤器")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("add",    help="新增書籍")
    p.add_argument("-t", "--title", required=True)
    p.add_argument("-a", "--author", default="")
    p.add_argument("-i", "--isbn", default="")
    p.add_argument("-p", "--price", type=float, default=0)
    p.add_argument("--priority", type=int, choices=[1,2,3,4], default=2)
    p.add_argument("--notes",    default="")
    p.add_argument("--tags", nargs="+", default=[])
    p.add_argument("--url",      default="")

    p = sub.add_parser("list",   help="列出清單")
    p.add_argument("-s", "--status", choices=["want","ordered","arrived","read"])

    p = sub.add_parser("remove", help="移除書籍")
    p.add_argument("book_id", help="書籍 ID")

    p = sub.add_parser("receive",help="標記為已到貨")
    p.add_argument("book_id")

    p = sub.add_parser("read",   help="標記為已讀")
    p.add_argument("book_id")
    p.add_argument("-r", "--rating", type=int, choices=[1,2,3,4,5], default=0)

    p = sub.add_parser("priority", help="更新優先順序")
    p.add_argument("book_id")
    p.add_argument("level", type=int, choices=[1,2,3,4])

    p = sub.add_parser("price",  help="檢查價格變化")
    p.add_argument("-n", "--dry-run", action="store_true")

    p = sub.add_parser("export", help="匯出 JSON")
    p.add_argument("-o", "--output", type=Path, required=True)

    args = parser.parse_args(sys.argv[1:] if len(sys.argv) > 1 else ["--help"])

    def log(msg=""): print(msg)

    if args.cmd == "add":
        log(add_book(args.title, args.author, args.isbn,
                     args.price, args.priority, args.notes, args.tags, args.url))

    elif args.cmd == "list":
        log(list_wishlist(getattr(args, "status", None)))

    elif args.cmd == "remove":
        log(remove_book(args.book_id))

    elif args.cmd == "receive":
        log(mark_received(args.book_id))

    elif args.cmd == "read":
        log(mark_read(args.book_id, getattr(args, "rating", 0)))

    elif args.cmd == "priority":
        log(reorder_priority(args.book_id, args.level))

    elif args.cmd == "price":
        if args.dry_run:
            log("🔍 預演模式：只顯示目前價格")
            data = _load()
            for b in data["books"][:5]:
                log(f"  {b['title']}：{b.get('price',0)} 元")
        else:
            log(check_prices())

    elif args.cmd == "export":
        out = export_wishlist(args.output)
        log(f"✅ 已匯出：{out}")


if __name__ == "__main__":
    main()
