#!/usr/bin/env python3
"""
豆包专用处理器 - 处理 doubao.com 的链接
特点：需要持久化上下文、多次滚动、特殊选择器
"""

import sys
import os
import time
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(script_dir))

from .base_handler import BaseURLHandler, register_handler, FetchResult
from typing import Any, Dict, List


@register_handler
class DoubaoHandler(BaseURLHandler):
    """豆包专用处理器"""
    
    SITE_TYPE = "doubao"
    SITE_NAME = "Doubao Thread"
    DOMAIN = "doubao.com"
    
    config = {
        "needs_js": True,
        "wait_time": 5,  # 5 秒基础等待
        "scroll_count": 10,  # 滚动 10 次
        "scroll_delay": 1.5,  # 每次间隔 1.5 秒
        "anti_detection": True,
        "use_persistent_context": True,  # 使用持久化上下文保存登录状态
        "content_selectors": [
            "[class*='message']",  # 豆包消息容器（最精准）
            "[class*='thread']",
            "[class*='content']",
            "body"  # 后备选择器
        ],
        "title_selectors": [
            "meta[property='og:title']",
            "h1",
            "title"
        ],
        "headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Referer": "https://www.doubao.com/",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
        }
    }
    
    def fetch(self, page: Any) -> FetchResult:
        """抓取豆包内容"""
        try:
            # 1. 等待页面完全加载
            self._wait_for_content(page)
            
            # 2. 滚动加载动态内容
            self._scroll_to_load(page)
            
            # 3. 验证内容是否加载成功
            body_text = page.evaluate("() => document.body.innerText")
            if len(body_text) < 100:
                self.result.error = f"内容加载失败，仅获取到{len(body_text)}字符"
                return self.result
            
            # 4. 提取标题
            title = self.extract_title(page)
            
            # 5. 提取内容（使用专用选择器）
            html, text = self._extract_doubao_content(page)
            
            if not html or len(text) < 50:
                self.result.error = "未找到豆包消息内容"
                return self.result
            
            # 6. 提取图片
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
                "site_type": "doubao"
            }
            
            return self.result
            
        except Exception as e:
            self.result.error = str(e)
            return self.result
    
    def _wait_for_content(self, page: Any):
        """等待内容加载"""
        try:
            # 等待 networkidle 状态
            page.wait_for_load_state("networkidle", timeout=15000)
        except:
            # 超时则继续，使用固定等待
            time.sleep(self.config.get("wait_time", 5))
    
    def _scroll_to_load(self, page: Any):
        """滚动加载动态内容"""
        scroll_config = self.get_scroll_config()
        scroll_count = scroll_config["count"]
        scroll_delay = scroll_config["delay"]
        scroll_height = scroll_config["height"]
        
        for i in range(scroll_count):
            page.evaluate(f"window.scrollBy(0, {scroll_height})")
            time.sleep(scroll_delay)
            
            # 每 3 次检查一次内容长度
            if i % 3 == 2:
                check_text = page.evaluate("() => document.body.innerText")
                if len(check_text) > 1000:
                    # 内容已足够，提前结束
                    break
        
        # 滚动回顶部
        page.evaluate("window.scrollTo(0, 0)")
        time.sleep(2)
    
    def _extract_doubao_content(self, page: Any) -> tuple:
        """提取豆包专用内容"""
        # 优先使用 [class*='message'] 选择器
        message_el = page.query_selector("[class*='message']")
        if message_el:
            html = message_el.inner_html()
            text = message_el.inner_text()
            if len(text) > 100:
                return html, text
        
        # 后备：使用通用方法
        return self.extract_content(page)
    
    def _extract_images(self, page: Any) -> List[Dict]:
        """提取图片（豆包特殊处理）"""
        images = []
        try:
            img_elements = page.query_selector_all("[class*='message'] img")
            for i, img in enumerate(img_elements[:10]):
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
