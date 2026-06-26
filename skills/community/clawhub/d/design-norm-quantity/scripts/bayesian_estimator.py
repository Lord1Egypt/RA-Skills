# -*- coding: utf-8 -*-
"""
度量衡智库 · 贝叶斯概率估算模块 v1.0
Bayesian Probability Estimation for Construction Cost
=====================================================

贝叶斯概率估算的核心优势：
1. 输出概率分布而非单点估计
2. 自然量化不确定性
3. 支持先验知识融合
4. 可迭代更新

整合的算法：
1. 贝叶斯线性回归 - 不确定性传播
2. 蒙特卡洛+贝叶斯融合 - 双重不确定性量化
3. 贝叶斯网络 - 多因素因果推理

来源:
- ASCE/JCEM 2020 "Bayesian Monte Carlo Simulation-Driver Approach"
- MDPI/IJERPH 2019 "Combining Monte Carlo Simulation and Bayesian Networks"
- ResearchGate "Risk Consideration and Cost Estimation in Construction"

作者：度量衡智库
版本：1.0.0
日期：2026-04-04
"""

import json
import math
import random
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict
from collections import defaultdict
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================
# 概率分布定义
# ============================================================

@dataclass
class ProbabilityDistribution:
    """概率分布"""
    name: str
    mean: float
    std: float
    min_val: float = 0
    max_val: float = 0
    
    def sample(self, n: int = 1) -> List[float]:
        """从分布中采样"""
        if self.name == "normal":
            return [random.gauss(self.mean, self.std) for _ in range(n)]
        elif self.name == "uniform":
            return [random.uniform(self.min_val, self.max_val) for _ in range(n)]
        elif self.name == "triangular":
            return [random.triangular(self.min_val, self.max_val, self.mean) for _ in range(n)]
        elif self.name == "lognormal":
            # 对数正态分布
            sigma = math.sqrt(math.log(1 + (self.std / self.mean) ** 2))
            mu = math.log(self.mean) - sigma ** 2 / 2
            return [random.lognormvariate(mu, sigma) for _ in range(n)]
        else:
            return [self.mean] * n


@dataclass
class CostFactor:
    """成本因子"""
    name: str
    distribution: ProbabilityDistribution
    weight: float  # 在总造价中的权重
    correlation_group: Optional[str] = None  # 相关性分组


# ============================================================
# 贝叶斯线性回归估算器
# ============================================================

class BayesianLinearRegressor:
    """
    贝叶斯线性回归估算器
    
    特点:
    - 输出预测区间而非单点估计
    - 自动计算不确定性
    - 可融合专家先验知识
    """
    
    def __init__(self, alpha_prior=1.0, beta_prior=1.0):
        self.alpha_prior = alpha_prior
        self.beta_prior = beta_prior
        self.alpha_posterior = alpha_prior
        self.beta_posterior = beta_prior
        self.mean_posterior = 0
        self.coefficients = []
        self.is_fitted = False
    
    def _normal_inverse_gamma_prior(self, X: List[List[float]], y: List[float]):
        """计算后验参数"""
        n = len(y)
        if n < 2:
            return
        
        x_mean = [sum(col) / n for col in zip(*X)]
        y_mean = sum(y) / n
        
        numerator = sum((X[i][0] - x_mean[0]) * (y[i] - y_mean) for i in range(n))
        denominator = sum((X[i][0] - x_mean[0]) ** 2 for i in range(n))
        
        if denominator > 0:
            slope = numerator / denominator
            intercept = y_mean - slope * x_mean[0]
            self.coefficients = [intercept, slope]
            
            residuals = [y[i] - (intercept + slope * X[i][0]) for i in range(n)]
            variance = sum(r ** 2 for r in residuals) / (n - 2) if n > 2 else self.beta_prior
            
            self.alpha_posterior = self.alpha_prior + n / 2
            self.beta_posterior = self.beta_prior + variance * n / 2
        
        self.is_fitted = True
    
    def fit(self, X: List[List[float]], y: List[float]):
        """训练"""
        logger.info(f"Training Bayesian Linear Regression with {len(X)} samples")
        self._normal_inverse_gamma_prior(X, y)
        logger.info("Bayesian LR training completed")
    
    def predict(self, X: List[List[float]]) -> Dict:
        """预测并返回概率分布"""
        if not self.is_fitted or not self.coefficients:
            return {
                "mean": sum(X[i][0] * 5000 for i in range(len(X))) / len(X) if X else 5000,
                "std": 500,
                "ci_90": [4000, 6000],
                "ci_95": [3800, 6200],
                "method": "Bayesian Linear Regression (Prior)"
            }
        
        predictions = []
        for x in X:
            pred = self.coefficients[0] + sum(c * xi for c, xi in zip(self.coefficients[1:], x))
            predictions.append(pred)
        
        mean_pred = sum(predictions) / len(predictions)
        std_pred = math.sqrt(self.beta_posterior / self.alpha_posterior)
        
        return {
            "mean": round(mean_pred, 2),
            "std": round(std_pred, 2),
            "ci_90": [round(mean_pred - 1.645 * std_pred, 2), round(mean_pred + 1.645 * std_pred, 2)],
            "ci_95": [round(mean_pred - 1.96 * std_pred, 2), round(mean_pred + 1.96 * std_pred, 2)],
            "coefficients": self.coefficients,
            "method": "Bayesian Linear Regression"
        }


