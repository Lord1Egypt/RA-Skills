# -*- coding: utf-8 -*-
"""
DLT五池分层采样器 + 博弈论输出层
=====================================
新版架构核心组件

设计理念：
- 废除"预测中奖"思维，转为"多样化组合生成"
- 5个池代表5种不同的号码分布假设，彼此互补
- 博弈论模块分析大众偏好，避免热门号码组合

作者：J.A.R.V.I.S. (贾维斯)
日期：2026-04-06
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Optional
from collections import Counter, defaultdict
import random

class DLTFivePoolSampler:
    """
    五池分层采样器
    
    5个池：
    1. 热号池 (Hot Pool) - 频率最高的号码
    2. 冷号池 (Cold Pool) - 遗漏值最高的号码  
    3. 均衡池 (Balanced Pool) - 频率和遗漏综合评估
    4. 博弈池 (Game Theory Pool) - 避开大众热门，选择被低估的号码
    5. 遗传池 (Genetic Pool) - 基于遗传算法优化多样性
    
    每个池生成6+4复式（6个前区+4个后区）
    """
    
    def __init__(self, n_front=35, n_back=12):
        self.n_front = n_front
        self.n_back = n_back
        
    def build_frequency_stats(self, history: List) -> Dict:
        """从历史数据构建频率统计"""
        front_counter = Counter()
        back_counter = Counter()
        front_missing = defaultdict(int)
        back_missing = defaultdict(int)
        
        # 初始化所有号码的遗漏值
        for i in range(1, self.n_front + 1):
            front_missing[i] = 0
        for i in range(1, self.n_back + 1):
            back_missing[i] = 0
        
        # 遍历历史数据
        for draw in history:
            front_nums = draw[0]  # 前区号码列表
            back_nums = draw[1]    # 后区号码列表
            
            # 更新频率
            for num in front_nums:
                front_counter[num] += 1
            for num in back_nums:
                back_counter[num] += 1
            
            # 更新遗漏（每个号码在draw中出现的次数）
            for i in range(1, self.n_front + 1):
                if i not in front_nums:
                    front_missing[i] += 1
            for i in range(1, self.n_back + 1):
                if i not in back_nums:
                    back_missing[i] += 1
        
        return {
            'front_freq': front_counter,
            'back_freq': back_counter,
            'front_missing': dict(front_missing),
            'back_missing': dict(back_missing),
            'total_periods': len(history)
        }
    
    def _normalize_scores(self, scores: Dict[int, float]) -> Dict[int, float]:
        """归一化分数到0-1范围"""
        if not scores:
            return {}
        values = list(scores.values())
        min_val, max_val = min(values), max(values)
        if max_val == min_val:
            return {k: 0.5 for k in scores}
        return {k: (v - min_val) / (max_val - min_val) for k, v in scores.items()}
    
    def pool_hot(self, stats: Dict, front_k: int = 5, back_k: int = 2) -> Tuple[List[int], List[int]]:
        """池1：热号池 - 频率最高的号码"""
        front_scores = self._normalize_scores(stats['front_freq'])
        back_scores = self._normalize_scores(stats['back_freq'])
        
        # 按频率排序
        front_sorted = sorted(range(1, self.n_front + 1), 
                            key=lambda x: front_scores.get(x, 0), reverse=True)
        back_sorted = sorted(range(1, self.n_back + 1),
                           key=lambda x: back_scores.get(x, 0), reverse=True)
        
        return front_sorted[:front_k], back_sorted[:back_k]
    
    def pool_cold(self, stats: Dict, front_k: int = 5, back_k: int = 2) -> Tuple[List[int], List[int]]:
        """池2：冷号池 - 遗漏值最高的号码"""
        front_scores = self._normalize_scores(stats['front_missing'])
        back_scores = self._normalize_scores(stats['back_missing'])
        
        front_sorted = sorted(range(1, self.n_front + 1),
                            key=lambda x: front_scores.get(x, 0), reverse=True)
        back_sorted = sorted(range(1, self.n_back + 1),
                           key=lambda x: back_scores.get(x, 0), reverse=True)
        
        return front_sorted[:front_k], back_sorted[:back_k]
    
    def pool_balanced(self, stats: Dict, front_k: int = 5, back_k: int = 2) -> Tuple[List[int], List[int]]:
        """池3：均衡池 - 频率和遗漏综合评估"""
        front_balanced = {}
        back_balanced = {}
        
        for i in range(1, self.n_front + 1):
            freq_score = stats['front_freq'].get(i, 0) / max(stats['total_periods'], 1)
            miss_score = stats['front_missing'].get(i, 0) / max(stats['total_periods'], 1)
            # 综合评分：频率高+遗漏高 = 反弹潜力大
            front_balanced[i] = freq_score * 0.5 + miss_score * 0.5
        
        for i in range(1, self.n_back + 1):
            freq_score = stats['back_freq'].get(i, 0) / max(stats['total_periods'], 1)
            miss_score = stats['back_missing'].get(i, 0) / max(stats['total_periods'], 1)
            back_balanced[i] = freq_score * 0.5 + miss_score * 0.5
        
        front_scores = self._normalize_scores(front_balanced)
        back_scores = self._normalize_scores(back_balanced)
        
        front_sorted = sorted(range(1, self.n_front + 1),
                            key=lambda x: front_scores.get(x, 0), reverse=True)
        back_sorted = sorted(range(1, self.n_back + 1),
                           key=lambda x: back_scores.get(x, 0), reverse=True)
        
        return front_sorted[:front_k], back_sorted[:back_k]
    
    def pool_game_theory(self, stats: Dict, front_k: int = 5, back_k: int = 2) -> Tuple[List[int], List[int]]:
        """池4：博弈池 - 避开大众热门，选择被低估的号码
        
        博弈论原理：
        - 大众倾向于选择生日、连号等"有意义"的号码
        - 这些号码中奖后奖金会被更多人分摊
        - 选择被大众忽视的号码，中奖后奖金独享的可能性更高
        """
        # 计算每个号码的"热门度"（频率越高越热门）
        front_popularity = self._normalize_scores(stats['front_freq'])
        back_popularity = self._normalize_scores(stats['back_freq'])
        
        # 被低估分数 = 1 - 热门度（越热门的号码越被高估）
        front_undervalued = {i: 1 - front_popularity.get(i, 0.5) for i in range(1, self.n_front + 1)}
        back_undervalued = {i: 1 - back_popularity.get(i, 0.5) for i in range(1, self.n_back + 1)}
        
        # 添加一些随机性避免完全确定性的选择
        for i in range(1, self.n_front + 1):
            front_undervalued[i] += random.random() * 0.2
        for i in range(1, self.n_back + 1):
            back_undervalued[i] += random.random() * 0.2
        
        front_sorted = sorted(range(1, self.n_front + 1),
                            key=lambda x: front_undervalued.get(x, 0), reverse=True)
        back_sorted = sorted(range(1, self.n_back + 1),
                           key=lambda x: back_undervalued.get(x, 0), reverse=True)
        
        return front_sorted[:front_k], back_sorted[:back_k]
    
    def pool_genetic(self, stats: Dict, front_k: int = 5, back_k: int = 2) -> Tuple[List[int], List[int]]:
        """池5：遗传池 - 基于多样性优化选择
        
        遗传算法原理：
        - 初始种群：随机生成多个候选解
        - 适应度函数：覆盖度 + 多样性
        - 交叉：两个候选解交换部分基因
        - 变异：随机改变部分基因
        - 迭代：多代进化后选择最优解
        """
        POP_SIZE = 50
        GENERATIONS = 30
        MUTATION_RATE = 0.1
        
        def create_individual():
            """创建个体：随机选择front_k个前区 + back_k个后区"""
            front_pool = list(range(1, self.n_front + 1))
            back_pool = list(range(1, self.n_back + 1))
            random.shuffle(front_pool)
            random.shuffle(back_pool)
            return sorted(front_pool[:front_k]), back_pool[:back_k]
        
        def fitness(individual):
            """适应度函数"""
            front, back = individual
            # 多样性得分：号码之间的间隔越大越好
            front_diversity = sum(b - a for a, b in zip(front[:-1], front[1:])) / max(front_k - 1, 1)
            back_diversity = sum(abs(back[j+1] - back[j]) for j in range(len(back)-1)) / max(back_k - 1, 1)
            
            # 频率得分：避免极端频率
            front_freq_score = sum(stats['front_freq'].get(n, 0) for n in front) / stats['total_periods']
            back_freq_score = sum(stats['back_freq'].get(n, 0) for n in back) / stats['total_periods']
            
            # 综合得分：多样性*0.6 + 避免极端*0.4
            return front_diversity * 0.3 + back_diversity * 0.3 - abs(front_freq_score - 0.15) * 0.2 - abs(back_freq_score - 0.167) * 0.2
        
        def crossover(parent1, parent2):
            """交叉操作"""
            front1, back1 = parent1
            front2, back2 = parent2
            # 前区交叉：随机选择部分基因
            cut = random.randint(1, front_k - 1)
            child_front = sorted(set(front1[:cut] + front2[cut:]))
            # 补足到front_k
            while len(child_front) < front_k:
                candidate = random.randint(1, self.n_front)
                if candidate not in child_front:
                    child_front.append(candidate)
            child_front = sorted(child_front)
            # 后区交叉
            child_back = list(back1) if random.random() > 0.5 else list(back2)
            return child_front, child_back
        
        def mutate(individual):
            """变异操作"""
            front, back = individual
            front, back = list(front), list(back)
            if random.random() < MUTATION_RATE:
                idx = random.randint(0, front_k - 1)
                new_num = random.randint(1, self.n_front)
                if new_num not in front:
                    front[idx] = new_num
                    front = sorted(front)
            if random.random() < MUTATION_RATE:
                idx = random.randint(0, back_k - 1)
                new_num = random.randint(1, self.n_back)
                if new_num not in back:
                    back[idx] = new_num
            return front, back
        
        # 初始化种群
        population = [create_individual() for _ in range(POP_SIZE)]
        
        # 进化
        for _ in range(GENERATIONS):
            # 评估适应度
            fitness_scores = [(ind, fitness(ind)) for ind in population]
            fitness_scores.sort(key=lambda x: x[1], reverse=True)
            
            # 选择最优
            survivors = [ind for ind, _ in fitness_scores[:POP_SIZE // 2]]
            
            # 生成新一代
            new_population = survivors.copy()
            while len(new_population) < POP_SIZE:
                p1, p2 = random.sample(survivors, 2)
                child = crossover(p1, p2)
                child = mutate(child)
                new_population.append(child)
            
            population = new_population
        
        # 返回最优解
        best = max(population, key=fitness)
        return list(best[0]), list(best[1])
    
    def generate_all_pools(self, history: List) -> Dict[str, Dict]:
        """生成所有5个池
        
        Returns:
            Dict: {
                'hot': {'front': [...], 'back': [...], 'strategy': '热号策略'},
                'cold': {'front': [...], 'back': [...], 'strategy': '冷号策略'},
                'balanced': {'front': [...], 'back': [...], 'strategy': '均衡策略'},
                'game_theory': {'front': [...], 'back': [...], 'strategy': '博弈策略'},
                'genetic': {'front': [...], 'back': [...], 'strategy': '遗传策略'}
            }
        """
        stats = self.build_frequency_stats(history)
        
        pools = {}
        
        # 生成5个池
        front_h, back_h = self.pool_hot(stats)
        pools['hot'] = {
            'front': front_h,
            'back': back_h,
            'strategy': '热号策略',
            'description': '选择近期出现频率最高的号码，基于"强者恒强"假设'
        }
        
        front_c, back_c = self.pool_cold(stats)
        pools['cold'] = {
            'front': front_c,
            'back': back_c,
            'strategy': '冷号策略',
            'description': '选择遗漏值最高的号码，基于"冷号反弹"假设'
        }
        
        front_b, back_b = self.pool_balanced(stats)
        pools['balanced'] = {
            'front': front_b,
            'back': back_b,
            'strategy': '均衡策略',
            'description': '频率和遗漏综合评估，追求平衡风险'
        }
        
        front_g, back_g = self.pool_game_theory(stats)
        pools['game_theory'] = {
            'front': front_g,
            'back': back_g,
            'strategy': '博弈策略',
            'description': '避开大众热门，选择被低估的号码，最大化期望回报'
        }
        
        front_ge, back_ge = self.pool_genetic(stats)
        pools['genetic'] = {
            'front': front_ge,
            'back': back_ge,
            'strategy': '遗传策略',
            'description': '基于遗传算法优化，追求号码多样性覆盖'
        }
        
        return pools
    
    def generate_compound_bets(self, history: List, n_sets: int = 5) -> List[Dict]:
        """生成n组6+4复式投注组合
        
        从5个池中选择n组，确保多样性
        """
        pools = self.generate_all_pools(history)
        pool_names = list(pools.keys())
        
        # 选择策略：优先选择不同的池
        selected_pools = []
        remaining_pools = pool_names.copy()
        
        for i in range(n_sets):
            if remaining_pools:
                pool = remaining_pools.pop(0)
            else:
                # 如果所有池都用过了，从所有池中随机选择（避免重复）
                pool = random.choice(pool_names)
            selected_pools.append(pool)
        
        bets = []
        for i, pool_name in enumerate(selected_pools):
            pool = pools[pool_name]
            bets.append({
                'set_id': i + 1,
                'pool_type': pool_name,
                'front': pool['front'],
                'back': pool['back'],
                'strategy': pool['strategy'],
                'description': pool['description'],
                'compound_type': '6+4复式',
                'cost': '22元'
            })
        
        return bets

    def generate_6_plus_4(self, history: List, n: int = 5) -> List[Dict]:
        """
        生成n组6+4复式投注组合（6个前区+4个后区）
        每个池贡献一组，确保多样性
        
        Args:
            history: 历史开奖数据
            n: 生成组数（最多5组，对应5个池）
        
    Returns:
            List[Dict]: 每组包含front, back, score, pool等信息
        """
        stats = self.build_frequency_stats(history)
        total = stats['total_periods']
        
        pool_configs = [
            ('hot', '热号池', '基于"强者恒强"假设，选择近期高频号码'),
            ('cold', '冷号池', '基于"冷号反弹"假设，选择遗漏值最高号码'),
            ('balanced', '均衡池', '频率与遗漏综合，追求风险平衡'),
            ('game_theory', '博弈池', '避开大众热门，选择被低估号码'),
            ('genetic', '遗传池', '遗传算法优化，追求号码多样性覆盖'),
        ]
        
        results = []
        for pool_name, pool_label, pool_desc in pool_configs[:n]:
            if pool_name == 'hot':
                front, back = self.pool_hot(stats, front_k=6, back_k=4)
            elif pool_name == 'cold':
                front, back = self.pool_cold(stats, front_k=6, back_k=4)
            elif pool_name == 'balanced':
                front, back = self.pool_balanced(stats, front_k=6, back_k=4)
            elif pool_name == 'game_theory':
                front, back = self.pool_game_theory(stats, front_k=6, back_k=4)
            elif pool_name == 'genetic':
                front, back = self.pool_genetic(stats, front_k=6, back_k=4)
            
            # 计算多维度评分
            front_freq_sum = sum(stats['front_freq'].get(f, 0) for f in front)
            back_freq_sum = sum(stats['back_freq'].get(b, 0) for b in back)
            front_miss_sum = sum(stats['front_missing'].get(f, 0) for f in front)
            back_miss_sum = sum(stats['back_missing'].get(b, 0) for b in back)
            
            # 综合得分（归一化）
            freq_score = (front_freq_sum + back_freq_sum) / (total * 10) if total > 0 else 0
            miss_score = (front_miss_sum + back_miss_sum) / (total * 10) if total > 0 else 0
            diversity_score = len(set(front)) / 6 * 0.5 + len(set(back)) / 4 * 0.5
            overall = freq_score * 0.4 + miss_score * 0.3 + diversity_score * 0.3
            
            results.append({
                'set_id': len(results) + 1,
                'pool': pool_label,
                'pool_key': pool_name,
                'front': sorted(front),
                'back': sorted(back),
                'score': round(overall, 4),
                'freq_score': round(freq_score, 4),
                'miss_score': round(miss_score, 4),
                'diversity_score': round(diversity_score, 4),
                'strategy': pool_desc,
                'compound_type': '6+4复式',
                'cost': '22元'
            })
        
        return results


class DLTGameTheoryAnalyzer:
    """
    博弈论分析器
    分析大众偏好，避免热门组合
    """
    
    def __init__(self):
        self.hot_patterns = [
            # 连号
            lambda x: any(x[j+1]-x[j]==1 for j in range(len(x)-1)),
            # 同尾号
            lambda x: len(set(n%10 for n in x)) < len(x) * 0.6,
            # 生日号（1-12）
            lambda x: any(1 <= n <= 12 for n in x),
        ]
    
    def calculate_popularity_score(self, numbers: List[int], is_front: bool = True) -> float:
        """计算号码组合的热门度分数（越高越热门）"""
        score = 0.0
        
        # 检查连号
        sorted_nums = sorted(numbers)
        if any(sorted_nums[j+1]-sorted_nums[j] <= 2 for j in range(len(sorted_nums)-1)):
            score += 0.3
        
        # 检查同尾
        if len(set(n % 10 for n in numbers)) < len(numbers) * 0.5:
            score += 0.2
        
        # 检查生日号（前区1-12）
        if is_front:
            birthday_count = sum(1 for n in numbers if 1 <= n <= 12)
            score += birthday_count * 0.05
        
        return score
    
    def rank_by_expected_value(self, pools: Dict, history: List) -> List[Dict]:
        """根据期望回报率对池进行排序
        
        期望回报 = 理论奖金 / 选择人数
        选择热门组合会降低单注回报，选择冷门组合可能独享奖金
        """
        # 统计历史中各号码的出现频率
        front_freq = Counter()
        back_freq = Counter()
        for draw in history:
            for n in draw[0]:
                front_freq[n] += 1
            for n in draw[1]:
                back_freq[n] += 1
        
        total = len(history)
        
        ranked = []
        for pool_name, pool_data in pools.items():
            # 计算该池的平均号码频率（越低说明越冷门）
            front_popularity = sum(front_freq.get(n, 0) for n in pool_data['front']) / total
            back_popularity = sum(back_freq.get(n, 0) for n in pool_data['back']) / total
            
            # 冷门度 = 1 - 热门度（热门度越高，冷门度越低）
            coldness = 1 - (front_popularity * 0.7 + back_popularity * 0.3)
            
            # 期望回报评估（博弈论视角）
            expected_value = coldness * 1.5  # 冷门组合有更高的期望回报潜力
            
            pool_data['expected_value'] = expected_value
            pool_data['front_popularity'] = front_popularity
            pool_data['back_popularity'] = back_popularity
            ranked.append((pool_name, pool_data, expected_value))
        
        # 按期望回报排序
        ranked.sort(key=lambda x: x[2], reverse=True)
        return ranked


def format_five_pool_report(bets: List[Dict], ranked_pools: List, period: str, latest_draw: Dict) -> str:
    """格式化五池采样报告"""
    lines = []
    lines.append("=" * 60)
    lines.append(f"🎯 DLT大乐透 6+4复式投注方案")
    lines.append(f"📅 最新期号: {period}")
    lines.append(f"🎱 最新开奖: 前区{latest_draw['front']} + 后区{latest_draw['back']}")
    lines.append("=" * 60)
    lines.append("")
    
    lines.append("📊 五池分层采样分析")
    lines.append("-" * 40)
    for i, (pool_name, pool_data, ev) in enumerate(ranked_pools):
        lines.append(f"  {i+1}. {pool_data['strategy']}: 前区{pool_data['front']} 后区{pool_data['back']}")
        lines.append(f"     期望回报: {ev:.3f} | 大众热门度: 前区{pool_data['front_popularity']:.2%} 后区{pool_data['back_popularity']:.2%}")
    lines.append("")
    
    lines.append("💰 推荐的5组6+4复式投注")
    lines.append("-" * 40)
    for bet in bets:
        lines.append(f"  第{bet['set_id']}组 [{bet['pool_type']}]")
        lines.append(f"    前区: {' '.join(f'{n:02d}' for n in bet['front'])}")
        lines.append(f"    后区: {' '.join(f'{n:02d}' for n in bet['back'])}")
        lines.append(f"    策略: {bet['strategy']}")
        lines.append(f"    成本: {bet['cost']}")
        lines.append(f"    说明: {bet['description']}")
        lines.append("")
    
    lines.append("-" * 40)
    lines.append("💡 投注建议:")
    lines.append("  • 热号池适合追求稳定中奖的用户")
    lines.append("  • 博弈池适合希望独享大奖的用户")
    lines.append("  • 建议分散投注，不要把所有资金放在单一策略上")
    lines.append("=" * 60)
    
    return "\n".join(lines)
