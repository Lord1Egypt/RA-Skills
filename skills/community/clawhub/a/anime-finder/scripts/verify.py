#!/usr/bin/env python3
"""Verify anime identity via Bangumi API before searching resources."""

import sys
import json
import urllib.request
import urllib.parse
import re


# Season/episode keywords to strip for fallback search
_SEASON_PATTERNS = [
    r'第[一二三四五六七八九十\d]+\s*(?:季|部|篇)',
    r'(?:Season|S)\s*\d+',
    r'Part\s*\d+',
    r'Season\s*\d+',
    r'[Ss]\d+',
]

_EPISODE_PATTERNS = [
    r'第[一二三四五六七八九十\d]+\s*(?:集|话|話|回|期)',
    r'(?:EP|E)\s*\d+',
    r'最新.*[集话]',
]


def _extract_core_query(query: str) -> str:
    """
    Strip season/episode indicators from query to get the core series name.
    e.g. "JOJO的奇妙冒险 第七季" → "JOJO的奇妙冒险"
         "斗罗大陆2绝世唐门 第133集" → "斗罗大陆2绝世唐门"
    """
    result = query
    for pattern in _SEASON_PATTERNS + _EPISODE_PATTERNS:
        result = re.sub(pattern, '', result, flags=re.IGNORECASE)
    return result.strip()


def _name_matches_query(name: str, query: str) -> bool:
    """Check if a name is relevantly similar to the user's query."""
    if not name:
        return False
    name_lower = name.lower()
    query_lower = query.lower()
    # Query is contained in the name
    if query_lower in name_lower:
        return True
    # Remove punctuation/spaces and check
    name_clean = re.sub(r'[\s\W_]', '', name_lower)
    query_clean = re.sub(r'[\s\W_]', '', query_lower)
    if query_clean in name_clean or name_clean in query_clean:
        return True
    return False


def search_bangumi(query: str) -> tuple[list[dict], bool]:
    """
    Search Bangumi for anime subjects.
    Returns (results, api_ok). api_ok is False on network/API errors.
    Retries up to 2 times with 3s interval on timeout.
    """
    url = f"https://api.bgm.tv/search/subject/{urllib.parse.quote(query)}?type=2"
    max_retries = 2

    for attempt in range(max_retries + 1):
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": "Mozilla/5.0",
                "Accept": "application/json",
            })
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode())
                return data.get("list", []), True
        except (urllib.error.URLError, TimeoutError, OSError):
            if attempt < max_retries:
                import time
                time.sleep(3)
            continue

    return [], False


def get_subject_info(subject_id: int) -> dict:
    """Get detailed subject info."""
    url = f"https://api.bgm.tv/subject/{subject_id}"
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json",
        })
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except Exception:
        return {}


def verify_anime(query: str, output_json: bool = False) -> dict:
    """
    Verify anime identity. Returns:
    {
        "status": "found|ambiguous|not_found|api_error",
        "query": "...",
        "match": {...},  # best match if found
        "alternatives": [...],  # other matches if ambiguous
        "suggestion": "...",  # corrected name if not found
    }
    """
    core_query = _extract_core_query(query)
    results, api_ok = search_bangumi(query)

    if not api_ok:
        return {
            "status": "api_error",
            "query": query,
            "core_query": core_query,
            "message": f"Bangumi API 无法访问，可能是网络问题或 API 限流",
        }

    if not results:
        # Fallback: strip season/episode and retry with core series name
        if core_query != query:
            core_results, core_api_ok = search_bangumi(core_query)
            if core_api_ok and core_results:
                # Build alternatives from the broader search
                alternatives = []
                for r in core_results[:5]:
                    r_info = get_subject_info(r["id"])
                    name = r_info.get("name_cn") or r_info.get("name") or r.get("name")
                    if name:
                        alternatives.append({
                            "name": name,
                            "name_jp": r.get("name"),
                            "air_date": r.get("air_date", ""),
                            "url": r.get("url", ""),
                            "rating": r_info.get("rating", {}).get("score", "N/A"),
                        })
                return {
                    "status": "not_found",
                    "query": query,
                    "core_query": core_query,
                    "message": f"Bangumi 上未找到与「{query}」完全匹配的番剧",
                    "suggestion": f"试试用系列名称「{core_query}」搜索，可能的选项见 alternatives",
                    "alternatives": alternatives,
                }

        return {
            "status": "not_found",
            "query": query,
            "core_query": core_query,
            "message": f"Bangumi 上未找到与「{query}」匹配的番剧",
        }

    best = results[0]

    # Get detailed info for the top result
    info = get_subject_info(best["id"])

    # Only include alternatives that are actually similar to the user's query
    alternatives = []
    if len(results) > 1:
        first_score = best.get("id", 0)
        for r in results[1:5]:
            r_info = get_subject_info(r["id"])
            name = r_info.get("name_cn") or r_info.get("name") or r.get("name")
            if name and name != (info.get("name_cn") or info.get("name")):
                # Only show as alternative if query-relevant
                if _name_matches_query(name, query):
                    alternatives.append({
                        "name": r.get("name_cn") or r.get("name"),
                        "name_jp": r.get("name"),
                        "air_date": r.get("air_date", ""),
                        "url": r.get("url", ""),
                    })

    status = "ambiguous" if alternatives else "found"

    result = {
        "status": status,
        "query": query,
        "core_query": core_query,
        "match": {
            "name": info.get("name_cn") or best.get("name"),
            "name_jp": best.get("name"),
            "air_date": best.get("air_date", ""),
            "rating": info.get("rating", {}).get("score", "N/A"),
            "url": best.get("url", ""),
            "id": best.get("id"),
        },
        "alternatives": alternatives,
    }

    return result


def main():
    if len(sys.argv) < 2:
        print("Usage: verify.py <anime_name> [--json]")
        sys.exit(1)

    query = sys.argv[1]
    output_json = "--json" in sys.argv
    data = verify_anime(query, output_json)

    if output_json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        match = data.get("match", {})
        print(f"📺 番剧确认")
        print(f"   你的搜索：{data['query']}")
        if match:
            print(f"   找到：「{match['name']}」")
            if match.get("air_date"):
                print(f"   首播：{match['air_date']}")
            if match.get("rating") and match['rating'] != "N/A":
                print(f"   Bangumi 评分：{match['rating']}")
            print(f"   详情：{match['url']}")

        alts = data.get("alternatives", [])
        if alts:
            print(f"\n   其他可能：")
            for i, a in enumerate(alts, 1):
                date_str = f'（{a["air_date"]}）' if a.get("air_date") else ""
                print(f"   {i}. 「{a['name']}」{date_str}")
                print(f"      {a['url']}")

        if data["status"] == "not_found":
            print(f"   ❌ {data.get('message', '未找到')}")
        elif data["status"] == "api_error":
            print(f"   ⚠️  {data.get('message', 'API 无法访问')}")
            print(f"   💡 建议：检查网络连接，或直接用番名在 Nyaa.si 搜索")


if __name__ == "__main__":
    main()
