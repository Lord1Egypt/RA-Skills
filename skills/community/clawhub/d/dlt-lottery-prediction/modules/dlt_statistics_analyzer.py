#!/usr/bin/env python3
"""
DLT数理统计分析师
基于视频7的数理统计分析师
大数定律 + 均值回归 + 正态分布

核心概念:
- 冷热熵值: 衡量号码冷热分布的均匀程度
- 均值回归: 极端值最终会回归到均值附近
- 统计偏离度: 组合与历史均值的偏差程度
- 冷热号分类: 基于历史频率将号码分为热、温、冷

统计定律:
1. 大数定律: 长期来看，号码出现频率趋于理论概率
2. 均值回归: 偏离均值过大的组合会逐渐回归
3. 正态分布: 号码和值等统计量近似正态分布
"""

from typing import List, Dict, Any, Tuple
import numpy as np


class DLTStatisticsAnalyzer:
    """
    数理统计分析师
    
    运用统计学方法分析彩票数据，提供:
    1. 冷热熵值分析 - 衡量号码分布的均匀性
    2. 均值回归分析 - 预测和值回归趋势
    3. 统计偏离度分析 - 评估组合的偏离程度
    4. 冷热温号分类 - 将号码分为不同热度等级
    
    Args:
        window: 分析窗口大小（默认30期）
    """
    
    # 统计常量
    FRONT_NUMBER_COUNT = 5  # 前区号码个数
    BACK_NUMBER_COUNT = 2   # 后区号码个数
    FRONT_RANGE = (1, 35)   # 前区范围
    BACK_RANGE = (1, 12)    # 后区范围
    
    # 和值统计参数
    EXPECTED_SUM_MEAN = 95      # 期望和值均值
    EXPECTED_SUM_STD = 15       # 期望和值标准差
    GOLDEN_SUM_RANGE = (70, 120) # 黄金和值区间
    
    def __init__(self, window: int = 30):
        """
        初始化统计分析师
        
        Args:
            window: 分析窗口大小（期数），用于计算近期统计
        """
        self.window = window
        self.historical_stats = None
    
    def calculate_hot_cold_entropy(self, frequency: np.ndarray) -> float:
        """
        计算冷热熵值
        
        熵值越高表示号码分布越均匀（冷热号码差异小）
        熵值越低表示号码分布越集中（冷热号码差异大）
        
        使用香农熵公式: H = -Σp*log(p)
        
        Args:
            frequency: 号码出现频率数组
            
        Returns:
            float: 熵值（0-1归一化）
        """
        # 归一化频率
        freq_sum = np.sum(frequency)
        if freq_sum == 0:
            return 0.0
        
        p = frequency / freq_sum
        
        # 计算熵
        entropy = -np.sum(p * np.log(p + 1e-10))
        
        # 归一化到0-1
        n = len(frequency[frequency > 0])
        if n > 1:
            max_entropy = np.log(n)
            entropy = entropy / max_entropy if max_entropy > 0 else 0.0
        
        return entropy
    
    def calculate_mean_reversion_score(self, recent_sums: np.ndarray) -> float:
        """
        计算均值回归度
        
        根据当前和值与历史均值的偏离程度，
        预测未来回归的概率和强度
        
        Args:
            recent_sums: 近期和值序列
            
        Returns:
            float: 回归度分数（0-1）
            - 0.8: 强回归预期（|z| > 1.5）
            - 0.6: 中等回归预期（|z| > 1.0）
            - 0.4: 弱回归预期（|z| > 0.5）
            - 0.2: 无明显回归（|z| <= 0.5）
        """
        if len(recent_sums) < 10:
            return 0.5
        
        mean = np.mean(recent_sums)
        std = np.std(recent_sums)
        last_sum = recent_sums[-1]
        
        # 计算偏离度（Z分数）
        z_score = (last_sum - mean) / (std + 1e-10)
        
        # 回归分数：偏离越大，回归概率越高
        if abs(z_score) > 1.5:
            return 0.8  # 强回归预期
        elif abs(z_score) > 1.0:
            return 0.6
        elif abs(z_score) > 0.5:
            return 0.4
        else:
            return 0.2
    
    def calculate_statistical_deviation(self, 
                                       combo: List[int], 
                                       historical_mean: float, 
                                       historical_std: float) -> float:
        """
        计算统计偏离度
        
        评估组合和值与历史均值的偏离程度
        
        Args:
            combo: 候选组合
            historical_mean: 历史和值均值
            historical_std: 历史和值标准差
            
        Returns:
            float: 偏离度分数（绝对Z分数）
        """
        combo_sum = sum(combo)
        z_score = (combo_sum - historical_mean) / (historical_std + 1e-10)
        return abs(z_score)
    
    def classify_hot_cold(self, frequency: np.ndarray) -> Dict[str, np.ndarray]:
        """
        分类冷热温号
        
        基于75%和25%分位数将号码分为:
        - 热号: 频率 >= 75%分位数
        - 温号: 25% < 频率 < 75%分位数
        - 冷号: 0 < 频率 <= 25%分位数
        
        Args:
            frequency: 号码出现频率数组
            
        Returns:
            Dict: 包含hot, warm, cold三个数组的字典，
                 数组元素为号码索引（0-34对应1-35）
        """
        # 只考虑非零频率
        non_zero_freq = frequency[frequency > 0]
        if len(non_zero_freq) == 0:
            return {'hot': np.array([]), 'warm': np.array([]), 'cold': np.array([])}
        
        threshold_high = np.percentile(non_zero_freq, 75)
        threshold_low = np.percentile(non_zero_freq, 25)
        
        hot = np.where(frequency >= threshold_high)[0]
        cold = np.where((frequency > 0) & (frequency <= threshold_low))[0]
        warm = np.where((frequency > threshold_low) & (frequency < threshold_high))[0]
        
        return {'hot': hot, 'warm': warm, 'cold': cold}
    
    def analyze_frequency_distribution(self, 
                                       draws: List[Tuple[List[int], List[int]]]) -> Dict[str, Any]:
        """
        分析历史开奖的频率分布
        
        Args:
            draws: 历史开奖记录列表
            
        Returns:
            Dict: 频率分析结果
        """
        if not draws:
            return {}
        
        # 计算前区频率
        front_freq = np.zeros(35)
        back_freq = np.zeros(12)
        
        for front, back in draws:
            for num in front:
                front_freq[num - 1] += 1
            for num in back:
                back_freq[num - 1] += 1
        
        # 计算熵值
        front_entropy = self.calculate_hot_cold_entropy(front_freq)
        back_entropy = self.calculate_hot_cold_entropy(back_freq)
        
        # 分类冷热
        front_classification = self.classify_hot_cold(front_freq)
        back_classification = self.classify_hot_cold(back_freq)
        
        # 计算和值统计
        sums = [sum(front) for front, _ in draws[-self.window:]]
        sum_mean = np.mean(sums) if sums else self.EXPECTED_SUM_MEAN
        sum_std = np.std(sums) if sums else self.EXPECTED_SUM_STD
        
        return {
            'front_frequency': front_freq,
            'back_frequency': back_freq,
            'front_entropy': front_entropy,
            'back_entropy': back_entropy,
            'front_classification': {
                'hot': (front_classification['hot'] + 1).tolist(),  # 转为1-35
                'warm': (front_classification['warm'] + 1).tolist(),
                'cold': (front_classification['cold'] + 1).tolist()
            },
            'back_classification': {
                'hot': (back_classification['hot'] + 1).tolist(),  # 转为1-12
                'warm': (back_classification['warm'] + 1).tolist(),
                'cold': (back_classification['cold'] + 1).tolist()
            },
            'sum_statistics': {
                'mean': float(sum_mean),
                'std': float(sum_std),
                'recent_sums': sums
            }
        }
    
    def predict_sum_trend(self, recent_sums: np.ndarray) -> Dict[str, Any]:
        """
        预测和值趋势
        
        基于均值回归原理，预测未来和值走向
        
        Args:
            recent_sums: 近期和值序列
            
        Returns:
            Dict: 趋势预测结果
        """
        if len(recent_sums) < 10:
            return {
                'trend': 'insufficient_data',
                'message': '数据不足，无法预测'
            }
        
        mean = np.mean(recent_sums)
        std = np.std(recent_sums)
        last_sum = recent_sums[-1]
        z_score = (last_sum - mean) / (std + 1e-10)
        
        # 判断趋势
        if z_score > 1.5:
            trend = 'high_to_normal'
            message = f'和值({last_sum})显著高于均值({mean:.1f})，预计将回落'
            expected_range = (mean - std, mean + std)
        elif z_score < -1.5:
            trend = 'low_to_normal'
            message = f'和值({last_sum})显著低于均值({mean:.1f})，预计将回升'
            expected_range = (mean - std, mean + std)
        elif z_score > 0.5:
            trend = 'slightly_high'
            message = f'和值({last_sum})略高于均值({mean:.1f})，可能小幅回落'
            expected_range = (mean - 0.5*std, mean + std)
        elif z_score < -0.5:
            trend = 'slightly_low'
            message = f'和值({last_sum})略低于均值({mean:.1f})，可能小幅回升'
            expected_range = (mean - std, mean + 0.5*std)
        else:
            trend = 'neutral'
            message = f'和值({last_sum})接近均值({mean:.1f})，保持稳定'
            expected_range = (mean - 0.5*std, mean + 0.5*std)
        
        return {
            'trend': trend,
            'message': message,
            'z_score': float(z_score),
            'current_sum': int(last_sum),
            'mean': float(mean),
            'std': float(std),
            'expected_range': (float(expected_range[0]), float(expected_range[1])),
            'reversion_score': self.calculate_mean_reversion_score(recent_sums)
        }
    
    def evaluate_combo_statistical_score(self, 
                                        combo: List[int],
                                        historical_stats: Dict[str, Any]) -> float:
        """
        评估组合的统计得分
        
        综合考虑:
        1. 和值是否在黄金区间
        2. 和值偏离度
        3. 跨度是否合理
        4. 冷热搭配
        
        Args:
            combo: 候选组合
            historical_stats: 历史统计信息
            
        Returns:
            float: 统计得分（0-1）
        """
        score = 0.0
        
        # 1. 和值黄金区间得分
        combo_sum = sum(combo)
        if 70 <= combo_sum <= 120:
            score += 0.3
            if 90 <= combo_sum <= 110:
                score += 0.1  # 核心区间额外加分
        
        # 2. 跨度得分
        span = max(combo) - min(combo)
        if 24 <= span <= 30:
            score += 0.2
        elif 20 <= span <= 35:
            score += 0.1
        
        # 3. 统计偏离度
        if 'sum_statistics' in historical_stats:
            sum_mean = historical_stats['sum_statistics']['mean']
            sum_std = historical_stats['sum_statistics']['std']
            z = abs((combo_sum - sum_mean) / (sum_std + 1e-10))
            if z < 1.0:
                score += 0.2
            elif z < 1.5:
                score += 0.1
        
        # 4. 冷热搭配
        if 'front_classification' in historical_stats:
            hot = historical_stats['front_classification']['hot']
            cold = historical_stats['front_classification']['cold']
            hot_count = sum(1 for n in combo if n in hot)
            cold_count = sum(1 for n in combo if n in cold)
            # 2-3个热号 + 1-2个冷号为理想搭配
            if 2 <= hot_count <= 3 and 1 <= cold_count <= 2:
                score += 0.2
        
        return min(score, 1.0)
    
    def get_recommended_numbers(self, 
                               historical_stats: Dict[str, Any],
                               n_front: int = 10,
                               n_back: int = 4) -> Dict[str, List[int]]:
        """
        获取推荐的号码列表
        
        基于统计分析，推荐:
        - 前区号码: 兼顾冷热，覆盖黄金区间
        - 后区号码: 均衡选择
        
        Args:
            historical_stats: 历史统计信息
            n_front: 推荐前区号码个数
            n_back: 推荐后区号码个数
            
        Returns:
            Dict: 包含front和back的推荐号码
        """
        recommendations = {
            'front': [],
            'back': [],
            'strategy': {}
        }
        
        if not historical_stats:
            # 无历史数据时，使用均匀分布
            recommendations['front'] = list(range(1, 36))[:n_front]
            recommendations['back'] = list(range(1, 13))[:n_back]
            recommendations['strategy'] = {'type': 'default', 'reason': '无历史数据，使用均匀分布'}
            return recommendations
        
        front_freq = historical_stats.get('front_frequency', np.zeros(35))
        back_freq = historical_stats.get('back_frequency', np.zeros(12))
        front_class = historical_stats.get('front_classification', {})
        back_class = historical_stats.get('back_classification', {})
        
        # 策略：2热 + 2温 + 1冷（前区）
        hot = front_class.get('hot', [])[:5]  # 取前5个热号
        warm = front_class.get('warm', [])[:10]  # 取前10个温号
        cold = front_class.get('cold', [])[:5]  # 取前5个冷号
        
        # 按频率加权选择
        scores = front_freq.copy()
        # 提高冷号被选中的概率（避免过度集中热号）
        for idx in cold:
            if idx + 1 not in hot[:3]:  # 不是最热的3个
                scores[idx] += 0.5
        
        # 选择得分最高的n_front个
        selected_idx = np.argsort(-scores)[:n_front]
        recommendations['front'] = (selected_idx + 1).tolist()
        
        # 后区：均衡选择
        back_scores = back_freq.copy()
        selected_back_idx = np.argsort(-back_scores)[:n_back]
        recommendations['back'] = (selected_back_idx + 1).tolist()
        
        recommendations['strategy'] = {
            'type': 'statistical',
            'hot_count': len([n for n in recommendations['front'] if n in hot]),
            'cold_count': len([n for n in recommendations['front'] if n in cold]),
            'reason': '基于历史频率和冷热分析的推荐'
        }
        
        return recommendations
    
    def calculate_number_expectancy(self, 
                                   frequency: np.ndarray,
                                   n_periods: int) -> np.ndarray:
        """
        计算号码的预期出现次数
        
        基于当前频率和理论概率，预测未来n期的期望值
        
        Args:
            frequency: 历史频率数组
            n_periods: 预测期数
            
        Returns:
            np.ndarray: 各号码的期望出现次数
        """
        # 理论概率（每个号码被选中的概率）
        n = len(frequency)
        theoretical_prob = 1.0 / n
        
        # 实际频率（归一化）
        freq_sum = np.sum(frequency)
        if freq_sum == 0:
            actual_prob = np.ones(n) / n
        else:
            actual_prob = frequency / freq_sum
        
        # 期望值 = 加权平均
        combined_prob = 0.7 * actual_prob + 0.3 * theoretical_prob
        
        return combined_prob * n_periods
    
    def generate_statistics_report(self, 
                                   draws: List[Tuple[List[int], List[int]]]) -> Dict[str, Any]:
        """
        生成完整的统计分析报告
        
        Args:
            draws: 历史开奖记录
            
        Returns:
            Dict: 完整的统计分析报告
        """
        if not draws:
            return {'error': '无历史数据'}
        
        # 基础频率分析
        freq_analysis = self.analyze_frequency_distribution(draws)
        
        # 和值趋势
        sums = [sum(front) for front, _ in draws[-self.window:]]
        sum_trend = self.predict_sum_trend(np.array(sums))
        
        # 号码期望
        front_expectancy = self.calculate_number_expectancy(
            freq_analysis['front_frequency'], 5
        )
        back_expectancy = self.calculate_number_expectancy(
            freq_analysis['back_frequency'], 5
        )
        
        return {
            'periods_analyzed': len(draws),
            'window': self.window,
            'frequency_analysis': freq_analysis,
            'sum_trend': sum_trend,
            'number_expectancy': {
                'front': front_expectancy.tolist(),
                'back': back_expectancy.tolist()
            },
            'recommendations': self.get_recommended_numbers(freq_analysis)
        }
