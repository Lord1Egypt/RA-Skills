#!/usr/bin/env python3
"""
DLT统一约束引擎 (dlt_constraint_engine.py)

统一管理所有约束验证逻辑，消除约束分散问题。

约束分为三类：
  1. 硬约束 (hard constraints)：必须满足，不满足则丢弃
  2. 策略约束 (strategy constraints)：策略特定条件（如20号、连号等）
  3. 软约束 (soft constraints)：评分扣分项，影响排序优先级

使用示例：
    engine = DLTConstraintEngine()
    
    # 硬约束验证
    valid = engine.validate_hard([1, 5, 12, 20, 28], [3, 9])
    
    # 策略约束验证（方案类型 1-5）
    ok = engine.validate_strategy([1, 5, 12, 20, 28], [3, 9], strategy_type=1)
    
    # 软约束评分（返回 0.0 ~ 1.0，越高越好）
    score = engine.score_soft([1, 5, 12, 20, 28], [3, 9])

作者: 贾维斯 (JARVIS)
日期: 2026-04-06
"""

from typing import List, Tuple, Optional, Dict
from dataclasses import dataclass


# ============================================================
# 常量
# ============================================================

FRONT_RANGE = (1, 35)
BACK_RANGE = (1, 12)
FRONT_COUNT = 5
BACK_COUNT = 2

PRIMES_FRONT = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31}
PRIMES_BACK = {2, 3, 5, 7, 11}


# ============================================================
# 策略配置（从 dlt_strategy_fusion_v2.py 迁移）
# ============================================================

STRATEGY_CONFIGS: Dict[int, Dict] = {
    1: {  # 稳中求胜
        "name": "稳中求胜策略",
        "hard_sum_range": (80, 105),
        "hard_odd_even": (2, 3),
        "hard_zone_required": True,
        "hard_span_min": 23,
        "hard_prime_count": (1, 3),
        "soft_ac_range": (6, 10),
        "soft_consecutive_min": 1,
        "soft_consecutive_max": 2,
        "soft_sum_ideal": (85, 100),
    },
    2: {  # 平衡配置
        "name": "平衡配置策略",
        "hard_sum_range": (70, 115),
        "hard_zone_required": True,
        "hard_span_min": 20,
        "soft_ac_range": (6, 10),
        "soft_consecutive_min": 0,
        "soft_consecutive_max": 2,
        "soft_sum_ideal": (80, 105),
    },
    3: {  # 激进高和值
        "name": "激进高和值策略",
        "hard_sum_range": (75, 110),
        "hard_zone_required": True,
        "hard_span_min": 20,
        "soft_ac_range": (6, 10),
        "soft_consecutive_min": 1,
        "soft_consecutive_max": 2,
        "soft_sum_ideal": (90, 115),
    },
    4: {  # 保守小和值
        "name": "保守小和值策略",
        "hard_sum_range": (50, 90),
        "hard_zone_required": True,
        "hard_span_min": 15,
        "soft_ac_range": (5, 9),
        "soft_consecutive_min": 0,
        "soft_consecutive_max": 3,
        "soft_sum_ideal": (55, 85),
    },
    5: {  # 追热策略
        "name": "追热策略",
        "hard_sum_range": (60, 100),
        "hard_zone_required": False,
        "hard_span_min": 18,
        "soft_ac_range": (5, 10),
        "soft_consecutive_min": 0,
        "soft_consecutive_max": 3,
        "soft_sum_ideal": (70, 95),
    },
}


# ============================================================
# 主引擎类
# ============================================================