# ============================================================
# 贝叶斯网络估算器
# ============================================================

class BayesianNetworkEstimator:
    """
    贝叶斯网络估算器
    
    特点:
    - 建模多因素因果关系
    - 条件概率推理
    - 因素影响力分析
    """
    
    def __init__(self):
        self.nodes = {
            "structure": {
                "parents": [],
                "states": ["框架", "框架-剪力墙", "框架-核心筒", "钢结构"],
                "cpt": {}
            },
            "height": {
                "parents": ["structure"],
                "states": ["低层", "多层", "高层", "超高层"],
                "cpt": {}
            },
            "decoration": {
                "parents": [],
                "states": ["普装", "精装", "高档"],
                "cpt": {}
            },
            "region": {
                "parents": [],
                "states": ["一线", "二线", "三线"],
                "cpt": {}
            },
            "unit_cost": {
                "parents": ["structure", "height", "decoration", "region"],
                "states": [],
                "distribution": {}
            }
        }
        
        self._init_cpt()
    
    def _init_cpt(self):
        """初始化条件概率表"""
        self.nodes["height"]["cpt"]["structure"] = {
            "框架": {"低层": 0.4, "多层": 0.4, "高层": 0.15, "超高层": 0.05},
            "框架-剪力墙": {"低层": 0.1, "多层": 0.3, "高层": 0.5, "超高层": 0.1},
            "框架-核心筒": {"低层": 0.02, "多层": 0.08, "高层": 0.4, "超高层": 0.5},
            "钢结构": {"低层": 0.2, "多层": 0.3, "高层": 0.35, "超高层": 0.15}
        }
        
        self.base_costs = {
            "框架": 4500,
            "框架-剪力墙": 5200,
            "框架-核心筒": 6500,
            "钢结构": 7000
        }
        
        self.height_factors = {
            "低层": 0.90,
            "多层": 1.00,
            "高层": 1.15,
            "超高层": 1.35
        }
        
        self.deco_factors = {
            "普装": 1.00,
            "精装": 1.20,
            "高档": 1.45
        }
        
        self.region_factors = {
            "一线": 1.15,
            "二线": 1.05,
            "三线": 0.95
        }
        
        self.uncertainty = {
            "structure": 0.08,
            "height": 0.05,
            "decoration": 0.06,
            "region": 0.10,
            "residual": 0.12
        }
    
    def _classify_height(self, floor_count: int) -> str:
        """根据层数分类高度"""
        if floor_count <= 7:
            return "低层"
        elif floor_count <= 18:
            return "多层"
        elif floor_count <= 40:
            return "高层"
        else:
            return "超高层"
    
    def _classify_region(self, region_factor: float) -> str:
        """根据地区系数分类"""
        if region_factor >= 1.10:
            return "一线"
        elif region_factor >= 1.03:
            return "二线"
        else:
            return "三线"
    
    def estimate(self, structure: str, floor_count: int, decoration: str, 
                 region_factor: float) -> Dict:
        """贝叶斯网络估算"""
        height_cat = self._classify_height(floor_count)
        region_cat = self._classify_region(region_factor)
        
        base = self.base_costs.get(structure, 5000)
        height_fac = self.height_factors.get(height_cat, 1.0)
        deco_fac = self.deco_factors.get(decoration, 1.0)
        region_fac = self.region_factors.get(region_cat, 1.0)
        
        mean_cost = base * height_fac * deco_fac * region_fac
        
        variance = 0
        variance += (self.uncertainty["structure"] * base) ** 2
        variance += (self.uncertainty["height"] * base * height_fac) ** 2
        variance += (self.uncertainty["decoration"] * base * deco_fac) ** 2
        variance += (self.uncertainty["region"] * mean_cost) ** 2
        variance += (self.uncertainty["residual"] * mean_cost) ** 2
        
        std_cost = math.sqrt(variance)
        
        return {
            "unit_cost": round(mean_cost, 2),
            "std": round(std_cost, 2),
            "ci_90": [round(mean_cost - 1.645 * std_cost, 2), round(mean_cost + 1.645 * std_cost, 2)],
            "ci_95": [round(mean_cost - 1.96 * std_cost, 2), round(mean_cost + 1.96 * std_cost, 2)],
            "factors": {
                "structure": {"type": structure, "base_cost": base, "contribution": base / mean_cost * 100},
                "height": {"category": height_cat, "factor": height_fac, "contribution": (height_fac - 1) * 100},
                "decoration": {"level": decoration, "factor": deco_fac, "contribution": (deco_fac - 1) * 100},
                "region": {"category": region_cat, "factor": region_fac, "contribution": (region_fac - 1) * 100}
            },
            "method": "Bayesian Network Estimation"
        }


