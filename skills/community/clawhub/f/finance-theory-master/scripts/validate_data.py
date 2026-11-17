#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""金融理论大师 —— 数据集校验器。

对 data/ 下四个数据集做自洽性校验：
  theory_index.csv            理论索引
  financial_history_timeline.csv  世界金融史时间线
  policy_toolkit.csv          四类行情下的政策工具箱
  investor_cases.csv          投资案例与判断逻辑

校验维度：文件与字段齐备、必填非空、枚举合法、标识唯一且合规、引用关系自洽、
覆盖度达标、知识正文齐备。

用法：
    python scripts/validate_data.py
退出码：0 通过，1 存在错误。
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

# 允许以 `python scripts/validate_data.py` 直接运行，也允许被测试当模块导入。
if __package__:
    from . import csvio, schema
else:  # pragma: no cover - 仅在脚本直接执行时走到
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import csvio
    import schema

ROOT = schema.ROOT
CSV_PATH = schema.PATH_THEORY
TIMELINE_PATH = schema.PATH_TIMELINE
POLICY_PATH = schema.PATH_POLICY
CASE_PATH = schema.PATH_CASES
REF_DIR = schema.REF_DIR

# 枚举与字段定义统一来自 schema.py
ENUM_MODULE = schema.ENUM_MODULE
ENUM_STRENGTH = schema.ENUM_STRENGTH
ENUM_STATUS = schema.ENUM_STATUS
ENUM_STAGE = schema.ENUM_STAGE
ENUM_HCATEGORY = schema.ENUM_HCATEGORY
ENUM_MARKET_STAGE = schema.ENUM_MARKET_STAGE
ENUM_POLICY_LEVEL = schema.ENUM_POLICY_LEVEL

FIELDS = schema.FIELDS_THEORY
TIMELINE_FIELDS = schema.FIELDS_TIMELINE
POLICY_FIELDS = schema.FIELDS_POLICY
CASE_FIELDS = schema.FIELDS_CASES

REQUIRED_FIELDS = schema.FIELDS_THEORY
OPTIONAL_FIELDS = schema.OPTIONAL_THEORY
EXPECTED_REFS = schema.EXPECTED_REFS

SLUG_RE = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")
YEAR_RE = re.compile(r"^(\d{4}|—)$")

PLACEHOLDER = schema.NOT_APPLICABLE | {""}

# 各数据集的最低记录数，低于此值给出覆盖度警告
MIN_ROWS = {CSV_PATH: 40, TIMELINE_PATH: 80, POLICY_PATH: 30, CASE_PATH: 15}


# ---------------------------------------------------------------------------
# 报告
# ---------------------------------------------------------------------------


@dataclass
class Report:
    """收集校验过程中的错误与警告。

    errors 非空即视为校验失败；warnings 只提示，不影响退出码。
    """

    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)


# ---------------------------------------------------------------------------
# 通用检查
# ---------------------------------------------------------------------------


def load(path: Path, fields: list[str], label: str, rep: Report) -> list[dict[str, str]]:
    """加载数据集并核对字段列是否齐全。

    字段缺失是结构性错误，直接返回空列表——后续检查在字段不全时没有意义。
    """
    try:
        header = csvio.read_header(path)
    except FileNotFoundError:
        rep.error(f"{label}数据集不存在：{path}")
        return []
    except Exception as exc:  # 表头读不出来说明文件损坏
        rep.error(f"{label}无法解析：{exc}")
        return []

    missing = [f for f in fields if f not in header]
    if missing:
        rep.error(f"{label}缺少字段列：{', '.join(missing)}")
        return []

    extra = [f for f in header if f not in fields]
    if extra:
        rep.warn(f"{label}存在未在规范中声明的字段：{', '.join(extra)}")

    try:
        return csvio.read_csv(path)
    except ValueError as exc:
        rep.error(str(exc))
        return []


