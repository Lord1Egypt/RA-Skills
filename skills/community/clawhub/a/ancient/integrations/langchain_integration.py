"""
LangChain 集成模块

提供与 LangChain 生态系统的无缝集成
"""

from typing import List, Optional, Dict, Any
import sys
import os

# 尝试导入 LangChain（如果可用）
try:
    from langchain.callbacks.base import BaseCallbackHandler
    from langchain.schema import LLMResult, HumanMessage, AIMessage, SystemMessage
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    BaseCallbackHandler = object

# 添加父目录到路径以导入主模块
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
try:
    from ancientman_enhanced import AncientmanCompressor, CompressionMode
except ImportError:
    from scripts.ancientman_enhanced import AncientmanCompressor, CompressionMode


if LANGCHAIN_AVAILABLE:
    class AncientmanCompressionHandler(BaseCallbackHandler):
        """
        LangChain 压缩回调处理器
        
        在 LLM 调用的输入/输出自动应用压缩
        
        用法:
        ```python
        from langchain.chat_models import ChatOpenAI
        from ancientman.integrations import AncientmanCompressionHandler
        
        llm = ChatOpenAI(
            callbacks=[AncientmanCompressionHandler(mode="standard")]
        )
        response = llm.predict("帮我优化数据库查询")
        ```
        
        参数:
            mode: 压缩模式
                - "lite": 轻度压缩
                - "standard": 标准压缩（默认）
                - "ultra": 极致压缩
                - "classical": 古风压缩
            preserve_tense: 是否保留时态标记
            compress_input: 是否压缩输入
            compress_output: 是否解压缩输出
        """
        
        def __init__(
            self,
            mode: str = "standard",
            preserve_tense: bool = True,
            compress_input: bool = True,
            compress_output: bool = False,
        ):
            super().__init__()
            mode_map = {
                "lite": CompressionMode.LITE,
                "standard": CompressionMode.STANDARD,
                "ultra": CompressionMode.ULTRA,
                "classical": CompressionMode.CLASSICAL,
            }
            self.mode = mode_map.get(mode, CompressionMode.STANDARD)
            self.preserve_tense = preserve_tense
            self.compress_input = compress_input
            self.compress_output = compress_output
            self.compressor = AncientmanCompressor(self.mode, self.preserve_tense)
            self._input_messages: List[str] = []
            self._output_messages: List[str] = []
        
        def on_llm_start(
            self, serialized: Dict[str, Any], prompts: List[str], **kwargs
        ) -> None:
            """LLM 开始处理时调用"""
            if self.compress_input and prompts:
                compressed_prompts = []
                for prompt in prompts:
                    result = self.compressor.compress(prompt)
                    compressed_prompts.append(result.compressed)
                return {"compressed_prompts": compressed_prompts}
        
        def on_llm_end(self, response: LLMResult, **kwargs) -> None:
            """LLM 完成处理时调用"""
            if self.compress_output and response.generations:
                for generation_list in response.generations:
                    for generation in generation_list:
                        if hasattr(generation, 'text'):
                            original = generation.text
                            decompressed = self.compressor.decompress(original)
                            generation.text = decompressed
        
        @property
        def compression_stats(self) -> Dict[str, Any]:
            """获取压缩统计信息"""
            total_input = sum(len(m) for m in self._input_messages)
            total_output = sum(len(m) for m in self._output_messages)
            return {
                "mode": self.mode.value,
                "input_count": len(self._input_messages),
                "output_count": len(self._output_messages),
                "total_input_chars": total_input,
                "total_output_chars": total_output,
            }
else:
    # LangChain 未安装时的占位符
    class AncientmanCompressionHandler:
        """LangChain 未安装，请先安装: pip install langchain"""
        def __init__(self, *args, **kwargs):
            raise ImportError(
                "LangChain 未安装。请先安装: pip install langchain\n"
                "或使用 AncientmanCompressor 直接进行压缩"
            )


class AncientmanDocumentTransformer:
    """
    LangChain 文档转换器
    
    批量压缩文档内容
    
    用法:
    ```python
    from ancientman.integrations import AncientmanDocumentTransformer
    
    transformer = AncientmanDocumentTransformer(mode="ultra")
    documents = ["文档内容1...", "文档内容2..."]
    results = transformer.transform_documents(documents)
    
    for r in results:
        print(f"原始: {r['original']}")
        print(f"压缩: {r['compressed']}")
        print(f"节省: {r['reduction_percent']}%")
    ```
    
    参数:
        mode: 压缩模式
        preserve_tense: 是否保留时态
    """
    
    def __init__(
        self,
        mode: str = "standard",
        preserve_tense: bool = True,
    ):
        mode_map = {
            "lite": CompressionMode.LITE,
            "standard": CompressionMode.STANDARD,
            "ultra": CompressionMode.ULTRA,
            "classical": CompressionMode.CLASSICAL,
        }
        self.mode = mode_map.get(mode, CompressionMode.STANDARD)
        self.preserve_tense = preserve_tense
        self.compressor = AncientmanCompressor(self.mode, preserve_tense)
    
    def transform_documents(self, documents: List[str]) -> List[Dict[str, Any]]:
        """
        批量转换文档
        
        Args:
            documents: 文档列表
            
        Returns:
            List[Dict]: 转换结果列表，每项包含:
                - original: 原始文本
                - compressed: 压缩后文本
                - reduction_percent: 节省百分比
                - mapping_log: 使用的映射关系
        """
        results = []
        for doc in documents:
            result = self.compressor.compress(doc)
            results.append({
                "original": doc,
                "compressed": result.compressed,
                "reduction_percent": result.reduction_percent,
                "original_length": result.original_length,
                "compressed_length": result.compressed_length,
                "mapping_log": result.mapping_log,
            })
        return results
    
    def transform_with_metadata(
        self,
        documents: List[Dict[str, Any]],
        text_field: str = "page_content",
    ) -> List[Dict[str, Any]]:
        """
        转换带有元数据的文档
        
        Args:
            documents: 文档列表，每个文档是包含 text_field 的字典
            text_field: 文本字段名
            
        Returns:
            List[Dict]: 转换后的文档，保留原有元数据
        """
        results = []
        for doc in documents:
            text = doc.get(text_field, "")
            result = self.compressor.compress(text)
            
            new_doc = doc.copy()
            new_doc[text_field] = result.compressed
            new_doc["compression_stats"] = {
                "reduction_percent": result.reduction_percent,
                "original_length": result.original_length,
                "compressed_length": result.compressed_length,
            }
            results.append(new_doc)
        return results


def create_compression_pipeline(
    mode: str = "standard",
    preserve_tense: bool = True,
) -> AncientmanDocumentTransformer:
    """
    创建压缩流水线（工厂函数）
    
    Args:
        mode: 压缩模式
        preserve_tense: 是否保留时态
        
    Returns:
        AncientmanDocumentTransformer: 文档转换器实例
    """
    return AncientmanDocumentTransformer(mode=mode, preserve_tense=preserve_tense)
