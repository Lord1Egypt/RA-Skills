#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""竞品/站点快照比对。

抓取目标字段，与历史快照 diff，输出变化。

用法:
  python snapshot.py <url> --field "price:.price" --field "title:h1" \
    --store state/productA.json --out diff.txt [--js] [--wait sel]
"""
import argparse
import json
import os
import sys

# 复用 web-fetch 的 scrape（同目录或回退到 skills/web-fetch/scripts）
try:
    from scrape import fetch, extract
except ImportError:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__),
                                    "..", "..", "web-fetch", "scripts"))
    from scrape import fetch, extract


def build_records(url, fields, use_js, wait, timeout):
    html = fetch(url, use_js, wait, timeout)
    # 构造临时 args 对象给 extract（仅 field 模式）
    class A:
        pass
    a = A()
    a.select = None
    a.attr = None
    a.text = False
    a.field = fields
    a.js = use_js
    a.wait = wait
    a.timeout = timeout
    a.out = None
    a.no_robots = False
    a.url = url
    return extract(html, a)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--field", action="append", default=[], help="字段:选择器")
    ap.add_argument("--store", help="快照存储 json")
    ap.add_argument("--out", help="diff 输出文件")
    ap.add_argument("--js", action="store_true")
    ap.add_argument("--wait", default=None)
    ap.add_argument("--timeout", type=int, default=20)
    args = ap.parse_args()

    try:
        recs = build_records(args.url, args.field, args.js, args.wait, args.timeout)
    except Exception as e:
        print(f"❌ 抓取失败: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(1)

    # 取第一条记录作为当前快照
    current = recs[0] if recs else {}

    diff_lines = []
    if args.store and os.path.exists(args.store):
        prev = json.load(open(args.store, encoding="utf-8"))
        for k in set(list(current) + list(prev)):
            ov, nv = prev.get(k), current.get(k)
            if ov != nv:
                diff_lines.append(f"[{k}] 旧: {ov} -> 新: {nv}")
        if not diff_lines:
            diff_lines.append("✅ 无变化")
    else:
        diff_lines.append("📌 已建立基线快照（首次运行）")

    report = "\n".join(diff_lines)
    print(report)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(report)
    if args.store:
        os.makedirs(os.path.dirname(args.store) or ".", exist_ok=True)
        json.dump(current, open(args.store, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
