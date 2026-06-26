"""策略参数优化器 - 贝叶斯优化/网格搜索/遗传算法"""
from __future__ import annotations
import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Callable, Any
import numpy as np
import pandas as pd
from itertools import product
from copy import deepcopy

logger = logging.getLogger(__name__)


@dataclass
class ParamSpace:
    """参数空间定义"""
    name: str
    param_type: str  # int, float, categorical
    low: float = 0.0
    high: float = 1.0
    choices: List = None
    step: float = None
    log_scale: bool = False

    def sample(self) -> Any:
        if self.param_type == "int":
            return int(np.random.randint(self.low, self.high + 1))
        elif self.param_type == "float":
            if self.log_scale:
                return float(np.exp(np.random.uniform(np.log(self.low), np.log(self.high))))
            return float(np.random.uniform(self.low, self.high))
        elif self.param_type == "categorical":
            return np.random.choice(self.choices)
        return None

    def grid_values(self) -> List:
        if self.param_type == "int":
            step = self.step or 1
            return list(range(int(self.low), int(self.high) + 1, int(step)))
        elif self.param_type == "float":
            step = self.step or (self.high - self.low) / 10
            return list(np.arange(self.low, self.high + step, step))
        elif self.param_type == "categorical":
            return self.choices
        return []


@dataclass
class OptimizationResult:
    """优化结果"""
    best_params: Dict[str, Any]
    best_score: float
    all_trials: List[Dict]
    optimization_method: str
    convergence_history: List[float] = field(default_factory=list)

    def summary(self) -> str:
        lines = [
            f"优化方法: {self.optimization_method}",
            f"最优得分: {self.best_score:.4f}",
            f"最优参数: {self.best_params}",
            f"总试验次数: {len(self.all_trials)}",
        ]
        return "\n".join(lines)


