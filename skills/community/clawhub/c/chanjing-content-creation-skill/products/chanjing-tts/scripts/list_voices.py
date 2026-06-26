#!/usr/bin/env python3
"""
列出公共声音人。与 chanjing-credentials-guard 使用同一配置文件获取 Token。
用法: list_voices [--page 1] [--size 100] [--fetch-all] [--json]
输出: 默认打印摘要表（id / name / gender / audition）；--json 时输出完整 data。
--fetch-all 从第 1 页起连续翻页直至 total_count 全覆盖（公共音色选型推荐）。
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _auth import resolve_chanjing_access_token

API_BASE = __import__("os").environ.get("CHANJING_API_BASE", "https://open-api.chanjing.cc")


def _fetch_page(token: str, page: int, size: int) -> dict:
    qs = urllib.parse.urlencode({"page": page, "size": size})
    url = f"{API_BASE}/open/v1/list_common_audio?{qs}"
    req = urllib.request.Request(url, headers={"access_token": token}, method="GET")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_until_complete(
    token: str,
    page_size: int,
    *,
    max_safety_pages: int = 50,
) -> tuple[list | None, list[int], dict, dict]:
    """从第 1 页连续请求直至空页或 total_count 覆盖。"""
    all_items: list = []
    pages_fetched: list[int] = []
    first_page_info: dict = {}
    last_data: dict = {}
    total_target: int | None = None
    page = 1

    for _ in range(max_safety_pages):
        res = _fetch_page(token, page, page_size)
        if res.get("code") != 0:
            return None, pages_fetched, first_page_info, res

        data = res.get("data", {}) or {}
        items = data.get("list") or []
        last_data = data

        if page == 1:
            first_page_info = dict(data.get("page_info") or {})
            tc = first_page_info.get("total_count")
            if tc is not None:
                try:
                    total_target = int(tc)
                except (TypeError, ValueError):
                    total_target = None

        if not items:
            break

        pages_fetched.append(page)
        all_items.extend(items)

        if total_target is not None and len(all_items) >= total_target:
            break
        page += 1

    seen: set = set()
    deduped: list = []
    for item in all_items:
        vid = str(item.get("id", "")).strip()
        key = vid or id(item)
        if key not in seen:
            seen.add(key)
            deduped.append(item)

    return deduped, pages_fetched, first_page_info, last_data


def print_table(items: list, header_note: str = "") -> None:
    print(header_note)
    print(
        f"{'id':<44}  {'name':<18}  {'gender':<8}  audition"
    )
    print("-" * 140)
    for v in items:
        print(
            f"{v.get('id', ''):<44}  "
            f"{v.get('name', ''):<18}  "
            f"{v.get('gender', ''):<8}  "
            f"{v.get('audition', '')}"
        )


def main():
    parser = argparse.ArgumentParser(description="列出蝉镜公共声音人")
    parser.add_argument("--page", type=int, default=1, help="起始页码")
    parser.add_argument("--size", type=int, default=100, help="每页数量")
    parser.add_argument(
        "--fetch-all",
        action="store_true",
        help="从第 1 页起自动翻页直至 total_count（推荐用于全量选型）",
    )
    parser.add_argument("--json", action="store_true", help="输出完整 JSON")
    args = parser.parse_args()

    token, err = resolve_chanjing_access_token()
    if err:
        print(err, file=sys.stderr)
        sys.exit(1)

    if args.fetch_all:
        merged, pages_fetched, first_pi, last_data = fetch_until_complete(
            token, args.size
        )
        if merged is None:
            err_msg = last_data if isinstance(last_data, dict) else {}
            print(err_msg.get("msg", err_msg) or "请求失败", file=sys.stderr)
            sys.exit(1)

        if args.json:
            print(
                json.dumps(
                    {
                        "fetch_all": True,
                        "pages_fetched": pages_fetched,
                        "data": {
                            "list": merged,
                            "page_info": {
                                **first_pi,
                                "merged_pages": pages_fetched,
                                "fetch_all": True,
                            },
                        },
                    },
                    ensure_ascii=False,
                    indent=2,
                )
            )
            return

        total_hint = first_pi.get("total_count", "")
        print_table(
            merged,
            f"# fetch-all | 接口 total≈{total_hint} | "
            f"已拉页 {pages_fetched} | 音色行 {len(merged)}",
        )
        return

    res = _fetch_page(token, args.page, args.size)
    if res.get("code") != 0:
        print(res.get("msg", res), file=sys.stderr)
        sys.exit(1)

    data = res.get("data", {})
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return

    items = data.get("list", [])
    page_info = data.get("page_info", {})
    print_table(
        items,
        f"# 共 {page_info.get('total_count', len(items))} 个声音 "
        f"(page={args.page}, size={args.size})",
    )


if __name__ == "__main__":
    main()
