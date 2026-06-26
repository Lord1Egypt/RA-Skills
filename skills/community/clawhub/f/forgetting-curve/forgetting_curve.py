#!/usr/bin/env python3
"""
Forgetting Curve 模块 - Ebbinghaus 遗忘曲线实现

提供标准化的记忆衰减计算和间隔重复调度功能。
"""

import math
from dataclasses import dataclass
from typing import Optional, Callable
from datetime import datetime, timedelta


@dataclass
class ForgettingCurveConfig:
    """遗忘曲线配置"""
    half_life_days: float = 30.0
    initial_strength: float = 1.0
    minimum_strength: float = 0.1
    decay_function: Optional[Callable[[float, float], float]] = None


class ForgettingCurve:
    """Ebbinghaus 遗忘曲线"""
    
    def __init__(self, config: Optional[ForgettingCurveConfig] = None):
        self.config = config or ForgettingCurveConfig()
        
        # 默认衰减函数：指数衰减
        if self.config.decay_function is None:
            self.config.decay_function = self._default_decay
    
    def _default_decay(self, age_days: float, strength: float) -> float:
        """默认指数衰减函数
        
        Args:
            age_days: 距离最后一次复习的天数
            strength: 当前记忆强度
            
        Returns:
            衰减后的强度
        """
        if age_days <= 0:
            return strength
        
        decay_factor = math.pow(2, -age_days / self.config.half_life_days)
        return strength * decay_factor
    
    def calculate_decay(self, age_days: float) -> float:
        """计算衰减因子（不依赖当前强度）
        
        Args:
            age_days: 距离最后一次复习的天数
            
        Returns:
            衰减因子 (0.0-1.0)
        """
        if age_days <= 0:
            return 1.0
        
        if self.config.decay_function is not None:
            # 使用自定义衰减函数（假设强度为1.0）
            return self.config.decay_function(age_days, 1.0)
        
        # 默认指数衰减
        return math.pow(2, -age_days / self.config.half_life_days)
    
    def apply_decay(self, strength: float, age_days: float) -> float:
        """应用衰减到记忆强度
        
        Args:
            strength: 当前记忆强度 (0.0-1.0)
            age_days: 距离最后一次复习的天数
            
        Returns:
            衰减后的强度
        """
        if strength <= self.config.minimum_strength:
            return self.config.minimum_strength
        
        if self.config.decay_function is not None:
            return self.config.decay_function(age_days, strength)
        
        # 使用默认衰减
        decay_factor = self.calculate_decay(age_days)
        decayed = strength * decay_factor
        
        # 确保不低于最小强度
        return max(decayed, self.config.minimum_strength)
    
    def age_from_decay(self, decay_factor: float) -> float:
        """从衰减因子反推天数
        
        Args:
            decay_factor: 衰减因子 (0.0-1.0)
            
        Returns:
            达到该衰减所需的天数
        """
        if decay_factor <= 0 or decay_factor >= 1:
            return 0.0
        
        # 从 decay = 2^(-age/half_life) 推导
        # age = -half_life * log2(decay)
        return -self.config.half_life_days * math.log2(decay_factor)
    
    def strength_after_time(self, initial_strength: float, age_days: float) -> float:
        """计算经过指定时间后的记忆强度
        
        Args:
            initial_strength: 初始强度
            age_days: 经过的天数
            
        Returns:
            衰减后的强度
        """
        return self.apply_decay(initial_strength, age_days)
    
    def time_to_threshold(self, current_strength: float, threshold: float = None) -> float:
        """计算记忆强度衰减到阈值所需的时间
        
        Args:
            current_strength: 当前强度
            threshold: 阈值（默认使用 minimum_strength）
            
        Returns:
            达到阈值所需的天数
        """
        if threshold is None:
            threshold = self.config.minimum_strength
        
        if current_strength <= threshold:
            return 0.0
        
        # 计算衰减因子：threshold / current_strength
        decay_needed = threshold / current_strength
        return self.age_from_decay(decay_needed)