class DLTConstraintEngine:
    """
    统一约束验证引擎

    提供三类约束验证：
    - validate_hard: 硬约束（前区5个∈[1,35]互不重复，后区2个∈[1,12]互不重复）
    - validate_strategy: 策略约束（和值、奇偶、三区、跨度、质数等）
    - score_soft: 软约束评分（三区分布、AC值、连号数等）
    """

    def __init__(self, strategy_configs: Optional[Dict[int, Dict]] = None):
        """
        Args:
            strategy_configs: 可选，覆盖默认策略配置
        """
        self.strategy_configs = strategy_configs or STRATEGY_CONFIGS

    # ----------------------------------------------------------
    # 硬约束验证
    # ----------------------------------------------------------

    def validate_hard(self, front: List[int], back: List[int]) -> Tuple[bool, str]:
        """
        硬约束验证：基本格式 + 范围检查

        必须满足：
        - 前区5个数 ∈ [1, 35]，互不重复
        - 后区2个数 ∈ [1, 12]，互不重复

        Returns:
            (是否通过, 原因描述)
        """
        # 前区硬约束
        if len(front) != FRONT_COUNT:
            return False, f"前区数量错误: {len(front)}，期望 {FRONT_COUNT}"

        if len(set(front)) != len(front):
            return False, f"前区存在重复号码: {front}"

        if not all(FRONT_RANGE[0] <= n <= FRONT_RANGE[1] for n in front):
            bad = [n for n in front if not (FRONT_RANGE[0] <= n <= FRONT_RANGE[1])]
            return False, f"前区号码超出范围[1,35]: {bad}"

        # 后区硬约束
        if len(back) != BACK_COUNT:
            return False, f"后区数量错误: {len(back)}，期望 {BACK_COUNT}"

        if len(set(back)) != len(back):
            return False, f"后区存在重复号码: {back}"

        if not all(BACK_RANGE[0] <= n <= BACK_RANGE[1] for n in back):
            bad = [n for n in back if not (BACK_RANGE[0] <= n <= BACK_RANGE[1])]
            return False, f"后区号码超出范围[1,12]: {bad}"

        return True, "OK"

    def validate_strategy(
        self,
        front: List[int],
        back: List[int],
        strategy_type: int
    ) -> Tuple[bool, str]:
        """
        策略约束验证

        根据 strategy_type 应用对应的策略配置进行验证。

        Args:
            front: 前区号码列表
            back: 后区号码列表
            strategy_type: 策略类型 (1-5)

        Returns:
            (是否通过, 原因描述)
        """
        if strategy_type not in self.strategy_configs:
            return False, f"未知策略类型: {strategy_type}"

        cfg = self.strategy_configs[strategy_type]
        front_sorted = sorted(front)

        # 和值范围
        if "hard_sum_range" in cfg:
            lo, hi = cfg["hard_sum_range"]
            s = sum(front)
            if not (lo <= s <= hi):
                return False, f"前区和值{s}不在策略范围[{lo},{hi}]"

        # 三区完整性
        if cfg.get("hard_zone_required", False):
            z1 = sum(1 for n in front if 1 <= n <= 12)
            z2 = sum(1 for n in front if 13 <= n <= 24)
            z3 = sum(1 for n in front if 25 <= n <= 35)
            if z1 == 0 or z2 == 0 or z3 == 0:
                return False, f"三区[{z1},{z2},{z3}]不完整（策略要求三区全有）"

        # 奇偶比
        if "hard_odd_even" in cfg:
            odd = sum(1 for n in front if n % 2 == 1)
            even = len(front) - odd
            target = cfg["hard_odd_even"]
            if (odd, even) != target and (odd, even) != (target[1], target[0]):
                return False, f"奇偶比({odd}:{even})不符合策略要求"

        # 跨度
        if "hard_span_min" in cfg:
            span = max(front) - min(front)
            if span < cfg["hard_span_min"]:
                return False, f"跨度{span}小于最小要求{cfg['hard_span_min']}"

        # 整十号排除
        if cfg.get("hard_no_round", False):
            if any(n % 10 == 0 for n in front):
                return False, "策略禁止整十号"

        # 质数数量
        if "hard_prime_count" in cfg:
            prime_cnt = sum(1 for n in front if n in PRIMES_FRONT)
            lo, hi = cfg["hard_prime_count"]
            if not (lo <= prime_cnt <= hi):
                return False, f"质数数量{prime_cnt}不在策略范围[{lo},{hi}]"

        return True, "OK"

    # ----------------------------------------------------------
    # 软约束评分
    # ----------------------------------------------------------

    def score_soft(
        self,
        front: List[int],
        back: List[int],
        strategy_type: Optional[int] = None
    ) -> float:
        """
        软约束评分

        根据策略配置计算满足度分数 (0.0 ~ 1.0)，越高越好。

        评分维度：
        - AC值是否在理想范围
        - 连号数量是否合适
        - 和值是否在理想区间

        Args:
            front: 前区号码列表
            back: 后区号码列表
            strategy_type: 可选，指定策略类型以获取对应评分标准

        Returns:
            满足度分数 (0.0 ~ 1.0)
        """
        score = 1.0

        # 策略特定配置
        cfg = {}
        if strategy_type and strategy_type in self.strategy_configs:
            cfg = self.strategy_configs[strategy_type]

        # AC值评分
        if "soft_ac_range" in cfg:
            ac = self._compute_ac(front)
            lo, hi = cfg["soft_ac_range"]
            if not (lo <= ac <= hi):
                score *= 0.5

        # 连号评分
        if "soft_consecutive_min" in cfg or "soft_consecutive_max" in cfg:
            consecutive_count = self._count_consecutive(front)
            lo = cfg.get("soft_consecutive_min", 0)
            hi = cfg.get("soft_consecutive_max", 999)
            if not (lo <= consecutive_count <= hi):
                score *= 0.7

        # 和值理想区间评分
        if "soft_sum_ideal" in cfg:
            s = sum(front)
            lo, hi = cfg["soft_sum_ideal"]
            if not (lo <= s <= hi):
                score *= 0.7

        return max(0.0, score)

    # ----------------------------------------------------------
    # 组合验证（硬约束 + 策略约束）
    # ----------------------------------------------------------

    def validate_full(
        self,
        front: List[int],
        back: List[int],
        strategy_type: int
    ) -> Tuple[bool, str]:
        """
        完整验证：硬约束 + 策略约束

        等价于依次调用 validate_hard 和 validate_strategy。
        """
        # 第一步：硬约束
        ok, msg = self.validate_hard(front, back)
        if not ok:
            return False, f"[硬约束] {msg}"

        # 第二步：策略约束
        ok, msg = self.validate_strategy(front, back, strategy_type)
        if not ok:
            return False, f"[策略约束] {msg}"

        return True, "OK"

    # ----------------------------------------------------------
    # 辅助计算方法
    # ----------------------------------------------------------

    @staticmethod
    def _compute_ac(numbers: List[int]) -> int:
        """计算AC值"""
        diffs = set()
        for i in range(len(numbers)):
            for j in range(i + 1, len(numbers)):
                diffs.add(abs(numbers[j] - numbers[i]))
        return len(diffs) - (len(numbers) - 1)

    @staticmethod
    def _count_consecutive(numbers: List[int]) -> int:
        """计算连号数量（相邻差为1的配对数）"""
        sorted_nums = sorted(numbers)
        count = 0
        i = 0
        while i < len(sorted_nums) - 1:
            if sorted_nums[i + 1] - sorted_nums[i] == 1:
                count += 1
                i += 2
            else:
                i += 1
        return count

    @staticmethod
    def _zone_distribution(front: List[int]) -> Tuple[int, int, int]:
        """计算三区分布"""
        z1 = sum(1 for n in front if 1 <= n <= 12)
        z2 = sum(1 for n in front if 13 <= n <= 24)
        z3 = sum(1 for n in front if 25 <= n <= 35)
        return z1, z2, z3

    @staticmethod
    def _odd_even_ratio(front: List[int]) -> Tuple[int, int]:
        """计算奇偶比"""
        odd = sum(1 for n in front if n % 2 == 1)
        even = len(front) - odd
        return odd, even


