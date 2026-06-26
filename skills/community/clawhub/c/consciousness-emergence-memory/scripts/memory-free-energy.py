#!/usr/bin/env python3
"""
自由能框架 - 基于主动推理的智能记忆系统

基于自由能原理（Free Energy Principle, FEP）：
- 主动推理（Active Inference）
- 预测编码（Predictive Coding）
- 变分推断（Variational Inference）
- 惊奇最小化（Surprise Minimization）

核心思想：
智能体通过最小化自由能来维持稳态
F = -ln p(o|m) - KL[q(s)||p(s|m)]

其中：
- o: 观测
- m: 模型
- s: 状态
- q: 近似后验
- p: 真实后验
"""
import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from pathlib import Path
import json
import math


@dataclass
class GenerativeModel:
    """生成模型"""
    prior: np.ndarray  # 先验分布 p(s)
    likelihood: np.ndarray  # 似然 p(o|s)
    transition: np.ndarray  # 状态转移 p(s_t|s_{t-1})


@dataclass
class VariationalPosterior:
    """变分后验 q(s)"""
    mean: np.ndarray
    variance: np.ndarray


@dataclass
class Prediction:
    """预测结果"""
    next_state: np.ndarray
    next_observation: np.ndarray
    uncertainty: float
    confidence: float


