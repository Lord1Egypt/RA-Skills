#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""coverage_matrix.py

从任意schema.json中“动态提取非空维度→维度值集合”，用于通用召回、兜底、门禁。
- 不依赖第三方包
- 不调用任何外部API

输出结构：
{
  "coverage_matrix": {"dimension": ["v1","v2",...]},
  "non_empty_dimensions": ["dimension", ...],
  "meta": {"min_query": 6, ...}
}

注意：本脚本只做“信息抽取”，不做业务判断。
"""

import argparse
import json
import re
from pathlib import Path
from typing import Any, Dict, List


# KEY_DIMENSIONS：从schema中优先抽取的“结构化维度键”。
# 目标：尽量不遗漏用户明确表达的要素；同时保持跨行业通用。
KEY_DIMENSIONS = [
    # 业务/品类
    "industry", "category", "interest",

    # 人群/画像
    "demographics", "audience", "constraints", "objective",

    # 地理/位置（含常见别名）
    "location", "geo", "geography", "region",
    "geo_focus", "geoLevel", "city", "cities", "city_level", "cityLevel", "city_tier", "cityTier",

    # 行为/场景
    "activity", "behavior", "scenario", "lifestyle",

    # 兼容：部分schema直接用这些字段表达目标人群/阶段
    "target_persona", "baby_age", "child_age", "age_stage",
]

_STOP = {
    "是", "否", "有", "无", "需要", "不要", "想要", "想", "做", "投放", "拉新", "转化", "覆盖",
}


def _norm(s: str) -> str:
    s = str(s).strip()
    s = re.sub(r"\s+", "", s)
    return s


def _is_value_like(x: Any) -> bool:
    if x is None:
        return False
    if isinstance(x, (int, float, bool)):
        return False
    if isinstance(x, str):
        t = _norm(x)
        if not t:
            return False
        if t in _STOP:
            return False
        return True
    return False


def _collect_strings(obj: Any) -> List[str]:
    out: List[str] = []
    if obj is None:
        return out
    if isinstance(obj, dict):
        for k, v in obj.items():
            if str(k).startswith("_"):
                continue
            out.extend(_collect_strings(v))
        return out
    if isinstance(obj, list):
        for it in obj:
            out.extend(_collect_strings(it))
        return out
    if _is_value_like(obj):
        s = _norm(obj)
        if s:
            # 原值保留
            out.append(s)
            # 通用拆分：避免用户表达用“+ / 、,，”等连接符导致召回漏掉
            parts = re.split(r"[\s\+\|/、,，;；]+", s)
            for p in parts:
                p = _norm(p)
                if p and p != s:
                    out.append(p)
    return out


def _dedup_keep_order(items: List[str]) -> List[str]:
    seen = set()
    out = []
    for x in items:
        if not x:
            continue
        if x in seen:
            continue
        seen.add(x)
        out.append(x)
    return out


def build_matrix(schema: Dict[str, Any]) -> Dict[str, List[str]]:
    matrix: Dict[str, List[str]] = {}

    # 1) 优先按预设维度键提取
    for dim in KEY_DIMENSIONS:
        if dim in schema and schema.get(dim) is not None:
            vals = _dedup_keep_order(_collect_strings(schema.get(dim)))
            if vals:
                matrix[dim] = vals

    # 2) 兜底：如果上述都没命中，直接从全schema抽取（避免空矩阵）
    if not matrix:
        vals = _dedup_keep_order(_collect_strings(schema))
        if vals:
            matrix["_fallback_all"] = vals

    # 3) 总是加入raw_text到一个特殊维度（用于召回补线索）
    raw = schema.get("_raw_text")
    if _is_value_like(raw):
        matrix.setdefault("_raw_text", [])
        matrix["_raw_text"] = _dedup_keep_order(matrix["_raw_text"] + [_norm(raw)])

    return matrix


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--schema", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    schema = json.loads(Path(args.schema).read_text(encoding="utf-8"))
    if not isinstance(schema, dict):
        raise SystemExit("schema.json必须为JSON对象")

    matrix = build_matrix(schema)
    non_empty = [k for k, v in matrix.items() if v]

    out = {
        "coverage_matrix": matrix,
        "non_empty_dimensions": non_empty,
        "meta": {
            "note": "维度与值完全来自schema（动态推导），不做行业硬编码。",
        },
    }

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"ok": True, "dims": len(non_empty), "out": args.out}, ensure_ascii=False))


if __name__ == "__main__":
    main()