def check_required(rows: list[dict[str, str]], fields: list[str], label: str,
                   rep: Report, id_field: str, skip: set[str] | None = None) -> None:
    """必填字段不得为空白。

    注意：「—」是显式的「不适用 / 无」，属于合法取值，不计为缺失。
    只有真正的空字符串才算错误。
    """
    skip = skip or set()
    for i, row in enumerate(rows, start=2):  # 第 1 行是表头
        rid = row.get(id_field) or f"<第{i}行>"
        for f in fields:
            if f in skip:
                continue
            if not row.get(f, ""):
                rep.error(f"[{label} {rid}] 必填字段为空：{f}")


def check_enum(rows: list[dict[str, str]], field_name: str, allowed: list[str],
               label: str, rep: Report, id_field: str) -> Counter:
    """校验某字段取值在枚举内，并返回取值分布。"""
    dist: Counter = Counter()
    for row in rows:
        val = row.get(field_name, "")
        dist[val] += 1
        if val not in allowed:
            rid = row.get(id_field, "?")
            rep.error(f"[{label} {rid}] {field_name} 取值非法：{val!r}，允许值 {allowed}")
    return dist


def check_unique(rows: list[dict[str, str]], field_name: str, label: str,
                 rep: Report, require_slug: bool = True) -> None:
    """校验标识唯一；require_slug 时同时校验 slug 格式。"""
    seen: Counter = Counter()
    for row in rows:
        val = row.get(field_name, "")
        seen[val] += 1
        if require_slug and not SLUG_RE.match(val):
            rep.error(f"[{label} {val or '?'}] {field_name} 不符合 slug 规则"
                      f"（小写字母、数字、下划线）")
    for val, n in seen.items():
        if n > 1:
            rep.error(f"[{label}] {field_name} 重复 {n} 次：{val}")


def check_coverage(dist: Counter, allowed: list[str], label: str, rep: Report) -> None:
    """枚举的每个取值都必须有记录，否则说明覆盖不全。"""
    for val in allowed:
        if dist.get(val, 0) == 0:
            rep.error(f"{label}无任何记录：{val}")


def check_size(rows: list[dict[str, str]], path: Path, label: str, rep: Report) -> None:
    n = len(rows)
    if n < MIN_ROWS.get(path, 1):
        rep.warn(f"{label}条目偏少（{n} 条），覆盖度可能不足")


# ---------------------------------------------------------------------------
# 理论索引专有检查
# ---------------------------------------------------------------------------


def check_year(rows: list[dict[str, str]], rep: Report) -> None:
    for row in rows:
        year = row.get("year", "")
        if not YEAR_RE.match(year):
            rep.error(f"[{row.get('theory_id')}] year 格式非法：{year!r}，应为四位年份或 —")
            continue
        if year not in PLACEHOLDER:
            y = int(year)
            if not (1900 <= y <= 2030):
                rep.error(f"[{row.get('theory_id')}] year 超出合理范围：{y}")


def check_relations(rows: list[dict[str, str]], rep: Report) -> None:
    """互补与冲突关系不得自引用，也不得指向同一对象。"""
    for row in rows:
        tid = row.get("theory_id", "?")
        comp = csvio.tokens(row.get("complementary", ""))
        conf = csvio.tokens(row.get("conflicting", ""))

        if tid in comp:
            rep.error(f"[{tid}] complementary 出现自引用")
        if tid in conf:
            rep.error(f"[{tid}] conflicting 出现自引用")

        overlap = comp & conf
        if overlap:
            rep.error(f"[{tid}] 同一对象同时出现在 complementary 与 conflicting 中：{sorted(overlap)}")


def check_refs(rep: Report) -> None:
    """知识正文文件齐备且篇幅不至于太薄。"""
    if not REF_DIR.is_dir():
        rep.error(f"知识文件目录不存在：{REF_DIR}")
        return
    for name in EXPECTED_REFS:
        p = REF_DIR / name
        if not p.exists():
            rep.error(f"缺少知识文件：{name}")
        elif p.stat().st_size < 2000:
            rep.warn(f"知识文件篇幅偏小（{p.stat().st_size} 字节）：{name}")


