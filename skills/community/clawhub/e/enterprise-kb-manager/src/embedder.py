"""
嵌入生成器 (Embedding Engine)

支持多种API提供商的文本嵌入生成，包括OpenAI和DashScope(阿里云千问)。
提供统一的接口和自动重试机制，确保嵌入生成的稳定性和可靠性。

支持的提供商:
- OpenAI: text-embedding-3-small, text-embedding-3-large
- DashScope: text-embedding-v3 (阿里云千问)

特性:
- 自动重试和指数退避
- 批量嵌入生成
- 错误处理和日志记录
- 多提供商统一接口
- 维度自动检测

作者: OpenClaw Team
版本: 1.0.0
"""

import logging
import time
from typing import List, Optional, Union
from openai import OpenAI
from dataclasses import dataclass

# 设置日志
logger = logging.getLogger(__name__)


@dataclass
class EmbeddingConfig:
    """嵌入配置类"""
    model: str
    api_key: str
    provider: str = "openai"
    base_url: Optional[str] = None
    max_retries: int = 3
    timeout: int = 30
    
    def __post_init__(self):
        """配置验证"""
        if not self.api_key:
            raise ValueError("API密钥不能为空")
        
        if self.provider not in ["openai", "dashscope"]:
            raise ValueError(f"不支持的提供商: {self.provider}")


class Embedder:
    """
    文本嵌入生成器
    
    支持OpenAI和DashScope API，提供统一的嵌入生成接口。
    包含自动重试、错误处理和性能优化功能。
    """
    
    # 支持的模型配置
    MODEL_CONFIGS = {
        "openai": {
            "text-embedding-3-small": {"dimension": 1536, "max_tokens": 8191},
            "text-embedding-3-large": {"dimension": 3072, "max_tokens": 8191},
            "text-embedding-ada-002": {"dimension": 1536, "max_tokens": 8191},
        },
        "dashscope": {
            "text-embedding-v3": {"dimension": 1024, "max_tokens": 2048},
            "text-embedding-v2": {"dimension": 1536, "max_tokens": 2048},
        }
    }
    
    def __init__(self, model: str = "text-embedding-3-small", api_key: str = None,
                 provider: str = "openai", base_url: str = None, 
                 max_retries: int = 3, timeout: int = 30):
        """
        初始化嵌入生成器
        
        Args:
            model: 嵌入模型名称
            api_key: API密钥
            provider: API提供商 (openai, dashscope)
            base_url: 自定义API基础URL
            max_retries: 最大重试次数
            timeout: 请求超时时间(秒)
        
        Raises:
            ValueError: 配置参数无效
            ConnectionError: API连接失败
        """
        # 创建配置对象
        self.config = EmbeddingConfig(
            model=model,
            api_key=api_key,
            provider=provider,
            base_url=base_url,
            max_retries=max_retries
        )
        
        # 设置提供商特定配置
        self._setup_provider()
        
        # 获取模型配置
        self._setup_model_config()
        
        logger.info(f"嵌入生成器已初始化: {provider}/{model} (维度: {self.dimension})")
    
    def _setup_provider(self):
        """设置API提供商配置"""
        if self.config.provider == "dashscope":
            # DashScope (阿里云千问) 配置
            self.client = OpenAI(
                api_key=self.config.api_key,
                base_url=self.config.base_url or "https://dashscope.aliyuncs.com/compatible-mode/v1",
                timeout=self.config.timeout
            )
            logger.info("使用DashScope API (阿里云千问)")
            
        elif self.config.provider == "openai":
            # OpenAI 配置
            client_kwargs = {
                "api_key": self.config.api_key,
                "timeout": self.config.timeout
            }
            if self.config.base_url:
                client_kwargs["base_url"] = self.config.base_url
                
            self.client = OpenAI(**client_kwargs)
            logger.info("使用OpenAI API")
            
        else:
            raise ValueError(f"不支持的提供商: {self.config.provider}")
    
    def _setup_model_config(self):
        """设置模型配置"""
        provider_models = self.MODEL_CONFIGS.get(self.config.provider, {})
        model_config = provider_models.get(self.config.model)
        
        if model_config:
            self.dimension = model_config["dimension"]
            self.max_tokens = model_config["max_tokens"]
        else:
            # 默认配置
            self.dimension = 1536
            self.max_tokens = 8191
            logger.warning(f"未知模型 {self.config.model}，使用默认配置")
    
    def embed_texts(self, texts: List[str], batch_size: int = 100) -> List[List[float]]:
        """
        批量生成文本嵌入
        
        Args:
            texts: 文本列表
            batch_size: 批处理大小
        
        Returns:
            嵌入向量列表
        
        Raises:
            RuntimeError: 嵌入生成失败
            ValueError: 输入参数无效
        """
        if not texts:
            logger.warning("输入文本列表为空")
            return []
        
        if not isinstance(texts, list):
            raise ValueError("texts必须是字符串列表")
        
        # 过滤空文本
        valid_texts = [text.strip() for text in texts if text and text.strip()]
        if len(valid_texts) != len(texts):
            logger.warning(f"过滤了 {len(texts) - len(valid_texts)} 个空文本")
        
        if not valid_texts:
            logger.warning("所有文本都为空")
            return []
        
        logger.info(f"开始生成 {len(valid_texts)} 个文本的嵌入向量")
        
        all_embeddings = []
        
        # 分批处理
        for i in range(0, len(valid_texts), batch_size):
            batch = valid_texts[i:i + batch_size]
            batch_embeddings = self._embed_batch(batch)
            all_embeddings.extend(batch_embeddings)
            
            logger.debug(f"已处理批次 {i//batch_size + 1}/{(len(valid_texts)-1)//batch_size + 1}")
        
        logger.info(f"成功生成 {len(all_embeddings)} 个嵌入向量")
        return all_embeddings
    
    def _embed_batch(self, texts: List[str]) -> List[List[float]]:
        """
        处理单个批次的嵌入生成
        
        Args:
            texts: 文本批次
        
        Returns:
            嵌入向量列表
        """
        for attempt in range(self.config.max_retries):
            try:
                # 调用API
                response = self.client.embeddings.create(
                    model=self.config.model,
                    input=texts
                )
                
                # 提取嵌入向量
                embeddings = [item.embedding for item in response.data]
                
                # 验证结果
                if len(embeddings) != len(texts):
                    raise RuntimeError(f"返回的嵌入数量({len(embeddings)})与输入文本数量({len(texts)})不匹配")
                
                # 验证维度
                for i, embedding in enumerate(embeddings):
                    if len(embedding) != self.dimension:
                        raise RuntimeError(f"嵌入向量维度错误: 期望{self.dimension}, 实际{len(embedding)}")
                
                return embeddings
                
            except Exception as e:
                error_msg = f"嵌入生成失败 (尝试 {attempt + 1}/{self.config.max_retries}): {str(e)}"
                
                if attempt < self.config.max_retries - 1:
                    # 指数退避
                    wait_time = 2 ** attempt
                    logger.warning(f"{error_msg}, {wait_time}秒后重试...")
                    time.sleep(wait_time)
                else:
                    logger.error(f"{error_msg}, 已达到最大重试次数")
                    raise RuntimeError(f"嵌入生成失败: {str(e)}")
    
    def embed_query(self, query: str) -> List[float]:
        """
        生成单个查询的嵌入向量
        
        Args:
            query: 查询文本
        
        Returns:
            嵌入向量
        
        Raises:
            ValueError: 查询文本无效
            RuntimeError: 嵌入生成失败
        """
        if not query or not query.strip():
            raise ValueError("查询文本不能为空")
        
        logger.debug(f"生成查询嵌入: {query[:50]}...")
        
        embeddings = self.embed_texts([query.strip()])
        return embeddings[0] if embeddings else []
    
    def get_model_info(self) -> dict:
        """
        获取模型信息
        
        Returns:
            模型配置字典
        """
        return {
            "provider": self.config.provider,
            "model": self.config.model,
            "dimension": self.dimension,
            "max_tokens": self.max_tokens,
            "base_url": self.config.base_url
        }
    
    def validate_connection(self) -> bool:
        """
        验证API连接
        
        Returns:
            连接是否成功
        """
        try:
            test_embedding = self.embed_query("测试连接")
            return len(test_embedding) == self.dimension
        except Exception as e:
            logger.error(f"连接验证失败: {e}")
            return False


