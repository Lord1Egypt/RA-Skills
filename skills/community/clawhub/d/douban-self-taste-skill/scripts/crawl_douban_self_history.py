#!/usr/bin/env python3
"""Crawl the user's own Douban shelves with cookies and store JSON cache files.

This script is intentionally scoped to the user's own account data. It uses a
browser-exported cookie JSON file and writes normalized JSON cache files.

Examples:
  python scripts/crawl_douban_self_history.py --uid myuid --category book
  python scripts/crawl_douban_self_history.py --uid myuid --category movie --force
  python scripts/crawl_douban_self_history.py --uid myuid --category all
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import asdict, dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urljoin, urlparse

import httpx
from bs4 import BeautifulSoup

RATING_RE = __import__("re").compile(r"(?:rating|allstar)(\d)(?:0)?(?:-t)?")
DATE_RE = __import__("re").compile(r"\d{4}-\d{2}-\d{2}")
TITLE_COUNT_RE = __import__("re").compile(r"\((\d+)\)")

BASE_DIR = Path(".local/douban-self-taste")
COOKIE_FILE = BASE_DIR / "cookies" / "douban_cookies.json"
CACHE_DIR = BASE_DIR / "cache" / "collections"
DEFAULT_INTERVAL = 1.5
STALE_DAYS = 7
STATUSES = ("wish", "doing", "done")
STATUS_PATHS = {
    "movie": {"wish": "wish", "doing": "do", "done": "collect"},
    "book": {"wish": "wish", "doing": "do", "done": "collect"},
    "music": {"wish": "wish", "doing": "do", "done": "collect"},
    "game": {"wish": "wish", "doing": "do", "done": "collect"},
}
HOSTS = {
    "movie": "https://movie.douban.com",
    "book": "https://book.douban.com",
    "music": "https://music.douban.com",
    "game": "https://www.douban.com",
}


@dataclass
class Item:
    title: str
    url: str | None = None
    douban_id: str | None = None
    subject_type: str | None = None
    status: str | None = None
    rating: int | None = None
    date: str | None = None
    tags: list[str] | None = None
    comment: str | None = None
    creators: list[str] | None = None
    year: str | None = None
    raw_meta: dict[str, Any] | None = None


def now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_cookies(path: Path) -> list[dict[str, Any]]:
    return json.loads(path.read_text(encoding="utf-8"))


def is_cache_fresh(path: Path, max_age_days: int = STALE_DAYS) -> bool:
    if not path.exists():
        return False
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        fetched_at = data.get("fetched_at")
        if not fetched_at:
            return False
        ts = datetime.fromisoformat(str(fetched_at).replace("Z", "+00:00"))
        return datetime.now(UTC) - ts <= timedelta(days=max_age_days)
    except Exception:
        return False


def normalize_date(text: str | None) -> str | None:
    if not text:
        return None
    m = DATE_RE.search(text)
    return m.group(0) if m else None


def extract_rating(node) -> int | None:
    if node is None:
        return None
    for el in node.select("span"):
        classes = " ".join(el.get("class", []))
        m = RATING_RE.search(classes)
        if m:
            return int(m.group(1))
    return None


def extract_id(url: str | None) -> str | None:
    if not url:
        return None
    parts = str(url).split("/subject/")
    if len(parts) < 2:
        return None
    tail = parts[1].split("/")[0]
    return tail or None


def pick_title_and_url(node):
    title_el = node.select_one("li.title a") or node.select_one(".title a") or node.select_one("h2 a") or node.select_one("a[href]")
    if not title_el:
        return None, None
    return title_el.get_text(" ", strip=True), title_el.get("href", "").strip() or None


def maybe_creators(raw: str | None) -> list[str]:
    if not raw:
        return []
    result = []
    for part in [x.strip() for x in raw.replace("｜", "/").split("/") if x.strip()]:
        if len(part) <= 40 and not any(ch.isdigit() for ch in part):
            result.append(part)
    return result[:3]


def parse_next_page_url(html: str, current_url: str) -> str | None:
    soup = BeautifulSoup(html, "lxml")
    next_el = soup.select_one("span.next a") or soup.select_one("a.next")
    if not next_el:
        return None
    href = next_el.get("href", "").strip()
    return urljoin(current_url, href) if href else None


def looks_like_login_or_auth_problem(html: str, final_url: str) -> bool:
    lowered = html.lower()
    final_url_lower = final_url.lower()
    if "accounts.douban.com/passport/login" in final_url_lower:
        return True

    strong_markers = [
        "登录豆瓣",
        "扫码登录",
        "验证码",
        "异常请求",
        "403 forbidden",
        'name="form_email"',
        'name="form_password"',
        'name="captcha-solution"',
    ]
    return any(x.lower() in lowered for x in strong_markers)


def parse_movie_page(html: str, status: str, source_url: str, source_name: str) -> list[Item]:
    soup = BeautifulSoup(html, "lxml")
    items: list[Item] = []
    for node in soup.select(".grid-view > .item"):
        title, url = pick_title_and_url(node)
        if not title:
            continue
        comment_el = node.select_one("span.comment") or node.select_one(".comment")
        intro_el = node.select_one(".intro")
        intro = intro_el.get_text(" ", strip=True) if intro_el else None
        items.append(Item(title=title, url=url, douban_id=extract_id(url), subject_type="movie", status=status, rating=extract_rating(node), date=normalize_date(node.get_text(" ", strip=True)), tags=[intro] if intro else [], comment=comment_el.get_text(" ", strip=True) if comment_el else None, creators=maybe_creators(intro), raw_meta={"source_page": source_url, "source_file": source_name, "intro": intro}))
    return items


def parse_book_page(html: str, status: str, source_url: str, source_name: str) -> list[Item]:
    soup = BeautifulSoup(html, "lxml")
    items: list[Item] = []
    for node in soup.select("li.subject-item"):
        info = node.select_one(".info") or node
        title, url = pick_title_and_url(info)
        if not title:
            continue
        pub_el = info.select_one(".pub")
        comment_el = info.select_one(".comment")
        pub = pub_el.get_text(" ", strip=True) if pub_el else None
        items.append(Item(title=title, url=url, douban_id=extract_id(url), subject_type="book", status=status, rating=extract_rating(info), date=normalize_date(info.get_text(" ", strip=True)), tags=[pub] if pub else [], comment=comment_el.get_text(" ", strip=True) if comment_el else None, creators=maybe_creators(pub), raw_meta={"source_page": source_url, "source_file": source_name, "pub": pub}))
    return items


def parse_music_page(html: str, status: str, source_url: str, source_name: str) -> list[Item]:
    soup = BeautifulSoup(html, "lxml")
    items: list[Item] = []
    for node in soup.select("li.item"):
        info = node.select_one(".info") or node
        title, url = pick_title_and_url(info)
        if not title or (url and "subject" not in url):
            continue
        intro_el = info.select_one(".intro") or info.select_one(".pub")
        comment_el = info.select_one(".comment")
        intro = intro_el.get_text(" ", strip=True) if intro_el else None
        items.append(Item(title=title, url=url, douban_id=extract_id(url), subject_type="music", status=status, rating=extract_rating(info), date=normalize_date(info.get_text(" ", strip=True)), tags=[intro] if intro else [], comment=comment_el.get_text(" ", strip=True) if comment_el else None, creators=maybe_creators(intro), raw_meta={"source_page": source_url, "source_file": source_name, "intro": intro}))
    return items


def parse_game_page(html: str, status: str, source_url: str, source_name: str) -> list[Item]:
    soup = BeautifulSoup(html, "lxml")
    items: list[Item] = []
    for node in soup.select(".game-list .common-item"):
        content = node.select_one(".content") or node
        title, url = pick_title_and_url(content)
        if not title:
            continue
        desc_el = content.select_one(".desc")
        comment_el = content.select_one(".comment")
        desc = desc_el.get_text(" ", strip=True) if desc_el else None
        items.append(Item(title=title, url=url, douban_id=extract_id(url), subject_type="game", status=status, rating=extract_rating(content), date=normalize_date(content.get_text(" ", strip=True)), tags=[desc] if desc else [], comment=comment_el.get_text(" ", strip=True) if comment_el else None, creators=[], raw_meta={"source_page": source_url, "source_file": source_name, "desc": desc}))
    return items


def parse_page(category: str, html: str, status: str, source_url: str, source_name: str) -> list[Item]:
    if category == "movie":
        return parse_movie_page(html, status, source_url, source_name)
    if category == "book":
        return parse_book_page(html, status, source_url, source_name)
    if category == "music":
        return parse_music_page(html, status, source_url, source_name)
    if category == "game":
        return parse_game_page(html, status, source_url, source_name)
    return []


def cache_path(category: str) -> Path:
    return CACHE_DIR / f"{category}.json"


def build_start_url(uid: str, category: str, status: str) -> str:
    if category == "game":
        return f"https://www.douban.com/people/{uid}/games?action={STATUS_PATHS[category][status]}"
    host = HOSTS[category]
    suffix = STATUS_PATHS[category][status]
    return f"{host}/people/{uid}/{suffix}"


def dedupe(items: list[Item]) -> list[dict[str, Any]]:
    seen = set()
    out: list[dict[str, Any]] = []
    for item in items:
        data = asdict(item)
        data["tags"] = data.get("tags") or []
        data["creators"] = data.get("creators") or []
        key = (data.get("subject_type"), data.get("douban_id") or data.get("url") or data.get("title"), data.get("status"), data.get("date"))
        if key in seen:
            continue
        seen.add(key)
        out.append({k: v for k, v in data.items() if v not in (None, [], "")})
    return out


def crawl_category(client: httpx.Client, uid: str, category: str, interval: float, page_limit: int | None) -> dict[str, Any]:
    items: list[Item] = []
    page_count = 0
    for status in STATUSES:
        next_url = build_start_url(uid, category, status)
        while next_url:
            page_count += 1
            resp = client.get(next_url)
            resp.raise_for_status()
            html = resp.text
            if looks_like_login_or_auth_problem(html, str(resp.url)):
                raise RuntimeError(f"Authentication failed while fetching {resp.url}")
            source_name = f"{category}-{status}-page-{page_count}.html"
            items.extend(parse_page(category, html, status, str(resp.url), source_name))
            if page_limit and page_count >= page_limit:
                next_url = None
            else:
                next_url = parse_next_page_url(html, str(resp.url))
            if next_url:
                time.sleep(interval)
    normalized = dedupe(items)
    return {
        "platform": "douban",
        "owner": "self",
        "subject_type": category,
        "fetched_at": now_iso(),
        "source": {"kind": "logged-in-crawl", "cookie_file": str(COOKIE_FILE), "uid": uid},
        "items": normalized,
        "count": len(normalized),
        "page_count": page_count,
    }


def ensure_dirs() -> None:
    (BASE_DIR / "cookies").mkdir(parents=True, exist_ok=True)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    (BASE_DIR / "analysis").mkdir(parents=True, exist_ok=True)


def make_client(cookie_file: Path, timeout: float) -> httpx.Client:
    raw = load_cookies(cookie_file)
    client = httpx.Client(timeout=timeout, follow_redirects=True, headers={"User-Agent": "Mozilla/5.0 OpenClaw DoubanSelfTasteSkill"})
    for item in raw:
        name = item.get("name")
        value = item.get("value")
        domain = item.get("domain")
        path = item.get("path", "/")
        if not name or value is None:
            continue
        client.cookies.set(name, value, domain=domain, path=path)
    return client


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--uid", required=True, help="Douban user uid under /people/<uid>/")
    p.add_argument("--category", choices=["movie", "book", "music", "game", "all"], required=True)
    p.add_argument("--cookie-file", default=str(COOKIE_FILE))
    p.add_argument("--cache-dir", default=str(CACHE_DIR))
    p.add_argument("--force", action="store_true")
    p.add_argument("--page-limit", type=int, default=None)
    p.add_argument("--timeout", type=float, default=20.0)
    p.add_argument("--interval", type=float, default=DEFAULT_INTERVAL)
    return p.parse_args(argv[1:])


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    global COOKIE_FILE, CACHE_DIR
    COOKIE_FILE = Path(args.cookie_file)
    CACHE_DIR = Path(args.cache_dir)
    ensure_dirs()

    if not COOKIE_FILE.exists():
        print(f"Cookie file missing: {COOKIE_FILE}", file=sys.stderr)
        return 2

    categories = [args.category] if args.category != "all" else ["movie", "book", "music", "game"]

    client = make_client(COOKIE_FILE, args.timeout)
    try:
        results = {}
        for category in categories:
            out_path = cache_path(category)
            if out_path.exists() and is_cache_fresh(out_path) and not args.force:
                results[category] = json.loads(out_path.read_text(encoding="utf-8"))
                continue
            data = crawl_category(client, args.uid, category, args.interval, args.page_limit)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            results[category] = data
        json.dump({"categories": results, "cache_dir": str(CACHE_DIR)}, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return 0
    finally:
        client.close()


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