class FreeEnergyFramework:
    """
    自由能框架 - 主动推理记忆系统

    核心算法：
    1. 预测编码：自顶向下的预测 vs 自底向上的误差
    2. 变分推断：近似后验更新
    3. 主动推理：通过行动减少自由能
    4. 惊奇最小化：学习更好的模型
    """

    def __init__(self, workspace: str = ".", state_dim: int = 50, obs_dim: int = 20):
        self.workspace = Path(workspace)
        self.state_dim = state_dim
        self.obs_dim = obs_dim

        # 初始化生成模型
        self.model = self._initialize_model()

        # 状态历史
        self.state_history: List[np.ndarray] = []

        # 自由能历史
        self.free_energy_history: List[float] = []

    def _initialize_model(self) -> GenerativeModel:
        """初始化生成模型"""
        # 先验：均匀分布
        prior = np.ones(self.state_dim) / self.state_dim

        # 似然：高斯分布（简化为随机矩阵）
        likelihood = np.random.randn(self.state_dim, self.obs_dim)

        # 转移：随机矩阵
        transition = np.random.randn(self.state_dim, self.state_dim)

        # 归一化
        transition = softmax_rows(transition)

        return GenerativeModel(prior=prior, likelihood=likelihood, transition=transition)

    def predict_next_state(self, current_state: np.ndarray) -> Prediction:
        """
        预测下一个状态

        使用状态转移模型进行预测
        p(s_{t+1}|s_t) = Σ p(s_{t+1}|s_t, s_{t-1}) p(s_{t-1}|s_t)
        """
        # 线性预测（简化）
        next_state = np.dot(self.model.transition, current_state)

        # 预测观测
        next_observation = np.dot(self.model.likelihood.T, next_state)

        # 不确定性（熵）
        uncertainty = -np.sum(next_state * np.log(next_state + 1e-10))

        # 置信度
        confidence = 1.0 - min(1.0, uncertainty / np.log(self.state_dim))

        return Prediction(
            next_state=next_state,
            next_observation=next_observation,
            uncertainty=uncertainty,
            confidence=confidence
        )

    def calculate_free_energy(self, observation: np.ndarray,
                               posterior: VariationalPosterior) -> float:
        """
        计算变分自由能

        F = -ln p(o|m) - KL[q(s)||p(s|m)]

        自由能 = 负对数似然 - KL 散度
        """
        # 负对数似然：-ln p(o|m)
        # p(o|m) = Σ p(o|s) p(s)
        marginal_likelihood = np.sum(
            np.dot(self.model.likelihood.T, posterior.mean) * observation
        )
        log_likelihood = np.log(marginal_likelihood + 1e-10)

        # KL 散度：KL[q(s)||p(s|m)]
        # p(s|m) ∝ p(o|s) p(s)（贝叶斯更新）
        prior_times_likelihood = self.model.prior * np.dot(self.model.likelihood, observation)
        true_posterior = prior_times_likelihood / np.sum(prior_times_likelihood + 1e-10)

        kl_divergence = self._calculate_kl_divergence(
            posterior.mean,
            true_posterior
        )

        # 自由能
        free_energy = -log_likelihood - kl_divergence

        return free_energy

    def _calculate_kl_divergence(self, p: np.ndarray, q: np.ndarray) -> float:
        """
        计算 KL 散度

        KL(p||q) = Σ p(x) log(p(x)/q(x))
        """
        kl = np.sum(p * np.log((p + 1e-10) / (q + 1e-10)))
        return kl

    def variational_inference(self, observation: np.ndarray,
                              num_iterations: int = 10) -> VariationalPosterior:
        """
        变分推断：更新后验分布

        最小化自由能：q*(s) = argmin_q F(q)
        """
        # 初始化后验
        mean = self.model.prior.copy()
        variance = np.ones(self.state_dim) * 0.1

        # 迭代优化（简化：梯度下降）
        for _ in range(num_iterations):
            # 计算梯度
            gradient = self._compute_gradient(mean, observation)

            # 更新
            mean -= 0.1 * gradient

            # 约束：非负、归一化
            mean = np.maximum(mean, 0)
            mean = mean / np.sum(mean)

        return VariationalPosterior(mean=mean, variance=variance)

    def _compute_gradient(self, posterior_mean: np.ndarray,
                         observation: np.ndarray) -> np.ndarray:
        """
        计算自由能梯度

        用于变分推断的梯度下降
        """
        # 简化：基于预测误差
        predicted_obs = np.dot(self.model.likelihood.T, posterior_mean)
        error = observation - predicted_obs

        # 梯度
        gradient = -np.dot(self.model.likelihood, error)

        return gradient

    def update_model(self, observation: np.ndarray,
                     action: Optional[np.ndarray] = None):
        """
        更新生成模型（学习）

        使用观测数据更新先验、似然和转移模型
        """
        # 更新先验：基于当前后验
        # p(s) ← q(s)
        self.model.prior = self.model.prior * 0.9 + self.model.prior * 0.1  # 缓慢更新

        # 更新似然：p(o|s)
        # 使用 Hebbian 学习
        if action is not None:
            # 强化学习：奖励增加相关连接
            self.model.likelihood += 0.01 * np.outer(self.model.prior, observation)

        # 归一化
        self.model.prior = self.model.prior / np.sum(self.model.prior)
        self.model.likelihood = self.model.likelihood / np.sum(self.model.likelihood, axis=1, keepdims=True)

    def active_inference(self, goal_observation: np.ndarray,
                         num_steps: int = 10) -> List[np.ndarray]:
        """
        主动推理：通过行动实现目标

        选择能够最小化期望自由能的行动
        """
        actions = []

        for step in range(num_steps):
            # 当前预测
            prediction = self.predict_next_state(self.model.prior)

            # 计算与目标的距离
            distance = np.linalg.norm(
                prediction.next_observation - goal_observation
            )

            # 如果距离足够小，停止
            if distance < 0.1:
                break

            # 选择行动（简化：向目标移动）
            action = (goal_observation - prediction.next_observation) * 0.5
            actions.append(action)

            # 更新模型
            self.update_model(goal_observation, action)

        return actions

    def surprise_minimization(self, observations: List[np.ndarray]):
        """
        惊奇最小化：学习更好的模型

        惊奇 = -ln p(o|m)
        通过更新模型最小化惊奇
        """
        for obs in observations:
            # 计算当前惊奇
            posterior = self.variational_inference(obs)
            free_energy = self.calculate_free_energy(obs, posterior)

            self.free_energy_history.append(free_energy)

            # 更新模型（降低惊奇）
            self.update_model(obs)

    def encode_predictive_memory(self, text: str) -> np.ndarray:
        """
        编码文本为预测记忆

        将文本映射到状态空间，支持预测推理
        """
        # 简化：使用词频作为特征
        words = text.lower().split()
        feature_dim = min(len(words), self.obs_dim)

        observation = np.zeros(self.obs_dim)
        for i, word in enumerate(words[:feature_dim]):
            # 使用词的 hash 作为索引
            idx = hash(word) % self.obs_dim
            observation[idx] += 1

        # 归一化
        if np.sum(observation) > 0:
            observation = observation / np.sum(observation)

        return observation

    def retrieve_by_prediction(self, query: str,
                               top_k: int = 5) -> List[Tuple[str, float]]:
        """
        基于预测编码检索记忆

        不是匹配查询，而是预测查询的"隐藏状态"
        """
        # 编码查询为观测
        query_obs = self.encode_predictive_memory(query)

        # 计算与存储观测的预测误差
        retrieval_scores = []

        # 这里应该从存储中读取历史观测
        # 简化：使用当前先验
        predicted_obs = np.dot(self.model.likelihood.T, self.model.prior)

        # 计算预测误差（自由能）
        error = query_obs - predicted_obs
        free_energy = np.sum(error ** 2)

        retrieval_scores.append(("current_state", free_energy))

        # 返回 Top-k
        retrieval_scores.sort(key=lambda x: x[1])
        return retrieval_scores[:top_k]

    def get_memory_uncertainty(self, memory_text: str) -> float:
        """
        获取记忆的不确定性

        基于预测编码的置信度
        """
        obs = self.encode_predictive_memory(memory_text)
        posterior = self.variational_inference(obs)

        # 计算后验熵
        entropy = -np.sum(posterior.mean * np.log(posterior.mean + 1e-10))

        return entropy

    def memory_importance_ranking(self, memories: List[Dict]) -> List[Dict]:
        """
        基于自由能原理排序记忆重要性

        重要性 = 1 / (自由能 + 随机性)

        自由能越小，记忆越重要
        """
        ranked = []

        for mem in memories:
            obs = self.encode_predictive_memory(mem["content"])
            posterior = self.variational_inference(obs)
            free_energy = self.calculate_free_energy(obs, posterior)

            # 重要性评分
            importance = 1.0 / (free_energy + 1.0)

            mem_copy = mem.copy()
            mem_copy["importance_fep"] = importance
            mem_copy["free_energy"] = free_energy
            ranked.append(mem_copy)

        # 按重要性降序排序
        ranked.sort(key=lambda x: x["importance_fep"], reverse=True)

        return ranked


