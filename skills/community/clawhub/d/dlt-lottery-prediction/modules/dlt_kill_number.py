#!/usr/bin/env python3
"""
DLT杀号逻辑 - 与数学滤网形成正反互补
基于视频15: 数据杀号 + 结构杀号 + 心理杀号
"""

from typing import List, Dict, Any, Tuple
import numpy as np


class DLTKillNumberAnalyzer:
    """
    杀号三维度：
    1. 数据杀号：热号极值杀、冷号长遗漏杀
    2. 结构杀号：极端形态杀（5:0奇偶、全大连号等）
    3. 心理杀号：大众号杀（生日号、纪念日等）
    
    注意：所有参数都有物理上界，确保不会超调
    """
    
    # 杀号参数（有界，确保0-1范围）
    KILL_HOT_THRESHOLD = 0.85  # 出现率>85%视为过热杀（有界：0-1）
    KILL_COLD_MAX_MISS = 25    # 遗漏>25期杀（有界：正整数）
    KILL_FORMATION_PATTERNS = [    # 极端形态模式
        [0, 0, 0, 0, 5],  # 5:0奇偶
        [5, 0, 0, 0, 0],  # 0:5奇偶
        [0, 0, 0, 0, 5],  # 5:0大小（全大）
        [5, 0, 0, 0, 0],  # 0:5大小（全小）
    ]
    
    def __init__(self, historical_data=None):
        """
        初始化杀号分析器
        
        Args:
            historical_data: 历史数据DataFrame（包含前区1-5列）
        """
        self.historical_data = historical_data
        self.frequency = None  # 号码出现频率
        self.miss_count = None  # 号码当前遗漏
        self._init_statistics()
    
    def _init_statistics(self):
        """从历史数据初始化统计信息"""
        if self.historical_data is not None:
            df = self.historical_data
            front_numbers = df[['前区1','前区2','前区3','前区4','前区5']].values
            
            # 计算每个号码的出现频率（归一化到0-1）
            self.frequency = np.zeros(36)  # 索引0-34对应号码1-35
            for row in front_numbers:
                for n in row:
                    n = int(n)
                    if 1 <= n <= 35:
                        self.frequency[n] += 1
            total_count = len(front_numbers)
            if total_count > 0:
                self.frequency /= total_count  # 有界：0-1
            
            # 计算每个号码的当前遗漏
            self.miss_count = np.zeros(36)
            for n in range(1, 36):
                for i in range(len(front_numbers) - 1, -1, -1):
                    if n in front_numbers[i]:
                        self.miss_count[n] = len(front_numbers) - 1 - i
                        break
                # 如果历史中从未出现，遗漏保持为0
        else:
            # 无历史数据时使用均匀分布
            self.frequency = np.ones(36) / 35  # 有界：0-1
            self.miss_count = np.zeros(36)
    
    def kill_by_hot_number(self, combo: List[int], threshold: float = 0.85) -> bool:
        """
        热号杀：组合中过热号码超过阈值
        
        Args:
            combo: 候选组合
            threshold: 热号阈值（有界：0-1）
            
        Returns:
            bool: 是否应该杀
        """
        if self.frequency is None:
            return False
        hot_count = sum(1 for n in combo if 1 <= n <= 35 and self.frequency[n] > threshold)
        return hot_count >= 2  # 超过2个热号则杀
    
    def kill_by_cold_long_miss(self, combo: List[int], max_miss: int = 25) -> bool:
        """
        冷号杀：长遗漏号码超过阈值（冷过头反而是杀号）
        
        Args:
            combo: 候选组合
            max_miss: 最大遗漏阈值（有界：正整数）
            
        Returns:
            bool: 是否应该杀
        """
        if self.miss_count is None:
            return False
        # 遗漏是有界的（最大为历史期数），但我们用max_miss来限制
        cold_miss_count = sum(1 for n in combo if 1 <= n <= 35 and self.miss_count[n] > max_miss)
        return cold_miss_count >= 2
    
    def kill_by_extreme_formation(self, combo: List[int]) -> bool:
        """
        结构杀：极端形态检测
        
        检测以下极端形态：
        - 5:0 或 0:5 奇偶比例
        - 全大（5:0）或全小（0:5）高低分布
        - 全在同一区（极端集中）
        
        Args:
            combo: 候选组合
            
        Returns:
            bool: 是否为极端形态
        """
        odd = sum(1 for n in combo if n % 2 == 1)
        high = sum(1 for n in combo if n > 18)
        
        # 5:0 或 0:5 奇偶（有界：0-5）
        if odd in [0, 5]:
            return True
        # 全大或全小（有界：0-5）
        if high in [0, 5]:
            return True
        # 全在同一区（0:0:5 或 5:0:0）
        zones = self._count_zones(combo)
        if max(zones) == 5:
            return True
        return False
    
    def kill_by_psychology(self, combo: List[int]) -> bool:
        """
        心理杀：大众偏好号检测
        
        大众倾向于选择：
        - 生日号段：1-12（小号区过多人选）
        - 整十号：10, 20, 30（纪念日效应）
        
        Args:
            combo: 候选组合
            
        Returns:
            bool: 是否包含大众偏好号
        """
        # 生日号段：1-12（小号区过多人选）（有界：0-5）
        birthday_like = sum(1 for n in combo if n <= 12)
        if birthday_like >= 4:
            return True
        # 整十号集中（10, 20, 30）（有界：0-5）
        round_nums = sum(1 for n in combo if n % 10 == 0 and n <= 30)
        if round_nums >= 3:
            return True
        return False
    
    def get_kill_score(self, combo: List[int]) -> float:
        """
        综合杀号分数（越高越该杀）
        
        分数组成（有界：0-1）：
        - 热号杀：0.3
        - 冷号长遗漏杀：0.2
        - 极端结构杀：0.3
        - 心理杀：0.2
        
        Args:
            combo: 候选组合
            
        Returns:
            float: 杀号分数（0-1，有界）
        """
        score = 0.0
        if self.kill_by_hot_number(combo): score += 0.3
        if self.kill_by_cold_long_miss(combo): score += 0.2
        if self.kill_by_extreme_formation(combo): score += 0.3
        if self.kill_by_psychology(combo): score += 0.2
        return min(score, 1.0)  # 有界：不超过1.0
    
    def should_kill(self, combo: List[int], threshold: float = 0.4) -> bool:
        """
        判断是否应该杀
        
        Args:
            combo: 候选组合
            threshold: 杀号阈值（有界：0-1）
            
        Returns:
            bool: 是否应该杀
        """
        return self.get_kill_score(combo) >= threshold
    
    def _count_zones(self, combo: List[int]) -> List[int]:
        """
        统计三区分布
        
        Args:
            combo: 候选组合
            
        Returns:
            List[int]: [1区数量, 2区数量, 3区数量]
        """
        zones = [0, 0, 0]
        for n in combo:
            if n <= 12:
                zones[0] += 1
            elif n <= 24:
                zones[1] += 1
            else:
                zones[2] += 1
        return zones
    
    def get_analysis_report(self, combo: List[int]) -> Dict[str, Any]:
        """
        获取杀号分析报告
        
        Args:
            combo: 候选组合
            
        Returns:
            Dict: 详细分析结果
        """
        return {
            'combo': combo,
            'kill_score': self.get_kill_score(combo),
            'should_kill': self.should_kill(combo),
            'hot_kill': self.kill_by_hot_number(combo),
            'cold_kill': self.kill_by_cold_long_miss(combo),
            'extreme_kill': self.kill_by_extreme_formation(combo),
            'psychology_kill': self.kill_by_psychology(combo),
            'zone_distribution': self._count_zones(combo),
            'odd_count': sum(1 for n in combo if n % 2 == 1),
            'high_count': sum(1 for n in combo if n > 18),
        }


# Backward compatibility alias
DLTKillNumber = DLTKillNumberAnalyzer
