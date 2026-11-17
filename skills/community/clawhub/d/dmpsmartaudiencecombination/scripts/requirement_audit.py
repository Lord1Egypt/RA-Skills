#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""requirement_audit.py

需求不遗漏审计（通用版·零依赖）：
- 把用户在schema中明确表达的要素（coverage_matrix的每个维度值）做“可执行信号→可验证产物”的对账
- 不做业务决策，不生成标签，不改写MUST

输出：audit.json
- per_dimension: 每个维度的值列表、是否在queries中出现、是否在候选tagName中出现
- missing: 缺失项汇总（missing_in_queries / missing_in_candidates）

注意：该脚本只基于字符串子串命中判断，字段含义以系统为准。
"""

import argparse
import json
import re
from pathlib import Path
from typing import Any, Dict, List


def _norm(s: str) -> str:
    s = str(s).strip().lower()
    s = re.sub(r"\s+", "", s)
    return s


def _load_json(path: str) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _hit(texts: List[str], token: str) -> bool:
    tn = _norm(token)
    if not tn:
        return False
    for t in texts:
        if tn in _norm(t):
            return True
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--schema", required=True)
    ap.add_argument("--coverage", required=True)
    ap.add_argument("--queries", required=True)
    ap.add_argument("--candidates", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    cov = _load_json(args.coverage)
    matrix = cov.get("coverage_matrix") if isinstance(cov, dict) else {}
    if not isinstance(matrix, dict):
        matrix = {}

    q = _load_json(args.queries)
    queries = q.get("queries") if isinstance(q, dict) else []
    if not isinstance(queries, list):
        queries = []

    cands = _load_json(args.candidates)
    cand_names = []
    if isinstance(cands, list):
        for it in cands:
            if isinstance(it, dict):
                nm = it.get("tagName")
                if isinstance(nm, str) and nm.strip():
                    cand_names.append(nm)

    report: Dict[str, Any] = {
        "ok": True,
        "per_dimension": {},
        "missing": {
            "missing_in_queries": [],
            "missing_in_candidates": [],
        },
        "meta": {
            "note": "审计仅基于子串命中；缺失不一定是召回失败，也可能是标签池能力缺口或命名口径差异。",
        },
    }

    for dim, vals in matrix.items():
        if not isinstance(vals, list) or not vals:
            continue
        # 跳过纯raw_text维度：它通常很长，不适合做硬门禁
        if str(dim) == "_raw_text":
            continue

        dim_items = []
        for v in vals:
            if not isinstance(v, str) or not v.strip():
                continue
            in_q = _hit(queries, v)
            in_c = _hit(cand_names, v)
            dim_items.append({
                "value": v,
                "in_queries": in_q,
                "in_candidates": in_c,
            })
            if not in_q:
                report["missing"]["missing_in_queries"].append({"dimension": dim, "value": v})
            if not in_c:
                report["missing"]["missing_in_candidates"].append({"dimension": dim, "value": v})

        if dim_items:
            report["per_dimension"][dim] = dim_items

    report["missing"]["missing_in_queries_count"] = len(report["missing"]["missing_in_queries"])
    report["missing"]["missing_in_candidates_count"] = len(report["missing"]["missing_in_candidates"])

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps({
        "ok": True,
        "missing_in_queries": report["missing"]["missing_in_queries_count"],
        "missing_in_candidates": report["missing"]["missing_in_candidates_count"],
        "out": args.out,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
