# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd. and/or its affiliates.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
文本向量化模块，基于火山引擎方舟API
"""
import os
import openai
from typing import List, Optional

class TextEmbedding:
    def __init__(self, 
                 api_key: Optional[str] = None,
                 base_url: Optional[str] = None,
                 model: Optional[str] = None,
                 dimensions: Optional[int] = None):
        """
        初始化文本向量化客户端
        :param api_key: 方舟API密钥，默认从环境变量ARK_API_KEY读取
        :param base_url: 方舟API地址，默认从环境变量ARK_BASE_URL读取
        :param model: 向量化模型，默认从环境变量EMBEDDING_MODEL读取
        :param dimensions: 向量维度，默认从环境变量EMBEDDING_DIMENSIONS读取，默认1536
        """
        self.api_key = api_key or os.getenv("ARK_API_KEY")
        self.base_url = base_url or os.getenv("ARK_BASE_URL", "https://ark.cn-beijing.volces.com/api/v3")
        self.model = model or os.getenv("EMBEDDING_MODEL", "doubao-embedding-text-240715")
        self.dimensions = dimensions or int(os.getenv("EMBEDDING_DIMENSIONS", "2560"))
        
        if not self.api_key:
            raise ValueError("请配置ARK_API_KEY环境变量或传入api_key参数")
        
        self.client = openai.OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
    
    def embed_text(self, text: str) -> List[float]:
        """
        生成单个文本的向量
        :param text: 输入文本
        :return: 向量列表
        """
        params = {
            "input": text,
            "model": self.model
        }
        # 仅当dimensions存在时传递参数，部分模型不支持自定义维度
        if self.dimensions:
            params["dimensions"] = self.dimensions
        
        response = self.client.embeddings.create(**params)
        return response.data[0].embedding
    
    def batch_embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        批量生成文本向量
        :param texts: 输入文本列表
        :return: 向量列表
        """
        params = {
            "input": texts,
            "model": self.model
        }
        # 仅当dimensions存在时传递参数，部分模型不支持自定义维度
        if self.dimensions:
            params["dimensions"] = self.dimensions
        
        response = self.client.embeddings.create(**params)
        return [item.embedding for item in response.data]
