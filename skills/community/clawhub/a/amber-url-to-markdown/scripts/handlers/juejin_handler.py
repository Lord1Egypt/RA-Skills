#!/usr/bin/env python3
"""
掘金专用处理器 - 处理 juejin.cn 的链接
特点：需要处理代码高亮、Markdown 渲染
"""

import sys
import os
import time
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(script_dir))

from .base_handler import BaseURLHandler, register_handler, FetchResult
from typing import Any, Dict, List


@register_handler
class JuejinHandler(BaseURLHandler):
    """掘金处理器"""
    
    SITE_TYPE = "juejin"
    SITE_NAME = "Juejin"
    DOMAIN = "juejin.cn"
    
    config = {
        "needs_js": True,
        "wait_time": 3,
        "scroll_count": 3,
        "scroll_delay": 1.0,
        "anti_detection": False,
        "use_persistent_context": False,
        "content_selectors": [
            ".article-content",  # 掘金文章正文
            "article",
            ".markdown-body",
            "body"
        ],
        "title_selectors": [
            "meta[property='og:title']",
            "h1.article-title",
            "h1",
            "title"
        ],
        "headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://juejin.cn/",
        }
    }
    
    def fetch(self, page: Any) -> FetchResult:
        """抓取掘金文章"""
        try:
            # 1. 等待页面加载
            try:
                page.wait_for_load_state("networkidle", timeout=10000)
            except:
                time.sleep(self.config.get("wait_time", 3))
            
            # 2. 滚动加载
            self._scroll_to_load(page)
            
            # 3. 提取标题
            title = self.extract_title(page)
            
            # 4. 提取内容
            html, text = self.extract_content(page)
            
            if not html:
                self.result.error = "未找到文章内容"
                return self.result
            
            # 5. 提取图片
            images = self._extract_images(page)
            
            self.result.success = True
            self.result.title = title
            self.result.html = html
            self.result.content = text
            self.result.images = images
            self.result.metadata = {
                "text_length": len(text),
                "html_length": len(html),
                "image_count": len(images),
                "site_type": "juejin"
            }
            
            return self.result
            
        except Exception as e:
            self.result.error = str(e)
            return self.result
    
    def _scroll_to_load(self, page: Any):
        """滚动加载"""
        scroll_config = self.get_scroll_config()
        for i in range(scroll_config["count"]):
            page.evaluate(f"window.scrollBy(0, 500)")
            time.sleep(scroll_config["delay"])
        page.evaluate("window.scrollTo(0, 0)")
    
    def _extract_images(self, page: Any) -> List[Dict]:
        """提取图片"""
        images = []
        try:
            content_el = page.query_selector(".article-content")
            if content_el:
                img_elements = content_el.query_selector_all("img")
                for i, img in enumerate(img_elements[:20]):
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
