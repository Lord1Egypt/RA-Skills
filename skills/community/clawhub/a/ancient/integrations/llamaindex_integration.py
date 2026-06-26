"""
LlamaIndex 集成模块

提供与 LlamaIndex 生态系统的无缝集成
"""

from typing import List, Dict, Any, Optional
import sys
import os

# 添加父目录到路径以导入主模块
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
try:
    from ancientman_enhanced import AncientmanCompressor, CompressionMode
except ImportError:
    from scripts.ancientman_enhanced import AncientmanCompressor, CompressionMode


class AncientmanQueryRewriter:
    """
    LlamaIndex 查询重写器
    
    在查询 LlamaIndex 向量数据库前压缩查询语句
    
    用法:
    ```python
    from llama_index import VectorStoreIndex
    from ancientman.integrations import AncientmanQueryRewriter
    
    # 创建重写器
    rewriter = AncientmanQueryRewriter(mode="standard")
    
    # 压缩用户查询
    compressed_query = rewriter.rewrite("如何优化PostgreSQL数据库的查询性能")
    # -> "优pg库查性"
    
    # 使用压缩后的查询进行检索
    index = VectorStoreIndex.from_documents(documents)
    query_engine = index.as_query_engine()
    response = query_engine.query(compressed_query)
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
    
    def rewrite(self, query: str) -> str:
        """
        重写（压缩）查询
        
        Args:
            query: 原始查询
            
        Returns:
            str: 压缩后的查询
        """
        result = self.compressor.compress(query)
        return result.compressed
    
    def rewrite_batch(self, queries: List[str]) -> List[str]:
        """
        批量重写查询
        
        Args:
            queries: 原始查询列表
            
        Returns:
            List[str]: 压缩后的查询列表
        """
        return [self.rewrite(q) for q in queries]


class AncientmanNodeParser:
    """
    LlamaIndex 节点解析器
    
    在文档分块时进行压缩
    
    用法:
    ```python
    from llama_index import SimpleDirectoryReader
    from ancientman.integrations import AncientmanNodeParser
    
    # 加载文档
    documents = SimpleDirectoryReader("./data").load_data()
    
    # 使用压缩解析器
    parser = AncientmanNodeParser(mode="ultra")
    nodes = parser.parse(documents)
    ```
    
    参数:
        mode: 压缩模式
        preserve_tense: 是否保留时态
    """
    
    def __init__(
        self,
        mode: str = "ultra",
        preserve_tense: bool = True,
    ):
        mode_map = {
            "lite": CompressionMode.LITE,
            "standard": CompressionMode.STANDARD,
            "ultra": CompressionMode.ULTRA,
            "classical": CompressionMode.CLASSICAL,
        }
        self.mode = mode_map.get(mode, CompressionMode.ULTRA)
        self.preserve_tense = preserve_tense
        self.compressor = AncientmanCompressor(self.mode, preserve_tense)
    
    def parse(self, documents: List[Any]) -> List[Dict[str, Any]]:
        """
        解析并压缩文档
        
        Args:
            documents: LlamaIndex Document 对象列表
            
        Returns:
            List[Dict]: 压缩后的节点列表
        """
        results = []
        for doc in documents:
            # 提取文本
            if hasattr(doc, 'text'):
                text = doc.text
            elif hasattr(doc, 'get_text'):
                text = doc.get_text()
            else:
                text = str(doc)
            
            # 压缩
            result = self.compressor.compress(text)
            
            # 构建节点
            node = {
                "text": result.compressed,
                "original_text": result.original,
                "compression_stats": {
                    "reduction_percent": result.reduction_percent,
                    "original_length": result.original_length,
                    "compressed_length": result.compressed_length,
                }
            }
            
            # 复制元数据
            if hasattr(doc, 'metadata'):
                node["metadata"] = doc.metadata
            
            results.append(node)
        
        return results


class AncientmanRetriever:
    """
    LlamaIndex 检索结果压缩器
    
    在检索后对结果进行压缩
    
    用法:
    ```python
    from llama_index import VectorStoreIndex
    from ancientman.integrations import AncientmanRetriever
    
    index = VectorStoreIndex.from_documents(documents)
    retriever = AncientmanRetriever(index.as_retriever(), mode="standard")
    
    # 检索（会自动压缩结果）
    nodes = retriever.retrieve("优化数据库性能")
    ```
    
    参数:
        base_retriever: 基础检索器
        mode: 压缩模式
        preserve_tense: 是否保留时态
    """
    
    def __init__(
        self,
        base_retriever: Any,
        mode: str = "standard",
        preserve_tense: bool = True,
    ):
        mode_map = {
            "lite": CompressionMode.LITE,
            "standard": CompressionMode.STANDARD,
            "ultra": CompressionMode.ULTRA,
            "classical": CompressionMode.CLASSICAL,
        }
        self.base_retriever = base_retriever
        self.mode = mode_map.get(mode, CompressionMode.STANDARD)
        self.preserve_tense = preserve_tense
        self.compressor = AncientmanCompressor(self.mode, preserve_tense)
    
    def retrieve(self, query: str) -> List[Any]:
        """
        检索并压缩结果
        
        Args:
            query: 查询语句
            
        Returns:
            List: 压缩后的检索结果
        """
        # 压缩查询
        compressed_query = self.compressor.compress(query).compressed
        
        # 获取原始结果
        nodes = self.base_retriever.retrieve(compressed_query)
        
        # 压缩结果文本
        for node in nodes:
            if hasattr(node, 'text'):
                compressed_text = self.compressor.compress(node.text).compressed
                node.text = compressed_text
            elif hasattr(node, 'get_text'):
                original = node.get_text()
                compressed = self.compressor.compress(original).compressed
                node.set_text(compressed)
        
        return nodes


def create_compressed_index(
    documents: List[Any],
    mode: str = "ultra",
    **kwargs
) -> Any:
    """
    创建压缩索引的便捷函数
    
    Args:
        documents: 文档列表
        mode: 压缩模式
        **kwargs: 传递给 VectorStoreIndex 的其他参数
        
    Returns:
        VectorStoreIndex: 压缩后的索引
    """
    try:
        from llama_index import VectorStoreIndex
        from llama_index.node_parser import SimpleNodeParser
        
        # 使用压缩节点解析器
        parser = AncientmanNodeParser(mode=mode)
        nodes = parser.parse(documents)
        
        # 创建索引
        index = VectorStoreIndex.from_documents(nodes, **kwargs)
        return index
        
    except ImportError:
        raise ImportError(
            "LlamaIndex 未安装。请先安装: pip install llama-index\n"
            "或使用 AncientmanCompressor 直接进行压缩"
        )