# ---------------------------------------------------------------------------
# 金融史时间线专有检查
# ---------------------------------------------------------------------------


def check_timeline_order(rows: list[dict[str, str]], rep: Report) -> None:
    """sort_key 必须是整数，且按非递减排列。

    历史数据天然是一年多事，因此允许 sort_key 重复，只要求非递减。
    """
    last_key: int | None = None
    dup_years: Counter = Counter()

    for i, row in enumerate(rows, start=2):
        label = row.get("year") or f"<第{i}行>"
        raw = row.get("sort_key", "")
        try:
            key = int(raw)
        except ValueError:
            rep.error(f"[时间线 {label}] sort_key 不是整数：{raw!r}")
            continue

        if last_key is not None and key < last_key:
            rep.error(f"[时间线 {label}] sort_key 未按非递减排列：{key} < {last_key}")
        last_key = key
        dup_years[raw] += 1

    repeated = {k: v for k, v in dup_years.items() if v > 1}
    if repeated:
        rep.warn(f"有 {len(repeated)} 个年份对应多个事件（属正常，仅提示）：{sorted(repeated)[:6]}")


# ---------------------------------------------------------------------------
# 投资案例专有检查
# ---------------------------------------------------------------------------


def check_case_survivorship(rows: list[dict[str, str]], rep: Report) -> None:
    """幸存者偏差必须显式标注，不能只写「无」以外的空泛表述。"""
    for row in rows:
        if len(row.get("survivorship", "")) < 8:
            rep.error(f"[案例 {row.get('case_id')}] survivorship 过短，"
                      f"必须说明该案例的幸存者偏差或失败风险")


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------


def main() -> int:
    rep = Report()

    # --- 理论索引 ---
    rows = load(CSV_PATH, REQUIRED_FIELDS, "理论索引", rep)
    dist: dict[str, Counter] = {}
    if rows:
        check_required(rows, REQUIRED_FIELDS, "理论", rep, "theory_id", skip=OPTIONAL_FIELDS)
        for fname, allowed in (("module", ENUM_MODULE),
                               ("hypothesis_strength", ENUM_STRENGTH),
                               ("evidence_status", ENUM_STATUS)):
            dist[fname] = check_enum(rows, fname, allowed, "理论", rep, "theory_id")
        check_unique(rows, "theory_id", "理论", rep)
        check_year(rows, rep)
        check_relations(rows, rep)
        for fname, allowed in (("module", ENUM_MODULE),
                               ("hypothesis_strength", ENUM_STRENGTH),
                               ("evidence_status", ENUM_STATUS)):
            check_coverage(dist[fname], allowed, f"板块/等级 {fname}", rep)
        check_size(rows, CSV_PATH, "理论索引", rep)

        names = Counter(r.get("name_cn", "") for r in rows)
        for name, n in names.items():
            if n > 1:
                rep.warn(f"name_cn 重复 {n} 次：{name}")

    check_refs(rep)

    # --- 金融史时间线 ---
    tl_rows = load(TIMELINE_PATH, TIMELINE_FIELDS, "金融史时间线", rep)
    tl_dist: dict[str, Counter] = {}
    if tl_rows:
        check_required(tl_rows, TIMELINE_FIELDS, "时间线", rep, "year")
        tl_dist["stage"] = check_enum(tl_rows, "stage", ENUM_STAGE, "时间线", rep, "year")
        tl_dist["category"] = check_enum(tl_rows, "category", ENUM_HCATEGORY, "时间线", rep, "year")
        check_timeline_order(tl_rows, rep)
        check_coverage(tl_dist["stage"], ENUM_STAGE, "时间线分期", rep)
        check_coverage(tl_dist["category"], ENUM_HCATEGORY, "时间线类别", rep)
        check_size(tl_rows, TIMELINE_PATH, "金融史时间线", rep)

    # --- 政策工具箱 ---
    pol_rows = load(POLICY_PATH, POLICY_FIELDS, "政策工具箱", rep)
    pol_dist: dict[str, Counter] = {}
    if pol_rows:
        check_required(pol_rows, POLICY_FIELDS, "政策", rep, "tool_id")
        check_unique(pol_rows, "tool_id", "政策", rep)
        pol_dist["market_stage"] = check_enum(pol_rows, "market_stage", ENUM_MARKET_STAGE,
                                             "政策", rep, "tool_id")
        pol_dist["level"] = check_enum(pol_rows, "level", ENUM_POLICY_LEVEL, "政策", rep, "tool_id")
        check_coverage(pol_dist["market_stage"], ENUM_MARKET_STAGE, "政策工具箱行情阶段", rep)
        check_coverage(pol_dist["level"], ENUM_POLICY_LEVEL, "政策工具箱政策层级", rep)
        check_size(pol_rows, POLICY_PATH, "政策工具箱", rep)

    # --- 投资案例 ---
    case_rows = load(CASE_PATH, CASE_FIELDS, "投资案例", rep)
    case_dist: Counter = Counter()
    if case_rows:
        check_required(case_rows, CASE_FIELDS, "案例", rep, "case_id")
        check_unique(case_rows, "case_id", "案例", rep)
        case_dist = check_enum(case_rows, "market_stage", ENUM_MARKET_STAGE, "案例", rep, "case_id")
        check_case_survivorship(case_rows, rep)
        check_size(case_rows, CASE_PATH, "投资案例", rep)
        if case_dist.get("危机行情", 0) == 0:
            rep.warn("投资案例中没有危机行情类案例")

    _print_report(rep, rows, dist, tl_rows, tl_dist, pol_rows, pol_dist, case_rows, case_dist)
    return 1 if rep.errors else 0


