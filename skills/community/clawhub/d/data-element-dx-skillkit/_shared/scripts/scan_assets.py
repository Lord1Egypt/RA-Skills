"""
数据资产扫描脚手架（融合 duckdb / pandas / csv-wrangler 能力）
================================================================

用途：dx-data-baseline 的"脚本化盘点"。先跑机器画像，再用问卷核对业务语义。

设计原则（来自 csv-data-wrangler 决策树）：
  < 1GB   → pandas
  1-10GB  → Polars 或 DuckDB
  > 10GB  → Spark / 分布式

本脚本为**零依赖骨架**（仅标准库），可枚举目录/文件/表头；
接入 DuckDB/Polars 后可扩展为库表结构、行数、空值率、唯一性画像。

用法：
  python scan_assets.py <目录>                 # 枚举文件并输出清单
  python scan_assets.py <目录> --out assets.csv # 导出 CSV
"""

import argparse
import csv
import os
import sys
from pathlib import Path
from typing import Dict, List

# 视为"数据文件"的扩展名（离线文件也是数据源，必须纳入盘点）
DATA_EXT = {".csv", ".tsv", ".xlsx", ".xls", ".parquet", ".json", ".jsonl", ".txt", ".db", ".sqlite", ".duckdb"}


def sniff_header(path: Path, max_bytes: int = 4096) -> str:
    """尝试读取文件表头（仅 CSV/TSV，其他返回空）。"""
    if path.suffix.lower() not in {".csv", ".tsv"}:
        return ""
    try:
        # utf-8-sig：兼容带 BOM 的 CSV（Windows 常见），避免首列名被 BOM 污染
        with path.open("r", encoding="utf-8-sig", errors="ignore") as f:
            first = f.readline(max_bytes).strip()
        return first[:200]
    except Exception:
        return ""


def scan(root: str) -> List[Dict]:
    rows: List[Dict] = []
    base = Path(root)
    if not base.exists():
        print(f"[ERROR] 目录不存在：{root}", file=sys.stderr)
        return rows

    for p in base.rglob("*"):
        if not p.is_file():
            continue
        if p.suffix.lower() not in DATA_EXT:
            continue
        try:
            st = p.stat()
        except OSError:
            continue
        rows.append({
            "路径": str(p.relative_to(base)),
            "文件": p.name,
            "类型": p.suffix.lower().lstrip("."),
            "大小MB": round(st.st_size / 1024 / 1024, 3),
            "修改时间": __import__("datetime").datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M"),
            "表头预览": sniff_header(p),
            # 以下字段需人工/问卷补全（脚本无法推断语义）
            "业务域": "",
            "字段业务含义": "",
            "主数据标识": "",
            "权威源": "",
            "敏感级别": "",
            "业务负责人": "",
            "技术负责人": "",
            "质量问题": "",
            "在用状态": "",
        })
    return rows


def size_hint(total_mb: float) -> str:
    if total_mb < 1024:
        return "总量 <1GB → pandas 足够"
    if total_mb < 10240:
        return "总量 1-10GB → 建议 Polars / DuckDB"
    return "总量 >10GB → 建议 Spark / 分布式"


def main():
    ap = argparse.ArgumentParser(description="数据资产扫描脚手架")
    ap.add_argument("root", help="待扫描目录")
    ap.add_argument("--out", default="", help="输出 CSV 路径（留空则打印）")
    args = ap.parse_args()

    rows = scan(args.root)
    total_mb = sum(r["大小MB"] for r in rows)

    print(f"[扫描完成] 命中 {len(rows)} 个数据文件，合计 {round(total_mb, 2)} MB")
    print(f"[工具建议] {size_hint(total_mb)}")
    print("[下一步] 用问卷向业务侧核对语义字段（业务域/含义/权威源/负责人）")

    if args.out and rows:
        with open(args.out, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
        print(f"[输出] {args.out}")


if __name__ == "__main__":
    main()
