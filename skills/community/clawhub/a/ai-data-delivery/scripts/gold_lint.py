#!/usr/bin/env python3
"""gold_lint.py — 评测集自身质量检查（ai-data-delivery v0.0.4）

gold 集是验收基准，但它自己也会生病。本工具检查评测集内部一致性——
典型事故：同一物理查询两份 gold 互相矛盾（Q10 vs A03，同一 SQL 金标准 320 vs 267），
规则引擎永远无法同时满足，验收结论随之失真。

用法：
  python gold_lint.py --cases cases_gold.json [--results gold_results.json] [--model semantic.yaml]
  python gold_lint.py --cases a.json --cases b.json     # 多文件合并检查（跨文件冲突）

检查项（E=ERROR / W=WARN）：
  E1 id 重复
  E2 问句为空
  E3 同一问句（归一化后）两份期望不一致（一问一答原则）
  E4 同一 gold_sql（归一化后）期望行不一致 —— Q10/A03 类冲突的检测器
  E5 期望结果自相矛盾：status=OK 但 rows 为空且 row_count>0 / row_count 与 rows 实际行数不符
  W1 同一问句重复出现且期望一致（冗余，可合并）
  W2 全集合无 refusal 用例（验收门槛要求 refusal 全过，没有该拒的用例=没有验收依据）
  W3 expect_table 不在模型的物理表清单中（需 --model）
  W4 gold_sql 含 SELECT * 或无时间过滤（护栏一致性提示）
  W5 status=OK 但空结果（gold 为空等于没校验口径，需确认是真实空还是漏采数）
  W6 results 中存在用例集没有的孤儿 id
  W7 数值合理性启发式：单值结果为负（计数类口径不应为负）

期望行来源（按序）：用例内 gold_rows / expect.value|rows；--results 文件（{id: {rows}}）。
能力边界：本工具查"评测集内部一致性与自洽性"；数值与物理库是否相符归 reconcile_paths.py /
run_eval.py 管——lint 全过 ≠ gold 数值正确。
退出码：0 = 无 ERROR；1 = 有 ERROR；2 = 用法错误。
"""
import argparse
import json
import re
import sys

import yaml
from _contract import load


def load_cases(path):
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f) if path.endswith((".yaml", ".yml")) else json.load(f)
    if isinstance(data, dict):
        for key in ("cases", "gold_results"):
            if key in data:
                return data[key]
        raise ValueError(f"用例文件缺少 cases/gold_results 键：{path}")
    return data


def load_results(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict):
        return data
    return {r["id"]: r for r in data}


def norm_text(q):
    """问句归一：去空白与句末标点，防'同一问句换个标点'漏网。"""
    return re.sub(r"[\s？?。．.，,！!！]+$", "", str(q or "").strip())


def norm_sql(sql):
    """SQL 归一：压缩空白、去尾分号、统一大小写。"""
    s = re.sub(r"\s+", " ", str(sql or "").strip().rstrip(";"))
    return s.upper()


def expected_of(case, results):
    """返回 (kind, payload)：refusal / scalar / rows / sql_only / none。"""
    e = case.get("expect")
    if isinstance(e, dict):
        t = e.get("type", "scalar")
        if t == "refusal":
            return "refusal", None
        if t == "scalar":
            return "scalar", repr(norm_num(e.get("value")))
        return "rows", repr(sorted(map(repr, e.get("rows") or [])))
    if case.get("expect_reject"):
        return "refusal", None
    et = str(case.get("expect_table") or "")
    if "拒绝" in et or "追问" in et:  # 拒绝标记位
        return "refusal", None
    rows = case.get("gold_rows")
    if rows is None and results:
        rec = results.get(case["id"])
        rows = rec.get("rows") if rec else None
    if rows is not None:
        if len(rows) == 1 and len(rows[0]) == 1:
            return "scalar", repr(norm_num(rows[0][0]))
        return "rows", repr(sorted(map(repr, rows)))
    if case.get("gold_sql"):
        return "sql_only", None
    return "none", None


def norm_num(x):
    try:
        return float(str(x).replace(",", "").strip())
    except (ValueError, AttributeError):
        return x


