#!/usr/bin/env python3
"""
公共素材「标签字典」：GET /open/v1/common/tag_list。

返回按业务大类分组的启用标签；大类含 name、business_type、weight、update_time、tag_child_count，
每条大类下 tag_list 为子标签明细（id/name/parent_id/level/weight 等）。子标签的 id 用于
list_common_dp 的 tag_ids 查询参数（多 id 为 AND）。

用法:
  list_tag_dict [--business-type 1] [--business-type 2 ...] [--json]
  list_tag_dict --business-type-csv "1,2"
不传 business_type 时接口返回全部业务大类（以官方为准）。
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


def fetch_tag_list(token: str, business_type_csv: str | None) -> dict:
    q: list[tuple[str, str]] = []
    if business_type_csv and business_type_csv.strip():
        q.append(("business_type", business_type_csv.strip()))
    qs = urllib.parse.urlencode(q) if q else ""
    url = f"{API_BASE}/open/v1/common/tag_list"
    if qs:
        url = f"{url}?{qs}"
    req = urllib.request.Request(
        url,
        headers={"access_token": token, "Content-Type": "application/json"},
        method="GET",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _sort_key_weight(item: dict) -> tuple:
    w = item.get("weight")
    try:
        wi = int(w) if w is not None else 0
    except (TypeError, ValueError):
        wi = 0
    return (-wi, str(item.get("name", "")))


def print_human(data_obj: dict) -> None:
    cats = data_obj.get("list") or []
    cats = sorted(cats, key=_sort_key_weight)
    print(
        f"# 业务大类 {len(cats)} 组（已按 weight 降序）；"
        f"子标签 id 可用于 list_figures --tag-ids（多 id 为 AND）"
    )
    for cat in cats:
        cid = cat.get("id", "")
        cname = cat.get("name", "")
        bt = cat.get("business_type", "")
        cw = cat.get("weight", "")
        ut = cat.get("update_time", "")
        cnt = cat.get("tag_child_count", "")
        print(
            f"\n## [{cid}] {cname}  | business_type={bt}  weight={cw}  "
            f"tag_child_count={cnt}  update_time={ut}"
        )
        tags = cat.get("tag_list") or []
        tags = sorted(tags, key=_sort_key_weight)
        print(
            f"{'tag_id':<8}  {'lvl':<4}  {'parent':<8}  {'w':<6}  "
            f"{'status':<6}  name"
        )
        print("-" * 72)
        for t in tags:
            tid = t.get("id", "")
            nm = t.get("name", "")
            pid = t.get("parent_id", "")
            lv = t.get("level", "")
            tw = t.get("weight", "")
            st = t.get("status", "")
            tu = t.get("update_time", "")
            try:
                li = int(lv)
            except (TypeError, ValueError):
                li = 1
            indent = "  " * max(0, li - 1)
            print(
                f"{tid!s:<8}  {str(lv):<4}  {str(pid):<8}  {str(tw):<6}  "
                f"{str(st):<6}  {indent}{nm}  ({tu})"
            )


def main() -> None:
    parser = argparse.ArgumentParser(description="蝉镜公共素材标签字典（大类 + 子标签）")
    parser.add_argument(
        "--business-type",
        action="append",
        dest="business_types",
        default=None,
        help="业务类型，可重复传入；多个值将拼为 CSV 传给接口（并集）。常见 1=数字人、2=声音",
    )
    parser.add_argument(
        "--business-type-csv",
        default="",
        help="等价于单个 CSV 参数 business_type=1,2（与重复 --business-type 二选一即可）",
    )
    parser.add_argument("--json", action="store_true", help="输出完整 API JSON")
    args = parser.parse_args()

    token, err = resolve_chanjing_access_token()
    if err:
        print(err, file=sys.stderr)
        sys.exit(1)

    csv = (args.business_type_csv or "").strip()
    if args.business_types:
        parts = [str(x).strip() for x in args.business_types if str(x).strip()]
        if csv:
            csv = csv + "," + ",".join(parts)
        else:
            csv = ",".join(parts)
    business_type_param = csv if csv else None

    res = fetch_tag_list(token, business_type_param)
    if res.get("code") != 0:
        print(res.get("msg", res), file=sys.stderr)
        sys.exit(1)

    data = res.get("data") or {}
    if args.json:
        print(
            json.dumps(
                {
                    "endpoint": "GET /open/v1/common/tag_list",
                    "business_type_query": business_type_param,
                    "data": data,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return

    print_human(data)


if __name__ == "__main__":
    main()
