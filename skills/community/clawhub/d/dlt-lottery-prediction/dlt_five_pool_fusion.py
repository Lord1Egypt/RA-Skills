#!/usr/bin/env python3
"""
五池×13维融合器 (FivePoolFusion)
实现 FeatureScorer(13维) × FivePoolSampler(5池) 的真正融合

核心思路：
1. 复用 FeatureScorer 的13维评分体系，不重复计算
2. 复用 FivePoolSampler 的5池生成逻辑
3. 每个池对13维有不同的权重偏好（如热池偏重hot_cold，冷池偏重missing_bayesian）
4. 用池×维度加权融合评分替代原有单一池评分

池→维度权重映射（启发式规则）：
- 热池  (hot):    hot_cold(0.40) + cooccurrence(0.20) + repeat(0.15) + size(0.10) + 其他(0.15)
- 冷池  (cold):   missing_bayesian(0.40) + zone(0.20) + consecutive(0.15) + 其他(0.25)
- 均衡池(balance):13维均匀权重(≈0.077/维)
- 博弈池(game):   sum(0.25) + range(0.20) + zone(0.20) + odd_even(0.15) + 其他(0.20)
- 遗传池(genetic):odd_even(0.20) + sum(0.20) + zone(0.20) + hot_cold(0.15) + 其他(0.25)

作者: 贾维斯 (JARVIS)
日期: 2026-04-07

# 默认池权重（前区/后区共用）
DEFAULT_POOL_WEIGHTS: Dict[str, float] = {
    'hot': 0.35,
    'cold': 0.20,
    'balance': 0.20,
    'game': 0.15,
    'genetic': 0.10,
}

"""

# 默认池权重（前区/后区共用）
DEFAULT_POOL_WEIGHTS = {
    'hot': 0.35,
    'cold': 0.20,
    'balance': 0.20,
    'game': 0.15,
    'genetic': 0.10,
}

import numpy as np
import random
from typing import List, Dict, Tuple, Optional

from dlt_strategy_fusion_v2 import FeatureScorer
from five_pool_sampler_complete_final import FivePoolSampler

# 13维维度名称常量
ALL_DIMENSIONS: List[str] = [
    'hot_cold', 'odd_even', 'consecutive', 'repeat', 'adjacent',
    'sum', 'prime', 'missing_bayesian', 'size', 'zone', 'ac', 'range', 'cooccurrence'
]

# 池类型常量
POOL_TYPES: List[str] = ['hot', 'cold', 'balance', 'game', 'genetic']

# 各池→维度的权重映射（预定义）
POOL_DIMENSION_WEIGHTS: Dict[str, Dict[str, float]] = {
    'hot': {
        'hot_cold': 0.40,
        'cooccurrence': 0.20,
        'repeat': 0.15,
        'size': 0.10,
        'odd_even': 0.04,
        'consecutive': 0.03,
        'adjacent': 0.03,
        'sum': 0.02,
        'prime': 0.01,
        'missing_bayesian': 0.01,
        'zone': 0.005,
        'ac': 0.005,
        'range': 0.00,
    },
    'cold': {
        'missing_bayesian': 0.40,
        'zone': 0.20,
        'consecutive': 0.15,
        'adjacent': 0.08,
        'range': 0.05,
        'hot_cold': 0.04,
        'size': 0.03,
        'cooccurrence': 0.02,
        'repeat': 0.01,
        'odd_even': 0.01,
        'sum': 0.01,
        'prime': 0.00,
        'ac': 0.00,
    },
    'balance': {
        # 13维均匀权重
        'hot_cold': 1 / 13,
        'odd_even': 1 / 13,
        'consecutive': 1 / 13,
        'repeat': 1 / 13,
        'adjacent': 1 / 13,
        'sum': 1 / 13,
        'prime': 1 / 13,
        'missing_bayesian': 1 / 13,
        'size': 1 / 13,
        'zone': 1 / 13,
        'ac': 1 / 13,
        'range': 1 / 13,
        'cooccurrence': 1 / 13,
    },
    'game': {
        'sum': 0.25,
        'range': 0.20,
        'zone': 0.20,
        'odd_even': 0.15,
        'size': 0.08,
        'consecutive': 0.04,
        'adjacent': 0.03,
        'prime': 0.02,
        'hot_cold': 0.01,
        'missing_bayesian': 0.01,
        'cooccurrence': 0.01,
        'repeat': 0.00,
        'ac': 0.00,
    },
    'genetic': {
        'odd_even': 0.20,
        'sum': 0.20,
        'zone': 0.20,
        'hot_cold': 0.15,
        'consecutive': 0.08,
        'range': 0.06,
        'size': 0.04,
        'prime': 0.03,
        'adjacent': 0.02,
        'missing_bayesian': 0.01,
        'cooccurrence': 0.01,
        'repeat': 0.00,
        'ac': 0.00,
    },
}


