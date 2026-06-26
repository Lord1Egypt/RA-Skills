#!/usr/bin/env python3
"""
知乎专用处理器 - 处理 zhihu.com 的链接
特点：需要处理富文本、公式、代码块
"""

import sys
import os
import time
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(script_dir))

from .base_handler import BaseURLHandler, register_handler, FetchResult
from typing import Any, Dict, List


@register_handler
class ZhihuHandler(BaseURLHandler):
    """知乎处理器"""
    
    SITE_TYPE = "zhihu"
    SITE_NAME = "Zhihu"
    DOMAIN = "zhihu.com"
    
    config = {
        "needs_js": True,
        "wait_time": 3,
        "scroll_count": 5,
        "scroll_delay": 1.0,
        "anti_detection": True,
        "use_persistent_context": False,
        "content_selectors": [
            ".Post-RichText",  # 知乎回答正文
            ".RichText",
            ".RichText-inner",
            "article",
            "body"
        ],
        "title_selectors": [
            "meta[property='og:title']",
            "h1.Post-Title",
            "h1",
            "title"
        ],
        "headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://www.zhihu.com/",
        }
    }
    
    def fetch(self, page: Any) -> FetchResult:
        """抓取知乎内容"""
        try:
            # 1. 等待页面加载
            try:
                page.wait_for_load_state("networkidle", timeout=10000)
            except:
                time.sleep(self.config.get("wait_time", 3))
            
            # 2. 滚动加载更多内容（知乎有懒加载）
            self._scroll_to_load(page)
            
            # 3. 提取标题
            title = self.extract_title(page)
            
            # 4. 提取内容
            html, text = self.extract_content(page)
            
            if not html:
                self.result.error = "未找到回答内容"
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
                "site_type": "zhihu"
            }
            
            return self.result
            
        except Exception as e:
            self.result.error = str(e)
            return self.result
    
    def _scroll_to_load(self, page: Any):
        """滚动加载（知乎特殊处理）"""
        scroll_config = self.get_scroll_config()
        
        for i in range(scroll_config["count"]):
            page.evaluate(f"window.scrollBy(0, 600)")
            time.sleep(scroll_config["delay"])
            
            # 检查是否还有更多内容
            try:
                has_more = page.query_selector(".Button--loading")
                if not has_more:
                    break
            except:
                pass
        
        page.evaluate("window.scrollTo(0, 0)")
        time.sleep(1)
    
    def _extract_images(self, page: Any) -> List[Dict]:
        """提取图片（知乎特殊处理）"""
        images = []
        try:
            # 知乎图片通常在 figure 标签内
            figure_elements = page.query_selector_all("figure")
            for i, figure in enumerate(figure_elements[:20]):
                img = figure.query_selector("img")
                if img:
                    src = img.get_attribute("src") or img.get_attribute("data-src")
                    alt = img.get_attribute("alt") or figure.get_attribute("aria-label") or f"图片{i+1}"
                    
                    if src and src.startswith("http"):
                        images.append({
                            "src": src,
                            "alt": alt,
                            "index": i + 1
                        })
        except:
            pass
        
        return images