# 便捷函数
def create_embedder(provider: str = "dashscope", api_key: str = None, **kwargs) -> Embedder:
    """
    创建嵌入生成器的便捷函数
    
    Args:
        provider: API提供商
        api_key: API密钥
        **kwargs: 其他配置参数
    
    Returns:
        配置好的Embedder实例
    """
    if provider == "dashscope":
        defaults = {
            "model": "text-embedding-v3",
            "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1"
        }
    else:
        defaults = {
            "model": "text-embedding-3-small"
        }
    
    # 合并默认配置和用户配置
    config = {**defaults, **kwargs}
    
    return Embedder(
        api_key=api_key,
        provider=provider,
        **config
    )


if __name__ == "__main__":
    # 测试嵌入生成器
    import os
    
    print("=" * 60)
    print("嵌入生成器测试")
    print("=" * 60)
    
    # 尝试DashScope
    dashscope_key = os.getenv("DASHSCOPE_API_KEY")
    if dashscope_key:
        print("\n🧪 测试DashScope API...")
        try:
            embedder = create_embedder("dashscope", dashscope_key)
            
            # 测试连接
            if embedder.validate_connection():
                print("✅ DashScope连接成功")
                
                # 测试单个嵌入
                vector = embedder.embed_query("这是一个测试查询")
                print(f"✅ 单个嵌入: {len(vector)}维向量")
                print(f"   前5个值: {vector[:5]}")
                
                # 测试批量嵌入
                texts = ["第一个文档", "第二个文档", "第三个文档"]
                vectors = embedder.embed_texts(texts)
                print(f"✅ 批量嵌入: {len(vectors)}个向量")
                
                # 显示模型信息
                info = embedder.get_model_info()
                print(f"✅ 模型信息: {info}")
                
            else:
                print("❌ DashScope连接失败")
                
        except Exception as e:
            print(f"❌ DashScope测试失败: {e}")
    
    # 尝试OpenAI
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        print("\n🧪 测试OpenAI API...")
        try:
            embedder = create_embedder("openai", openai_key)
            
            if embedder.validate_connection():
                print("✅ OpenAI连接成功")
                vector = embedder.embed_query("This is a test query")
                print(f"✅ 生成嵌入: {len(vector)}维向量")
            else:
                print("❌ OpenAI连接失败")
                
        except Exception as e:
            print(f"❌ OpenAI测试失败: {e}")
    
    if not dashscope_key and not openai_key:
        print("\n❌ 未找到API密钥")
        print("请设置环境变量:")
        print("  $env:DASHSCOPE_API_KEY='your-key'")
        print("  $env:OPENAI_API_KEY='your-key'")
    
    print("\n" + "=" * 60)