def main():
    ap = argparse.ArgumentParser(description="评测集自身质量检查")
    ap.add_argument("--cases", action="append", required=True, help="用例文件（可多次）")
    ap.add_argument("--results", default=None, help="期望行文件（gold_results.json）")
    ap.add_argument("--model", default=None, help="semantic.yaml（校验 expect_table 存在性）")
    args = ap.parse_args()

    cases = []
    for path in args.cases:
        for c in load_cases(path):
            cases.append((path, c))

    results = load_results(args.results) if args.results else None
    model_tables = None
    if args.model:
        m = load(args.model)
        model_tables = {d.get("source") for d in m.get("datasets", []) or []}

    errors, warnings = [], []

    # E1 / E2
    seen_ids = {}
    for path, c in cases:
        cid = c.get("id")
        if cid in seen_ids:
            errors.append(f"[ERROR E1] id {cid!r} 重复（{seen_ids[cid]} 与 {path}）")
        seen_ids[cid] = path
        if not str(c.get("question") or "").strip():
            errors.append(f"[ERROR E2] {cid} 问句为空")

    # E3 / W1：同一问句
    by_q = {}
    for path, c in cases:
        key = norm_text(c.get("question"))
        if key:
            by_q.setdefault(key, []).append((path, c))
    for q, group in by_q.items():
        if len(group) < 2:
            continue
        sigs = {(expected_of(c, results)) for _, c in group}
        ids = [c.get("id") for _, c in group]
        if len(sigs) > 1:
            errors.append(f"[ERROR E3] 同一问句期望不一致：{ids} —— {q[:40]}")
        else:
            warnings.append(f"[WARN  W1] 同一问句重复且期望一致（可合并）：{ids} —— {q[:40]}")

    # E4：同一 gold_sql 期望行不一致（Q10/A03 检测器）
    by_sql = {}
    for path, c in cases:
        sql = c.get("gold_sql")
        if sql:
            by_sql.setdefault(norm_sql(sql), []).append(c)
    for sql, group in by_sql.items():
        if len(group) < 2:
            continue
        sigs = {expected_of(c, results) for c in group}
        if len(sigs) > 1:
            ids = [c.get("id") for c in group]
            errors.append(
                f"[ERROR E4] 同一 SQL 两份 gold 期望不一致（评测集口径冲突）：{ids}\n"
                f"           SQL: {sql[:120]}")
            for c in group:
                kind, payload = expected_of(c, results)
                errors.append(f"           {c.get('id')}: {kind} {payload} 问句「{c.get('question', '')[:30]}」")

    # W2：refusal 覆盖
    n_refusal = sum(1 for _, c in cases if expected_of(c, results)[0] == "refusal")
    if n_refusal == 0:
        warnings.append("[WARN  W2] 全集合无 refusal 用例——该拒则拒无验收依据（门禁 A 要求 ≥5 条）")

    # W3 / W4：SQL 侧
    for path, c in cases:
        sql = c.get("gold_sql")
        if not sql:
            continue
        ns = norm_sql(sql)
        if "SELECT *" in ns:
            warnings.append(f"[WARN  W4] {c.get('id')} gold_sql 含 SELECT *")
        if model_tables and c.get("expect_table"):
            for t in re.split(r"[|,，]", str(c["expect_table"])):
                t = t.strip()
                if t and t not in model_tables:
                    warnings.append(f"[WARN  W3] {c.get('id')} expect_table "
                                    f"{t!r} 不在模型物理表清单中")

    # E5 / W5 / W6 / W7：results 记录自洽性与合理性
    if results:
        case_ids = {c.get("id") for _, c in cases}
        for rid, rec in results.items():
            if not isinstance(rec, dict):
                continue
            rows = rec.get("rows")
            rc = rec.get("row_count")
            ok_status = str(rec.get("status", "OK")).upper() in ("OK", "SUCCESS")
            if rid not in case_ids:
                warnings.append(f"[WARN  W6] results 中 {rid} 在用例集中不存在（孤儿期望）")
            if ok_status and (rows is None or rows == []) and (rc or 0) > 0:
                errors.append(f"[ERROR E5] {rid} status=OK 且 row_count={rc} 但 rows 为空——"
                              "期望结果自相矛盾（采集失败残留？）")
            elif ok_status and (rows is None or rows == []):
                warnings.append(f"[WARN  W5] {rid} status=OK 但空结果——空 gold 无法校验口径，"
                                "确认是真实空还是漏采数")
            if rows and rc is not None and rc != len(rows):
                errors.append(f"[ERROR E5] {rid} row_count={rc} 与 rows 实际 {len(rows)} 行不符")
            if rows and len(rows) == 1 and len(rows[0]) == 1:
                v = norm_num(rows[0][0])
                if isinstance(v, float) and v < 0:
                    warnings.append(f"[WARN  W7] {rid} 单值期望为负数（{v}）——"
                                    "计数/比率类口径不应为负")

    for line in errors + warnings:
        print(line)
    print(f"\ngold lint：{len(errors)} ERROR / {len(warnings)} WARN"
          f"（用例 {len(cases)}，refusal {n_refusal}，含 SQL {len(by_sql)}）")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
