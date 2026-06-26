#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
百度榜单抓取（首页聚合）
- 热搜
- 小说
- 电影
- 电视剧
"""

from __future__ import annotations

import argparse
import json
import re
from typing import Dict, List

import requests
from bs4 import BeautifulSoup

BAIDU_TOP_URL = "https://top.baidu.com/board?platform=pc&tab=homepage&sa=pc_index_homepage_all"
DEFAULT_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)


def _norm_line(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").strip())


def _fetch_lines(url: str, timeout: float, ua: str) -> List[str]:
    headers = {"User-Agent": ua or DEFAULT_UA}
    r = requests.get(url, headers=headers, timeout=timeout)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    text = soup.get_text("\n", strip=True)
    out: List[str] = []
    for x in text.splitlines():
        t = _norm_line(x)
        if t:
            out.append(t)
    return out


def _find_section(lines: List[str], title: str, end_titles: List[str]) -> List[str]:
    start = -1
    for i, x in enumerate(lines):
        if title in x:
            start = i + 1
            break
    if start < 0:
        return []
    end = len(lines)
    for i in range(start, len(lines)):
        if any(t in lines[i] for t in end_titles):
            end = i
            break
    return lines[start:end]


def _parse_ranked_items(lines: List[str], limit: int) -> List[Dict[str, str]]:
    items: List[Dict[str, str]] = []
    seen_rank = set()
    i = 0
    while i < len(lines):
        cur = lines[i]
        if re.fullmatch(r"\d{1,2}", cur):
            rank = int(cur)
            if rank not in seen_rank:
                title = ""
                j = i + 1
                while j < len(lines):
                    v = lines[j]
                    if re.fullmatch(r"\d{1,2}", v):
                        break
                    if v in ("热", "新", "更多", "实时脉搏", "热点活动", "百度指数"):
                        j += 1
                        continue
                    title = v
                    break

                if title:
                    heat = ""
                    k = j + 1
                    for _ in range(8):
                        if k >= len(lines):
                            break
                        hv = lines[k]
                        m = re.search(r"热搜指数[:：]\s*([0-9]+)", hv)
                        if m:
                            heat = m.group(1)
                            break
                        if re.fullmatch(r"[0-9]{3,}", hv):
                            heat = hv
                            break
                        if re.fullmatch(r"\d{1,2}", hv):
                            break
                        k += 1

                    items.append({"rank": rank, "title": title, "hot_score": heat})
                    seen_rank.add(rank)
                    if len(items) >= limit:
                        break
        i += 1

    items.sort(key=lambda x: int(x["rank"]))
    return items


def fetch_baidu_top(limit: int, timeout: float, ua: str) -> Dict[str, object]:
    n = max(1, min(int(limit), 50))
    lines = _fetch_lines(BAIDU_TOP_URL, timeout=timeout, ua=ua)

    sec_hot = _find_section(lines, "热搜榜", ["实时脉搏", "小说榜"])
    sec_novel = _find_section(lines, "小说榜", ["电影榜"])
    sec_movie = _find_section(lines, "电影榜", ["电视剧榜"])
    sec_drama = _find_section(lines, "电视剧榜", ["设为首页", "关于百度", "查看榜单规则"])

    return {
        "ok": True,
        "source": BAIDU_TOP_URL,
        "limit": n,
        "boards": {
            "hot": _parse_ranked_items(sec_hot, n),
            "novel": _parse_ranked_items(sec_novel, n),
            "movie": _parse_ranked_items(sec_movie, n),
            "tv": _parse_ranked_items(sec_drama, n),
        },
    }


def _print_human(data: Dict[str, object]) -> None:
    boards = data.get("boards", {}) if isinstance(data, dict) else {}
    title_map = [("hot", "热搜"), ("novel", "小说"), ("movie", "电影"), ("tv", "电视剧")]
    for key, name in title_map:
        arr = boards.get(key, []) if isinstance(boards, dict) else []
        print(f"【{name}榜】")
        if not arr:
            print("无")
            print("")
            continue
        for it in arr:
            rank = it.get("rank", "")
            t = it.get("title", "") or "无"
            hot = it.get("hot_score", "") or "无"
            print(f"{rank}. {t}（热度：{hot}）")
        print("")


def main() -> None:
    ap = argparse.ArgumentParser(description="百度榜单抓取：热搜/小说/电影/电视剧")
    ap.add_argument("-n", "--limit", type=int, default=10, help="每个榜单返回条数，默认 10，最大 50")
    ap.add_argument("--timeout", type=float, default=15.0, help="请求超时秒数，默认 15")
    ap.add_argument("--ua", default="", help="自定义 User-Agent")
    ap.add_argument("--json", action="store_true", help="以 JSON 输出（默认可读文本）")
    args = ap.parse_args()

    try:
        data = fetch_baidu_top(limit=args.limit, timeout=float(args.timeout), ua=args.ua.strip())
    except Exception as e:
        fail = {"ok": False, "error": str(e)}
        print(json.dumps(fail, ensure_ascii=False, indent=2))
        raise SystemExit(1)

    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        _print_human(data)


if __name__ == "__main__":
    main()

