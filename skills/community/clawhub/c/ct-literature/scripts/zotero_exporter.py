#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
zotero_exporter.py — Zotero / 文献管理软件集成（升级项 F）.

将 .merged.json 导出为 Zotero 可导入的格式：
  - zotero.csv   标准 Zotero CSV 列（作者用 "||" 分隔，标签用 "||" 分隔，
                  与 Zotero 自身导出格式一致，可往返导入）
  - zotero.ris   通用 RIS 书目交换格式（Zotero 原生支持，最稳妥的导入路径）

纯本地、零联网、仅依赖标准库。可被 ct_literature.py 流水线直接调用，
也可作为独立 CLI 运行：

  python zotero_exporter.py --in .merged.json --out-dir ./out

说明：CSV 为便捷格式（列名对齐 Zotero 导入约定）；RIS 为跨平台书目交换的
权威格式，建议优先用 RIS 导入 Zotero。
"""
import argparse
import csv
import io
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# reuse format_citations' RIS serializer (DRY, same schema)
from format_citations import to_ris, _authors_list  # noqa: E402


def _split_name(name):
    name = (name or "").strip()
    if not name:
        return "", ""
    if "," in name:
        last, first = name.split(",", 1)
        return last.strip(), first.strip()
    if re.search(r"[\u4e00-\u9fff]", name):
        return name, ""
    parts = name.split()
    if len(parts) == 1:
        return parts[0], ""
    return parts[-1], " ".join(parts[:-1])


def _zotero_authors(work):
    """Return 'Last, First || Last2, First2' string (Zotero CSV convention)."""
    out = []
    for n in _authors_list(work):
        last, first = _split_name(n)
        out.append(("%s, %s" % (last, first)).strip(", "))
    return " || ".join(out)


def _pages(work):
    p = work.get("page") or ""
    return str(p).strip().replace(" ", "")


def _tags(work):
    tags = []
    for fld in ("mesh", "concepts", "keywords"):
        v = work.get(fld)
        if isinstance(v, list):
            tags.extend(str(x).strip() for x in v if x)
        elif isinstance(v, str) and v:
            tags.append(v.strip())
    # de-dup preserve order
    seen = set()
    uniq = []
    for t in tags:
        if t.lower() not in seen:
            seen.add(t.lower())
            uniq.append(t)
    return " || ".join(uniq[:12])


def to_zotero_csv(works):
    """Return CSV text with Zotero-compatible columns."""
    buf = io.StringIO()
    # Zotero CSV import recognizes these headers
    fieldnames = ["Item Type", "Title", "Date", "Publication Title",
                  "Author", "DOI", "URL", "Abstract Note", "Tags"]
    w = csv.DictWriter(buf, fieldnames=fieldnames)
    w.writeheader()
    for wk in works:
        w.writerow({
            "Item Type": "journalArticle",
            "Title": wk.get("title") or "",
            "Date": wk.get("year") or "",
            "Publication Title": wk.get("publication") or "",
            "Author": _zotero_authors(wk),
            "DOI": wk.get("doi") or "",
            "URL": wk.get("url") or (("https://doi.org/" + wk["doi"]) if wk.get("doi") else ""),
            "Abstract Note": (wk.get("abstract_snippet") or "")[:2000],
            "Tags": _tags(wk),
        })
    return buf.getvalue()


def export_zotero(merged, out_dir=".", lang="auto"):
    """Write zotero.csv + zotero.ris. Returns dict {csv, ris, count}."""
    works = [w for w in (merged.get("works") or []) if isinstance(w, dict)
             and w.get("title")]
    os.makedirs(out_dir, exist_ok=True)
    csv_path = os.path.join(out_dir, "zotero.csv")
    ris_path = os.path.join(out_dir, "zotero.ris")

    with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
        f.write(to_zotero_csv(works))
    with open(ris_path, "w", encoding="utf-8") as f:
        f.write(to_ris(works))

    return {"csv": csv_path, "ris": ris_path, "count": len(works)}


def main():
    ap = argparse.ArgumentParser(description="Export .merged.json to Zotero CSV/RIS.")
    ap.add_argument("--in", default=".merged.json", dest="inp", help=".merged.json path")
    ap.add_argument("--out-dir", default=".", help="output directory")
    ap.add_argument("--lang", default="auto", choices=["auto", "zh", "en"])
    args = ap.parse_args()
    data = json.load(open(args.inp, encoding="utf-8"))
    res = export_zotero(data, out_dir=args.out_dir, lang=args.lang)
    print("[OK] zotero entries=%d" % res["count"])
    print("     csv -> %s" % res["csv"])
    print("     ris -> %s" % res["ris"])


if __name__ == "__main__":
    main()
