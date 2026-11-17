#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""capability_probe.py

能力层：先探测标签池，再召回。
- 输入：schema.json + tag_pool.json + coverage_matrix.json
- 输出：probe_report.json（每个维度/值在tag_pool中是否可覆盖；gap与降级建议）

不做召回，不调用外部API。
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


def _load_json(p: str) -> Any:
    return json.loads(Path(p).read_text(encoding="utf-8"))


def _match_in_pool(tag_pool: List[Dict], token: str) -> List[Dict]:
    token_n = _norm(token)
    hits = []
    if not token_n:
        return hits
    for t in tag_pool:
        name = _norm(t.get("tagName", ""))
        if token_n and token_n in name:
            hits.append(t)
    hits.sort(key=lambda x: int(x.get("tagId") or 0))
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--schema", required=True)
    ap.add_argument("--tag-pool", required=True)
    ap.add_argument("--coverage", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    schema = _load_json(args.schema)
    tag_pool = _load_json(args.tag_pool)
    cov = _load_json(args.coverage)

    matrix = cov.get("coverage_matrix") if isinstance(cov, dict) else {}
    if not isinstance(matrix, dict):
        matrix = {}

    report = {
        "ok": True,
        "coverage_probe": {},
        "gaps": [],
        "downgrade_suggestions": [],
        "meta": {
            "note": "仅做tag_pool覆盖探测；缺失不等于召回失败，可能是标签池能力缺口。",
        },
    }

    # 按维度逐值探测
    for dim, vals in matrix.items():
        if not isinstance(vals, list) or not vals:
            continue
        dim_rec = []
        for v in vals[:30]:
            if not isinstance(v, str) or not v.strip():
                continue
            hits = _match_in_pool(tag_pool, v)
            dim_rec.append({
                "value": v,
                "hit_count": len(hits),
                "sample_tag_ids": [h.get("tagId") for h in hits[:5]],
            })
            if len(hits) == 0:
                report["gaps"].append({"dimension": dim, "value": v, "reason": "tag_pool_missing"})
        report["coverage_probe"][dim] = dim_rec

    # 城市级别的特殊降级：仅当schema/coverage中出现“新一线”字样且池内无命中时给建议
    raw_text = str(schema.get("_raw_text") or "")
    joined = raw_text + " " + " ".join([str(x) for x in matrix.get("location", []) if isinstance(x, str)])
    if "新一线" in joined:
        # 判断标签池是否存在“新一线城市”
        has_new = len(_match_in_pool(tag_pool, "新一线城市")) > 0 or len(_match_in_pool(tag_pool, "新一线")) > 0
        if not has_new:
            report["downgrade_suggestions"].append({
                "dimension": "location.city_tier",
                "gap": "new_tier_missing",
                "recommended": ["一线城市", "二线城市"],
                "note": "标签池缺失‘新一线’相关标签：建议用‘一线 OR 二线’近似高线口径（不自动选中）。",
            })

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"ok": True, "gap_count": len(report["gaps"]), "out": args.out}, ensure_ascii=False))


if __name__ == "__main__":
    main()
