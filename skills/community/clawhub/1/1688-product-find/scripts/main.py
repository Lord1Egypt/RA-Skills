# -*- coding: utf-8 -*-
"""
1688 Find Product - 智能找商品 Skill 主入口

统一调度三大搜索能力：
1. text_search: 自然语言文本搜索
2. image_search: 图片找同款
3. link_search: 链接找同款
"""

import os
from typing import Dict, Any, Optional, List
from pathlib import Path

from .settings import settings
from .text_search import text_search as _text_search
from .image_search import image_search as _image_search
from .link_search import link_search as _link_search


class SmartProductFinder:
    """智能找商品主类"""
    
    def __init__(self):
        self.name = settings.SKILL_NAME
        self.version = settings.SKILL_VERSION
    
    def find(self, query: Optional[str] = None,
             image_path: Optional[str] = None,
             url: Optional[str] = None,
             platform: str = "1688",
             limit: int = 10) -> Dict[str, Any]:
        """
        统一的找商品入口
        
        Args:
            query: 自然语言描述（文本搜索时使用）
            image_path: 图片路径（图片搜索时使用）
            url: 商品链接或 ID（链接搜索时使用）
            platform: 目标平台 [1688, taobao, tmall]
            limit: 返回结果数量
            
        Returns:
            搜索结果字典
        """
        # 判断使用哪种搜索方式
        if image_path:
            return self._search_by_image(image_path, platform, limit)
        elif url:
            return self._search_by_link(url, platform, limit)
        elif query:
            return self._search_by_text(query, platform, limit)
        else:
            return {
                "success": False,
                "error": "请提供查询描述、图片或商品链接"
            }
    
    def _search_by_text(self, query: str, platform: str, limit: int) -> Dict[str, Any]:
        """文本搜索"""
        print(f"[Text Search] 查询：{query}")
        return _text_search(query=query, platform=platform, limit=limit)
    
    def _search_by_image(self, image_path: str, platform: str, limit: int) -> Dict[str, Any]:
        """图片搜索"""
        print(f"[Image Search] 图片：{image_path}")
        return _image_search(
            image_path=image_path,
            platform=platform,
            limit=limit
        )
    
    def _search_by_link(self, url: str, platform: str, limit: int) -> Dict[str, Any]:
        """链接搜索"""
        print(f"[Link Search] 链接：{url}")
        return _link_search(url=url, platform=platform, limit=limit)
    
    def get_capabilities(self) -> List[Dict[str, str]]:
        """获取支持的能力列表"""
        return [
            {
                "name": "text_search",
                "display_name": "文本搜索",
                "description": "通过自然语言描述找商品",
                "trigger_words": ["想要", "找", "搜", "帮我找"]
            },
            {
                "name": "image_search",
                "display_name": "图片找同款",
                "description": "上传图片找同款或相似商品",
                "trigger_words": ["图片找货", "找同款", "搜相似"]
            },
            {
                "name": "link_search",
                "display_name": "链接找同款",
                "description": "通过商品链接或 ID 找同款",
                "trigger_words": ["链接找货", "这个的同款", "商品链接"]
            }
        ]


# ========== Agent 集成接口 ==========

def execute_capability(capability: str, **kwargs) -> Dict[str, Any]:
    """
    Agent 调用 Skill 的统一接口
    
    Args:
        capability: 能力名称 (text_search, image_search, link_search)
        **kwargs: 能力对应的参数
        
    Returns:
        执行结果
    """
    finder = SmartProductFinder()
    
    if capability == "text_search":
        return finder.find(
            query=kwargs.get("query"),
            platform=kwargs.get("platform", "1688"),
            limit=kwargs.get("limit", 10)
        )
    
    elif capability == "image_search":
        return finder.find(
            image_path=kwargs.get("image_path"),
            platform=kwargs.get("platform", "1688"),
            limit=kwargs.get("limit", 10)
        )
    
    elif capability == "link_search":
        return finder.find(
            url=kwargs.get("url"),
            platform=kwargs.get("platform", "1688"),
            limit=kwargs.get("limit", 10)
        )
    
    else:
        return {
            "success": False,
            "error": f"未知的能力：{capability}"
        }


# ========== CLI 测试入口 ==========

def main():
    """命令行测试入口"""
    import sys
    
    finder = SmartProductFinder()
    
    print(f"=== {finder.name} v{finder.version} ===\n")
    print("支持三种找货方式:")
    print("1. 文本搜索：直接输入商品描述")
    print("2. 图片搜索：提供图片路径")
    print("3. 链接搜索：提供商品链接或 ID\n")
    
    if len(sys.argv) > 1:
        # 命令行参数模式
        mode = sys.argv[1]
        
        if mode == "text" and len(sys.argv) > 2:
            query = " ".join(sys.argv[2:])
            result = finder.find(query=query)
            print(f"\n解析结果：{result['parsed_query']}")
        
        elif mode == "image" and len(sys.argv) > 2:
            image_path = sys.argv[2]
            result = finder.find(image_path=image_path)
            print(f"\n找到 {result['total_results']} 个相似商品")
        
        elif mode == "link" and len(sys.argv) > 2:
            url = sys.argv[2]
            result = finder.find(url=url)
            print(f"\n原商品：{result['source_product']['title']}")
            print(f"找到 {result['total_results']} 个同款")
        
        else:
            print("用法:")
            print("  python -m scripts.text <查询描述>")
            print("  python -m scripts.image <图片路径>")
            print("  python -m scripts.link <商品链接>")
    else:
        # 交互模式
        print("请输入查询（或输入 quit 退出）:\n")
        while True:
            try:
                user_input = input("> ").strip()
                if user_input.lower() in ["quit", "exit", "q"]:
                    break
                
                result = finder.find(query=user_input)
                print(f"\n解析到属性：{result['parsed_query']['attributes']}")
                print(f"关键词：{result['parsed_query']['keywords']}")
                print(f"找到 {result['total_results']} 个商品\n")
            
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"错误：{e}\n")


if __name__ == "__main__":
    main()
