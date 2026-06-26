#!/usr/bin/env python3
"""
全局优化器 - Global Optimizer

核心思想：
统一优化整个记忆系统，实现全局最优化。

数学基础：
目标函数：J = α·H(X) + β·T_access + γ·C_complexity

其中：
- H(X) = -∑p(x)log₂p(x) - 系统熵（信息不确定性）
- T_access - 访问延迟（O(1) ~ O(log N)）
- C_complexity - 算法复杂度（Grover O(√N), Dijkstra O(E log V)）

优化策略：
1. 自适应权重调整（α, β, γ 根据系统状态动态调整）
2. 多目标优化（Pareto 最优）
3. 实时监控（J 值实时计算）
4. 反馈控制（根据 J 值调整系统参数）

应用：
- 全局优化
- 自适应调整
- 实时监控
- 反馈控制
"""
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import math
import time
from collections import deque


class OptimizationGoal(Enum):
    """优化目标"""
    MINIMIZE_ENTROPY = "minimize_entropy"  # 最小化熵
    MINIMIZE_ACCESS_TIME = "minimize_access_time"  # 最小化访问时间
    MINIMIZE_COMPLEXITY = "minimize_complexity"  # 最小化复杂度
    BALANCE = "balance"  # 平衡优化


@dataclass
class SystemMetrics:
    """系统指标"""
    entropy: float  # 系统熵 H(X)
    access_time: float  # 访问延迟 T_access
    complexity: float  # 算法复杂度 C_complexity
    node_count: int  # 节点数量
    edge_count: int  # 边数量
    memory_usage: float  # 内存使用
    timestamp: float  # 时间戳


@dataclass
class OptimizationResult:
    """优化结果"""
    objective_value: float  # 目标函数值 J
    weights: Dict[str, float]  # 权重 {alpha, beta, gamma}
    metrics: SystemMetrics  # 系统指标
    improvements: Dict[str, float]  # 改进幅度
    recommendations: List[str]  # 优化建议


@dataclass
class AdaptiveWeights:
    """自适应权重"""
    alpha: float = 0.3  # 熵权重
    beta: float = 0.4  # 访问延迟权重
    gamma: float = 0.3  # 复杂度权重
    
    # 自适应参数
    learning_rate: float = 0.01  # 学习率
    momentum: float = 0.9  # 动量
    history: List[Dict[str, float]] = field(default_factory=list)  # 历史权重
    
    def update(self, entropy_trend: float, access_trend: float,
               complexity_trend: float):
        """
        更新自适应权重
        
        参数：
        - entropy_trend: 熵变化趋势（正表示增加）
        - access_trend: 访问延迟变化趋势
        - complexity_trend: 复杂度变化趋势
        """
        # 如果熵增加，增加熵权重（更多优化熵）
        if entropy_trend > 0:
            self.alpha += self.learning_rate
        else:
            self.alpha -= self.learning_rate * 0.5
        
        # 如果访问延迟增加，增加访问延迟权重
        if access_trend > 0:
            self.beta += self.learning_rate
        else:
            self.beta -= self.learning_rate * 0.5
        
        # 如果复杂度增加，增加复杂度权重
        if complexity_trend > 0:
            self.gamma += self.learning_rate
        else:
            self.gamma -= self.learning_rate * 0.5
        
        # 归一化权重
        total = self.alpha + self.beta + self.gamma
        self.alpha /= total
        self.beta /= total
        self.gamma /= total
        
        # 记录历史
        self.history.append({
            "alpha": self.alpha,
            "beta": self.beta,
            "gamma": self.gamma
        })
        
        # 保持历史长度
        if len(self.history) > 100:
            self.history.pop(0)