class SpacedRepetitionScheduler:
    """间隔重复调度器"""
    
    def __init__(self, base_interval: float = 1.0, strength_factor: float = 1.5):
        self.base_interval = base_interval  # 基础间隔（天）
        self.strength_factor = strength_factor  # 强度因子
        
        # 难度因子
        self.easy_factor = 1.3
        self.normal_factor = 1.0
        self.hard_factor = 0.8
    
    def next_review_interval(self, current_strength: float, difficulty: str = "normal") -> float:
        """计算下一次复习间隔
        
        Args:
            current_strength: 当前记忆强度 (0.0-1.0)
            difficulty: 难度 ("easy", "normal", "hard")
            
        Returns:
            下一次复习间隔（天）
        """
        # 基础公式：interval = base * (strength ^ factor)
        factor = {
            "easy": self.easy_factor,
            "normal": self.normal_factor,
            "hard": self.hard_factor
        }.get(difficulty, self.normal_factor)
        
        # 确保强度在合理范围内
        clamped_strength = max(0.1, min(0.99, current_strength))
        
        interval = self.base_interval * (math.pow(clamped_strength, factor))
        
        # 最小间隔为0.1天
        return max(0.1, interval)
    
    def update_strength(self, current_strength: float, success: bool, 
                        difficulty: str = "normal") -> float:
        """更新记忆强度（复习后）
        
        Args:
            current_strength: 当前强度
            success: 是否成功回忆
            difficulty: 难度
            
        Returns:
            更新后的强度
        """
        if not success:
            # 回忆失败，重置为较低强度
            return max(0.2, current_strength * 0.5)
        
        # 根据难度调整强度增量
        difficulty_factor = {
            "easy": 1.2,
            "normal": 1.0,
            "hard": 0.8
        }.get(difficulty, 1.0)
        
        # 基础增量（成功回忆增加强度）
        base_increment = 0.15 * difficulty_factor
        
        # 当前强度越高，增量越小
        strength_factor = 1.0 - (current_strength * 0.5)
        
        new_strength = current_strength + (base_increment * strength_factor)
        
        # 限制在合理范围内
        return min(0.99, max(0.1, new_strength))


def batch_decay(memories, half_life_days: float = 30.0):
    """批量计算衰减
    
    Args:
        memories: 记忆列表，每个元素需包含 'strength' 和 'age_days' 字段
        half_life_days: 半衰期
        
    Returns:
        包含 'decayed_strength' 的新列表
    """
    curve = ForgettingCurve(ForgettingCurveConfig(half_life_days=half_life_days))
    
    results = []
    for mem in memories:
        decayed = curve.apply_decay(mem.get('strength', 0.5), mem.get('age_days', 0))
        
        # 创建新字典，保留原字段
        new_mem = dict(mem)
        new_mem['decayed_strength'] = decayed
        results.append(new_mem)
    
    return results


# 便捷函数
def create_standard_curve(half_life_days: float = 30.0) -> ForgettingCurve:
    """创建标准遗忘曲线"""
    return ForgettingCurve(ForgettingCurveConfig(half_life_days=half_life_days))


def create_short_term_curve() -> ForgettingCurve:
    """创建短期记忆曲线（3天半衰期）"""
    return create_standard_curve(3.0)


def create_long_term_curve() -> ForgettingCurve:
    """创建长期记忆曲线（90天半衰期）"""
    return create_standard_curve(90.0)


# 测试代码
if __name__ == "__main__":
    print("🧪 Forgetting Curve 模块测试")
    print("=" * 40)
    
    # 测试基本衰减
    curve = create_standard_curve(30.0)
    
    test_cases = [
        (0.9, 7),   # 7天前记忆，强度0.9
        (0.7, 15),  # 15天前
        (0.5, 30),  # 30天前
        (0.3, 60),  # 60天前
    ]
    
    print("衰减计算:")
    for strength, age in test_cases:
        decayed = curve.apply_decay(strength, age)
        decay_factor = curve.calculate_decay(age)
        print(f"  强度 {strength:.2f}, {age}天 → 衰减因子 {decay_factor:.3f}, 最终强度 {decayed:.3f}")
    
    print()
    
    # 测试间隔重复
    scheduler = SpacedRepetitionScheduler()
    strengths = [0.3, 0.5, 0.7, 0.9]
    
    print("间隔重复调度:")
    for strength in strengths:
        interval = scheduler.next_review_interval(strength)
        print(f"  强度 {strength:.2f} → 下次复习间隔: {interval:.1f} 天")
    
    print()
    print("✅ 测试完成")