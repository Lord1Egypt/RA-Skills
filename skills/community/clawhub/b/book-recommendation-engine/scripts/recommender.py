#!/usr/bin/env python3
"""
recommender.py — 書籍推薦核心引擎
支援：協同過濾 / 內容相似度 / 熱門暢銷 / 標籤擴展 四種推薦演算法
"""

import sys
import json
import argparse
import math
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict

DATA_DIR = Path.home() / ".bookshelf-plus" / "recommendations"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# ── 資料結構 ────────────────────────────────────────────────────────────────

class Book:
    def __init__(self, id: str, title: str, author: str = "",
                 categories: list[str] | None = None,
                 tags: list[str] | None = None,
                 rating: float = 0, pages: int = 0,
                 description: str = "", year: str = "",
                 isbn: str = "", provider: str = ""):
        self.id          = str(id)
        self.title      = title
        self.author      = author
        self.categories  = categories or []
        self.tags       = tags or []
        self.rating      = rating
        self.pages       = pages
        self.description = description
        self.year        = year
        self.isbn        = isbn
        self.provider    = provider

    def to_dict(self):
        return vars(self)

    @staticmethod
    def from_dict(d: dict):
        return Book(**{k: v for k, v in d.items() if k in Book.__init__.__code__.co_varnames})


# ── 圖書館管理 ──────────────────────────────────────────────────────────────

LIBRARY_FILE = DATA_DIR / "library.json"
USERS_FILE   = DATA_DIR / "users.json"


def load_library() -> list[Book]:
    if LIBRARY_FILE.exists():
        data = json.loads(LIBRARY_FILE.read_text(encoding="utf-8"))
        return [Book.from_dict(b) for b in data]
    return []


