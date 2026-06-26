"""
内存有效期检索器模块

实现 ValidityRetrieverProtocol 接口，采用零外部向量库依赖的内存检索方案：
- 使用已有的 SemanticMatcherProtocol 获取 Embedding
- 用 NumPy 矩阵乘法批量计算余弦相似度
- 关键词/日期正则奖励加权
- 低分熔断机制，避免无意义的 LLM 调用

遵循架构规范：
- 实现 Core 层定义的 ValidityRetrieverProtocol 接口
- 通过构造函数接收 SemanticMatcherProtocol（依赖注入）
- 不直接导入 Domain 层或 Application 层
"""

import re
import logging
from typing import List, Optional, Tuple

logger = logging.getLogger(__name__)

# 静态 Query：覆盖合规文档中有效期的核心表达
_VALIDITY_QUERY = "有效期 截止日期 到期时间 长期有效 永久有效"

# 关键词奖励正则：命中时加 +0.20
_KEYWORD_BONUS_PATTERN = re.compile(
    r"有效期|截止|到期|至.*?年|长期|永久",
    re.IGNORECASE,
)

# 日期正则奖励：命中完整日期时再加 +0.15
_DATE_BONUS_PATTERN = re.compile(
    r"\d{4}[年\-/\.]\d{1,2}[月\-/\.]\d{1,2}日?"
)

# 关键词奖励分值
_KEYWORD_BONUS = 0.20

# 完整日期奖励分值
_DATE_BONUS = 0.15


