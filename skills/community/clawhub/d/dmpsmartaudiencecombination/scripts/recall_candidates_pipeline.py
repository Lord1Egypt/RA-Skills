#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""recall_candidates_pipeline.py

候选标签召回总控脚本（通用稳健版）：
- 先探测标签池能力（tag_pool覆盖）再召回
- 从schema动态生成coverage_matrix与queries
- 多轮自检与重跑（候选过少/跑偏/关键维度缺口）
- 动态兜底（按coverage_matrix逐维度补候选）
- 输出 merged_candidates.json + recall_diag.json

说明：
- 本脚本会调用接口拉取 tag/list（通过现有 query_tag_list.py）。
- 不会创建人群包，不会修改用户的MUST/PREFERRED/OPTIONAL选择。

输入：
- --schema: schema.json
- --out-dir: 输出目录（默认 data/run）
- --replay-from: 回放目录（可选；提供后将直接复用该目录的召回产物，保证同需求二次运行一致）
- --synonyms: 同义扩展表（默认 references/synonyms_map.json）

输出：
- tag_pool.json / coverage_matrix.json / probe_report.json / queries.json / candidates.json
- merged_candidates.json / recall_diag.json
"""

import argparse
import json
import os
import re
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Tuple

import shutil

SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent


def _run(cmd: List[str]) -> Dict[str, Any]:
    r = subprocess.run(cmd, capture_output=True, text=True)
    out = (r.stdout or "").strip()
    err = (r.stderr or "").strip()
    if r.returncode != 0:
        raise RuntimeError(f"command_failed: {' '.join(cmd)}\n{err or out}")
    # 尝试解析最后一行json
    last = out.splitlines()[-1] if out else ""
    try:
        return json.loads(last)
    except Exception:
        return {"ok": True, "raw": out}


def _load_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _save_json(p: Path, data: Any):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _norm(s: str) -> str:
    s = str(s).strip().lower()
    s = re.sub(r"\s+", "", s)
    return s


def _token_overlap(a: str, b: str) -> int:
    # 粗粒度字符交集计数（仅用于假阳性启发式）
    aa = set(list(_norm(a)))
    bb = set(list(_norm(b)))
    return len([c for c in aa if c in bb])


def _contains_any(text: str, words: List[str]) -> bool:
    t = _norm(text)
    for w in words:
        ww = _norm(w)
        if ww and ww in t:
            return True
    return False


def _is_false_positive(tag_name: str, matched_query: str, boost_words: List[str], schema_tokens: List[str]) -> bool:
    """通用假阳性判定（不靠行业黑名单）：
    - 规则1：短query(<=2)命中，且tag不含任何boost
    - 规则2：tag与query字符重叠<=2，且tag不含schema任一锚点token
    """
    qn = _norm(matched_query)
    tn = _norm(tag_name)

    if len(qn) <= 2 and not _contains_any(tn, boost_words):
        return True

    ov = _token_overlap(tn, qn)
    if ov <= 2 and (not _contains_any(tn, boost_words)) and (not _contains_any(tn, schema_tokens)):
        return True

    return False


def _pick_anchor_tokens(coverage_matrix: Dict[str, List[str]]) -> List[str]:
    # 选取较长的token作为锚点
    tokens = []
    for _, vals in (coverage_matrix or {}).items():
        if isinstance(vals, list):
            tokens.extend([v for v in vals if isinstance(v, str) and v.strip()])
    tokens = list(dict.fromkeys(tokens))
    tokens = sorted(tokens, key=lambda x: (-len(x), x))
    return tokens[:20]


def _fallback_by_matrix(tag_pool: List[Dict], candidates: List[Dict], matrix: Dict[str, List[str]], boost_words: List[str]) -> Tuple[List[Dict], List[Dict]]:
    """按coverage_matrix逐维度兜底：如果某维度的所有值在candidate中都没出现，则从tag_pool中按子串匹配补候选。"""
    cand_names = [_norm(c.get("tagName", "")) for c in candidates if isinstance(c, dict)]

    gaps = []
    added = []
    existing_ids = {c.get("tagId") for c in candidates if isinstance(c, dict)}

    for dim, vals in (matrix or {}).items():
        if not isinstance(vals, list) or not vals:
            continue
        vv = [v for v in vals if isinstance(v, str) and v.strip()]
        if not vv:
            continue

        hit = False
        for v in vv:
            vn = _norm(v)
            if not vn:
                continue
            if any(vn in nm for nm in cand_names):
                hit = True
                break

        if hit:
            continue

        # gap
        gaps.append({"dimension": dim, "values": vv, "reason": "no_coverage_in_candidates"})

        # 从tag_pool中按值匹配补候选（每个维度最多补3个）
        fb = []
        for v in vv:
            vn = _norm(v)
            if not vn:
                continue
            for t in tag_pool:
                name = _norm(t.get("tagName", ""))
                if vn and vn in name:
                    fb.append(t)
            if len(fb) >= 10:
                break

        # 去重+排序
        dedup = {}
        for t in fb:
            tid = t.get("tagId")
            if tid is None or tid in existing_ids:
                continue
            if tid not in dedup:
                dedup[tid] = t
        fb2 = list(dedup.values())
        fb2.sort(key=lambda x: int(x.get("tagId") or 0))

        for t in fb2[:3]:
            item = {
                "tagId": t.get("tagId"),
                "tagName": t.get("tagName"),
                "parentId": t.get("parentId"),
                "tagType": t.get("tagType"),
                "isDirectory": t.get("isDirectory"),
                "similarity": 0.86 if _contains_any(t.get("tagName", ""), boost_words) else 0.82,
                "recall_source": "fallback_dict",
            }
            added.append(item)
            existing_ids.add(item["tagId"])

    return added, gaps


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--schema", required=True)
    ap.add_argument("--out-dir", default=str(Path("data/run")))
    ap.add_argument("--replay-from", default="", help="回放目录：直接复用上一轮召回产物，保证同需求二次运行一致")
    ap.add_argument("--synonyms", default=str(SKILL_DIR / "references" / "synonyms_map.json"))
    ap.add_argument("--tag-types", nargs="+", default=["1", "3"], help="默认同时拉取1和3")
    ap.add_argument("--top-k", type=int, default=60)
    ap.add_argument("--threshold", type=float, default=0.15)
    ap.add_argument("--max-rerun", type=int, default=2)
    ap.add_argument("--min-candidates", type=int, default=30)
    args = ap.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    diag: Dict[str, Any] = {
        "ok": True,
        "reruns": [],
        "gaps": [],
        "downgrades": [],
        "gate": None,
    }

    # 回放模式：直接复用上一轮召回产物，避免二次运行因重跑/参数调整产生差异
    if args.replay_from:
        replay_dir = Path(args.replay_from)
        if not replay_dir.exists() or not replay_dir.is_dir():
            raise SystemExit(f"回放目录不存在或不可用: {args.replay_from}")

        # 需要复用的产物清单（均为本脚本输出）
        artifacts = [
            "tag_pool.json",
            "coverage_matrix.json",
            "probe_report.json",
            "queries.json",
            "queries.txt",
            "candidates.json",
            "merged_candidates.json",
            "recall_diag.json",
        ]

        copied = []
        missing = []
        for fn in artifacts:
            src = replay_dir / fn
            dst = out_dir / fn
            if src.exists() and src.is_file():
                shutil.copy2(src, dst)
                copied.append(fn)
            else:
                missing.append(fn)

        if missing:
            raise SystemExit(
                "回放目录缺少必要文件，无法保证一致性：" + ",".join(missing)
            )

        # 读取回放结果并直接输出
        merged_path = out_dir / "merged_candidates.json"
        diag_path = out_dir / "recall_diag.json"
        merged = _load_json(merged_path)
        diag = _load_json(diag_path)
        gate = diag.get("gate") if isinstance(diag, dict) else None

        print(json.dumps({
            "ok": True,
            "mode": "replay",
            "replay_from": str(replay_dir),
            "out_dir": str(out_dir),
            "copied": copied,
            "merged": str(merged_path),
            "diag": str(diag_path),
            "merged_total": len(merged) if isinstance(merged, list) else None,
            "gate": gate,
        }, ensure_ascii=False))
        return

    # Step A: 拉取tag_pool（接口调用）
    tag_pool_path = out_dir / "tag_pool.json"
    _run([
        "python3", str(SCRIPT_DIR / "query_tag_list.py"),
        "--only-leaf", "--out", str(tag_pool_path),
        "--tag-types", *[str(x) for x in args.tag_types],
    ])

    # Step B: coverage_matrix
    cov_path = out_dir / "coverage_matrix.json"
    _run(["python3", str(SCRIPT_DIR / "coverage_matrix.py"), "--schema", args.schema, "--out", str(cov_path)])

    cov = _load_json(cov_path)
    matrix = cov.get("coverage_matrix", {}) if isinstance(cov, dict) else {}

    # Step C: 能力探测
    probe_path = out_dir / "probe_report.json"
    _run(["python3", str(SCRIPT_DIR / "capability_probe.py"), "--schema", args.schema, "--tag-pool", str(tag_pool_path), "--coverage", str(cov_path), "--out", str(probe_path)])
    probe = _load_json(probe_path)
    diag["gaps"].extend(probe.get("gaps", []) if isinstance(probe, dict) else [])
    diag["downgrades"].extend(probe.get("downgrade_suggestions", []) if isinstance(probe, dict) else [])

    # Step D: 生成稳健queries
    queries_path = out_dir / "queries.json"
    _run(["python3", str(SCRIPT_DIR / "build_queries_generic.py"), "--schema", args.schema, "--coverage", str(cov_path), "--synonyms", args.synonyms, "--min-query", "6", "--out", str(queries_path)])

    queries_obj = _load_json(queries_path)
    boost_words = queries_obj.get("boost_words", []) if isinstance(queries_obj, dict) else []
    queries_list = queries_obj.get("queries", []) if isinstance(queries_obj, dict) else []

    # 写queries.txt给语义召回脚本使用
    queries_txt = out_dir / "queries.txt"
    queries_txt.write_text("\n".join([str(q) for q in queries_list if str(q).strip()]), encoding="utf-8")

    # Step E: 语义召回（带自检重跑）
    tag_pool = _load_json(tag_pool_path)
    schema = _load_json(Path(args.schema))
    schema_tokens = _pick_anchor_tokens(matrix)

    cur_topk = args.top_k
    cur_th = args.threshold

    candidates_path = out_dir / "candidates.json"

    def run_semantic(topk: int, threshold: float):
        _run([
            "python3", str(SCRIPT_DIR / "tag_semantic_search.py"),
            "--tags", str(tag_pool_path),
            "--query-file", str(queries_txt),
            "--boost-words-json", str(queries_path),
            "--boost-value", "0.03",
            "--top-k", str(topk),
            "--threshold", str(threshold),
            "--out", str(candidates_path),
        ])

    run_semantic(cur_topk, cur_th)

    rerun_count = 0
    while rerun_count < args.max_rerun:
        candidates = _load_json(candidates_path)
        if not isinstance(candidates, list):
            candidates = []

        # 自检1：候选过少
        if len(candidates) < args.min_candidates:
            diag["reruns"].append({"reason": "too_few_candidates", "before": {"topk": cur_topk, "threshold": cur_th}})
            # 调参并重跑
            cur_topk = min(200, int(cur_topk * 2))
            cur_th = max(0.05, float(cur_th) - 0.05)
            run_semantic(cur_topk, cur_th)
            rerun_count += 1
            continue

        # 自检2：明显跑偏（Top50假阳性比例）
        topn = candidates[:50]
        fp = 0
        for c in topn:
            # 用最短query近似（取第一条）做启发式判断
            q0 = queries_list[-1] if queries_list else ""
            if _is_false_positive(str(c.get("tagName", "")), str(q0), boost_words, schema_tokens):
                fp += 1
        fp_ratio = fp / 50.0 if topn else 0.0
        if fp_ratio > 0.2:
            diag["reruns"].append({"reason": "high_false_positive_ratio", "fp_ratio": fp_ratio, "before": {"topk": cur_topk, "threshold": cur_th}})
            cur_topk = min(200, int(cur_topk * 2))
            cur_th = max(0.05, float(cur_th) - 0.03)
            run_semantic(cur_topk, cur_th)
            rerun_count += 1
            continue

        break

    candidates = _load_json(candidates_path)
    if not isinstance(candidates, list):
        candidates = []

    # Step F: 动态兜底（按coverage_matrix）
    fb_added, fb_gaps = _fallback_by_matrix(tag_pool, candidates, matrix, boost_words)
    diag["gaps"].extend(fb_gaps)

    # 合并：保留semantic原记录；兜底补入
    merged = []
    seen = set()
    for c in candidates:
        if not isinstance(c, dict):
            continue
        tid = c.get("tagId")
        if tid in seen:
            continue
        c2 = dict(c)
        c2.setdefault("recall_source", "semantic")
        merged.append(c2)
        seen.add(tid)
    for f in fb_added:
        tid = f.get("tagId")
        if tid in seen:
            continue
        merged.append(f)
        seen.add(tid)

    # Step G: 门禁（输出前检查）
    # 规则：merged < 5 或 gaps过多 → gate=GAP
    gate = {"status": "OK"}
    if len(merged) < 5:
        gate = {"status": "TOO_FEW", "count": len(merged)}
    elif len(diag.get("gaps", [])) > 0:
        gate = {"status": "GAP", "gap_count": len(diag.get("gaps", []))}
    diag["gate"] = gate


    merged_path = out_dir / "merged_candidates.json"
    diag_path = out_dir / "recall_diag.json"
    _save_json(merged_path, merged)

    # Step F.5: 需求不遗漏审计（coverage_matrix -> queries -> merged_candidates）
    # 仅输出审计结果文件与缺失计数，不做业务决策。
    audit_path = out_dir / "requirement_audit.json"
    _run([
        "python3", str(SCRIPT_DIR / "requirement_audit.py"),
        "--schema", args.schema,
        "--coverage", str(cov_path),
        "--queries", str(queries_path),
        "--candidates", str(merged_path),
        "--out", str(audit_path),
    ])

    _save_json(diag_path, diag)

    print(json.dumps({
        "ok": True,
        "tag_pool": str(tag_pool_path),
        "coverage": str(cov_path),
        "probe": str(probe_path),
        "queries": str(queries_path),
        "candidates": str(candidates_path),
        "merged": str(merged_path),
        "diag": str(diag_path),
        "merged_total": len(merged),
        "gate": gate,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()