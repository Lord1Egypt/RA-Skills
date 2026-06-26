#!/usr/bin/env python3
"""
彩票预测评价指标工具
提供Hit@K, NDCG@K, ECE, CalibrationCurve等指标
"""

import numpy as np
from typing import List, Dict, Tuple, Optional
import warnings

try:
    from sklearn.metrics import ndcg_score
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False


class LotteryMetrics:
    """彩票预测评价指标计算器"""
    
    @staticmethod
    def hit_at_k(predicted: List[int], actual: List[int], k: int) -> float:
        """
        计算Hit@K指标
        predicted: 预测的号码列表（已排序，分数高的在前）
        actual: 实际中奖号码列表
        k: 考虑前K个预测
        """
        if k <= 0:
            return 0.0
        predicted_k = predicted[:k]
        actual_set = set(actual)
        hits = sum(1 for num in predicted_k if num in actual_set)
        return float(hits > 0)  # Hit@K: 至少有1个命中即为1
    
    @staticmethod
    def hit_count_at_k(predicted: List[int], actual: List[int], k: int) -> int:
        """
        计算Hit Count@K（命中的号码数量）
        """
        predicted_k = predicted[:k]
        actual_set = set(actual)
        return sum(1 for num in predicted_k if num in actual_set)
    
    @staticmethod
    def ndcg_at_k(predicted: List[int], actual: List[int], k: int, 
                  relevance: Optional[List[float]] = None) -> float:
        """
        计算NDCG@K指标
        predicted: 预测的号码列表（已排序）
        actual: 实际中奖号码列表
        k: 考虑前K个
        relevance: 相关性分数，默认为binary(命中=1, 否则=0)
        """
        if k <= 0:
            return 0.0
        
        # 如果没有sklearn，使用手动实现
        if not SKLEARN_AVAILABLE:
            return LotteryMetrics._ndcg_at_k_manual(predicted, actual, k)
        
        # 构建相关性矩阵 (1 x k)
        if relevance is None:
            actual_set = set(actual)
            relevance = [1.0 if num in actual_set else 0.0 for num in predicted[:k]]
        
        # 填充到k长度
        while len(relevance) < k:
            relevance.append(0.0)
        relevance = np.array([relevance[:k]])
        
        # 构建预测分数（按排序位置衰减）
        predicted_scores = np.array([[k - i for i in range(k)]])
        
        try:
            return ndcg_score(relevance, predicted_scores, k=k)
        except:
            return LotteryMetrics._ndcg_at_k_manual(predicted, actual, k)
    
    @staticmethod
    def _ndcg_at_k_manual(predicted: List[int], actual: List[int], k: int) -> float:
        """手动计算NDCG@K"""
        actual_set = set(actual)
        k = min(k, len(predicted))
        
        # DCG
        dcg = 0.0
        for i in range(k):
            num = predicted[i]
            rel = 1.0 if num in actual_set else 0.0
            dcg += rel / np.log2(i + 2)  # i+2因为i从0开始
        
        # IDCG (ideal DCG)
        idcg = 0.0
        num_actual = min(len(actual), k)
        for i in range(num_actual):
            idcg += 1.0 / np.log2(i + 2)
        
        if idcg == 0:
            return 0.0
        
        return dcg / idcg
    
    @staticmethod
    def precision_at_k(predicted: List[int], actual: List[int], k: int) -> float:
        """计算Precision@K"""
        if k <= 0:
            return 0.0
        predicted_k = predicted[:k]
        actual_set = set(actual)
        hits = sum(1 for num in predicted_k if num in actual_set)
        return hits / k
    
    @staticmethod
    def recall_at_k(predicted: List[int], actual: List[int], k: int) -> float:
        """计算Recall@K"""
        if k <= 0 or len(actual) == 0:
            return 0.0
        predicted_k = predicted[:k]
        actual_set = set(actual)
        hits = sum(1 for num in predicted_k if num in actual_set)
        return hits / len(actual)
    
    @staticmethod
    def expected_calibration_error(y_true: np.ndarray, 
                                    y_prob: np.ndarray, 
                                    n_bins: int = 10) -> float:
        """
        计算ECE (Expected Calibration Error)
        ECE = sum(|B_m| / n * |acc(B_m) - conf(B_m)|)
        y_true: 真实标签 (0或1)
        y_prob: 预测概率 [0, 1]
        n_bins: 分箱数量
        """
        bin_edges = np.linspace(0, 1, n_bins + 1)
        ece = 0.0
        total = len(y_true)
        
        for i in range(n_bins):
            bin_lower = bin_edges[i]
            bin_upper = bin_edges[i + 1]
            
            # 找到该分箱的样本
            if i == n_bins - 1:
                in_bin = (y_prob >= bin_lower) & (y_prob <= bin_upper)
            else:
                in_bin = (y_prob >= bin_lower) & (y_prob < bin_upper)
            
            bin_size = np.sum(in_bin)
            if bin_size == 0:
                continue
            
            # 该分箱的平均预测概率（置信度）
            avg_confidence = np.mean(y_prob[in_bin])
            
            # 该分箱的准确率
            accuracy = np.mean(y_true[in_bin])
            
            # 加权
            ece += (bin_size / total) * np.abs(accuracy - avg_confidence)
        
        return ece
    
    @staticmethod
    def calibration_curve(y_true: np.ndarray, 
                          y_prob: np.ndarray, 
                          n_bins: int = 10) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        计算校准曲线
        返回: (fraction_of_positives, mean_predicted_value, bin_edges)
        """
        bin_edges = np.linspace(0, 1, n_bins + 1)
        fractions = []
        means = []
        
        for i in range(n_bins):
            bin_lower = bin_edges[i]
            bin_upper = bin_edges[i + 1]
            
            if i == n_bins - 1:
                in_bin = (y_prob >= bin_lower) & (y_prob <= bin_upper)
            else:
                in_bin = (y_prob >= bin_lower) & (y_prob < bin_upper)
            
            bin_size = np.sum(in_bin)
            if bin_size == 0:
                fractions.append(0.0)
                means.append((bin_lower + bin_upper) / 2)
            else:
                fractions.append(np.mean(y_true[in_bin]))
                means.append(np.mean(y_prob[in_bin]))
        
        return np.array(fractions), np.array(means), bin_edges
    
    @staticmethod
    def evaluate_prediction_set(predicted_ranked: List[int], 
                                actual: List[int], 
                                k_values: List[int] = None) -> Dict:
        """
        综合评估预测结果
        返回多种指标
        """
        if k_values is None:
            k_values = [3, 5, 6, 10]
        
        results = {}
        for k in k_values:
            results[f'hit@{k}'] = LotteryMetrics.hit_at_k(predicted_ranked, actual, k)
            results[f'hit_count@{k}'] = LotteryMetrics.hit_count_at_k(predicted_ranked, actual, k)
            results[f'ndcg@{k}'] = LotteryMetrics.ndcg_at_k(predicted_ranked, actual, k)
            results[f'precision@{k}'] = LotteryMetrics.precision_at_k(predicted_ranked, actual, k)
            results[f'recall@{k}'] = LotteryMetrics.recall_at_k(predicted_ranked, actual, k)
        
        return results


class DLTPrizeEvaluator:
    """大乐透奖项计算器"""
    
    # 奖项定义: (前区命中数, 后区命中数) -> (奖项名称, 奖金)
    PRIZE_RULES = {
        (5, 2): ("一等奖(头奖)", None),      # 5+2
        (5, 1): ("二等奖", None),              # 5+1
        (5, 0): ("三等奖", 5000),              # 5+0
        (4, 2): ("三等奖", 6666),              # 4+2
        (4, 1): ("四等奖", 300),               # 4+1
        (3, 2): ("四等奖", 380),                # 3+2
        (4, 0): ("五等奖", 150),               # 4+0
        (3, 1): ("五等奖", 200),                # 3+1
        (2, 2): ("五等奖", 200),                # 2+2
        (3, 0): ("六等奖", 15),                # 3+0
        (2, 1): ("六等奖", 18),                # 2+1
        (1, 2): ("六等奖", 18),                # 1+2
        (0, 2): ("七等奖", 5),                 # 0+2
        (2, 0): ("七等奖", 5),                 # 2+0
        (1, 1): ("七等奖", 5),                 # 1+1
        (3, 0): ("七等奖", 5),                 # 3+0
    }
    
    @staticmethod
    def evaluate(front_pred: List[int], back_pred: List[int],
                 front_actual: List[int], back_actual: List[int]) -> Dict:
        """
        评估单次预测的中奖情况
        """
        front_hit = len(set(front_pred) & set(front_actual))
        back_hit = len(set(back_pred) & set(back_actual))
        
        key = (front_hit, back_hit)
        
        # 检查所有可能匹配的奖项
        prize_name = "未中奖"
        prize_level = 0
        
        # 按优先级检查
        for (f, b), (name, _) in sorted(DLTPrizeEvaluator.PRIZE_RULES.items(), 
                                         key=lambda x: -(x[0][0] * 10 + x[0][1])):
            if front_hit == f and back_hit == b:
                prize_name = name
                prize_level = DLTPrizeEvaluator._get_level(f, b)
                break
        
        return {
            'front_hit': front_hit,
            'back_hit': back_hit,
            'prize_name': prize_name,
            'prize_level': prize_level,
            'is_winner': prize_level > 0
        }
    
    @staticmethod
    def _get_level(front_hit: int, back_hit: int) -> int:
        """根据命中数确定奖项等级"""
        if front_hit == 5 and back_hit == 2:
            return 1
        elif front_hit == 5 and back_hit == 1:
            return 2
        elif (front_hit == 5 and back_hit == 0) or (front_hit == 4 and back_hit == 2):
            return 3
        elif (front_hit == 4 and back_hit == 1) or (front_hit == 3 and back_hit == 2):
            return 4
        elif (front_hit == 4 and back_hit == 0) or (front_hit == 3 and back_hit == 1) or (front_hit == 2 and back_hit == 2):
            return 5
        elif (front_hit == 3 and back_hit == 0) or (front_hit == 2 and back_hit == 1) or (front_hit == 1 and back_hit == 2) or (front_hit == 0 and back_hit == 2):
            return 6
        elif front_hit + back_hit >= 2:  # 2+0, 1+1, 0+1+...
            return 7
        return 0
    
    @staticmethod
    def evaluate_batch(predictions: List[Tuple[List[int], List[int]]],
                       actuals: List[Tuple[List[int], List[int]]]) -> Dict:
        """
        批量评估预测结果
        predictions: [(front_pred, back_pred), ...]
        actuals: [(front_actual, back_actual), ...]
        """
        results = []
        prize_counts = {i: 0 for i in range(1, 8)}
        prize_counts[0] = 0
        
        for (front_pred, back_pred), (front_actual, back_actual) in zip(predictions, actuals):
            eval_result = DLTPrizeEvaluator.evaluate(
                front_pred, back_pred, front_actual, back_actual
            )
            results.append(eval_result)
            prize_counts[eval_result['prize_level']] += 1
        
        total = len(results)
        
        return {
            'total': total,
            'prize_counts': prize_counts,
            'hit_rates': {k: v / total for k, v in prize_counts.items()},
            'results': results
        }


if __name__ == '__main__':
    # 测试代码
    metrics = LotteryMetrics()
    
    # 模拟预测：35个前区按分数排序
    predicted_front = list(range(1, 36))  # 假设1-35按分数排序
    actual_front = [3, 12, 25, 26, 27]    # 假设实际开奖
    
    print("=== 前区预测评估 ===")
    results = metrics.evaluate_prediction_set(predicted_front, actual_front)
    for k, v in results.items():
        print(f"  {k}: {v:.4f}")
    
    # 测试ECE
    y_true = np.array([1, 1, 0, 0, 1, 0, 1, 0, 0, 1])
    y_prob = np.array([0.9, 0.8, 0.3, 0.2, 0.7, 0.1, 0.85, 0.15, 0.25, 0.75])
    ece = metrics.expected_calibration_error(y_true, y_prob, n_bins=5)
    print(f"\nECE: {ece:.4f}")
    
    # 测试奖项
    print("\n=== 奖项评估 ===")
    eval_result = DLTPrizeEvaluator.evaluate(
        front_pred=[11, 12, 25, 26, 27],
        back_pred=[8, 11],
        front_actual=[11, 12, 25, 26, 27],
        back_actual=[8, 11]
    )
    print(f"结果: {eval_result}")