def save_library(books: list[Book]):
    LIBRARY_FILE.write_text(
        json.dumps([b.to_dict() for b in books], ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


def load_ratings() -> dict[str, dict[str, float]]:
    if USERS_FILE.exists():
        return json.loads(USERS_FILE.read_text(encoding="utf-8"))
    return {}


def save_ratings(ratings: dict[str, dict[str, float]]):
    USERS_FILE.write_text(
        json.dumps(ratings, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


# ── 相似度計算 ───────────────────────────────────────────────────────────────

def _normalize(text: str) -> str:
    return re.sub(r"[^\w\s]", " ", text.lower())


def _tokenize(text: str) -> set[str]:
    return set(_normalize(text).split())


def _jaccard(s1: set[str], s2: set[str]) -> float:
    if not s1 or not s2: return 0.0
    inter = len(s1 & s2)
    union = len(s1 | s2)
    return inter / union if union else 0.0


def _cosine(vec1: dict[str, int], vec2: dict[str, int]) -> float:
    common = set(vec1) & set(vec2)
    if not common: return 0.0
    dot = sum(vec1[k] * vec2[k] for k in common)
    norm1 = math.sqrt(sum(v*v for v in vec1.values()))
    norm2 = math.sqrt(sum(v*v for v in vec2.values()))
    return dot / (norm1 * norm2) if (norm1 and norm2) else 0.0


def _tfidf_weight(tokens: set[str], text: str) -> dict[str, int]:
    words = _normalize(text).split()
    freq  = defaultdict(int)
    for w in words:
        if w in tokens:
            freq[w] += 1
    return dict(freq)


# ── 演算法 ───────────────────────────────────────────────────────────────────

def content_based_recommend(books: list[Book],
                              seed_id: str,
                              top_n: int = 5) -> list[tuple[Book, float]]:
    """基於內容相似度：作者 + 分類 + 標籤 + 描述"""
    seed = next((b for b in books if b.id == seed_id), None)
    if not seed:
        return []
    seed_tokens = (
        _tokenize(seed.title) |
        _tokenize(seed.author) |
        _tokenize(" ".join(seed.categories)) |
        _tokenize(" ".join(seed.tags)) |
        _tokenize(seed.description)
    )
    results = []
    for b in books:
        if b.id == seed_id:
            continue
        b_tokens = (
            _tokenize(b.title) |
            _tokenize(b.author) |
            _tokenize(" ".join(b.categories)) |
            _tokenize(" ".join(b.tags)) |
            _tokenize(b.description)
        )
        score = _jaccard(seed_tokens, b_tokens)
        if score > 0:
            results.append((b, score))
    results.sort(key=lambda x: -x[1])
    return results[:top_n]


def collaborative_filter(user_id: str,
                          ratings: dict[str, dict[str, float]],
                          books: list[Book],
                          top_n: int = 5) -> list[tuple[Book, float]]:
    """基於用戶評分的協同過濾：找相似口味用戶推薦的書"""
    if user_id not in ratings or not ratings[user_id]:
        return popular_recommend(books, top_n)

    user_ratings = ratings[user_id]
    rated_books  = set(user_ratings.keys())

    # 找相似用戶
    scores: dict[str, float] = defaultdict(float)
    for other, other_ratings in ratings.items():
        if other == user_id or not other_ratings:
            continue
        common = set(user_ratings) & set(other_ratings)
        if not common:
            continue
        # Pearson correlation
        u_vals = [user_ratings[k] for k in common]
        o_vals = [other_ratings[k] for k in common]
        u_mean = sum(u_vals) / len(u_vals)
        o_mean = sum(o_vals) / len(o_vals)
        num = sum((u - u_mean)*(o - o_mean) for u, o in zip(u_vals, o_vals))
        den = math.sqrt(sum((u-u_mean)**2 for u in u_vals)) * \
              math.sqrt(sum((o-o_mean)**2 for o in o_vals))
        if den == 0:
            continue
        similarity = num / den
        if similarity > 0:
            for book_id, rating in other_ratings.items():
                if book_id not in rated_books:
                    scores[book_id] += similarity * rating

    if not scores:
        return popular_recommend(books, top_n)

    book_map = {b.id: b for b in books}
    results = [(book_map[bid], score)
               for bid, score in scores.items() if bid in book_map]
    results.sort(key=lambda x: -x[1])
    return results[:top_n]


def popular_recommend(books: list[Book],
                       ratings: dict[str, dict[str, float]],
                       top_n: int = 5) -> list[tuple[Book, float]]:
    """熱門推薦：評分人數 × 平均評分"""
    count  = defaultdict(int)
    total  = defaultdict(float)
    for user_ratings in ratings.values():
        for bid, r in user_ratings.items():
            count[bid] += 1
            total[bid] += r

    scored = []
    for b in books:
        c = count.get(b.id, 0)
        t = total.get(b.id, 0)
        # Popularity score: count * avg
        score = c * (t / c if c else 0)
        if c > 0:
            scored.append((b, score))

    scored.sort(key=lambda x: -x[1])
    return scored[:top_n]


def tag_expand_recommend(books: list[Book],
                           seed_tags: list[str],
                           top_n: int = 5) -> list[tuple[Book, float]]:
    """標籤擴展：seed_tags 是用戶喜歡的標籤列表"""
    seed_set = set(_normalize(t) for t in seed_tags)
    results  = []
    for b in books:
        book_tag_set = set(_normalize(t) for t in b.tags + b.categories)
        score = len(seed_set & book_tag_set) / len(seed_set | book_tag_set) \
                if seed_set else 0
        if score > 0:
            results.append((b, score))
    results.sort(key=lambda x: -x[1])
    return results[:top_n]


def random_discovery(books: list[Book], top_n: int = 5) -> list[Book]:
    import random
    pool = [b for b in books if b.rating >= 4.0]
    if len(pool) < top_n:
        pool = books
    return random.sample(pool, min(top_n, len(pool)))


# ── CLI ──────────────────────────────────────────────────────────────────────

def _fmt_book(b: Book, score: float | None = None) -> str:
    stars = "⭐" * int(b.rating) if b.rating else "—"
    cats  = " / ".join(b.categories[:2]) if b.categories else ""
    lines = [
        f"  📖 《{b.title}》",
        f"     作者：{b.author or '未知'}",
        f"     評分：{stars} {b.rating}/5" if b.rating else "",
        f"     分類：{cats}" if cats else "",
        f"     年份：{b.year}" if b.year else "",
    ]
    if score is not None and not isinstance(b, Book):
        lines.append(f"     匹配度：{score:.0%}")
    elif isinstance(b, Book) and not hasattr(b, '_score'):
        pass
    return "\n".join(l for l in lines if l)


def main():
    parser = argparse.ArgumentParser(description="📚 書籍推薦引擎")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("recommend", help="推薦書籍")
    p.add_argument("-u", "--user", default="default", help="用戶 ID")
    p.add_argument("-b", "--book-id", help="以某本書為種子")
    p.add_argument("-t", "--tags", nargs="+", help="標籤關鍵字")
    p.add_argument("-m", "--method",
                   choices=["content","collab","popular","tag","mixed"],
                   default="mixed", help="推薦演算法")
    p.add_argument("-n", "--top", type=int, default=5)
    p.add_argument("-q", "--query", help="自然語言查詢描述")

    p = sub.add_parser("rate", help="對書籍評分")
    p.add_argument("-u", "--user", default="default")
    p.add_argument("book_id", help="書籍 ID")
    p.add_argument("rating", type=float, choices=[1,1.5,2,2.5,3,3.5,4,4.5,5])

    p = sub.add_parser("add-book", help="新增書籍到圖書館")
    p.add_argument("-t", "--title", required=True)
    p.add_argument("-a", "--author", default="")
    p.add_argument("-c", "--categories", nargs="+", default=[])
    p.add_argument("-g", "--tags", nargs="+", default=[])
    p.add_argument("-r", "--rating", type=float, default=0)
    p.add_argument("-y", "--year", default="")
    p.add_argument("-p", "--pages", type=int, default=0)
    p.add_argument("-d", "--description", default="")
    p.add_argument("-i", "--isbn", default="")

    p = sub.add_parser("list", help="列出圖書館中的書")
    p.add_argument("-s", "--search", help="關鍵字搜尋")
    p.add_argument("-c", "--category")

    args = parser.parse_args(sys.argv[1:] if len(sys.argv) > 1 else ["--help"])

    def log(msg): print(msg)

    if args.cmd == "recommend":
        books   = load_library()
        ratings = load_ratings()

        if not books:
            log("❌ 圖書館為空，請先使用 add-book 新增書籍")
            return

        results: list[tuple[Book, float]] = []

        if args.book_id:
            results = content_based_recommend(books, args.book_id, args.top)
            log(f"\n📖 基於《{args.book_id}》的推薦：")

        elif args.tags:
            results = tag_expand_recommend(books, args.tags, args.top)
            log(f"\n🏷️  標籤「{' '.join(args.tags)}」的推薦：")

        elif args.method == "collab":
            results = collaborative_filter(args.user, ratings, books, args.top)
            log(f"\n👥 與你品味相近的讀者也在看：")

        elif args.method == "popular":
            results = popular_recommend(books, ratings, args.top)
            log(f"\n🔥 熱門推薦：")

        elif args.method == "tag":
            log("❌ 請提供 -t/--tags 參數")
            return

        elif args.method == "mixed":
            # 混合方法
            content = content_based_recommend(books, args.book_id or "", 3) \
                      if args.book_id else []
            collab = collaborative_filter(args.user, ratings, books, 3)
            pop    = popular_recommend(books, ratings, 3)
            merged: dict[str, tuple[Book, float]] = {}
            for b, s in (content + collab + pop):
                if b.id not in merged:
                    merged[b.id] = (b, 0)
                merged[b.id] = (b, merged[b.id][1] + s * 0.5)
            results = sorted(merged.values(), key=lambda x: -x[1])[:args.top]
            log(f"\n✨ 混合推薦（綜合多種演算法）：")

        if not results:
            log("  找不到符合條件的推薦")
            return

        for i, (b, score) in enumerate(results, 1):
            stars = "⭐" * int(b.rating) if b.rating else ""
            cats  = " / ".join(b.categories[:2])
            print(f"\n  {i}. 📖 《{b.title}》")
            print(f"       作者：{b.author or '未知'}  |  {stars}")
            if cats: print(f"       分類：{cats}")
            if score: print(f"       匹配度：{min(score*20, 100):.0f}%")

    elif args.cmd == "rate":
        ratings = load_ratings()
        ratings.setdefault(args.user, {})[args.book_id] = args.rating
        save_ratings(ratings)
        log(f"✅ 已記錄評分：{args.book_id} → {args.rating} ⭐")

    elif args.cmd == "add-book":
        books = load_library()
        book_id = args.isbn or args.title[:20].replace(" ", "_")
        book = Book(
            id          = book_id,
            title       = args.title,
            author      = args.author,
            categories  = args.categories,
            tags        = args.tags,
            rating      = args.rating,
            year        = args.year,
            pages       = args.pages,
            description = args.description,
            isbn        = args.isbn,
        )
        books = [b for b in books if b.id != book_id]
        books.append(book)
        save_library(books)
        log(f"✅ 已新增：《{args.title}》")

    elif args.cmd == "list":
        books = load_library()
        if not books:
            log("📭 圖書館為空")
            return
        if args.search:
            q = args.search.lower()
            books = [b for b in books
                     if q in b.title.lower() or q in b.author.lower()
                     or q in " ".join(b.categories).lower()]
        if args.category:
            books = [b for b in books if args.category in b.categories]
        log(f"\n📚 圖書館（共 {len(books)} 本）\n")
        for b in books:
            stars = "⭐" * int(b.rating) if b.rating else ""
            print(f"  [{b.id}] 《{b.title}》— {b.author or '未知'}  {stars}")


if __name__ == "__main__":
    main()