# ============================================================================
# 五池×13维融合器
# ============================================================================

class FivePoolFusion:
    """
    五池×13维融合器

    实现 FeatureScorer(13维) × FivePoolSampler(5池) 的真正融合：
    1. 复用 FeatureScorer 预计算的13维评分
    2. 复用 FivePoolSampler 的5池号码列表
    3. 建立五池→维度的映射关系（启发式权重）
    4. 每个号码获得 5池×13维 的融合评分

    Example:
        >>> fusion = FivePoolFusion(historical_draws)
        >>> scores = fusion.generate_fused_pool_scores('front')
        >>> sample = fusion.sample_from_fused_pool('front',
        ...     {'hot': 0.4, 'cold': 0.2, 'balance': 0.2, 'game': 0.1, 'genetic': 0.1}, n=5)
    """

    def __init__(self, draws: List[Tuple[List[int], List[int]]]):
        """
        初始化五池×13维融合器

        Args:
            draws: 历史开奖数据，格式为[(前区5个号码, 后区2个号码), ...]
        """
        self.draws = draws
        self.front_draws = [d[0] for d in draws]
        self.back_draws = [d[1] for d in draws]

        # 初始化13维评分器（FeatureScorer）
        self.scorer = FeatureScorer(draws)

        # 初始化五池采样器（FivePoolSampler）
        self.pool_sampler = FivePoolSampler(draws)

        # 13维评分缓存（延迟计算，按zone分开）
        self._score_cache: Dict[str, Dict[str, Dict[int, float]]] = {
            'front': {},
            'back': {},
        }

        # 五池号码缓存
        self._pool_cache: Dict[str, Dict[str, List[int]]] = {
            'front': {},
            'back': {},
        }

        # 融合评分缓存
        self._fused_cache: Dict[str, Dict[int, Dict[str, float]]] = {
            'front': {},
            'back': {},
        }

        self._pools_generated = False

        print(f"✅ FivePoolFusion 初始化完成")
        print(f"   历史数据: {len(draws)} 期")
        print(f"   维度数: {len(ALL_DIMENSIONS)}")
        print(f"   池类型: {POOL_TYPES}")

    # ------------------------------------------------------------------------
    # 公共接口
    # ------------------------------------------------------------------------

    def get_pool_dimension_weights(self, pool_type: str, zone: str) -> Dict[str, float]:
        """
        获取某池在各维度的权重分布

        Args:
            pool_type: 池类型，'hot' | 'cold' | 'balance' | 'game' | 'genetic'
            zone:      区域，'front' 或 'back'

        Returns:
            Dict[str, float]: 13维权重字典，权重和为1.0

        Raises:
            ValueError: 无效的池类型

        Example:
            >>> weights = fusion.get_pool_dimension_weights('hot', 'front')
            >>> # {'hot_cold': 0.40, 'cooccurrence': 0.20, ...}
        """
        if pool_type not in POOL_TYPES:
            raise ValueError(f"无效池类型: {pool_type}，可选: {POOL_TYPES}")

        weights = POOL_DIMENSION_WEIGHTS.get(pool_type, {})

        # 归一化确保和为1.0
        total = sum(weights.values())
        if abs(total - 1.0) > 1e-6:
            weights = {k: v / total for k, v in weights.items()}

        return weights

    def get_all_pool_dimension_weights(self, zone: str) -> Dict[str, Dict[str, float]]:
        """
        获取所有池的维度权重（方便调试/展示）

        Args:
            zone: 'front' 或 'back'

        Returns:
            Dict[str, Dict[str, float]]: {pool_type: {dimension: weight}}
        """
        return {pool: self.get_pool_dimension_weights(pool, zone) for pool in POOL_TYPES}

    def _ensure_scores(self, zone: str) -> None:
        """延迟加载13维评分"""
        if zone not in self._score_cache or not self._score_cache[zone]:
            self._score_cache[zone] = self.scorer.get_all_scores(zone)

    def _ensure_pools(self, zone: str, pool_size: int = 20) -> None:
        """延迟生成本池号码列表"""
        if not self._pools_generated or zone not in self._pool_cache or not self._pool_cache[zone]:
            if zone == 'front':
                self._pool_cache['front'] = {
                    'hot':     self.pool_sampler.generate_hot_pool(pool_size, 'front'),
                    'cold':    self.pool_sampler.generate_cold_pool(pool_size, 'front'),
                    'balance': self.pool_sampler.generate_balance_pool(pool_size, 'front'),
                    'game':    self.pool_sampler.generate_game_theory_pool(pool_size, 'front'),
                    'genetic': self.pool_sampler.generate_genetic_pool(pool_size, 'front'),
                }
            else:
                self._pool_cache['back'] = {
                    'hot':     self.pool_sampler.generate_hot_pool(pool_size, 'back'),
                    'cold':    self.pool_sampler.generate_cold_pool(pool_size, 'back'),
                    'balance': self.pool_sampler.generate_balance_pool(pool_size, 'back'),
                    'game':    self.pool_sampler.generate_game_theory_pool(pool_size, 'back'),
                    'genetic': self.pool_sampler.generate_genetic_pool(pool_size, 'back'),
                }
            self._pools_generated = True

    def fuse_pool_with_dimensions(
        self, pool_nums: List[int], pool_type: str, zone: str
    ) -> Dict[int, float]:
        """
        将某池的号码用对应维度加权融合评分

        用该池偏好的维度权重，对池内每个号码的13维评分进行加权求和，
        得到该池对每个号码的融合评分。

        Args:
            pool_nums:  池内号码列表
            pool_type:  池类型
            zone:       'front' 或 'back'

        Returns:
            Dict[int, float]: {号码: 融合评分}

        Example:
            >>> scores = fusion.fuse_pool_with_dimensions([1,2,3,4,5], 'hot', 'front')
            >>> # {1: 0.82, 2: 0.75, 3: 0.68, 4: 0.91, 5: 0.73}
        """
        self._ensure_scores(zone)
        dim_weights = self.get_pool_dimension_weights(pool_type, zone)
        all_scores = self._score_cache[zone]

        fused_scores: Dict[int, float] = {}
        for num in pool_nums:
            score = 0.0
            for dim_name, weight in dim_weights.items():
                if dim_name in all_scores and num in all_scores[dim_name]:
                    score += weight * all_scores[dim_name][num]
            fused_scores[num] = score

        return fused_scores

    def generate_fused_pool_scores(self, zone: str = 'front') -> Dict[int, Dict[str, float]]:
        """
        为每个号码生成五池×13维的融合评分矩阵

        遍历5个池×全部号码，生成 {号码: {pool_type: fused_score}} 评分矩阵。

        Args:
            zone: 'front' 或 'back'

        Returns:
            Dict[int, Dict[str, float]]:
                {号码: {pool_type: fused_score}}

        Example:
            >>> matrix = fusion.generate_fused_pool_scores('front')
            >>> # {3: {'hot': 0.82, 'cold': 0.15, ...}, 7: {...}, ...}
        """
        self._ensure_pools(zone)
        self._ensure_scores(zone)

        if zone in self._fused_cache and self._fused_cache[zone]:
            return self._fused_cache[zone]

        fused: Dict[int, Dict[str, float]] = {}

        for pool_type in POOL_TYPES:
            pool_nums = self._pool_cache[zone].get(pool_type, [])
            if not pool_nums:
                continue

            pool_fused = self.fuse_pool_with_dimensions(pool_nums, pool_type, zone)

            for num, score in pool_fused.items():
                if num not in fused:
                    fused[num] = {}
                fused[num][pool_type] = score

        self._fused_cache[zone] = fused
        return fused

    def get_pool_blended_score(self, num: int, zone: str) -> float:
        """
        综合五池权重，计算某号码的最终融合评分

        将某号码在5个池中的融合评分，按默认池权重加权求和。

        默认池权重：
            hot=0.35, cold=0.20, balance=0.20, game=0.15, genetic=0.10

        Args:
            num:  目标号码
            zone: 'front' 或 'back'

        Returns:
            float: 融合评分（0~1之间）

        Example:
            >>> score = fusion.get_pool_blended_score(7, 'front')
        """
        default_pool_weights: Dict[str, float] = {
            'hot': 0.35,
            'cold': 0.20,
            'balance': 0.20,
            'game': 0.15,
            'genetic': 0.10,
        }
        return self._blend_score_with_pool_weights(num, zone, default_pool_weights)

    def _blend_score_with_pool_weights(
        self, num: int, zone: str, pool_weights: Dict[str, float]
    ) -> float:
        """用指定的池权重计算某号码的融合评分"""
        self._ensure_pools(zone)
        self._ensure_scores(zone)

        if zone not in self._fused_cache or not self._fused_cache[zone]:
            self.generate_fused_pool_scores(zone)

        fused = self._fused_cache[zone]

        if num not in fused:
            return 0.5

        pool_scores = fused[num]

        blended = 0.0
        weight_sum = 0.0
        for pool_type, weight in pool_weights.items():
            if pool_type in pool_scores:
                blended += weight * pool_scores[pool_type]
                weight_sum += weight

        if weight_sum == 0:
            return 0.5

        return blended / weight_sum if weight_sum < 1.0 else blended

    def get_pool_blended_score_custom(
        self, num: int, zone: str, pool_weights: Dict[str, float]
    ) -> float:
        """
        使用自定义池权重计算某号码的最终融合评分

        Args:
            num:         目标号码
            zone:        'front' 或 'back'
            pool_weights: 自定义池权重，{'hot': 0.4, 'cold': 0.2, ...}

        Returns:
            float: 融合评分（0~1之间）
        """
        total = sum(pool_weights.values())
        if abs(total - 1.0) > 1e-6:
            pool_weights = {k: v / total for k, v in pool_weights.items()}
        return self._blend_score_with_pool_weights(num, zone, pool_weights)

    def get_top_numbers(
        self,
        zone: str,
        pool_weights: Optional[Dict[str, float]] = None,
        top_k: int = 10,
        temperature: float = 1.0,
    ) -> List[int]:
        """
        获取融合评分最高的top_k个号码

        Args:
            zone:        'front' 或 'back'
            pool_weights: 池权重，默认使用 0.35/0.20/0.20/0.15/0.10
            top_k:       返回号码数量
            temperature: 温度参数（>1分散，<1集中），用于概率采样

        Returns:
            List[int]: 排序后的号码列表（从高到低）
        """
        if pool_weights is None:
            pool_weights = {
                'hot': 0.35, 'cold': 0.20,
                'balance': 0.20, 'game': 0.15, 'genetic': 0.10,
            }

        self._ensure_pools(zone)

        # 确定号码范围
        num_range = range(1, 36) if zone == 'front' else range(1, 13)

        # 计算每个号码的融合评分
        num_scores: Dict[int, float] = {}
        for num in num_range:
            num_scores[num] = self.get_pool_blended_score_custom(num, zone, pool_weights)

        # 温度调整
        if temperature != 1.0 and temperature > 0:
            scores_arr = np.array(list(num_scores.values()))
            scores_arr = scores_arr / temperature
            scores_arr = scores_arr - scores_arr.max()
            exp_scores = np.exp(scores_arr)
            probas = exp_scores / exp_scores.sum()
            indices = np.argsort(-probas)
            return [list(num_scores.keys())[i] for i in indices[:top_k]]

        # 直接按评分降序
        sorted_nums = sorted(num_scores.items(), key=lambda x: x[1], reverse=True)
        return [num for num, _ in sorted_nums[:top_k]]

    def sample_from_fused_pool(
        self,
        zone: str,
        pool_weights: Dict[str, float],
        n: int,
        temperature: float = 1.0,
    ) -> List[int]:
        """
        从融合池中按权重比例采样n个号码

        融合流程：
        1. 计算每个号码在各池中的融合评分
        2. 按 pool_weights 加权得到最终评分
        3. 用温度调整后的 softmax 概率分布采样n个号码（无放回）

        Args:
            zone:        'front' 或 'back'
            pool_weights: 各池权重分布，{'hot': 0.4, 'cold': 0.2, 'balance': 0.2, 'game': 0.1, 'genetic': 0.1}
            n:           采样数量
            temperature: 温度参数，默认1.0（越大越分散，越小越集中）

        Returns:
            List[int]: 采样的号码列表（无重复，按采样顺序排列）

        Raises:
            ValueError: n超出号码范围

        Example:
            >>> fusion.sample_from_fused_pool('front',
            ...     {'hot': 0.4, 'cold': 0.2, 'balance': 0.2, 'game': 0.1, 'genetic': 0.1}, n=5)
            [3, 7, 12, 21, 28]
        """
        # 归一化池权重
        total = sum(pool_weights.values())
        if abs(total - 1.0) > 1e-6:
            pool_weights = {k: v / total for k, v in pool_weights.items()}

        # 确定号码范围
        num_range = range(1, 36) if zone == 'front' else range(1, 13)
        max_n = len(num_range)

        if n > max_n:
            raise ValueError(f"n={n}超出{zone}区号码范围(1-{max_n})")

        # 预热缓存
        self._ensure_pools(zone)

        # 计算每个号码的融合评分
        num_scores: Dict[int, float] = {}
        for num in num_range:
            num_scores[num] = self.get_pool_blended_score_custom(num, zone, pool_weights)

        # 转换为numpy数组
        nums_list = list(num_range)
        scores_arr = np.array([num_scores[n] for n in nums_list])

        # 温度调整
        if temperature > 0:
            scores_arr = scores_arr / temperature
            scores_arr = scores_arr - scores_arr.max()
            exp_scores = np.exp(scores_arr)
            probas = exp_scores / exp_scores.sum()
        else:
            probas = np.zeros_like(scores_arr)
            probas[np.argmax(scores_arr)] = 1.0

        # 采样（无放回）
        sampled_indices = np.random.choice(len(nums_list), size=n, replace=False, p=probas)
        sampled = [nums_list[i] for i in sorted(sampled_indices)]

        return sampled

    def generate_recommendation(
        self,
        zone: str,
        n: int = 5,
        pool_weights: Optional[Dict[str, float]] = None,
        temperature: float = 1.0,
    ) -> List[int]:
        """
        生成推荐号码组合（便捷接口）

        从融合池中采样n个号码组成推荐组合。

        Args:
            zone:        'front' 或 'back'
            n:           号码数量（默认5个前区/2个后区）
            pool_weights: 池权重，默认使用 hot=0.35/cold=0.20/balance=0.20/game=0.15/genetic=0.10
            temperature: 温度参数，默认1.0

        Returns:
            List[int]: 推荐号码列表
        """
        if pool_weights is None:
            pool_weights = {
                'hot': 0.35, 'cold': 0.20,
                'balance': 0.20, 'game': 0.15, 'genetic': 0.10,
            }

        return self.sample_from_fused_pool(zone, pool_weights, n, temperature)

    def diagnose_fusion(self, zone: str = 'front') -> Dict:
        """
        诊断融合评分质量（调试用）

        返回：
        - 各池的号码列表
        - 各池的维度权重
        - 各号码在每个池中的融合评分
        - 最终融合评分排名

        Args:
            zone: 'front' 或 'back'

        Returns:
            Dict: 完整的诊断信息
        """
        self._ensure_pools(zone, pool_size=15)
        self._ensure_scores(zone)
        fused = self.generate_fused_pool_scores(zone)

        # 池权重（默认）
        default_weights = {
            'hot': 0.35, 'cold': 0.20,
            'balance': 0.20, 'game': 0.15, 'genetic': 0.10,
        }

        # 计算每个号码的最终融合评分
        num_range = range(1, 36) if zone == 'front' else range(1, 13)
        all_scores = {}
        for num in num_range:
            all_scores[num] = self.get_pool_blended_score_custom(num, zone, default_weights)

        sorted_scores = sorted(all_scores.items(), key=lambda x: x[1], reverse=True)

        return {
            'zone': zone,
            'pools': {pool: self._pool_cache[zone].get(pool, []) for pool in POOL_TYPES},
            'dimension_weights': self.get_all_pool_dimension_weights(zone),
            'fused_scores': fused,
            'ranked_numbers': sorted_scores,
            'top5': [num for num, _ in sorted_scores[:5]],
        }

    def clear_cache(self) -> None:
        """清空所有缓存，强制重新计算"""
        self._score_cache = {'front': {}, 'back': {}}
        self._pool_cache = {'front': {}, 'back': {}}
        self._fused_cache = {'front': {}, 'back': {}}
        self._pools_generated = False
        print("🗑️ 缓存已清空")


