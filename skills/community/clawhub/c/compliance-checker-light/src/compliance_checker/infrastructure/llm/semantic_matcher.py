"""
语义匹配器模块

使用嵌入模型计算文本相似度，实现 SemanticMatcherProtocol 接口。
"""

import hashlib
import logging
import os
from typing import Dict, List, Optional

from ...core.interfaces import SemanticMatcherProtocol

logger = logging.getLogger(__name__)


class LLMSemanticMatcher(SemanticMatcherProtocol):
    """
    语义匹配器 - 使用嵌入模型计算文件名相似度

    实现 SemanticMatcherProtocol 接口，支持依赖注入。
    配置通过构造函数传入，不直接访问环境变量。
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
        timeout: float = 30.0,
        max_retries: int = 3,
    ):
        """
        初始化语义匹配器

        Args:
            api_key: API 密钥（可选，默认从环境变量读取）
            base_url: API 基础 URL（可选）
            model: 嵌入模型名称（可选）
            timeout: 请求超时时间（秒）
            max_retries: 最大重试次数
        """
        self._api_key = api_key
        self._base_url = base_url
        self._model = model or "text-embedding-v3"
        self._timeout = timeout
        self._max_retries = max_retries

        self._client = None
        self._cache: Dict[str, List[float]] = {}

    def _get_client(self):
        """延迟加载嵌入模型客户端"""
        if self._client is None:
            try:
                import openai

                # 如果未提供 api_key，从环境变量读取
                api_key = self._api_key or os.getenv("EMBED_API_KEY") or os.getenv("LLM_API_KEY")
                base_url = (
                    self._base_url
                    or os.getenv("EMBED_BASE_URL")
                    or os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
                )

                if not api_key:
                    raise ValueError("未配置 EMBED_API_KEY 或 LLM_API_KEY")

                self._client = openai.AsyncOpenAI(
                    api_key=api_key,
                    base_url=base_url,
                    timeout=self._timeout,
                    max_retries=self._max_retries,
                )
                logger.debug(f"嵌入模型客户端初始化成功: {base_url}")
            except Exception as e:
                logger.debug(f"嵌入模型客户端初始化失败: {e}")
                raise
        return self._client

    async def get_embedding(self, text: str) -> List[float]:
        """
        获取文本的嵌入向量

        Args:
            text: 输入文本

        Returns:
            嵌入向量（浮点数列表）
        """
        # 检查缓存
        if text in self._cache:
            return self._cache[text]

        try:
            client = self._get_client()
            response = await client.embeddings.create(model=self._model, input=text)
            embedding = response.data[0].embedding
            self._cache[text] = embedding
            return embedding
        except Exception as e:
            logger.debug(f"嵌入 API 调用失败，使用备用方法: {e}")
            # 备用：使用简单的字符级特征
            return self._simple_embedding(text)

    def _simple_embedding(self, text: str) -> List[float]:
        """
        简单的字符级嵌入（备用方法）

        基于字符 n-gram 频率的简化嵌入
        """
        text = text.lower()
        # 使用字符 trigram 作为特征
        features = {}
        for i in range(len(text) - 2):
            trigram = text[i : i + 3]
            features[trigram] = features.get(trigram, 0) + 1

        # 转换为固定长度的向量
        vector = [0.0] * 128
        for trigram, count in features.items():
            idx = int(hashlib.md5(trigram.encode()).hexdigest(), 16) % 128
            vector[idx] = count / len(text)

        # 归一化
        norm = sum(x**2 for x in vector) ** 0.5
        if norm > 0:
            vector = [x / norm for x in vector]

        return vector

    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """计算余弦相似度"""
        dot = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = sum(a**2 for a in vec1) ** 0.5
        norm2 = sum(b**2 for b in vec2) ** 0.5
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return dot / (norm1 * norm2)

    async def get_similarity(self, text1: str, text2: str) -> float:
        """
        计算两个文本的语义相似度

        Args:
            text1: 第一个文本
            text2: 第二个文本

        Returns:
            相似度分数 (0-1)
        """
        try:
            emb1 = await self.get_embedding(text1)
            emb2 = await self.get_embedding(text2)
            return self._cosine_similarity(emb1, emb2)
        except Exception as e:
            logger.warning(f"语义相似度计算失败: {e}")
            return 0.0

    async def find_best_match(self, text: str, candidates: List[str]) -> tuple:
        """
        从候选列表中找到最佳匹配

        Args:
            text: 待匹配文本
            candidates: 候选文本列表

        Returns:
            (最佳匹配文本, 相似度分数)
        """
        if not candidates:
            return None, 0.0

        try:
            text_embedding = await self.get_embedding(text)

            best_match = None
            best_similarity = 0.0

            for candidate in candidates:
                candidate_embedding = await self.get_embedding(candidate)
                similarity = self._cosine_similarity(text_embedding, candidate_embedding)
                if similarity > best_similarity:
                    best_similarity = similarity
                    best_match = candidate

            return best_match, best_similarity
        except Exception as e:
            logger.warning(f"最佳匹配查找失败: {e}")
            return None, 0.0

    async def calculate_similarity(self, file_name: str, target_names: List[str]) -> float:
        """
        计算文件名与目标名称列表的最高相似度

        Args:
            file_name: 实际文件名
            target_names: 清单名称及别名列表

        Returns:
            最高相似度分数 (0-1)
        """
        if not target_names:
            return 0.0

        max_similarity = 0.0
        for target in target_names:
            similarity = await self.get_similarity(file_name, target)
            max_similarity = max(max_similarity, similarity)

        return max_similarity