class ObjectiveFunction:
    """
    目标函数
    
    J = α·H(X) + β·T_access + γ·C_complexity
    """
    
    def __init__(self, alpha: float = 0.3, beta: float = 0.4, gamma: float = 0.3):
        """
        初始化目标函数
        
        参数：
        - alpha: 熵权重
        - beta: 访问延迟权重
        - gamma: 复杂度权重
        """
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        
        # 归一化权重
        total = alpha + beta + gamma
        self.alpha /= total
        self.beta /= total
        self.gamma /= total
    
    def calculate(self, metrics: SystemMetrics) -> float:
        """
        计算目标函数值
        
        J = α·H(X) + β·T_access + γ·C_complexity
        """
        # 归一化各项（避免量纲差异）
        normalized_entropy = metrics.entropy / (math.log2(metrics.node_count + 1) + 1e-10)
        normalized_access = metrics.access_time / 1000.0  # 假设最大 1000ms
        normalized_complexity = metrics.complexity / (metrics.node_count ** 2 + 1e-10)
        
        # 计算目标函数
        J = (self.alpha * normalized_entropy +
             self.beta * normalized_access +
             self.gamma * normalized_complexity)
        
        return J
    
    def gradient(self, metrics: SystemMetrics) -> np.ndarray:
        """
        计算梯度（用于优化）
        """
        # 归一化各项
        normalized_entropy = metrics.entropy / (math.log2(metrics.node_count + 1) + 1e-10)
        normalized_access = metrics.access_time / 1000.0
        normalized_complexity = metrics.complexity / (metrics.node_count ** 2 + 1e-10)
        
        # 梯度
        gradient = np.array([
            normalized_entropy,  # ∂J/∂α
            normalized_access,   # ∂J/∂β
            normalized_complexity  # ∂J/∂γ
        ])
        
        return gradient
    
    def update_weights(self, gradient: np.ndarray, learning_rate: float = 0.01):
        """
        梯度下降更新权重
        """
        weights = np.array([self.alpha, self.beta, self.gamma])
        weights -= learning_rate * gradient
        
        # 归一化
        weights = np.clip(weights, 0.01, 0.99)
        weights /= np.sum(weights)
        
        self.alpha, self.beta, self.gamma = weights


class SystemMonitor:
    """
    系统监控器
    
    实时监控系统状态
    """
    
    def __init__(self, window_size: int = 100):
        """
        初始化系统监控器
        
        参数：
        - window_size: 滑动窗口大小
        """
        self.window_size = window_size
        self.metrics_history: deque = deque(maxlen=window_size)
        self.baseline_metrics: Optional[SystemMetrics] = None
    
    def record_metrics(self, metrics: SystemMetrics):
        """记录系统指标"""
        self.metrics_history.append(metrics)
        
        # 设置基线（第一次记录）
        if self.baseline_metrics is None:
            self.baseline_metrics = metrics
    
    def get_trends(self) -> Dict[str, float]:
        """
        获取指标变化趋势
        
        返回：
        - entropy_trend: 熵变化趋势
        - access_trend: 访问延迟变化趋势
        - complexity_trend: 复杂度变化趋势
        """
        if len(self.metrics_history) < 2:
            return {
                "entropy_trend": 0.0,
                "access_trend": 0.0,
                "complexity_trend": 0.0
            }
        
        # 计算最近趋势（最近 10 次）
        recent_metrics = list(self.metrics_history)[-10:]
        
        entropy_trend = (recent_metrics[-1].entropy - recent_metrics[0].entropy)
        access_trend = (recent_metrics[-1].access_time - recent_metrics[0].access_time)
        complexity_trend = (recent_metrics[-1].complexity - recent_metrics[0].complexity)
        
        return {
            "entropy_trend": entropy_trend,
            "access_trend": access_trend,
            "complexity_trend": complexity_trend
        }
    
    def detect_anomalies(self, threshold: float = 3.0) -> List[str]:
        """
        检测异常
        
        参数：
        - threshold: 异常阈值（标准差倍数）
        
        返回：
        - 异常列表
        """
        if len(self.metrics_history) < 10:
            return []
        
        anomalies = []
        
        # 计算统计量
        entropies = [m.entropy for m in self.metrics_history]
        access_times = [m.access_time for m in self.metrics_history]
        complexities = [m.complexity for m in self.metrics_history]
        
        entropy_mean = np.mean(entropies)
        entropy_std = np.std(entropies)
        access_mean = np.mean(access_times)
        access_std = np.std(access_times)
        complexity_mean = np.mean(complexities)
        complexity_std = np.std(complexities)
        
        latest = self.metrics_history[-1]
        
        # 检测异常
        if abs(latest.entropy - entropy_mean) > threshold * entropy_std:
            anomalies.append(f"熵异常: {latest.entropy:.4f} (均值: {entropy_mean:.4f})")
        
        if abs(latest.access_time - access_mean) > threshold * access_std:
            anomalies.append(f"访问延迟异常: {latest.access_time:.4f}ms (均值: {access_mean:.4f}ms)")
        
        if abs(latest.complexity - complexity_mean) > threshold * complexity_std:
            anomalies.append(f"复杂度异常: {latest.complexity:.4f} (均值: {complexity_mean:.4f})")
        
        return anomalies