# ============================================================================
# 便捷函数
# ============================================================================

def quick_fusion_sample(
    draws: List[Tuple[List[int], List[int]]],
    zone: str = 'front',
    pool_weights: Optional[Dict[str, float]] = None,
    n: int = 5,
    temperature: float = 1.0,
) -> List[int]:
    """
    快速融合采样（无需手动初始化）

    Args:
        draws:       历史开奖数据
        zone:        'front' 或 'back'
        pool_weights: 池权重
        n:           采样数量
        temperature: 温度参数

    Returns:
        List[int]: 采样的号码列表
    """
    if pool_weights is None:
        pool_weights = {
            'hot': 0.35, 'cold': 0.20,
            'balance': 0.20, 'game': 0.15, 'genetic': 0.10,
        }

    fusion = FivePoolFusion(draws)
    return fusion.sample_from_fused_pool(zone, pool_weights, n, temperature)


# ============================================================================
# 单元测试
# ============================================================================

if __name__ == '__main__':
    import warnings
    warnings.filterwarnings('ignore')

    # 构造100期模拟数据
    random.seed(42)
    np.random.seed(42)

    simulated_draws: List[Tuple[List[int], List[int]]] = []
    for _ in range(100):
        front = sorted(random.sample(range(1, 36), 5))
        back = sorted(random.sample(range(1, 13), 2))
        simulated_draws.append((front, back))

    print("=" * 60)
    print("五池×13维融合器 (FivePoolFusion) 单元测试")
    print("=" * 60)

    # 1. 初始化
    fusion = FivePoolFusion(simulated_draws)

    # 2. 测试池维度权重
    print("\n--- 池维度权重测试 ---")
    for pool in POOL_TYPES:
        w = fusion.get_pool_dimension_weights(pool, 'front')
        top_dims = sorted(w.items(), key=lambda x: x[1], reverse=True)[:3]
        print(f"  {pool:10s}: {', '.join(f'{d}({v:.3f})' for d,v in top_dims)}")
        assert abs(sum(w.values()) - 1.0) < 1e-6, f"权重和={sum(w.values())}≠1"

    # 3. 测试融合评分生成
    print("\n--- 融合评分矩阵测试 ---")
    fused = fusion.generate_fused_pool_scores('front')
    print(f"  前区评分矩阵包含号码数: {len(fused)}")
    assert len(fused) > 0, "融合评分矩阵为空"

    # 4. 测试融合评分计算
    print("\n--- 融合评分计算测试 ---")
    score7 = fusion.get_pool_blended_score(7, 'front')
    score15 = fusion.get_pool_blended_score(15, 'front')
    print(f"  号码7  融合评分: {score7:.4f}")
    print(f"  号码15 融合评分: {score15:.4f}")
    assert 0 <= score7 <= 1, "评分超出范围"
    assert 0 <= score15 <= 1, "评分超出范围"

    # 5. 测试采样
    print("\n--- 融合采样测试 ---")
    pool_weights = {'hot': 0.4, 'cold': 0.2, 'balance': 0.2, 'game': 0.1, 'genetic': 0.1}
    sample = fusion.sample_from_fused_pool('front', pool_weights, n=5, temperature=1.0)
    print(f"  采样结果(5个前区): {sample}")
    assert len(sample) == 5, "采样数量错误"
    assert len(set(sample)) == 5, "采样存在重复"

    sample_back = fusion.sample_from_fused_pool('back', pool_weights, n=2, temperature=1.0)
    print(f"  采样结果(2个后区): {sample_back}")
    assert len(sample_back) == 2, "后区采样数量错误"

    # 6. 测试诊断
    print("\n--- 诊断信息测试 ---")
    diag = fusion.diagnose_fusion('front')
    print(f"  Top5推荐: {diag['top5']}")

    # 7. 快速采样
    print("\n--- 快速采样测试 ---")
    quick = quick_fusion_sample(simulated_draws, 'front', n=5)
    print(f"  快速采样: {quick}")

    print("\n" + "=" * 60)
    print("✅ 全部测试通过！")
    print("=" * 60)