def softmax_rows(matrix: np.ndarray) -> np.ndarray:
    """对矩阵的每行进行 softmax"""
    return np.exp(matrix) / np.sum(np.exp(matrix), axis=1, keepdims=True)


def main():
    """命令行接口"""
    import argparse

    parser = argparse.ArgumentParser(description="自由能框架 - 主动推理记忆系统")
    parser.add_argument("action", choices=["predict", "infer", "rank", "encode"])
    parser.add_argument("--text", help="文本内容")
    parser.add_argument("--workspace", default=".", help="工作目录")

    args = parser.parse_args()

    fep = FreeEnergyFramework(args.workspace)

    if args.action == "predict":
        if not args.text:
            print("错误: 需要指定 --text")
            return

        obs = fep.encode_predictive_memory(args.text)
        prediction = fep.predict_next_state(fep.model.prior)

        print("🔮 预测结果")
        print(f"下一个状态维度: {prediction.next_state.shape}")
        print(f"不确定性: {prediction.uncertainty:.4f}")
        print(f"置信度: {prediction.confidence:.4f}")

    elif args.action == "infer":
        if not args.text:
            print("错误: 需要指定 --text")
            return

        obs = fep.encode_predictive_memory(args.text)
        posterior = fep.variational_inference(obs)
        free_energy = fep.calculate_free_energy(obs, posterior)

        print("🧠 变分推断")
        print(f"后验均值: {posterior.mean[:5]}...")
        print(f"自由能: {free_energy:.4f}")

    elif args.action == "rank":
        # 示例：排序记忆重要性
        memories = [
            {"content": "用户偏好暗色主题"},
            {"content": "使用 React 作为前端框架"},
            {"content": "项目需要在周五前完成"},
        ]

        ranked = fep.memory_importance_ranking(memories)

        print("📊 记忆重要性排序（基于自由能）")
        for mem in ranked:
            print(f"  {mem['content']}")
            print(f"    重要性: {mem['importance_fep']:.4f}, 自由能: {mem['free_energy']:.4f}")

    elif args.action == "encode":
        if not args.text:
            print("错误: 需要指定 --text")
            return

        obs = fep.encode_predictive_memory(args.text)
        print(f"✓ 编码结果: {obs.shape}")


if __name__ == "__main__":
    main()
