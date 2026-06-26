"""
企业知识库系统 (Enterprise Knowledge Base System)

这是一个基于ChromaDB的本地企业知识库系统，支持多种文档格式的上传、
语义搜索和RAG(检索增强生成)问答功能。

主要特性:
- 多格式文档支持 (PDF, DOCX, TXT, MD)
- 本地向量存储 (ChromaDB)
- 语义搜索和相似度匹配
- 智能文档分块和嵌入
- RAG问答系统集成
- 多API提供商支持 (OpenAI, DashScope)

作者: Enterprise KB System Team
版本: 1.0.0
创建日期: 2026-05-06
许可证: MIT
"""

__version__ = "1.0.0"
__author__ = "Enterprise KB System Team"
__email__ = "team@yourproject.com"
__license__ = "MIT"

# 核心配置模块
from .config_loader import load_config, KnowledgeBaseConfig, ConfigLoader

# 向量数据库模块
from .chroma_client import ChromaVectorDB, SearchResult

# 文档处理模块
from .chunker import DocumentChunker, Chunk
from .parser import DocumentParser
from .document_processor import DocumentProcessor, ProcessResult

# 嵌入和检索模块
from .embedder import Embedder
from .retriever import Retriever, RetrievalResult

# 管理模块
from .manager import KnowledgeBaseManager

# 导出所有公共接口
__all__ = [
    # 版本信息
    "__version__",
    "__author__", 
    "__email__",
    "__license__",
    
    # 配置管理
    "load_config",
    "KnowledgeBaseConfig", 
    "ConfigLoader",
    
    # 数据库接口
    "ChromaVectorDB",
    "SearchResult",
    
    # 文档处理
    "DocumentChunker",
    "Chunk",
    "DocumentParser", 
    "DocumentProcessor",
    "ProcessResult",
    
    # 嵌入和检索
    "Embedder",
    "Retriever",
    "RetrievalResult",
    
    # 管理接口
    "KnowledgeBaseManager",
]

# 模块级别的配置
import logging

# 设置日志格式
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# 创建模块日志器
logger = logging.getLogger(__name__)
logger.info(f"企业知识库系统 v{__version__} 已加载")

# 兼容性检查
import sys
if sys.version_info < (3, 8):
    logger.warning("建议使用Python 3.8+以获得最佳性能和兼容性")

# 可选依赖检查
try:
    import chromadb
    logger.info(f"ChromaDB v{chromadb.__version__} 已加载")
except ImportError:
    logger.error("ChromaDB未安装，请运行: pip install chromadb>=0.4.0")

try:
    import openai
    logger.info(f"OpenAI客户端 v{openai.__version__} 已加载")
except ImportError:
    logger.error("OpenAI客户端未安装，请运行: pip install openai>=1.0.0")

# 模块初始化完成
logger.info("所有模块加载完成，系统就绪")

