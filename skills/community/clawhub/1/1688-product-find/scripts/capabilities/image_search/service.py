# -*- coding: utf-8 -*-
"""
图片搜索能力实现
基于上传的商品图片搜索同款或相似商品
"""

import os
import base64
import logging
from typing import Dict, List, Any

from _http import search_products
from _errors import ServiceError
from _image import ImagePreprocessor

logger = logging.getLogger("1688_image_search")


class ImageSearchExecutor:
    """图片搜索执行器"""
    
    def __init__(self, platform: str = "1688"):
        self.platform = platform
        self.preprocessor = ImagePreprocessor()
    
    def search(self, image_path: str, limit: int = 10, 
               sort_type: str = None, score_level: str = "high",
               purchase_amount: int = 1,
               tags: str = "4306497", ic_tags: str = None) -> Dict[str, Any]:
        """
        执行图片搜索
        
        Args:
            image_path: 图片路径或 URL
            limit: 返回数量
            sort_type: 排序类型（price_asc/price_desc/sold_desc/yx_desc）
            score_level: 相关性档位（high/medium/low）
            purchase_amount: 采购件数
            tags: TC标（品池标签），英文逗号分隔
            ic_tags: IC标（品池标签），英文逗号分隔
            
        Returns:
            搜索结果
        """
        # 预处理图片
        img_info = self.preprocessor.preprocess(image_path)
        
        # 执行搜索（直接使用 API）
        results = self._search_via_api(img_info, limit, sort_type, score_level, purchase_amount,
                                         tags=tags, ic_tags=ic_tags)
        
        return {
            "success": True,
            "source_image": image_path,
            "similar_products": results,
            "search_type": "image_similarity",
            "total_results": len(results)
        }
    
    def _search_via_api(self, img_info: Dict, limit: int,
                        sort_type: str = None, score_level: str = "high",
                        purchase_amount: int = 1,
                        extra_params: Dict = None,
                        tags: str = "4306497", ic_tags: str = None) -> List[Dict]:
        """通过 API 搜索

        Args:
            img_info: 预处理后的图片信息
            limit: 返回数量
            sort_type: 排序类型
            score_level: 相关性档位
            purchase_amount: 采购件数
            extra_params: 额外请求参数（如 query）

        Returns:
            商品列表
        """
        image_base64 = ""
        image_url = None
        converted_path = None
        
        # 根据图片类型处理
        if img_info.get("type") == "url":
            image_url = img_info.get("url")
        else:
            image_path = img_info.get("path")
            if not image_path or not os.path.exists(image_path):
                raise ServiceError("图片路径无效")
            if img_info.get("converted"):
                converted_path = image_path
            with open(image_path, "rb") as f:
                image_base64 = base64.b64encode(f.read()).decode("utf-8")
        
        try:
            request = {
                "imgBase64": image_base64,
                "imageUrl": image_url,
                "pageSize": limit,
                "purchaseAmount": purchase_amount
            }
            # 排序类型（可选）
            if sort_type:
                request["sortType"] = sort_type
            
            # 相关性档位（默认 high）
            if score_level:
                request["scoreLevel"] = score_level

            # 品池标签
            if tags:
                request["tags"] = tags
            if ic_tags:
                request["icTags"] = ic_tags

            # 合并额外参数（如 compare 传入的 query）
            if extra_params:
                request.update(extra_params)
            
            return search_products(request)
        finally:
            if converted_path:
                try:
                    os.unlink(converted_path)
                except OSError:
                    pass
    

# ========== 主入口函数 ==========

def image_search(image_path: str, platform: str = "1688", 
                 limit: int = 10,
                 sort_type: str = None, score_level: str = "high",
                 purchase_amount: int = 1,
                 tags: str = "4306497", ic_tags: str = None) -> Dict[str, Any]:
    """
    图片搜索主函数
    
    Args:
        image_path: 图片本地路径或 URL
        platform: 目标平台
        limit: 返回数量
        sort_type: 排序类型（price_asc/price_desc/sold_desc/yx_desc）
        score_level: 相关性档位（high/medium/low）
        purchase_amount: 采购件数
        tags: TC标（品池标签），英文逗号分隔，默认 "4306497"
        ic_tags: IC标（品池标签），英文逗号分隔
        
    Returns:
        搜索结果
    """
    executor = ImageSearchExecutor(platform=platform)
    return executor.search(
        image_path=image_path,
        limit=limit,
        sort_type=sort_type,
        score_level=score_level,
        purchase_amount=purchase_amount,
        tags=tags,
        ic_tags=ic_tags,
    )


if __name__ == "__main__":
    # 测试示例
    test_image = "/workspace/test_product.jpg"
    if os.path.exists(test_image):
        result = image_search(test_image)
        print(f"找到 {result['total_results']} 个相似商品")
    else:
        print(f"测试图片不存在：{test_image}")