def _print_dist(title: str, dist: Counter, order: list[str], width: int = 8) -> None:
    print(f"\n{title}")
    for k in order:
        print(f"  {k:<{width}} {dist.get(k, 0):>3} 条")


def _print_report(rep: Report, rows, dist, tl_rows, tl_dist,
                  pol_rows, pol_dist, case_rows, case_dist) -> None:
    print("=" * 64)
    print("金融理论大师 —— 数据集校验报告")
    print("=" * 64)

    if rows:
        print(f"\n【理论索引】记录总数：{len(rows)}")
        _print_dist("按板块：", dist["module"], ENUM_MODULE)
        _print_dist("按假设强度：", dist["hypothesis_strength"], ENUM_STRENGTH, width=6)
        _print_dist("按实证地位：", dist["evidence_status"], ENUM_STATUS, width=6)

    if tl_rows:
        print(f"\n【金融史时间线】记录总数：{len(tl_rows)}")
        _print_dist("按分期：", tl_dist["stage"], ENUM_STAGE, width=16)
        _print_dist("按类别：", tl_dist["category"], ENUM_HCATEGORY)

    if pol_rows:
        print(f"\n【政策工具箱】记录总数：{len(pol_rows)}")
        _print_dist("按行情阶段：", pol_dist["market_stage"], ENUM_MARKET_STAGE)
        _print_dist("按政策层级：", pol_dist["level"], ENUM_POLICY_LEVEL, width=12)

    if case_rows:
        print(f"\n【投资案例】记录总数：{len(case_rows)}")
        _print_dist("按行情阶段：", case_dist, ENUM_MARKET_STAGE)

    if rep.warnings:
        print(f"\n警告 {len(rep.warnings)} 项：")
        for w in rep.warnings:
            print(f"  [WARN] {w}")

    if rep.errors:
        print(f"\n错误 {len(rep.errors)} 项：")
        for e in rep.errors:
            print(f"  [ERROR] {e}")
        print("\n结果：失败")
        return

    print("\n结果：通过")


if __name__ == "__main__":
    sys.exit(main())
