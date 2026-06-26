#!/usr/bin/env python3
"""
时序交叉验证模块
提供TimeSeriesSplit和ExpandingWindowCV用于消除数据泄漏
"""

import numpy as np
from typing import List, Tuple, Optional, Callable, Dict, Any, Generator
from dataclasses import dataclass


@dataclass
class TimeSeriesSplitResult:
    """时序分割结果"""
    train_indices: np.ndarray
    test_indices: np.ndarray
    train_start: int
    train_end: int
    test_start: int
    test_end: int
    fold: int


class TimeSeriesSplit:
    """
    sklearn风格的TimeSeriesSplit
    
    时序交叉验证的核心思想：
    - 训练集总是在测试集之前
    - 避免使用未来信息预测过去（数据泄漏）
    
    用法:
        tscv = TimeSeriesSplit(n_splits=5, gap=0)
        for train_idx, test_idx in tscv.split(X):
            # train_idx: 早期数据
            # test_idx: 后期数据
            X_train, X_test = X[train_idx], X[test_idx]
    """
    
    def __init__(self, n_splits: int = 5, gap: int = 0, test_size: Optional[int] = None):
        """
        初始化时序分割器
        
        Args:
            n_splits: 分割数量
            gap: 训练集和测试集之间的间隔（用于避免数据泄漏）
            test_size: 每个测试集的大小，如果为None则自动计算
        """
        self.n_splits = n_splits
        self.gap = gap
        self.test_size = test_size
    
    def split(self, X: np.ndarray, 
              y: Optional[np.ndarray] = None,
              groups: Optional[np.ndarray] = None) -> Generator[Tuple[np.ndarray, np.ndarray], None, None]:
        """
        生成训练/测试索引分割
        
        Args:
            X: 特征矩阵 [n_samples, n_features]
            y: 标签（可选）
            groups: 分组标签（可选，用于确保同一组数据不在训练和测试中分裂）
            
        Yields:
            (train_indices, test_indices)
        """
        n_samples = len(X)
        
        # 计算测试集大小
        if self.test_size is None:
            # 均匀分割，但确保至少有n_splits个测试样本
            test_size = max(n_samples // (self.n_splits + 1), 1)
        else:
            test_size = self.test_size
        
        # 验证
        if n_samples < 2 * test_size:
            # 如果数据太少，只生成一个分割
            test_size = n_samples // 2
        
        # 生成分割
        for fold in range(self.n_splits):
            # 测试集：[n_samples - (n_splits - fold) * test_size, n_samples - (n_splits - fold - 1) * test_size)
            test_end = n_samples - fold * test_size
            test_start = test_end - test_size
            
            # 训练集：[0, test_start - gap)
            train_end = max(0, test_start - self.gap)
            train_start = 0
            
            # 确保有足够的训练数据
            if train_end - train_start < test_size:
                # 合并到前一个分割
                continue
            
            train_indices = np.arange(train_start, train_end)
            test_indices = np.arange(max(test_start, train_end), test_end)
            
            if len(test_indices) == 0:
                continue
            
            yield train_indices, test_indices
    
    def get_n_splits(self, X: Optional[np.ndarray] = None, 
                     y: Optional[np.ndarray] = None, 
                     groups: Optional[np.ndarray] = None) -> int:
        """返回分割数量"""
        return self.n_splits


class ExpandingWindowCV:
    """
    Expanding Window (扩展窗口) 交叉验证
    
    与TimeSeriesSplit的区别：
    - TimeSeriesSplit: 训练窗口固定，测试窗口滑动
    - ExpandingWindowCV: 训练窗口逐步扩大，测试窗口固定或滑动
    
    这种方法更适合彩票预测：
    - 每次用更多的历史数据训练
    - 保持测试集大小一致，便于比较
    """
    
    def __init__(self, 
                 n_splits: int = 10,
                 test_size: int = 5,
                 min_train_size: int = 50,
                 gap: int = 0):
        """
        初始化扩展窗口CV
        
        Args:
            n_splits: 最大分割数量
            test_size: 每个测试集的大小
            min_train_size: 最少训练样本数
            gap: 训练集和测试集之间的间隔
        """
        self.n_splits = n_splits
        self.test_size = test_size
        self.min_train_size = min_train_size
        self.gap = gap
    
    def split(self, X: np.ndarray,
              y: Optional[np.ndarray] = None,
              groups: Optional[np.ndarray] = None) -> Generator[Tuple[np.ndarray, np.ndarray], None, None]:
        """
        生成扩展窗口分割
        
        每个分割：
        - 训练集从开始逐步扩大
        - 测试集固定大小，在训练集之后
        """
        n_samples = len(X)
        
        # 有效分割数量
        max_folds = n_samples - self.min_train_size - self.test_size
        actual_splits = min(self.n_splits, max(1, max_folds))
        
        if actual_splits <= 0:
            # 数据太少，只有一个分割
            train_indices = np.arange(0, n_samples - self.test_size)
            test_indices = np.arange(n_samples - self.test_size, n_samples)
            yield train_indices, test_indices
            return
        
        # 计算每个fold的训练大小增量
        train_size_range = n_samples - self.test_size - self.min_train_size
        if actual_splits > 1:
            train_increment = train_size_range // (actual_splits - 1)
        else:
            train_increment = 0
        
        for fold in range(actual_splits):
            # 训练大小从min_train_size开始，逐步增加
            train_size = self.min_train_size + fold * train_increment
            
            # 训练集：[0, train_size)
            train_end = train_size
            train_start = 0
            
            # 测试集：[train_end + gap, train_end + gap + test_size)
            test_start = train_end + self.gap
            test_end = min(test_start + self.test_size, n_samples)
            
            train_indices = np.arange(train_start, train_end)
            test_indices = np.arange(test_start, test_end)
            
            # 确保索引有效
            if len(train_indices) < self.min_train_size or len(test_indices) == 0:
                if test_start >= n_samples:
                    continue
            
            yield train_indices, test_indices
    
    def get_n_splits(self, X: Optional[np.ndarray] = None,
                     y: Optional[np.ndarray] = None,
                     groups: Optional[np.ndarray] = None) -> int:
        return self.n_splits


class PurgedTimeSeriesCV:
    """
    Purge Time Series Cross-Validation (净化时序交叉验证)
    
    在训练集和测试集之间引入gap，以避免信息泄漏。
    特别适合金融/时序预测场景。
    
    原理：
    - 在训练集末尾和测试集开始之间保留一个"缓冲区"
    - 缓冲区内的样本既不在训练也不在测试中使用
    """
    
    def __init__(self,
                 n_splits: int = 5,
                 gap: int = 2,
                 horizon: int = 1):
        """
        Args:
            n_splits: 分割数量
            gap: 训练集和测试集之间的间隔（单位：样本数）
            horizon: 预测视野（预测目标与训练集末尾的距离）
        """
        self.n_splits = n_splits
        self.gap = gap
        self.horizon = horizon
    
    def split(self, X: np.ndarray,
              y: Optional[np.ndarray] = None) -> Generator[Tuple[np.ndarray, np.ndarray], None, None]:
        """
        生成净化时序分割
        
        每个分割：
        - 训练集：[0, train_end)
        - 缓冲带：[train_end, train_end + gap)
        - 测试集：[train_end + gap + horizon, train_end + gap + horizon + test_size)
        """
        n_samples = len(X)
        test_size = max(1, n_samples // (self.n_splits + 1))
        
        for fold in range(self.n_splits):
            # 测试集末端位置
            test_end = n_samples - fold * test_size
            
            # 测试集开始位置
            test_start = max(0, test_end - test_size)
            
            # 训练集末端（测试集开始前的gap之后）
            train_end = max(0, test_start - self.gap - self.horizon)
            
            # 确保有足够的训练数据
            if train_end < self.min_train_size(fold):
                continue
            
            train_indices = np.arange(0, train_end)
            test_indices = np.arange(test_start, test_end)
            
            if len(test_indices) == 0:
                continue
            
            yield train_indices, test_indices
    
    def min_train_size(self, fold: int) -> int:
        """计算第fold折的最少训练样本数"""
        return max(10, 50 - fold * 5)


class BacktestRunner:
    """
    时序回测运行器
    
    用于在时序数据上运行完整的回测流程
    """
    
    def __init__(self, cv: Optional[Any] = None):
        self.cv = cv or ExpandingWindowCV(n_splits=10, test_size=5)
        self.results_ = []
    
    def run(self,
            X: np.ndarray,
            y: Optional[np.ndarray] = None,
            model_factory: Callable = None,
            predict_fn: Callable = None,
            eval_fn: Callable = None,
            train_kwargs: Dict = None,
            predict_kwargs: Dict = None) -> Dict[str, Any]:
        """
        运行回测
        
        Args:
            X: 特征数据 [n_samples, n_features]
            y: 标签数据
            model_factory: 模型工厂函数 () -> model
            predict_fn: 预测函数 (model, X_test) -> predictions
            eval_fn: 评估函数 (predictions, y_test) -> metrics_dict
            train_kwargs: 训练模型时的额外参数
            predict_kwargs: 预测时的额外参数
            
        Returns:
            回测结果字典
        """
        train_kwargs = train_kwargs or {}
        predict_kwargs = predict_kwargs or {}
        
        all_metrics = []
        fold_details = []
        
        for fold, (train_idx, test_idx) in enumerate(self.cv.split(X)):
            X_train, X_test = X[train_idx], X[test_idx]
            y_train = y[train_idx] if y is not None else None
            y_test = y[test_idx] if y is not None else None
            
            # 训练模型
            model = model_factory()
            if hasattr(model, 'fit'):
                if y_train is not None:
                    model.fit(X_train, y_train, **train_kwargs)
                else:
                    model.fit(X_train, **train_kwargs)
            
            # 预测
            if predict_fn is not None:
                predictions = predict_fn(model, X_test, **predict_kwargs)
            else:
                predictions = model.predict(X_test)
            
            # 评估
            if eval_fn is not None and y_test is not None:
                metrics = eval_fn(predictions, y_test)
            else:
                metrics = {}
            
            all_metrics.append(metrics)
            fold_details.append({
                'fold': fold,
                'train_size': len(train_idx),
                'test_size': len(test_idx),
                'train_range': (train_idx[0], train_idx[-1]),
                'test_range': (test_idx[0], test_idx[-1]),
                'metrics': metrics
            })
        
        # 汇总结果
        summary = self._summarize_metrics(all_metrics)
        
        return {
            'folds': fold_details,
            'summary': summary,
            'n_folds': len(fold_details),
            'total_test_samples': sum(f['test_size'] for f in fold_details)
        }
    
    def _summarize_metrics(self, all_metrics: List[Dict]) -> Dict[str, Any]:
        """汇总所有折的指标"""
        if not all_metrics:
            return {}
        
        summary = {}
        for key in all_metrics[0].keys():
            values = [m[key] for m in all_metrics if key in m and m[key] is not None]
            if values:
                summary[key] = {
                    'mean': np.mean(values),
                    'std': np.std(values),
                    'min': np.min(values),
                    'max': np.max(values),
                    'values': values
                }
        
        return summary


# sklearn compatibility
try:
    from sklearn.model_selection import TimeSeriesSplit as SklearnTS
    HAS_SKLEARN_CV = True
except ImportError:
    HAS_SKLEARN_CV = False


def get_sklearn_timeseries_split(n_splits: int = 5, gap: int = 0) -> Any:
    """获取sklearn的TimeSeriesSplit（如果可用）"""
    if HAS_SKLEARN_CV:
        return SklearnTS(n_splits=n_splits, gap=gap)
    else:
        return TimeSeriesSplit(n_splits=n_splits, gap=gap)


if __name__ == '__main__':
    # 测试代码
    np.random.seed(42)
    n = 100
    X = np.random.randn(n, 5)
    y = np.random.randint(0, 2, n)
    
    print("=== TimeSeriesSplit ===")
    tscv = TimeSeriesSplit(n_splits=5, test_size=5)
    for fold, (train_idx, test_idx) in enumerate(tscv.split(X)):
        print(f"Fold {fold}: train=[{train_idx[0]}:{train_idx[-1]}] size={len(train_idx)}, "
              f"test=[{test_idx[0]}:{test_idx[-1]}] size={len(test_idx)}")
    
    print("\n=== ExpandingWindowCV ===")
    ewcv = ExpandingWindowCV(n_splits=5, test_size=5, min_train_size=20)
    for fold, (train_idx, test_idx) in enumerate(ewcv.split(X)):
        print(f"Fold {fold}: train=[{train_idx[0]}:{train_idx[-1]}] size={len(train_idx)}, "
              f"test=[{test_idx[0]}:{test_idx[-1]}] size={len(test_idx)}")
    
    print("\n=== BacktestRunner 示例 ===")
    from sklearn.ensemble import RandomForestClassifier
    
    def rf_factory():
        return RandomForestClassifier(n_estimators=10, random_state=42)
    
    def eval_predictions(y_pred, y_true):
        return {'accuracy': np.mean(y_pred == y_true)}
    
    runner = BacktestRunner(cv=ExpandingWindowCV(n_splits=3, test_size=10, min_train_size=30))
    result = runner.run(X, y, model_factory=rf_factory, eval_fn=eval_predictions)
    
    print(f"总折数: {result['n_folds']}")
    for key, val in result['summary'].items():
        print(f"  {key}: mean={val['mean']:.4f}, std={val['std']:.4f}")
