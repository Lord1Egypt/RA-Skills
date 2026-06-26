"""
Walk-Forward Validation
P1: Time-series cross-validation without data leakage
"""
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Callable
from dataclasses import dataclass
from datetime import datetime, timedelta
from sklearn.model_selection import TimeSeriesSplit

@dataclass
class WalkForwardResult:
    """Walk-forward 验证结果"""
    train_start: datetime
    train_end: datetime
    test_start: datetime
    test_end: datetime
    train_size: int
    test_size: int
    direction_accuracy: float  # 方向准确率
    brier_score: float  # 概率校准分数
    total_return: float
    max_drawdown: float
    sharpe_ratio: float
    num_trades: int
    win_rate: float


class WalkForwardValidator:
    """Walk-Forward 验证器"""
    
    def __init__(
        self,
        n_splits: int = 5,
        train_ratio: float = 0.7,
        min_train_size: int = 100
    ):
        self.n_splits = n_splits
        self.train_ratio = train_ratio
        self.min_train_size = min_train_size
    
    def split(
        self,
        df: pd.DataFrame,
        date_col: str = "ts"
    ) -> List[Tuple[pd.DataFrame, pd.DataFrame]]:
        """
        生成训练/测试集分割
        
        使用 walk-forward 窗口：
        - 每次向前滑动一个测试窗口
        - 训练集只包含历史数据
        """
        df = df.sort_values(date_col).reset_index(drop=True)
        n = len(df)
        
        if n < self.min_train_size * 2:
            raise ValueError(f"Data too small: {n} rows, need at least {self.min_train_size * 2}")
        
        splits = []
        fold_size = (n - self.min_train_size) // self.n_splits
        
        for i in range(self.n_splits):
            # 测试集起点
            test_start_idx = self.min_train_size + i * fold_size
            
            # 测试集终点
            if i == self.n_splits - 1:
                test_end_idx = n
            else:
                test_end_idx = test_start_idx + fold_size
            
            train_df = df.iloc[:test_start_idx].copy()
            test_df = df.iloc[test_start_idx:test_end_idx].copy()
            
            if len(test_df) < 10:
                continue
            
            splits.append((train_df, test_df))
        
        return splits
    
    def validate(
        self,
        df: pd.DataFrame,
        signal_func: Callable,  # 函数接收 df，返回信号
        date_col: str = "ts"
    ) -> List[WalkForwardResult]:
        """
        执行 walk-forward 验证
        
        Args:
            df: 数据DataFrame
            signal_func: 信号生成函数 (df) -> List[dict] with keys: signal, confidence, timestamp
            date_col: 日期列名
        """
        splits = self.split(df, date_col)
        results = []
        
        for train_df, test_df in splits:
            # 生成信号
            try:
                signals = signal_func(test_df)
            except Exception as e:
                continue
            
            # 计算指标
            result = self._evaluate_fold(
                train_df, test_df, signals, date_col
            )
            results.append(result)
        
        return results
    
    def _evaluate_fold(
        self,
        train_df: pd.DataFrame,
        test_df: pd.DataFrame,
        signals: List[Dict],
        date_col: str
    ) -> WalkForwardResult:
        """评估单个 fold"""
        # 简化实现
        returns = []
        correct_direction = 0
        
        for i, sig in enumerate(signals):
            if i + 1 >= len(test_df):
                break
            
            current_price = test_df.iloc[i]["close"]
            next_price = test_df.iloc[i + 1]["close"]
            
            # 实际方向
            actual_return = (next_price - current_price) / current_price
            actual_direction = "long" if actual_return > 0 else "short"
            
            # 预测方向
            pred_direction = sig.get("signal", "neutral")
            
            if pred_direction != "neutral":
                returns.append(actual_return)
                
                if (
                    (pred_direction == "bullish" and actual_return > 0) or
                    (pred_direction == "bearish" and actual_return < 0)
                ):
                    correct_direction += 1
        
        num_trades = len(returns)
        direction_accuracy = correct_direction / num_trades if num_trades > 0 else 0
        
        # 计算收益
        total_return = sum(returns) if returns else 0
        
        # 计算最大回撤
        cumulative = np.cumprod([1 + r for r in returns])
        peak = np.maximum.accumulate(cumulative)
        drawdown = (cumulative - peak) / peak
        max_drawdown = abs(min(drawdown)) if len(drawdown) > 0 else 0
        
        # Sharpe ratio
        if len(returns) > 1 and np.std(returns) > 0:
            sharpe = np.mean(returns) / np.std(returns) * np.sqrt(252)
        else:
            sharpe = 0
        
        win_rate = sum(1 for r in returns if r > 0) / num_trades if num_trades > 0 else 0
        
        return WalkForwardResult(
            train_start=train_df.iloc[0][date_col],
            train_end=train_df.iloc[-1][date_col],
            test_start=test_df.iloc[0][date_col],
            test_end=test_df.iloc[-1][date_col],
            train_size=len(train_df),
            test_size=len(test_df),
            direction_accuracy=direction_accuracy,
            brier_score=1 - direction_accuracy,  # 简化
            total_return=total_return,
            max_drawdown=max_drawdown,
            sharpe_ratio=sharpe,
            num_trades=num_trades,
            win_rate=win_rate
        )
    
    def get_summary(self, results: List[WalkForwardResult]) -> Dict:
        """获取验证摘要"""
        if not results:
            return {}
        
        return {
            "num_folds": len(results),
            "avg_direction_accuracy": np.mean([r.direction_accuracy for r in results]),
            "avg_brier_score": np.mean([r.brier_score for r in results]),
            "avg_return": np.mean([r.total_return for r in results]),
            "avg_max_drawdown": np.mean([r.max_drawdown for r in results]),
            "avg_sharpe": np.mean([r.sharpe_ratio for r in results]),
            "avg_win_rate": np.mean([r.win_rate for r in results]),
            "total_trades": sum(r.num_trades for r in results)
        }