# ============================================================
# 蒙特卡洛+贝叶斯融合估算器
# ============================================================

class BayesianMonteCarloEstimator:
    """
    蒙特卡洛+贝叶斯融合估算器
    
    双重不确定性量化:
    1. 蒙特卡洛模拟材料价格、市场波动
    2. 贝叶斯更新融合历史数据和专家判断
    """
    
    def __init__(self, n_simulations: int = 10000):
        self.n_simulations = n_simulations
        
        self.cost_factors = [
            CostFactor(
                name="钢筋",
                distribution=ProbabilityDistribution("lognormal", mean=4800, std=720),
                weight=0.15
            ),
            CostFactor(
                name="混凝土",
                distribution=ProbabilityDistribution("normal", mean=550, std=55),
                weight=0.12
            ),
            CostFactor(
                name="人工费",
                distribution=ProbabilityDistribution("triangular", mean=150, std=0, min_val=130, max_val=180),
                weight=0.25
            ),
            CostFactor(
                name="机械费",
                distribution=ProbabilityDistribution("uniform", mean=0, std=0, min_val=40, max_val=60),
                weight=0.08
            ),
            CostFactor(
                name="管理费",
                distribution=ProbabilityDistribution("normal", mean=80, std=8),
                weight=0.15
            ),
            CostFactor(
                name="利润",
                distribution=ProbabilityDistribution("normal", mean=70, std=10),
                weight=0.10
            ),
            CostFactor(
                name="税金",
                distribution=ProbabilityDistribution("normal", mean=90, std=5),
                weight=0.15
            )
        ]
        
        self.region_factor = 1.0
    
    def _bayesian_update(self, prior_mean: float, prior_std: float,
                        sample_data: List[float]) -> Tuple[float, float]:
        """贝叶斯更新"""
        n = len(sample_data)
        if n == 0:
            return prior_mean, prior_std
        
        sample_mean = sum(sample_data) / n
        sample_std = math.sqrt(sum((x - sample_mean) ** 2 for x in sample_data) / n) if n > 1 else prior_std
        
        posterior_mean = (n / (n + 1)) * sample_mean + (1 / (n + 1)) * prior_mean
        
        prior_var = prior_std ** 2
        sample_var = sample_std ** 2 if sample_std > 0 else prior_var
        posterior_var = 1 / (1 / prior_var + n / sample_var)
        posterior_std = math.sqrt(posterior_var)
        
        return posterior_mean, posterior_std
    
    def _monte_carlo_simulate(self, factor_samples: Dict[str, List[float]]) -> List[float]:
        """蒙特卡洛模拟"""
        total_costs = []
        n = len(list(factor_samples.values())[0])
        
        for i in range(n):
            total = 0
            for factor in self.cost_factors:
                if factor.name in factor_samples:
                    total += factor_samples[factor.name][i] * factor.weight
            total_costs.append(total)
        
        return total_costs
    
    def estimate(self, region_factor: float = 1.0,
                historical_data: Optional[List[float]] = None) -> Dict:
        """贝叶斯蒙特卡洛估算"""
        self.region_factor = region_factor
        
        factor_samples = {}
        for factor in self.cost_factors:
            if historical_data:
                posterior_mean, posterior_std = self._bayesian_update(
                    factor.distribution.mean,
                    factor.distribution.std,
                    historical_data
                )
                dist = ProbabilityDistribution(
                    factor.distribution.name,
                    posterior_mean,
                    posterior_std,
                    factor.distribution.min_val,
                    factor.distribution.max_val
                )
                factor_samples[factor.name] = dist.sample(self.n_simulations)
            else:
                factor_samples[factor.name] = factor.distribution.sample(self.n_simulations)
        
        total_costs = self._monte_carlo_simulate(factor_samples)
        total_costs.sort()
        
        p10_idx = int(self.n_simulations * 0.10)
        p50_idx = int(self.n_simulations * 0.50)
        p90_idx = int(self.n_simulations * 0.90)
        
        mean_cost = sum(total_costs) / len(total_costs)
        median_cost = total_costs[p50_idx]
        
        mean_cost *= region_factor
        median_cost *= region_factor
        p10_cost = total_costs[p10_idx] * region_factor
        p90_cost = total_costs[p90_idx] * region_factor
        
        std_cost = math.sqrt(sum((c - mean_cost) ** 2 for c in total_costs) / len(total_costs))
        precision_95 = 1.96 * std_cost / mean_cost * 100
        
        factor_contributions = {}
        for factor in self.cost_factors:
            factor_contributions[factor.name] = {
                "weight": factor.weight,
                "base_value": factor.distribution.mean,
                "uncertainty": factor.distribution.std / factor.distribution.mean * 100 if factor.distribution.mean > 0 else 0,
                "contribution": factor.weight * 100
            }
        
        return {
            "unit_cost": {
                "mean": round(mean_cost, 2),
                "median": round(median_cost, 2),
                "p10": round(p10_cost, 2),
                "p50": round(total_costs[p50_idx] * region_factor, 2),
                "p90": round(p90_cost, 2)
            },
            "ci_95": [round(mean_cost - 1.96 * std_cost * region_factor, 2), 
                      round(mean_cost + 1.96 * std_cost * region_factor, 2)],
            "std": round(std_cost * region_factor, 2),
            "precision_95": round(precision_95, 1),
            "factor_contributions": factor_contributions,
            "method": "Bayesian Monte Carlo Fusion"
        }