class FeedbackController:
    """
    反馈控制器
    
    根据目标函数值调整系统参数
    """
    
    def __init__(self, kp: float = 0.5, ki: float = 0.1, kd: float = 0.2):
        """
        PID 控制器
        
        参数：
        - kp: 比例系数
        - ki: 积分系数
        - kd: 微分系数
        """
        self.kp = kp
        self.ki = ki
        self.kd = kd
        
        # PID 状态
        self.integral = 0.0
        self.previous_error = 0.0
    
    def control(self, setpoint: float, current_value: float) -> float:
        """
        PID 控制
        
        参数：
        - setpoint: 目标值
        - current_value: 当前值
        
        返回：
        - 控制输出
        """
        error = setpoint - current_value
        
        # PID 计算
        p = self.kp * error
        self.integral += error
        i = self.ki * self.integral
        d = self.kd * (error - self.previous_error)
        
        self.previous_error = error
        
        output = p + i + d
        
        return output
    
    def reset(self):
        """重置控制器"""
        self.integral = 0.0
        self.previous_error = 0.0


class GlobalOptimizer:
    """
    全局优化器
    
    统一优化整个记忆系统
    """
    
    def __init__(self, goal: OptimizationGoal = OptimizationGoal.BALANCE):
        """
        初始化全局优化器
        
        参数：
        - goal: 优化目标
        """
        self.goal = goal
        
        # 自适应权重
        self.adaptive_weights = AdaptiveWeights()
        
        # 目标函数
        self.objective_function = ObjectiveFunction(
            alpha=self.adaptive_weights.alpha,
            beta=self.adaptive_weights.beta,
            gamma=self.adaptive_weights.gamma
        )
        
        # 系统监控
        self.monitor = SystemMonitor(window_size=100)
        
        # 反馈控制
        self.controller = FeedbackController()
        
        # 优化历史
        self.optimization_history: List[OptimizationResult] = []
        
        # 目标值（根据优化目标设置）
        self.setpoint = self._get_setpoint()
    
    def _get_setpoint(self) -> float:
        """获取目标值"""
        if self.goal == OptimizationGoal.MINIMIZE_ENTROPY:
            return 0.0  # 熵最小化
        elif self.goal == OptimizationGoal.MINIMIZE_ACCESS_TIME:
            return 0.0  # 访问延迟最小化
        elif self.goal == OptimizationGoal.MINIMIZE_COMPLEXITY:
            return 0.0  # 复杂度最小化
        else:  # BALANCE
            return 0.3  # 平衡优化
    
    def optimize(self, metrics: SystemMetrics,
                 spiderweb_graph: Optional[Any] = None) -> OptimizationResult:
        """
        执行优化
        
        参数：
        - metrics: 系统指标
        - spiderweb_graph: 蜘蛛网图（可选，用于获取更多指标）
        
        返回：
        - 优化结果
        """
        # 记录指标
        self.monitor.record_metrics(metrics)
        
        # 获取趋势
        trends = self.monitor.get_trends()
        
        # 更新自适应权重
        self.adaptive_weights.update(
            entropy_trend=trends["entropy_trend"],
            access_trend=trends["access_trend"],
            complexity_trend=trends["complexity_trend"]
        )
        
        # 更新目标函数权重
        self.objective_function.alpha = self.adaptive_weights.alpha
        self.objective_function.beta = self.adaptive_weights.beta
        self.objective_function.gamma = self.adaptive_weights.gamma
        
        # 计算目标函数值
        objective_value = self.objective_function.calculate(metrics)
        
        # 梯度下降优化权重
        gradient = self.objective_function.gradient(metrics)
        self.objective_function.update_weights(gradient)
        
        # 生成优化建议
        recommendations = self._generate_recommendations(metrics, trends)
        
        # 计算改进幅度
        improvements = self._calculate_improvements(metrics)
        
        # 创建优化结果
        result = OptimizationResult(
            objective_value=objective_value,
            weights={
                "alpha": self.adaptive_weights.alpha,
                "beta": self.adaptive_weights.beta,
                "gamma": self.adaptive_weights.gamma
            },
            metrics=metrics,
            improvements=improvements,
            recommendations=recommendations
        )
        
        # 记录优化历史
        self.optimization_history.append(result)
        
        return result
    
    def _generate_recommendations(self, metrics: SystemMetrics,
                                  trends: Dict[str, float]) -> List[str]:
        """生成优化建议"""
        recommendations = []
        
        # 熵建议
        if trends["entropy_trend"] > 0.01:
            recommendations.append("系统熵增加，建议增强熵减机制（降低低价值节点权重）")
        elif trends["entropy_trend"] < -0.01:
            recommendations.append("系统熵减少，熵减机制运行良好")
        
        # 访问延迟建议
        if trends["access_trend"] > 1.0:  # 1ms
            recommendations.append("访问延迟增加，建议优化 Hot RAM Layer（提升缓存命中率）")
        elif trends["access_trend"] < -1.0:
            recommendations.append("访问延迟减少，访问层性能良好")
        
        # 复杂度建议
        if trends["complexity_trend"] > 0.1:
            recommendations.append("复杂度增加，建议优化算法（使用 Grover 搜索替代线性搜索）")
        elif trends["complexity_trend"] < -0.1:
            recommendations.append("复杂度降低，算法优化有效")
        
        # 节点数量建议
        if metrics.node_count > 10000:
            recommendations.append("节点数量较多，建议归档低价值节点到 Cold Layer")
        
        # 内存使用建议
        if metrics.memory_usage > 0.8:  # 80%
            recommendations.append("内存使用率高，建议清理低价值节点或增加熵减频率")
        
        return recommendations
    
    def _calculate_improvements(self, metrics: SystemMetrics) -> Dict[str, float]:
        """计算改进幅度"""
        if len(self.monitor.metrics_history) < 2:
            return {}
        
        previous_metrics = self.monitor.metrics_history[-2]
        
        improvements = {
            "entropy_improvement": previous_metrics.entropy - metrics.entropy,
            "access_time_improvement": previous_metrics.access_time - metrics.access_time,
            "complexity_improvement": previous_metrics.complexity - metrics.complexity
        }
        
        return improvements
    
    def get_optimization_summary(self) -> Dict[str, Any]:
        """
        获取优化摘要
        
        返回：
        - 优化摘要信息
        """
        if not self.optimization_history:
            return {}
        
        latest = self.optimization_history[-1]
        
        # 计算 J 值趋势
        j_values = [r.objective_value for r in self.optimization_history]
        j_trend = j_values[-1] - j_values[0] if len(j_values) > 1 else 0.0
        
        return {
            "latest_objective_value": latest.objective_value,
            "j_value_trend": j_trend,
            "current_weights": latest.weights,
            "current_metrics": {
                "entropy": latest.metrics.entropy,
                "access_time": latest.metrics.access_time,
                "complexity": latest.metrics.complexity
            },
            "recommendations": latest.recommendations,
            "optimization_count": len(self.optimization_history)
        }


