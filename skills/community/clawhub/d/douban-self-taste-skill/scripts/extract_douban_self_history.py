#!/usr/bin/env python3
"""Extract the user's own Douban collection records from saved HTML pages.

This script is intentionally scoped to self-owned history pages that were already
saved/exported by the user. It does not crawl the public web by itself.

Usage:
  python scripts/extract_douban_self_history.py page1.html [page2.html ...]
  python scripts/extract_douban_self_history.py exports/*.html > collection.json

Output:
  JSON object containing normalized items.
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import asdict, dataclass
from html import unescape
from pathlib import Path
from typing import Iterable
from urllib.parse import urlparse

from bs4 import BeautifulSoup

RATING_RE = re.compile(r"(?:rating|allstar)(\d)(?:0)?(?:-t)?")
DATE_RE = re.compile(r"\b(\d{4}-\d{1,2}-\d{1,2})\b")
ID_RE = re.compile(r"/subject/(\d+)/")
YEAR_RE = re.compile(r"\b(19|20)\d{2}\b")


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
    raw_meta: dict | None = None


def normalize_date(text: str | None) -> str | None:
    if not text:
        return None
    m = DATE_RE.search(text)
    if not m:
        return None
    y, mo, d = m.group(1).split("-")
    return f"{y}-{mo.zfill(2)}-{d.zfill(2)}"


def extract_rating(node) -> int | None:
    if node is None:
        return None
    for el in node.select("span"):
        classes = " ".join(el.get("class", []))
        m = RATING_RE.search(classes)
        if m:
            return int(m.group(1))
    return None


def extract_douban_id(url: str | None) -> str | None:
    if not url:
        return None
    m = ID_RE.search(url)
    return m.group(1) if m else None


def infer_subject_type(url: str | None, html_text: str = "") -> str | None:
    if url:
        host = urlparse(url).netloc
        if host == "movie.douban.com":
            return "movie"
        if host == "book.douban.com":
            return "book"
        if host == "music.douban.com":
            return "music"
        if "game.douban.com" in host or "/game/" in url or "/games/" in url:
            return "game"
    lowered = html_text.lower()
    for kind in ("movie", "book", "music", "game"):
        if kind in lowered:
            return kind
    return None


def infer_status_from_path(path: Path) -> str | None:
    text = path.name.lower()
    if any(x in text for x in ["wish", "想看", "想读", "想听", "想玩"]):
        return "wish"
    if any(x in text for x in ["do", "doing", "在看", "在读", "在听", "在玩"]):
        return "doing"
    if any(x in text for x in ["collect", "done", "看过", "读过", "听过", "玩过"]):
        return "done"
    return None


def pick_title_and_url(node):
    title_el = (
        node.select_one("li.title a")
        or node.select_one(".title a")
        or node.select_one("h2 a")
        or node.select_one("a[href]")
    )
    if not title_el:
        return None, None
    title = title_el.get_text(" ", strip=True)
    url = title_el.get("href", "").strip() or None
    return title, url


def split_tags(text: str | None) -> list[str]:
    if not text:
        return []
    parts = re.split(r"[,;/，；、|]+", text)
    return [p.strip() for p in parts if p.strip()]


def clean_text(text: str | None) -> str | None:
    if text is None:
        return None
    value = unescape(text).strip()
    return value or None


def maybe_creators_from_intro(intro: str | None) -> list[str]:
    if not intro:
        return []
    parts = [p.strip() for p in re.split(r"/|｜|\|", intro) if p.strip()]
    if not parts:
        return []
    creator_like = []
    for p in parts[:3]:
        if YEAR_RE.search(p):
            continue
        if len(p) <= 40:
            creator_like.append(p)
    return creator_like[:3]


def parse_movie_grid(soup: BeautifulSoup, status: str | None, source_name: str) -> list[Item]:
    items: list[Item] = []
    for node in soup.select(".grid-view > .item"):
        title, url = pick_title_and_url(node)
        if not title:
            continue
        comment_el = node.select_one("span.comment") or node.select_one(".comment")
        intro_el = node.select_one(".intro")
        intro = clean_text(intro_el.get_text(" ", strip=True) if intro_el else None)
        year = None
        if intro:
            m = YEAR_RE.search(intro)
            if m:
                year = m.group(0)
        items.append(
            Item(
                title=title,
                url=url,
                douban_id=extract_douban_id(url),
                subject_type="movie",
                status=status,
                rating=extract_rating(node),
                date=normalize_date(node.get_text(" ", strip=True)),
                tags=[intro] if intro else [],
                comment=clean_text(comment_el.get_text(" ", strip=True) if comment_el else None),
                creators=maybe_creators_from_intro(intro),
                year=year,
                raw_meta={"source_file": source_name, "intro": intro} if intro else {"source_file": source_name},
            )
        )
    return items


def parse_book_list(soup: BeautifulSoup, status: str | None, source_name: str) -> list[Item]:
    items: list[Item] = []
    for node in soup.select("li.subject-item"):
        info = node.select_one(".info") or node
        title, url = pick_title_and_url(info)
        if not title:
            continue
        pub_el = info.select_one(".pub")
        comment_el = info.select_one(".comment")
        pub = clean_text(pub_el.get_text(" ", strip=True) if pub_el else None)
        year = None
        if pub:
            m = YEAR_RE.search(pub)
            if m:
                year = m.group(0)
        items.append(
            Item(
                title=title,
                url=url,
                douban_id=extract_douban_id(url),
                subject_type="book",
                status=status,
                rating=extract_rating(info),
                date=normalize_date(info.get_text(" ", strip=True)),
                tags=[pub] if pub else [],
                comment=clean_text(comment_el.get_text(" ", strip=True) if comment_el else None),
                creators=maybe_creators_from_intro(pub),
                year=year,
                raw_meta={"source_file": source_name, "pub": pub} if pub else {"source_file": source_name},
            )
        )
    return items


def parse_music_list(soup: BeautifulSoup, status: str | None, source_name: str) -> list[Item]:
    items: list[Item] = []
    for node in soup.select("li.item"):
        info = node.select_one(".info") or node
        title, url = pick_title_and_url(info)
        if not title or (url and "subject" not in url):
            continue
        intro_el = info.select_one(".intro") or info.select_one(".pub")
        comment_el = info.select_one(".comment")
        intro = clean_text(intro_el.get_text(" ", strip=True) if intro_el else None)
        year = None
        if intro:
            m = YEAR_RE.search(intro)
            if m:
                year = m.group(0)
        items.append(
            Item(
                title=title,
                url=url,
                douban_id=extract_douban_id(url),
                subject_type="music",
                status=status,
                rating=extract_rating(info),
                date=normalize_date(info.get_text(" ", strip=True)),
                tags=[intro] if intro else [],
                comment=clean_text(comment_el.get_text(" ", strip=True) if comment_el else None),
                creators=maybe_creators_from_intro(intro),
                year=year,
                raw_meta={"source_file": source_name, "intro": intro} if intro else {"source_file": source_name},
            )
        )
    return items


def parse_game_list(soup: BeautifulSoup, status: str | None, source_name: str) -> list[Item]:
    items: list[Item] = []
    for node in soup.select(".game-list .common-item"):
        content = node.select_one(".content") or node
        title, url = pick_title_and_url(content)
        if not title:
            continue
        desc_el = content.select_one(".desc")
        comment_el = content.select_one(".comment")
        desc = clean_text(desc_el.get_text(" ", strip=True) if desc_el else None)
        items.append(
            Item(
                title=title,
                url=url,
                douban_id=extract_douban_id(url),
                subject_type="game",
                status=status,
                rating=extract_rating(content),
                date=normalize_date(content.get_text(" ", strip=True)),
                tags=[desc] if desc else [],
                comment=clean_text(comment_el.get_text(" ", strip=True) if comment_el else None),
                creators=[],
                year=None,
                raw_meta={"source_file": source_name, "desc": desc} if desc else {"source_file": source_name},
            )
        )
    return items


def parse_file(path: Path) -> list[Item]:
    html = path.read_text(encoding="utf-8", errors="ignore")
    soup = BeautifulSoup(html, "lxml")
    status = infer_status_from_path(path)
    subject_type = infer_subject_type(None, html)

    if soup.select(".grid-view > .item"):
        return parse_movie_grid(soup, status, path.name)
    if soup.select("li.subject-item"):
        return parse_book_list(soup, status, path.name)
    if soup.select(".game-list .common-item"):
        return parse_game_list(soup, status, path.name)
    if subject_type == "music" or soup.select("li.item .info .title"):
        return parse_music_list(soup, status, path.name)
    return []


def load_paths(argv: list[str]) -> list[Path]:
    if len(argv) < 2:
        print("Usage: extract_douban_self_history.py <html-file> [more html files...]", file=sys.stderr)
        raise SystemExit(2)
    return [Path(p) for p in argv[1:]]


def dedupe(items: Iterable[Item]) -> list[dict]:
    seen: set[tuple] = set()
    result: list[dict] = []
    for item in items:
        data = asdict(item)
        data["tags"] = data.get("tags") or []
        data["creators"] = data.get("creators") or []
        key = (
            data.get("subject_type"),
            data.get("douban_id") or data.get("url") or data.get("title"),
            data.get("status"),
            data.get("date"),
        )
        if key in seen:
            continue
        seen.add(key)
        result.append({k: v for k, v in data.items() if v not in (None, [], "")})
    return result


def main(argv: list[str]) -> int:
    paths = load_paths(argv)
    collected: list[Item] = []
    for path in paths:
        if not path.exists():
            print(f"Missing file: {path}", file=sys.stderr)
            return 2
        collected.extend(parse_file(path))

    output = {
        "platform": "douban",
        "owner": "self",
        "items": dedupe(collected),
        "count": len(dedupe(collected)),
        "sources": [str(p) for p in paths],
    }
    json.dump(output, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
