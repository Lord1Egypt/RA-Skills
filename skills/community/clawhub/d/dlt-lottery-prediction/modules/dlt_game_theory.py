#!/usr/bin/env python3
"""
DLT博弈论分析器
基于视频2的博弈论分析器
追冷策略与分奖防御

核心概念:
- 大众偏好回避度: 避开大多数人选的号码，提高独享奖金概率
- 视觉规律度: 无规律组合更可能成为冷门
- 冷组合识别: 综合多维度特征识别可能被忽视的组合

六大冷组合特征:
1. 高号比例: 28-35区间号码占多数
2. 奇偶极端: 5:0或0:5的比例
3. 大跨度: 30左右
4. 无规律感: 无连号、无等差
5. 非整十数字集中: 避开10, 20, 30等热门整十
6. 极端和值: 超出黄金和值区间
"""

from typing import List, Dict, Any, Tuple
import numpy as np


class DLTGameTheoryAnalyzer:
    """
    博弈论分析器
    
    从博弈论角度分析彩票号码组合，帮助用户:
    1. 识别大众偏好模式，回避热门号码
    2. 识别冷门组合，提高独享奖金概率
    3. 平衡风险与收益
    
    核心策略:
    - 追冷策略: 选择被低估的冷门组合
    - 防御策略: 确保至少覆盖基本奖项
    """
    
    # 六大冷组合特征（从视频提取）
    COLD_COMBO_FEATURES = {
        'high_number_ratio': 0.6,  # 高号比例（28-35区间）
        'extreme_parity': 0.0,     # 奇偶极端（5:0或0:5）
        'large_span': 30,           # 大跨度
        'no_regularity': True,     # 无规律感
        'no_round_numbers': True,  # 非整十数字集中
        'extreme_sum': True        # 极端和值
    }
    
    # 热门号码段（基于大众偏好统计）
    HOT_NUMBER_RANGES = {
        'low': list(range(1, 11)),      # 1-10 低号段（最热）
        'round_10': [10, 20, 30],       # 整十数（较热）
        'lucky': [6, 8, 18, 28],        # 所谓"幸运数"
        'birthday': list(range(1, 13))  # 月份相关
    }
    
    def __init__(self):
        """初始化博弈论分析器"""
        self.analysis_cache = {}
    
    def calculate_popularity_avoidance_score(self, combo: List[int]) -> float:
        """
        计算大众偏好回避度分数
        
        分数越高表示该组合越能避开大众选择，独自获奖概率越高
        
        计分规则:
        - 避开1-10低号段: <=1个 +0.3分
        - 避开整十数字: <=1个 +0.2分
        - 高号比例高: >=3个28-35号码 +0.3分
        - 奇偶极端: 5:0或0:5 +0.2分
        
        Args:
            combo: 候选组合（5个号码）
            
        Returns:
            float: 回避度分数（0-1）
        """
        score = 0.0
        
        # 避开热门号码（1-10低号段）
        low_count = sum(1 for n in combo if n <= 10)
        if low_count <= 1:
            score += 0.3
        
        # 避开整十数字（10, 20, 30）
        round_count = sum(1 for n in combo if n % 10 == 0)
        if round_count <= 1:
            score += 0.2
        
        # 高号比例（28-35区间）
        high_count = sum(1 for n in combo if n >= 28)
        if high_count >= 3:
            score += 0.3
        
        # 奇偶极端检测（5:0或0:5）
        odd = sum(1 for n in combo if n % 2 == 1)
        if odd in [0, 5]:
            score += 0.2
        
        return min(score, 1.0)
    
    def calculate_visual_regularity_score(self, combo: List[int]) -> float:
        """
        计算视觉规律度分数
        
        无规律的组合更容易成为冷门，被大众忽视
        
        计分规则:
        - 无连号: +0.4分
        - 有1个间连号: +0.2分
        - 等差数列: -0.3分（太规律）
        
        Args:
            combo: 候选组合
            
        Returns:
            float: 规律度分数（0-1，越高越无规律）
        """
        score = 0.0
        
        # 检测连号（间连号也算，间隔<=2）
        sorted_combo = sorted(combo)
        consecutive_count = 0
        for i in range(len(sorted_combo) - 1):
            if sorted_combo[i+1] - sorted_combo[i] <= 2:
                consecutive_count += 1
        
        # 无连号高分
        if consecutive_count == 0:
            score += 0.4
        elif consecutive_count == 1:
            score += 0.2
        
        # 检测等差数列（所有相邻差相等）
        if len(sorted_combo) >= 3:
            diffs = [sorted_combo[i+1] - sorted_combo[i] for i in range(len(sorted_combo)-1)]
            if len(set(diffs)) == 1:
                score -= 0.3  # 等差数列低分
        
        return max(0.0, min(score, 1.0))
    
    def is_cold_combo(self, combo: List[int]) -> bool:
        """
        判断是否为冷组合
        
        冷组合定义:
        - 大众偏好回避度 + 视觉规律度 > 0.6
        
        Args:
            combo: 候选组合
            
        Returns:
            bool: 是否为冷组合
        """
        score = self.calculate_popularity_avoidance_score(combo)
        regularity = self.calculate_visual_regularity_score(combo)
        return score + regularity > 0.6
    
    def analyze_combo(self, combo: List[int]) -> Dict[str, Any]:
        """
        全面分析组合的博弈论特征
        
        Args:
            combo: 候选组合
            
        Returns:
            Dict: 详细的分析结果
        """
        sorted_combo = sorted(combo)
        
        # 基本统计
        odd_count = sum(1 for n in combo if n % 2 == 1)
        even_count = 5 - odd_count
        low_count = sum(1 for n in combo if n <= 10)
        high_count = sum(1 for n in combo if n >= 28)
        round_count = sum(1 for n in combo if n % 10 == 0)
        span = max(combo) - min(combo)
        total = sum(combo)
        
        # 计算各项分数
        avoidance_score = self.calculate_popularity_avoidance_score(combo)
        regularity_score = self.calculate_visual_regularity_score(combo)
        
        # 识别特征
        features = {
            'is_cold_combo': self.is_cold_combo(combo),
            'avoidance_score': avoidance_score,
            'regularity_score': regularity_score,
            'combined_score': avoidance_score + regularity_score,
            'characteristics': self._identify_characteristics(combo)
        }
        
        # 风险评估
        features['risk_assessment'] = self._assess_risk(combo)
        
        # 策略建议
        features['strategy_suggestion'] = self._suggest_strategy(features)
        
        return {
            'combo': combo,
            'sorted_combo': sorted_combo,
            'statistics': {
                'odd_count': odd_count,
                'even_count': even_count,
                'low_count': low_count,
                'high_count': high_count,
                'round_count': round_count,
                'span': span,
                'sum': total
            },
            'scores': features
        }
    
    def _identify_characteristics(self, combo: List[int]) -> List[str]:
        """识别组合特征"""
        chars = []
        
        odd = sum(1 for n in combo if n % 2 == 1)
        if odd in [0, 5]:
            chars.append('奇偶极端(5:0或0:5)')
        elif odd in [1, 4]:
            chars.append('奇偶偏态')
        
        high = sum(1 for n in combo if n >= 28)
        if high >= 3:
            chars.append('高号集中')
        elif high <= 1:
            chars.append('低号集中')
        
        low = sum(1 for n in combo if n <= 10)
        if low >= 3:
            chars.append('热门低号区')
        
        round_count = sum(1 for n in combo if n % 10 == 0)
        if round_count >= 2:
            chars.append('多整十数')
        elif round_count == 0:
            chars.append('无整十数')
        
        span = max(combo) - min(combo)
        if span > 30:
            chars.append('大跨度')
        elif span < 20:
            chars.append('小跨度')
        
        # 检测规律性
        sorted_c = sorted(combo)
        consecutive = 0
        for i in range(len(sorted_c) - 1):
            if sorted_c[i+1] - sorted_c[i] <= 2:
                consecutive += 1
        if consecutive >= 2:
            chars.append('多连号')
        elif consecutive == 1:
            chars.append('单连号')
        
        return chars
    
    def _assess_risk(self, combo: List[int]) -> Dict[str, Any]:
        """评估组合风险"""
        avoidance = self.calculate_popularity_avoidance_score(combo)
        regularity = self.calculate_visual_regularity_score(combo)
        
        # 风险等级
        combined = avoidance + regularity
        if combined > 0.8:
            risk_level = '极高'
            risk_desc = '极度冷门，可能无人选择'
        elif combined > 0.6:
            risk_level = '高'
            risk_desc = '较冷门，独自获奖概率高'
        elif combined > 0.4:
            risk_level = '中'
            risk_desc = '常规组合'
        else:
            risk_level = '低'
            risk_desc = '热门组合，可能多人选择'
        
        return {
            'level': risk_level,
            'description': risk_desc,
            'avoidance_component': avoidance,
            'regularity_component': regularity
        }
    
    def _suggest_strategy(self, features: Dict[str, Any]) -> str:
        """根据特征建议策略"""
        if features['is_cold_combo']:
            return '追冷策略：此组合较冷门，适合博取高奖金'
        elif features['avoidance_score'] > 0.5:
            return '防御策略：避开热门，提高独享概率'
        else:
            return '平衡策略：混合选择，兼顾中奖与收益'
    
    def compare_combos(self, combos: List[List[int]]) -> List[Dict[str, Any]]:
        """
        对比多个组合的博弈论特征
        
        Args:
            combos: 组合列表
            
        Returns:
            List[Dict]: 各组合的分析结果，按综合分数排序
        """
        results = []
        for combo in combos:
            analysis = self.analyze_combo(combo)
            analysis['rank_score'] = analysis['scores']['combined_score']
            results.append(analysis)
        
        # 按综合分数降序排列
        results.sort(key=lambda x: x['rank_score'], reverse=True)
        
        # 添加排名
        for i, r in enumerate(results):
            r['rank'] = i + 1
        
        return results
    
    def generate_cold_strategies(self, 
                                 n_strategies: int = 3,
                                 avoid_hot: bool = True) -> List[List[int]]:
        """
        生成冷门策略号码组合
        
        Args:
            n_strategies: 需要生成的策略数量
            avoid_hot: 是否主动避开热门号码
            
        Returns:
            List[List[int]]: 冷门组合列表
        """
        import random
        strategies = []
        
        for _ in range(n_strategies * 10):  # 最多尝试10倍次数
            if len(strategies) >= n_strategies:
                break
            
            # 随机生成组合
            combo = sorted(random.sample(range(1, 36), 5))
            
            # 检查是否为冷组合
            if self.is_cold_combo(combo):
                # 检查是否已存在
                if combo not in strategies:
                    strategies.append(combo)
        
        return strategies
    
    def get_hot_avoidance_guide(self) -> Dict[str, Any]:
        """
        获取热门号码回避指南
        
        Returns:
            Dict: 详细的回避建议
        """
        return {
            'hot_zones': {
                'low_numbers': {
                    'range': '1-10',
                    'reason': '最容易选择的号码段',
                    'avoidance': '该区间选择不超过1个'
                },
                'round_numbers': {
                    'range': '10, 20, 30',
                    'reason': '象征性数字，选择率高',
                    'avoidance': '该区间选择不超过1个'
                },
                'lucky_numbers': {
                    'numbers': '6, 8, 18, 28',
                    'reason': '所谓的幸运数字',
                    'avoidance': '适当选择或回避'
                }
            },
            'cold_zones': {
                'high_range': {
                    'range': '28-35',
                    'reason': '多数人认为太极端',
                    'opportunity': '高号组合可能带来惊喜'
                },
                'non_round': {
                    'reason': '如13, 17, 23等',
                    'opportunity': '这些号码较少被选择'
                }
            },
            'pattern_avoidance': {
                'consecutive': '连号组合（1,2,3,4,5等）应避免',
                'arithmetic': '等差数列（如5,10,15,20,25）应避免',
                'birthday': '基于生日的号码（1-31）选择过多'
            }
        }
