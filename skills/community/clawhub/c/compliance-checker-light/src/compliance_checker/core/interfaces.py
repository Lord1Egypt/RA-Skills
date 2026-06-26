"""
Core 层接口定义

定义所有抽象接口（Protocol），实现依赖倒置原则。
Domain 层只依赖这些接口，Infrastructure 层实现这些接口。

注意：此文件只包含类型提示，不包含具体实现逻辑。
"""

from dataclasses import dataclass
from typing import Protocol, List, Dict, Any, Optional, Tuple, runtime_checkable


@dataclass
class RetrievedChunk:
    """
    RAG 检索结果块

    表示从文档中检索出的一个文本片段及其相关得分信息。
    供 ValidityRetrieverProtocol 返回，由 TimelinessChecker 消费。
    """

    text: str                   # Chunk 文本内容
    score: float                # 综合得分（语义相似度 + 关键词奖励）
    start_pos: int              # 在原文中的起始字符位置
    has_keyword_bonus: bool     # 是否命中关键词/日期正则加权


@runtime_checkable
class SemanticMatcherProtocol(Protocol):
    """
    语义匹配器接口

    用于计算文本相似度，支持文档名称的语义匹配。
    Infrastructure 层实现此接口（如 LLMSemanticMatcher）。
    """

    async def get_similarity(self, text1: str, text2: str) -> float:
        """
        计算两个文本的语义相似度

        Args:
            text1: 第一个文本
            text2: 第二个文本

        Returns:
            相似度分数 (0-1)
        """
        ...

    async def get_embedding(self, text: str) -> List[float]:
        """
        获取文本的嵌入向量

        Args:
            text: 输入文本

        Returns:
            嵌入向量（浮点数列表）
        """
        ...

    async def find_best_match(self, text: str, candidates: List[str]) -> tuple:
        """
        从候选列表中找到最佳匹配

        Args:
            text: 待匹配文本
            candidates: 候选文本列表

        Returns:
            (最佳匹配文本, 相似度分数)
        """
        ...


@runtime_checkable
class DocumentParserProtocol(Protocol):
    """
    文档解析器接口

    用于解析各种格式的文档（PDF、Word等）。
    Infrastructure 层实现此接口（如 PDFParser、DocxParser）。
    """

    def parse(self, file_path: str) -> "Document":
        """
        解析文档文件

        Args:
            file_path: 文档文件路径

        Returns:
            Document 对象

        Raises:
            FileNotFoundError: 文件不存在
            ValueError: 不支持的文件格式
        """
        ...


@runtime_checkable
class VisualCheckerProtocol(Protocol):
    """
    视觉检查器接口

    用于检测文档中的印章、签名等视觉元素。
    Infrastructure 层实现此接口（如 QwenVLClient）。
    """

    def is_available(self) -> bool:
        """
        检查视觉检查器是否可用

        Returns:
            True 如果 API 已配置且可用
        """
        ...

    async def detect_seal(self, image_path: str, context: Optional[str] = None) -> Dict[str, Any]:
        """
        检测图片中的公章

        Args:
            image_path: 图片文件路径
            context: 上下文信息（如文档类型）

        Returns:
            {
                "success": bool,
                "found": bool,
                "confidence": float,
                "reasoning": str,
                "location": str
            }
        """
        ...

    async def detect_signature(
        self, image_path: str, context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        检测图片中的签名

        Args:
            image_path: 图片文件路径
            context: 上下文信息

        Returns:
            检测结果字典
        """
        ...


@runtime_checkable
class LLMClientProtocol(Protocol):
    """
    LLM 客户端接口

    用于调用大语言模型生成文本或结构化输出。
    Infrastructure 层实现此接口（如 LLMClient）。
    """

    async def complete(self, prompt: str, temperature: float = 0.3, max_tokens: int = 2000) -> str:
        """
        调用 LLM 完成文本生成

        Args:
            prompt: 提示词
            temperature: 温度参数 (0-1)
            max_tokens: 最大生成 token 数

        Returns:
            生成的文本内容
        """
        ...

    async def generate_yaml(self, user_description: str, temperature: float = 0.3) -> dict:
        """
        将自然语言描述转换为 YAML 结构

        Args:
            user_description: 用户描述
            temperature: 温度参数

        Returns:
            解析后的 YAML 字典
        """
        ...


@runtime_checkable
class OCREngineProtocol(Protocol):
    """
    OCR 引擎接口

    用于识别扫描件中的文字。
    Infrastructure 层实现此接口。
    """

    def recognize_pdf(self, file_path: str, dpi: int = 200) -> List[tuple]:
        """
        识别 PDF 文件中的文字

        Args:
            file_path: PDF 文件路径
            dpi: 渲染分辨率

        Returns:
            [(page_num, ocr_text), ...] 列表
        """
        ...

    def recognize_image(self, image_path: str) -> str:
        """
        识别图片中的文字

        Args:
            image_path: 图片文件路径

        Returns:
            识别出的文字
        """
        ...


@runtime_checkable
class ValidityRetrieverProtocol(Protocol):
    """
    有效期 RAG 检索器接口

    对文档全文执行内存向量检索，返回与有效期最相关的 Chunk 列表。
    Infrastructure 层实现此接口（如 InMemoryValidityRetriever）。
    """

    async def retrieve(
        self, text: str, top_k: int = 2
    ) -> Tuple[bool, List[RetrievedChunk]]:
        """
        检索与有效期最相关的 Chunk。

        Args:
            text: 待检索的文档全文
            top_k: 返回最高得分的 Chunk 数量

        Returns:
            (has_validity, chunks):
              - has_validity=False 触发熔断，文档中无有效期信息，调用方应跳过 LLM
              - has_validity=True  返回 top_k 个高分 RetrievedChunk
        """
        ...


@runtime_checkable
class PDFConverterProtocol(Protocol):
    """
    PDF 转换器接口

    用于将 PDF 文件转换为图片格式，以便视觉大模型处理。
    Infrastructure 层实现此接口（如 PyMuPDFConverter）。
    """

    async def convert_to_images(self, file_path_or_bytes: str | bytes) -> List[bytes]:
        """
        将 PDF 转换为图片字节流列表（每页对应一张图）

        Args:
            file_path_or_bytes: PDF 文件路径或字节流

        Returns:
            图片字节流列表（PNG 格式），每页对应一个 bytes 对象
        """
        ...
