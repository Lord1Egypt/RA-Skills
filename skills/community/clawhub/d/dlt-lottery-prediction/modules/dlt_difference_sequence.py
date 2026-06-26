#!/usr/bin/env python3
"""
DLT差值序列分析 - 基于视频8
核心理论：分析号码间的差值序列规律
"""

from typing import List, Dict, Any
import numpy as np


class DLTDifferenceSequence:
    """
    差值序列分析：
    1. 一阶差分：相邻号码的差值
    2. 二阶差分：差值的差值（加速度）
    3. 差值熵：差值分布的混乱程度
    
    注意：所有参数都有物理上界，确保不会超调
    """
    
    # 差值黄金分布（从历史数据统计）
    DIFF_HIGH_FREQ = [1, 2, 3, 4, 5, 6]  # 高频差值（有界）
    DIFF_VERY_RARE = [15, 16, 17, 18]   # 极稀有差值（有界）
    
    def __init__(self, historical_data=None):
        """
        初始化差值序列分析器
        
        Args:
            historical_data: 历史数据DataFrame（包含前区1-5列）
        """
        self.historical_data = historical_data
        self.diff_distribution = None  # 差值分布概率
        if historical_data is not None:
            self._build_diff_distribution()
    
    def _build_diff_distribution(self):
        """从历史数据构建差值分布"""
        df = self.historical_data
        front_numbers = df[['前区1','前区2','前区3','前区4','前区5']].values
        
        diff_counts = np.zeros(35)  # 差值1-34
        
        for row in front_numbers:
            sorted_row = sorted([int(n) for n in row])
            for i in range(len(sorted_row) - 1):
                diff = sorted_row[i + 1] - sorted_row[i]
                if 1 <= diff <= 34:
                    diff_counts[diff - 1] += 1
        
        # 归一化为概率（有界：0-1）
        total = diff_counts.sum()
        if total > 0:
            self.diff_distribution = diff_counts / total
        else:
            self.diff_distribution = None
    
    def calculate_diff_sequence(self, combo: List[int]) -> np.ndarray:
        """
        计算组合的差值序列（一阶差分）
        
        Args:
            combo: 候选组合
            
        Returns:
            np.ndarray: 差值数组（4个差值）
        """
        sorted_combo = sorted(combo)
        diffs = np.array([
            sorted_combo[i + 1] - sorted_combo[i] 
            for i in range(len(sorted_combo) - 1)
        ])
        return diffs
    
    def calculate_diff_entropy(self, combo: List[int]) -> float:
        """
        计算差值熵（越低说明规律性越强）
        
        熵的计算：H = -Σp*log(p)
        
        Args:
            combo: 候选组合
            
        Returns:
            float: 差值熵（0-1，有界）
        """
        diffs = self.calculate_diff_sequence(combo)
        
        if self.diff_distribution is None:
            return 0.5  # 无历史数据时返回中性（有界：0.5）
        
        # 计算差值分布的熵
        p_diff = np.zeros(35)
        for d in diffs:
            if 1 <= d <= 35:
                p_diff[d - 1] += 1
        p_diff /= len(diffs)  # 有界：0-1
        
        # 计算香农熵
        entropy = -np.sum(p_diff * np.log(p_diff + 1e-10))
        
        # 归一化到0-1（有界）
        max_entropy = np.log(35)  # 最大熵
        return min(entropy / max_entropy, 1.0)
    
    def calculate_diff_regularity(self, combo: List[int]) -> float:
        """
        计算差值规律度（越高说明越有规律）
        
        与熵相反
        
        Args:
            combo: 候选组合
            
        Returns:
            float: 规律度分数（0-1，有界）
        """
        return 1.0 - self.calculate_diff_entropy(combo)
    
    def check_diff_balance(self, combo: List[int]) -> bool:
        """
        检查差值是否平衡
        
        规则：
        - 不能有差值=1（连号本身降低概率）
        - 不能有差值>15（太大则分布不均匀）
        
        Args:
            combo: 候选组合
            
        Returns:
            bool: 是否平衡
        """
        diffs = self.calculate_diff_sequence(combo)
        
        # 不能有差值=1（连号）
        if 1 in diffs:
            return False
        # 不能有差值>15（太大）
        if max(diffs) > 15:
            return False
        return True
    
    def check_diff_smoothness(self, combo: List[int]) -> bool:
        """
        检查差值平滑度
        
        二阶差分（加速度）不应太大
        
        Args:
            combo: 候选组合
            
        Returns:
            bool: 是否平滑
        """
        diffs = self.calculate_diff_sequence(combo)
        if len(diffs) < 3:
            return True
        
        # 二阶差分
        second_diff = np.diff(diffs)
        
        # 二阶差分绝对值之和应该小于某个阈值
        return np.sum(np.abs(second_diff)) < 10
    
    def get_diff_score(self, combo: List[int]) -> float:
        """
        综合差值评分
        
        分数组成（有界：0-1）：
        - 无连号加分：0.3
        - 差值分布均匀加分：0.3
        - 差值熵适中加分：0.4
        
        Args:
            combo: 候选组合
            
        Returns:
            float: 综合分数（0-1，有界）
        """
        diffs = self.calculate_diff_sequence(combo)
        score = 0.0
        
        # 无连号加分（0.3）
        if 1 not in diffs:
            score += 0.3
        
        # 差值分布均匀加分（0.3）
        diff_range = max(diffs) - min(diffs)
        if diff_range < 10:
            score += 0.3
        
        # 差值熵适中加分（0.4）
        entropy = self.calculate_diff_entropy(combo)
        if 0.3 < entropy < 0.7:
            score += 0.4
        
        return min(score, 1.0)  # 有界：不超过1.0
    
    def get_diff_report(self, combo: List[int]) -> Dict[str, Any]:
        """
        获取差值分析报告
        
        Args:
            combo: 候选组合
            
        Returns:
            Dict: 详细分析结果
        """
        diffs = self.calculate_diff_sequence(combo)
        entropy = self.calculate_diff_entropy(combo)
        
        return {
            'combo': combo,
            'diffs': diffs.tolist(),
            'diff_score': self.get_diff_score(combo),
            'diff_entropy': entropy,
            'diff_regularity': 1.0 - entropy,
            'diff_balance': self.check_diff_balance(combo),
            'diff_smoothness': self.check_diff_smoothness(combo),
            'diff_range': int(max(diffs) - min(diffs)) if len(diffs) > 0 else 0,
        }
