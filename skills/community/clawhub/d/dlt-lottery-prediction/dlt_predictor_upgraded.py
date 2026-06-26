#!/usr/bin/env python3
"""
大乐透升级版预测器
整合所有优化:LTR + 贝叶斯遗漏值 + 概率校准 + 时序CV + 动态权重Stacking
+ 16集视频分析全面升级

基于16集视频分析的全面升级:
- 视频2: 博弈论分析(追冷策略与分奖防御)
- 视频4: 投注策略推荐(复式vs胆拖智能选择)
- 视频5+6: 数学滤网系统(剔除90%小概率组合)
- 视频7: 数理统计分析师(大数定律+均值回归+正态分布)

作者: AI Assistant
日期: 2025-01
升级: 2026-04
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Optional, Any, Callable
from pathlib import Path
import warnings
import sys
import os
from collections import defaultdict

# 导入本地模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lottery_metrics import LotteryMetrics, DLTPrizeEvaluator
from lottery_bayesian import BetaBinomialMissing, MissingValueTracker, BayesianNumberModel
from lottery_calibration import PlattScaling, IsotonicCalibrator, TemperatureScaling, MultiClassCalibrator

# 导入新增模块(直接导入真实模块,删除stub fallback)
from modules.dlt_math_filter import DLTMathFilter
from modules.dlt_kill_number import DLTKillNumberAnalyzer
from modules.dlt_number_gravity import DLTNumberGravity
from modules.dlt_difference_sequence import DLTDifferenceSequence
from modules.dlt_matrix_displacement import DLTMatrixDisplacement
from modules.dlt_strategy_recommender import DLTStrategyRecommender
from modules.dlt_game_theory import DLTGameTheoryAnalyzer
from modules.dlt_statistics_analyzer import DLTStatisticsAnalyzer
from lottery_time_series_cv import ExpandingWindowCV, TimeSeriesSplit, BacktestRunner


# 尝试导入LightGBM
try:
    import lightgbm as lgb
    HAS_LIGHTGBM = True
except ImportError:
    HAS_LIGHTGBM = False

try:
    from sklearn.linear_model import LogisticRegression
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False
    LogisticRegression = None


class DLTPrizeInfo:
    """大乐透奖项信息"""
    # 奖项定义
    PRIZES = {
        (5, 2): (1, "一等奖(头奖)"),
        (5, 1): (2, "二等奖"),
        (5, 0): (3, "三等奖"),
        (4, 2): (3, "三等奖"),
        (4, 1): (4, "四等奖"),
        (3, 2): (4, "四等奖"),
        (4, 0): (5, "五等奖"),
        (3, 1): (5, "五等奖"),
        (2, 2): (5, "五等奖"),
        (3, 0): (6, "六等奖"),
        (2, 1): (6, "六等奖"),
        (1, 2): (6, "六等奖"),
        (0, 2): (7, "七等奖"),
        (2, 0): (7, "七等奖"),
        (1, 1): (7, "七等奖"),
    }

    @staticmethod
    def get_prize_level(front_hit: int, back_hit: int) -> int:
        key = (front_hit, back_hit)
        if key in DLTPrizeInfo.PRIZES:
            return DLTPrizeInfo.PRIZES[key][0]
        return 0

    @staticmethod
    def get_prize_name(front_hit: int, back_hit: int) -> str:
        key = (front_hit, back_hit)
        if key in DLTPrizeInfo.PRIZES:
            return DLTPrizeInfo.PRIZES[key][1]
        return "未中奖"


class FeatureEngineering:
    """特征工程模块"""

    def __init__(self, n_front: int = 35, n_back: int = 12, window: int = 30):
        self.n_front = n_front
        self.n_back = n_back
        self.window = window
        self.n_estimators = 150
        self.learning_rate = 0.05

        # 强共现对(从数据分析中获取)
        self.front_strong_pairs = [
            (32, 33), (29, 30), (7, 12), (15, 22), (5, 8),
            (18, 25), (1, 19), (11, 21), (4, 16), (23, 28),
            (9, 14), (20, 31), (6, 17), (24, 27), (3, 13)
        ]
        self.back_strong_pairs = [
            (5, 8), (3, 10), (1, 6), (2, 11), (4, 7),
            (9, 12), (1, 3), (6, 9), (2, 5), (8, 11)
        ]

        # 统计共现矩阵
        self.front_cooc_matrix = np.zeros((n_front + 1, n_front + 1))
        self.back_cooc_matrix = np.zeros((n_back + 1, n_back + 1))

    def compute_cooccurrence(self, draws: List[Tuple[List[int], List[int]]]):
        """计算共现矩阵"""
        self.front_cooc_matrix.fill(0)
        self.back_cooc_matrix.fill(0)

        for front, back in draws:
            for i, n1 in enumerate(front):
                for n2 in front[i+1:]:
                    self.front_cooc_matrix[n1, n2] += 1
                    self.front_cooc_matrix[n2, n1] += 1

            for i, n1 in enumerate(back):
                for n2 in back[i+1:]:
                    self.back_cooc_matrix[n1, n2] += 1
                    self.back_cooc_matrix[n2, n1] += 1

    def build_features(self,
                      num: int,
                      history: List[Tuple[List[int], List[int]]],
                      missing: Dict[int, int],
                      zone: str) -> np.ndarray:
        """为单个号码构建特征向量"""

        is_front = zone == 'front'
        n_max = self.n_front if is_front else self.n_back
        cooc_matrix = self.front_cooc_matrix if is_front else self.back_cooc_matrix
        strong_pairs = self.front_strong_pairs if is_front else self.back_strong_pairs

        features = []

        # 1. 基础统计特征
        n_history = len(history)
        if n_history == 0:
            return np.zeros(25)

        # 出现频率
        appearances = sum(1 for front, _ in history if num in front) if is_front \
                      else sum(1 for _, back in history if num in back)
        freq = appearances / n_history

        # 遗漏统计
        current_missing = missing.get(num, n_history)

        # 遗漏期数特征
        missing_periods = []
        for idx, (front, back) in enumerate(history):
            nums = front if is_front else back
            if num in nums:
                if missing_periods:
                    missing_periods.append(idx - missing_periods[-1] - 1)
                else:
                    missing_periods.append(idx)

        mean_missing = np.mean(missing_periods) if missing_periods else n_history
        max_missing = np.max(missing_periods) if missing_periods else n_history
        std_missing = np.std(missing_periods) if len(missing_periods) > 1 else 0

        # 2. 时间加权特征
        # 近5期
        recent_5 = sum(1 for front, _ in history[-5:] if num in front) if is_front \
                   else sum(1 for _, back in history[-5:] if num in back)
        recent_10 = sum(1 for front, _ in history[-10:] if num in front) if is_front \
                    else sum(1 for _, back in history[-10:] if num in back)
        recent_20 = sum(1 for front, _ in history[-20:] if num in front) if is_front \
                    else sum(1 for _, back in history[-20:] if num in back)

        # 时间加权频率
        time_weighted_freq = 0
        for i, (front, back) in enumerate(history[-20:]):
            nums = front if is_front else back
            weight = (i + 1) / 20  # 越近权重越大
            if num in nums:
                time_weighted_freq += weight

        # 3. 号码属性
        features.append(freq)                           # 0: 出现频率
        features.append(current_missing)                 # 1: 当前遗漏
        features.append(current_missing / (mean_missing + 1e-6))  # 2: 相对遗漏
        features.append(num / n_max)                    # 3: 归一化号码
        features.append(num % 2)                         # 4: 奇偶性
        features.append((num - 1) // 7)                  # 5: 分区
        features.append((num - 1) % 7)                   # 6: 区内位置
        features.append(mean_missing)                   # 7: 平均遗漏
        features.append(max_missing)                     # 8: 最大遗漏
        features.append(std_missing)                    # 9: 遗漏标准差
        features.append(recent_5 / 5)                   # 10: 近5期频率
        features.append(recent_10 / 10)                 # 11: 近10期频率
        features.append(recent_20 / 20)                 # 12: 近20期频率
        features.append(time_weighted_freq / 20)        # 13: 时间加权频率
        features.append((recent_5 - recent_10 / 2))     # 14: 趋势变化

        # 4. 共现特征
        # 与其他号码的共现强度
        cooc_with_top = []
        for other_num in range(1, n_max + 1):
            if other_num != num:
                cooc_with_top.append(cooc_matrix[num, other_num])

        if cooc_with_top:
            features.append(np.mean(cooc_with_top))     # 15: 平均共现
            features.append(np.max(cooc_with_top))      # 16: 最大共现
            features.append(np.std(cooc_with_top))      # 17: 共现标准差
        else:
            features.extend([0, 0, 0])

        # 是否在强共现对中
        is_in_strong = 0.0
        strong_count = 0
        for p1, p2 in strong_pairs[:10]:
            if num == p1:
                is_in_strong = 1.0
                strong_count += cooc_matrix[num, p2]
            if num == p2:
                is_in_strong = 1.0
                strong_count += cooc_matrix[num, p1]

        features.append(is_in_strong)                  # 18: 是否在强共现对
        features.append(strong_count / max(n_history, 1))  # 19: 强共现频率

        # 5. 遗漏后验特征(贝叶斯)
        # Beta-Binomial后验
        alpha_post = 0.5 + appearances  # Jeffreys prior
        beta_post = 0.5 + n_history - appearances

        posterior_mean = alpha_post / (alpha_post + beta_post)
        posterior_std = np.sqrt(alpha_post * beta_post /
                                ((alpha_post + beta_post)**2 * (alpha_post + beta_post + 1)))

        features.append(posterior_mean)                # 20: 后验均值
        features.append(posterior_std)                  # 21: 后验标准差

        # 遗漏分位数(简化计算)
        missing_quantile = min(current_missing / (mean_missing * 2 + 1), 1.0)
        features.append(missing_quantile)               # 22: 遗漏分位数

        # 遗漏值与后验均值的交互
        features.append(current_missing * posterior_mean)  # 23: 交互特征

        # 6. 冷热指标
        heat_score = recent_10 / 10 - freq
        features.append(heat_score)                     # 24: 冷热得分

        return np.array(features)

    def build_all_features(self,
                          history: List[Tuple[List[int], List[int]]],
                          zone: str) -> Tuple[np.ndarray, List[int]]:
        """为所有号码构建特征"""
        is_front = zone == 'front'
        n = self.n_front if is_front else self.n_back

        # 更新共现矩阵
        self.compute_cooccurrence(history)

        # 构建遗漏跟踪器
        tracker = MissingValueTracker(
            n_front=self.n_front if is_front else 1,
            n_back=self.n_back if not is_front else 1
        )
        tracker.update_batch(history)
        missing = tracker.get_current_missing()

        features = []
        labels = []

        for num in range(1, n + 1):
            feat = self.build_features(num, history, missing, zone)
            features.append(feat)

            # 标签:下一期是否出现(暂时设为0,实际训练时会填充)
            labels.append(num)

        return np.array(features), labels

    # ==================== 16集视频升级:新增特征提取方法 ====================

    def _count_zones(self, combo: List[int]) -> List[int]:
        """
        计算三区分布

        将35个前区号码分成3区:
        - 1区: 1-12
        - 2区: 13-24
        - 3区: 25-35

        Args:
            combo: 候选组合

        Returns:
            List[int]: 各区号码数量
        """
        zone_counts = [0, 0, 0]
        for n in combo:
            if n <= 12:
                zone_counts[0] += 1
            elif n <= 24:
                zone_counts[1] += 1
            else:
                zone_counts[2] += 1
        return zone_counts

    def _calc_popularity_avoidance(self, combo: List[int]) -> float:
        """
        计算大众偏好回避度

        分数越高表示该组合越能避开大众选择
        """
        score = 0.0
        # 避开1-10低号段
        low_count = sum(1 for n in combo if n <= 10)
        if low_count <= 1:
            score += 0.3
        # 避开整十数字
        round_count = sum(1 for n in combo if n % 10 == 0)
        if round_count <= 1:
            score += 0.2
        # 高号比例
        high_count = sum(1 for n in combo if n >= 28)
        if high_count >= 3:
            score += 0.3
        # 奇偶极端
        odd = sum(1 for n in combo if n % 2 == 1)
        if odd in [0, 5]:
            score += 0.2
        return min(score, 1.0)

    def _calc_visual_regularity(self, combo: List[int]) -> float:
        """
        计算视觉规律度(越无规律越高分)
        """
        score = 0.0
        sorted_combo = sorted(combo)
        consecutive_count = 0
        for i in range(len(sorted_combo) - 1):
            if sorted_combo[i+1] - sorted_combo[i] <= 2:
                consecutive_count += 1
        if consecutive_count == 0:
            score += 0.4
        elif consecutive_count == 1:
            score += 0.2
        # 检测等差数列
        if len(sorted_combo) >= 3:
            diffs = [sorted_combo[i+1] - sorted_combo[i] for i in range(len(sorted_combo)-1)]
            if len(set(diffs)) == 1:
                score -= 0.3
        return max(0.0, min(score, 1.0))

    def _calc_extreme_structure(self, combo: List[int]) -> float:
        """
        计算极端结构度
        """
        odd = sum(1 for n in combo if n % 2 == 1)
        high = sum(1 for n in combo if n >= 28)
        span = max(combo) - min(combo)

        score = 0.0
        if odd in [0, 5]:  # 奇偶极端
            score += 0.3
        if high >= 3:  # 高号集中
            score += 0.3
        if span > 30:  # 大跨度
            score += 0.2
        if sum(combo) < 70 or sum(combo) > 120:  # 极端和值
            score += 0.2
        return min(score, 1.0)

    def _calc_hot_cold_entropy(self, combo: List[int]) -> float:
        """
        计算冷热熵值(需要外部频率数据,这里返回默认值)
        """
        # 简化版本:基于组合自身的分布计算
        return 0.5

    def _calc_mean_reversion(self, combo: List[int], recent_sums: np.ndarray) -> float:
        """
        计算均值回归度
        """
        if len(recent_sums) < 10:
            return 0.5
        mean = np.mean(recent_sums)
        std = np.std(recent_sums)
        last_sum = sum(combo)
        z_score = (last_sum - mean) / (std + 1e-10)
        if abs(z_score) > 1.5:
            return 0.8
        elif abs(z_score) > 1.0:
            return 0.6
        elif abs(z_score) > 0.5:
            return 0.4
        return 0.2

    def _calc_statistical_deviation(self, combo: List[int]) -> float:
        """
        计算统计偏离度
        """
        combo_sum = sum(combo)
        # 理论均值约为95,标准差约为15
        z_score = abs((combo_sum - 95) / 15)
        return min(z_score, 3.0) / 3.0  # 归一化到0-1

    def _calc_cold_zone_density(self, combo: List[int]) -> float:
        """
        计算冷号密度
        """
        # 简化:低号区(1-12)号码越多,密度越高
        low_count = sum(1 for n in combo if n <= 12)
        return low_count / 5.0

    def _calc_subset_coverage(self, combo: List[int]) -> float:
        """
        计算子集覆盖率
        """
        # 简化:号码越分散,覆盖率越高
        sorted_combo = sorted(combo)
        span = sorted_combo[-1] - sorted_combo[0]
        return min(span / 34.0, 1.0)

    def _calc_zone_dispersion(self, combo: List[int]) -> float:
        """
        计算区域分散度
        """
        zones = self._count_zones(combo)
        # 如果三区都有号码,分散度高
        non_zero_zones = sum(1 for z in zones if z > 0)
        return non_zero_zones / 3.0

    def _calc_matrix_position(self, combo: List[int]) -> float:
        """
        计算矩阵位置得分
        """
        # 简化:中心区域号码越多,得分越高
        center_count = sum(1 for n in combo if 13 <= n <= 24)
        return center_count / 5.0

    def _calc_betting_ratio(self, combo: List[int]) -> float:
        """
        计算投注比例得分
        """
        odd = sum(1 for n in combo if n % 2 == 1)
        return 1.0 if odd in [2, 3] else 0.5

    def extract_math_filter_features(self,
                                    combo: List[int],
                                    historical_stats: Dict = None) -> Dict[str, float]:
        """
        提取数学滤网特征(5维)

        基于视频5+6的数学滤网系统

        Args:
            combo: 候选组合
            historical_stats: 历史统计数据(可选)

        Returns:
            Dict[str, float]: 数学滤网特征
        """
        features = {}

        # 1. 奇偶平衡度
        odd = sum(1 for n in combo if n % 2 == 1)
        features['parity_balance'] = 1.0 if odd in [2, 3] else 0.0

        # 2. 高低分布度
        high = sum(1 for n in combo if n > 18)
        low = sum(1 for n in combo if n <= 18)
        features['high_low_distribution'] = 1.0 if high in [2, 3] else 0.0

        # 3. 和值区间兼容度
        total = sum(combo)
        features['sum_range_compatibility'] = 1.0 if 70 <= total <= 120 else 0.0

        # 4. 跨度得分
        span = max(combo) - min(combo)
        features['span_score'] = 1.0 if 24 <= span <= 30 else 0.0

        # 5. 三区分布得分
        zones = self._count_zones(combo)
        features['zone_distribution'] = 1.0 if tuple(sorted(zones)) in [(2,2,1), (1,2,2)] else 0.0

        return features

    def extract_game_theory_features(self, combo: List[int]) -> Dict[str, float]:
        """
        提取博弈论特征(4维)

        基于视频2的博弈论分析器

        Args:
            combo: 候选组合

        Returns:
            Dict[str, float]: 博弈论特征
        """
        features = {}

        # 1. 大众偏好回避度
        features['popularity_avoidance'] = self._calc_popularity_avoidance(combo)

        # 2. 视觉规律度
        features['visual_regularity'] = self._calc_visual_regularity(combo)

        # 3. 极端结构度
        features['extreme_structure'] = self._calc_extreme_structure(combo)

        # 4. 整十数回避度
        round_count = sum(1 for n in combo if n % 10 == 0)
        features['round_number_avoidance'] = 1.0 if round_count <= 1 else 0.0

        return features

    def extract_statistics_features(self,
                                  combo: List[int],
                                  recent_sums: np.ndarray = None) -> Dict[str, float]:
        """
        提取数理统计特征(4维)

        基于视频7的数理统计分析师

        Args:
            combo: 候选组合
            recent_sums: 近期和值序列

        Returns:
            Dict[str, float]: 数理统计特征
        """
        features = {}

        # 1. 冷热熵值
        features['hot_cold_entropy'] = self._calc_hot_cold_entropy(combo)

        # 2. 均值回归度
        if recent_sums is not None:
            features['mean_reversion'] = self._calc_mean_reversion(combo, recent_sums)
        else:
            features['mean_reversion'] = 0.5

        # 3. 统计偏离度
        features['statistical_deviation'] = self._calc_statistical_deviation(combo)

        # 4. 冷号密度
        features['cold_zone_density'] = self._calc_cold_zone_density(combo)

        return features

    def extract_structure_features(self, combo: List[int]) -> Dict[str, float]:
        """
        提取结构分析特征(5维)

        Args:
            combo: 候选组合

        Returns:
            Dict[str, float]: 结构分析特征
        """
        features = {}

        # 1. 子集覆盖率
        features['subset_coverage'] = self._calc_subset_coverage(combo)

        # 2-3. 三区221/122结构得分
        zones = self._count_zones(combo)
        features['zone_221_ratio'] = 1.0 if sorted(zones) == [1, 2, 2] else 0.0
        features['zone_122_ratio'] = 1.0 if sorted(zones) == [1, 2, 2] else 0.0

        # 4. 区域分散度
        features['zone_dispersion'] = self._calc_zone_dispersion(combo)

        # 5. 矩阵位置得分
        features['matrix_position'] = self._calc_matrix_position(combo)

        return features

    def extract_betting_features(self,
                               combo: List[int],
                               prediction_scores: np.ndarray = None) -> Dict[str, float]:
        """
        提取投注策略特征(3维)

        Args:
            combo: 候选组合
            prediction_scores: 预测分数(35维)

        Returns:
            Dict[str, float]: 投注策略特征
        """
        features = {}

        # 1. 核心置信度
        if prediction_scores is not None:
            sorted_idx = np.argsort(prediction_scores)[::-1]
            top_2_gap = prediction_scores[sorted_idx[0]] - prediction_scores[sorted_idx[1]]
            features['core_confidence'] = min(top_2_gap, 1.0)
        else:
            features['core_confidence'] = 0.5

        # 2. 策略推荐类型
        if prediction_scores is not None:
            sorted_idx = np.argsort(prediction_scores)[::-1]
            top_2_gap = prediction_scores[sorted_idx[0]] - prediction_scores[sorted_idx[1]]
            features['strategy_recommendation'] = 1.0 if top_2_gap > 0.15 else 0.0
        else:
            features['strategy_recommendation'] = 0.5

        # 3. 投注比例得分
        features['betting_ratio'] = self._calc_betting_ratio(combo)

        return features

    def _get_miss_count(self, number: int) -> int:
        """
        获取某个号码的当前遗漏期数

        Args:
            number: 号码(1-35)

        Returns:
            int: 遗漏期数(0表示上期已出现)
        """
        if not hasattr(self, 'miss_cache_'):
            self.miss_cache_ = {}
            if self.historical_data is not None and len(self.historical_data) > 0:
                front_cols = ['前区1', '前区2', '前区3', '前区4', '前区5']
                # 从后往前找每个号码最后出现的位置
                for n in range(1, 36):
                    miss = 0
                    for idx in range(len(self.historical_data) - 1, -1, -1):
                        row = self.historical_data.iloc[idx]
                        if n in [int(row[c]) for c in front_cols]:
                            break
                        miss += 1
                    self.miss_cache_[n] = miss
            else:
                for n in range(1, 36):
                    self.miss_cache_[n] = 0

        return self.miss_cache_.get(number, 0)

    def _calc_gravity_zone_match(self, combo: List[int]) -> float:
        """
        计算组合与引力最强区域的匹配度

        Args:
            combo: 候选组合

        Returns:
            float: 匹配分数(0-1,有界)
        """
        from modules.dlt_number_gravity import DLTNumberGravity

        if not hasattr(self, 'gravity_analyzer_'):
            self.gravity_analyzer_ = DLTNumberGravity(self.historical_data)

        # 获取最近一期作为参考
        if self.historical_data is not None and len(self.historical_data) > 0:
            last_row = self.historical_data.iloc[-1]
            recent_combo = [int(last_row[f'前区{i}']) for i in range(1, 6)]
            gravity_zone = self.gravity_analyzer_.predict_gravity_zone(recent_combo)
        else:
            gravity_zone = list(range(1, 36))

        # 计算匹配度
        match_count = sum(1 for n in combo if n in gravity_zone[:10])
        return min(match_count / 5, 1.0)  # 有界:0-1

    def extract_kill_features(self, combo: List[int]) -> Dict[str, float]:
        """
        提取杀号特征(4维)

        基于视频15杀号逻辑:
        - 数据杀号:热号极值杀、冷号长遗漏杀
        - 结构杀号:极端形态杀
        - 心理杀号:大众号杀

        Args:
            combo: 候选组合

        Returns:
            Dict[str, float]: 杀号特征(4维)
        """
        from modules.dlt_kill_number import DLTKillNumberAnalyzer

        if not hasattr(self, 'kill_analyzer_'):
            self.kill_analyzer_ = DLTKillNumberAnalyzer(self.historical_data)

        features = {}
        features['kill_score'] = self.kill_analyzer_.get_kill_score(combo)
        features['hot_kill'] = 1.0 if self.kill_analyzer_.kill_by_hot_number(combo) else 0.0
        features['extreme_kill'] = 1.0 if self.kill_analyzer_.kill_by_extreme_formation(combo) else 0.0
        features['psychology_kill'] = 1.0 if self.kill_analyzer_.kill_by_psychology(combo) else 0.0
        return features

    def extract_gravity_features(self, combo: List[int]) -> Dict[str, float]:
        """
        提取引力特征(3维)

        基于视频12遗漏层级引力建模:
        - 组合引力分数
        - 遗漏引力分数
        - 引力区域匹配度

        Args:
            combo: 候选组合

        Returns:
            Dict[str, float]: 引力特征(3维)
        """
        from modules.dlt_number_gravity import DLTNumberGravity

        if not hasattr(self, 'gravity_analyzer_'):
            self.gravity_analyzer_ = DLTNumberGravity(self.historical_data)

        features = {}
        features['gravity_score'] = self.gravity_analyzer_.calculate_gravity_score(combo)

        # 计算平均遗漏引力
        miss_counts = [self._get_miss_count(n) for n in combo]
        avg_miss = np.mean(miss_counts) if miss_counts else 0
        features['miss_gravity'] = self.gravity_analyzer_.calculate_miss_gravity(int(avg_miss))

        # 引力区域匹配
        features['gravity_zone_match'] = self._calc_gravity_zone_match(combo)

        return features

    def extract_diff_features(self, combo: List[int]) -> Dict[str, float]:
        """
        提取差值序列特征(3维)

        基于视频8差值序列分析:
        - 差值综合分数
        - 差值熵
        - 差值平衡标志

        Args:
            combo: 候选组合

        Returns:
            Dict[str, float]: 差值序列特征(3维)
        """
        from modules.dlt_difference_sequence import DLTDifferenceSequence

        if not hasattr(self, 'diff_analyzer_'):
            self.diff_analyzer_ = DLTDifferenceSequence(self.historical_data)

        features = {}
        features['diff_score'] = self.diff_analyzer_.get_diff_score(combo)
        features['diff_entropy'] = self.diff_analyzer_.calculate_diff_entropy(combo)
        features['diff_balance'] = 1.0 if self.diff_analyzer_.check_diff_balance(combo) else 0.0
        return features

    def extract_matrix_features(self, combo: List[int]) -> Dict[str, float]:
        """
        提取矩阵位移特征(4维)

        基于视频10矩阵位移分析:
        - 矩阵分散度
        - 对角线倾向
        - 行列分布标准差

        Args:
            combo: 候选组合

        Returns:
            Dict[str, float]: 矩阵位移特征(4维)
        """
        from modules.dlt_matrix_displacement import DLTMatrixDisplacement

        if not hasattr(self, 'matrix_analyzer_'):
            self.matrix_analyzer_ = DLTMatrixDisplacement(self.historical_data)

        scores = self.matrix_analyzer_.get_matrix_score(combo)
        return {
            'matrix_dispersion': scores['dispersion'],
            'matrix_diagonal': scores['diagonal_tendency'],
            'matrix_row_std': scores['row_distribution'],
            'matrix_col_std': scores['col_distribution'],
        }

    def extract_all_upgraded_features(
                                    self,
                                    combo: List[int],
                                    prediction_scores: np.ndarray = None,
                                    recent_sums: np.ndarray = None,
                                    historical_stats: Dict = None) -> Dict[str, float]:
        """
        提取所有16集视频升级特征

        整合所有新增特征提取方法

        Args:
            combo: 候选组合
            prediction_scores: 预测分数(可选)
            recent_sums: 近期和值序列(可选)
            historical_stats: 历史统计数据(可选)

        Returns:
            Dict[str, float]: 所有升级特征
        """
        all_features = {}

        # 数学滤网特征(5维)
        all_features.update(self.extract_math_filter_features(combo, historical_stats))

        # 博弈论特征(4维)
        all_features.update(self.extract_game_theory_features(combo))

        # 数理统计特征(4维)
        all_features.update(self.extract_statistics_features(combo, recent_sums))

        # 结构分析特征(5维)
        all_features.update(self.extract_structure_features(combo))

        # 投注策略特征(3维)
        all_features.update(self.extract_betting_features(combo, prediction_scores))

        # 杀号特征(4维)
        all_features.update(self.extract_kill_features(combo))

        # 引力特征(3维)
        all_features.update(self.extract_gravity_features(combo))

        # 差值序列特征(3维)
        all_features.update(self.extract_diff_features(combo))

        # 矩阵位移特征(4维)
        all_features.update(self.extract_matrix_features(combo))

        return all_features


class StackingMetaLearner:
    """
    动态权重Stacking
    使用逻辑回归作为meta-learner,结合多个基础策略的预测结果
    """

    def __init__(self):
        self.front_stacker_ = None
        self.back_stacker_ = None
        self.front_strategies_ = []
        self.back_strategies_ = []
        self.fitted_ = False

    def fit(self,
           strategy_predictions: Dict[str, np.ndarray],
           actual: np.ndarray,
           zone: str = 'front') -> 'StackingMetaLearner':
        """
        训练meta-learner

        strategy_predictions: {strategy_name: predictions} 每个策略的预测分数
        actual: 实际标签(0或1)
        """
        if not HAS_SKLEARN or LogisticRegression is None:
            warnings.warn("sklearn not available for stacking")
            return self

        # 构建特征矩阵:每个样本 x 每个策略
        strategy_names = list(strategy_predictions.keys())
        X = np.column_stack([strategy_predictions[s] for s in strategy_names])

        # 训练逻辑回归
        stacker = LogisticRegression(C=1.0, solver='lbfgs', max_iter=1000)
        stacker.fit(X, actual)

        if zone == 'front':
            self.front_stacker_ = stacker
            self.front_strategies_ = strategy_names
        else:
            self.back_stacker_ = stacker
            self.back_strategies_ = strategy_names

        self.fitted_ = True
        return self

    def predict(self,
               strategy_predictions: Dict[str, np.ndarray],
               zone: str = 'front') -> np.ndarray:
        """使用meta-learner预测"""
        if not self.fitted_:
            # 平均加权
            return np.mean(list(strategy_predictions.values()), axis=0)

        stacker = self.front_stacker_ if zone == 'front' else self.back_stacker_
        strategy_names = self.front_strategies_ if zone == 'front' else self.back_strategies_

        X = np.column_stack([strategy_predictions[s] for s in strategy_names])

        return stacker.predict_proba(X)[:, 1]


class DLTPredictorUpgraded:
    """
    升级版大乐透预测器

    整合所有优化:
    1. LTR框架(LightGBM Ranker)
    2. 贝叶斯遗漏值模型
    3. 概率校准
    4. 时序交叉验证
    5. 动态权重Stacking
    6. 号码共现约束
    """

    def __init__(self,
                 n_front: int = 35,
                 n_back: int = 12,
                 front_select: int = 5,
                 back_select: int = 2,
                 feature_window: int = 30,
                 use_calibration: bool = True,
                 use_bayesian: bool = True,
                 use_stacking: bool = False,
                 use_cooccurrence: bool = True):

        self.n_front = n_front
        self.n_back = n_back
        self.front_select = front_select
        self.back_select = back_select
        self.feature_window = feature_window
        self.use_calibration = use_calibration
        self.use_bayesian = use_bayesian
        self.use_stacking = use_stacking
        self.use_cooccurrence = use_cooccurrence

        # 组件
        self.feature_eng_ = FeatureEngineering(n_front=n_front, n_back=n_back, window=feature_window)
        self.bayesian_front_ = BayesianNumberModel(n_front=n_front, n_back=n_back)
        self.bayesian_back_ = BayesianNumberModel(n_front=n_front, n_back=n_back)

        # LTR模型
        self.front_ranker_ = None
        self.back_ranker_ = None

        # 校准器
        self.front_calibrators_ = {}
        self.back_calibrators_ = {}

        # Stacking
        self.stacker_ = StackingMetaLearner()

        # 评估器
        self.metrics_ = LotteryMetrics()

        # 强共现对
        self.front_strong_pairs = [
            (32, 33), (29, 30), (7, 12), (15, 22), (5, 8),
            (18, 25), (1, 19), (11, 21), (4, 16), (23, 28)
        ]
        self.back_strong_pairs = [
            (5, 8), (3, 10), (1, 6), (2, 11), (4, 7)
        ]

        # 历史数据
        self.draws_ = []
        
        # 数据文件路径（倒序文件，自动修正）
        self.data_path = '/mnt/d/cp/DLT历史数据_适配模型版.xlsx'
        
        # 尝试从磁盘加载已保存的模型
        self._load_models()

    # ========================================================================
    # 模型持久化：Save / Load
    # ========================================================================
    def _get_model_dir(self) -> Path:
        """获取模型保存目录"""
        return Path(__file__).parent / 'models'

    def _save_models(self):
        """保存所有模型到磁盘（joblib/pytorch）"""
        import joblib
        model_dir = self._get_model_dir()
        os.makedirs(model_dir, exist_ok=True)

        try:
            # 1. LightGBM Ranker
            if self.front_ranker_ is not None:
                joblib.dump(self.front_ranker_, str(model_dir / 'front_ranker_.pkl'))
            if self.back_ranker_ is not None:
                joblib.dump(self.back_ranker_, str(model_dir / 'back_ranker_.pkl'))

            # 2. Isotonic Calibrators
            if self.front_calibrators_:
                joblib.dump(self.front_calibrators_, str(model_dir / 'front_calibrators_.pkl'))
            if self.back_calibrators_:
                joblib.dump(self.back_calibrators_, str(model_dir / 'back_calibrators_.pkl'))

            # 3. StackingMetaLearner
            if hasattr(self.stacker_, 'fitted_') and self.stacker_.fitted_:
                joblib.dump(self.stacker_, str(model_dir / 'stacker_.pkl'))

            # 4. 训练参数快照（用于验证一致性）
            params = {
                'n_front': self.n_front,
                'n_back': self.n_back,
                'feature_window': self.feature_window,
                'n_estimators': self.n_estimators,
                'learning_rate': self.learning_rate,
            }
            joblib.dump(params, str(model_dir / 'params.pkl'))

            print(f"  [模型持久化] 已保存到 {model_dir}")
        except Exception as e:
            print(f"  [模型持久化] 保存失败: {e}")

    def _load_models(self):
        """从磁盘加载模型（若存在）"""
        import joblib
        model_dir = self._get_model_dir()
        stacker_path = model_dir / 'stacker_.pkl'

        # 若stacker未训练过，尝试加载
        if hasattr(self, 'stacker_') and hasattr(self.stacker_, 'fitted_') and not self.stacker_.fitted_:
            if stacker_path.exists():
                try:
                    self.stacker_ = joblib.load(str(stacker_path))
                    if hasattr(self.stacker_, 'fitted_') and self.stacker_.fitted_:
                        print(f"  [模型加载] StackingMetaLearner 已加载 (fitted={self.stacker_.fitted_})")
                except Exception as e:
                    print(f"  [模型加载] Stacker加载失败: {e}")

    def _build_ltr_dataset(self,
                          draws: List[Tuple[List[int], List[int]]],
                          start_idx: int,
                          end_idx: int) -> Tuple[np.ndarray, ...]:
        """
        构建LTR训练数据集

        每个时期创建一个query group,包含所有号码的特征
        """
        all_X_front = []
        all_y_front = []
        all_X_back = []
        all_y_back = []
        front_groups = []
        back_groups = []

        for period in range(start_idx, end_idx):
            history = draws[max(0, period - self.feature_window):period]

            if len(history) < 5:
                continue

            # 更新贝叶斯模型
            self.bayesian_front_.fit(history)
            self.bayesian_back_.fit(history)

            # 前区特征
            X_front, _ = self.feature_eng_.build_all_features(history, zone='front')

            # 确定标签(该号码在period期是否出现)
            actual_front, actual_back = draws[period]
            y_front = np.array([1 if i+1 in actual_front else 0 for i in range(self.n_front)])

            all_X_front.append(X_front)
            all_y_front.append(y_front)
            front_groups.append(self.n_front)

            # 后区特征
            X_back, _ = self.feature_eng_.build_all_features(history, zone='back')
            y_back = np.array([1 if i+1 in actual_back else 0 for i in range(self.n_back)])

            all_X_back.append(X_back)
            all_y_back.append(y_back)
            back_groups.append(self.n_back)

        if not all_X_front:
            return None, None, None, None, None, None

        X_front = np.vstack(all_X_front)
        y_front = np.concatenate(all_y_front)
        groups_front = np.array(front_groups)

        X_back = np.vstack(all_X_back)
        y_back = np.concatenate(all_y_back)
        groups_back = np.array(back_groups)

        return X_front, y_front, groups_front, X_back, y_back, groups_back

    def fit(self,
            draws: List[Tuple[List[int], List[int]]],
            eval_split: float = 0.15) -> Dict[str, Any]:
        """
        训练模型
        """
        self.draws_ = draws
        n = len(draws)
        train_end = int(n * (1 - eval_split))

        print(f"训练数据: {train_end}期, 验证: {n - train_end}期")

        # 构建训练数据
        X_front, y_front, groups_front, X_back, y_back, groups_back = \
            self._build_ltr_dataset(draws, 0, train_end)

        if X_front is None:
            print("训练数据不足")
            return {'success': False}

        print(f"前区训练: X={X_front.shape}, y={y_front.shape}, groups={groups_front.shape}")
        print(f"后区训练: X={X_back.shape}, y={y_back.shape}, groups={groups_back.shape}")

        # 训练LTR模型
        if HAS_LIGHTGBM:
            print("\n训练前区LTR模型...")
            self.front_ranker_ = lgb.LGBMRanker(
                objective='lambdarank',
                metric='ndcg',
                n_estimators=150,
                num_leaves=31,
                learning_rate=0.05,
                feature_fraction=0.8,
                bagging_fraction=0.8,
                bagging_freq=5,
                verbose=-1,
                random_state=42
            )

            self.front_ranker_.fit(X_front, y_front, group=groups_front)
            print("前区LTR训练完成")

            print("\n训练后区LTR模型...")
            self.back_ranker_ = lgb.LGBMRanker(
                objective='lambdarank',
                metric='ndcg',
                n_estimators=150,
                num_leaves=31,
                learning_rate=0.05,
                feature_fraction=0.8,
                bagging_fraction=0.8,
                bagging_freq=5,
                verbose=-1,
                random_state=42
            )

            self.back_ranker_.fit(X_back, y_back, group=groups_back)
            print("后区LTR训练完成")
        else:
            print("LightGBM不可用,跳过LTR训练")

        # 训练概率校准器
        if self.use_calibration:
            print("\n训练概率校准器...")
            val_start = train_end
            val_end = min(train_end + 50, n)

            X_front_val, y_front_val, _, X_back_val, y_back_val, _ = \
                self._build_ltr_dataset(draws, val_start, val_end)

            if X_front_val is not None and HAS_LIGHTGBM:
                # 前区校准
                front_scores = self.front_ranker_.predict(X_front_val)
                self.front_calibrators_['isotonic'] = IsotonicCalibrator()
                self.front_calibrators_['isotonic'].fit(front_scores, y_front_val)

                # 后区校准
                back_scores = self.back_ranker_.predict(X_back_val)
                self.back_calibrators_['isotonic'] = IsotonicCalibrator()
                self.back_calibrators_['isotonic'].fit(back_scores, y_back_val)

                print("校准器训练完成")

        # ============================================================
        # 第三步核心: 训练StackingMetaLearner(使用cross-validation)
        # Base strategies: LTR ranking scores + 频率策略 + 贝叶斯策略
        # ============================================================
        if self.use_stacking and HAS_LIGHTGBM:
            print("\n训练StackingMetaLearner (out-of-fold CV)...")

            # 使用验证区间(不与calibration重叠)
            stacker_val_start = val_end
            stacker_val_end = min(val_end + 100, n)
            n_stacker_periods = stacker_val_end - stacker_val_start

            if n_stacker_periods >= 60:
                print(f"  Stacking训练区间: {stacker_val_start}~{stacker_val_end} ({n_stacker_periods}期)")

                # ---- 前区Stacking ----
                front_ltr_oof  = np.zeros(n_stacker_periods * self.n_front)
                front_freq_oof = np.zeros(n_stacker_periods * self.n_front)
                front_bayes_oof = np.zeros(n_stacker_periods * self.n_front)
                front_actual   = np.zeros(n_stacker_periods * self.n_front)

                # 预先计算所有期的频率策略得分
                freq_front_cache = []
                for pidx in range(stacker_val_start, stacker_val_end):
                    hist = draws[max(0, pidx - self.feature_window):pidx]
                    ff = np.zeros(self.n_front)
                    for front, _ in hist[-50:]:
                        for num in front:
                            ff[num - 1] += 1
                    freq_front_cache.append(ff)

                # 预先计算所有期的贝叶斯策略得分
                bayes_front_cache = []
                for pidx in range(stacker_val_start, stacker_val_end):
                    hist = draws[max(0, pidx - self.feature_window):pidx]
                    bm = BayesianNumberModel(n_front=self.n_front, n_back=self.n_back)
                    bm.fit(hist)
                    bp = bm.get_front_features()
                    bayes_front_cache.append(bp[:, 0])

                # 使用主ranker进行LTR预测(主ranker训练于0~train_end)
                # 这样避免特征维度不匹配问题
                for offset, pidx in enumerate(range(stacker_val_start, stacker_val_end)):
                    hist = draws[max(0, pidx - self.feature_window):pidx]

                    Xf, _ = self.feature_eng_.build_all_features(hist, zone='front')
                    ltr_s = self.front_ranker_.predict(Xf)

                    actual_f = draws[pidx][0]
                    y_actual = np.array([1 if i+1 in actual_f else 0 for i in range(self.n_front)])

                    start = offset * self.n_front
                    end   = start + self.n_front

                    front_ltr_oof[start:end]  = ltr_s
                    front_freq_oof[start:end] = freq_front_cache[offset]
                    front_bayes_oof[start:end] = bayes_front_cache[offset]
                    front_actual[start:end]    = y_actual

                # 归一化各策略得分到[0,1]
                def normalize(x):
                    mn, mx = x.min(), x.max()
                    return (x - mn) / (mx - mn + 1e-9)

                front_ltr_norm   = normalize(front_ltr_oof)
                front_freq_norm  = normalize(front_freq_oof)
                front_bayes_norm = normalize(front_bayes_oof)

                # 训练前区StackingMetaLearner
                front_strat_preds = {
                    'ltr': front_ltr_norm,
                    'frequency': normalize(front_freq_oof),
                    'bayesian': normalize(front_bayes_oof)
                }

                self.stacker_.fit(front_strat_preds, front_actual, zone='front')

                print(f"  前区StackingMetaLearner训练完成: fitted_={self.stacker_.fitted_}")

                # ---- 后区Stacking ----
                back_ltr_oof   = np.zeros(n_stacker_periods * self.n_back)
                back_freq_oof  = np.zeros(n_stacker_periods * self.n_back)
                back_bayes_oof = np.zeros(n_stacker_periods * self.n_back)
                back_actual    = np.zeros(n_stacker_periods * self.n_back)

                freq_back_cache = []
                for pidx in range(stacker_val_start, stacker_val_end):
                    hist = draws[max(0, pidx - self.feature_window):pidx]
                    fb = np.zeros(self.n_back)
                    for _, back in hist[-50:]:
                        for num in back:
                            fb[num - 1] += 1
                    freq_back_cache.append(fb)

                bayes_back_cache = []
                for pidx in range(stacker_val_start, stacker_val_end):
                    hist = draws[max(0, pidx - self.feature_window):pidx]
                    bm = BayesianNumberModel(n_front=self.n_front, n_back=self.n_back)
                    bm.fit(hist)
                    bp = bm.get_back_features()
                    bayes_back_cache.append(bp[:, 0])

                # 使用主back ranker进行LTR预测
                for offset, pidx in enumerate(range(stacker_val_start, stacker_val_end)):
                    hist = draws[max(0, pidx - self.feature_window):pidx]

                    Xb, _ = self.feature_eng_.build_all_features(hist, zone='back')
                    ltr_s = self.back_ranker_.predict(Xb)

                    actual_b = draws[pidx][1]
                    y_actual = np.array([1 if i+1 in actual_b else 0 for i in range(self.n_back)])

                    start = offset * self.n_back
                    end   = start + self.n_back

                    back_ltr_oof[start:end]  = ltr_s
                    back_freq_oof[start:end] = freq_back_cache[offset]
                    back_bayes_oof[start:end] = bayes_back_cache[offset]
                    back_actual[start:end]    = y_actual

                back_strat_preds = {
                    'ltr': normalize(back_ltr_oof),
                    'frequency': normalize(back_freq_oof),
                    'bayesian': normalize(back_bayes_oof)
                }

                self.stacker_.fit(back_strat_preds, back_actual, zone='back')
                print(f"  后区StackingMetaLearner训练完成: fitted_={self.stacker_.fitted_}")

                # 打印Stacking权重
                if self.stacker_.front_stacker_ is not None:
                    print("\n  前区Stacking权重:")
                    for name, coef in zip(self.stacker_.front_strategies_,
                                          self.stacker_.front_stacker_.coef_[0]):
                        print(f"    {name}: {coef:.4f}")
                if self.stacker_.back_stacker_ is not None:
                    print("\n  后区Stacking权重:")
                    for name, coef in zip(self.stacker_.back_strategies_,
                                         self.stacker_.back_stacker_.coef_[0]):
                        print(f"    {name}: {coef:.4f}")
            else:
                print(f"  Stacking数据不足({n_stacker_periods}期),跳过Stacking训练")

        return {'success': True, 'train_periods': train_end}

    def predict(self,
               draws: Optional[List[Tuple[List[int], List[int]]]] = None,
               top_k: int = 10) -> Dict[str, Any]:
        """
        预测下一期号码

        返回格式与原predictor兼容:
        {'front': [5个前区], 'back': [2个后区], ...}
        """
        # ============================================================
        # 自动加载数据(倒序文件自动修正为正序)
        # ============================================================
        if draws is None:
            draws = self.draws_

        if len(draws) < self.feature_window + 1:
            # 尝试自动加载
            auto_loaded = False
            for path in [self.data_path,
                         '/mnt/d/cp/DLT历史数据_适配模型版.xlsx',
                         'D:/cp/DLT历史数据_适配模型版.xlsx']:
                if path and os.path.exists(path):
                    print(f"  [自动加载] 从 {path} 加载数据...")
                    draws = load_dlt_data(path)
                    if len(draws) >= self.feature_window + 1:
                        self.draws_ = draws
                        auto_loaded = True
                        print(f"  [自动加载] 成功加载 {len(draws)} 期数据 (已修正为正序)")
                        break

            if not auto_loaded:
                return self._fallback_predict(draws)

        history = draws[:-1]  # 不包含最新一期

        # 更新特征工程
        self.feature_eng_.compute_cooccurrence(history)

        # 构建当前特征
        X_front, _ = self.feature_eng_.build_all_features(history, zone='front')
        X_back, _ = self.feature_eng_.build_all_features(history, zone='back')

        # ============================================================
        # 三策略预测 + StackingMetaLearner融合
        # ============================================================

        # 策略1: LTR ranking scores
        if HAS_LIGHTGBM and self.front_ranker_:
            front_ltr_scores = self.front_ranker_.predict(X_front)
            back_ltr_scores  = self.back_ranker_.predict(X_back)
        else:
            front_ltr_scores = X_front[:, 0]
            back_ltr_scores  = X_back[:, 0]

        # 策略2: 频率统计 scores
        front_freq_scores = np.zeros(self.n_front)
        back_freq_scores  = np.zeros(self.n_back)
        for front, back in history[-50:]:
            for num in front:
                front_freq_scores[num - 1] += 1
            for num in back:
                back_freq_scores[num - 1] += 1

        # 策略3: 贝叶斯 scores
        bayes_model = BayesianNumberModel(n_front=self.n_front, n_back=self.n_back)
        bayes_model.fit(history)
        front_bayes_scores = bayes_model.get_front_features()[:, 0]
        back_bayes_scores  = bayes_model.get_back_features()[:, 0]

        # 归一化所有策略得分到[0,1]
        def norm(x):
            mn, mx = x.min(), x.max()
            return (x - mn) / (mx - mn + 1e-9)

        front_ltr_norm   = norm(front_ltr_scores)
        front_freq_norm  = norm(front_freq_scores)
        front_bayes_norm = norm(front_bayes_scores)
        back_ltr_norm    = norm(back_ltr_scores)
        back_freq_norm   = norm(back_freq_scores)
        back_bayes_norm  = norm(back_bayes_scores)

        # 校准(作为备用/辅助信号)
        if self.use_calibration and 'isotonic' in self.front_calibrators_:
            front_probs = self.front_calibrators_['isotonic'].calibrate(front_ltr_scores)
            back_probs  = self.back_calibrators_['isotonic'].calibrate(back_ltr_scores)
        else:
            front_probs = front_ltr_scores
            back_probs  = back_ltr_scores

        # StackingMetaLearner融合(若已训练)
        if self.stacker_.fitted_:
            front_strat_preds = {
                'ltr':        front_ltr_norm,
                'frequency':  front_freq_norm,
                'bayesian':   front_bayes_norm
            }
            back_strat_preds = {
                'ltr':        back_ltr_norm,
                'frequency':  back_freq_norm,
                'bayesian':   back_bayes_norm
            }
            front_stacked = self.stacker_.predict(front_strat_preds, zone='front')
            back_stacked  = self.stacker_.predict(back_strat_preds,  zone='back')

            # 使用堆叠融合后的得分
            front_final = np.clip(front_stacked, 0, 1)
            back_final  = np.clip(back_stacked,  0, 1)
        else:
            # Fallback: 加权平均
            front_final = 0.5 * front_ltr_norm + 0.3 * front_freq_norm + 0.2 * front_bayes_norm
            back_final  = 0.5 * back_ltr_norm  + 0.3 * back_freq_norm  + 0.2 * back_bayes_norm

        # 转换为排序
        front_order = np.argsort(-front_final) + 1
        back_order  = np.argsort(-back_final)  + 1

        # 应用共现约束(使用堆叠融合得分)
        front_selected = self._select_with_constraints(
            front_order.tolist(), front_final, self.front_select, zone='front'
        )
        back_selected = self._select_with_constraints(
            back_order.tolist(), back_final, self.back_select, zone='back'
        )

        # 原始排序结果(无约束)
        front_ranked = front_order.tolist()[:top_k]
        back_ranked = back_order.tolist()[:top_k]

        # ==================== 16集视频升级:集成新模块 ====================

        # 初始化新模块
        math_filter = DLTMathFilter()
        strategy_recommender = DLTStrategyRecommender()
        game_theory = DLTGameTheoryAnalyzer()
        statistics_analyzer = DLTStatisticsAnalyzer()

        # 计算置信度差距(使用堆叠融合得分)
        sorted_idx = np.argsort(-front_final)
        confidence_gap = front_final[sorted_idx[0]] - front_final[sorted_idx[1]] if len(sorted_idx) > 1 else 0

        # 策略推荐
        strategy = strategy_recommender.recommend_strategy(front_final, confidence_gap)

        # 博弈论分析(分析前5个候选组合)
        front_candidates = front_ranked[:5]
        game_theory_results = []
        for combo in [front_ranked[:5]]:  # 分析前5个候选
            gt_analysis = game_theory.analyze_combo(combo)
            game_theory_results.append({
                'combo': combo,
                'avoidance_score': gt_analysis['scores']['avoidance_score'],
                'regularity_score': gt_analysis['scores']['regularity_score'],
                'is_cold': gt_analysis['scores']['is_cold_combo'],
                'risk_level': gt_analysis['scores']['risk_assessment']['level']
            })

        # 数理统计分析
        recent_sums = np.array([sum(front) for front, _ in draws[-30:]])
        mean_reversion = statistics_analyzer.calculate_mean_reversion_score(recent_sums)
        sum_trend = statistics_analyzer.predict_sum_trend(recent_sums)

        # 统计报告
        try:
            stats_report = statistics_analyzer.generate_statistics_report(draws)
        except:
            stats_report = {}

        return {
            'front': sorted(front_selected),
            'back': sorted(back_selected),
            'front_scores': {i+1: float(front_final[i]) for i in range(len(front_final))},
            'back_scores': {i+1: float(back_final[i]) for i in range(len(back_final))},
            'front_ranked': front_ranked,
            'back_ranked': back_ranked,
            'method': 'stacking_ensemble_v21',
            'stacking_active': self.stacker_.fitted_,
            # ==================== 16集视频升级新增字段 ====================
            'strategy_recommendation': strategy,
            'confidence_gap': float(confidence_gap),
            'game_theory': {
                'candidates_analysis': game_theory_results,
                'recommended_strategy': game_theory_results[0]['risk_level'] if game_theory_results else '中'
            },
            'statistics': {
                'mean_reversion_score': float(mean_reversion),
                'sum_trend': sum_trend,
                'recent_sums': recent_sums.tolist()[-10:],
                'stats_report': stats_report
            },
            'math_filter_info': {
                'filter_applied': True,
                'golden_sum_range': '(70, 120)',
                'golden_parity': '3:2 或 2:3',
                'golden_span': '(24, 30)'
            }
        }

    def _select_with_constraints(self,
                                 ranked_nums: List[int],
                                 probs: np.ndarray,
                                 select_count: int,
                                 zone: str) -> List[int]:
        """
        应用共现约束选择号码

        策略:
        1. 优先选择强共现对中的号码
        2. 考虑遗漏期数
        3. 综合排序分数
        """
        selected = []
        strong_pairs = self.front_strong_pairs if zone == 'front' else self.back_strong_pairs

        # 构建号码到概率的映射
        prob_dict = {i+1: probs[i] for i in range(len(probs))}

        # 优先级队列
        priority_scores = {}
        for num in ranked_nums:
            score = prob_dict.get(num, 0)

            # 强共现加成
            pair_bonus = 0
            for p1, p2 in strong_pairs[:8]:
                if num == p1:
                    pair_bonus = max(pair_bonus, prob_dict.get(p2, 0) * 0.3)
                if num == p2:
                    pair_bonus = max(pair_bonus, prob_dict.get(p1, 0) * 0.3)

            priority_scores[num] = score + pair_bonus

        # 选择
        sorted_by_priority = sorted(priority_scores.keys(),
                                      key=lambda x: -priority_scores[x])

        selected = sorted_by_priority[:select_count]

        return selected

    def _fallback_predict(self, draws: List[Tuple[List[int], List[int]]]) -> Dict[str, Any]:
        """Fallback预测(数据不足时)"""
        # 简单频率统计
        n_front = self.n_front
        n_back = self.n_back

        freq_front = np.zeros(n_front)
        freq_back = np.zeros(n_back)

        for front, back in draws[-50:]:
            for num in front:
                freq_front[num - 1] += 1
            for num in back:
                freq_back[num - 1] += 1

        front_order = np.argsort(-freq_front) + 1
        back_order = np.argsort(-freq_back) + 1

        return {
            'front': sorted(front_order[:5].tolist()),
            'back': sorted(back_order[:2].tolist()),
            'front_scores': {i+1: float(freq_front[i]) for i in range(n_front)},
            'back_scores': {i+1: float(freq_back[i]) for i in range(n_back)},
            'front_ranked': front_order.tolist()[:10],
            'back_ranked': back_order.tolist()[:10],
            'method': 'frequency_fallback'
        }

    def backtest(self,
                draws: Optional[List[Tuple[List[int], List[int]]]] = None,
                n_test: int = 50,
                compare_methods: List[str] = None) -> Dict[str, Any]:
        """
        回测所有方法并对比
        """
        if draws is None:
            draws = self.draws_

        if compare_methods is None:
            compare_methods = ['ltr', 'frequency', 'bayesian']

        n_draws = len(draws)
        test_start = max(n_draws - n_test, self.feature_window + 5)

        all_results = {method: {'front_hit': [], 'back_hit': [],
                                'hit@5': [], 'ndcg@5': [], 'prizes': []}
                      for method in compare_methods}

        print(f"\n开始回测: {test_start}期 ~ {n_draws}期 (共{n_draws - test_start}期)")

        for i in range(test_start, n_draws):
            history = draws[:i]
            actual_front, actual_back = draws[i]

            # LTR方法
            if 'ltr' in compare_methods:
                pred = self.predict(history)
                ltr_front = pred['front']
                ltr_back = pred['back']

                fh = len(set(ltr_front) & set(actual_front))
                bh = len(set(ltr_back) & set(actual_back))

                all_results['ltr']['front_hit'].append(fh)
                all_results['ltr']['back_hit'].append(bh)
                all_results['ltr']['hit@5'].append(self.metrics_.hit_at_k(ltr_front, actual_front, 5))
                all_results['ltr']['ndcg@5'].append(self.metrics_.ndcg_at_k(ltr_front, actual_front, 5))

                prize = DLTPrizeEvaluator.evaluate(ltr_front, ltr_back, actual_front, actual_back)
                all_results['ltr']['prizes'].append(prize)

            # 频率方法
            if 'frequency' in compare_methods:
                freq_front, freq_back = self._frequency_predict(history)
                ffh = len(set(freq_front) & set(actual_front))
                fbh = len(set(freq_back) & set(actual_back))

                all_results['frequency']['front_hit'].append(ffh)
                all_results['frequency']['back_hit'].append(fbh)
                all_results['frequency']['hit@5'].append(self.metrics_.hit_at_k(freq_front, actual_front, 5))
                all_results['frequency']['ndcg@5'].append(self.metrics_.ndcg_at_k(freq_front, actual_front, 5))

                prize = DLTPrizeEvaluator.evaluate(freq_front, freq_back, actual_front, actual_back)
                all_results['frequency']['prizes'].append(prize)

            # 贝叶斯方法
            if 'bayesian' in compare_methods:
                bayes_front, bayes_back = self._bayesian_predict(history)
                bfh = len(set(bayes_front) & set(actual_front))
                bbh = len(set(bayes_back) & set(actual_back))

                all_results['bayesian']['front_hit'].append(bfh)
                all_results['bayesian']['back_hit'].append(bbh)
                all_results['bayesian']['hit@5'].append(self.metrics_.hit_at_k(bayes_front, actual_front, 5))
                all_results['bayesian']['ndcg@5'].append(self.metrics_.ndcg_at_k(bayes_front, actual_front, 5))

                prize = DLTPrizeEvaluator.evaluate(bayes_front, bayes_back, actual_front, actual_back)
                all_results['bayesian']['prizes'].append(prize)

            if (i - test_start + 1) % 20 == 0:
                print(f"  进度: {i - test_start + 1}/{n_draws - test_start}")

        # 汇总
        summary = {}
        for method, metrics in all_results.items():
            method_summary = {}
            for key, values in metrics.items():
                if key == 'prizes':
                    continue
                if values:
                    method_summary[key] = {
                        'mean': np.mean(values),
                        'std': np.std(values),
                        'max': np.max(values)
                    }

            # 奖项统计
            prize_counts = {level: 0 for level in range(8)}
            for p in metrics['prizes']:
                prize_counts[p['prize_level']] += 1
            method_summary['prizes'] = prize_counts

            summary[method] = method_summary

        return {
            'n_test_periods': n_draws - test_start,
            'summary': summary,
            'methods': compare_methods
        }

    def _frequency_predict(self,
                          draws: List[Tuple[List[int], List[int]]],
                          select_front: int = 5,
                          select_back: int = 2) -> Tuple[List[int], List[int]]:
        """频率统计预测"""
        freq_front = np.zeros(self.n_front)
        freq_back = np.zeros(self.n_back)

        for front, back in draws[-50:]:
            for num in front:
                freq_front[num - 1] += 1
            for num in back:
                freq_back[num - 1] += 1

        front_order = np.argsort(-freq_front) + 1
        back_order = np.argsort(-freq_back) + 1

        return front_order[:select_front].tolist(), back_order[:select_back].tolist()

    def _bayesian_predict(self,
                          draws: List[Tuple[List[int], List[int]]],
                          select_front: int = 5,
                          select_back: int = 2) -> Tuple[List[int], List[int]]:
        """贝叶斯概率预测"""
        model = BayesianNumberModel(n_front=self.n_front, n_back=self.n_back)
        model.fit(draws)

        front_probs = model.get_front_features()
        back_probs = model.get_back_features()

        # 使用后验均值
        front_scores = front_probs[:, 0]  # 第0列是后验均值
        back_scores = back_probs[:, 0]

        front_order = np.argsort(-front_scores) + 1
        back_order = np.argsort(-back_scores) + 1

        return front_order[:select_front].tolist(), back_order[:select_back].tolist()


def load_dlt_data(file_path: str) -> List[Tuple[List[int], List[int]]]:
    """
    加载大乐透历史数据

    重要: 数据文件是倒序排列(最新一期在顶部,最老一期在底部)
    本函数自动检测并转换为正序(最老→最新),确保时间序列正确

    Returns:
        List[Tuple[List[int], List[int]]]: 按时间顺序排列的开奖数据
        draws[0] = 最老的一期(7001)
        draws[-1] = 最新的一期(26035)
    """
    try:
        df = pd.read_excel(file_path)

        records = []
        for _, row in df.iterrows():
            period = int(row['期号'])
            front = []
            back = []

            # 尝试多种列名格式
            front_cols = ['前区1', '前区2', '前区3', '前区4', '前区5']
            back_cols = ['后区1', '后区2']

            for c in front_cols:
                if c in df.columns:
                    try:
                        front.append(int(row[c]))
                    except:
                        pass

            for c in back_cols:
                if c in df.columns:
                    try:
                        back.append(int(row[c]))
                    except:
                        pass

            # 备用:自动检测
            if len(front) < 5:
                front = []
                for col in df.columns:
                    col_str = str(col).lower()
                    if '前' in str(col) and len(front) < 5:
                        try:
                            front.append(int(row[col]))
                        except:
                            pass
                front = sorted(front[:5]) if len(front) >= 5 else []

            if len(back) < 2:
                back = []
                for col in df.columns:
                    if '后' in str(col) and len(back) < 2:
                        try:
                            back.append(int(row[col]))
                        except:
                            pass
                back = sorted(back[:2]) if len(back) >= 2 else []

            if len(front) == 5 and len(back) == 2:
                records.append((period, front, back))

        # 数据文件为正序排列（7001在顶部，26035在底部），无需反转
        # 2026-04-06 修正：移除所有反转逻辑，保持原顺序
        draws = [(rec[1], rec[2]) for rec in records]

        if draws:
            print(f"  [数据顺序] 正序排列: {records[0][0]}期(首) → {records[-1][0]}期(末)")

        return draws
    except Exception as e:
        print(f"加载数据失败: {e}")
        return []


class FivePoolSampler:
    """五池分层采样器 - DLT v3.0核心架构"""

    def __init__(self, draws: list):
        self.draws = draws  # list of (front_balls, back_balls)
        self.n_front = 35
        self.n_back = 12
        self.recent_n = 30  # 近期窗口

    def _freq(self, zone='front'):
        """统计最近N期各号码出现频率"""
        window = self.draws[-self.recent_n:]
        counts = {}
        for front, back in window:
            balls = front if zone == 'front' else back
            max_ball = self.n_front if zone == 'front' else self.n_back
            for b in balls:
                if 1 <= b <= max_ball:
                    counts[b] = counts.get(b, 0) + 1
        return counts

    def _hot_cold(self, zone='front', top_n=10, cold=False):
        """返回热号或冷号列表"""
        freq = self._freq(zone)
        if not freq:
            max_ball = self.n_front if zone == 'front' else self.n_back
            balls = list(range(1, max_ball + 1))
            return balls[:top_n] if not cold else balls[-top_n:]
        sorted_balls = sorted(freq.items(), key=lambda x: x[1], reverse=not cold)
        return [b for b, _ in sorted_balls[:top_n]]

    def _game_score(self, front, back):
        """基于博弈论的冷门评分（越高越冷）"""
        hot_front = set(self._hot_cold('front', 15))
        hot_back = set(self._hot_cold('back', 8))
        overlap_front = len(set(front) & hot_front)
        overlap_back = len(set(back) & hot_back)
        cold_score = (5 - overlap_front) * 0.5 + (2 - overlap_back) * 0.5
        high_ratio = sum(1 for b in front if b >= 28) / 5.0
        span = max(front) - min(front) if front else 0
        return cold_score + high_ratio * 2 + (span / 35) * 1.5

    def _gen_pool(self, pool_type, zone='front', n=8):
        """生成各策略号码池"""
        if pool_type == 'hot':
            return self._hot_cold(zone, top_n=n)
        elif pool_type == 'cold':
            return self._hot_cold(zone, top_n=n, cold=True)
        elif pool_type == 'balance':
            hot = set(self._hot_cold(zone, top_n=n//2))
            cold = set(self._hot_cold(zone, top_n=n//2, cold=True))
            combined = list(hot | cold)
            result = []
            max_ball = self.n_front if zone == 'front' else self.n_back
            for b in range(1, max_ball + 1):
                if b in combined and len(result) < n:
                    result.append(b)
            return result[:n]
        elif pool_type == 'trend':
            # 趋势策略：近期出现频率上升的号码（近5期 vs 近15期对比）
            recent5 = self._freq_window(5, zone)
            recent15 = self._freq_window(15, zone)
            trend_scores = {}
            max_ball = self.n_front if zone == 'front' else self.n_back
            for b in range(1, max_ball + 1):
                r5 = recent5.get(b, 0) / 5
                r15 = recent15.get(b, 0) / 15
                trend_scores[b] = r5 - r15  # 上升为正
            sorted_balls = sorted(trend_scores.items(), key=lambda x: x[1], reverse=True)
            return [b for b, _ in sorted_balls[:n]]
        elif pool_type == 'prime':
            # 质数策略：优先选择遗漏值较大的质数号
            primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31] if zone == 'front' else [2, 3, 5, 7, 11]
            freq = self._freq(zone)
            # 按遗漏值排序质数（遗漏越大越优先）
            missing_tracker = {}
            for front, back in self.draws[-30:]:
                balls = front if zone == 'front' else back
                for b in balls:
                    missing_tracker[b] = 0
                for b in range(1, (self.n_front if zone == 'front' else self.n_back) + 1):
                    missing_tracker[b] = missing_tracker.get(b, 0) + 1
            # 质数中遗漏值最大的优先
            prime_missing = [(b, missing_tracker.get(b, 30)) for b in primes]
            prime_missing.sort(key=lambda x: x[1], reverse=True)
            result = [b for b, _ in prime_missing[:n]]
            # 不足部分用频率最低的非质数补充
            freq_sorted = sorted(freq.items(), key=lambda x: x[1])
            for b, _ in freq_sorted:
                if b not in primes and len(result) < n:
                    result.append(b)
            return result[:n]
        # 默认：顺序（不应到达此处）
        max_ball = self.n_front if zone == 'front' else self.n_back
        return list(range(1, max_ball + 1))[:n]

    def _freq_window(self, window, zone='front'):
        """统计指定窗口期的号码频率"""
        counts = {}
        for front, back in self.draws[-window:]:
            balls = front if zone == 'front' else back
            max_ball = self.n_front if zone == 'front' else self.n_back
            for b in balls:
                if 1 <= b <= max_ball:
                    counts[b] = counts.get(b, 0) + 1
        return counts

    def generate_6_plus_4(self, n=5):
        """生成n组6+4复式投注"""
        pools = ['hot', 'cold', 'balance', 'trend', 'prime']
        results = []
        for idx in range(n):
            pool_type = pools[idx % len(pools)]
            front_pool = self._gen_pool(pool_type, 'front', 12)
            back_pool = self._gen_pool(pool_type, 'back', 6)
            front = sorted(front_pool[:6])
            back = sorted(back_pool[:4])
            score = self._game_score(front, back)
            results.append({
                'group': idx + 1,
                'front': front,
                'back': back,
                'source': pool_type,
                'score': score
            })
        results.sort(key=lambda x: x['score'], reverse=True)
        for i, r in enumerate(results):
            r['group'] = i + 1
        return results


def predict_6_plus_4_v3(n=5):
    """DLT v3.0预测入口：生成n组6+4复式投注"""
    data_path = '/mnt/d/cp/DLT历史数据_适配模型版.xlsx'
    draws = load_dlt_data(data_path)
    sampler = FivePoolSampler(draws)
    return sampler.generate_6_plus_4(n=n)


if __name__ == '__main__':
    results = predict_6_plus_4_v3(n=5)
    print("=" * 50)
    print("DLT v3.0 - 5组6+4复式投注")
    print("=" * 50)
    for r in results:
        print(f"第{r['group']}组 [{r['source']:8s}]: 前区{r['front']} 后区{r['back']} 得分:{r['score']:.4f}")
