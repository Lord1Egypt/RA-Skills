"""dlt_compound_betting.py
多复式投注生成器 - 大乐透 (DLT)

支持以下复式类型:
  6+2, 6+3, 6+4
  7+2, 7+3, 7+4, 7+5
  8+2, 8+3, 8+4, 8+5
  9+2, 9+3, 9+4, 9+5

复式原理: 从N个前区候选中选5个号(产生C(N,5)注), 从M个后区候选中选2个号(产生C(M,2)注)
总注数 = C(N,5) × C(M,2)

示例:
  6+3 = 从6个前区候选选5个(C(6,5)=6注) × 从3个后区候选选2个(C(3,2)=3注) = 18注, 36元
  9+4 = 从9个前区候选选5个(C(9,5)=126注) × 从4个后区候选选2个(C(4,2)=6注) = 756注, 1512元
"""

from __future__ import annotations

from itertools import combinations
from math import comb
from typing import List, Tuple, Dict, Any
import random

FRONT_MAX = 35
BACK_MAX = 12

# ─────────────────────────────────────────────
# 工具函数
# ─────────────────────────────────────────────

def _sum5(nums: Tuple[int, ...]) -> int:
    return sum(nums)

def _odd_count(nums: Tuple[int, ...]) -> int:
    return sum(1 for n in nums if n % 2 == 1)

def _ac5(nums: Tuple[int, ...]) -> int:
    ac = 0
    s = sorted(nums)
    for i in range(1, len(s)):
        if s[i] - s[i - 1] > 1:
            ac += 1
    return ac

def _spread5(nums: Tuple[int, ...]) -> float:
    import math
    positions = [n / FRONT_MAX for n in nums]
    mean = sum(positions) / len(positions)
    return math.sqrt(sum((p - mean) ** 2 for p in positions))

def _consecutive5(nums: Tuple[int, ...]) -> int:
    count = 0
    s = sorted(nums)
    for i in range(1, len(s)):
        if s[i] - s[i - 1] == 1:
            count += 1
    return count

def _extract_features(combo: Tuple[Tuple[int, ...], Tuple[int, ...]]) -> Tuple:
    front = combo[0]
    return (_sum5(front), _odd_count(front), _ac5(front), int(_spread5(front) * 100), _consecutive5(front))

# ─────────────────────────────────────────────
# 1. 核心组合生成
# ─────────────────────────────────────────────

def generate_all_compound(
    front_pool: List[int], back_pool: List[int],
    front_compound: int, back_compound: int
) -> List[Tuple[Tuple[int, ...], Tuple[int, ...]]]:
    """生成指定复式类型的全部注单。

    复式原理: 从N个前区候选中选5个号(产生C(N,5)注),
             从M个后区候选中选2个号(产生C(M,2)注)
    总注数 = C(N,5) × C(M,2)

    Args:
        front_pool: 前区号码候选池
        back_pool: 后区号码候选池
        front_compound: 复式前区数 (即池中号码数量, 如6+3的6)
        back_compound: 复式后区数 (即池中号码数量, 如6+3的3)

    Returns:
        标准注单列表 [(5个前区号tuple, 2个后区号tuple), ...]
    """
    if len(front_pool) < front_compound:
        raise ValueError(f"前区候选池只有{len(front_pool)}个号码，不足以生成{front_compound}+{back_compound}（需要{front_compound}个）")
    if len(back_pool) < back_compound:
        raise ValueError(f"后区候选池只有{len(back_pool)}个号码，不足以生成{front_compound}+{back_compound}（需要{back_compound}个）")

    # 取前front_compound个作为复式池（从候选池头部取，不足则用全部）
    fp = sorted(front_pool[:front_compound])
    bp = sorted(back_pool[:back_compound])

    # 生成全部注单
    front_combos = list(combinations(fp, 5))
    back_combos = list(combinations(bp, 2))

    return [(fc, bc) for fc in front_combos for bc in back_combos]

def compound_info(front_compound: int, back_compound: int) -> Dict[str, Any]:
    """计算复式类型的基础信息"""
    return {
        "type": f"{front_compound}+{back_compound}",
        "front_pool_size": front_compound,
        "back_pool_size": back_compound,
        "front_bets": comb(front_compound, 5),
        "back_bets": comb(back_compound, 2),
        "total_bets": comb(front_compound, 5) * comb(back_compound, 2),
        "total_cost_yuan": comb(front_compound, 5) * comb(back_compound, 2) * 2,
    }

# ─────────────────────────────────────────────
# 2. 多样性筛选
# ─────────────────────────────────────────────

def filter_and_score(combos: List[Tuple[Tuple[int, ...], Tuple[int, ...]]]) -> List[Tuple]:
    """应用和值/奇偶/AC过滤"""
    filtered = []
    for fc, bc in combos:
        s = sum(fc)
        odd = sum(1 for n in fc if n % 2 == 1)
        ac = _ac5(fc)
        if 40 <= s <= 130 and 1 <= odd <= 4 and ac >= 3:
            filtered.append((fc, bc))
    return filtered