def create_global_optimizer(goal: str = "balance") -> GlobalOptimizer:
    """
    创建全局优化器
    
    参数：
    - goal: 优化目标（"minimize_entropy", "minimize_access_time", 
             "minimize_complexity", "balance"）
    
    返回：
    - 全局优化器实例
    """
    goal_mapping = {
        "minimize_entropy": OptimizationGoal.MINIMIZE_ENTROPY,
        "minimize_access_time": OptimizationGoal.MINIMIZE_ACCESS_TIME,
        "minimize_complexity": OptimizationGoal.MINIMIZE_COMPLEXITY,
        "balance": OptimizationGoal.BALANCE
    }
    
    opt_goal = goal_mapping.get(goal, OptimizationGoal.BALANCE)
    
    return GlobalOptimizer(goal=opt_goal)


if __name__ == "__main__":
    # 测试全局优化器
    print("=" * 60)
    print("全局优化器测试")
    print("=" * 60)
    
    # 创建优化器
    optimizer = create_global_optimizer(goal="balance")
    
    # 模拟系统指标
    for i in range(10):
        metrics = SystemMetrics(
            entropy=2.5 - i * 0.05,  # 熵逐渐降低
            access_time=50.0 - i * 2.0,  # 访问延迟逐渐降低
            complexity=100.0 - i * 5.0,  # 复杂度逐渐降低
            node_count=1000 + i * 10,
            edge_count=2000 + i * 20,
            memory_usage=0.5 + i * 0.01,
            timestamp=time.time()
        )
        
        result = optimizer.optimize(metrics)
        
        print(f"\n优化迭代 {i + 1}:")
        print(f"  目标函数值 J: {result.objective_value:.4f}")
        print(f"  权重: α={result.weights['alpha']:.3f}, "
              f"β={result.weights['beta']:.3f}, "
              f"γ={result.weights['gamma']:.3f}")
        print(f"  系统熵: {result.metrics.entropy:.4f}")
        print(f"  访问延迟: {result.metrics.access_time:.4f}ms")
        print(f"  复杂度: {result.metrics.complexity:.4f}")
        print(f"  优化建议: {', '.join(result.recommendations[:2])}")
    
    # 获取优化摘要
    summary = optimizer.get_optimization_summary()
    print("\n" + "=" * 60)
    print("优化摘要:")
    print("=" * 60)
    print(f"最新 J 值: {summary['latest_objective_value']:.4f}")
    print(f"J 值趋势: {summary['j_value_trend']:.4f}")
    print(f"当前权重: α={summary['current_weights']['alpha']:.3f}, "
          f"β={summary['current_weights']['beta']:.3f}, "
          f"γ={summary['current_weights']['gamma']:.3f}")
    print(f"优化次数: {summary['optimization_count']}")
    
    print("\n" + "=" * 60)
    print("全局优化器测试完成")
    print("=" * 60)
