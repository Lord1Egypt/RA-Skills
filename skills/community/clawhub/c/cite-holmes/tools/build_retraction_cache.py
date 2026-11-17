#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Retraction Watch 本地索引一键构建（v4.3.0——--retraction-cache 的配套工具）。

数据源：Crossref 托管的 Retraction Watch 官方 dump（GitLab 仓库 csv，免费、
每个工作日更新）。构建 {doi_lower: {date, type, reason}} 索引供
verify_refs.py --retraction-cache 离线秒查（--profile medical 大批量前建议）。

用法：
  python3 tools/build_retraction_cache.py --csv retraction_watch.csv --out ~/.cache/rw_index.json
  python3 tools/build_retraction_cache.py --download --out ~/.cache/rw_index.json  # 直拉官方源

索引格式与 v3.2.0 --retraction-cache 完全兼容（含 v4.1.0 通告分档的 type 字段：
Retraction / Partial Retraction / Withdrawal / Expression of Concern / Correction）。"""
import argparse
import csv
import json
import sys
import urllib.request

RWDB_CSV_URL = ("https://gitlab.com/crossref/retraction-watch-data/-/raw/main/"
                "retraction_watch.csv")


def build_index(rows) -> dict:
    """CSV 行 → 索引。原始论文 DOI 为键；撤稿通告 DOI 不入键（查的是被撤论文）。
    同 DOI 多条通告保留信息量最大的一条（type 优先级：撤稿族 > EoC > 更正）。"""
    prio = {"retraction": 5, "retract and republish": 5, "withdrawal": 4,
            "partial retraction": 3, "retract and republish notice": 5,
            "expression of concern": 2}
    out = {}
    for row in rows:
        doi = (row.get("OriginalPaperDOI") or row.get("OriginalPaperdoi") or "").strip().lower()
        if not doi:
            continue
        nature = (row.get("RetractionNature") or "").strip()
        date = (row.get("RetractionDate") or "").strip()
        reason = (row.get("RetractionReason") or "").strip()[:200]
        key = nature.lower()
        entry = {"date": date, "type": nature or "Retraction", "reason": reason}
        old = out.get(doi)
        if old is None or prio.get(key, 1) > prio.get((old.get("type") or "").lower(), 1):
            out[doi] = entry
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", help="已下载的 retraction_watch.csv 路径")
    ap.add_argument("--download", action="store_true", help="直拉官方 GitLab 源（约 60MB）")
    ap.add_argument("--out", required=True, help="索引 JSON 输出路径")
    a = ap.parse_args()
    if a.csv:
        text = open(a.csv, encoding="utf-8", errors="replace").read()
    elif a.download:
        print(f"[download] {RWDB_CSV_URL}")
        with urllib.request.urlopen(urllib.request.Request(
                RWDB_CSV_URL, headers={"User-Agent": "cite-holmes retraction-cache-builder"}),
                timeout=300) as r:
            text = r.read().decode("utf-8", "replace")
    else:
        print("需要 --csv 或 --download")
        return 2
    rows = list(csv.DictReader(text.splitlines()))
    idx = build_index(rows)
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(idx, f, ensure_ascii=False)
    n_ret = sum(1 for v in idx.values()
                if (v.get("type") or "").lower().startswith(("retraction", "withdraw",
                                                             "partial", "retract and")))
    n_eoc = sum(1 for v in idx.values()
                if "concern" in (v.get("type") or "").lower())
    print(f"== 索引构建完成 == 记录 {len(rows):,} → 索引 {len(idx):,} 条 "
          f"（撤稿族 {n_ret:,} / EoC {n_eoc:,}）→ {a.out}")
    print("用法：python3 scripts/verify_refs.py --refs ... --retraction-cache " + a.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
