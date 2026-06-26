#!/usr/bin/env python3
"""
DLT号码引力模型 - 基于视频12
核心理论：每个号码都有"引力"，影响周围号码的出现概率
"""

from typing import List, Dict, Any, Tuple
import numpy as np


class DLTNumberGravity:
    """
    引力模型三要素：
    1. 纵深引力：同列纵向联系（同一位置历史上的纵向号码）
    2. 横向引力：同期横向联系（同一期出现的号码相互吸引）
    3. 间隔引力：号码间隔的引力场（某些间隔模式更具吸引力）
    
    注意：所有参数都有物理上界，确保不会超调
    """
    
    # 引力参数（有界：0-1）
    GRAVITY_RADIUS = 3        # 引力作用半径（±3）
    GRAVITY_STRENGTH = 0.15   # 引力强度系数（有界：0-1）
    
    def __init__(self, historical_data=None):
        """
        初始化引力模型
        
        Args:
            historical_data: 历史数据DataFrame（包含前区1-5列）
        """
        self.historical_data = historical_data
        self.gravity_matrix = None  # 引力矩阵（35x35）
        if historical_data is not None:
            self._build_gravity_matrix()
    
    def _build_gravity_matrix(self):
        """从历史数据构建引力矩阵"""
        df = self.historical_data
        front_numbers = df[['前区1','前区2','前区3','前区4','前区5']].values
        
        # 初始化引力矩阵（35x35，索引0-34对应号码1-35）
        self.gravity_matrix = np.zeros((36, 36))
        
        # 横向引力：同组合出现的号码相互吸引
        for row in front_numbers:
            row_int = [int(n) for n in row]
            for i in range(len(row_int)):
                for j in range(len(row_int)):
                    if i != j:
                        n_i, n_j = row_int[i], row_int[j]
                        if 1 <= n_i <= 35 and 1 <= n_j <= 35:
                            self.gravity_matrix[n_i][n_j] += 1
        
        # 归一化（每行的引力之和为1，有界：0-1）
        row_sums = self.gravity_matrix.sum(axis=1, keepdims=True)
        row_sums[row_sums == 0] = 1  # 避免除零
        self.gravity_matrix /= row_sums
    
    def calculate_gravity_score(self, combo: List[int]) -> float:
        """
        计算组合的引力分数
        
        高引力 = 组合内号码相互吸引力强
        
        Args:
            combo: 候选组合
            
        Returns:
            float: 引力分数（0-1，有界）
        """
        if self.gravity_matrix is None or self.gravity_matrix.sum() == 0:
            return 0.5  # 无历史数据时返回中性（有界：0.5）
        
        total_gravity = 0.0
        count = 0
        for n in combo:
            if 1 <= n <= 35:
                for m in combo:
                    if 1 <= m <= 35 and n != m:
                        total_gravity += self.gravity_matrix[n][m]
                        count += 1
        
        if count == 0:
            return 0.5  # 有界：中性值
        
        # 放大并有界（0-1）
        raw_score = total_gravity / count * 5
        return min(max(raw_score, 0.0), 1.0)
    
    def predict_gravity_zone(self, recent_combo: List[int]) -> List[int]:
        """
        根据上期号码预测引力最强区域
        
        Args:
            recent_combo: 最近一期的开奖号码
            
        Returns:
            List[int]: 引力最强的10个号码（降序排列）
        """
        if self.gravity_matrix is None or len(recent_combo) == 0:
            return list(range(1, 36))  # 返回全部号码
        
        # 计算每个号码的引力强度
        gravity_strength = np.zeros(36)
        for n in range(1, 36):
            for recent_n in recent_combo:
                if 1 <= recent_n <= 35:
                    gravity_strength[n] += self.gravity_matrix[recent_n][n]
        
        # 返回引力最强的10个号码
        top_indices = np.argsort(gravity_strength)[-10:][::-1]
        return [i for i in top_indices if 1 <= i <= 35]
    
    def calculate_miss_gravity(self, miss_count: int) -> float:
        """
        计算遗漏引力（遗漏越长，引力越强）
        
        基于"均值回归"理论：遗漏越长，回归概率越高
        
        Args:
            miss_count: 遗漏期数（有界：非负整数）
            
        Returns:
            float: 遗漏引力分数（0-1，有界）
        """
        # 使用指数衰减函数，有物理上界1.0
        # 引力 = 1 - exp(-遗漏期数 / 15)
        miss_count = max(0, miss_count)  # 有界：非负
        gravity = 1.0 - np.exp(-miss_count / 15.0)
        return min(gravity, 1.0)  # 有界：不超过1.0
    
    def calculate_interval_gravity(self, combo: List[int]) -> float:
        """
        计算间隔引力（号码之间的间隔模式吸引力）
        
        Args:
            combo: 候选组合
            
        Returns:
            float: 间隔引力分数（0-1，有界）
        """
        if len(combo) < 2:
            return 0.5  # 有界：中性值
        
        sorted_combo = sorted(combo)
        
        # 高频间隔模式（基于视频12）
        high_freq_intervals = {1, 2, 3, 4, 5, 6}
        
        # 计算间隔引力
        interval_gravity = 0.0
        for i in range(len(sorted_combo) - 1):
            interval = sorted_combo[i + 1] - sorted_combo[i]
            if interval in high_freq_intervals:
                interval_gravity += 0.15  # 每个高频间隔加0.15
        
        return min(interval_gravity, 1.0)  # 有界：不超过1.0
    
    def get_gravity_report(self, combo: List[int]) -> Dict[str, Any]:
        """
        获取引力分析报告
        
        Args:
            combo: 候选组合
            
        Returns:
            Dict: 详细分析结果
        """
        sorted_combo = sorted(combo)
        miss_counts = []
        for n in combo:
            if 1 <= n <= 35 and self.gravity_matrix is not None:
                # 计算该号码的平均遗漏（近似）
                miss_counts.append(self.calculate_miss_gravity(n))
        
        avg_miss_gravity = np.mean(miss_counts) if miss_counts else 0.5
        
        return {
            'combo': combo,
            'gravity_score': self.calculate_gravity_score(combo),
            'interval_gravity': self.calculate_interval_gravity(combo),
            'avg_miss_gravity': avg_miss_gravity,
            'gravity_zone': self.predict_gravity_zone(combo)[:5],
        }
