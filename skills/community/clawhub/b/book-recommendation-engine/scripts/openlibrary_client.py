#!/usr/bin/env python3
"""
openlibrary_client.py — Open Library API 客戶端
提供：書名/作者/ISBN 搜尋、暢銷書榜、書評摘要、作者資訊
"""

import sys
import json
import urllib.request
import urllib.parse
import argparse
from pathlib import Path
from datetime import datetime

API_BASE  = "https://openlibrary.org"
COVER_URL = "https://covers.openlibrary.org/b"
CACHE_DIR = Path.home() / ".bookshelf-plus" / "recommendations" / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)


# ── HTTP Helper ───────────────────────────────────────────────────────────────

def _fetch(url: str, params: dict | None = None) -> dict | None:
    if params:
        url += "?" + urllib.parse.urlencode(params)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "QClaw-Reader/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8", errors="replace"))
    except Exception as e:
        print(f"⚠️  網路請求失敗：{e}", file=sys.stderr)
        return None


def _cache_key(url: str) -> str:
    import hashlib
    return hashlib.md5(url.encode()).hexdigest()


def _cached(url: str) -> dict | None:
    key  = _cache_key(url)
    file = CACHE_DIR / f"{key}.json"
    if file.exists():
        age = datetime.now() - datetime.fromtimestamp(file.stat().st_mtime)
        if age.days < 7:  # 7天緩存
            return json.loads(file.read_text(encoding="utf-8"))
    data = _fetch(url)
    if data:
        file.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    return data


# ── 書名/作者搜尋 ────────────────────────────────────────────────────────────

def search(query: str, fields: str = "key,title,author_name,first_publish_year,"
             "subject,isbn,rating,cover_i,number_of_pages_median,editions_count",
           limit: int = 10) -> list[dict]:
    """搜尋書名或作者"""
    url = f"{API_BASE}/search.json"
    params = {"q": query, "fields": fields, "limit": limit, "lang": "zh,en"}
    result = _cached(url + "?" + urllib.parse.urlencode(params))
    if result and "docs" in result:
        return result["docs"]
    return []


def search_by_isbn(isbn: str) -> dict | None:
    url = f"{API_BASE}/isbn/{isbn}.json"
    result = _cached(url)
    if result:
        # 補充作者資訊
        if "authors" in result:
            author_keys = [a.get("key","") for a in result["authors"]]
            authors = []
            for ak in author_keys[:2]:
                ad = _fetch(f"{API_BASE}{ak}.json")
                if ad:
                    authors.append(ad.get("name",""))
            if authors:
                result["author_names"] = authors
    return result


def search_by_author(author_name: str, limit: int = 10) -> list[dict]:
    url = f"{API_BASE}/search.json"
    params = {
        "author": author_name,
        "fields": "key,title,author_name,first_publish_year,subject,"
                  "isbn,cover_i,number_of_pages_median,ratings_average",
        "limit": limit,
    }
    result = _cached(url + "?" + urllib.parse.urlencode(params))
    if result and "docs" in result:
        return result["docs"]
    return []


# ── 暢銷書 / 主題書單 ─────────────────────────────────────────────────────────

def get_trending(limit: int = 20) -> list[dict]:
    """熱門借閱（Trending）"""
    url = f"{API_BASE}/trending/daily.json"
    params = {"limit": limit}
    result = _cached(url + "?" + urllib.parse.urlencode(params))
    if result and "works" in result:
        return result["works"]
    return []


def get_subject(subject: str, limit: int = 15) -> list[dict]:
    """依主題取書"""
    slug = urllib.parse.quote(subject.lower())
    url = f"{API_BASE}/subjects/{slug}.json"
    params = {"limit": limit}
    result = _cached(url + "?" + urllib.parse.urlencode(params))
    if result and "works" in result:
        return result["works"]
    return []


def get_author(author_key: str) -> dict | None:
    """作者詳細資訊"""
    key  = author_key.lstrip("/")
    url  = f"{API_BASE}/authors/{key}.json"
    return _cached(url)


