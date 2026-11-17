#!/usr/bin/env python3
"""
analytics.py - Local owner / category portrait from accumulated cache (BidHunter v2.0, A3).

Reads all qualification outputs in bid_cache/ and produces a local-only portrait:
  - 平台分布 (which platforms yield most 可投)
  - 行业类目分布 (industry category hit counts)
  - 可投率趋势 (per day)
  - 评分分布
No external data, no cloud. The more you run pipeline, the richer the portrait.

Usage:
  python3 analytics.py [--days 30]
"""
import os
import sys
import json
import glob
import argparse
from collections import defaultdict, Counter
from datetime import datetime, timedelta

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "bid_cache")


def load_all(days):
    items = []
    files = sorted(glob.glob(os.path.join(CACHE_DIR, "qual_*.jsonl")))
    cutoff = datetime.now() - timedelta(days=days)
    for f in files:
        dstr = os.path.basename(f).replace("qual_", "").replace(".jsonl", "")
        try:
            dt = datetime.strptime(dstr, "%Y-%m-%d")
        except Exception:
            dt = None
        if dt and dt < cutoff:
            continue
        with open(f, "r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    items.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return items


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=30)
    args = ap.parse_args()

    items = load_all(args.days)
    if not items:
        print("暂无可分析数据。请先运行若干次 pipeline 积累 bid_cache。")
        return

    by_platform = Counter()
    by_industry = Counter()
    by_verdict = Counter()
    by_day = defaultdict(lambda: defaultdict(int))
    scores = []

    for it in items:
        src = it.get("source") or it.get("platform") or "未知"
        by_platform[src] += 1
        ind = it.get("industry") or ""
        if ind:
            by_industry[ind] += 1
        v = it.get("verdict", "needs_review")
        by_verdict[v] += 1
        dstr = ""
        if "id" in it and it.get("source"):
            pass
        sc = it.get("score")
        if isinstance(sc, int):
            scores.append(sc)

    total = len(items)
    invest = by_verdict.get("investable", 0)
    print("=" * 50)
    print(f"📊 本地标讯画像（近 {args.days} 天，共 {total} 条）")
    print("=" * 50)
    print(f"\n【可投率】可投 {invest} / {total} = "
          f"{invest*100//total if total else 0}%")
    print("\n【按平台分布】")
    for k, v in by_platform.most_common():
        print(f"  {k:<14} {v}")
    if by_industry:
        print("\n【按行业类目】")
        for k, v in by_industry.most_common():
            print(f"  {k:<14} {v}")
    print("\n【判定分布】")
    for k in ("investable", "needs_review", "not_investable", "skip"):
        print(f"  {k:<14} {by_verdict.get(k,0)}")
    if scores:
        avg = sum(scores) / len(scores)
        hi = sum(1 for s in scores if s >= 80)
        print(f"\n【评分】均值 {avg:.0f} | 强烈推荐(≥80) {hi} 条")
    print("\n" + "=" * 50)
    print("💡 画像来自本机 bid_cache 累积，越用越准（数据闭环）。")


if __name__ == "__main__":
    main()
