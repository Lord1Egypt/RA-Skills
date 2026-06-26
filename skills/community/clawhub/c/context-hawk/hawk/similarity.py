"""
similarity.py — SimHash 去重 + MMR 多样性召回

SimHash: 快速判断两段记忆是否重复（海明距离）
MMR: 最大边缘相关性 — 召回时既相关又不重复
"""

import hashlib
import struct
from typing import List, Tuple


class SimHash:
    """
    SimHash 实现 — 用于自动去重

    步骤：
    1. 对文本分词，计算每个词的 hash
    2. 合并 hash 向量（相同位相加）
    3. 降维：>0 → 1, <=0 → 0
    4. 得到固定长度指纹
    5. 两指纹比较，海明距离 < k 则认为重复
    """

    def __init__(self, hash_bits: int = 64):
        self.hash_bits = hash_bits

    def _tokenize(self, text: str) -> List[str]:
        """简单分词：按空格/标点拆分，转小写"""
        import re
        text = re.sub(r'[^\w\s]', ' ', text.lower())
        return [w for w in text.split() if len(w) >= 2]

    def _hash(self, token: str) -> int:
        """单词 hash → 64位整数"""
        h = hashlib.md5(token.encode('utf-8')).digest()
        return struct.unpack('>q', h[:8])[0]

    def compute(self, text: str) -> int:
        """计算文本的 SimHash 指纹"""
        tokens = self._tokenize(text)
        if not tokens:
            return 0

        # 合并向量
        v = [0] * self.hash_bits
        for token in tokens:
            h = self._hash(token)
            for i in range(self.hash_bits):
                bit = (h >> i) & 1
                v[i] += 1 if bit else -1

        # 降维成 64 位指纹
        fingerprint = 0
        for i in range(self.hash_bits):
            if v[i] > 0:
                fingerprint |= (1 << i)
        return fingerprint

    def hamming_distance(self, hash1: int, hash2: int) -> int:
        """计算两个指纹的海明距离"""
        xor = hash1 ^ hash2
        return bin(xor).count('1')

    def is_duplicate(self, text1: str, text2: str, threshold: int = 3) -> bool:
        """
        判断两段文本是否重复
        threshold: 海明距离阈值（默认3）→ 距离<3认为重复
        """
        h1 = self.compute(text1)
        h2 = self.compute(text2)
        return self.hamming_distance(h1, h2) <= threshold

    def find_duplicates(self, texts: List[str], threshold: int = 3) -> List[Tuple[int, int]]:
        """
        在一组文本中找出所有重复对
        返回: [(index1, index2), ...]
        """
        hashes = [self.compute(t) for t in texts]
        duplicates = []
        for i in range(len(hashes)):
            for j in range(i + 1, len(hashes)):
                if self.hamming_distance(hashes[i], hashes[j]) <= threshold:
                    duplicates.append((i, j))
        return duplicates


class MMR:
    """
    Maximal Marginal Relevance (MMR) — 最大边缘相关性

    用于记忆召回时：既保证相关性，又保证多样性

    MMR 公式：
    MMR = argmax[ λ * Sim(q, doc) - (1-λ) * max(Sim(doc, already_selected)) ]

    其中：
    - q = 查询向量
    - doc = 待选文档
    - λ = 多样性系数（0.7 表示 70% 相关性，30% 多样性）
    - 已选文档的多样性惩罚项：选择与已选文档最相似的文档
    """

    def __init__(self, lambda_param: float = 0.7):
        """
        Args:
            lambda_param: 0.7 → 70%相关性 + 30%多样性
                         调高 → 更相关，调低 → 更多样
        """
        self.lambda_param = lambda_param

    def score(
        self,
        query_vector: List[float],
        doc_vector: List[float],
        selected_vectors: List[List[float]],
    ) -> float:
        """
        计算单个文档的 MMR 分数
        """
        import math

        # 相关性分数：query 和 doc 的余弦相似度
        def cosine_sim(a: List[float], b: List[float]) -> float:
            dot = sum(x * y for x, y in zip(a, b))
            norm_a = math.sqrt(sum(x * x for x in a))
            norm_b = math.sqrt(sum(x * x for x in b))
            if norm_a == 0 or norm_b == 0:
                return 0.0
            return dot / (norm_a * norm_b)

        relevance = cosine_sim(query_vector, doc_vector)

        if not selected_vectors:
            # 第一个文档，直接用相关性
            return self.lambda_param * relevance

        # 多样性惩罚：与已选文档的最大相似度
        max_sim_to_selected = max(
            cosine_sim(doc_vector, sv) for sv in selected_vectors
        )

        # MMR 分数
        mmr_score = (
            self.lambda_param * relevance
            - (1 - self.lambda_param) * max_sim_to_selected
        )
        return mmr_score

    def select(
        self,
        query_vector: List[float],
        doc_vectors: List[List[float]],
        top_k: int = 5,
    ) -> List[int]:
        """
        从 doc_vectors 中选出 top_k 个既相关又多样的文档

        Args:
            query_vector: 查询向量
            doc_vectors: 所有候选文档的向量列表
            top_k: 选择数量

        Returns:
            选中的文档索引列表
        """
        selected_indices = []
        selected_vectors = []

        for _ in range(min(top_k, len(doc_vectors))):
            best_score = float('-inf')
            best_idx = -1

            for i, doc_vec in enumerate(doc_vectors):
                if i in selected_indices:
                    continue
                score = self.score(query_vector, doc_vec, selected_vectors)
                if score > best_score:
                    best_score = score
                    best_idx = i

            if best_idx != -1:
                selected_indices.append(best_idx)
                selected_vectors.append(doc_vectors[best_idx])

        return selected_indices
