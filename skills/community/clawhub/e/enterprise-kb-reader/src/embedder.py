#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
嵌入器 - 只读查询器专用
"""

import os
from typing import List, Optional
import openai


class Embedder:
    """文本嵌入器"""
    
    def __init__(self, model: str = "text-embedding-v3", 
                 api_key: str = "", 
                 provider: str = "dashscope",
                 base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"):
        """
        初始化嵌入器
        
        Args:
            model: 嵌入模型名称
            api_key: API密钥
            provider: 提供商 (dashscope/openai)
            base_url: API基础URL
        """
        self.model = model
        self.provider = provider
        
        # 设置API密钥
        if not api_key:
            if provider == "dashscope":
                api_key = os.getenv("DASHSCOPE_API_KEY", "")
            elif provider == "openai":
                api_key = os.getenv("OPENAI_API_KEY", "")
        
        if not api_key:
            raise ValueError(f"未找到 {provider} API密钥")
        
        # 初始化客户端
        if provider == "dashscope":
            self.client = openai.OpenAI(
                api_key=api_key,
                base_url=base_url
            )
        elif provider == "openai":
            self.client = openai.OpenAI(api_key=api_key)
        else:
            raise ValueError(f"不支持的提供商: {provider}")
    
    def embed_text(self, text: str) -> List[float]:
        """
        生成文本嵌入向量
        
        Args:
            text: 输入文本
            
        Returns:
            嵌入向量
        """
        try:
            # 清理文本
            text = text.strip().replace('\n', ' ')
            if not text:
                return [0.0] * 1024
            
            # 调用API
            response = self.client.embeddings.create(
                model=self.model,
                input=text
            )
            
            return response.data[0].embedding
            
        except Exception as e:
            print(f"生成嵌入向量失败: {e}")
            return [0.0] * 1024
    
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """
        批量生成嵌入向量
        
        Args:
            texts: 文本列表
            
        Returns:
            嵌入向量列表
        """
        try:
            # 清理文本
            cleaned_texts = []
            for text in texts:
                cleaned = text.strip().replace('\n', ' ')
                cleaned_texts.append(cleaned if cleaned else " ")
            
            # 调用API
            response = self.client.embeddings.create(
                model=self.model,
                input=cleaned_texts
            )
            
            return [item.embedding for item in response.data]
            
        except Exception as e:
            print(f"批量生成嵌入向量失败: {e}")
            return [[0.0] * 1024] * len(texts)