def get_book_details(work_key: str) -> dict | None:
    """書本詳細頁（含簡介）"""
    key = work_key.lstrip("/")
    url = f"{API_BASE}/{key}.json"
    return _cached(url)


# ── 封面圖 ──────────────────────────────────────────────────────────────────

def cover_url(cover_id: int | None, size: str = "M", fallback_isbn: str = "") -> str:
    """取得封面 URL（S/M/L）"""
    if cover_id:
        return f"{COVER_URL}/id/{cover_id}-{size}.jpg"
    if fallback_isbn:
        return f"{COVER_URL}/isbn/{fallback_isbn}-{size}.jpg"
    return ""


# ── 實用工具 ───────────────────────────────────────────────────────────────

def parse_subject_works(works: list[dict]) -> list[dict]:
    """統一不同 endpoint 的欄位名"""
    results = []
    for w in works:
        if "key" in w:
            # subject / trending endpoint
            results.append({
                "key":        w.get("key",""),
                "title":      w.get("title",""),
                "author":     ", ".join(w.get("author_names", [])) or
                              ", ".join(a.get("name",[]) for a in w.get("authors",[]) if a) or "未知",
                "year":       w.get("first_publish_year", ""),
                "subject":    w.get("subject", [])[:5],
                "cover_id":   w.get("cover_id"),
                "cover_i":    w.get("cover_i"),
                "isbn":       (w.get("isbn") or [{}])[0] if w.get("isbn") else "",
                "ratings":    w.get("ratings_average", 0) or w.get("rating", 0),
                "cover_url":  cover_url(w.get("cover_id") or w.get("cover_i"), size="M"),
            })
        elif "docs" in w:
            # search endpoint
            pass
    return results


# ── CLI ──────────────────────────────────────────────────────────────────────

def _fmt_book(b: dict, idx: int = 0) -> str:
    title   = b.get("title","未知")
    author  = b.get("author","未知作者")
    year    = b.get("year","")
    subjects= b.get("subject", [])[:3]
    rating  = b.get("ratings", 0) or 0
    url     = b.get("cover_url","")
    stars   = "⭐" * int(rating) if rating else ""

    parts = [f"\n  {idx+1}. 📖 《{title}》"]
    parts.append(f"     作者：{author}")
    if year:  parts.append(f"     年份：{year}")
    if stars: parts.append(f"     評分：{stars} {rating}")
    if subjects: parts.append(f"     主題：{' / '.join(subjects)}")
    if url and "covers.openlibrary.org" in url:
        parts.append(f"     封面：{url}")
    return "\n".join(parts)


