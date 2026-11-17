"""Fetch details for manually added favorite items by douban_id.

Usage: add douban IDs to data/douban-monitor-favorites.json as a JSON array,
e.g. ["36190514", "35626404"]. This script will:
  1. Remove IDs already present in result.json (auto-cleanup)
  2. Fetch details (title, category, rating, etc.) from Douban Rexxar API
  3. Write enriched items to data/douban-monitor-favorites-result.json
  4. Fetch posters and metadata for these items (shared with main pipeline)
"""
from __future__ import annotations

import json
import os
import sys
import time
import urllib.request
from pathlib import Path

_ROOT = Path(__file__).parent.parent
_ENV_FILE = _ROOT / ".env"
if _ENV_FILE.exists():
    for _line in _ENV_FILE.read_text(encoding="utf-8").splitlines():
        _line = _line.strip()
        if _line and not _line.startswith("#") and "=" in _line:
            _k, _, _v = _line.partition("=")
            os.environ.setdefault(_k.strip(), _v.strip())

sys.path.insert(0, str(Path(__file__).parent))
from monitor import tmdb_get, DEFAULT_CONFIG

DATA_DIR = _ROOT / "data"
FAVORITES_FILE = DATA_DIR / "douban-monitor-favorites.json"
FAVORITES_RESULT_FILE = DATA_DIR / "douban-monitor-favorites-result.json"
RESULT_FILE = DATA_DIR / "douban-monitor-result.json"
POSTERS_FILE = DATA_DIR / "douban-monitor-posters.json"
META_FILE = DATA_DIR / "douban-monitor-metadata.json"

TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"


def _load_json(path: Path) -> dict | list:
    if not path.exists():
        return {} if path.suffix == ".json" else []
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return {} if "result" in path.name or "posters" in path.name or "metadata" in path.name else []
    try:
        return json.loads(text)
    except (json.JSONDecodeError, ValueError):
        return {} if "result" in path.name else []


_REXXAR_UA = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 "
    "Mobile/15E148 Safari/604.1"
)


def _rexxar_get(douban_id: str, media_type: str) -> dict:
    """Fetch subject detail via Douban mobile Rexxar API."""
    url = f"https://m.douban.com/rexxar/api/v2/{media_type}/{douban_id}?ck=&for_mobile=1"
    req = urllib.request.Request(url, headers={
        "User-Agent": _REXXAR_UA,
        "Accept": "application/json",
        "Referer": "https://m.douban.com/",
    })
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _fetch_subject(douban_id: str) -> dict | None:
    """Fetch movie/tv details from Douban mobile Rexxar API."""
    for media_type in ("movie", "tv"):
        try:
            d = _rexxar_get(douban_id, media_type)
            title = d.get("title", "")
            if not title:
                continue

            rating_obj = d.get("rating") or {}
            rating = rating_obj.get("value")
            rating_count = rating_obj.get("count")
            year_str = str(d.get("year") or "")

            # Category
            subtype = d.get("subtype") or d.get("type") or media_type
            if subtype == "movie":
                category = "movie"
            else:
                category = "tv"

            # Check for variety show
            genres = d.get("genres") or []
            if any(k in " ".join(genres) for k in ("真人秀", "综艺", "脱口秀")):
                category = "variety"

            # IMDB ID
            imdb_id = str(d.get("imdb") or "").strip() or None

            return {
                "title": title,
                "category": category,
                "douban_id": douban_id,
                "rating": float(rating) if rating else None,
                "rating_count": int(rating_count) if rating_count else None,
                "year": year_str,
                "url": f"https://movie.douban.com/subject/{douban_id}/",
                "imdb_id": imdb_id,
            }
        except Exception:
            continue
    return None


def _find_tmdb(imdb_id: str | None, title: str, category: str, year: str, config: dict) -> tuple[int, str] | None:
    """Find TMDB ID via IMDB or search."""
    if imdb_id and imdb_id.startswith("tt"):
        try:
            data = tmdb_get(f"/find/{imdb_id}", config, {
                "external_source": "imdb_id", "language": "zh-CN",
            })
            for key, typ in (("movie_results", "movie"), ("tv_results", "tv")):
                rows = data.get(key) or []
                if rows:
                    return int(rows[0]["id"]), typ
        except Exception:
            pass

    ep = "/search/movie" if category == "movie" else "/search/tv"
    typ = "movie" if category == "movie" else "tv"
    params: dict = {"query": title, "language": "zh-CN", "page": 1}
    if year and year.isdigit():
        k = "primary_release_year" if category == "movie" else "first_air_date_year"
        params[k] = int(year)
    try:
        rows = tmdb_get(ep, config, params).get("results") or []
        if rows:
            return int(rows[0]["id"]), typ
    except Exception:
        pass
    return None


