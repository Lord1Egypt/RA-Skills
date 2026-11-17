#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_queries_generic.py

通用版 Query 生成器：从 coverage_matrix（由 coverage_matrix.py 生成）动态生成 queries / boost_words。
核心目标：不依赖任何行业词硬编码；完全由 schema 的“非空维度与值”驱动。

输入：
- --schema schema.json
- --coverage coverage_matrix.json（可选；不传则内部调用coverage_matrix逻辑）
- --synonyms synonyms_map.json（可选，同义扩展）
输出：
- --out queries.json

约束：
- 总 query 数 >= max(min_query, 2 * 非空维度数)
- 高歧义短词不得单独成 query（若出现则与锚点拼接）
"""

import argparse
import json
import re
from itertools import combinations
from pathlib import Path
from typing import Any, Dict, List, Tuple

# 可扩展：跨行业通用歧义短词（不写行业词）
AMBIGUOUS_SHORT = {
    "粉", "宝宝", "宝", "车", "酒", "茶", "猫", "狗", "米", "油", "糖",
}


def _norm(s: str) -> str:
    s = str(s).strip()
    s = re.sub(r"\s+", "", s)
    return s


def _dedup_keep_order(items: List[str]) -> List[str]:
    seen = set()
    out = []
    for x in items:
        x = _norm(x)
        if not x or x in seen:
            continue
        seen.add(x)
        out.append(x)
    return out


def _load_synonyms(path: str) -> List[Tuple[str, List[str]]]:
    if not path:
        return []
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    items = data.get("items") if isinstance(data, dict) else None
    out = []
    if isinstance(items, list):
        for it in items:
            if not isinstance(it, dict):
                continue
            trig = it.get("trigger")
            exps = it.get("expand_terms")
            if isinstance(trig, str) and isinstance(exps, list):
                out.append((_norm(trig), [_norm(x) for x in exps if isinstance(x, str)]))
    return out


def _expand_by_synonyms(raw_words: List[str], synonyms: List[Tuple[str, List[str]]]) -> List[str]:
    out = list(raw_words)
    joined = " ".join(raw_words)
    for trig, exps in synonyms:
        if trig and trig in joined:
            out.extend([e for e in exps if e])
    return _dedup_keep_order(out)


def _choose_anchors(words: List[str], top_n: int = 8) -> List[str]:
    # 选“较长词”作为锚点，减少字面碰撞
    cands = [w for w in words if len(w) >= 2]
    cands = sorted(cands, key=lambda x: (-len(x), x))
    return cands[:top_n]


def _protect_ambiguous(words: List[str], anchors: List[str]) -> List[str]:
    safe = []
    for w in words:
        if w in AMBIGUOUS_SHORT:
            continue
        safe.append(w)
    # 将歧义短词与锚点拼接成组合query
    for w in words:
        if w in AMBIGUOUS_SHORT:
            for a in anchors:
                if a and a != w:
                    safe.append(f"{w}{a}")
                    safe.append(f"{a}{w}")
                    break
    return _dedup_keep_order(safe)


def _flatten_matrix(matrix: Dict[str, List[str]]) -> List[str]:
    out = []
    for dim, vals in (matrix or {}).items():
        if not isinstance(vals, list):
            continue
        for v in vals:
            if isinstance(v, str):
                out.append(_norm(v))
    return _dedup_keep_order(out)


def _build_queries(matrix: Dict[str, List[str]], synonyms_path: str, min_query: int) -> Tuple[List[str], List[str], Dict[str, Any]]:
    raw = _flatten_matrix(matrix)
    syn = _load_synonyms(synonyms_path)
    expanded = _expand_by_synonyms(raw, syn)

    anchors = _choose_anchors(expanded)
    protected = _protect_ambiguous(expanded, anchors)

    # 维度内保证：每个非空维度至少生成1条query（取该维度的前2个值组成短语）
    per_dim_q = []
    for dim, vals in (matrix or {}).items():
        if not isinstance(vals, list) or not vals:
            continue
        vv = [_norm(x) for x in vals if isinstance(x, str) and _norm(x)]
        vv = _dedup_keep_order(vv)
        if not vv:
            continue
        if len(vv) == 1:
            per_dim_q.append(vv[0])
        else:
            per_dim_q.append(f"{vv[0]} {vv[1]}")

    # 组合query（跨维度二元组合，增强覆盖）
    core = _choose_anchors(protected, top_n=10)
    combo = []
    for a, b in combinations(core, 2):
        if a != b:
            combo.append(f"{a} {b}")

    queries = _dedup_keep_order(per_dim_q + protected + combo)

    # 最小条数门禁
    non_empty_dims = len([k for k, v in (matrix or {}).items() if isinstance(v, list) and v])
    need = max(min_query, 2 * max(1, non_empty_dims))
    if len(queries) < need:
        # 用 anchors 继续补齐
        fillers = []
        for a in anchors:
            for b in anchors:
                if a != b:
                    fillers.append(f"{a} {b}")
                if len(queries) + len(fillers) >= need:
                    break
            if len(queries) + len(fillers) >= need:
                break
        queries = _dedup_keep_order(queries + fillers)

    queries = queries[:120]

    # boost_words：取anchors前12个（不含组合）
    boost = _dedup_keep_order([w for w in anchors if " " not in w])[:12]

    meta = {
        "min_query": min_query,
        "non_empty_dims": non_empty_dims,
        "query_target_min": need,
        "ambiguous_short": sorted(list(AMBIGUOUS_SHORT)),
    }
    return queries, boost, meta


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--schema", required=True)
    ap.add_argument("--coverage", default="")
    ap.add_argument("--synonyms", default="")
    ap.add_argument("--min-query", type=int, default=6)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    schema = json.loads(Path(args.schema).read_text(encoding="utf-8"))
    if not isinstance(schema, dict):
        raise SystemExit("schema.json必须为JSON对象")

    if args.coverage:
        cov = json.loads(Path(args.coverage).read_text(encoding="utf-8"))
        matrix = cov.get("coverage_matrix") if isinstance(cov, dict) else {}
    else:
        # fallback：简单抽取所有字符串作为一个维度
        matrix = {"_fallback_all": [str(schema.get("_raw_text") or "")]}

    queries, boost, meta = _build_queries(matrix, args.synonyms, args.min_query)

    out = {
        "queries": queries,
        "boost_words": boost,
        "query_count": len(queries),
        "boost_count": len(boost),
        "meta": meta,
    }

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"ok": True, "query_count": len(queries), "boost_count": len(boost), "out": args.out}, ensure_ascii=False))


if __name__ == "__main__":
    main()
