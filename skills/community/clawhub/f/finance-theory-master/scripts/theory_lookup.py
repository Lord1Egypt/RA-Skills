#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""金融理论大师 —— 理论索引查询工具。

从 data/theory_index.csv 检索理论，输出对比表。供 SKILL.md 工作流程
Step 2 使用：先用本脚本定位相关理论，再按需加载 references/ 下的正文。

用法示例：
    python scripts/theory_lookup.py --keyword 波动率
    python scripts/theory_lookup.py --module 资产定价
    python scripts/theory_lookup.py --status 有争议
    python scripts/theory_lookup.py --strength 极强
    python scripts/theory_lookup.py --id capm
    python scripts/theory_lookup.py --list
    python scripts/theory_lookup.py --keyword 因子 --format json

退出码：
    0  正常（至少命中 1 条）
    1  参数错误或数据集不可用
    2  检索命中 0 条（显式失败，不静默返回空表）
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

# 允许以 `python scripts/theory_lookup.py` 直接运行，也允许被测试当模块导入。
if __package__:
    from . import csvio, schema
else:  # pragma: no cover - 仅在脚本直接执行时走到
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import csvio
    import schema

ROOT = schema.ROOT
CSV_PATH = schema.PATH_THEORY

ENUM_MODULE = schema.ENUM_MODULE
ENUM_STRENGTH = schema.ENUM_STRENGTH
ENUM_STATUS = schema.ENUM_STATUS

# 关键词检索覆盖的字段（按相关性排序）与简要表列，均来自 schema
SEARCH_FIELDS = schema.SEARCH_FIELDS
BRIEF_COLS = schema.BRIEF_COLS


class LookupError(Exception):
    """查询失败。命中为 0 时必须抛错，不允许静默返回空结果。"""


def load(path: Path = CSV_PATH) -> list[dict[str, str]]:
    """加载理论索引。文件缺失或为空时抛 LookupError。"""
    try:
        return csvio.read_csv(path)
    except (FileNotFoundError, ValueError) as exc:
        raise LookupError(f"{exc}。请先运行 scripts/gen_data.py 生成。") from exc


def search_keyword(rows: list[dict[str, str]], keyword: str) -> list[dict[str, str]]:
    """在多个字段中做子串匹配（大小写不敏感），按命中字段权重与命中次数排序。"""
    kw_raw = keyword.strip()
    if not kw_raw:
        raise LookupError("关键词为空")
    kw = kw_raw.casefold()

    scored: list[tuple[float, dict[str, str]]] = []
    for row in rows:
        score = 0.0
        hits = 0
        for rank, field in enumerate(SEARCH_FIELDS):
            val = row.get(field, "").casefold()
            if kw in val:
                hits += val.count(kw)
                score += (len(SEARCH_FIELDS) - rank) * 10
        if score > 0:
            score += hits
            scored.append((score, row))

    if not scored:
        raise LookupError(f"关键词「{kw_raw}」未命中任何理论。请换用更通用的词，或用 --list 查看全部条目。")

    scored.sort(key=lambda t: (-t[0], t[1].get("theory_id", "")))
    return [r for _, r in scored]


def filter_field(rows: list[dict[str, str]], field: str, value: str) -> list[dict[str, str]]:
    matched = [r for r in rows if r.get(field, "") == value]
    if not matched:
        allowed = {
            "module": ENUM_MODULE,
            "hypothesis_strength": ENUM_STRENGTH,
            "evidence_status": ENUM_STATUS,
        }.get(field, [])
        hint = f"，可选值：{allowed}" if allowed else ""
        raise LookupError(f"{field} = {value!r} 无任何命中{hint}")
    return matched


def render_brief(rows: list[dict[str, str]]) -> str:
    widths = {c: max(len(c), *(len(_display(r, c)) for r in rows)) for c in BRIEF_COLS}
    lines = ["| " + " | ".join(c.ljust(widths[c]) for c in BRIEF_COLS) + " |"]
    lines.append("|" + "|".join("-" * (widths[c] + 2) for c in BRIEF_COLS) + "|")
    for r in rows:
        lines.append("| " + " | ".join(_display(r, c).ljust(widths[c]) for c in BRIEF_COLS) + " |")
    return "\n".join(lines)


def _display(row: dict[str, str], col: str) -> str:
    v = row.get(col, "")
    return v if v else "—"


def render_detail(row: dict[str, str]) -> str:
    lines = []
    for key, label in schema.DETAIL_LABELS:
        val = row.get(key, "")
        if val and val not in schema.NOT_APPLICABLE:
            lines.append(f"**{label}**：{val}")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="金融理论索引查询",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--keyword", "-k", help="关键词检索（覆盖名称、命题、局限、适用场景等字段）")
    ap.add_argument("--module", "-m", choices=ENUM_MODULE, help="按板块筛选")
    ap.add_argument("--status", "-s", choices=ENUM_STATUS, help="按实证地位筛选")
    ap.add_argument("--strength", "-t", choices=ENUM_STRENGTH, help="按假设强度筛选")
    ap.add_argument("--id", dest="tid", help="按 theory_id 精确查询，输出完整字段")
    ap.add_argument("--list", action="store_true", help="列出全部理论标识与名称")
    ap.add_argument("--format", "-f", choices=["md", "json", "csv"], default="md", help="输出格式")
    ap.add_argument("--data", default=str(CSV_PATH), help="数据集路径")
    args = ap.parse_args()

    try:
        rows = load(Path(args.data))

        if args.list:
            result = [{"theory_id": r["theory_id"], "name_cn": r["name_cn"], "module": r["module"]} for r in rows]
            if args.format == "json":
                print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                print(f"共 {len(result)} 条理论\n")
                for r in result:
                    print(f"  {r['theory_id']:<22} {r['module']:<6} {r['name_cn']}")
            return 0

        if args.tid:
            matched = [r for r in rows if r.get("theory_id") == args.tid]
            if not matched:
                raise LookupError(f"未找到 theory_id = {args.tid!r}。用 --list 查看可用标识。")
            if args.format == "json":
                print(json.dumps(matched[0], ensure_ascii=False, indent=2))
            else:
                print(render_detail(matched[0]))
            return 0

        result = rows
        applied = []
        if args.keyword:
            result = search_keyword(result, args.keyword)
            applied.append(f"关键词「{args.keyword}」")
        if args.module:
            result = [r for r in result if r["module"] == args.module]
            applied.append(f"板块「{args.module}」")
        if args.status:
            result = [r for r in result if r["evidence_status"] == args.status]
            applied.append(f"实证地位「{args.status}」")
        if args.strength:
            result = [r for r in result if r["hypothesis_strength"] == args.strength]
            applied.append(f"假设强度「{args.strength}」")

        if not applied:
            ap.error("请至少指定 --keyword / --module / --status / --strength / --id / --list 之一")

        if not result:
            raise LookupError(
                f"组合条件（{' + '.join(applied)}）命中 0 条。请放宽条件后重试。"
            )

        if args.format == "json":
            print(json.dumps(result, ensure_ascii=False, indent=2))
        elif args.format == "csv":
            writer = csv.DictWriter(sys.stdout, fieldnames=list(result[0].keys()), lineterminator="\n")
            writer.writeheader()
            writer.writerows(result)
        else:
            print(f"命中 {len(result)} 条（{' + '.join(applied)}）\n")
            print(render_brief(result))
            print("\n详细字段用 --id <theory_id> 查询；知识正文见 references/ 对应文件。")
        return 0

    except LookupError as exc:
        print(f"[查询失败] {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
