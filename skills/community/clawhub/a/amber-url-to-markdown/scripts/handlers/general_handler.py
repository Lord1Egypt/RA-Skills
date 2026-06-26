#!/usr/bin/env python3
"""
通用网页处理器 - 处理没有特殊要求的网站
"""

import sys
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(script_dir))

from .base_handler import BaseURLHandler, register_handler, FetchResult
from typing import Any, Dict, List


@register_handler
class GeneralHandler(BaseURLHandler):
    """通用网页处理器"""
    
    SITE_TYPE = "general"
    SITE_NAME = "General Web Page"
    DOMAIN = "*"  # 通配符，匹配所有未注册的域名
    
    config = {
        "needs_js": False,
        "wait_time": 2,
        "scroll_count": 0,
        "scroll_delay": 1.0,
        "anti_detection": False,
        "use_persistent_context": False,
        "content_selectors": [
            "article",
            "[role='article']",
            ".post-content",
            ".article-content",
            ".entry-content",
            ".content",
            "main",
            "body"
        ],
        "title_selectors": [
            "meta[property='og:title']",
            "meta[name='title']",
            "h1",
            "title"
        ],
        "headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        }
    }
    
    def fetch(self, page: Any) -> FetchResult:
        """抓取通用网页内容"""
        try:
            # 提取标题
            title = self.extract_title(page)
            
            # 提取内容
            html, text = self.extract_content(page)
            
            if not html:
                self.result.error = "未找到正文内容"
                return self.result
            
            # 提取图片
            images = self._extract_images(page)
            
            self.result.success = True
            self.result.title = title
            self.result.html = html
            self.result.content = text  # 后续会转换为 Markdown
            self.result.images = images
            self.result.metadata = {
                "text_length": len(text),
                "html_length": len(html),
                "image_count": len(images)
            }
            
            return self.result
            
        except Exception as e:
            self.result.error = str(e)
            return self.result
    
    def _extract_images(self, page: Any) -> List[Dict]:
        """提取页面图片"""
        images = []
        try:
            img_elements = page.query_selector_all("img")
            for i, img in enumerate(img_elements[:20]):  # 最多 20 张
                src = img.get_attribute("src") or img.get_attribute("data-src")
                alt = img.get_attribute("alt") or f"图片{i+1}"
                
                if src and src.startswith("http"):
                    images.append({
                        "src": src,
                        "alt": alt,
                        "index": i + 1
                    })
        except:
            pass
        
        return images
