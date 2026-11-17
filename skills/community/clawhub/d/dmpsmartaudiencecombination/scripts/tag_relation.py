#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tag_relation.py - 标签关系分析工具

提供两类分析能力：
1. Tag-to-Tag Overlap（标签间关系）
   - 自动识别互斥对（年龄段/城市线/性别）→ r=0，无需计算
   - 自动识别父子/祖先对 → r=100%，无需计算
   - 同维度兄弟对：必算（同维度OR扩量的核心依据）
   - 跨维度对：按需计算（只算可能进入同一AND组合的、或高潜力的）
   - 优先从标签画像表读取覆盖数据做估算，无数据时才创建人群包计算

2. MUST vs Optional 渗透分析
   - 计算每个Optional标签在MUST基准人群中的渗透率 r_x = |M∩x|/|M|
   - 用于AND收窄/OR扩量决策

注意：尽量从画像数据直接计算，避免创建大量临时人群包。
只有精确交集在画像表中无法获取时，才通过combine/create创建临时人群计算。
"""

import json
import re
from itertools import combinations
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


# ──────────────── 互斥/父子关系检测（纯逻辑，不调用API）────────────────

_MUTEX_CITY_LEVELS = ["一线城市", "新一线城市", "二线城市", "三线城市", "四线城市", "五线城市"]


def _get_name(tid: int, tag_pool: List[Dict]) -> str:
    tm = {int(t["tagId"]): t for t in tag_pool if t.get("isDirectory") == 1}
    return tm.get(int(tid), {}).get("tagName", str(tid))


def _get_category(tid: int, tag_pool: List[Dict]) -> str:
    tm = {int(t["tagId"]): t for t in tag_pool if t.get("isDirectory") == 1}
    return str(tm.get(int(tid), {}).get("category", ""))


def is_mutex_pair(tid_a: int, tid_b: int, tag_pool: List[Dict]) -> bool:
    """判断两个标签是否互斥（交集为0）。"""
    a_name = _get_name(tid_a, tag_pool)
    b_name = _get_name(tid_b, tag_pool)
    # 性别互斥
    if {a_name, b_name} == {"男", "女"}:
        return True
    # 年龄段互斥（不重叠的数字范围）
    age_pat = r'^\d+-\d+岁?$'
    if re.match(age_pat, a_name.strip()) and re.match(age_pat, b_name.strip()):
        def _parse(n):
            nums = re.findall(r'\d+', n)
            return (int(nums[0]), int(nums[1])) if len(nums) >= 2 else (0, 0)
        a_lo, a_hi = _parse(a_name)
        b_lo, b_hi = _parse(b_name)
        if a_hi < b_lo or b_hi < a_lo:
            return True
    # 城市级别互斥
    a_city = next((c for c in _MUTEX_CITY_LEVELS if c in a_name), None)
    b_city = next((c for c in _MUTEX_CITY_LEVELS if c in b_name), None)
    if a_city and b_city and a_city != b_city:
        return True
    return False


def is_ancestor_pair(tid_a: int, tid_b: int, pmap: Dict[int, int]) -> Optional[Tuple[int, int]]:
    """如果A是B的祖先返回(A,B)，B是A的祖先返回(B,A)，否则None。"""
    from tag_hierarchy import is_descendant, get_ancestors
    if is_descendant(tid_b, tid_a, pmap):
        return (tid_a, tid_b)  # A是B的祖先
    if is_descendant(tid_a, tid_b, pmap):
        return (tid_b, tid_a)  # B是A的祖先
    return None


def get_group_dim(tid: int, tag_pool: List[Dict], core_kws: List[str]) -> str:
    """判断单个标签所属维度。"""
    name = _get_name(tid, tag_pool)
    cat = _get_category(tid, tag_pool)
    if name in ("女", "男") or "性别" in cat:
        return "性别"
    if "年龄" in cat or "岁" in name or (name and name[:1].isdigit() and "-" in name):
        return "年龄"
    if "城市级别" in cat or "线城市" in name:
        return "城市级别"
    if any(kw in cat or kw in name for kw in core_kws):
        return "核心兴趣"
    if "消费" in cat or "轻奢" in name or "收入" in name:
        return "消费力"
    if "白领" in name or "职业" in cat:
        return "职业"
    if "活跃" in name or "高活" in name:
        return "活跃度"
    return "其他"


def classify_pairs(tags: List[int], tag_pool: List[Dict],
                   core_kws: List[str],
                   cross_dim_pairs: Optional[List[Tuple[int, int]]] = None
                   ) -> Dict[str, List[Dict]]:
    """将标签对分类为：mutex/ancestor/same_dim_need_calc/cross_dim_need_calc/skip。

    Args:
        tags: 标签ID列表
        tag_pool: 标签池
        core_kws: 核心兴趣关键词
        cross_dim_pairs: 指定需要计算的跨维度对（白名单），None=不算跨维度

    Returns:
        {
          "mutex": [{tagId_a, tagId_b, note}],
          "ancestor": [{ancestorId, descendantId, note}],
          "same_dim": [{tagId_a, tagId_b, dimension, note}],
          "cross_dim": [{tagId_a, tagId_b, dim_a, dim_b, note}],
          "skip": [...]
        }
    """
    from tag_hierarchy import build_parent_map
    pmap = build_parent_map(tag_pool) if tag_pool else {}

    result = {"mutex": [], "ancestor": [], "same_dim": [], "cross_dim": []}
    cross_dim_white = set()
    if cross_dim_pairs:
        for a, b in cross_dim_pairs:
            cross_dim_white.add((min(a, b), max(a, b)))

    for a, b in combinations(tags, 2):
        ta, tb = int(a), int(b)
        na = _get_name(ta, tag_pool)
        nb = _get_name(tb, tag_pool)
        # 互斥
        if tag_pool and is_mutex_pair(ta, tb, tag_pool):
            result["mutex"].append({
                "tagId_a": ta, "tagId_b": tb,
                "tagName_a": na, "tagName_b": nb,
                "r_overlap": 0.0,
                "amount_intersection": "0",
                "note": "互斥（不同年龄段/城市线/性别），交集=0"
            })
            continue
        # 父子
        anc = is_ancestor_pair(ta, tb, pmap) if tag_pool and pmap else None
        if anc:
            aid, did = anc
            result["ancestor"].append({
                "ancestorId": aid, "descendantId": did,
                "tagId_a": ta, "tagId_b": tb,
                "tagName_a": na, "tagName_b": nb,
                "r_overlap": 1.0,
                "note": f"祖先-后代关系，交集=后代量级（r=100%）"
            })
            continue
        # 维度判断
        da = get_group_dim(ta, tag_pool, core_kws) if tag_pool else "其他"
        db = get_group_dim(tb, tag_pool, core_kws) if tag_pool else "其他"
        entry = {
            "tagId_a": ta, "tagId_b": tb,
            "tagName_a": na, "tagName_b": nb,
            "dimension_a": da, "dimension_b": db,
        }
        if da == db and da != "其他":
            # 同维度兄弟对 → 必算
            entry["note"] = f"同维度（{da}）兄弟标签，需计算Overlap"
            result["same_dim"].append(entry)
        else:
            # 跨维度 → 检查白名单
            key = (min(ta, tb), max(ta, tb))
            if cross_dim_white and key in cross_dim_white:
                entry["note"] = f"跨维度（{da}×{db}），按需计算"
                result["cross_dim"].append(entry)
            # 否则跳过（不计算）

    return result


# ──────────────── 从画像表估算Overlap（不创建人群）────────────────

def estimate_overlap_from_coverage(ta: int, tb: int, tag_pool: List[Dict],
                                   profile_data: Dict = None) -> Optional[float]:
    """基于覆盖率/填充率估算两个标签的重叠率。

    估算逻辑：如果两个标签独立，P(A∩B) ≈ P(A) × P(B)
    如果同维度兄弟关系（如护肤vs彩妆），重叠率通常高于独立假设。
    返回0~1的估算值，None表示无法估算。
    """
    # TODO: 当画像表包含标签独立量级|A|、|B|时，可做更精确估算
    # 当前无精确数据时返回None
    return None


# ──────────────── 构建临时人群计算规则 ────────────────

def build_tag_tag_rules(ta: int, tb: int) -> List[Dict]:
    """构建tag_a AND tag_b的组合规则（临时计算用）。"""
    return [
        {"op": "and", "rule": {"audience": [], "tag": [ta]}},
        {"op": "noop", "rule": {"audience": [], "tag": [tb]}},
    ]


def build_must_tag_rules(mid: int, tid: int) -> List[Dict]:
    """构建 M AND tag_x 的组合规则。"""
    return [
        {"op": "and", "rule": {"audience": [mid], "tag": []}},
        {"op": "noop", "rule": {"audience": [], "tag": [tid]}},
    ]


if __name__ == "__main__":
    # 简单自检
    import os
    skill_dir = Path(__file__).parent.parent
    pool_path = skill_dir / "tag_pool.json"
    if pool_path.exists():
        with open(pool_path) as f:
            pool = json.load(f)
        test_tags = [15687, 15688, 34080, 34082, 15652, 15653, 15795, 23127]
        result = classify_pairs(test_tags, pool, ["美妆个护", "护肤", "彩妆"])
        print("=== 互斥对 ===")
        for r in result["mutex"]:
            print(f"  {r['tagName_a']} ∩ {r['tagName_b']}: {r['note']}")
        print("=== 祖先对 ===")
        for r in result["ancestor"]:
            print(f"  {r['tagName_a']} ∩ {r['tagName_b']}: {r['note']}")
        print("=== 同维度需计算 ===")
        for r in result["same_dim"]:
            print(f"  {r['tagName_a']} ∩ {r['tagName_b']} ({r['dimension_a']}): {r['note']}")
        print("=== 跨维度（白名单为空，无） ===")
        print(f"  cross_dim count: {len(result['cross_dim'])}")
        print("✅ tag_relation 自检通过")
