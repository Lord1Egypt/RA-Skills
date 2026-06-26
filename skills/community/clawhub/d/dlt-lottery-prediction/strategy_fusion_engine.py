#!/usr/bin/env python3
"""
DLT多维度策略融合引擎 (Strategy Fusion Engine)
基于13维特征的全新融合架构设计

核心设计思路:
- 每组方案综合多个维度（而非单一池）
- 每组有明确的硬约束+软约束
- 支持多种融合算法
- 最终通过多策略协同评分选号

作者: AI Assistant
日期: 2026-04-06
"""

import numpy as np
import random
from typing import List, Dict, Tuple, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict


# ============================================================
# 1. 数据结构定义
# ============================================================

class FusionAlgorithm(Enum):
    WEIGHTED_VOTING = "weighted_voting"
    BAYESIAN_FUSION = "bayesian_fusion"
    ML_PROBABILITY_FUSION = "ml_probability_fusion"
    GENETIC_OPTIMIZATION = "genetic_optimization"
    GAME_THEORY_EQUILIBRIUM = "game_theory"


@dataclass
class DimensionConfig:
    name: str
    weight: float
    scoring_func: Callable
    direction: str = "higher"


@dataclass
class HardConstraints:
    sum_range: Tuple[int, int] = (70, 120)
    parity_ratios: List[str] = None
    span_range: Tuple[int, int] = (20, 32)
    ac_min: int = 6
    zone_required: bool = True
    consecutive_allowed: Tuple[int, int] = (0, 2)

    def __post_init__(self):
        if self.parity_ratios is None:
            self.parity_ratios = ['3:2', '2:3']


@dataclass
class SoftConstraints:
    sum_prefer: Tuple[int, int] = (85, 105)
    parity_prefer: str = "3:2"
    span_prefer: Tuple[int, int] = (24, 28)
    ac_prefer: int = 8
    cooc_boost: bool = True
    zone_prefer: str = "221"


@dataclass
class GroupStrategy:
    group_id: int
    name: str
    description: str
    dimensions: List[DimensionConfig]
    hard_constraints: HardConstraints
    soft_constraints: SoftConstraints
    fusion_algorithm: FusionAlgorithm
    ml_model_weight: float = 0.0


@dataclass
class ScoredCandidate:
    front: List[int]
    back: List[int]
    total_score: float = 0.0
    dimension_scores: Dict[str, float] = field(default_factory=dict)
    constraint_violations: List[str] = field(default_factory=list)
    group_id: int = 0
    strategy_name: str = ""


# ============================================================
# 2. 特征提取器
# ============================================================