class StrategyOptimizer:
    """策略参数优化器"""

    def __init__(self, strategy_class, metric_func: Callable = None):
        self.strategy_class = strategy_class
        self.metric_func = metric_func or self._default_metric
        self.param_spaces: Dict[str, ParamSpace] = {}

    def add_param(self, name: str, param_type: str, **kwargs) -> "StrategyOptimizer":
        self.param_spaces[name] = ParamSpace(name=name, param_type=param_type, **kwargs)
        return self

    def _default_metric(self, signals: List, df: pd.DataFrame) -> float:
        """默认评估指标：信号准确率加权收益"""
        if not signals:
            return 0.0
        correct = 0
        total_return = 0.0
        for sig in signals:
            idx = sig.get("index", 0)
            if idx + 5 < len(df):
                future_return = (float(df.iloc[idx + 5]["close"]) - float(df.iloc[idx]["close"])) / float(df.iloc[idx]["close"])
                if sig["direction"] == "BUY" and future_return > 0:
                    correct += 1
                    total_return += future_return
                elif sig["direction"] == "SELL" and future_return < 0:
                    correct += 1
                    total_return += abs(future_return)
        accuracy = correct / len(signals) if signals else 0
        avg_return = total_return / len(signals) if signals else 0
        return accuracy * 0.6 + min(avg_return * 10, 0.4)

    def _evaluate_params(self, params: Dict, df: pd.DataFrame) -> float:
        """评估单组参数"""
        try:
            strategy = self.strategy_class()
            for k, v in params.items():
                setattr(strategy, k, v)
            signals = []
            lookback = max(30, max(params.values()) if params else 30)
            for i in range(lookback, len(df)):
                window = df.iloc[:i + 1]
                signal = strategy.evaluate(window)
                if signal:
                    signals.append({
                        "index": i,
                        "direction": signal.direction,
                        "confidence": signal.confidence,
                        "strategy": signal.strategy_name
                    })
            return self.metric_func(signals, df)
        except Exception as e:
            logger.debug(f"参数评估失败: {e}, params={params}")
            return 0.0

    def grid_search(self, df: pd.DataFrame, n_jobs: int = 1) -> OptimizationResult:
        """网格搜索优化"""
        if not self.param_spaces:
            return OptimizationResult({}, 0.0, [], "grid_search")

        param_names = list(self.param_spaces.keys())
        param_values = [self.param_spaces[n].grid_values() for n in param_names]

        all_trials = []
        best_score = -np.inf
        best_params = {}

        for combo in product(*param_values):
            params = dict(zip(param_names, combo))
            score = self._evaluate_params(params, df)
            all_trials.append({"params": params, "score": score})

            if score > best_score:
                best_score = score
                best_params = params.copy()

            logger.debug(f"Grid: {params} -> {score:.4f}")

        return OptimizationResult(
            best_params=best_params,
            best_score=best_score,
            all_trials=all_trials,
            optimization_method="grid_search",
            convergence_history=[t["score"] for t in all_trials]
        )

    def random_search(self, df: pd.DataFrame, n_trials: int = 100) -> OptimizationResult:
        """随机搜索优化"""
        if not self.param_spaces:
            return OptimizationResult({}, 0.0, [], "random_search")

        all_trials = []
        best_score = -np.inf
        best_params = {}
        convergence = []

        for _ in range(n_trials):
            params = {name: space.sample() for name, space in self.param_spaces.items()}
            score = self._evaluate_params(params, df)
            all_trials.append({"params": params, "score": score})

            if score > best_score:
                best_score = score
                best_params = params.copy()

            convergence.append(best_score)

        return OptimizationResult(
            best_params=best_params,
            best_score=best_score,
            all_trials=all_trials,
            optimization_method="random_search",
            convergence_history=convergence
        )

    def bayesian_optimization(self, df: pd.DataFrame, n_trials: int = 50, n_initial: int = 10) -> OptimizationResult:
        """贝叶斯优化（简化版，使用高斯过程代理模型）"""
        if not self.param_spaces:
            return OptimizationResult({}, 0.0, [], "bayesian")

        all_trials = []
        best_score = -np.inf
        best_params = {}
        convergence = []

        initial_trials = min(n_initial, n_trials)
        for _ in range(initial_trials):
            params = {name: space.sample() for name, space in self.param_spaces.items()}
            score = self._evaluate_params(params, df)
            all_trials.append({"params": params, "score": score})
            if score > best_score:
                best_score = score
                best_params = params.copy()
            convergence.append(best_score)

        for trial_idx in range(initial_trials, n_trials):
            if len(all_trials) >= 2:
                params = self._acquisition_function(all_trials)
            else:
                params = {name: space.sample() for name, space in self.param_spaces.items()}

            score = self._evaluate_params(params, df)
            all_trials.append({"params": params, "score": score})
            if score > best_score:
                best_score = score
                best_params = params.copy()
            convergence.append(best_score)

        return OptimizationResult(
            best_params=best_params,
            best_score=best_score,
            all_trials=all_trials,
            optimization_method="bayesian",
            convergence_history=convergence
        )

    def _acquisition_function(self, trials: List[Dict]) -> Dict:
        """采集函数：基于历史试验选择下一个参数点"""
        scores = [t["score"] for t in trials]
        mean_score = np.mean(scores)
        std_score = np.std(scores) if len(scores) > 1 else 1.0

        best_trial = max(trials, key=lambda x: x["score"])
        best_params = best_trial["params"]

        new_params = {}
        for name, space in self.param_spaces.items():
            if np.random.random() < 0.7:
                best_val = best_params.get(name)
                if best_val is not None:
                    if space.param_type == "float":
                        noise = np.random.normal(0, (space.high - space.low) * 0.1)
                        new_val = np.clip(best_val + noise, space.low, space.high)
                        new_params[name] = float(new_val)
                    elif space.param_type == "int":
                        noise = np.random.randint(-2, 3)
                        new_val = np.clip(best_val + noise, space.low, space.high)
                        new_params[name] = int(new_val)
                    else:
                        new_params[name] = best_val
                else:
                    new_params[name] = space.sample()
            else:
                new_params[name] = space.sample()

        return new_params

    def genetic_algorithm(self, df: pd.DataFrame, n_generations: int = 20,
                          population_size: int = 30, mutation_rate: float = 0.1) -> OptimizationResult:
        """遗传算法优化"""
        if not self.param_spaces:
            return OptimizationResult({}, 0.0, [], "genetic")

        def create_individual():
            return {name: space.sample() for name, space in self.param_spaces.items()}

        def crossover(parent1, parent2):
            child = {}
            for name in self.param_spaces:
                child[name] = parent1[name] if np.random.random() < 0.5 else parent2[name]
            return child

        def mutate(individual):
            mutated = individual.copy()
            for name, space in self.param_spaces.items():
                if np.random.random() < mutation_rate:
                    mutated[name] = space.sample()
            return mutated

        population = [create_individual() for _ in range(population_size)]
        all_trials = []
        best_score = -np.inf
        best_params = {}
        convergence = []

        for gen in range(n_generations):
            fitness = []
            for ind in population:
                score = self._evaluate_params(ind, df)
                fitness.append(score)
                all_trials.append({"params": ind.copy(), "score": score, "generation": gen})
                if score > best_score:
                    best_score = score
                    best_params = ind.copy()

            convergence.append(best_score)
            logger.info(f"Gen {gen}: best={best_score:.4f}")

            sorted_indices = np.argsort(fitness)[::-1]
            elite_size = max(2, population_size // 5)
            elites = [population[i] for i in sorted_indices[:elite_size]]

            new_population = elites.copy()
            while len(new_population) < population_size:
                tournament_size = 3
                tournament = np.random.choice(len(population), tournament_size, replace=False)
                parent1_idx = tournament[np.argmax([fitness[i] for i in tournament])]
                tournament = np.random.choice(len(population), tournament_size, replace=False)
                parent2_idx = tournament[np.argmax([fitness[i] for i in tournament])]

                child = crossover(population[parent1_idx], population[parent2_idx])
                child = mutate(child)
                new_population.append(child)

            population = new_population[:population_size]

        return OptimizationResult(
            best_params=best_params,
            best_score=best_score,
            all_trials=all_trials,
            optimization_method="genetic_algorithm",
            convergence_history=convergence
        )


class WalkForwardOptimizer:
    """滚动窗口优化器（Walk-Forward Optimization）"""

    def __init__(self, strategy_class, train_ratio: float = 0.7, n_splits: int = 5):
        self.strategy_class = strategy_class
        self.train_ratio = train_ratio
        self.n_splits = n_splits

    def optimize(self, df: pd.DataFrame, optimizer_method: str = "bayesian",
                 n_trials: int = 50) -> List[OptimizationResult]:
        """滚动窗口优化"""
        total_len = len(df)
        split_size = total_len // self.n_splits
        results = []

        for i in range(self.n_splits):
            start_idx = i * split_size
            end_idx = min((i + 1) * split_size + split_size // 2, total_len)

            train_end = start_idx + int((end_idx - start_idx) * self.train_ratio)

            train_df = df.iloc[start_idx:train_end].reset_index(drop=True)
            test_df = df.iloc[train_end:end_idx].reset_index(drop=True)

            if len(train_df) < 30 or len(test_df) < 10:
                continue

            optimizer = StrategyOptimizer(self.strategy_class)
            self._add_default_params(optimizer)

            if optimizer_method == "bayesian":
                result = optimizer.bayesian_optimization(train_df, n_trials=n_trials)
            elif optimizer_method == "grid":
                result = optimizer.grid_search(train_df)
            else:
                result = optimizer.random_search(train_df, n_trials=n_trials)

            strategy = self.strategy_class()
            for k, v in result.best_params.items():
                setattr(strategy, k, v)

            test_signals = []
            for j in range(30, len(test_df)):
                window = test_df.iloc[:j + 1]
                signal = strategy.evaluate(window)
                if signal:
                    test_signals.append({
                        "index": j,
                        "direction": signal.direction,
                        "confidence": signal.confidence
                    })

            result.all_trials.append({
                "split": i,
                "train_score": result.best_score,
                "test_signals": len(test_signals),
                "params": result.best_params
            })

            results.append(result)
            logger.info(f"Split {i}: train_score={result.best_score:.4f}, test_signals={len(test_signals)}")

        return results

    def _add_default_params(self, optimizer: StrategyOptimizer):
        """添加默认参数空间"""
        optimizer.add_param("vol_multiplier", "float", low=1.0, high=3.0)
        optimizer.add_param("rsi_threshold", "int", low=20, high=40)
        optimizer.add_param("ma_period", "int", low=5, high=30)


class EnsembleOptimizer:
    """集成优化器 - 结合多种优化方法"""

    def __init__(self, strategy_class):
        self.strategy_class = strategy_class

    def optimize(self, df: pd.DataFrame, methods: List[str] = None,
                 n_trials: int = 50) -> OptimizationResult:
        """多方法集成优化"""
        if methods is None:
            methods = ["bayesian", "random", "genetic"]

        all_results = []

        for method in methods:
            optimizer = StrategyOptimizer(self.strategy_class)
            self._add_default_params(optimizer)

            if method == "bayesian":
                result = optimizer.bayesian_optimization(df, n_trials=n_trials)
            elif method == "genetic":
                result = optimizer.genetic_algorithm(df, n_generations=10)
            else:
                result = optimizer.random_search(df, n_trials=n_trials)

            all_results.append(result)

        if not all_results:
            return OptimizationResult({}, 0.0, [], "ensemble")

        best_result = max(all_results, key=lambda x: x.best_score)

        param_votes = {}
        for result in all_results:
            for trial in sorted(result.all_trials, key=lambda x: x.get("score", 0), reverse=True)[:5]:
                for k, v in trial.get("params", {}).items():
                    if k not in param_votes:
                        param_votes[k] = []
                    param_votes[k].append(v)

        consensus_params = {}
        for k, values in param_votes.items():
            if isinstance(values[0], (int, float)):
                consensus_params[k] = np.median(values)
                if isinstance(values[0], int):
                    consensus_params[k] = int(consensus_params[k])
            else:
                consensus_params[k] = max(set(values), key=values.count)

        consensus_score = StrategyOptimizer(self.strategy_class)._evaluate_params(consensus_params, df)

        if consensus_score >= best_result.best_score:
            return OptimizationResult(
                best_params=consensus_params,
                best_score=consensus_score,
                all_trials=[t for r in all_results for t in r.all_trials],
                optimization_method="ensemble_consensus"
            )

        return best_result

    def _add_default_params(self, optimizer: StrategyOptimizer):
        optimizer.add_param("vol_multiplier", "float", low=1.0, high=3.0)
        optimizer.add_param("rsi_threshold", "int", low=20, high=40)
        optimizer.add_param("ma_period", "int", low=5, high=30)
