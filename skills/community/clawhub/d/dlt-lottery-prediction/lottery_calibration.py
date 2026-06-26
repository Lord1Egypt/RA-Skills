#!/usr/bin/env python3
"""
彩票预测概率校准工具
提供Platt Scaling和Isotonic Regression校准
"""

import numpy as np
from typing import List, Tuple, Optional, Dict
from abc import ABC, abstractmethod
import warnings

try:
    from sklearn.calibration import CalibratedClassifierCV
    from sklearn.linear_model import LogisticRegression
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    LogisticRegression = None


class BaseCalibrator(ABC):
    """概率校准基类"""
    
    @abstractmethod
    def fit(self, y_score: np.ndarray, y_true: np.ndarray) -> 'BaseCalibrator':
        """拟合校准模型"""
        pass
    
    @abstractmethod
    def calibrate(self, y_score: np.ndarray) -> np.ndarray:
        """将原始分数转换为校准概率"""
        pass
    
    def fit_calibrate(self, y_score: np.ndarray, y_true: np.ndarray) -> np.ndarray:
        """fit + calibrate"""
        self.fit(y_score, y_true)
        return self.calibrate(y_score)


class PlattScaling(BaseCalibrator):
    """
    Platt Scaling (Platt Calibration)
    将原始分数通过逻辑回归映射到[0,1]概率
    
    原理: P(y=1|x) = sigmoid(a * score + b)
    通过最大似然估计a和b
    """
    
    def __init__(self, min_prob: float = 0.001, max_prob: float = 0.999):
        self.a = 1.0  # 缩放系数
        self.b = 0.0  # 偏移系数
        self.min_prob = min_prob
        self.max_prob = max_prob
        self.fitted_ = False
    
    def _sigmoid(self, x: np.ndarray) -> np.ndarray:
        """Safe sigmoid"""
        x = np.clip(x, -500, 500)
        return 1.0 / (1.0 + np.exp(-x))
    
    def fit(self, y_score: np.ndarray, y_true: np.ndarray) -> 'PlattScaling':
        """
        使用最大似然估计拟合Platt参数
        y_score: 原始分数 [n_samples]
        y_true: 真实标签 [n_samples], 0或1
        """
        if not SKLEARN_AVAILABLE:
            return self._fit_manual(y_score, y_true)
        
        y_score = np.asarray(y_score).flatten()
        y_true = np.asarray(y_true).flatten()
        
        # 使用sklearn逻辑回归
        # 注意：sklearn的LogisticRegression需要2D特征，我们把score作为1D特征
        X = y_score.reshape(-1, 1)
        
        try:
            lr = LogisticRegression(
                solver='lbfgs',
                max_iter=1000,
                C=1e10,  # 几乎无正则化
                warm_start=False
            )
            lr.fit(X, y_true)
            self.a = lr.coef_[0][0]
            self.b = lr.intercept_[0]
            self.fitted_ = True
            
            # 保存用于predict
            self._lr_model = lr
        except Exception as e:
            warnings.warn(f"Platt sklearn failed: {e}, falling back to manual")
            return self._fit_manual(y_score, y_true)
        
        return self
    
    def _fit_manual(self, y_score: np.ndarray, y_true: np.ndarray) -> 'PlattScaling':
        """手动拟合Platt参数（梯度下降）"""
        from scipy.optimize import minimize
        
        def neg_log_likelihood(params):
            a, b = params
            prob = self._sigmoid(a * y_score + b)
            prob = np.clip(prob, 1e-15, 1 - 1e-15)
            # 负对数似然
            nll = -np.mean(y_true * np.log(prob) + (1 - y_true) * np.log(1 - prob))
            return nll
        
        # 初始化
        x0 = [1.0, 0.0]
        result = minimize(neg_log_likelihood, x0, method='BFGS')
        self.a, self.b = result.x
        self.fitted_ = True
        return self
    
    def calibrate(self, y_score: np.ndarray) -> np.ndarray:
        """将分数转换为校准概率"""
        y_score = np.asarray(y_score).flatten()
        
        if not self.fitted_:
            raise ValueError("Calibrator not fitted. Call fit() first.")
        
        prob = self._sigmoid(self.a * y_score + self.b)
        prob = np.clip(prob, self.min_prob, self.max_prob)
        return prob
    
    def get_params(self) -> Dict:
        return {'a': self.a, 'b': self.b}