def _fetch_tmdb_detail(tmdb_id: int, tmdb_type: str, config: dict) -> dict:
    """Fetch full TMDB metadata."""
    ep = f"/movie/{tmdb_id}" if tmdb_type == "movie" else f"/tv/{tmdb_id}"
    try:
        d = tmdb_get(ep, config, {
            "language": "zh-CN",
            "append_to_response": "credits,images,similar,recommendations",
            "include_image_language": "null,zh,en",
        })
        genres = [g["name"] for g in (d.get("genres") or [])]
        runtime = d.get("runtime")
        if runtime is None:
            ep_rt = d.get("episode_run_time") or []
            runtime = ep_rt[0] if ep_rt else None

        backdrop_path = d.get("backdrop_path") or ""
        poster_path = d.get("poster_path") or ""

        if tmdb_type == "movie":
            countries = [c.get("name", c.get("iso_3166_1", ""))
                         for c in (d.get("production_countries") or [])]
        else:
            countries = list(d.get("origin_country") or [])

        credits = d.get("credits") or {}
        if tmdb_type == "movie":
            directors = [p["name"] for p in (credits.get("crew") or [])
                         if p.get("job") == "Director"]
            director = directors[0] if directors else ""
        else:
            creators = d.get("created_by") or []
            director = creators[0]["name"] if creators else ""

        cast_raw = (credits.get("cast") or [])[:8]
        cast = [{"name": p.get("name", ""),
                 "character": p.get("character", ""),
                 "profile_path": p.get("profile_path") or ""}
                for p in cast_raw]

        images = d.get("images") or {}
        stills = [img["file_path"] for img in (images.get("backdrops") or [])[:10]
                  if img.get("file_path")]

        sim_raw = (d.get("similar") or {}).get("results") or []
        rec_raw = (d.get("recommendations") or {}).get("results") or []
        seen_ids: set[int] = set()
        similar: list[dict] = []
        for r in sim_raw + rec_raw:
            rid = r.get("id")
            if rid and rid not in seen_ids:
                seen_ids.add(rid)
                similar.append({
                    "tmdb_id": rid,
                    "title": r.get("title") or r.get("name") or "",
                    "poster_path": r.get("poster_path") or "",
                    "vote_average": r.get("vote_average") or 0,
                })
            if len(similar) >= 8:
                break

        return {
            "poster_path": poster_path,
            "metadata": {
                "tmdb_id": tmdb_id,
                "tmdb_type": tmdb_type,
                "original_title": d.get("original_title") or d.get("original_name") or "",
                "overview": d.get("overview") or "",
                "genres": genres,
                "runtime": runtime,
                "release_date": d.get("release_date") or d.get("first_air_date") or "",
                "backdrop_path": backdrop_path,
                "countries": countries,
                "director": director,
                "cast": cast,
                "stills": stills,
                "similar": similar,
            },
        }
    except Exception:
        return {}


def main() -> None:
    # Load favorites (one douban ID per line, plain text)
    fav_ids: list[str] = []
    if FAVORITES_FILE.exists():
        for line in FAVORITES_FILE.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                fav_ids.append(line)

    if not fav_ids:
        print("收藏列表为空，跳过")
        # Clear result file
        FAVORITES_RESULT_FILE.write_text(
            json.dumps({"qualified": []}, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        return

    # Load existing result.json to find already-qualified IDs
    result = _load_json(RESULT_FILE)
    if isinstance(result, dict):
        qualified_ids = {it["douban_id"] for it in (result.get("qualified") or []) if it.get("douban_id")}
    else:
        qualified_ids = set()

    # Auto-cleanup: remove IDs already in result.json
    cleaned_ids = [i for i in fav_ids if i not in qualified_ids]
    removed = set(fav_ids) - set(cleaned_ids)
    if removed:
        print(f"自动移除已收录的: {', '.join(removed)}")
        FAVORITES_FILE.write_text(
            "\n".join(cleaned_ids) + ("\n" if cleaned_ids else ""), encoding="utf-8"
        )

    if not cleaned_ids:
        print("所有收藏已被收录，清空收藏结果")
        FAVORITES_RESULT_FILE.write_text(
            json.dumps({"qualified": []}, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        return

    # Load existing poster/metadata stores
    posters: dict[str, str] = _load_json(POSTERS_FILE) if POSTERS_FILE.exists() else {}
    meta: dict[str, dict] = _load_json(META_FILE) if META_FILE.exists() else {}

    config = {**DEFAULT_CONFIG, "tmdb_language": "zh-CN", "tmdb_region": "CN"}

    items: list[dict] = []
    total = len(cleaned_ids)

    for i, did in enumerate(cleaned_ids):
        prefix = f"[{i+1}/{total}]"
        print(f"{prefix} {did}", end="  ", flush=True)

        # Fetch from Douban
        info = _fetch_subject(did)
        if not info:
            print("(豆瓣获取失败)")
            continue

        title = info["title"]
        print(f"{title}", end="  ", flush=True)
        time.sleep(0.3)

        # Build result item (without imdb_id which is internal)
        item = {k: v for k, v in info.items() if k != "imdb_id"}
        items.append(item)

        # Fetch TMDB data (poster + metadata) if not already cached
        if did not in posters or (did not in meta or "backdrop_path" not in (meta.get(did) or {})):
            found = _find_tmdb(info.get("imdb_id"), title, info["category"], info["year"], config)
            time.sleep(0.2)

            if found:
                tmdb_id, tmdb_type = found
                print(f"tmdb={tmdb_id}", end="  ", flush=True)
                detail = _fetch_tmdb_detail(tmdb_id, tmdb_type, config)

                if detail.get("poster_path") and did not in posters:
                    posters[did] = f"{TMDB_IMAGE_BASE}{detail['poster_path']}"

                if detail.get("metadata") and (did not in meta or "backdrop_path" not in (meta.get(did) or {})):
                    meta[did] = detail["metadata"]

                time.sleep(0.2)
            else:
                print("(TMDB未找到)", end="  ", flush=True)

        print("OK")

    # Save favorites result
    FAVORITES_RESULT_FILE.write_text(
        json.dumps({"qualified": items}, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # Save updated posters and metadata
    POSTERS_FILE.write_text(
        json.dumps(posters, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    META_FILE.write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"\n完成：{len(items)} 部收藏已处理，保存至 {FAVORITES_RESULT_FILE}")


if __name__ == "__main__":
    main()