class DLTFeatureExtractor:
    """DLT 13维特征提取器"""

    FRONT_PRIMES = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31}
    BACK_PRIMES = {2, 3, 5, 7, 11}

    def __init__(self, draws: List[Tuple[List[int], List[int]]], window: int = 30):
        self.draws = draws
        self.window = window
        self.n_front = 35
        self.n_back = 12
        self._compute_statistics()

    def _compute_statistics(self):
        recent = self.draws[-self.window:]

        self.front_freq = defaultdict(int)
        self.front_missing = {}
        self.front_cooc = np.zeros((self.n_front + 1, self.n_front + 1))
        self.back_freq = defaultdict(int)
        self.back_missing = {}
        self.front_trend = {}
        self.back_trend = {}

        for front, _ in recent:
            for n in front:
                self.front_freq[n] += 1

        for n in range(1, self.n_front + 1):
            m = 0
            for front, _ in reversed(recent):
                if n in front:
                    break
                m += 1
            self.front_missing[n] = m

        for front, _ in recent:
            for i, n1 in enumerate(front):
                for n2 in front[i+1:]:
                    self.front_cooc[n1, n2] += 1
                    self.front_cooc[n2, n1] += 1

        for _, back in recent:
            for n in back:
                self.back_freq[n] += 1

        for n in range(1, self.n_back + 1):
            m = 0
            for _, back in reversed(recent):
                if n in back:
                    break
                m += 1
            self.back_missing[n] = m

        recent5 = self.draws[-5:]
        recent15 = self.draws[-15:]

        for n in range(1, self.n_front + 1):
            r5 = sum(1 for f, _ in recent5 if n in f) / max(len(recent5), 1)
            r15 = sum(1 for f, _ in recent15 if n in f) / max(len(recent15), 1)
            self.front_trend[n] = r5 - r15

        for n in range(1, self.n_back + 1):
            r5 = sum(1 for _, b in recent5 if n in b) / max(len(recent5), 1)
            r15 = sum(1 for _, b in recent15 if n in b) / max(len(recent15), 1)
            self.back_trend[n] = r5 - r15

    def get_hot_score(self, num: int, zone: str = 'front') -> float:
        freq = self.front_freq if zone == 'front' else self.back_freq
        total = len(self.draws[-self.window:]) if self.draws else 1
        return freq.get(num, 0) / max(total, 1)

    def get_repeat_score(self, num: int, zone: str = 'front') -> float:
        if not self.draws:
            return 0.0
        last = self.draws[-1]
        nums = last[0] if zone == 'front' else last[1]
        return 1.0 if num in nums else 0.0

    def get_adjacent_score(self, num: int, zone: str = 'front') -> float:
        if not self.draws:
            return 0.0
        last = self.draws[-1]
        nums = set(last[0] if zone == 'front' else last[1])
        return 1.0 if (num - 1) in nums or (num + 1) in nums else 0.0

    def get_missing_score(self, num: int, zone: str = 'front') -> float:
        miss = self.front_missing.get(num, self.window) if zone == 'front' \
               else self.back_missing.get(num, self.window)
        return min(miss / (self.window * 2), 1.0)

    def get_trend_score(self, num: int, zone: str = 'front') -> float:
        trend = self.front_trend.get(num, 0.0) if zone == 'front' \
                else self.back_trend.get(num, 0.0)
        return (trend + 1.0) / 2.0

    def get_prime_score(self, num: int, zone: str = 'front') -> float:
        primes = self.FRONT_PRIMES if zone == 'front' else self.BACK_PRIMES
        return 1.0 if num in primes else 0.0

    def get_cooc_score(self, num: int, zone: str = 'front',
                       selected: List[int] = None) -> float:
        if zone != 'front' or not selected:
            return 0.5
        cooc_sum = sum(self.front_cooc[num, n] for n in selected if n != num)
        return min(cooc_sum / 50.0, 1.0)


# ============================================================
# 3. 约束检查器
# ============================================================

class ConstraintChecker:
    FRONT_PRIMES = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31}

    def check_hard_constraints(self, combo: List[int],
                               hc: HardConstraints) -> Tuple[bool, List[str]]:
        violations = []
        s = sum(combo)
        if not (hc.sum_range[0] <= s <= hc.sum_range[1]):
            violations.append(f"sum={s} not in {hc.sum_range}")
        odd = sum(1 for n in combo if n % 2 == 1)
        ratio = f"{odd}:{len(combo)-odd}"
        if hc.parity_ratios and ratio not in hc.parity_ratios:
            violations.append(f"parity={ratio} not allowed")
        span = max(combo) - min(combo)
        if not (hc.span_range[0] <= span <= hc.span_range[1]):
            violations.append(f"span={span} not in {hc.span_range}")
        ac = self._compute_ac(combo)
        if ac < hc.ac_min:
            violations.append(f"ac={ac}<{hc.ac_min}")
        if hc.zone_required:
            zones = self._compute_zone(combo)
            if 0 in zones:
                violations.append(f"zone={zones} has empty")
        consec = self._count_consecutive(combo)
        if not (hc.consecutive_allowed[0] <= consec <= hc.consecutive_allowed[1]):
            violations.append(f"consecutive={consec} not allowed")
        return len(violations) == 0, violations

    def score_soft_constraints(self, combo: List[int], sc: SoftConstraints) -> float:
        score = 0.0
        s = sum(combo)
        sm, sM = sc.sum_prefer
        if sm <= s <= sM:
            mid = (sm + sM) / 2
            score += 1.0 - abs(s - mid) / (sM - mid + 1)
        sp, sP = sc.span_prefer
        span = max(combo) - min(combo)
        if sp <= span <= sP:
            mid = (sp + sP) / 2
            score += 1.0 - abs(span - mid) / (sP - mid + 1)
        ac = self._compute_ac(combo)
        score += 1.0 if ac == sc.ac_prefer else (0.5 if ac >= sc.ac_prefer - 1 else 0.0)
        zones = self._compute_zone(combo)
        zstr = ''.join(map(str, zones))
        score += 1.0 if zstr == sc.zone_prefer else (0.0 if 0 in zones else 0.5)
        pc = sum(1 for n in combo if n in self.FRONT_PRIMES)
        pr = pc / len(combo)
        score += 1.0 if 0.2 <= pr <= 0.5 else (0.3 if pr > 0 else 0.0)
        if sc.cooc_boost:
            score += 0.15
        return min(score / 5.0, 1.0)

    def _compute_ac(self, combo: List[int]) -> int:
        if len(combo) < 2:
            return 0
        diffs = [abs(combo[j]-combo[i]) for i in range(len(combo)) for j in range(i+1, len(combo))]
        return len(set(diffs))

    def _compute_zone(self, combo: List[int], max_num: int = 35) -> List[int]:
        z1 = sum(1 for n in combo if n <= 11)
        z2 = sum(1 for n in combo if 12 <= n <= 23)
        z3 = sum(1 for n in combo if 24 <= n <= 35)
        return [z1, z2, z3]

    def _count_consecutive(self, combo: List[int]) -> int:
        if len(combo) < 2:
            return 0
        sc = sorted(combo)
        groups = 0
        i = 0
        while i < len(sc) - 1:
            if sc[i+1] == sc[i] + 1:
                groups += 1
                while i < len(sc) - 1 and sc[i+1] == sc[i] + 1:
                    i += 1
            i += 1
        return groups


