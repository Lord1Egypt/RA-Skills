"""Fetch rich metadata (overview, genres, original title, runtime) from TMDB."""
from __future__ import annotations

import json
import os
import re
import sys
import time
from difflib import SequenceMatcher
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
from monitor import rexxar_get, tmdb_get, DEFAULT_CONFIG

DATA_DIR = _ROOT / "data"
RESULT_FILE = DATA_DIR / "douban-monitor-result.json"
META_FILE   = DATA_DIR / "douban-monitor-metadata.json"

_SEASON_RE = re.compile(
    r"\s*(?:第[一二三四五六七八九十百\d]+[季部篇章]|Season\s*\d+|S\d+)\s*$",
    re.IGNORECASE,
)
_CJK_LATIN_TAIL_RE = re.compile(
    r"^([\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af\d]+)([A-Za-z]+)$"
)


def _clean(t: str) -> str:
    return _SEASON_RE.sub("", t).strip()


def _sim(a: str, b: str) -> float:
    return SequenceMatcher(None, _clean(a).lower(), _clean(b).lower()).ratio()


def _variants(title: str) -> list[str]:
    clean = _clean(title)
    vs = [clean]
    parts = clean.split()
    if len(parts) > 1:
        m = _CJK_LATIN_TAIL_RE.match(parts[-1])
        if m and m.group(1):
            c = " ".join(parts[:-1] + [m.group(1)])
            if c not in vs:
                vs.append(c)
        wo = " ".join(parts[:-1])
        if wo and wo not in vs:
            vs.append(wo)
    return vs


def _get_imdb(douban_id: str) -> str | None:
    for ep in (f"/movie/{douban_id}", f"/tv/{douban_id}"):
        try:
            data = rexxar_get(ep)
            v = str(data.get("imdb") or data.get("imdb_id") or "").strip()
            if v.startswith("tt"):
                return v
        except Exception:
            continue
    return None


def _find_by_imdb(imdb_id: str, config: dict) -> tuple[int, str] | None:
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
    return None


def _find_by_search(title: str, category: str, year: str, config: dict) -> tuple[int, str] | None:
    ep = "/search/movie" if category == "movie" else "/search/tv"
    typ = "movie" if category == "movie" else "tv"
    for variant in _variants(title):
        for use_year in (True, False):
            params: dict = {"query": variant, "language": "zh-CN", "page": 1}
            if use_year and year and year.isdigit():
                k = "primary_release_year" if category == "movie" else "first_air_date_year"
                params[k] = int(year)
            try:
                rows = tmdb_get(ep, config, params).get("results") or []
                if rows:
                    best = max(rows, key=lambda r: _sim(title, r.get("title") or r.get("name") or ""))
                    return int(best["id"]), typ
            except Exception:
                pass
            time.sleep(0.15)
    return None


def _fetch_detail(tmdb_id: int, tmdb_type: str, config: dict) -> dict:
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
        release_date = d.get("release_date") or d.get("first_air_date") or ""

        # Backdrop
        backdrop_path = d.get("backdrop_path") or ""

        # Countries
        if tmdb_type == "movie":
            countries = [c.get("name", c.get("iso_3166_1", ""))
                         for c in (d.get("production_countries") or [])]
        else:
            countries = list(d.get("origin_country") or [])

        # Director / Creator
        credits = d.get("credits") or {}
        if tmdb_type == "movie":
            directors = [p["name"] for p in (credits.get("crew") or [])
                         if p.get("job") == "Director"]
            director = directors[0] if directors else ""
        else:
            creators = d.get("created_by") or []
            director = creators[0]["name"] if creators else ""

        # Cast (top 8)
        cast_raw = (credits.get("cast") or [])[:8]
        cast = [{"name": p.get("name", ""),
                 "character": p.get("character", ""),
                 "profile_path": p.get("profile_path") or ""}
                for p in cast_raw]

        # Stills / backdrops (top 10)
        images = d.get("images") or {}
        stills = [img["file_path"] for img in (images.get("backdrops") or [])[:10]
                  if img.get("file_path")]

        # Similar + Recommendations (merge, dedupe, top 8)
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
            "tmdb_id":        tmdb_id,
            "tmdb_type":      tmdb_type,
            "original_title": d.get("original_title") or d.get("original_name") or "",
            "overview":       d.get("overview") or "",
            "genres":         genres,
            "runtime":        runtime,
            "release_date":   release_date,
            "backdrop_path":  backdrop_path,
            "poster_path":    d.get("poster_path") or "",
            "countries":      countries,
            "director":       director,
            "cast":           cast,
            "stills":         stills,
            "similar":        similar,
        }
    except Exception:
        return {}


def main() -> None:
    text = RESULT_FILE.read_text(encoding="utf-8").strip() if RESULT_FILE.exists() else ""
    if not text:
        print(f"{RESULT_FILE} 缺失或为空，跳过元数据抓取")
        return
    try:
        result = json.loads(text)
    except json.JSONDecodeError as e:
        print(f"{RESULT_FILE} 解析失败（{e}），跳过元数据抓取")
        return
    items = result.get("qualified", [])

    seen: set[str] = set()
    unique = []
    for item in items:
        did = item.get("douban_id")
        if did and did not in seen:
            seen.add(did)
            unique.append(item)

    meta: dict[str, dict] = {}
    if META_FILE.exists():
        text = META_FILE.read_text(encoding="utf-8").strip()
        if text:
            meta = json.loads(text)

    config = {**DEFAULT_CONFIG, "tmdb_language": "zh-CN", "tmdb_region": "CN"}
    total = len(unique)

    for i, item in enumerate(unique):
        did      = item["douban_id"]
        title    = item["title"]
        category = item.get("category", "movie")
        year     = str(item.get("year") or "")
        prefix   = f"[{i+1}/{total}]"

        if did in meta and "backdrop_path" in meta[did]:
            mark = "[OK]" if meta[did].get("overview") else "[--]"
            print(f"{prefix} skip {mark} {title}")
            continue

        print(f"{prefix} {title} ({category})", end="  ", flush=True)
        found: tuple[int, str] | None = None

        if category != "show":
            imdb_id = _get_imdb(did)
            time.sleep(0.3)
            if imdb_id:
                found = _find_by_imdb(imdb_id, config)
                if found:
                    print(f"imdb={imdb_id}", end=" ", flush=True)
                time.sleep(0.2)

        if not found:
            found = _find_by_search(title, category, year, config)
            if found:
                print(f"tmdb={found[0]}", end=" ", flush=True)

        if not found:
            meta[did] = {}
            print("(not found)")
            continue

        detail = _fetch_detail(found[0], found[1], config)
        meta[did] = detail
        time.sleep(0.25)
        ov = detail.get("overview") or ""
        print(ov[:60] + "…" if len(ov) > 60 else (ov or "(no overview)"))

    META_FILE.write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    found_count = sum(1 for v in meta.values() if v.get("overview"))
    print(f"\n完成：{found_count}/{len(meta)} 条有简介，保存至 {META_FILE}")


if __name__ == "__main__":
    main()
