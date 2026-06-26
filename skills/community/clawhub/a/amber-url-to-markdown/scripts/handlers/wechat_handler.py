#!/usr/bin/env python3
"""
微信公众号专用处理器 - 处理 mp.weixin.qq.com 的链接
特点：需要特殊代码块处理、图片防盗链
"""

import sys
import os
import time
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(script_dir))

from .base_handler import BaseURLHandler, register_handler, FetchResult
from typing import Any, Dict, List


@register_handler
class WeChatHandler(BaseURLHandler):
    """微信公众号处理器"""
    
    SITE_TYPE = "wechat"
    SITE_NAME = "WeChat Official Account"
    DOMAIN = "mp.weixin.qq.com"
    
    config = {
        "needs_js": True,
        "wait_time": 3,
        "scroll_count": 3,
        "scroll_delay": 1.0,
        "anti_detection": False,
        "use_persistent_context": False,
        "content_selectors": [
            "#js_content",
            ".rich_media_content",
            "article",
            "body"
        ],
        "title_selectors": [
            "meta[property='og:title']",
            "#activity-name",
            "h1",
            "title"
        ],
        "headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://mp.weixin.qq.com/",
        }
    }
    
    def fetch(self, page: Any) -> FetchResult:
        """抓取微信公众号文章"""
        try:
            try:
                page.wait_for_load_state("networkidle", timeout=10000)
            except:
                time.sleep(self.config.get("wait_time", 3))
            
            self._scroll_to_load(page)
            title = self.extract_title(page)
            html, text = self.extract_content(page)
            
            if not html:
                self.result.error = "未找到文章内容"
                return self.result
            
            html = self._optimize_wechat_html(html)
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
                "site_type": "wechat"
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
    
    def _optimize_wechat_html(self, html: str) -> str:
        """优化微信 HTML - 将三重引号代码块转换为标准格式"""
        from bs4 import BeautifulSoup
        import re
        
        soup = BeautifulSoup(html, 'html.parser')
        
        TRIPLE_QUOTE = '"' * 3
        quote_spans = []
        for span in soup.find_all('span'):
            if span.get_text(strip=True) == TRIPLE_QUOTE:
                quote_spans.append(span)
        
        if len(quote_spans) >= 2:
            for i in range(0, len(quote_spans) - 1, 2):
                start_span = quote_spans[i]
                end_span = quote_spans[i + 1]
                
                content_elements = []
                current = start_span.next_sibling
                while current and current != end_span:
                    content_elements.append(current)
                    current = current.next_sibling
                
                if content_elements:
                    code_wrapper = soup.new_tag('pre')
                    code_inner = soup.new_tag('code')
                    code_wrapper.append(code_inner)
                    
                    for elem in content_elements:
                        if hasattr(elem, 'extract'):
                            code_inner.append(elem.extract())
                        else:
                            code_inner.append(soup.new_string(str(elem)))
                    
                    start_span.replace_with(code_wrapper)
                    end_span.extract()
        
        return str(soup)
    
    def _extract_images(self, page: Any) -> List[Dict]:
        """提取图片"""
        images = []
        try:
            content_el = page.query_selector("#js_content")
            if content_el:
                img_elements = content_el.query_selector_all("img")
                for i, img in enumerate(img_elements[:20]):
                    src = img.get_attribute("data-src") or img.get_attribute("src")
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
