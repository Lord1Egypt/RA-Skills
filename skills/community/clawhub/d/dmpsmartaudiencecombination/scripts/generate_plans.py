#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""generate_plans.py - 基于Overlap和扩缩量分析，生成4种组合方案

方案定义：
- 扩展型：MUST only，覆盖面最大
- 精准型：MUST + 全部PREFERRED（同维度OR，跨维度AND）
- 综合型：MUST + 核心PREFERRED + 1个收窄适中的Optional AND
- 扩量型：MUST + 同维度OR追加 / 减非核心AND条件（比精准型大，比扩展型定向强）

⚠️ 不生成跨维度OR方案（会改变人群方向）。
⚠️ 预测量级区分exact和estimated。
⚠️ 父子标签已在前置步骤处理。
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).parent))
from rules_helper import build_rules_http, validate_rules_http
from tag_hierarchy import must_to_or_groups, build_parent_map, get_ancestors, group_tags_by_dimension


def _load_list(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    out = []
    for it in (data if isinstance(data, list) else []):
        if isinstance(it, dict) and it.get("tagId") is not None:
            out.append({"tagId": int(it["tagId"]), "tagName": it.get("tagName")})
        elif not isinstance(it, dict):
            out.append({"tagId": int(it), "tagName": None})
    return out


def _name_map(tag_pool):
    return {int(t["tagId"]): t.get("tagName", "") for t in tag_pool if t.get("isDirectory") == 1}


def _fmt_logic(or_groups, nm):
    parts = []
    for g in or_groups:
        names = [nm.get(t, str(t)) for t in g]
        parts.append("(" + " OR ".join(names) + ")" if len(names) > 1 else names[0])
    return " AND ".join(parts)


def _build_rules(or_groups):
    rules = build_rules_http(or_groups)
    errors = validate_rules_http(rules)
    if errors:
        raise ValueError(f"规则校验失败: {';'.join(errors)}")
    return rules


def _get_group_dim(g, tag_pool, core_kws):
    """判断一个OR组属于哪个维度。"""
    for tid in g:
        t = {int(t["tagId"]): t for t in tag_pool}.get(tid, {})
        cat = str(t.get("category", ""))
        name = t.get("tagName", "")
        if re.match(r'^(?:基础属性|基本属性)?_?性别_[男女]$', name) or name in ("女", "男", "女性", "男性") or "性别" in cat:
            return "性别"
        if re.search(r'_年龄_\d', name) or "年龄" in cat or "岁" in name or (name and name[:1].isdigit() and "-" in name):
            return "年龄"
        if "居住城市级别" in name or "城市级别" in cat or re.search(r'[一二三四新]线城市', name):
            return "城市级别"
        if any(kw in cat or kw in name for kw in core_kws):
            return "核心兴趣"
        if "消费" in cat or "轻奢" in name or "收入" in name:
            return "消费力"
        if "白领" in name or "职业" in cat:
            return "职业"
    return "其他"


def _merge_pref(base_groups, pref_ids, tag_pool, core_kws):
    """将PREFERRED标签合并到base_groups（同维度OR追加，新维度AND追加）。"""
    if not pref_ids:
        return [list(g) for g in base_groups]
    result = [sorted(set(g)) for g in base_groups]
    must_all = set()
    for g in result:
        must_all.update(g)
    pmap = build_parent_map(tag_pool) if tag_pool else {}
    # 父子去重
    deduped = []
    for tid in pref_ids:
        if tag_pool and pmap:
            ancs = get_ancestors(tid, pmap)
            if ancs & must_all:
                continue
        deduped.append(tid)
    if not deduped:
        return result
    pref_groups = group_tags_by_dimension(deduped, tag_pool, core_kws)
    dim2idx = {}
    for i, g in enumerate(result):
        d = _get_group_dim(g, tag_pool, core_kws)
        dim2idx[d] = i
    dim_order = ["性别", "年龄", "城市级别", "核心兴趣", "消费力", "职业", "活跃度", "其他"]
    for dim in dim_order:
        if dim not in pref_groups:
            continue
        add = sorted(pref_groups[dim])
        if dim in dim2idx:
            idx = dim2idx[dim]
            result[idx] = sorted(set(result[idx] + add))
        else:
            result.append(add)
    return result


def _estimate_and(m_amt, extra_tag_ids, overlap_data):
    """估算AND多个额外标签后的量级：M × ∏r（条件独立假设，粗略估算）。"""
    mvo = {r["tagId"]: r for r in overlap_data.get("must_vs_optional", [])}
    amt = m_amt
    for tid in extra_tag_ids:
        r = mvo.get(tid, {}).get("r")
        if r is not None:
            amt = int(amt * r)
        else:
            return None  # 缺少r值无法估算
    return max(amt, 0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--must", required=True)
    ap.add_argument("--preferred", default=None)
    ap.add_argument("--optional", default=None)
    ap.add_argument("--overlap", required=True, help="analyze_overlap.py输出")
    ap.add_argument("--scale-report", default=None, help="analyze_scale.py输出（可选）")
    ap.add_argument("--tag-pool", default=None)
    ap.add_argument("--core-kws", default="美妆个护,护肤,彩妆")
    ap.add_argument("--amount-m", type=int, required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    skill_dir = Path(__file__).parent.parent
    pool_path = Path(args.tag_pool) if args.tag_pool else skill_dir / "tag_pool.json"
    tag_pool = []
    if pool_path.exists():
        with open(pool_path, "r", encoding="utf-8") as f:
            tag_pool = json.load(f)
    core_kws = [kw.strip() for kw in args.core_kws.split(",") if kw.strip()]
    nm = _name_map(tag_pool)

    # 加载Overlap
    with open(args.overlap, "r", encoding="utf-8") as f:
        overlap_data = json.load(f)
    mvo = {r["tagId"]: r for r in overlap_data.get("must_vs_optional", [])}

    # 加载scale report（可选）
    scale_report = {}
    if args.scale_report:
        with open(args.scale_report, "r", encoding="utf-8") as f:
            scale_report = json.load(f)

    # 加载MUST并自动分组+父子去重
    must_raw = _load_list(args.must)
    must_ids = [x["tagId"] for x in must_raw]
    if tag_pool:
        must_groups, removed_must, warns = must_to_or_groups(must_ids, tag_pool, core_kws)
    else:
        must_groups = [[tid] for tid in must_ids]
        removed_must = []

    must_all = set()
    for g in must_groups:
        must_all.update(g)

    preferred = _load_list(args.preferred) if args.preferred else []
    optional = _load_list(args.optional) if args.optional else []
    pref_ids = [x["tagId"] for x in preferred]
    opt_ids = [x["tagId"] for x in optional if x["tagId"] not in must_all]

    M = args.amount_m
    plans = []

    # ────── 方案1：扩展型（MUST only）──────
    ext_groups = [list(g) for g in must_groups]
    ext_data = _build_rules(ext_groups)
    plans.append({
        "plan_name": "扩展型",
        "plan_type": "扩展",
        "logic_text": _fmt_logic(ext_groups, nm),
        "or_groups": ext_groups,
        "data": ext_data,
        "tags_used": [t for g in ext_groups for t in g],
        "expansion_type": "must_only",
        "estimated_amount": M,
        "amount_precision": "exact",
        "notes": "仅MUST核心条件，覆盖面最大，适合拉新/曝光。"
    })

    # ────── 方案2：精准型（MUST + 全部PREFERRED AND）──────
    prec_groups = _merge_pref(must_groups, pref_ids, tag_pool, core_kws)
    prec_data = _build_rules(prec_groups)
    prec_extra = [t for g in prec_groups for t in g if t not in must_all]
    prec_amt = _estimate_and(M, prec_extra, overlap_data)
    plans.append({
        "plan_name": "精准型",
        "plan_type": "精准",
        "logic_text": _fmt_logic(prec_groups, nm),
        "or_groups": prec_groups,
        "data": prec_data,
        "tags_used": [t for g in prec_groups for t in g],
        "expansion_type": "and_narrow",
        "estimated_amount": prec_amt,
        "amount_precision": "estimated" if prec_amt else "unknown",
        "notes": "MUST + 全部PREFERRED（同维度OR，跨维度AND），定向最精准。需创建后确认真实量级。"
    })

    # ────── 方案3：综合型（MUST + 核心PREFERRED + 1个r适中的Optional AND）──────
    # 从scale_report或mvo中选r最接近0.3的
    pref_core = pref_ids[:max(1, len(pref_ids)//2)] if pref_ids else []
    bal_groups = _merge_pref(must_groups, pref_core, tag_pool, core_kws)
    and_opt = None
    best_dist = 1.0
    for tid in opt_ids:
        r = mvo.get(tid, {}).get("r")
        if r is not None and 0.15 <= r <= 0.5:
            dist = abs(r - 0.3)
            if dist < best_dist:
                best_dist = dist
                and_opt = tid
    bal_extra = list(pref_core)
    if and_opt:
        opt_dim = group_tags_by_dimension([and_opt], tag_pool, core_kws) if tag_pool else {"其他": [and_opt]}
        for dim, tags in opt_dim.items():
            if tags:
                bal_groups.append(sorted(tags))
                bal_extra.append(and_opt)
    bal_data = _build_rules(bal_groups)
    bal_amt = _estimate_and(M, bal_extra, overlap_data)
    opt_name = nm.get(and_opt, str(and_opt)) if and_opt else "无"
    plans.append({
        "plan_name": "综合型",
        "plan_type": "综合",
        "logic_text": _fmt_logic(bal_groups, nm),
        "or_groups": bal_groups,
        "data": bal_data,
        "tags_used": [t for g in bal_groups for t in g],
        "expansion_type": "and_narrow_moderate",
        "estimated_amount": bal_amt,
        "amount_precision": "estimated" if bal_amt else "unknown",
        "and_optional_tag": and_opt,
        "and_optional_name": opt_name,
        "notes": f"MUST + 核心PREFERRED + {opt_name}（AND r≈{mvo.get(and_opt,{}).get('r','?'):.0%}），平衡规模与精准。" if and_opt else "MUST + 核心PREFERRED，无合适Optional。"
    })

    # ────── 方案4：扩量型（同维度OR追加/减非核心AND）──────
    # 默认策略：在精准型基础上，去掉消费力/职业等非核心PREFERRED，或同维度OR追加标签
    # 简化版：取MUST + 核心2个维度PREFERRED（性别+年龄+核心兴趣+城市），不加消费力/职业
    # 如果scale_report有or_expansion数据，可以做精确OR扩量
    exp_core_pref = []
    # 只保留核心维度的PREFERRED：年龄、城市级别
    if tag_pool:
        for tid in pref_ids:
            d = None
            tmap = {int(t["tagId"]): t for t in tag_pool}
            t = tmap.get(tid, {})
            cat = str(t.get("category", ""))
            tn = t.get("tagName", "")
            if "年龄" in cat or "岁" in tn or (tn and tn[:1].isdigit() and "-" in tn):
                d = "年龄"
            elif "城市级别" in cat or "线城市" in tn:
                d = "城市级别"
            if d in ("年龄", "城市级别"):
                exp_core_pref.append(tid)
    exp_groups = _merge_pref(must_groups, exp_core_pref, tag_pool, core_kws) if exp_core_pref else [list(g) for g in must_groups]
    exp_extra = [t for g in exp_groups for t in g if t not in must_all]
    exp_amt = _estimate_and(M, exp_extra, overlap_data) if exp_extra else M
    exp_data = _build_rules(exp_groups)
    plans.append({
        "plan_name": "扩量型",
        "plan_type": "扩量",
        "logic_text": _fmt_logic(exp_groups, nm),
        "or_groups": exp_groups,
        "data": exp_data,
        "tags_used": [t for g in exp_groups for t in g],
        "expansion_type": "reduce_and_or_core_dim",
        "estimated_amount": exp_amt,
        "amount_precision": "estimated" if exp_amt != M else "exact",
        "notes": "在MUST基础上保留核心定向维度（如年龄+城市），不加消费力/职业等收窄强条件。比精准型覆盖广，比扩展型定向强。如需同维度OR追加标签（如加三线/加35-39岁），可在此基础上调整。"
    })

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(plans, f, ensure_ascii=False, indent=2)

    print(json.dumps({
        "ok": True,
        "plans": len(plans),
        "plan_names": [p["plan_name"] for p in plans],
        "out": args.out,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
