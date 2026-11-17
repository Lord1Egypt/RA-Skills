"""Fetch poster URLs for qualified items.

Strategy (per item):
  1. Rexxar API → IMDB ID → TMDB /find/{imdb_id}   (movies & TV, most accurate)
  2. TMDB fuzzy search → best-match by title similarity  (all categories incl. shows)
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
from difflib import SequenceMatcher
from pathlib import Path

# Load .env from project root
_ROOT = Path(__file__).parent.parent
_ENV_FILE = _ROOT / ".env"
if _ENV_FILE.exists():
    for _line in _ENV_FILE.read_text(encoding="utf-8").splitlines():
        _line = _line.strip()
        if _line and not _line.startswith("#") and "=" in _line:
            _k, _, _v = _line.partition("=")
            os.environ.setdefault(_k.strip(), _v.strip())

sys.path.insert(0, str(Path(__file__).parent))
from monitor import rexxar_get, tmdb_get, DEFAULT_CONFIG

DATA_DIR = Path(__file__).parent.parent / "data"
RESULT_FILE = DATA_DIR / "douban-monitor-result.json"
POSTERS_FILE = DATA_DIR / "douban-monitor-posters.json"

TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"

_SEASON_RE = re.compile(
    r"\s*(?:第[一二三四五六七八九十百\d]+[季部篇章]|Season\s*\d+|S\d+)\s*$",
    re.IGNORECASE,
)
# Matches a token that ends with CJK/digits then Latin letters, e.g. "十周年MT"
_CJK_LATIN_TAIL_RE = re.compile(
    r"^([\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af\d]+)([A-Za-z]+)$"
)


def _clean(title: str) -> str:
    return _SEASON_RE.sub("", title).strip()


def _similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, _clean(a).lower(), _clean(b).lower()).ratio()


def _title_variants(title: str) -> list[str]:
    """Return search candidates from most specific to least specific.

    Examples
    --------
    "请回答1988 十周年MT"  →  ["请回答1988 十周年MT", "请回答1988 十周年", "请回答1988"]
    "犯罪现场 Zero"        →  ["犯罪现场 Zero", "犯罪现场"]
    "单身即地狱"           →  ["单身即地狱"]
    """
    clean = _clean(title)
    variants: list[str] = [clean]
    parts = clean.split()

    if len(parts) > 1:
        last = parts[-1]
        # Rule 1: CJK+Latin混合末词 → 保留 CJK 部分，去掉 Latin 后缀
        m = _CJK_LATIN_TAIL_RE.match(last)
        if m and m.group(1):
            candidate = " ".join(parts[:-1] + [m.group(1)])
            if candidate not in variants:
                variants.append(candidate)

        # Rule 2: 直接去掉最后一个词
        without_last = " ".join(parts[:-1])
        if without_last and without_last not in variants:
            variants.append(without_last)

    return variants


def _best_poster(results: list[dict], ref_title: str) -> str:
    """Pick the result with highest title similarity and return its poster URL."""
    if not results:
        return ""
    best = max(
        results,
        key=lambda r: _similarity(ref_title, r.get("title") or r.get("name") or ""),
    )
    path = best.get("poster_path") or ""
    return f"{TMDB_IMAGE_BASE}{path}" if path else ""


# ---------------------------------------------------------------------------
# Step 1: Rexxar → IMDB ID → TMDB /find
# ---------------------------------------------------------------------------

def get_imdb_id_from_rexxar(douban_id: str) -> str | None:
    for endpoint in (f"/movie/{douban_id}", f"/tv/{douban_id}"):
        try:
            data = rexxar_get(endpoint)
            imdb = str(data.get("imdb") or data.get("imdb_id") or "").strip()
            if imdb.startswith("tt"):
                return imdb
        except Exception:
            continue
    return None


def find_poster_by_imdb(imdb_id: str, config: dict) -> str:
    try:
        data = tmdb_get(f"/find/{imdb_id}", config, {
            "external_source": "imdb_id",
            "language": "zh-CN",
        })
        for key in ("movie_results", "tv_results", "tv_season_results"):
            for item in (data.get(key) or []):
                path = item.get("poster_path") or ""
                if path:
                    return f"{TMDB_IMAGE_BASE}{path}"
    except Exception:
        pass
    return ""


# ---------------------------------------------------------------------------
# Step 2: TMDB fuzzy search (all categories)
# ---------------------------------------------------------------------------

def search_poster_fuzzy(title: str, category: str, year: str, config: dict) -> str:
    """Search TMDB with progressively simplified title variants.

    Each variant is tried with year filter first, then without. The best
    matching result (by title similarity) across all attempts is returned.
    """
    endpoint = "/search/movie" if category == "movie" else "/search/tv"
    variants = _title_variants(title)

    def _search(q: str, with_year: bool) -> list[dict]:
        params: dict = {"query": q, "language": "zh-CN", "page": 1}
        if with_year and year and year.isdigit():
            key = "primary_release_year" if category == "movie" else "first_air_date_year"
            params[key] = int(year)
        try:
            return tmdb_get(endpoint, config, params).get("results") or []
        except Exception:
            return []

    for variant in variants:
        for use_year in (True, False):
            results = _search(variant, use_year)
            if results:
                url = _best_poster(results, title)
                if url:
                    return url
            time.sleep(0.15)

    return ""


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    text = RESULT_FILE.read_text(encoding="utf-8").strip() if RESULT_FILE.exists() else ""
    if not text:
        print(f"{RESULT_FILE} 缺失或为空，跳过封面抓取")
        return
    try:
        result = json.loads(text)
    except json.JSONDecodeError as e:
        print(f"{RESULT_FILE} 解析失败（{e}），跳过封面抓取")
        return
    items = result.get("qualified", [])

    seen: set[str] = set()
    unique = []
    for item in items:
        did = item.get("douban_id")
        if did and did not in seen:
            seen.add(did)
            unique.append(item)

    posters: dict[str, str] = {}
    if POSTERS_FILE.exists():
        text = POSTERS_FILE.read_text(encoding="utf-8").strip()
        if text:
            posters = json.loads(text)

    metadata: dict = {}
    _meta_file = Path(__file__).parent.parent / "data" / "douban-monitor-metadata.json"
    if _meta_file.exists():
        try:
            metadata = json.loads(_meta_file.read_text(encoding="utf-8"))
        except Exception:
            pass

    config = {**DEFAULT_CONFIG, "tmdb_language": "zh-CN", "tmdb_region": "CN"}

    total = len(unique)
    for i, item in enumerate(unique):
        did = item["douban_id"]
        title = item["title"]
        category = item.get("category", "movie")
        year = str(item.get("year") or "")
        prefix = f"[{i+1}/{total}]"

        # Skip only when a non-empty poster URL is already cached
        if posters.get(did):
            print(f"{prefix} skip [OK] {title}")
            continue

        print(f"{prefix} {title} ({category})", end="  ", flush=True)
        url = ""

        # Step 0: use poster_path already stored in metadata (most reliable)
        meta = metadata.get(did, {})
        if meta.get("poster_path"):
            url = f"{TMDB_IMAGE_BASE}{meta['poster_path']}"
            print(f"meta={meta['poster_path']}", end=" ", flush=True)

        # Step 1: IMDB → TMDB /find
        if not url:
            imdb_id = get_imdb_id_from_rexxar(did)
            time.sleep(0.3)
            if imdb_id:
                print(f"imdb={imdb_id}", end=" ", flush=True)
                url = find_poster_by_imdb(imdb_id, config)
                time.sleep(0.2)

        # Step 2: direct TMDB id lookup (tmdb_id stored in metadata)
        if not url and meta.get("tmdb_id") and meta.get("tmdb_type"):
            tmdb_type = meta["tmdb_type"]
            tmdb_id = meta["tmdb_id"]
            try:
                d = tmdb_get(f"/{tmdb_type}/{tmdb_id}", config, {"language": "zh-CN"})
                path = d.get("poster_path") or ""
                if path:
                    url = f"{TMDB_IMAGE_BASE}{path}"
                    print(f"tmdb_id={tmdb_id}", end=" ", flush=True)
            except Exception:
                pass
            time.sleep(0.2)

        # Step 3: TMDB fuzzy search
        if not url:
            url = search_poster_fuzzy(title, category, year, config)
            time.sleep(0.2)

        posters[did] = url
        short = (url[:72] + "…") if len(url) > 72 else url
        print(short or "(none)")

    POSTERS_FILE.write_text(
        json.dumps(posters, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    found = sum(1 for v in posters.values() if v)
    print(f"\n完成：{found}/{len(posters)} 条找到封面，已保存到 {POSTERS_FILE}")


if __name__ == "__main__":
    main()
