"""排行榜质量 + 榜源 schema 校验（L0#4 / L0#5）。

从 leaderboard.py 拆出，避免主编排模块膨胀（P0#4 模块体量守护：单文件 ≤ 800 行）。
校验逻辑为纯函数，无榜源依赖，可独立单测；canon_key 来自叶子模块 aiweekly.canon
（P2-1：循环依赖已消除，改为顶部导入）。
"""
from aiweekly.canon import canon_key  # P2-1：叶子模块，无循环依赖

# 排行行允许字段白名单（L0#5）：fetcher 漏出的非标字段（如旧 cost_in/cost_out）会被标红。
# 注意：likes（社区点赞数）/ params（参数量）是 HF、LLM-Stats、ModelScope 等开源榜
# fetcher 有意附加的真实元数据字段（见 leaderboard_sources.py），属标准开放字段而非脏数据，
# 故纳入白名单，避免每周开源榜命中时误报 24/25。
LB_ROW_FIELDS = {
    "model", "rank", "score", "org", "developer", "license", "context",
    "price_in", "price_out", "delta", "spark", "cn_access", "open_source",
    "multimodal", "best_for", "commercial", "currency",
    "likes", "params",
}


def validate_leaderboard_data(data: dict) -> dict:
    """对 LEADERBOARD_DATA 做结构化质量 + schema 校验（L0#4 / L0#5）。

    返回 {"ok": bool, "issues": [str], "checks": {...}}。
    checks 含每榜：rows 数、source/url/snapshot 非空（仅非缓存槽）、model 非空、
    同榜归一键去重、跨榜(lmarena vs aa)同名 rank 差 ≤ 20、selection_notes 三段齐全、
    schema 白名单命中率、delta 字段覆盖率。
    """
    issues = []
    checks = {}
    if not isinstance(data, dict):
        return {"ok": False, "issues": ["LEADERBOARD_DATA 非 dict"], "checks": {}}
    comp = data.get("comprehensive", {}) or {}
    osb = data.get("open_source", {}) or {}
    boards = [
        ("comprehensive.lmarena", comp.get("lmarena", {})),
        ("comprehensive.aa", comp.get("aa", {})),
        ("open_source.ls", osb.get("ls", {})),
        ("open_source.hf", osb.get("hf", {})),
    ]
    for name, slot in boards:
        slot = slot or {}
        rows = slot.get("rows", []) or []
        c = {"rows": len(rows)}
        # 每榜 ≥ 5 条
        if len(rows) < 5:
            issues.append(f"[{name}] 行数 {len(rows)} < 5")
            c["min_rows"] = False
        else:
            c["min_rows"] = True
        # source/url/snapshot 非空（仅非缓存槽要求；缓存兜底本就空 url）
        if not slot.get("is_cache"):
            for fld in ("source", "url", "snapshot"):
                if not str(slot.get(fld, "")).strip():
                    issues.append(f"[{name}] 字段 {fld} 为空")
                    c.setdefault("meta_complete", False)
                else:
                    c["meta_complete"] = c.get("meta_complete", True)
        # model 字段非空（无空字符串）
        empty_model = any((not str(r.get("model", "")).strip()) for r in rows)
        if empty_model:
            issues.append(f"[{name}] 存在空 model 字段")
            c["model_nonempty"] = False
        else:
            c["model_nonempty"] = True
        # 同榜归一键去重
        keys = [canon_key(r.get("model", "")) for r in rows]
        dups = len(keys) - len(set(k for k in keys if k))
        if dups > 0:
            issues.append(f"[{name}] 同榜归一键重复 {dups} 处（变体双胞胎未合并）")
            c["dedup"] = False
        else:
            c["dedup"] = True
        # schema 白名单：统计非标字段
        unknown = set()
        for r in rows:
            for k in r.keys():
                if k not in LB_ROW_FIELDS:
                    unknown.add(k)
        if unknown:
            issues.append(f"[{name}] 出现非标字段：{sorted(unknown)}")
            c["schema_ok"] = False
        else:
            c["schema_ok"] = True
        # delta 字段覆盖率（L1 守护：≥ 50% 行含 delta）
        has_delta = sum(1 for r in rows if isinstance(r.get("delta"), dict))
        c["delta_coverage"] = round(has_delta / len(rows), 2) if rows else 0
        if has_delta < (len(rows) * 0.5) and rows:
            issues.append(f"[{name}] delta 覆盖率 {c['delta_coverage']} < 0.5")
            c["delta_ok"] = False
        else:
            c["delta_ok"] = True
        checks[name] = c

    # 跨榜一致性：lmarena vs aa 同名（归一键）rank 差 ≤ 20
    lm_rows = {canon_key(r.get("model", "")): r.get("rank")
               for r in (comp.get("lmarena", {}).get("rows", []) or [])
               if r.get("rank") is not None}
    aa_rows = {canon_key(r.get("model", "")): r.get("rank")
               for r in (comp.get("aa", {}).get("rows", []) or [])
               if r.get("rank") is not None}
    cross_bad = []
    for ck, lr in lm_rows.items():
        ar = aa_rows.get(ck)
        if ar is not None and abs(lr - ar) > 20:
            cross_bad.append(ck)
    if cross_bad:
        issues.append(f"跨榜(lmarena vs aa) rank 差 > 20：{cross_bad}")
        checks["cross_consistency"] = False
    else:
        checks["cross_consistency"] = True

    # selection_notes 三段齐全（开发者/PM/自媒体）
    sn = data.get("selection_notes")
    if isinstance(sn, dict) and all(sn.get(k) for k in ("开发者", "PM", "自媒体")):
        checks["selection_notes"] = True
    else:
        issues.append("selection_notes 缺少 开发者/PM/自媒体 三段")
        checks["selection_notes"] = False

    return {"ok": len(issues) == 0, "issues": issues, "checks": checks}