# ============================================================
# 4. 五组策略定义
# ============================================================

def build_group_strategies(fe: DLTFeatureExtractor) -> List[GroupStrategy]:
    strategies = []

    # --- 组1: 热号重号均衡 ---
    dim1 = [
        DimensionConfig('hot', 0.30, lambda n, ctx: fe.get_hot_score(n, 'front'), 'higher'),
        DimensionConfig('repeat', 0.25, lambda n, ctx: fe.get_repeat_score(n, 'front'), 'higher'),
        DimensionConfig('odd_even', 0.20, lambda n, ctx: 0.5, 'higher'),
        DimensionConfig('zone_small', 0.15, lambda n, ctx: 1.0 if n <= 18 else 0.3, 'higher'),
        DimensionConfig('missing', 0.10, lambda n, ctx: fe.get_missing_score(n, 'front'), 'higher'),
    ]
    strategies.append(GroupStrategy(
        group_id=1, name="热号重号均衡", description="热号+重号+奇偶均衡+小三区+遗漏",
        dimensions=dim1,
        hard_constraints=HardConstraints(sum_range=(80,110), parity_ratios=['3:2','2:3'],
            span_range=(20,32), ac_min=6, zone_required=True, consecutive_allowed=(1,2)),
        soft_constraints=SoftConstraints(sum_prefer=(88,102), parity_prefer='3:2',
            span_prefer=(24,28), ac_prefer=8, cooc_boost=True, zone_prefer='221'),
        fusion_algorithm=FusionAlgorithm.WEIGHTED_VOTING, ml_model_weight=0.0
    ))

    # --- 组2: 冷号遗漏反转 ---
    dim2 = [
        DimensionConfig('missing', 0.35, lambda n, ctx: fe.get_missing_score(n, 'front'), 'higher'),
        DimensionConfig('cold', 0.25, lambda n, ctx: 1.0 - fe.get_hot_score(n, 'front'), 'higher'),
        DimensionConfig('trend', 0.15, lambda n, ctx: fe.get_trend_score(n, 'front'), 'higher'),
        DimensionConfig('prime', 0.15, lambda n, ctx: fe.get_prime_score(n, 'front'), 'higher'),
        DimensionConfig('cooc', 0.10, lambda n, ctx: fe.get_cooc_score(n,'front',ctx.get('selected',[]))
                        if ctx.get('selected') else 0.5, 'higher'),
    ]
    strategies.append(GroupStrategy(
        group_id=2, name="冷号遗漏反转", description="遗漏+冷号+趋势反弹+质数+共现",
        dimensions=dim2,
        hard_constraints=HardConstraints(sum_range=(75,115), parity_ratios=['3:2','2:3','4:1'],
            span_range=(18,34), ac_min=5, zone_required=True, consecutive_allowed=(0,2)),
        soft_constraints=SoftConstraints(sum_prefer=(80,100), parity_prefer='3:2',
            span_prefer=(22,30), ac_prefer=7, cooc_boost=True, zone_prefer='212'),
        fusion_algorithm=FusionAlgorithm.BAYESIAN_FUSION, ml_model_weight=0.2
    ))

    # --- 组3: 趋势动量策略 ---
    dim3 = [
        DimensionConfig('trend', 0.35, lambda n, ctx: fe.get_trend_score(n, 'front'), 'higher'),
        DimensionConfig('repeat', 0.20, lambda n, ctx: fe.get_repeat_score(n, 'front'), 'higher'),
        DimensionConfig('adjacent', 0.20, lambda n, ctx: fe.get_adjacent_score(n, 'front'), 'higher'),
        DimensionConfig('hot', 0.15, lambda n, ctx: fe.get_hot_score(n, 'front'), 'higher'),
        DimensionConfig('missing', 0.10, lambda n, ctx: fe.get_missing_score(n, 'front'), 'higher'),
    ]
    strategies.append(GroupStrategy(
        group_id=3, name="趋势动量策略", description="趋势+重号+临号共振+热号+遗漏",
        dimensions=dim3,
        hard_constraints=HardConstraints(sum_range=(85,115), parity_ratios=['3:2','2:3','4:1','1:4'],
            span_range=(20,30), ac_min=6, zone_required=True, consecutive_allowed=(0,3)),
        soft_constraints=SoftConstraints(sum_prefer=(90,108), parity_prefer='3:2',
            span_prefer=(24,28), ac_prefer=8, cooc_boost=True, zone_prefer='122'),
        fusion_algorithm=FusionAlgorithm.GAME_THEORY_EQUILIBRIUM, ml_model_weight=0.15
    ))

    # --- 组4: 博弈论冷门策略 ---
    dim4 = [
        DimensionConfig('cold', 0.30, lambda n, ctx: 1.0 - fe.get_hot_score(n, 'front'), 'higher'),
        DimensionConfig('prime', 0.25, lambda n, ctx: fe.get_prime_score(n, 'front'), 'higher'),
        DimensionConfig('high_range', 0.20, lambda n, ctx: 1.0 if n >= 28 else 0.2, 'higher'),
        DimensionConfig('missing', 0.15, lambda n, ctx: fe.get_missing_score(n, 'front'), 'higher'),
        DimensionConfig('cooc', 0.10, lambda n, ctx: fe.get_cooc_score(n,'front',ctx.get('selected',[]))
                        if ctx.get('selected') else 0.5, 'higher'),
    ]
    strategies.append(GroupStrategy(
        group_id=4, name="博弈论冷门策略", description="冷号+质数+高号区间+遗漏+共现规避",
        dimensions=dim4,
        hard_constraints=HardConstraints(sum_range=(90,125), parity_ratios=['3:2','2:3','4:1','1:4','5:0','0:5'],
            span_range=(25,34), ac_min=5, zone_required=False, consecutive_allowed=(0,1)),
        soft_constraints=SoftConstraints(sum_prefer=(95,115), parity_prefer='4:1',
            span_prefer=(28,32), ac_prefer=9, cooc_boost=False, zone_prefer='113'),
        fusion_algorithm=FusionAlgorithm.GAME_THEORY_EQUILIBRIUM, ml_model_weight=0.25
    ))

    # --- 组5: ML概率融合策略 ---
    dim5 = [
        DimensionConfig('hot', 0.20, lambda n, ctx: fe.get_hot_score(n, 'front'), 'higher'),
        DimensionConfig('missing', 0.20, lambda n, ctx: fe.get_missing_score(n, 'front'), 'higher'),
        DimensionConfig('trend', 0.20, lambda n, ctx: fe.get_trend_score(n, 'front'), 'higher'),
        DimensionConfig('repeat', 0.20, lambda n, ctx: fe.get_repeat_score(n, 'front'), 'higher'),
        DimensionConfig('cooc', 0.20, lambda n, ctx: fe.get_cooc_score(n,'front',ctx.get('selected',[]))
                        if ctx.get('selected') else 0.5, 'higher'),
    ]
    strategies.append(GroupStrategy(
        group_id=5, name="ML概率融合策略", description="均衡五维+ML概率加权+动态校准",
        dimensions=dim5,
        hard_constraints=HardConstraints(sum_range=(75,120), parity_ratios=['3:2','2:3','4:1','1:4'],
            span_range=(18,32), ac_min=6, zone_required=True, consecutive_allowed=(0,2)),
        soft_constraints=SoftConstraints(sum_prefer=(85,105), parity_prefer='3:2',
            span_prefer=(24,28), ac_prefer=8, cooc_boost=True, zone_prefer='221'),
        fusion_algorithm=FusionAlgorithm.ML_PROBABILITY_FUSION, ml_model_weight=0.4
    ))

    return strategies


