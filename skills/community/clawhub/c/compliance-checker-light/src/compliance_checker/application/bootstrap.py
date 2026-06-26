"""
Application 层启动器模块

提供依赖注入容器 Container 和工厂函数 create_container()。
CLI 命令模块通过 create_container() 获取所需的 Infrastructure 服务。

架构原则：
- 环境变量读取（os.getenv）属于 I/O 操作，归属于 Infrastructure 层
- Application 层从 Infrastructure 层导入配置，注入到 Domain 层
"""

import logging
from typing import Optional

from ..infrastructure.llm.client import LLMClient
from ..infrastructure.llm.ocr_engine import create_ocr_engine, OCREngineProtocol
from ..infrastructure.config.settings import CheckerConfig
from ..infrastructure.visual.qwen_client import QwenVLClient
from ..infrastructure.converter.pdf_converter import PyMuPDFConverter
from ..infrastructure.rag.validity_retriever import InMemoryValidityRetriever

logger = logging.getLogger(__name__)


class Container:
    """
    依赖注入容器

    管理所有 Infrastructure 层客户端实例的生命周期，
    并在 Application 层组装依赖关系。
    """

    def __init__(self, config: CheckerConfig):
        """
        初始化容器

        Args:
            config: 检查器配置
        """
        self.config = config
        self._llm_client: Optional[LLMClient] = None
        self._semantic_matcher: Optional["LLMSemanticMatcher"] = None
        self._visual_client: Optional[QwenVLClient] = None
        self._ocr_engine: Optional[OCREngineProtocol] = None
        self._pdf_converter: Optional[PyMuPDFConverter] = None
        self._validity_retriever: Optional[InMemoryValidityRetriever] = None

    @property
    def llm_client(self) -> Optional[LLMClient]:
        """获取 LLM 客户端实例（延迟加载）"""
        if self._llm_client is None:
            if self.config.llm_config.api_key:
                try:
                    self._llm_client = LLMClient(self.config.llm_config)
                    logger.info(f"LLM 客户端初始化成功: {self.config.llm_config.model}")
                except Exception as e:
                    logger.warning(f"LLM 客户端初始化失败: {e}")
            else:
                logger.warning("未配置 LLM_API_KEY，LLM 功能将不可用")
        return self._llm_client

    @property
    def semantic_matcher(self) -> Optional["LLMSemanticMatcher"]:
        """获取语义匹配器实例（延迟加载）"""
        if self._semantic_matcher is None and self.config.use_semantic:
            try:
                # 延迟导入，避免循环依赖
                from ..infrastructure.llm.semantic_matcher import LLMSemanticMatcher

                self._semantic_matcher = LLMSemanticMatcher(
                    api_key=self.config.embed_api_key,
                    base_url=self.config.embed_base_url,
                    model=self.config.embed_model,
                    timeout=self.config.embed_timeout,
                    max_retries=self.config.embed_max_retries,
                )
                logger.info(f"语义匹配器初始化成功: {self.config.embed_model}")
            except Exception as e:
                logger.warning(f"语义匹配器初始化失败: {e}")
        return self._semantic_matcher

    @property
    def visual_client(self) -> Optional[QwenVLClient]:
        """获取视觉客户端实例（延迟加载）"""
        if self._visual_client is None and self.config.visual_enabled:
            try:
                self._visual_client = QwenVLClient(
                    api_key=self.config.vision_api_key,
                    base_url=self.config.vision_base_url,
                    model=self.config.vision_model,
                )
                if self._visual_client.is_available():
                    logger.info(f"视觉客户端初始化成功: {self._visual_client.model}")
                else:
                    logger.warning("视觉客户端初始化完成，但 API 未配置")
            except Exception as e:
                logger.warning(f"视觉客户端初始化失败: {e}")
        return self._visual_client

    @property
    def ocr_engine(self) -> Optional[OCREngineProtocol]:
        """获取 OCR 引擎实例（延迟加载）"""
        if self._ocr_engine is None:
            try:
                self._ocr_engine = create_ocr_engine(self.config.ocr_backend)
                logger.info(f"OCR 引擎初始化成功: {self.config.ocr_backend}")
            except Exception as e:
                logger.warning(f"OCR 引擎初始化失败: {e}，将使用无 OCR 模式")
                from ..infrastructure.llm.ocr_engine import NoOCREngine

                self._ocr_engine = NoOCREngine()
        return self._ocr_engine

    @property
    def pdf_converter(self) -> Optional[PyMuPDFConverter]:
        """获取 PDF 转换器实例（延迟加载）"""
        if self._pdf_converter is None:
            try:
                self._pdf_converter = PyMuPDFConverter(
                    zoom_factor=self.config.pdf_zoom_factor,
                )
                logger.info("PDF 转换器初始化成功 (PyMuPDF)")
            except Exception as e:
                logger.warning(f"PDF 转换器初始化失败: {e}")
        return self._pdf_converter

    @property
    def validity_retriever(self) -> Optional[InMemoryValidityRetriever]:
        """获取有效期 RAG 检索器实例（延迟加载）"""
        if self._validity_retriever is None and self.config.rag_enabled:
            matcher = self.semantic_matcher
            if matcher is not None:
                try:
                    self._validity_retriever = InMemoryValidityRetriever(
                        semantic_matcher=matcher,
                        chunk_size=self.config.rag_chunk_size,
                        chunk_overlap=self.config.rag_chunk_overlap,
                        top_k=self.config.rag_top_k,
                        circuit_breaker_threshold=self.config.rag_circuit_breaker_threshold,
                    )
                    logger.info(
                        f"Micro-RAG 检索器初始化成功: "
                        f"chunk_size={self.config.rag_chunk_size}, "
                        f"top_k={self.config.rag_top_k}"
                    )
                except Exception as e:
                    logger.warning(f"Micro-RAG 检索器初始化失败: {e}")
            else:
                logger.debug("SemanticMatcher 不可用，跳过 Micro-RAG 初始化")
        return self._validity_retriever

def create_container(config: Optional[CheckerConfig] = None) -> Container:
    """
    按需创建依赖注入容器（CLI 命令层使用）。

    仅创建 Container，不初始化 CheckerRegistry。
    各 command 模块按需从 container 中获取所需服务。

    Args:
        config: 可选的配置对象，默认从环境变量加载

    Returns:
        Container 实例
    """
    if config is None:
        config = CheckerConfig.from_env()

    return Container(config)