class IsotonicCalibrator(BaseCalibrator):
    """
    Isotonic Regression Calibration (保序回归校准)
    非参数化方法，优点是不假设函数形式，缺点是可能过拟合
    
    原理：找到单调非递减的分段常数函数f，使得f(score)逼近真实概率
    """
    
    def __init__(self, min_prob: float = 0.001, max_prob: float = 0.999):
        self.min_prob = min_prob
        self.max_prob = max_prob
        self.fitted_ = False
        self.x_out_ = None
        self.y_out_ = None
    
    def fit(self, y_score: np.ndarray, y_true: np.ndarray) -> 'IsotonicCalibrator':
        """
        使用保序回归拟合
        y_score: 原始分数 [n_samples]
        y_true: 真实标签 [n_samples], 0或1
        """
        y_score = np.asarray(y_score).flatten()
        y_true = np.asarray(y_true).flatten()
        
        # 排序
        idx = np.argsort(y_score)
        y_score_sorted = y_score[idx]
        y_true_sorted = y_true[idx]
        
        # 使用pool adjacent violators algorithm (PAVA)
        self.x_out_, self.y_out_ = self._pava(y_score_sorted, y_true_sorted)
        self.fitted_ = True
        
        return self
    
    def _pava(self, x: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Pool Adjacent Violators Algorithm
        实现保序回归
        """
        n = len(x)
        if n == 0:
            return np.array([]), np.array([])
        
        # 初始：每个点作为一个block
        blocks_x = [[x[i]] for i in range(n)]
        blocks_y = [[y[i]] for i in range(n)]
        
        # 合并违反单调性的block
        i = 0
        while i < len(blocks_y) - 1:
            # 计算当前block的平均y值
            current_mean = np.mean(blocks_y[i])
            next_mean = np.mean(blocks_y[i + 1])
            
            if current_mean > next_mean:  # 违反单调性
                # 合并两个block
                blocks_x[i] = blocks_x[i] + blocks_x[i + 1]
                blocks_y[i] = blocks_y[i] + blocks_y[i + 1]
                del blocks_x[i + 1]
                del blocks_y[i + 1]
                # 回退检查
                if i > 0:
                    i -= 1
            else:
                i += 1
        
        # 计算每个block的边界和平均值
        x_out = []
        y_out = []
        
        for bx, by in zip(blocks_x, blocks_y):
            x_out.append(min(bx))
            x_out.append(max(bx))
            mean_y = np.mean(by)
            y_out.append(mean_y)
            y_out.append(mean_y)
        
        return np.array(x_out), np.array(y_out)
    
    def calibrate(self, y_score: np.ndarray) -> np.ndarray:
        """将分数转换为校准概率（通过查表插值）"""
        y_score = np.asarray(y_score).flatten()
        
        if not self.fitted_:
            raise ValueError("Calibrator not fitted. Call fit() first.")
        
        # 边界
        x_out, y_out = self.x_out_, self.y_out_
        result = np.zeros_like(y_score, dtype=float)
        
        for i, score in enumerate(y_score):
            if score <= x_out[0]:
                result[i] = y_out[0]
            elif score >= x_out[-1]:
                result[i] = y_out[-1]
            else:
                # 线性插值
                idx = np.searchsorted(x_out, score) - 1
                idx = max(0, min(idx, len(x_out) - 2))
                t = (score - x_out[idx]) / (x_out[idx + 1] - x_out[idx] + 1e-10)
                result[i] = y_out[idx] * (1 - t) + y_out[idx + 1] * t
        
        result = np.clip(result, self.min_prob, self.max_prob)
        return result


class TemperatureScaling(BaseCalibrator):
    """
    Temperature Scaling
    最简单的校准方法：P = sigmoid(score / T)
    T是温度参数，通过最小化NLL拟合
    """
    
    def __init__(self, min_prob: float = 0.001, max_prob: float = 0.999):
        self.T = 1.0
        self.min_prob = min_prob
        self.max_prob = max_prob
        self.fitted_ = False
    
    def _sigmoid(self, x: np.ndarray) -> np.ndarray:
        x = np.clip(x, -500, 500)
        return 1.0 / (1.0 + np.exp(-x))
    
    def fit(self, y_score: np.ndarray, y_true: np.ndarray) -> 'TemperatureScaling':
        """拟合温度参数T"""
        from scipy.optimize import minimize_scalar
        
        y_score = np.asarray(y_score).flatten()
        y_true = np.asarray(y_true).flatten()
        
        def neg_log_likelihood(T):
            prob = self._sigmoid(y_score / T)
            prob = np.clip(prob, 1e-15, 1 - 1e-15)
            nll = -np.mean(y_true * np.log(prob) + (1 - y_true) * np.log(1 - prob))
            return nll
        
        result = minimize_scalar(neg_log_likelihood, bounds=(0.01, 10.0), method='bounded')
        self.T = result.x
        self.fitted_ = True
        return self
    
    def calibrate(self, y_score: np.ndarray) -> np.ndarray:
        y_score = np.asarray(y_score).flatten()
        if not self.fitted_:
            raise ValueError("Calibrator not fitted. Call fit() first.")
        
        prob = self._sigmoid(y_score / self.T)
        prob = np.clip(prob, self.min_prob, self.max_prob)
        return prob
    
    def get_params(self) -> Dict:
        return {'T': self.T}


class MultiClassCalibrator:
    """
    多分类校准器
    对每个类别分别进行Platt或Isotonic校准
    """
    
    def __init__(self, method: str = 'platt', n_classes: int = 35):
        self.method = method
        self.n_classes = n_classes
        self.calibrators_ = {}
        self.fitted_ = False
    
    def fit(self, y_scores: np.ndarray, y_true_onehot: np.ndarray) -> 'MultiClassCalibrator':
        """
        拟合多分类校准器
        y_scores: 原始分数 [n_samples, n_classes]
        y_true_onehot: 真实标签的one-hot编码 [n_samples, n_classes]
        """
        n_samples, n_classes = y_scores.shape
        
        for c in range(n_classes):
            if self.method == 'platt':
                calibrator = PlattScaling()
            elif self.method == 'isotonic':
                calibrator = IsotonicCalibrator()
            elif self.method == 'temperature':
                calibrator = TemperatureScaling()
            else:
                raise ValueError(f"Unknown method: {self.method}")
            
            y_score_c = y_scores[:, c]
            y_true_c = y_true_onehot[:, c]
            
            # 跳过没有正样本的类别
            if y_true_c.sum() < 1:
                continue
            
            calibrator.fit(y_score_c, y_true_c)
            self.calibrators_[c] = calibrator
        
        self.fitted_ = True
        return self
    
    def calibrate(self, y_scores: np.ndarray) -> np.ndarray:
        """
        校准多分类分数
        y_scores: [n_samples, n_classes]
        返回: 校准后的概率 [n_samples, n_classes]
        """
        if not self.fitted_:
            raise ValueError("Calibrator not fitted.")
        
        n_samples, n_classes = y_scores.shape
        calibrated = np.zeros_like(y_scores, dtype=float)
        
        for c in range(n_classes):
            if c in self.calibrators_:
                calibrated[:, c] = self.calibrators_[c].calibrate(y_scores[:, c])
            else:
                # 没有校准器的类别，用softmax归一化
                calibrated[:, c] = y_scores[:, c]
        
        # softmax归一化确保和为1
        calibrated_exp = np.exp(calibrated - np.max(calibrated, axis=1, keepdims=True))
        calibrated = calibrated_exp / np.sum(calibrated_exp, axis=1, keepdims=True)
        
        return calibrated


if __name__ == '__main__':
    # 测试代码
    np.random.seed(42)
    
    # 模拟原始分数（过度自信的模型）
    n = 1000
    y_score = np.random.randn(n) * 0.5 + 0.5
    y_score = np.clip(y_score, 0, 1)
    
    # 模拟真实标签（真实概率约等于score本身，有噪声）
    y_true = (y_score + np.random.randn(n) * 0.2 > 0.5).astype(int)
    
    # 测试Platt Scaling
    platt = PlattScaling()
    platt.fit(y_score, y_true)
    y_prob_platt = platt.calibrate(y_score)
    print(f"Platt params: a={platt.a:.4f}, b={platt.b:.4f}")
    
    # 测试Isotonic
    iso = IsotonicCalibrator()
    iso.fit(y_score, y_true)
    y_prob_iso = iso.calibrate(y_score)
    print("Isotonic fitted successfully")
    
    # 测试Temperature Scaling
    temp = TemperatureScaling()
    temp.fit(y_score, y_true)
    y_prob_temp = temp.calibrate(y_score)
    print(f"Temperature: T={temp.T:.4f}")
    
    # 验证校准效果
    from lottery_metrics import LotteryMetrics
    metrics = LotteryMetrics()
    
    ece_orig = metrics.expected_calibration_error(y_true, y_score, n_bins=10)
    ece_platt = metrics.expected_calibration_error(y_true, y_prob_platt, n_bins=10)
    ece_iso = metrics.expected_calibration_error(y_true, y_prob_iso, n_bins=10)
    ece_temp = metrics.expected_calibration_error(y_true, y_prob_temp, n_bins=10)
    
    print(f"\nECE对比:")
    print(f"  原始分数: {ece_orig:.4f}")
    print(f"  Platt Scaling: {ece_platt:.4f}")
    print(f"  Isotonic: {ece_iso:.4f}")
    print(f"  Temperature: {ece_temp:.4f}")