# ============================================================
# 5. 融合算法运行器
# ============================================================

class FusionAlgorithmRunner:
    def __init__(self, fe: DLTFeatureExtractor, cc: ConstraintChecker):
        self.fe = fe
        self.cc = cc

    def _score_number(self, num: int, strategy: GroupStrategy,
                      zone: str, selected: List[int] = None) -> float:
        selected = selected or []
        context = {'selected': selected}
        total = 0.0
        for dim in strategy.dimensions:
            s = dim.scoring_func(num, context)
            if dim.direction == 'lower':
                s = 1.0 - s
            total += s * dim.weight
        return total

    def weighted_voting(self, strategy: GroupStrategy, zone: str = 'front',
                        n_select: int = 5, selected: List[int] = None) -> List[Tuple[int, float]]:
        max_num = self.fe.n_front if zone == 'front' else self.fe.n_back
        selected = selected or []
        scores = {}
        for num in range(1, max_num + 1):
            scores[num] = self._score_number(num, strategy, zone, selected)
        return sorted(scores.items(), key=lambda x: x[1], reverse=True)[:n_select]

    def bayesian_fusion(self, strategy: GroupStrategy, zone: str = 'front',
                        n_select: int = 5, selected: List[int] = None) -> List[Tuple[int, float]]:
        max_num = self.fe.n_front if zone == 'front' else self.fe.n_back
        selected = selected or []
        n_hist = len(self.fe.draws)
        results = []
        for num in range(1, max_num + 1):
            context = {'selected': selected}
            prior = sum(dim.scoring_func(num, context) * dim.weight
                        for dim in strategy.dimensions)
            freq = self.fe.front_freq.get(num, 0) if zone == 'front' \
                   else self.fe.back_freq.get(num, 0)
            alpha, beta = 0.5 + freq, 0.5 + n_hist - freq
            likelihood = alpha / (alpha + beta)
            ml_w = strategy.ml_model_weight
            posterior = (prior ** max(ml_w, 0.01)) * (likelihood ** (1 - max(ml_w, 0.01)))
            miss = self.fe.front_missing.get(num, n_hist) if zone == 'front' \
                   else self.fe.back_missing.get(num, n_hist)
            ma = (0.5 + miss) / (0.5 + miss + 0.5 + n_hist)
            final = posterior * (0.7 + 0.3 * ma)
            results.append((num, final))
        return sorted(results, key=lambda x: x[1], reverse=True)[:n_select]

    def game_theory_fusion(self, strategy: GroupStrategy, zone: str = 'front',
                           n_select: int = 5, selected: List[int] = None) -> List[Tuple[int, float]]:
        max_num = self.fe.n_front if zone == 'front' else self.fe.n_back
        selected = selected or []
        popular = set(range(1, 11)) | {10, 20, 30}
        birthday = set(range(1, 13))
        results = []
        for num in range(1, max_num + 1):
            base = self._score_number(num, strategy, zone, selected)
            adjust = 0.0
            if num not in popular:
                adjust += 0.15
            if num not in birthday:
                adjust += 0.05
            if zone == 'front' and num >= 28:
                adjust += 0.10
            miss = self.fe.front_missing.get(num, 0) if zone == 'front' \
                   else self.fe.back_missing.get(num, 0)
            if miss > 15:
                adjust += 0.10
            results.append((num, min(base + adjust, 1.0)))
        return sorted(results, key=lambda x: x[1], reverse=True)[:n_select]

    def run(self, strategy: GroupStrategy, zone: str,
            n_select: int, selected: List[int] = None) -> List[Tuple[int, float]]:
        if strategy.fusion_algorithm == FusionAlgorithm.BAYESIAN_FUSION:
            return self.bayesian_fusion(strategy, zone, n_select, selected)
        elif strategy.fusion_algorithm == FusionAlgorithm.GAME_THEORY_EQUILIBRIUM:
            return self.game_theory_fusion(strategy, zone, n_select, selected)
        else:
            return self.weighted_voting(strategy, zone, n_select, selected)