# ============================================================
# 独立函数接口（兼容旧代码）
# ============================================================

# 全局默认引擎实例
_default_engine: Optional[DLTConstraintEngine] = None


def get_engine() -> DLTConstraintEngine:
    """获取全局约束引擎实例（延迟创建）"""
    global _default_engine
    if _default_engine is None:
        _default_engine = DLTConstraintEngine()
    return _default_engine


def validate_hard(front: List[int], back: List[int]) -> Tuple[bool, str]:
    """独立函数：验证硬约束"""
    return get_engine().validate_hard(front, back)


def validate_strategy(
    front: List[int],
    back: List[int],
    strategy_type: int
) -> Tuple[bool, str]:
    """独立函数：验证策略约束"""
    return get_engine().validate_strategy(front, back, strategy_type)


def score_soft(
    front: List[int],
    back: List[int],
    strategy_type: Optional[int] = None
) -> float:
    """独立函数：计算软约束评分"""
    return get_engine().score_soft(front, back, strategy_type)


# ============================================================
# 快速测试
# ============================================================

if __name__ == "__main__":
    engine = DLTConstraintEngine()

    # 测试用例
    test_cases = [
        ([8, 11, 18, 24, 33], [3, 9], 1, True, "稳中求胜-正常(和值94)"),
        ([1, 1, 3, 5, 7], [1, 2], 1, False, "前区重复"),
        ([1, 5, 12, 20, 28], [3, 3], 1, False, "后区重复"),
        ([1, 5, 12, 20, 40], [3, 9], 1, False, "前区超范围"),
        ([1, 5, 12, 20, 28], [3, 15], 1, False, "后区超范围"),
    ]

    print("DLTConstraintEngine 验证测试")
    print("=" * 60)

    all_pass = True
    for front, back, stype, expected_ok, desc in test_cases:
        ok_h, msg_h = engine.validate_hard(front, back)
        if not ok_h:
            ok_s, msg_s = False, "前置硬约束失败"
        else:
            ok_s, msg_s = engine.validate_strategy(front, back, stype)

        ok_full, _ = engine.validate_full(front, back, stype)
        sc = engine.score_soft(front, back, stype)
        actual_ok = ok_full

        status = "✅" if actual_ok == expected_ok else "❌"
        if actual_ok != expected_ok:
            all_pass = False
        print(f"{status} {desc}")
        print(f"   硬约束: {ok_h} {msg_h}")
        print(f"   策略约束: {ok_s} {msg_s}")
        print(f"   软约束评分: {sc:.2f}")

    print("=" * 60)
    print(f"测试结果: {'✅ 全部通过' if all_pass else '❌ 存在失败'}")
