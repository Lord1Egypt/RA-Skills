#!/usr/bin/env python3
"""
五池分层采样器 + 博弈论输出层 + 遗传优化输出层
基于DLT最终诊断报告实现的全新架构
"""

import numpy as np
import random
from typing import List, Dict, Tuple, Any, Optional
import warnings
warnings.filterwarnings('ignore')

# 导入博弈论和遗传算法模块
from modules.dlt_game_theory import DLTGameTheoryAnalyzer
from modules.dlt_genetic_optimizer import DLTGeneticOptimizer, Chromosome


class FivePoolSampler:
    """五池分层采样器 - 替代原有Stacking预测架构"""
    
    def __init__(self, draws: List[Tuple[List[int], List[int]]]):
        """
        初始化五池分层采样器
        
        Args:
            draws: 历史开奖数据，格式为[(前区5个号码, 后区2个号码), ...]
        """
        self.draws = draws  # 历史开奖数据
        self.front_balls = [d[0] for d in draws]   # 前区号码
        self.back_balls = [d[1] for d in draws]    # 后区号码
        
        # 初始化博弈论分析器
        self.game_theory_analyzer = DLTGameTheoryAnalyzer()
        
        # 初始化遗传算法优化器
        self.genetic_optimizer = DLTGeneticOptimizer(
            population_size=100,
            generations=50,
            crossover_rate=0.8,
            mutation_rate=0.2,
            elite_size=10
        )
        
        # 热冷评分缓存
        self.hot_cold_cache = {'front': {}, 'back': {}}
        
        print(f"🧬 五池分层采样器初始化完成")
        print(f"   历史数据: {len(draws)} 期")
        print(f"   前区号码范围: 1-35")
        print(f"   后区号码范围: 1-12")
    
    def _get_hot_cold_scores(self, zone: str = 'front', window: int = 30) -> Dict[int, float]:
        """
        计算号码热冷评分
        
        Args:
            zone: 'front' 或 'back'
            window: 统计窗口期数
            
        Returns:
            Dict[int, float]: {号码: 热冷评分}，评分越高表示越热
        """
        if zone in self.hot_cold_cache and len(self.hot_cold_cache[zone]) > 0:
            return self.hot_cold_cache[zone]
        
        # 确定号码范围
        if zone == 'front':
            balls_list = self.front_balls
            num_range = range(1, 36)
        else:
            balls_list = self.back_balls
            num_range = range(1, 13)
        
        # 统计最近window期出现次数
        recent_draws = balls_list[-window:] if len(balls_list) > window else balls_list
        frequency = {num: 0 for num in num_range}
        
        for draw in recent_draws:
            for num in draw:
                if num in frequency:
                    frequency[num] += 1
        
        # 计算热冷评分（归一化到0-1）
        max_freq = max(frequency.values()) if frequency else 1
        min_freq = min(frequency.values()) if frequency else 0
        
        scores = {}
        for num in num_range:
            if max_freq == min_freq:
                scores[num] = 0.5  # 所有号码出现次数相同
            else:
                scores[num] = (frequency[num] - min_freq) / (max_freq - min_freq)
        
        # 缓存结果
        self.hot_cold_cache[zone] = scores
        return scores
    
    def generate_hot_pool(self, n: int = 10, zone: str = 'front') -> List[int]:
        """
        热号池：最近30期出现次数最多的号码
        
        Args:
            n: 返回的热号数量
            zone: 'front' 或 'back'
            
        Returns:
            List[int]: 热号列表
        """
        scores = self._get_hot_cold_scores(zone)
        
        # 按评分降序排序
        sorted_nums = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        # 返回前n个热号
        hot_pool = [num for num, score in sorted_nums[:n]]
        
        print(f"🔥 生成{zone}热号池: {hot_pool}")
        return hot_pool
    
    def generate_cold_pool(self, n: int = 10, zone: str = 'front') -> List[int]:
        """
        冷号池：最近30期出现次数最少的号码
        
        Args:
            n: 返回的冷号数量
            zone: 'front' 或 'back'
            
        Returns:
            List[int]: 冷号列表
        """
        scores = self._get_hot_cold_scores(zone)
        
        # 按评分升序排序
        sorted_nums = sorted(scores.items(), key=lambda x: x[1])
        
        # 返回前n个冷号
        cold_pool = [num for num, score in sorted_nums[:n]]
        
        print(f"❄️ 生成{zone}冷号池: {cold_pool}")
        return cold_pool
    
    def generate_balance_pool(self, n: int = 10, zone: str = 'front') -> List[int]:
        """
        均衡池：热冷号各取一半
        
        Args:
            n: 返回的均衡号数量
            zone: 'front' 或 'back'
            
        Returns:
            List[int]: 均衡号列表
        """
        hot_pool = self.generate_hot_pool(n // 2, zone)
        cold_pool = self.generate_cold_pool(n // 2, zone)
        
        # 合并并去重
        balance_pool = list(set(hot_pool + cold_pool))
        
        # 如果数量不足，补充随机号码
        if len(balance_pool) < n:
            if zone == 'front':
                all_nums = list(range(1, 36))
            else:
                all_nums = list(range(1, 13))
            
            available = [num for num in all_nums if num not in balance_pool]
            if available:
                needed = n - len(balance_pool)
                balance_pool.extend(random.sample(available, min(needed, len(available))))
        
        print(f"⚖️ 生成{zone}均衡池: {balance_pool[:n]}")
        return balance_pool[:n]
    
    def generate_game_theory_pool(self, n: int = 10, zone: str = 'front') -> List[int]:
        """
        博弈池：参考dlt_game_theory.py的期望值分析
        
        Args:
            n: 返回的博弈号数量
            zone: 'front' 或 'back'
            
        Returns:
            List[int]: 博弈号列表
        """
        if zone == 'front':
            num_range = list(range(1, 36))
        else:
            num_range = list(range(1, 13))
        
        # 生成随机组合并评估博弈论分数
        combo_scores = []
        
        for _ in range(1000):  # 生成1000个随机组合进行评估
            combo = sorted(random.sample(num_range, 5 if zone == 'front' else 2))
            
            # 使用博弈论分析器评估组合
            analysis = self.game_theory_analyzer.analyze_combo(combo)
            score = analysis['scores']['combined_score']
            
            combo_scores.append((combo, score))
        
        # 按分数降序排序
        combo_scores.sort(key=lambda x: x[1], reverse=True)
        
        # 提取所有号码并计算平均分数
        num_scores = {}
        for combo, score in combo_scores[:100]:  # 取前100个最佳组合
            for num in combo:
                if num not in num_scores:
                    num_scores[num] = []
                num_scores[num].append(score)
        
        # 计算每个号码的平均博弈论分数
        avg_scores = {num: np.mean(scores) for num, scores in num_scores.items()}
        
        # 按平均分数降序排序
        sorted_nums = sorted(avg_scores.items(), key=lambda x: x[1], reverse=True)
        
        # 返回前n个号码
        game_pool = [num for num, score in sorted_nums[:n]]
        
        print(f"🎯 生成{zone}博弈池: {game_pool}")
        return game_pool
    
    def generate_genetic_pool(self, n: int = 10, zone: str = 'front') -> List[int]:
        """
        遗传池：参考dlt_genetic_optimizer.py的遗传算法
        
        Args:
            n: 返回的遗传号数量
            zone: 'front' 或 'back'
            
        Returns:
            List[int]: 遗传号列表
        """
        # 生成概率分布（基于热冷评分）
        scores = self._get_hot_cold_scores(zone)
        
        if zone == 'front':
            probs = np.zeros(35)
            for num, score in scores.items():
                probs[num-1] = score + 0.1  # 添加平滑项
        else:
            probs = np.zeros(12)
            for num, score in scores.items():
                probs[num-1] = score + 0.1
        
        # 归一化概率
        probs = probs / probs.sum()
        
        # 使用遗传算法优化
        if zone == 'front':
            # 前区优化
            results = self.genetic_optimizer.optimize_with_probabilities(
                front_probs=probs,
                back_probs=np.ones(12) / 12,  # 后区使用均匀分布
                top_k=5
            )
            
            # 提取前区号码
            genetic_numbers = []
            for result in results:
                genetic_numbers.extend(result['front_numbers'])
        else:
            # 后区优化
            results = self.genetic_optimizer.optimize_with_probabilities(
                front_probs=np.ones(35) / 35,  # 前区使用均匀分布
                back_probs=probs,
                top_k=5
            )
            
            # 提取后区号码
            genetic_numbers = []
            for result in results:
                genetic_numbers.extend(result['back_numbers'])
        
        # 去重并限制数量
        genetic_pool = list(set(genetic_numbers))[:n]
        
        print(f"🧬 生成{zone}遗传池: {genetic_pool}")
        return genetic_pool
    
    def stratified_sample(self, n_combinations: int = 5, zone: str = 'front') -> List[List[int]]:
        """
        分层采样：5池各取一定比例，生成n组不同组合
        
        采样比例：热号40% + 冷号20% + 均衡25% + 博弈10% + 遗传5%
        
        Args:
            n_combinations: 生成的组合数量
            zone: 'front' 或 'back'
            
        Returns:
            List[List[int]]: 生成的组合列表
        """
        # 生成各池
        hot_pool = self.generate_hot_pool(20, zone)
        cold_pool = self.generate_cold_pool(20, zone)
        balance_pool = self.generate_balance_pool(20, zone)
        game_pool = self.generate_game_theory_pool(20, zone)
        genetic_pool = self.generate_genetic_pool(20, zone)
        
        # 确定组合大小
        if zone == 'front':
            combo_size = 5
        else:
            combo_size = 2
        
        combinations = []
        
        for _ in range(n_combinations):
            combo = []
            
            # 热号池贡献40%
            hot_count = int(combo_size * 0.4)
            if hot_pool and hot_count > 0:
                combo.extend(random.sample(hot_pool, min(hot_count, len(hot_pool))))
            
            # 冷号池贡献20%
            cold_count = int(combo_size * 0.2)
            if cold_pool and cold_count > 0:
                combo.extend(random.sample(cold_pool, min(cold_count, len(cold_pool))))
            
            # 均衡池贡献25%
            balance_count = int(combo_size * 0.25)
            if balance_pool and balance_count > 0:
                combo.extend(random.sample(balance_pool, min(balance_count, len(balance_pool))))
            
            # 博弈池贡献10%
            game_count = int(combo_size * 0.1)
            if game_pool and game_count > 0:
                combo.extend(random.sample(game_pool, min(game_count, len(game_pool))))
            
            # 遗传池贡献5%
            genetic_count = int(combo_size * 0.05)
            if genetic_pool and genetic_count > 0:
                combo.extend(random.sample(genetic_pool, min(genetic_count, len(genetic_pool))))
            
            # 如果数量不足，从热号池补充
            if len(combo) < combo_size:
                needed = combo_size - len(combo)
                available = [num for num in hot_pool if num not in combo]
                if available:
                    combo.extend(random.sample(available, min(needed, len(available))))
            
            # 如果仍然不足，从所有号码中随机选择
            if len(combo) < combo_size:
                needed = combo_size - len(combo)
                if zone == 'front':
                    all_nums = list(range(1, 36))
                else:
                    all_nums = list(range(1, 13))
                
                available = [num for num in all_nums if num not in combo]
                if available:
                    combo.extend(random.sample(available, min(needed, len(available))))
            
            # 排序并添加到结果
            combo = sorted(combo[:combo_size])
            if combo not in combinations:
                combinations.append(combo)
        
        print(f"🎲 生成{zone}分层采样组合: {len(combinations)} 组")
        return combinations
    
    def generate_6_plus_4(self, n: int = 5) -> List[Dict[str, Any]]:
        """
        生成n组6+4复式投注
        
        前区6个号码 + 后区4个号码
        
        Args:
            n: 生成的复式投注数量
            
        Returns:
            List[Dict[str, Any]]: 复式投注列表，包含前区和后区号码
        """
        results = []
        
        for i in range(n):
            # 生成前区6个号码（使用分层采样）
            front_combinations = self.stratified_sample(n_combinations=10, zone='front')
            
            # 选择最佳前区组合（基于博弈论分数）
            best_front = None
            best_score = -1
            
            for combo in front_combinations:
                analysis = self.game_theory_analyzer.analyze_combo(combo)
                score = analysis['scores']['combined_score']
                
                if score > best_score:
                    best_score = score
                    best_front = combo
            
            # 如果找不到最佳组合，使用第一个
            if best_front is None and front_combinations:
                best_front = front_combinations[0]
            
            # 扩展前区到6个号码（从热号池补充）
            if best_front and len(best_front) < 6:
                hot_pool = self.generate_hot_pool(20, 'front')
                available = [num for num in hot_pool if num not in best_front]
                if available:
                    needed = 6 - len(best_front)
                    best_front.extend(random.sample(available, min(needed, len(available))))
                    best_front = sorted(best_front)
            
            # 如果仍然不足6个，随机补充
            if len(best_front) < 6:
                needed = 6 - len(best_front)
                all_nums = list(range(1, 36))
                available = [num for num in all_nums if num not in best_front]
                if available:
                    best_front.extend(random.sample(available, min(needed, len(available))))
                    best_front = sorted(best_front)
            
            # 生成后区4个号码（使用分层采样）
            back_combinations = self.stratified_sample(n_combinations=10, zone='back')
            
            # 选择最佳后区组合（基于热冷评分）
            best_back = None
            best_back_score = -1
            
            for combo in back_combinations:
                # 计算后区组合的平均热冷评分
                scores = self._get_hot_cold_scores('back')
                avg_score = np.mean([scores.get(num, 0.5) for num in combo])
                
                if avg_score > best_back_score:
                    best_back_score = avg_score
                    best_back = combo
            
            # 如果找不到最佳组合，使用第一个
            if best_back is None and back_combinations:
                best_back = back_combinations[0]
            
            # 扩展后区到4个号码（从热号池补充）
            if best_back and len(best_back) < 4:
                hot_pool_back = self.generate_hot_pool(10, 'back')
                available = [num for num in hot_pool_back if num not in best_back]
                if available:
                    needed = 4 - len(best_back)
                    best_back.extend(random.sample(available, min(needed, len(available))))
                    best_back = sorted(best_back)
            
            # 如果仍然不足4个，随机补充
            if len(best_back) < 4:
                needed = 4 - len(best_back)
                available = [num for num in range(1, 13) if num not in best_back]
                if available:
                    best_back.extend(random.sample(available, min(needed, len(available))))
                    best_back = sorted(best_back)

            # 计算策略评分
            try:
                gt_analysis = self.game_theory_analyzer.analyze_combo(best_front)
                strategy_score = gt_analysis['scores']['combined_score']
            except:
                strategy_score = 0.5

            results.append({
                'front': sorted(best_front) if best_front else [],
                'back': sorted(best_back) if best_back else [],
                'front_count': len(best_front) if best_front else 0,
                'back_count': len(best_back) if best_back else 0,
                'pool_type': 'genetic',
                'strategy_score': strategy_score,
                'bet_type': f'6+4'
            })

        return results

    def generate_compound_bet(self, front_count: int, back_count: int,
                              strategy: str = 'game_theory', n: int = 1) -> List[Dict[str, Any]]:
        """
        生成指定格式的复式投注（前区front_count个号码 + 后区back_count个号码）

        Args:
            front_count: 前区号码个数（5-9）
            back_count: 后区号码个数（2-6）
            strategy: 策略池 ('hot', 'cold', 'balance', 'game_theory', 'genetic', 'mixed')
            n: 生成多少组

        Returns:
            List[Dict]: 每组包含 front, back, pool_type, strategy_score
        """
        results = []
        for _ in range(n):
            # 根据strategy选择池
            if strategy == 'hot':
                front_pool = self.generate_hot_pool(20, 'front')
                back_pool = self.generate_hot_pool(8, 'back')
            elif strategy == 'cold':
                front_pool = self.generate_cold_pool(20, 'front')
                back_pool = self.generate_cold_pool(8, 'back')
            elif strategy == 'balance':
                front_pool = self.generate_balance_pool(20, 'front')
                back_pool = self.generate_balance_pool(8, 'back')
            elif strategy == 'game_theory':
                front_pool = self.generate_game_theory_pool(20, 'front')
                back_pool = self.generate_game_theory_pool(8, 'back')
            elif strategy == 'genetic':
                front_pool = self.generate_genetic_pool(20, 'front')
                back_pool = self.generate_genetic_pool(8, 'back')
            else:  # mixed
                pools = [
                    self.generate_hot_pool(10, 'front'),
                    self.generate_cold_pool(10, 'front'),
                    self.generate_balance_pool(10, 'front'),
                ]
                front_pool = []
                for p in pools:
                    for num in p:
                        if num not in front_pool:
                            front_pool.append(num)
                back_pools = [
                    self.generate_hot_pool(4, 'back'),
                    self.generate_cold_pool(4, 'back'),
                    self.generate_balance_pool(4, 'back'),
                ]
                back_pool = []
                for p in back_pools:
                    for num in p:
                        if num not in back_pool:
                            back_pool.append(num)

            # 确保池足够大
            if len(front_pool) < front_count or len(back_pool) < back_count:
                all_front = list(range(1, 36))
                all_back = list(range(1, 13))
                if len(front_pool) < front_count:
                    front_pool = all_front[:front_count]
                if len(back_pool) < back_count:
                    back_pool = all_back[:back_count]

            # 按博弈论分数排序选择前区
            scored = []
            for num in front_pool[:max(front_count, len(front_pool))]:
                try:
                    analysis = self.game_theory_analyzer.analyze_combo([num])
                    score = analysis['scores']['combined_score']
                except:
                    score = 0.5
                scored.append((num, score))
            scored.sort(key=lambda x: x[1], reverse=True)
            front = sorted([x[0] for x in scored[:front_count]])

            # 后区：直接取前back_count个
            back = sorted(back_pool[:back_count])

            # 计算策略评分
            try:
                gt_analysis = self.game_theory_analyzer.analyze_combo(front)
                strategy_score = gt_analysis['scores']['combined_score']
            except:
                strategy_score = 0.5

            results.append({
                'front': front,
                'back': back,
                'front_count': len(front),
                'back_count': len(back),
                'pool_type': strategy,
                'strategy_score': strategy_score,
                'bet_type': f'{len(front)}+{len(back)}'
            })

        return results

    def generate_6_plus_3(self, n: int = 5, strategy: str = 'game_theory') -> List[Dict[str, Any]]:
        """生成n组6+3复式投注"""
        return self.generate_compound_bet(6, 3, strategy, n)

    def generate_7_plus_2(self, n: int = 5, strategy: str = 'mixed') -> List[Dict[str, Any]]:
        """生成n组7+2复式投注"""
        return self.generate_compound_bet(7, 2, strategy, n)

    def generate_7_plus_3(self, n: int = 5, strategy: str = 'mixed') -> List[Dict[str, Any]]:
        """生成n组7+3复式投注"""
        return self.generate_compound_bet(7, 3, strategy, n)

    def generate_8_plus_2(self, n: int = 5, strategy: str = 'hot') -> List[Dict[str, Any]]:
        """生成n组8+2复式投注"""
        return self.generate_compound_bet(8, 2, strategy, n)

    def generate_8_plus_3(self, n: int = 5, strategy: str = 'mixed') -> List[Dict[str, Any]]:
        """生成n组8+3复式投注"""
        return self.generate_compound_bet(8, 3, strategy, n)

    def generate_9_plus_3(self, n: int = 5, strategy: str = 'cold') -> List[Dict[str, Any]]:
        """生成n组9+3复式投注"""
        return self.generate_compound_bet(9, 3, strategy, n)

    def generate_9_plus_4(self, n: int = 5, strategy: str = 'cold') -> List[Dict[str, Any]]:
        """生成n组9+4复式投注"""
        return self.generate_compound_bet(9, 4, strategy, n)

    def generate_9_plus_6(self, n: int = 5, strategy: str = 'balance') -> List[Dict[str, Any]]:
        """生成n组9+6复式投注"""
        return self.generate_compound_bet(9, 6, strategy, n)
    # ============================================================
    # 复式投注生成方法（前区5-9 + 后区2-6）
    # ============================================================

    def generate_compound_bet(self, front_count: int, back_count: int,
                              strategy: str = 'game_theory', n: int = 1) -> List[Dict[str, Any]]:
        """
        生成指定格式的复式投注（前区front_count个号码 + 后区back_count个号码）

        Args:
            front_count: 前区号码个数（5-9）
            back_count: 后区号码个数（2-6）
            strategy: 策略池 ('hot', 'cold', 'balance', 'game_theory', 'genetic', 'mixed')
            n: 生成多少组

        Returns:
            List[Dict]: 每组包含 front, back, pool_type, strategy_score
        """
        results = []
        all_front = list(range(1, 36))
        all_back = list(range(1, 13))

        for _ in range(n):
            # 根据strategy选择池
            if strategy == 'hot':
                front_pool = self.generate_hot_pool(20, 'front')
                back_pool = self.generate_hot_pool(8, 'back')
            elif strategy == 'cold':
                front_pool = self.generate_cold_pool(20, 'front')
                back_pool = self.generate_cold_pool(8, 'back')
            elif strategy == 'balance':
                front_pool = self.generate_balance_pool(20, 'front')
                back_pool = self.generate_balance_pool(8, 'back')
            elif strategy == 'game_theory':
                front_pool = self.generate_game_theory_pool(20, 'front')
                back_pool = self.generate_game_theory_pool(8, 'back')
            elif strategy == 'genetic':
                front_pool = self.generate_genetic_pool(20, 'front')
                back_pool = self.generate_genetic_pool(8, 'back')
            else:  # mixed
                pools_f = [self.generate_hot_pool(8, 'front'),
                           self.generate_cold_pool(8, 'front'),
                           self.generate_balance_pool(8, 'front')]
                front_pool = []
                for p in pools_f:
                    for num in p:
                        if num not in front_pool:
                            front_pool.append(num)
                pools_b = [self.generate_hot_pool(4, 'back'),
                           self.generate_cold_pool(4, 'back'),
                           self.generate_balance_pool(4, 'back')]
                back_pool = []
                for p in pools_b:
                    for num in p:
                        if num not in back_pool:
                            back_pool.append(num)

            # 确保池足够大
            if len(front_pool) < front_count:
                for num in all_front:
                    if num not in front_pool:
                        front_pool.append(num)
                    if len(front_pool) >= front_count:
                        break
            if len(back_pool) < back_count:
                for num in all_back:
                    if num not in back_pool:
                        back_pool.append(num)
                    if len(back_pool) >= back_count:
                        break

            # 按博弈论分数排序选择前区
            scored = []
            for num in front_pool[:max(front_count, len(front_pool))]:
                try:
                    analysis = self.game_theory_analyzer.analyze_combo([num])
                    score = analysis['scores']['combined_score']
                except:
                    score = 0.5
                scored.append((num, score))
            scored.sort(key=lambda x: x[1], reverse=True)
            front = sorted([x[0] for x in scored[:front_count]])

            # 后区：直接取前back_count个
            back = sorted(back_pool[:back_count])

            # 计算策略评分
            try:
                gt_analysis = self.game_theory_analyzer.analyze_combo(front)
                strategy_score = gt_analysis['scores']['combined_score']
            except:
                strategy_score = 0.5

            results.append({
                'front': front,
                'back': back,
                'front_count': len(front),
                'back_count': len(back),
                'pool_type': strategy,
                'strategy_score': strategy_score,
                'bet_type': f'{len(front)}+{len(back)}'
            })

        return results

    def generate_6_plus_3(self, n: int = 5, strategy: str = 'game_theory') -> List[Dict[str, Any]]:
        """生成n组6+3复式投注"""
        return self.generate_compound_bet(6, 3, strategy, n)

    def generate_7_plus_2(self, n: int = 5, strategy: str = 'mixed') -> List[Dict[str, Any]]:
        """生成n组7+2复式投注"""
        return self.generate_compound_bet(7, 2, strategy, n)

    def generate_7_plus_3(self, n: int = 5, strategy: str = 'mixed') -> List[Dict[str, Any]]:
        """生成n组7+3复式投注"""
        return self.generate_compound_bet(7, 3, strategy, n)

    def generate_8_plus_2(self, n: int = 5, strategy: str = 'hot') -> List[Dict[str, Any]]:
        """生成n组8+2复式投注"""
        return self.generate_compound_bet(8, 2, strategy, n)

    def generate_8_plus_3(self, n: int = 5, strategy: str = 'mixed') -> List[Dict[str, Any]]:
        """生成n组8+3复式投注"""
        return self.generate_compound_bet(8, 3, strategy, n)

    def generate_9_plus_3(self, n: int = 5, strategy: str = 'cold') -> List[Dict[str, Any]]:
        """生成n组9+3复式投注"""
        return self.generate_compound_bet(9, 3, strategy, n)

    def generate_9_plus_4(self, n: int = 5, strategy: str = 'cold') -> List[Dict[str, Any]]:
        """生成n组9+4复式投注"""
        return self.generate_compound_bet(9, 4, strategy, n)

    def generate_9_plus_6(self, n: int = 5, strategy: str = 'balance') -> List[Dict[str, Any]]:
        """生成n组9+6复式投注"""
        return self.generate_compound_bet(9, 6, strategy, n)

    def generate_6_plus_4(self, n: int = 5, strategy: str = 'game_theory') -> List[Dict[str, Any]]:
        """生成n组6+4复式投注（前区6个+后区4个）"""
        return self.generate_compound_bet(6, 4, strategy, n)

    def generate_7_plus_3(self, n: int = 5, strategy: str = 'mixed') -> List[Dict[str, Any]]:
        """生成n组7+3复式投注（前区7个+后区3个）"""
        return self.generate_compound_bet(7, 3, strategy, n)

    def generate_7_plus_4(self, n: int = 5, strategy: str = 'balance') -> List[Dict[str, Any]]:
        """生成n组7+4复式投注（前区7个+后区4个）"""
        return self.generate_compound_bet(7, 4, strategy, n)

    def generate_8_plus_4(self, n: int = 5, strategy: str = 'cold') -> List[Dict[str, Any]]:
        """生成n组8+4复式投注（前区8个+后区4个）"""
        return self.generate_compound_bet(8, 4, strategy, n)

    def generate_8_plus_5(self, n: int = 5, strategy: str = 'cold') -> List[Dict[str, Any]]:
        """生成n组8+5复式投注（前区8个+后区5个）"""
        return self.generate_compound_bet(8, 5, strategy, n)