# ============================================================
# 6. 候选生成器
# ============================================================

class CandidateGenerator:
    def __init__(self, fe: DLTFeatureExtractor, cc: ConstraintChecker, fr: FusionAlgorithmRunner):
        self.fe = fe
        self.cc = cc
        self.fr = fr

    def _generate_front(self, strategy: GroupStrategy, n: int = 5) -> List[int]:
        selected = []
        top_candidates = self.fr.run(strategy, 'front', n * 3, selected)
        for num, _ in top_candidates:
            if num not in selected:
                selected.append(num)
                if len(selected) >= n:
                    break
        return sorted(selected[:n])

    def _generate_back(self, strategy: GroupStrategy, n: int = 2) -> List[int]:
        selected = []
        top_candidates = self.fr.run(strategy, 'back', n * 3, selected)
        for num, _ in top_candidates:
            if num not in selected:
                selected.append(num)
                if len(selected) >= n:
                    break
        return sorted(selected[:n])

    def generate_candidates(self, strategy: GroupStrategy,
                            n_front: int = 5, n_back: int = 2,
                            max_attempts: int = 80) -> List[ScoredCandidate]:
        candidates = []
        for _ in range(max_attempts):
            front = self._generate_front(strategy, n_front)
            back = self._generate_back(strategy, n_back)
            if len(front) != n_front or len(back) != n_back:
                continue
            is_valid, violations = self.cc.check_hard_constraints(front, strategy.hard_constraints)
            soft_score = self.cc.score_soft_constraints(front, strategy.soft_constraints)
            dim_scores = {}
            for dim in strategy.dimensions:
                vals = [dim.scoring_func(n, {'selected': front}) for n in front]
                dim_scores[dim.name] = float(np.mean(vals))
            base = sum(dim_scores.get(d.name, 0.5) * d.weight for d in strategy.dimensions)
            total = base * (0.6 + 0.4 * soft_score)
            back_top = self.fr.run(strategy, 'back', 1, [])[0][1] if self.fr.run(strategy, 'back', 1, []) else 0.5
            total = total * 0.85 + back_top * 0.15
            if is_valid:
                candidates.append(ScoredCandidate(
                    front=sorted(front), back=sorted(back),
                    total_score=total, dimension_scores=dim_scores,
                    constraint_violations=violations,
                    group_id=strategy.group_id, strategy_name=strategy.name
                ))
            if len(candidates) >= 30:
                break
        return candidates