class InMemoryValidityRetriever:
    """
    内存有效期 RAG 检索器

    对文档全文执行：
    1. 文本清洗 + 滑动窗口分块（委托给 ValidityTextChunker）
    2. 静态 Query Embedding 缓存（服务启动后首次 retrieve 时计算一次）
    3. NumPy 批量余弦相似度计算
    4. 关键词/日期正则奖励加权
    5. 低分熔断：全部 Chunk 得分 < circuit_breaker_threshold 时直接返回 (False, [])
    6. Top-K 高分 Chunk 返回
    """

    def __init__(
        self,
        semantic_matcher,  # SemanticMatcherProtocol（避免循环导入，用 Any 接收）
        chunk_size: int = 200,
        chunk_overlap: int = 50,
        top_k: int = 2,
        circuit_breaker_threshold: float = 0.25,
    ):
        """
        初始化检索器

        Args:
            semantic_matcher: 语义匹配器，实现 SemanticMatcherProtocol
            chunk_size: 每个 Chunk 的目标字符数
            chunk_overlap: 相邻 Chunk 的重叠字符数
            top_k: 返回最高分 Chunk 数量
            circuit_breaker_threshold: 熔断阈值，所有 Chunk 综合得分均低于此值时触发熔断
        """
        from .chunker import ValidityTextChunker

        self._matcher = semantic_matcher
        self._chunk_size = chunk_size
        self._chunk_overlap = chunk_overlap
        self._top_k = top_k
        self._circuit_breaker_threshold = circuit_breaker_threshold
        self._chunker = ValidityTextChunker()

        # 静态 Query Embedding 缓存（首次 retrieve 时懒加载）
        self._query_embedding: Optional[List[float]] = None

    async def _get_query_embedding(self) -> List[float]:
        """获取静态 Query 的 Embedding（带缓存）"""
        if self._query_embedding is None:
            self._query_embedding = await self._matcher.get_embedding(_VALIDITY_QUERY)
            logger.debug(
                f"静态 Query Embedding 已缓存，维度={len(self._query_embedding)}"
            )
        return self._query_embedding

    def _compute_bonus(self, text: str) -> Tuple[float, bool]:
        """
        计算关键词/日期奖励分

        Args:
            text: Chunk 文本

        Returns:
            (bonus_score, has_bonus) 元组
        """
        bonus = 0.0
        has_bonus = False

        if _KEYWORD_BONUS_PATTERN.search(text):
            bonus += _KEYWORD_BONUS
            has_bonus = True

        if _DATE_BONUS_PATTERN.search(text):
            bonus += _DATE_BONUS
            has_bonus = True

        return bonus, has_bonus

    @staticmethod
    def _cosine_similarity_numpy(query_vec: List[float], chunk_vecs: List[List[float]]) -> List[float]:
        """
        使用 NumPy 批量计算余弦相似度

        Args:
            query_vec: Query 向量
            chunk_vecs: Chunk 向量列表

        Returns:
            每个 Chunk 对应的余弦相似度列表
        """
        try:
            import numpy as np

            q = np.array(query_vec, dtype=np.float32)
            c = np.array(chunk_vecs, dtype=np.float32)  # shape: (N, D)

            # 矩阵乘法：(N, D) @ (D,) → (N,)
            dots = c @ q

            # 归一化
            q_norm = np.linalg.norm(q)
            c_norms = np.linalg.norm(c, axis=1)

            # 避免除以零
            denominators = c_norms * q_norm
            denominators = np.where(denominators == 0, 1e-9, denominators)

            similarities = dots / denominators
            return similarities.tolist()

        except ImportError:
            # numpy 不可用时回退到纯 Python（不影响正确性，仅性能略差）
            logger.warning("numpy 不可用，回退到纯 Python 余弦相似度计算")
            results = []
            q_norm = sum(x ** 2 for x in query_vec) ** 0.5
            for vec in chunk_vecs:
                dot = sum(a * b for a, b in zip(query_vec, vec))
                v_norm = sum(x ** 2 for x in vec) ** 0.5
                denom = q_norm * v_norm
                results.append(dot / denom if denom > 0 else 0.0)
            return results

    async def retrieve(
        self, text: str, top_k: int = 2
    ) -> Tuple[bool, list]:
        """
        检索与有效期最相关的 Chunk

        流程：
        1. 文本清洗
        2. 滑动窗口分块
        3. 获取静态 Query Embedding（带缓存）
        4. 批量计算 Chunk Embedding 并做矩阵余弦相似度
        5. 关键词/日期正则加权
        6. 熔断判断
        7. 返回 Top-K

        Args:
            text: 文档全文
            top_k: 返回 Chunk 数量（覆盖构造函数默认值）

        Returns:
            (has_validity, chunks):
              - (False, []) 触发熔断
              - (True, List[RetrievedChunk]) 返回高分 Chunk
        """
        from ...core.interfaces import RetrievedChunk

        effective_top_k = top_k if top_k > 0 else self._top_k

        # 1. 文本清洗
        cleaned = self._chunker.clean(text)
        if not cleaned:
            logger.debug("文档清洗后为空，触发熔断")
            return False, []

        # 2. 滑动窗口分块
        chunks_raw = self._chunker.chunk(
            cleaned,
            chunk_size=self._chunk_size,
            overlap=self._chunk_overlap,
        )

        if not chunks_raw:
            logger.debug("分块结果为空，触发熔断")
            return False, []

        # 3. 获取静态 Query Embedding（缓存）
        try:
            query_emb = await self._get_query_embedding()
        except Exception as e:
            logger.warning(f"Query Embedding 获取失败，触发熔断: {e}")
            return False, []

        # 4. 批量获取 Chunk Embedding
        chunk_texts = [ct for ct, _ in chunks_raw]
        chunk_embs: List[List[float]] = []

        for chunk_text in chunk_texts:
            try:
                emb = await self._matcher.get_embedding(chunk_text)
                chunk_embs.append(emb)
            except Exception as e:
                logger.warning(f"Chunk Embedding 获取失败，使用零向量: {e}")
                # 用零向量占位，不影响其他 Chunk
                chunk_embs.append([0.0] * len(query_emb))

        # 5. 批量余弦相似度
        semantic_scores = self._cosine_similarity_numpy(query_emb, chunk_embs)

        # 6. 关键词/日期奖励加权 + 构建 RetrievedChunk 列表
        scored_chunks = []
        for i, ((chunk_text, start_pos), sem_score) in enumerate(
            zip(chunks_raw, semantic_scores)
        ):
            bonus, has_bonus = self._compute_bonus(chunk_text)
            total_score = float(sem_score) + bonus
            scored_chunks.append(
                RetrievedChunk(
                    text=chunk_text,
                    score=total_score,
                    start_pos=start_pos,
                    has_keyword_bonus=has_bonus,
                )
            )

        # 7. 熔断判断：所有 Chunk 得分均低于阈值
        max_score = max((c.score for c in scored_chunks), default=0.0)
        if max_score < self._circuit_breaker_threshold:
            logger.info(
                f"熔断触发：最高得分 {max_score:.3f} < 阈值 {self._circuit_breaker_threshold}，"
                f"文档可能无有效期信息"
            )
            return False, []

        # 8. 排序并返回 Top-K
        scored_chunks.sort(key=lambda c: c.score, reverse=True)
        top_chunks = scored_chunks[:effective_top_k]

        logger.debug(
            f"RAG 检索完成：共 {len(scored_chunks)} 个 Chunk，"
            f"最高分={max_score:.3f}，返回 Top-{len(top_chunks)}"
        )
        return True, top_chunks