def select_diverse(
    combos: List[Tuple[Tuple[int, ...], Tuple[int, ...]]],
    target: int, seed: int = 42
) -> List[Tuple[Tuple[int, ...], Tuple[int, ...]]]:
    """贪心选择target个多样性组合"""
    if len(combos) <= target:
        return list(combos)

    random.seed(seed)
    data = list(combos)
    random.shuffle(data)

    features_all = [_extract_features(c) for c in data]
    selected: List[Tuple] = []
    used_features: List[Tuple] = []

    for _ in range(target):
        best_idx = 0
        best_score = -1

        for i, combo in enumerate(data):
            if combo in selected:
                continue
            feat = features_all[i]
            min_dist = min(
                abs(feat[0] - uf[0]) + abs(feat[2] - uf[2]) * 5
                for uf in used_features
            ) if used_features else 9999
            quality = min_dist + feat[2] * 8 + feat[3]
            if quality > best_score:
                best_score = quality
                best_idx = i

        selected.append(data[best_idx])
        used_features.append(features_all[best_idx])

    return selected

# ─────────────────────────────────────────────
# 3. 主预测接口
# ─────────────────────────────────────────────

ALL_COMPOUND_TYPES = [
    (6, 2), (6, 3), (6, 4),
    (7, 2), (7, 3), (7, 4), (7, 5),
    (8, 2), (8, 3), (8, 4), (8, 5),
    (9, 2), (9, 3), (9, 4), (9, 5),
]

def generate_compound_predictions(
    front_pool: List[int], back_pool: List[int],
    front_compound: int, back_compound: int,
    group_count: int = 5,
    apply_filters: bool = True
) -> Dict[str, Any]:
    """生成指定复式类型的预测组合"""
    all_combos = generate_all_compound(front_pool, back_pool, front_compound, back_compound)

    if apply_filters:
        filtered = filter_and_score(all_combos)
        if len(filtered) < group_count:
            filtered = all_combos
    else:
        filtered = all_combos

    selected = select_diverse(filtered, group_count)

    return {
        "compound_type": f"{front_compound}+{back_compound}",
        "info": compound_info(front_compound, back_compound),
        "total_generated": len(all_combos),
        "after_filter": len(filtered),
        "selected_count": len(selected),
        "combinations": [{"front": list(fc), "back": list(bc)} for fc, bc in selected],
        "front_pool_used": sorted(front_pool[:front_compound]),
        "back_pool_used": sorted(back_pool[:back_compound]),
    }

def generate_all_compound_types(
    front_pool: List[int], back_pool: List[int],
    compound_types: List[Tuple[int, int]] = None,
    groups_per_type: int = 3
) -> Dict[str, Any]:
    """为多种复式类型生成预测"""
    if compound_types is None:
        compound_types = [(6, 3), (7, 2), (8, 4)]

    results = {}
    for fc, bc in compound_types:
        key = f"{fc}+{bc}"
        try:
            results[key] = generate_compound_predictions(
                front_pool, back_pool, fc, bc,
                group_count=groups_per_type
            )
        except Exception as e:
            results[key] = {"error": str(e)}
    return results

def format_compound_report(
    report: Dict[str, Any], period: int,
    latest_draw: Dict = None
) -> str:
    """格式化预测报告"""
    lines = []
    lines.append(f"{'='*60}")
    lines.append(f"🌟 DLT 大乐透 第{period}期 多复式预测报告")
    lines.append(f"{'='*60}")

    if latest_draw:
        front = [int(latest_draw[f'front_{i}']) for i in range(1, 6)]
        back = [int(latest_draw[f'back_{i}']) for i in range(1, 3)]
        lines.append(f"上期开奖: {' '.join(f'{n:02d}' for n in front)} + {' '.join(f'{n:02d}' for n in back)}")
        lines.append("")

    total_cost = 0
    for ctype, data in report.items():
        if "error" in data:
            lines.append(f"💰 {ctype}: 错误 - {data['error']}")
            continue

        info = data["info"]
        lines.append(f"📋 {ctype} 复式 (前区{info['front_bets']}注×后区{info['back_bets']}注 = {info['total_bets']}注, {info['total_cost_yuan']}元)")
        lines.append(f"   前区候选({info['front_pool_size']}个): {' '.join(f'{n:02d}' for n in data['front_pool_used'])}")
        lines.append(f"   后区候选({info['back_pool_size']}个): {' '.join(f'{n:02d}' for n in data['back_pool_used'])}")
        lines.append(f"   {data['total_generated']}注 → {data['after_filter']}注(过滤) → {data['selected_count']}组推荐")

        for i, combo in enumerate(data["combinations"], 1):
            front_str = " ".join(f"{n:02d}" for n in combo["front"])
            back_str = " ".join(f"{n:02d}" for n in combo["back"])
            lines.append(f"     方案{i}: 前区[{front_str}] 后区[{back_str}]")
        total_cost += info['total_cost_yuan']
        lines.append("")

    lines.append(f"💰 合计投入: {total_cost}元")
    lines.append(f"\n⚠️  仅供参考娱乐，请理性投注！")
    return "\n".join(lines)

# ─────────────────────────────────────────────
# 4. 入口
# ─────────────────────────────────────────────

if __name__ == "__main__":
    front_pool = [3, 5, 8, 11, 12, 15, 19, 22, 25, 26, 27, 30, 31, 32, 33]
    back_pool = [1, 3, 5, 7, 8, 10, 11]

    report = generate_all_compound_types(
        front_pool, back_pool,
        compound_types=[(6, 3), (7, 2), (6, 4), (8, 4), (7, 5)],
        groups_per_type=3
    )
    print(format_compound_report(report, 26035))