# ============================================================
# 7. 主融合引擎
# ============================================================

class StrategyFusionEngine:
    """
    多维度策略融合引擎

    工作流程:
    1. 初始化: 加载历史数据, 构建特征提取器
    2. 策略构建: 为5组定义不同的多维度融合策略
    3. 候选生成: 每组策略独立生成候选
    4. 约束过滤: 硬约束过滤 + 软约束评分
    5. 全局排序: 多维度综合评分排序
    6. 输出: 最终推荐的号码组合
    """

    def __init__(self, draws: List[Tuple[List[int], List[int]]], n_groups: int = 5):
        self.draws = draws
        self.n_groups = n_groups
        self.fe = DLTFeatureExtractor(draws)
        self.cc = ConstraintChecker()
        self.fr = FusionAlgorithmRunner(self.fe, self.cc)
        self.cg = CandidateGenerator(self.fe, self.cc, self.fr)
        self.strategies = build_group_strategies(self.fe)
        print(f"[SFE] 初始化完成 | 历史{len(draws)}期 | {n_groups}组策略")

    def generate_group_1(self, n_front=5, n_back=2):
        """热号重号均衡策略: 热号30%+重号25%+奇偶均衡20%+小三区15%+遗漏10%, 加权投票"""
        candidates = self.cg.generate_candidates(self.strategies[0], n_front, n_back)
        candidates.sort(key=lambda x: x.total_score, reverse=True)
        return candidates

    def generate_group_2(self, n_front=5, n_back=2):
        """冷号遗漏反转策略: 遗漏35%+冷号25%+趋势反弹15%+质数15%+共现10%, 贝叶斯融合"""
        candidates = self.cg.generate_candidates(self.strategies[1], n_front, n_back)
        candidates.sort(key=lambda x: x.total_score, reverse=True)
        return candidates

    def generate_group_3(self, n_front=5, n_back=2):
        """趋势动量策略: 趋势35%+重号20%+临号共振20%+热号15%+遗漏10%, 博弈论均衡"""
        candidates = self.cg.generate_candidates(self.strategies[2], n_front, n_back)
        candidates.sort(key=lambda x: x.total_score, reverse=True)
        return candidates

    def generate_group_4(self, n_front=5, n_back=2):
        """博弈论冷门策略: 冷号30%+质数25%+高号区间20%+遗漏15%+共现规避10%, 博弈论均衡"""
        candidates = self.cg.generate_candidates(self.strategies[3], n_front, n_back)
        candidates.sort(key=lambda x: x.total_score, reverse=True)
        return candidates

    def generate_group_5(self, n_front=5, n_back=2):
        """ML概率融合策略: 均衡五维(各20%), ML概率融合"""
        candidates = self.cg.generate_candidates(self.strategies[4], n_front, n_back)
        candidates.sort(key=lambda x: x.total_score, reverse=True)
        return candidates

    def generate_all_groups(self, n_per_group=5, n_front=5, n_back=2):
        results = {}
        methods = [self.generate_group_1, self.generate_group_2,
                   self.generate_group_3, self.generate_group_4, self.generate_group_5]
        for i, m in enumerate(methods[:self.n_groups]):
            cands = m(n_front, n_back)
            results[i+1] = cands[:n_per_group]
            print(f"  组{i+1}({m.__name__}): {len(cands)}候选, top={cands[0].total_score:.4f}" if cands else f"  组{i+1}: 无候选")
        return results

    def select_and_rank(self, all_candidates: Dict[int, List[ScoredCandidate]], top_n=5):
        all_c = []
        for gid, cands in all_candidates.items():
            for c in cands:
                c.group_id = gid
                all_c.append(c)
        seen = set()
        unique = []
        for c in all_c:
            k = (tuple(c.front), tuple(c.back))
            if k not in seen:
                seen.add(k)
                unique.append(c)

        def div_score(cand, sel):
            if not sel:
                return 1.0
            scores = []
            for s in sel:
                fo = len(set(cand.front) & set(s.front)) / 5.0
                bo = len(set(cand.back) & set(s.back)) / 2.0
                scores.append((fo + bo) / 2)
            return max(0.5, 1.0 - np.mean(scores))

        def rec_score(cand):
            if not self.draws:
                return 0.5
            fh = bh = 0.0
            for front, back in self.draws[-min(10, len(self.draws)):]:
                fh += len(set(cand.front) & set(front)) / 5.0
                bh += len(set(cand.back) & set(back)) / 2.0
            n = min(10, len(self.draws))
            return min((fh + bh) / (n * 2), 1.0)

        selected = []
        remaining = unique[:]
        for _ in range(min(top_n, len(remaining))):
            best_s, best_c, best_i = -float('inf'), None, -1
            for i, c in enumerate(remaining):
                final = c.total_score * (0.7 + 0.3 * div_score(c, selected))
                final = final * (0.9 + 0.1 * rec_score(c))
                if final > best_s:
                    best_s, best_c, best_i = final, c, i
            if best_c:
                selected.append(best_c)
                remaining.pop(best_i)

        selected.sort(key=lambda x: x.total_score, reverse=True)
        return selected

    def run(self, n_per_group=5, top_n=5):
        print("\n" + "="*60)
        print("StrategyFusionEngine.run() 开始执行...")
        print("="*60)
        all_candidates = self.generate_all_groups(n_per_group)
        final = self.select_and_rank(all_candidates, top_n)
        print(f"\n🎯 最终推荐 {len(final)} 组:")
        for i, r in enumerate(final):
            print(f"  {i+1}. 前区{r.front} 后区{r.back}  "
                  f"[{r.strategy_name}] score={r.total_score:.4f}")
        return final


# ============================================================
# 8. 入口函数
# ============================================================

def load_dlt_data(path: str) -> List[Tuple[List[int], List[int]]]:
    try:
        import pandas as pd
        df = pd.read_excel(path)
        draws = []
        for j in range(len(df)):
            front = sorted([int(df.iloc[j][f'前区{i}']) for i in range(1, 6)])
            back = sorted([int(df.iloc[j][f'后区{i}']) for i in range(1, 3)])
            draws.append((front, back))
        return draws
    except Exception as e:
        print(f"数据加载失败: {e}")
        return []


def predict_fusion(n_groups=5, top_n=5):
    data_path = '/mnt/d/cp/DLT历史数据_适配模型版.xlsx'
    draws = load_dlt_data(data_path)
    if not draws:
        print("⚠️ 无历史数据，请检查路径")
        return []
    engine = StrategyFusionEngine(draws, n_groups=n_groups)
    return engine.run(n_per_group=n_groups, top_n=top_n)


if __name__ == '__main__':
    predict_fusion(5, 5)