def main():
    parser = argparse.ArgumentParser(description="📚 Open Library API 客戶端")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("search",    help="搜尋書名/作者")
    p.add_argument("query", help="關鍵字")
    p.add_argument("-n", "--limit", type=int, default=8)

    p = sub.add_parser("isbn",      help="以 ISBN 查書")
    p.add_argument("isbn", help="ISBN")

    p = sub.add_parser("author",    help="查某作者的作品")
    p.add_argument("name", help="作者名")
    p.add_argument("-n", "--limit", type=int, default=8)

    p = sub.add_parser("trending",   help="今日熱門書")
    p.add_argument("-n", "--limit", type=int, default=10)

    p = sub.add_parser("subject",    help="依主題取書")
    p.add_argument("subject", help="主題，如：science_fiction, history, self_help")
    p.add_argument("-n", "--limit", type=int, default=10)

    p = sub.add_parser("author-info", help="作者資訊")
    p.add_argument("key", help="作者 key，如 /authors/OL23919A")

    p = sub.add_parser("book-info",  help="書本詳細資訊")
    p.add_argument("key", help="書 key，如 /works/OL82563W")

    args = parser.parse_args(sys.argv[1:] if len(sys.argv) > 1 else ["--help"])

    def log(msg=""): print(msg)

    if args.cmd == "search":
        docs = search(args.query, limit=args.limit)
        if not docs:
            log("❌ 找不到結果"); return
        log(f"\n🔍 搜尋「{args.query}」共 {len(docs)} 筆：")
        for i, d in enumerate(docs):
            b = {
                "title":    d.get("title",""),
                "author":   ", ".join(d.get("author_name",[])) or "未知",
                "year":     d.get("first_publish_year",""),
                "cover_id": d.get("cover_i"),
                "isbn":     (d.get("isbn") or [{}])[0] if d.get("isbn") else "",
                "ratings":  d.get("ratings_average", 0),
                "subject":  d.get("subject",[])[:3],
                "cover_url": cover_url(d.get("cover_i"), size="M"),
            }
            log(_fmt_book(b, i))

    elif args.cmd == "isbn":
        book = search_by_isbn(args.isbn)
        if not book:
            log("❌ 找不到此 ISBN"); return
        log(f"\n📖 《{book.get('title','?')}》")
        if book.get("author_names"):
            log(f"   作者：{', '.join(book['author_names'])}")
        if book.get("publishers"):
            log(f"   出版社：{book['publishers'][0]}")
        if book.get("publish_date"):
            log(f"   出版：{book['publish_date']}")
        if book.get("number_of_pages"):
            log(f"   頁數：{book['number_of_pages']}")
        if book.get("isbn_13"):
            log(f"   ISBN-13：{book['isbn_13'][0]}")
        if book.get("description"):
            desc = book["description"]
            if isinstance(desc, dict):
                desc = desc.get("value","")
            log(f"\n   簡介：{str(desc)[:200]}")
        cover_id = book.get("covers", [None])[0]
        if cover_id:
            log(f"\n   封面：{cover_url(cover_id, size='L')}")

    elif args.cmd == "author":
        works = search_by_author(args.name, limit=args.limit)
        if not works:
            log("❌ 找不到作者"); return
        log(f"\n👤 {args.name} 作品（{len(works)} 本）：")
        for i, d in enumerate(works):
            b = {
                "title":    d.get("title",""),
                "author":   args.name,
                "year":     d.get("first_publish_year",""),
                "cover_id": d.get("cover_i"),
                "ratings":  d.get("ratings_average",0),
                "cover_url": cover_url(d.get("cover_i"), size="M"),
            }
            log(_fmt_book(b, i))

    elif args.cmd == "trending":
        works = get_trending(args.limit)
        if not works: log("❌ 無法取得"); return
        log(f"\n🔥 今日熱門（共 {len(works)} 本）：")
        parsed = parse_subject_works(works)
        for i, b in enumerate(parsed):
            log(_fmt_book(b, i))

    elif args.cmd == "subject":
        works = get_subject(args.subject, args.limit)
        if not works: log(f"❌ 主題「{args.subject}」找不到"); return
        log(f"\n📚 主題「{args.subject}」書籍（共 {len(works)} 本）：")
        parsed = parse_subject_works(works)
        for i, b in enumerate(parsed):
            log(_fmt_book(b, i))

    elif args.cmd == "author-info":
        info = get_author(args.key)
        if not info: log("❌ 找不到作者"); return
        log(f"\n👤 {info.get('name','?')}")
        if info.get("bio"):
            bio = info["bio"]
            if isinstance(bio, dict): bio = bio.get("value","")
            log(f"   簡介：{bio[:200]}")
        if info.get("birth_date"):
            log(f"   出生：{info['birth_date']}")
        if info.get("wikipedia"):
            log(f"   Wikipedia：{info['wikipedia']}")
        if info.get("photos"):
            photo_id = info["photos"][0]
            log(f"   照片：{COVER_URL}/a/OL{photo_id}-L.jpg")

    elif args.cmd == "book-info":
        info = get_book_details(args.key)
        if not info: log("❌ 找不到"); return
        log(f"\n📖 《{info.get('title','?')}》")
        if info.get("description"):
            desc = info["description"]
            if isinstance(desc, dict): desc = desc.get("value","")
            log(f"   {desc[:300]}")


if __name__ == "__main__":
    main()
