#!/usr/bin/env python3
"""Parse generic `mail ...` commands into structured JSON actions.

Portable parser for community skill usage.
"""

from __future__ import annotations

import json
import os
import re
import sys
from dataclasses import asdict, dataclass
from typing import Literal

Mode = Literal["keyword", "semantic", "hybrid"]
Action = Literal["help", "search", "recents", "sync", "labels", "status"]


@dataclass
class Parsed:
    action: Action
    query: str | None = None
    mode: Mode = "hybrid"
    limit: int = 5
    label: str | None = None
    resume: bool = False
    after: str | None = None
    before: str | None = None


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip())


def _env_int(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, str(default)))
    except Exception:
        return default


def _defaults() -> tuple[Mode, int, int]:
    max_limit = max(1, _env_int("MAIL_MAX_LIMIT", 25))
    default_limit = min(max(1, _env_int("MAIL_DEFAULT_LIMIT", 5)), max_limit)
    mode = os.getenv("MAIL_DEFAULT_MODE", "hybrid").strip().lower()
    if mode not in {"keyword", "semantic", "hybrid"}:
        mode = "hybrid"
    return mode, default_limit, max_limit  # type: ignore[return-value]


def _parse_fuzzy_date(s: str):
    import datetime as dt

    t = s.strip()

    m = re.fullmatch(r"(\d{4})", t)
    if m:
        return dt.date(int(m.group(1)), 1, 1), "year"

    m = re.fullmatch(r"(\d{1,2})/(\d{4})", t)
    if m:
        return dt.date(int(m.group(2)), int(m.group(1)), 1), "month"

    m = re.fullmatch(r"(\d{4})-(\d{1,2})", t)
    if m:
        return dt.date(int(m.group(1)), int(m.group(2)), 1), "month"

    m = re.fullmatch(r"(\d{4})-(\d{1,2})-(\d{1,2})", t)
    if m:
        return dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3))), "day"

    return None, None


def _month_add(d, months: int):
    import datetime as dt

    y = d.year + (d.month - 1 + months) // 12
    m = (d.month - 1 + months) % 12 + 1
    return dt.date(y, m, 1)


def _parse_limit_tokens(tokens: list[str], max_limit: int, fallback: int) -> int:
    limit = fallback
    for i, tok in enumerate(tokens):
        if tok.lower() in {"max", "top", "limit", "limite"} and i + 1 < len(tokens):
            n = re.sub(r"[^0-9]", "", tokens[i + 1])
            if n.isdigit():
                limit = min(max(1, int(n)), max_limit)
                break
    return limit


def parse(text: str) -> Parsed:
    default_mode, default_limit, max_limit = _defaults()

    t = text.strip()
    m = re.match(r"^\s*mail\b[:\-–—\s]*", t, flags=re.IGNORECASE)
    if not m:
        return Parsed(action="help", mode=default_mode, limit=default_limit)

    rest = _norm(t[m.end() :])
    if not rest or rest.lower() in {"help", "?"}:
        return Parsed(action="help", mode=default_mode, limit=default_limit)

    low = rest.lower()
    if low in {"sync"}:
        return Parsed(action="sync", mode=default_mode, limit=default_limit)
    if low in {"labels", "label"}:
        return Parsed(action="labels", mode=default_mode, limit=default_limit)
    if low in {"status", "stat"}:
        return Parsed(action="status", mode=default_mode, limit=default_limit)

    recents_words = ("recents", "recent", "recentes", "récents", "récénts")
    if low.startswith(recents_words):
        tokens = rest.split(" ")
        limit = _parse_limit_tokens(tokens, max_limit=max_limit, fallback=default_limit)
        return Parsed(action="recents", mode=default_mode, limit=limit)

    limit = default_limit
    resume = False
    mode: Mode = default_mode
    label = None
    after: str | None = None
    before: str | None = None

    tokens = rest.split(" ")
    consumed = set()

    def get_int(i: int) -> int | None:
        if i < 0 or i >= len(tokens):
            return None
        try:
            return int(re.sub(r"[^0-9]", "", tokens[i]))
        except Exception:
            return None

    i = 0
    while i < len(tokens):
        tok = tokens[i].lower()

        if tok in {"max", "top", "limit", "limite"}:
            n = get_int(i + 1)
            if n is not None and n > 0:
                limit = max(1, min(n, max_limit))
                consumed.update({i, i + 1})
                i += 2
                continue

        if tok in {"resume", "résume", "résumé", "summary"}:
            resume = True
            consumed.add(i)
            i += 1
            continue

        if tok in {"keyword", "fts"}:
            mode = "keyword"
            consumed.add(i)
            i += 1
            continue
        if tok in {"semantic", "semantique", "sémantique"}:
            mode = "semantic"
            consumed.add(i)
            i += 1
            continue
        if tok in {"hybrid", "mix", "fusion"}:
            mode = "hybrid"
            consumed.add(i)
            i += 1
            continue

        if tok in {"label", "tag"} and i + 1 < len(tokens):
            label = tokens[i + 1]
            consumed.update({i, i + 1})
            i += 2
            continue

        if tok in {"after"} and i + 1 < len(tokens):
            d, _ = _parse_fuzzy_date(tokens[i + 1])
            if d:
                after = d.isoformat()
                consumed.update({i, i + 1})
                i += 2
                continue

        if tok in {"before"} and i + 1 < len(tokens):
            d, _ = _parse_fuzzy_date(tokens[i + 1])
            if d:
                before = d.isoformat()
                consumed.update({i, i + 1})
                i += 2
                continue

        if tok in {"between"} and i + 3 < len(tokens) and tokens[i + 2].lower() == "and":
            d1, _p1 = _parse_fuzzy_date(tokens[i + 1])
            d2, p2 = _parse_fuzzy_date(tokens[i + 3])
            if d1 and d2:
                import datetime as dt

                after = d1.isoformat()
                if p2 == "year":
                    before = dt.date(d2.year + 1, 1, 1).isoformat()
                elif p2 == "month":
                    before = _month_add(d2, 1).isoformat()
                else:
                    before = (d2 + dt.timedelta(days=1)).isoformat()

                consumed.update({i, i + 1, i + 2, i + 3})
                i += 4
                continue

        i += 1

    query_tokens = [t for j, t in enumerate(tokens) if j not in consumed]
    query = _norm(" ".join(query_tokens))

    if not query:
        return Parsed(action="help", mode=default_mode, limit=default_limit)

    return Parsed(
        action="search",
        query=query,
        mode=mode,
        limit=limit,
        label=label,
        resume=resume,
        after=after,
        before=before,
    )


def main(argv: list[str]) -> int:
    text = " ".join(argv) if argv else sys.stdin.read()
    print(json.dumps(asdict(parse(text)), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
