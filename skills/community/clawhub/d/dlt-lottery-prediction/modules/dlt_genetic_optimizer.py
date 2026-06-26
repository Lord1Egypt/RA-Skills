#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DLT遗传算法优化器 - 使用遗传算法优化号码组合
基于进化算法寻找最优的6+3组合
"""

import numpy as np
import random
from typing import List, Dict, Any, Tuple, Callable
from dataclasses import dataclass
from copy import deepcopy
import warnings
warnings.filterwarnings('ignore')

@dataclass
class Chromosome:
    """染色体 - 表示一个6+3组合"""
    front_numbers: List[int]  # 前区6个号码
    back_numbers: List[int]   # 后区3个号码
    fitness: float = 0.0      # 适应度分数
    
    def __post_init__(self):
        """初始化后处理"""
        self.front_numbers = sorted(self.front_numbers)
        self.back_numbers = sorted(self.back_numbers)
    
    def __str__(self):
        return f"前区: {self.front_numbers} | 后区: {self.back_numbers} | 适应度: {self.fitness:.4f}"


class DLTGeneticOptimizer:
    """DLT遗传算法优化器"""
    
    def __init__(self, 
                 population_size: int = 100,
                 generations: int = 50,
                 crossover_rate: float = 0.8,
                 mutation_rate: float = 0.2,
                 elite_size: int = 10):
        """初始化遗传算法优化器"""
        self.population_size = population_size
        self.generations = generations
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.elite_size = elite_size
        
        # 搜索空间
        self.front_range = (1, 35)  # 前区范围
        self.back_range = (1, 12)   # 后区范围
        
        # 种群
        self.population: List[Chromosome] = []
        self.best_chromosome: Chromosome = None
        self.fitness_history: List[float] = []
        
        # 适应度函数
        self.fitness_function: Callable = None
        
        print(f"🧬 DLT遗传算法优化器初始化")
        print(f"   种群大小: {population_size}")
        print(f"   进化代数: {generations}")
        print(f"   交叉率: {crossover_rate}")
        print(f"   变异率: {mutation_rate}")
        print(f"   精英保留: {elite_size}")
    
    def set_fitness_function(self, fitness_func: Callable):
        """设置适应度函数"""
        self.fitness_function = fitness_func
        print("✅ 适应度函数已设置")
    
    def initialize_population(self):
        """初始化种群"""
        print("🧬 初始化种群...")
        
        self.population = []
        
        for _ in range(self.population_size):
            # 随机生成前区6个号码
            front_numbers = random.sample(
                range(self.front_range[0], self.front_range[1] + 1), 
                6
            )
            
            # 随机生成后区3个号码
            back_numbers = random.sample(
                range(self.back_range[0], self.back_range[1] + 1), 
                3
            )
            
            chromosome = Chromosome(
                front_numbers=sorted(front_numbers),
                back_numbers=sorted(back_numbers)
            )
            
            self.population.append(chromosome)
        
        print(f"✅ 种群初始化完成: {len(self.population)} 个个体")
    
    def evaluate_fitness(self, hot_numbers: Dict[str, List[int]] = None):
        """评估种群适应度"""
        if self.fitness_function is None:
            # 使用默认适应度函数
            self._default_fitness_evaluation(hot_numbers)
        else:
            # 使用自定义适应度函数
            for chromosome in self.population:
                chromosome.fitness = self.fitness_function(chromosome)
        
        # 按适应度排序
        self.population.sort(key=lambda x: x.fitness, reverse=True)
        
        # 更新最佳染色体
        if self.best_chromosome is None or self.population[0].fitness > self.best_chromosome.fitness:
            self.best_chromosome = deepcopy(self.population[0])
        
        # 记录适应度历史
        avg_fitness = np.mean([c.fitness for c in self.population])
        self.fitness_history.append(avg_fitness)
    
    def _default_fitness_evaluation(self, hot_numbers: Dict[str, List[int]] = None):
        """默认适应度评估函数"""
        if hot_numbers is None:
            hot_numbers = {
                'front_hot': list(range(1, 36))[:15],  # 前15个为热号
                'back_hot': list(range(1, 13))[:6]     # 前6个为热号
            }
        
        for chromosome in self.population:
            fitness = 0.0
            
            # 1. 热号比例 (40%)
            front_hot_count = len(set(chromosome.front_numbers) & set(hot_numbers['front_hot']))
            back_hot_count = len(set(chromosome.back_numbers) & set(hot_numbers['back_hot']))
            
            fitness += (front_hot_count / 6) * 0.3  # 前区热号比例
            fitness += (back_hot_count / 3) * 0.1   # 后区热号比例
            
            # 2. 奇偶平衡 (20%)
            front_odd_count = sum(1 for n in chromosome.front_numbers if n % 2 == 1)
            back_odd_count = sum(1 for n in chromosome.back_numbers if n % 2 == 1)
            
            # 理想奇偶比: 前区3:3或4:2，后区1:2或2:1
            front_odd_score = 1 - abs(front_odd_count - 3) / 3  # 越接近3分越高
            back_odd_score = 1 - abs(back_odd_count - 1.5) / 1.5  # 越接近1.5分越高
            
            fitness += front_odd_score * 0.15
            fitness += back_odd_score * 0.05
            
            # 3. 号码分布 (15%)
            # 检查号码是否均匀分布在1-35之间
            front_spread = max(chromosome.front_numbers) - min(chromosome.front_numbers)
            spread_score = min(front_spread / 30, 1.0)  # 最大差30为满分
            
            fitness += spread_score * 0.15
            
            # 4. 连号控制 (10%)
            # 检查是否有过多连号
            front_sorted = sorted(chromosome.front_numbers)
            consecutive_count = 0
            for i in range(len(front_sorted) - 1):
                if front_sorted[i+1] - front_sorted[i] == 1:
                    consecutive_count += 1
            
            consecutive_score = 1 - min(consecutive_count / 2, 1.0)  # 最多允许2个连号
            
            fitness += consecutive_score * 0.10
            
            # 5. 和值范围 (10%)
            front_sum = sum(chromosome.front_numbers)
            # 理想和值范围: 90-130
            if 90 <= front_sum <= 130:
                sum_score = 1.0
            else:
                sum_score = 1 - min(abs(front_sum - 110) / 50, 1.0)  # 离110越近分越高
            
            fitness += sum_score * 0.10
            
            # 6. 重复模式惩罚 (5%)
            # 检查是否有重复的号码对模式
            pattern_penalty = 0
            for i in range(len(front_sorted) - 1):
                diff = front_sorted[i+1] - front_sorted[i]
                if diff < 3:  # 号码过于密集
                    pattern_penalty += 0.02
            
            fitness -= pattern_penalty
            
            # 确保适应度在0-1之间
            chromosome.fitness = max(0, min(fitness, 1))
    
    def selection(self) -> List[Chromosome]:
        """选择操作 - 轮盘赌选择"""
        # 计算适应度总和
        total_fitness = sum(c.fitness for c in self.population)
        
        # 计算选择概率
        if total_fitness == 0:
            # 如果所有适应度都为0，均匀选择
            probabilities = [1/len(self.population)] * len(self.population)
        else:
            probabilities = [c.fitness / total_fitness for c in self.population]
        
        # 轮盘赌选择
        selected = []
        for _ in range(self.population_size - self.elite_size):
            r = random.random()
            cumulative = 0
            for i, prob in enumerate(probabilities):
                cumulative += prob
                if r <= cumulative:
                    selected.append(deepcopy(self.population[i]))
                    break
        
        return selected
    
    def crossover(self, parent1: Chromosome, parent2: Chromosome) -> Tuple[Chromosome, Chromosome]:
        """交叉操作 - 两点交叉"""
        if random.random() > self.crossover_rate:
            return deepcopy(parent1), deepcopy(parent2)
        
        # 前区交叉
        front_crossover_point = random.randint(1, 5)
        
        child1_front = parent1.front_numbers[:front_crossover_point] + parent2.front_numbers[front_crossover_point:]
        child2_front = parent2.front_numbers[:front_crossover_point] + parent1.front_numbers[front_crossover_point:]
        
        # 去重并补充
        child1_front = self._repair_chromosome(child1_front, self.front_range, 6)
        child2_front = self._repair_chromosome(child2_front, self.front_range, 6)
        
        # 后区交叉
        back_crossover_point = random.randint(1, 2)
        
        child1_back = parent1.back_numbers[:back_crossover_point] + parent2.back_numbers[back_crossover_point:]
        child2_back = parent2.back_numbers[:back_crossover_point] + parent1.back_numbers[back_crossover_point:]
        
        # 去重并补充
        child1_back = self._repair_chromosome(child1_back, self.back_range, 3)
        child2_back = self._repair_chromosome(child2_back, self.back_range, 3)
        
        child1 = Chromosome(front_numbers=child1_front, back_numbers=child1_back)
        child2 = Chromosome(front_numbers=child2_front, back_numbers=child2_back)
        
        return child1, child2
    
    def mutation(self, chromosome: Chromosome) -> Chromosome:
        """变异操作"""
        mutated = deepcopy(chromosome)
        
        # 前区变异
        if random.random() < self.mutation_rate:
            # 随机替换一个号码
            idx = random.randint(0, 5)
            current = mutated.front_numbers[idx]
            
            # 选择不在当前组合中的号码
            available = [n for n in range(self.front_range[0], self.front_range[1] + 1) 
                        if n not in mutated.front_numbers]
            
            if available:
                mutated.front_numbers[idx] = random.choice(available)
                mutated.front_numbers.sort()
        
        # 后区变异
        if random.random() < self.mutation_rate:
            # 随机替换一个号码
            idx = random.randint(0, 2)
            current = mutated.back_numbers[idx]
            
            # 选择不在当前组合中的号码
            available = [n for n in range(self.back_range[0], self.back_range[1] + 1) 
                        if n not in mutated.back_numbers]
            
            if available:
                mutated.back_numbers[idx] = random.choice(available)
                mutated.back_numbers.sort()
        
        return mutated
    
    def _repair_chromosome(self, numbers: List[int], num_range: Tuple[int, int], target_size: int) -> List[int]:
        """修复染色体（去重并补充到目标大小）"""
        # 去重
        unique_numbers = list(set(numbers))
        
        # 如果数量不足，补充随机号码
        if len(unique_numbers) < target_size:
            available = [n for n in range(num_range[0], num_range[1] + 1) 
                        if n not in unique_numbers]
            needed = target_size - len(unique_numbers)
            
            if len(available) >= needed:
                unique_numbers.extend(random.sample(available, needed))
            else:
                # 如果可用号码不足，随机生成
                while len(unique_numbers) < target_size:
                    new_num = random.randint(num_range[0], num_range[1])
                    if new_num not in unique_numbers:
                        unique_numbers.append(new_num)
        
        # 如果数量过多，随机删除
        elif len(unique_numbers) > target_size:
            unique_numbers = random.sample(unique_numbers, target_size)
        
        return sorted(unique_numbers)
    
    def evolve(self, hot_numbers: Dict[str, List[int]] = None) -> List[Chromosome]:
        """执行进化过程"""
        print(f"🔁 开始遗传算法进化 ({self.generations} 代)...")
        
        # 初始化种群
        self.initialize_population()
        
        # 进化循环
        for generation in range(self.generations):
            # 评估适应度
            self.evaluate_fitness(hot_numbers)
            
            # 输出当前代信息
            if generation % 10 == 0 or generation == self.generations - 1:
                print(f"   第{generation+1:3d}代 | 平均适应度: {self.fitness_history[-1]:.4f} | "
                      f"最佳适应度: {self.best_chromosome.fitness:.4f}")
            
            # 选择精英
            elites = self.population[:self.elite_size]
            
            # 选择
            selected = self.selection()
            
            # 交叉和变异生成新种群
            new_population = []
            
            # 保留精英
            new_population.extend(elites)
            
            # 生成后代
            while len(new_population) < self.population_size:
                # 随机选择父母
                parent1 = random.choice(selected)
                parent2 = random.choice(selected)
                
                # 交叉
                child1, child2 = self.crossover(parent1, parent2)
                
                # 变异
                child1 = self.mutation(child1)
                child2 = self.mutation(child2)
                
                new_population.append(child1)
                if len(new_population) < self.population_size:
                    new_population.append(child2)
            
            # 更新种群
            self.population = new_population
        
        # 最终评估
        self.evaluate_fitness(hot_numbers)
        
        print(f"✅ 进化完成")
        print(f"   最佳适应度: {self.best_chromosome.fitness:.4f}")
        print(f"   最佳组合: {self.best_chromosome}")
        
        return self.population
    
    def get_best_solutions(self, top_k: int = 5) -> List[Chromosome]:
        """获取最佳解决方案"""
        # 确保种群已评估
        if not self.population or self.population[0].fitness == 0:
            self.evaluate_fitness()
        
        # 按适应度排序
        sorted_population = sorted(self.population, key=lambda x: x.fitness, reverse=True)
        
        # 去重
        unique_solutions = []
        seen = set()
        
        for chrom in sorted_population:
            key = (tuple(chrom.front_numbers), tuple(chrom.back_numbers))
            if key not in seen:
                seen.add(key)
                unique_solutions.append(chrom)
        
        return unique_solutions[:top_k]
    
    def optimize_with_probabilities(self, front_probs: np.ndarray, back_probs: np.ndarray, 
                                  top_k: int = 5) -> List[Dict[str, Any]]:
        """基于概率分布进行优化"""
        print(f"🎯 基于概率分布进行遗传算法优化...")
        
        # 定义基于概率的适应度函数
        def probability_fitness(chromosome: Chromosome) -> float:
            fitness = 0.0
            
            # 前区概率得分
            front_prob_score = np.mean([front_probs[num-1] for num in chromosome.front_numbers])
            
            # 后区概率得分
            back_prob_score = np.mean([back_probs[num-1] for num in chromosome.back_numbers])
            
            # 组合得分
            fitness = front_prob_score * 0.7 + back_prob_score * 0.3
            
            # 添加多样性奖励（避免过于集中）
            front_spread = max(chromosome.front_numbers) - min(chromosome.front_numbers)
            spread_bonus = min(front_spread / 30, 0.2)  # 最多20%奖励
            
            fitness += spread_bonus
            
            return fitness
        
        # 设置适应度函数
        self.set_fitness_function(probability_fitness)
        
        # 执行进化
        self.evolve()
        
        # 获取最佳解决方案
        best_solutions = self.get_best_solutions(top_k)
        
        # 转换为字典格式
        results = []
        for i, chrom in enumerate(best_solutions, 1):
            results.append({
                'rank': i,
                'front_numbers': chrom.front_numbers,
                'back_numbers': chrom.back_numbers,
                'confidence': chrom.fitness,
                'front_confidence': np.mean([front_probs[num-1] for num in chrom.front_numbers]),
                'back_confidence': np.mean([back_probs[num-1] for num in chrom.back_numbers]),
                'optimization_method': '遗传算法'
            })
        
        print(f"✅ 遗传算法优化完成: 生成 {len(results)} 个优化组合")
        
        return results


if __name__ == "__main__":
    print("🔬 DLT遗传算法优化器测试")
    print("=" * 60)
    
    # 创建优化器
    optimizer = DLTGeneticOptimizer(
        population_size=50,
        generations=20,
        crossover_rate=0.8,
        mutation_rate=0.2,
        elite_size=5
    )
    
    # 模拟概率分布
    np.random.seed(42)
    front_probs = np.random.rand(35)
    front_probs = front_probs / front_probs.sum()
    
    back_probs = np.random.rand(12)
    back_probs = back_probs / back_probs.sum()
    
    # 执行优化
    results = optimizer.optimize_with_probabilities(front_probs, back_probs, top_k=3)
    
    print(f"\\n🏆 优化结果:")
    for result in results:
        print(f"   第{result['rank']}组 (置信度: {result['confidence']:.4f}):")
        print(f"       前区: {result['front_numbers']}")
        print(f"       后区: {result['back_numbers']}")
    
    print(f"\\n📈 进化过程统计:")
    print(f"   最终平均适应度: {optimizer.fitness_history[-1]:.4f}")
    print(f"   最佳适应度: {optimizer.best_chromosome.fitness:.4f}")
    
    print(f"\\n🎯 第三阶段优化完成: 遗传算法优化器集成成功")