# ============================================================
# 快速估算接口
# ============================================================

def bayesian_estimate(
    structure_type: str,
    floor_count: int,
    decoration_level: str,
    region_factor: float,
    total_area: float,
    method: str = "bayesian_mc"
) -> Dict:
    """贝叶斯快速估算接口"""
    if method == "bayesian_lr":
        estimator = BayesianLinearRegressor()
        X = [[floor_count / 10, region_factor, 1 if "核心筒" in structure_type else 0]]
        result = estimator.predict(X)
        result["unit_cost"] = result.pop("mean")
        result["method"] = "Bayesian Linear Regression"
        
    elif method == "bayesian_network":
        estimator = BayesianNetworkEstimator()
        result = estimator.estimate(structure_type, floor_count, decoration_level, region_factor)
        
    else:
        estimator = BayesianMonteCarloEstimator(n_simulations=10000)
        result = estimator.estimate(region_factor)
        
        structure_adjustments = {
            "框架": 1.0,
            "框架-剪力墙": 1.08,
            "框架-核心筒": 1.25,
            "剪力墙": 1.05,
            "钢结构": 1.35
        }
        adj = structure_adjustments.get(structure_type, 1.0)
        
        result["unit_cost"]["mean"] *= adj
        result["unit_cost"]["median"] *= adj
        result["unit_cost"]["p10"] *= adj
        result["unit_cost"]["p50"] *= adj
        result["unit_cost"]["p90"] *= adj
        result["ci_95"] = [x * adj for x in result["ci_95"]]
        result["std"] *= adj
        result["precision_95"] = round(result["std"] / result["unit_cost"]["mean"] * 100 * 1.96, 1)
    
    result["project_info"] = {
        "structure_type": structure_type,
        "floor_count": floor_count,
        "decoration_level": decoration_level,
        "region_factor": region_factor,
        "total_area": total_area
    }
    
    if "unit_cost" in result:
        if isinstance(result["unit_cost"], dict):
            result["total_cost"] = {
                k: round(v * total_area / 10000, 2) 
                for k, v in result["unit_cost"].items()
            }
        else:
            result["total_cost"] = round(result["unit_cost"] * total_area / 10000, 2)
    
    return result


if __name__ == "__main__":
    print("=" * 70)
    print("度量衡智库 - 贝叶斯概率估算模块 v1.0")
    print("=" * 70)
    
    test_cases = [
        {
            "name": "苏州31层框架-核心筒办公楼",
            "params": {
                "structure_type": "框架-核心筒",
                "floor_count": 31,
                "decoration_level": "精装",
                "region_factor": 1.08,
                "total_area": 50000
            }
        }
    ]
    
    for test in test_cases:
        print(f"\n{'=' * 60}")
        print(f"测试项目: {test['name']}")
        print(f"{'=' * 60}")
        
        result = bayesian_estimate(method="bayesian_mc", **test["params"])
        
        print(f"\n方法: {result['method']}")
        print(f"\n单方造价 (元/m2):")
        print(f"  均值: {result['unit_cost']['mean']:,.0f}")
        print(f"  P10: {result['unit_cost']['p10']:,.0f}")
        print(f"  P50: {result['unit_cost']['p50']:,.0f}")
        print(f"  P90: {result['unit_cost']['p90']:,.0f}")
        
        print(f"\n95%置信区间: {result['ci_95'][0]:,.0f} ~ {result['ci_95'][1]:,.0f}")
        print(f"精度(95%): +-{result['precision_95']}%")
