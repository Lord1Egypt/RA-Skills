#!/usr/bin/env python3
"""
DLT数学滤网系统
基于视频5+6的数学滤网 - 剔除90%小概率组合

黄金参数库（从视频提取）:
- 奇偶平衡: 3:2 或 2:3 → 覆盖68%中奖号码
- 黄金和值: 70-120 → 覆盖70%中奖号码
- 核心和值: 90-110 → 覆盖50%
- 高频跨度: 20-32 → 覆盖72.2%
- 三区比例: 023/014等 → 覆盖99.4%
"""

from typing import List, Dict, Any
import numpy as np


class DLTMathFilter:
    """
    数学滤网系统
    
    基于历史数据分析提取的黄金参数，对候选组合进行多维度过滤，
    剔除不符合统计规律的小概率组合，保留高概率组合。
    
    滤网维度:
    1. 奇偶平衡滤网 - 3:2或2:3
    2. 和值黄金区间滤网 - 70-120
    3. 跨度滤网 - 24-30高频区间
    4. 三区分布滤网 - 221或122
    5. 高低大小分布滤网 - 3:2或2:3
    """
    
    # 黄金参数库（从视频提取）
    PARITY_GOLDEN_RATIO = [3, 2]  # 3:2 或 2:3 → 覆盖68%中奖号码
    SUM_GOLDEN_RANGE = (70, 120)  # 黄金和值区间 → 覆盖70%中奖号码
    SUM_CENTER_RANGE = (90, 110)  # 核心和值区间 → 覆盖50%
    SPAN_ACCEPTABLE_RANGE = (20, 32)  # 放宽跨度区间（原24-30太严格，目标≥60%）
    HIGH_LOW_SPLIT = 18  # 前区高低分割点
    ZONE_ACCEPTABLE = [  # 放宽三区分布（覆盖99.4%，远超67%目标）
        (1, 2, 2),  # 122 - 41.3%
        (2, 1, 2),  # 212
        (2, 2, 1),  # 221
        (1, 1, 3),  # 113 - 23.0%
        (1, 3, 1),  # 131
        (3, 1, 1),  # 311
        (0, 2, 3),  # 023 - 新增：24.5%（无小号区，中号2个，大号3个）
        (0, 1, 4),  # 014 - 新增：10.6%（无小号区，中号1个，大号4个）
    ]
    
    def __init__(self):
        """初始化数学滤网系统"""
        self.filter_stats = {
            'total_checked': 0,
            'parity_passed': 0,
            'sum_passed': 0,
            'span_passed': 0,
            'zone_passed': 0,
            'high_low_passed': 0,
            'all_passed': 0
        }
        # 放宽后的参数（有界）
        self.SPAN_ACCEPTABLE_RANGE = (20, 32)  # 跨度20-32
        self.ZONE_ACCEPTABLE = [  # 三区分布放宽（覆盖99.4%）
            (1, 2, 2), (2, 1, 2), (2, 2, 1),
            (1, 1, 3), (1, 3, 1), (3, 1, 1),
            (0, 2, 3),  # 023 - 24.5%
            (0, 1, 4),  # 014 - 10.6%
        ]
    
    def apply_all_filters(self, combo: List[int]) -> bool:
        """
        应用全部数学滤网
        
        Args:
            combo: 候选组合（5个前区号码）
            
        Returns:
            bool: 是否通过所有滤网
        """
        self.filter_stats['total_checked'] += 1
        
        parity_ok = self._check_parity(combo)
        sum_ok = self._check_sum_range(combo)
        span_ok = self._check_span_range(combo)
        zone_ok = self._check_zone_distribution(combo)
        high_low_ok = self._check_high_low_distribution(combo)
        
        if parity_ok:
            self.filter_stats['parity_passed'] += 1
        if sum_ok:
            self.filter_stats['sum_passed'] += 1
        if span_ok:
            self.filter_stats['span_passed'] += 1
        if zone_ok:
            self.filter_stats['zone_passed'] += 1
        if high_low_ok:
            self.filter_stats['high_low_passed'] += 1
        
        result = parity_ok and sum_ok and span_ok and zone_ok and high_low_ok
        if result:
            self.filter_stats['all_passed'] += 1
        
        return result
    
    def _check_parity(self, combo: List[int]) -> bool:
        """
        奇偶平衡滤网 - 3:2或2:3
        
        统计规律显示，68%的中奖号码奇偶比例为3:2或2:3
        极端比例（5:0或0:5）出现概率极低
        """
        odd = sum(1 for n in combo if n % 2 == 1)
        return odd in [2, 3]
    
    def _check_sum_range(self, combo: List[int]) -> bool:
        """
        和值黄金区间滤网 - 70-120
        
        统计规律显示，70%的中奖号码和值落在70-120区间
        核心区间90-110覆盖50%
        """
        total = sum(combo)
        return 70 <= total <= 120
    
    def _check_span_range(self, combo: List[int]) -> bool:
        """
        跨度滤网 - 20-32区间（放宽版）
        
        最大号与最小号的差值（跨度）是重要的参考指标
        原24-30区间太严格（覆盖率仅43.5%），放宽至20-32（目标≥60%）
        """
        span = max(combo) - min(combo)
        return 20 <= span <= 32
    
    def _check_zone_distribution(self, combo: List[int]) -> bool:
        """
        三区分布滤网 - 放宽版（接受多种均衡分布）
        
        将35个前区号码分成3区:
        - 1区: 1-12
        - 2区: 13-24  
        - 3区: 25-35
        
        原221/122比例太严格（覆盖率仅41.3%），放宽至接受多种均衡分布：
        122, 212, 221, 113, 131, 311（目标覆盖率≥67%）
        """
        zone_counts = [0, 0, 0]
        for n in combo:
            if n <= 12:
                zone_counts[0] += 1
            elif n <= 24:
                zone_counts[1] += 1
            else:
                zone_counts[2] += 1
        
        sorted_zones = tuple(sorted(zone_counts))
        return sorted_zones in self.ZONE_ACCEPTABLE
    
    def _check_high_low_distribution(self, combo: List[int]) -> bool:
        """
        高低大小分布滤网 - 3:2或2:3
        
        以18为分割点:
        - 高价区: 19-35
        - 低价区: 1-18
        
        3:2或2:3比例为高概率分布
        """
        high = sum(1 for n in combo if n > self.HIGH_LOW_SPLIT)
        low = sum(1 for n in combo if n <= self.HIGH_LOW_SPLIT)
        return high in [2, 3] and low in [2, 3]
    
    def get_filter_pass_rate(self, combos: List[List[int]]) -> float:
        """
        计算组合通过率
        
        Args:
            combos: 组合列表
            
        Returns:
            float: 通过率（0-1）
        """
        if not combos:
            return 0.0
        passed = sum(1 for c in combos if self.apply_all_filters(c))
        return passed / len(combos)
    
    def filter_combos(self, combos: List[List[int]]) -> List[List[int]]:
        """
        过滤组合列表
        
        Args:
            combos: 候选组合列表
            
        Returns:
            List[List[int]]: 通过滤网的组合列表
        """
        return [c for c in combos if self.apply_all_filters(c)]
    
    def get_filter_statistics(self) -> Dict[str, Any]:
        """
        获取滤网统计信息
        
        Returns:
            Dict: 各滤网的通过率统计
        """
        total = max(self.filter_stats['total_checked'], 1)
        return {
            'total_checked': self.filter_stats['total_checked'],
            'parity_pass_rate': self.filter_stats['parity_passed'] / total,
            'sum_pass_rate': self.filter_stats['sum_passed'] / total,
            'span_pass_rate': self.filter_stats['span_passed'] / total,
            'zone_pass_rate': self.filter_stats['zone_passed'] / total,
            'high_low_pass_rate': self.filter_stats['high_low_passed'] / total,
            'all_pass_rate': self.filter_stats['all_passed'] / total,
        }
    
    def reset_statistics(self):
        """重置统计信息"""
        self.filter_stats = {
            'total_checked': 0,
            'parity_passed': 0,
            'sum_passed': 0,
            'span_passed': 0,
            'zone_passed': 0,
            'high_low_passed': 0,
            'all_passed': 0
        }
    
    def analyze_combo(self, combo: List[int]) -> Dict[str, Any]:
        """
        分析单个组合的滤网表现
        
        Args:
            combo: 候选组合
            
        Returns:
            Dict: 详细的分析结果
        """
        return {
            'combo': combo,
            'parity_ok': self._check_parity(combo),
            'odd_count': sum(1 for n in combo if n % 2 == 1),
            'sum_ok': self._check_sum_range(combo),
            'sum': sum(combo),
            'span_ok': self._check_span_range(combo),
            'span': max(combo) - min(combo),
            'zone_ok': self._check_zone_distribution(combo),
            'zone_distribution': self._get_zone_distribution(combo),
            'high_low_ok': self._check_high_low_distribution(combo),
            'high_count': sum(1 for n in combo if n > self.HIGH_LOW_SPLIT),
            'low_count': sum(1 for n in combo if n <= self.HIGH_LOW_SPLIT),
            'overall_pass': self.apply_all_filters(combo)
        }
    
    def _get_zone_distribution(self, combo: List[int]) -> List[int]:
        """获取三区分布"""
        zone_counts = [0, 0, 0]
        for n in combo:
            if n <= 12:
                zone_counts[0] += 1
            elif n <= 24:
                zone_counts[1] += 1
            else:
                zone_counts[2] += 1
        return zone_counts
