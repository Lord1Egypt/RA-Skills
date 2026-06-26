#!/usr/bin/env python3
"""
列出可用于视频合成的数字人形象。
用法: list_figures [--source customised|common] [--page 1] [--page-size 20]
      [--max-pages N] [--fetch-all] [--json]
      [--tag-ids CSV] [--common-dp-source N]   # 仅 --source common：透传 list_common_dp
输出: 默认打印摘要表；--json 时输出完整 data。
--max-pages >1 时从 --page 起连续请求多页，合并 list 后再输出（便于跨页对比选型）。
--fetch-all 时按 total_count 自动翻页直至拉全（公共库选型：先全量列表再全局匹配；安全上限 300 页可调）。

公共库 tag_ids：逗号分隔，与 list_tag_dict 返回的子标签 id 一致；多 id 为 AND（官方语义）。
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _auth import resolve_chanjing_access_token

API_BASE = __import__("os").environ.get("CHANJING_API_BASE", "https://open-api.chanjing.cc")


@dataclass
class CommonListParams:
    """list_common_dp 可选查询：仅 source=common 时使用。"""

    tag_ids: str = ""
    common_dp_source: Optional[int] = None


def fetch_customised(token, page, page_size):
    body = json.dumps({"page": page, "page_size": page_size}).encode("utf-8")
    req = urllib.request.Request(
        f"{API_BASE}/open/v1/list_customised_person",
        data=body,
        headers={"access_token": token, "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_common(
    token, page, page_size, common: Optional[CommonListParams] = None
):
    q: dict = {"page": page, "size": page_size}
    if common is not None:
        if common.common_dp_source is not None:
            q["source"] = common.common_dp_source
        tid = (common.tag_ids or "").strip()
        if tid:
            q["tag_ids"] = tid
    params = urllib.parse.urlencode(q)
    req = urllib.request.Request(
        f"{API_BASE}/open/v1/list_common_dp?{params}",
        headers={"access_token": token, "Content-Type": "application/json"},
        method="GET",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _merge_lists_unique_by_person_id(items):
    """公共列表按人物 id 去重（跨页不应重复，兜底）。"""
    seen = set()
    out = []
    for item in items:
        pid = str(item.get("id", "")).strip()
        key = pid or id(item)
        if key in seen:
            continue
        seen.add(key)
        out.append(item)
    return out


def fetch_merged(
    token,
    source,
    start_page,
    page_size,
    max_pages,
    *,
    common: Optional[CommonListParams] = None,
):
    """
    连续拉取 [start_page, start_page + max_pages - 1]，合并 data.list。
    返回 (merged_list, pages_fetched, page_info_from_first, last_raw_data)
    """
    if max_pages < 1:
        raise ValueError("max_pages 须 >= 1")
    if max_pages > 100:
        raise ValueError("max_pages 过大（>100），请缩小范围")

    all_items = []
    pages_fetched = []
    first_page_info = {}
    last_data = {}

    for i in range(max_pages):
        page = start_page + i
        if source == "customised":
            res = fetch_customised(token, page, page_size)
        else:
            res = fetch_common(token, page, page_size, common)

        if res.get("code") != 0:
            return None, pages_fetched, first_page_info, res

        data = res.get("data", {}) or {}
        last_data = data
        items = data.get("list") or []
        if i == 0:
            first_page_info = dict(data.get("page_info") or {})

        if not items:
            break

        pages_fetched.append(page)
        all_items.extend(items)

        total = (data.get("page_info") or {}).get("total_count")
        if total is not None and len(all_items) >= int(total):
            break

    if source == "common":
        all_items = _merge_lists_unique_by_person_id(all_items)

    return all_items, pages_fetched, first_page_info, last_data


def fetch_until_complete(
    token,
    source,
    page_size: int,
    *,
    max_safety_pages: int = 300,
    common: Optional[CommonListParams] = None,
):
    """
    从第 1 页起连续请求，直到某页 list 为空或已收集条数 >= page_info.total_count。
    公共库在合并前按页累加 person 行；最后对 common 做 id 去重。
    返回 (merged_list, pages_fetched, first_page_info, last_raw_data)；失败时 merged_list 为 None。
    """
    if max_safety_pages < 1 or max_safety_pages > 500:
        raise ValueError("max_safety_pages 须在 1–500")

    all_items: list = []
    pages_fetched: list[int] = []
    first_page_info: dict = {}
    last_data: dict = {}
    total_target: int | None = None
    page = 1

    for _ in range(max_safety_pages):
        if source == "customised":
            res = fetch_customised(token, page, page_size)
        else:
            res = fetch_common(token, page, page_size, common)

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

    if source == "common":
        all_items = _merge_lists_unique_by_person_id(all_items)

    return all_items, pages_fetched, first_page_info, last_data


def build_rows(source, items):
    rows = []
    if source == "customised":
        for item in items:
            width = item.get("width")
            height = item.get("height")
            size = f"{width}x{height}" if width and height else "-"
            rows.append(
                {
                    "source": "customised",
                    "person_id": item.get("id", ""),
                    "name": item.get("name", ""),
                    "figure_type": "-",
                    "size": size,
                    "audio_man_id": item.get("audio_man_id", ""),
                    "note": f"support_4k={item.get('support_4k', '')}",
                    "preview_url": item.get("preview_url", ""),
                }
            )
        return rows

    for item in items:
        tnames = item.get("tag_names") or []
        tag_hint = ""
        if tnames:
            tag_hint = "tags=" + ",".join(str(x) for x in tnames[:6])
            if len(tnames) > 6:
                tag_hint += "…"
        for figure in item.get("figures", []):
            base_note = f"audio_name={item.get('audio_name', '')}"
            note = f"{base_note}; {tag_hint}" if tag_hint else base_note
            rows.append(
                {
                    "source": "common",
                    "person_id": item.get("id", ""),
                    "name": item.get("name", ""),
                    "figure_type": figure.get("type", ""),
                    "size": f"{figure.get('width', '')}x{figure.get('height', '')}",
                    "audio_man_id": item.get("audio_man_id", ""),
                    "note": note,
                    "preview_url": figure.get("preview_video_url", ""),
                }
            )
    return rows


def main():
    parser = argparse.ArgumentParser(description="列出蝉镜视频合成可用数字人形象")
    parser.add_argument(
        "--source",
        choices=["customised", "common"],
        default="customised",
        help="数字人来源：customised 为定制数字人，common 为公共数字人",
    )
    parser.add_argument("--page", type=int, default=1, help="起始页码")
    parser.add_argument(
        "--page-size",
        type=int,
        default=20,
        help="每页数量；公共库选型建议加大（如 50~100）以减少请求次数",
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=1,
        help="从 --page 起连续拉取并合并的页数（>1 时合并多页后再输出，便于跨页对比）",
    )
    parser.add_argument(
        "--fetch-all",
        action="store_true",
        help="从第 1 页起自动翻页直至 total_count 或空页（公共/定制均可用；公共库须先全量再全局匹配选型时推荐）",
    )
    parser.add_argument(
        "--tag-ids",
        default="",
        help="仅 public：list_common_dp 的 tag_ids（逗号分隔）；多 ID 为 AND，须与 list_tag_dict 子标签 id 一致",
    )
    parser.add_argument(
        "--common-dp-source",
        type=int,
        default=None,
        help="仅 public：list_common_dp 的 source 整型筛选（可选，取值以平台为准）",
    )
    parser.add_argument("--json", action="store_true", help="输出完整 JSON")
    args = parser.parse_args()

    token, err = resolve_chanjing_access_token()
    if err:
        print(err, file=sys.stderr)
        sys.exit(1)

    common_params: Optional[CommonListParams] = None
    if args.source == "common":
        common_params = CommonListParams(
            tag_ids=args.tag_ids or "",
            common_dp_source=args.common_dp_source,
        )
    elif (args.tag_ids or "").strip() or args.common_dp_source is not None:
        print(
            "# 提示: --tag-ids / --common-dp-source 仅对 --source common 生效",
            file=sys.stderr,
        )

    if args.fetch_all and args.max_pages > 1:
        print("# 提示: 已指定 --fetch-all，忽略 --max-pages", file=sys.stderr)

    def _json_extra() -> dict:
        if args.source != "common" or common_params is None:
            return {}
        return {
            "list_common_dp_filters": {
                "tag_ids": (common_params.tag_ids or "").strip() or None,
                "source": common_params.common_dp_source,
            }
        }

    if args.fetch_all:
        merged, pages_fetched, first_pi, last_data = fetch_until_complete(
            token, args.source, args.page_size, common=common_params
        )
        if merged is None:
            err = last_data if isinstance(last_data, dict) else {}
            print(err.get("msg", err) or "请求失败", file=sys.stderr)
            sys.exit(1)

        data = {
            "list": merged,
            "page_info": {
                **first_pi,
                "merged_pages": pages_fetched,
                "fetch_all": True,
                "merged_figure_rows": len(build_rows(args.source, merged)),
            },
        }
        if args.json:
            print(
                json.dumps(
                    {
                        "source": args.source,
                        "pages_fetched": pages_fetched,
                        "fetch_all": True,
                        "data": data,
                        **_json_extra(),
                    },
                    ensure_ascii=False,
                    indent=2,
                )
            )
            return

        items = merged
        rows = build_rows(args.source, items)
        total_hint = first_pi.get("total_count", "")
        print(
            f"# source={args.source} fetch-all | 接口 total≈{total_hint} | "
            f"已拉页 {pages_fetched} | 人物行 {len(items)} → 展开形象行 {len(rows)}"
        )
    elif args.max_pages > 1:
        merged, pages_fetched, first_pi, last_data = fetch_merged(
            token,
            args.source,
            args.page,
            args.page_size,
            args.max_pages,
            common=common_params,
        )
        if merged is None:
            err = last_data if isinstance(last_data, dict) else {}
            print(err.get("msg", err) or "请求失败", file=sys.stderr)
            sys.exit(1)

        data = {
            "list": merged,
            "page_info": {
                **first_pi,
                "merged_pages": pages_fetched,
                "merged_figure_rows": len(build_rows(args.source, merged)),
            },
        }
        if args.json:
            print(
                json.dumps(
                    {
                        "source": args.source,
                        "pages_fetched": pages_fetched,
                        "data": data,
                        **_json_extra(),
                    },
                    ensure_ascii=False,
                    indent=2,
                )
            )
            return

        items = merged
        rows = build_rows(args.source, items)
        total_hint = first_pi.get("total_count", "")
        print(
            f"# source={args.source} 接口 total≈{total_hint} | "
            f"已合并页 {pages_fetched} | 本输出人物行 {len(items)} → 展开形象行 {len(rows)}"
        )
    else:
        if args.source == "customised":
            res = fetch_customised(token, args.page, args.page_size)
        else:
            res = fetch_common(token, args.page, args.page_size, common_params)

        if res.get("code") != 0:
            print(res.get("msg", res), file=sys.stderr)
            sys.exit(1)

        data = res.get("data", {})
        if args.json:
            print(
                json.dumps(
                    {"source": args.source, "data": data, **_json_extra()},
                    ensure_ascii=False,
                    indent=2,
                )
            )
            return

        items = data.get("list", [])
        page_info = data.get("page_info", {})
        rows = build_rows(args.source, items)
        print(
            f"# source={args.source} 共 {page_info.get('total_count', len(items))} 个形象 "
            f"(page={args.page}, page_size={args.page_size})"
        )
    print(
        f"{'source':<10}  {'person_id':<36}  {'name':<14}  {'figure_type':<12}  "
        f"{'size':<11}  {'audio_man_id':<36}  {'note':<24}  preview_url"
    )
    print("-" * 220)
    for row in rows:
        print(
            f"{row['source']:<10}  "
            f"{row['person_id']:<36}  "
            f"{row['name']:<14}  "
            f"{row['figure_type']:<12}  "
            f"{row['size']:<11}  "
            f"{row['audio_man_id']:<36}  "
            f"{row['note']:<24}  "
            f"{row['preview_url']}"
        )


if __name__ == "__main__":
    main()
