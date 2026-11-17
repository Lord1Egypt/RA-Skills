"""Generate static HTML detail pages for each qualified work.
Each page has proper OG meta tags for WeChat/social sharing."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

_ROOT = Path(__file__).parent.parent
DATA_DIR = _ROOT / "data"
DETAIL_DIR = _ROOT / "detail"

RESULT_FILE = DATA_DIR / "douban-monitor-result.json"
FAVORITES_FILE = DATA_DIR / "douban-monitor-favorites-result.json"
METADATA_FILE = DATA_DIR / "douban-monitor-metadata.json"
POSTERS_FILE = DATA_DIR / "douban-monitor-posters.json"
LIBRARY_FILE = DATA_DIR / "douban-monitor-library.json"


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, ValueError):
        return {}


def esc(s: str) -> str:
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def generate_detail_html(item: dict, metadata: dict, posters: dict) -> str:
    """Generate a minimal HTML page with OG meta tags for sharing."""
    douban_id = item.get("douban_id", "")
    title = item.get("title", "未知")
    rating = item.get("rating", "N/A")
    rating_count = item.get("rating_count", 0)
    year = item.get("year", "")
    category = item.get("category", "")

    # Get extended metadata
    meta = metadata.get(douban_id, {})
    poster_path = meta.get("poster_path") or posters.get(douban_id)
    genres = meta.get("genres", [])
    release_date = meta.get("release_date", "")
    overview = (meta.get("overview") or "")[:150]
    countries = meta.get("countries", [])

    # posters.json already stores full TMDB URLs; only metadata.poster_path is a bare path.
    tmdb_base = "https://image.tmdb.org/t/p/w500"
    if not poster_path:
        poster_url = ""
    elif poster_path.startswith("http://") or poster_path.startswith("https://"):
        poster_url = poster_path
    else:
        poster_url = f"{tmdb_base}/{poster_path.lstrip('/')}"

    # Format rating count
    if rating_count >= 10000:
        count_str = f"{rating_count / 10000:.1f}万"
    else:
        count_str = str(rating_count)

    # Build title and description for WeChat share card
    og_title = f"《{title}》"

    cat_label = {"movie": "电影", "tv": "剧集", "variety": "综艺"}.get(category, "")
    release_year = (release_date[:4] if release_date else None) or (str(year) if year else "")
    _country_names = {
        "CN": "中国", "HK": "香港", "TW": "台湾", "JP": "日本",
        "KR": "韩国", "US": "美国", "GB": "英国", "FR": "法国",
        "DE": "德国", "IT": "意大利", "ES": "西班牙", "TH": "泰国",
        "IN": "印度", "AU": "澳大利亚", "CA": "加拿大", "RU": "俄罗斯",
    }
    raw_country = countries[0] if countries else ""
    country = _country_names.get(raw_country, raw_country)
    genre_str = "、".join(genres[:2]) if genres else ""

    parts = []
    if release_year:
        parts.append(f"{release_year}年")
    if country:
        parts.append(country)
    if cat_label:
        parts.append(cat_label)

    lines = ["·".join(parts)]
    if genre_str:
        lines.append(genre_str)
    lines.append(f"{count_str}人打出{rating}分")
    og_desc = "\n".join(line for line in lines if line)

    # Generate minimal HTML with OG tags
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{esc(og_title)}</title>
  
  <!-- Open Graph for WeChat / social sharing -->
  <meta property="og:title" content="{esc(og_title)}" />
  <meta property="og:description" content="{esc(og_desc)}" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="https://douban.juryory.com/detail/{douban_id}.html" />
'''
    if poster_url:
        html += f'  <meta property="og:image" content="{esc(poster_url)}" />\n'
    
    html += f'''
  <!-- WeChat specific -->
  <meta name="weixin:share:description" content="{esc(og_desc)}" />
  <meta itemprop="name" content="{esc(og_title)}" />
  <meta itemprop="description" content="{esc(og_desc)}" />
'''
    if poster_url:
        html += f'  <meta itemprop="image" content="{esc(poster_url)}" />\n'
    
    # Use JS redirect (not meta refresh) so crawlers like WeChat stop at this
    # static page and read its OG/title tags instead of following the redirect
    # to index.html and picking up its generic "豆瓣高分监控" title.
    html += f'''
  <script>window.location.replace("../#detail/{douban_id}");</script>
  <noscript><meta http-equiv="refresh" content="0;url=../#detail/{douban_id}" /></noscript>
</head>
<body style="text-align:center;padding:40px;font-family:sans-serif;">
  <p>正在跳转到 <a href="../#detail/{douban_id}">{esc(title)}</a>...</p>
</body>
</html>'''
    return html


def _library_item_to_share_item(lib_item: dict) -> dict:
    """Adapt a library.json item to the shape generate_detail_html expects."""
    return {
        "douban_id": lib_item.get("douban_id") or lib_item.get("key", ""),
        "title": lib_item.get("title", "未知"),
        "rating": lib_item.get("last_rating", "N/A"),
        "rating_count": lib_item.get("last_rating_count", 0) or 0,
        "year": lib_item.get("year", ""),
        "category": lib_item.get("category", ""),
    }


def main() -> None:
    # Load data
    result = load_json(RESULT_FILE)
    fav_result = load_json(FAVORITES_FILE)
    metadata = load_json(METADATA_FILE)
    posters = load_json(POSTERS_FILE)
    library = load_json(LIBRARY_FILE)

    # Collect all qualified works
    all_items: list[dict] = []
    seen: set[str] = set()

    for item in result.get("qualified", []):
        did = item.get("douban_id")
        if did and did not in seen:
            seen.add(did)
            all_items.append(item)

    for item in fav_result.get("qualified", []):
        did = item.get("douban_id")
        if did and did not in seen:
            seen.add(did)
            all_items.append(item)

    # Also refresh any existing detail page whose item is still in the library,
    # so historical pages stop showing stale share metadata.
    DETAIL_DIR.mkdir(parents=True, exist_ok=True)
    lib_items = library.get("items", {}) if isinstance(library, dict) else {}
    for html_path in sorted(DETAIL_DIR.glob("*.html")):
        did = html_path.stem
        if did in seen:
            continue
        lib_item = lib_items.get(did)
        if not lib_item or not lib_item.get("douban_id"):
            continue
        seen.add(did)
        all_items.append(_library_item_to_share_item(lib_item))

    if not all_items:
        print("无达标作品，跳过生成详情页")
        return

    generated = 0
    for item in all_items:
        douban_id = item.get("douban_id", "")
        title = item.get("title", "未知")

        html = generate_detail_html(item, metadata, posters)
        output_path = DETAIL_DIR / f"{douban_id}.html"
        output_path.write_text(html, encoding="utf-8")
        generated += 1
        print(f"  [OK] {title} ({douban_id})")

    print(f"\n完成：生成 {generated} 个详情页至 {DETAIL_DIR}")


if __name__ == "__main__":
    main()
