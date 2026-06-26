#!/usr/bin/env python3
"""
贝叶斯遗漏值模型
使用Beta-Binomial共轭先验建模每个彩票号码的基础出现概率
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from collections import defaultdict
from scipy.special import beta as beta_func, betaln, gammaln
from scipy.stats import beta as beta_dist


class BetaBinomialMissing:
    """
    贝叶斯遗漏值模型
    
    使用Beta-Binomial共轭先验建模每个号码的出现概率
    - 先验: Beta(α, β)，表示在没有数据时的先验信念
    - 似然: Binomial(n, p)，n次试验中号码出现k次
    - 后验: Beta(α + k, β + n - k)
    
    对于遗漏值（missing value），我们计算后验分位数作为特征
    """
    
    def __init__(self, 
                 alpha_prior: float = 1.0, 
                 beta_prior: float = 1.0,
                 # 使用Jeffreys先验 alpha=0.5, beta=0.5
                 # 或均匀先验 alpha=1, beta=1
                 method: str = 'jeffreys'):
        """
        初始化贝叶斯遗漏值模型
        
        Args:
            alpha_prior: Beta先验的α参数
            beta_prior: Beta先验的β参数
            method: 先验方法
                - 'jeffreys': Jeffreys先验 α=0.5, β=0.5
                - 'uniform': 均匀先验 α=1, β=1
                - 'laplacian': 拉普拉斯平滑 α=1, β=1 (等价于uniform)
                - 'custom': 自定义
        """
        if method == 'jeffreys':
            self.alpha_prior = 0.5
            self.beta_prior = 0.5
        elif method == 'uniform' or method == 'laplacian':
            self.alpha_prior = 1.0
            self.beta_prior = 1.0
        elif method == 'custom':
            self.alpha_prior = alpha_prior
            self.beta_prior = beta_prior
        else:
            raise ValueError(f"Unknown method: {method}")
        
        self.method = method
        self.history_ = {}  # 存储每个号码的历史统计
    
    def update(self, numbers: List[int], n_trials: int = 1):
        """
        用新数据更新贝叶斯模型
        numbers: 本期出现的号码列表
        n_trials: 试验次数（通常为1）
        """
        for num in numbers:
            if num not in self.history_:
                self.history_[num] = {'alpha': self.alpha_prior, 
                                      'beta': self.beta_prior}
            
            # 更新后验：Beta(α + k, β + n - k)，k是出现次数
            self.history_[num]['alpha'] += 1 * n_trials  # k=1
            self.history_[num]['beta'] += (1 - 1) * n_trials  # n-k=0
    
    def update_batch(self, all_draws: List[List[int]], n_trials: int = 1):
        """
        批量更新
        all_draws: 历史开奖记录列表，每条记录是一个号码列表
        """
        for numbers in all_draws:
            self.update(numbers, n_trials)
    
    def get_posterior_params(self, num: int) -> Tuple[float, float]:
        """
        获取某个号码的后验Beta分布参数
        """
        if num not in self.history_:
            return self.alpha_prior, self.beta_prior
        
        return self.history_[num]['alpha'], self.history_[num]['beta']
    
    def get_expected_prob(self, num: int) -> float:
        """
        获取某个号码出现概率的期望值（后验均值）
        E[p | data] = α / (α + β)
        """
        alpha, beta = self.get_posterior_params(num)
        return alpha / (alpha + beta)
    
    def get_missing_value(self, num: int, current_missing: int) -> float:
        """
        计算遗漏值的贝叶斯特征
        
        遗漏值本身不是独立的随机变量，我们用后验预测分布来建模
        考虑当前遗漏期数current_missing，计算：
        1. 后验均值
        2. 后验分位数
        3. 遗漏超过current_missing的后验概率
        """
        alpha, beta = self.get_posterior_params(num)
        
        # 后验均值
        mean_prob = alpha / (alpha + beta)
        
        # 遗漏超过current_missing期的后验概率
        # 即 P(X > current_missing | data)，其中X是下一次出现前的遗漏期数
        # 这等价于计算后验预测分布中 P(p < mean_prob) 随着遗漏增加的变化
        
        # 更实用的做法：计算后验分位数
        # P(p <= x | data) = CDF_Beta(x; alpha, beta)
        # 分位数特征：
        # - 中位数分位数
        # - 低分位数（表示当前遗漏期数相对异常）
        # - 高分位数
        
        # 计算遗漏值超过当前遗漏期数的"异常度"
        # 基于Beta-Binomial预测分布
        # P(missed > m) = sum_{k=0}^{m} C(n,k) p^k (1-p)^(n-k) 在后验p上的积分
        
        # 简化：用后验分布的累积概率作为遗漏异常度
        # 如果mean_prob很低但遗漏了很久，说明可能快出了
        
        return current_missing * mean_prob  # 遗漏加权的期望概率
    
    def get_missing_quantile(self, num: int, current_missing: int) -> float:
        """
        计算遗漏值的贝叶斯后验分位数作为特征
        
        返回：当前遗漏期数对应的后验分位数
        即 P(p <= observed_freq | data) 的值
        """
        alpha, beta = self.get_posterior_params(num)
        
        # 计算先验/后验均值作为"观测频率"
        observed_freq = alpha / (alpha + beta)
        
        # 计算遗漏分位数
        # 这是一个简化的启发式方法
        # 真实的遗漏分位数需要考虑等待时间分布
        
        # Beta分布的CDF：P(p <= x) = I_x(alpha, beta) / B(alpha, beta)
        # 我们用均值作为基准，计算遗漏对概率估计的影响
        
        # 遗漏分位数 = 1 - CDF(beta; alpha_post, beta_post) at current_missing
        # 这个公式比较复杂，用近似：
        
        # 简化为：遗漏越长，分位数越极端（接近0或1）
        # 如果遗漏很久且均值低 -> 接近0（异常）
        # 如果遗漏很久且均值高 -> 接近1（即将出现）
        
        # 计算当前遗漏期的分位数
        # 用Beta分布的生存函数
        try:
            # P(X > current_missing) using Beta-Binomial predictive
            # 近似：使用后验分布的生存函数
            # 这个近似在遗漏期数较小时比较准确
            if current_missing <= 0:
                return 0.5
            
            # 使用Beta分布的CDF
            # P(p > mean) = 1 - CDF(mean; alpha, beta)
            mean_prob = alpha / (alpha + beta)
            
            # 计算遗漏期数的标准化
            # 假设遗漏期数服从几何分布，均值为1/p
            # 那么 observed_missing 的标准化值 = current_missing * mean_prob
            
            # 用Beta分布计算后验分位数
            # 分位数 = P(p <= mean_prob | data) 的"遗漏加权"
            # 近似为：
            missing_factor = min(current_missing * mean_prob / 10.0, 1.0)
            
            # 后验分位数
            try:
                quantile = beta_dist.cdf(mean_prob, alpha, beta)
            except:
                quantile = 0.5
            
            # 遗漏加权分位数
            # 如果遗漏很久但均值高，分数量向1偏移（即将出现）
            # 如果遗漏很久但均值低，分数量向0偏移（不太可能出现）
            weighted_quantile = quantile + (1 - quantile) * missing_factor if mean_prob > 0.15 else quantile * (1 - missing_factor)
            
            return np.clip(weighted_quantile, 0.0, 1.0)
            
        except Exception:
            return 0.5
    
    def compute_missing_features(self, all_numbers: List[int], 
                                 current_missing: Dict[int, int]) -> np.ndarray:
        """
        计算所有号码的遗漏特征向量
        
        Args:
            all_numbers: 所有可能的号码列表
            current_missing: 每个号码当前的遗漏期数字典
            
        Returns:
            特征矩阵 [n_numbers, n_features]
            每行是一个号码的特征：[expected_prob, missing_quantile, missing_value, posterior_alpha, posterior_beta]
        """
        features = []
        
        for num in all_numbers:
            alpha, beta = self.get_posterior_params(num)
            exp_prob = self.get_expected_prob(num)
            miss = current_missing.get(num, 0)
            miss_quantile = self.get_missing_quantile(num, miss)
            miss_value = self.get_missing_value(num, miss)
            
            features.append([
                exp_prob,       # 后验均值概率
                miss_quantile,  # 贝叶斯遗漏分位数
                miss_value,    # 遗漏加权特征
                alpha,         # 后验α
                beta,          # 后验β
                miss,          # 当前遗漏期数
            ])
        
        return np.array(features)
    
    def get_all_number_probs(self, all_numbers: List[int]) -> Dict[int, float]:
        """
        获取所有号码的出现概率字典
        """
        return {num: self.get_expected_prob(num) for num in all_numbers}


class MissingValueTracker:
    """
    遗漏值跟踪器
    跟踪每个号码自上次出现以来的遗漏期数
    """
    
    def __init__(self, n_front: int = 35, n_back: int = 12):
        self.n_front = n_front
        self.n_back = n_back
        self.last_appeared_ = {}
        self.reset()
    
    def reset(self):
        """重置跟踪器"""
        self.last_appeared_ = {}
        self.current_missing_ = {}
        
        # 初始化所有号码的遗漏为极大值
        for i in range(1, self.n_front + 1):
            self.current_missing_[i] = 0
        for i in range(1, self.n_back + 1):
            self.current_missing_[i] = 0
    
    def update(self, draw: Tuple[List[int], List[int]]):
        """
        更新遗漏值
        draw: (前区号码列表, 后区号码列表)
        """
        front_nums, back_nums = draw
        
        # 增加所有号码的遗漏期数
        for num in self.current_missing_:
            self.current_missing_[num] += 1
        
        # 重置出现的号码的遗漏期数
        for num in front_nums:
            self.current_missing_[num] = 0
            self.last_appeared_[num] = self.last_appeared_.get(num, 0) + 1
        
        for num in back_nums:
            self.current_missing_[num] = 0
            self.last_appeared_[num] = self.last_appeared_.get(num, 0) + 1
    
    def update_batch(self, draws: List[Tuple[List[int], List[int]]]):
        """批量更新"""
        for draw in draws:
            self.update(draw)
    
    def get_current_missing(self) -> Dict[int, int]:
        """获取当前遗漏期数"""
        return self.current_missing_.copy()
    
    def get_missing_vector(self, numbers: List[int]) -> np.ndarray:
        """获取指定号码的遗漏向量"""
        return np.array([self.current_missing_.get(n, 0) for n in numbers])
    
    def get_stats(self) -> Dict:
        """获取遗漏值统计信息"""
        front_missing = [self.current_missing_[i] for i in range(1, self.n_front + 1)]
        back_missing = [self.current_missing_[i] for i in range(1, self.n_back + 1)]
        
        return {
            'front': {
                'mean': np.mean(front_missing),
                'std': np.std(front_missing),
                'max': max(front_missing),
                'min': min(front_missing),
                'missing_vector': front_missing
            },
            'back': {
                'mean': np.mean(back_missing),
                'std': np.std(back_missing),
                'max': max(back_missing),
                'min': min(back_missing),
                'missing_vector': back_missing
            }
        }


class BayesianNumberModel:
    """
    综合贝叶斯号码模型
    整合Beta-Binomial遗漏值模型和共现分析
    """
    
    def __init__(self, n_front: int = 35, n_back: int = 12):
        self.n_front = n_front
        self.n_back = n_back
        self.front_model = BetaBinomialMissing(method='jeffreys')
        self.back_model = BetaBinomialMissing(method='jeffreys')
        self.front_missing_tracker = MissingValueTracker(n_front=n_front)
        self.back_missing_tracker = MissingValueTracker(n_back=n_back)
        
        # 共现统计
        self.front_cooccurrence_ = defaultdict(lambda: defaultdict(int))
        self.back_cooccurrence_ = defaultdict(lambda: defaultdict(int))
    
    def fit(self, draws: List[Tuple[List[int], List[int]]]):
        """
        用历史数据拟合模型
        draws: [(front_nums, back_nums), ...]
        """
        # 更新贝叶斯模型
        for front_nums, back_nums in draws:
            self.front_model.update_batch([front_nums])
            self.back_model.update_batch([back_nums])
        
        # 更新遗漏跟踪器
        self.front_missing_tracker.update_batch(draws)
        self.back_missing_tracker.update_batch(draws)
        
        # 更新共现统计
        for front_nums, _ in draws:
            for i, n1 in enumerate(front_nums):
                for n2 in front_nums[i+1:]:
                    self.front_cooccurrence_[n1][n2] += 1
                    self.front_cooccurrence_[n2][n1] += 1
        
        for _, back_nums in draws:
            for i, n1 in enumerate(back_nums):
                for n2 in back_nums[i+1:]:
                    self.back_cooccurrence_[n1][n2] += 1
                    self.back_cooccurrence_[n2][n1] += 1
    
    def get_front_features(self) -> np.ndarray:
        """获取前区所有号码的特征"""
        all_nums = list(range(1, self.n_front + 1))
        missing = self.front_missing_tracker.get_current_missing()
        return self.front_model.compute_missing_features(all_nums, missing)
    
    def get_back_features(self) -> np.ndarray:
        """获取后区所有号码的特征"""
        all_nums = list(range(1, self.n_back + 1))
        missing = self.back_missing_tracker.get_current_missing()
        return self.back_model.compute_missing_features(all_nums, missing)
    
    def get_cooccurrence_strength(self, num1: int, num2: int, zone: str = 'front') -> float:
        """
        获取两个号码的共现强度
        zone: 'front' 或 'back'
        """
        cooc = self.front_cooccurrence_ if zone == 'front' else self.back_cooccurrence_
        total_appearances = sum(
            1 for front, _ in []  # 这个需要从外部传入
        )
        
        count = cooc.get(num1, {}).get(num2, 0)
        return count
    
    def get_strong_pairs(self, zone: str = 'front', top_n: int = 10) -> List[Tuple[int, int, int]]:
        """
        获取最强的共现对
        返回: [(num1, num2, count), ...]
        """
        cooc = self.front_cooccurrence_ if zone == 'front' else self.back_cooccurrence_
        
        pairs = set()
        for n1 in cooc:
            for n2 in cooc[n1]:
                if n1 < n2:  # 避免重复
                    pairs.add((n1, n2, cooc[n1][n2]))
        
        # 按共现次数排序
        sorted_pairs = sorted(pairs, key=lambda x: -x[2])
        return sorted_pairs[:top_n]


if __name__ == '__main__':
    # 测试代码
    np.random.seed(42)
    
    # 模拟历史数据
    n_draws = 500
    front_draws = []
    for _ in range(n_draws):
        front = sorted(np.random.choice(range(1, 36), 5, replace=False).tolist())
        back = sorted(np.random.choice(range(1, 13), 2, replace=False).tolist())
        front_draws.append((front, back))
    
    # 拟合模型
    model = BayesianNumberModel()
    model.fit(front_draws)
    
    # 获取特征
    front_features = model.get_front_features()
    back_features = model.get_back_features()
    
    print("前区特征形状:", front_features.shape)
    print("后区特征形状:", back_features.shape)
    
    print("\n前区特征示例 (前5个号码):")
    print("号码  后验均值  遗漏分位数  遗漏加权  后验α  后验β  当前遗漏")
    for i in range(5):
        nums = list(range(1, 36))
        f = front_features[i]
        print(f"  {nums[i]:2d}  {f[0]:.4f}   {f[1]:.4f}    {f[2]:.4f}   {f[3]:.2f}  {f[4]:.2f}    {int(f[5])}")
    
    # 获取最强共现对
    print("\n前区最强共现对:")
    pairs = model.get_strong_pairs('front', top_n=5)
    for n1, n2, count in pairs:
        print(f"  {n1}-{n2}: {count}次")
    
    # 遗漏统计
    front_missing = model.front_missing_tracker.get_current_missing()
    back_missing = model.back_missing_tracker.get_current_missing()
    
    print(f"\n前区遗漏: 平均={np.mean(list(front_missing.values())):.1f}, "
          f"最大={max(front_missing.values())}")
    print(f"后区遗漏: 平均={np.mean(list(back_missing.values())):.1f}, "
          f"最大={max(back_missing.values())}")
