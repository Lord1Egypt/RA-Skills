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
多模态向量化模块
基于豆包多模态向量化模型实现文本、图片、视频的向量化
"""

import os
import numpy as np
from volcenginesdkarkruntime import Ark
from typing import List, Union, Dict


class MultimodalEmbedding:
    """多模态向量化客户端"""
    
    def __init__(self):
        self.client = Ark(
            api_key=os.environ.get("ARK_API_KEY"),
            base_url=os.environ.get("ARK_BASE_URL", "https://ark.cn-beijing.volces.com/api/v3")
        )
        self.model = os.environ.get("EMBEDDING_MODEL", "doubao-embedding-vision-251215")
        self.dimensions = int(os.environ.get("EMBEDDING_DIMENSIONS", 1536))
    
    def encode(self, 
               input_data: Union[str, List[Dict]], 
               modality: str = "text",
               instruction: str = None) -> List[float]:
        """
        多模态向量化接口
        
        Args:
            input_data: 输入数据
                - 文本：直接传入字符串
                - 图片/视频：传入 {"type": "image_url"/"video_url", "url": "xxx"} 格式
            modality: 数据类型，可选 text/image/video
            instruction: 自定义指令，用于提升特定场景检索精度
        
        Returns:
            向量列表
        """
        try:
            if isinstance(input_data, str):
                input_item = {"type": "text", "text": input_data}
            else:
                input_item = input_data
            
            # 输入格式校验
            if modality in ["image", "video"] and not isinstance(input_item, dict):
                raise ValueError(f"{modality}类型输入必须为包含url的字典格式")
            
            # 构造请求参数
            request_params = {
                "model": self.model,
                "encoding_format": "float",
                "input": [input_item],
                "dimensions": self.dimensions
            }
            
            # 添加自定义指令（251215及以上版本支持）
            if instruction and "251215" in self.model:
                request_params["instructions"] = instruction
            
            # 调用 API
            resp = self.client.multimodal_embeddings.create(**request_params)
            
            if hasattr(resp, 'data') and len(resp.data) > 0 and hasattr(resp.data[0], 'embedding'):
                embedding = resp.data[0].embedding
                vec = np.array(embedding).flatten().tolist()
                
                # 校验向量维度
                if len(vec) != self.dimensions:
                    raise ValueError(f"向量维度不匹配：期望{self.dimensions}维，实际返回{len(vec)}维")
                
                return vec
            else:
                raise ValueError("API响应格式错误，未找到embedding字段")
        
        except Exception as e:
            error_msg = str(e).lower()
            if "api key" in error_msg or "unauthorized" in error_msg or "permission" in error_msg:
                raise PermissionError(f"向量化失败：API密钥无效或权限不足。错误详情：{e}")
            elif "connection" in error_msg or "timeout" in error_msg or "network" in error_msg:
                raise ConnectionError(f"向量化失败：网络连接异常。错误详情：{e}")
            elif "invalid" in error_msg or "parameter" in error_msg or "format" in error_msg:
                raise ValueError(f"向量化失败：输入参数或格式错误。错误详情：{e}")
            else:
                raise Exception(f"向量化失败：{e}")
    
    def encode_text(self, text: str, instruction: str = None) -> List[float]:
        """文本向量化"""
        return self.encode(text, "text", instruction)
    
    def encode_image(self, image_url: str, instruction: str = None) -> List[float]:
        """图片URL向量化"""
        input_item = {"type": "image_url", "image_url": {"url": image_url}}
        return self.encode(input_item, "image", instruction)
    
    def encode_video(self, video_url: str, instruction: str = None) -> List[float]:
        """视频URL向量化"""
        input_item = {"type": "video_url", "video_url": {"url": video_url}}
        return self.encode(input_item, "video", instruction)
