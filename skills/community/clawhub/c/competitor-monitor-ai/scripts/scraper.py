#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
竞品数据抓取模块
支持多平台数据抓取和截图
"""

import re
import json
import time
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Any
from urllib.parse import urlparse

# 尝试导入playwright
try:
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False
    print("警告: 未安装Playwright，请运行: pip install playwright && playwright install chromium")


class DataScraper:
    """数据抓取器"""
    
    # 平台预设选择器
    PLATFORM_SELECTORS = {
        'douyin': {
            'likes': '[data-e2e="like-count"], .video-count .like-count, span[class*="like"]',
            'comments': '[data-e2e="comment-count"], .video-count .comment-count',
            'shares': '[data-e2e="share-count"], .video-count .share-count',
            'views': '[data-e2e="play-count"], .video-count .play-count',
            'title': '.title, .video-title, h1'
        },
        'xiaohongshu': {
            'likes': '.like-wrapper .count, .interaction-item .like-count',
            'collections': '.collect-wrapper .count, .interaction-item .collect-count',
            'comments': '.comment-wrapper .count, .interaction-item .comment-count',
            'title': '.title, .note-title, h1'
        },
        'weibo': {
            'likes': '.woo-like-count, .toolbar .like-count',
            'comments': '.woo-comment-count, .toolbar .comment-count',
            'reposts': '.woo-repost-count, .toolbar .repost-count',
            'views': '.woo-read-count, .toolbar .read-count',
            'title': '.weibo-text, .wbpro-text, .detail-text'
        },
        'bilibili': {
            'likes': '.video-like .like-text, .like span',
            'coins': '.video-coin .coin-text, .coin span',
            'collections': '.video-fav .fav-text, .fav span',
            'views': '.view-text, .play-count',
            'comments': '.reply-item, .comment-count',
            'title': '.video-title, h1.title'
        },
        'kuaishou': {
            'likes': '.like-count, .video-like-count',
            'comments': '.comment-count, .video-comment-count',
            'views': '.play-count, .video-play-count',
            'title': '.video-title, h1'
        },
        'taobao': {
            'sell_count': '.sell-count, [data-spm="sellercount"]',
            'rate_count': '.rate-count, [data-spm="ratecount"]',
            'price': '.price, .tb-rmb-num',
            'title': '.tb-detail-hd h1, .item-title'
        },
        'jd': {
            'sell_count': '#comment-count, .comment-count',
            'price': '.price, .p-price .price',
            'title': '.sku-name, .product-intro h1'
        },
        'pdd': {
            'sell_count': '.sold-num, [data-testid="sold-num"]',
            'price': '.price, [data-testid="price"]',
            'title': '.goods-name, h1'
        }
    }
    
    def __init__(self, headless: bool = True, timeout: int = 30):
        self.headless = headless
        self.timeout = timeout
        self.browser = None
        self.context = None
        self.page = None
        
    def __enter__(self):
        """上下文管理器入口"""
        if not HAS_PLAYWRIGHT:
            raise ImportError("请先安装Playwright: pip install playwright && playwright install chromium")
        
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=self.headless)
        self.context = self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        self.page = self.context.new_page()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if hasattr(self, 'playwright'):
            self.playwright.stop()
    
    def detect_platform(self, url: str) -> Optional[str]:
        """从URL检测平台类型"""
        domain = urlparse(url).netloc.lower()
        
        platform_map = {
            'douyin': 'douyin',
            'iesdouyin': 'douyin',
            'xiaohongshu': 'xiaohongshu',
            'weibo': 'weibo',
            'bilibili': 'bilibili',
            'b23.tv': 'bilibili',
            'kuaishou': 'kuaishou',
            'taobao': 'taobao',
            'tmall': 'taobao',
            'jd': 'jd',
            'pinduoduo': 'pdd',
            'yangkeduo': 'pdd'
        }
        
        for key, platform in platform_map.items():
            if key in domain:
                return platform
        
        return None
    
    def scrape(self, url: str, platform: str = None, screenshot: bool = False,
               screenshot_path: str = None) -> Dict[str, Any]:
        """
        抓取页面数据
        
        Args:
            url: 页面URL
            platform: 平台类型，不指定则自动检测
            screenshot: 是否截图
            screenshot_path: 截图保存路径
            
        Returns:
            抓取结果字典
        """
        result = {
            'url': url,
            'timestamp': datetime.now().isoformat(),
            'platform': platform or self.detect_platform(url),
            'success': False,
            'data': {},
            'screenshot': None,
            'error': None
        }
        
        try:
            # 访问页面
            print(f"正在访问: {url}")
            self.page.goto(url, wait_until='networkidle', timeout=self.timeout * 1000)
            
            # 等待页面加载
            time.sleep(2)
            
            # 获取平台选择器
            platform = result['platform']
            if not platform or platform not in self.PLATFORM_SELECTORS:
                result['error'] = f"不支持的平台或未识别的URL: {url}"
                return result
            
            selectors = self.PLATFORM_SELECTORS[platform]
            
            # 抓取数据
            for metric, selector in selectors.items():
                try:
                    value = self._extract_number(selector)
                    if value is not None:
                        result['data'][metric] = value
                except Exception as e:
                    print(f"抓取 {metric} 失败: {e}")
            
            # 截图
            if screenshot:
                if screenshot_path is None:
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    screenshot_path = f"screenshot_{timestamp}.png"
                
                self.page.screenshot(path=screenshot_path, full_page=True)
                result['screenshot'] = screenshot_path
                print(f"截图已保存: {screenshot_path}")
            
            result['success'] = True
            print(f"抓取成功: {result['data']}")
            
        except PlaywrightTimeout:
            result['error'] = "页面加载超时"
        except Exception as e:
            result['error'] = str(e)
            print(f"抓取失败: {e}")
        
        return result
    
    def _extract_number(self, selector: str) -> Optional[int]:
        """从页面元素提取数字"""
        # 尝试多个选择器
        selectors = selector.split(',')
        
        for sel in selectors:
            sel = sel.strip()
            try:
                # 等待元素出现
                element = self.page.locator(sel).first
                if element.is_visible():
                    text = element.inner_text()
                    return self._parse_number(text)
            except:
                continue
        
        return None
    
    def _parse_number(self, text: str) -> Optional[int]:
        """解析数字文本"""
        if not text:
            return None
        
        # 移除空白字符
        text = text.strip()
        
        # 匹配数字（支持万、千、百万等单位）
        patterns = [
            r'(\d+\.?\d*)\s*万',  # 1.2万
            r'(\d+\.?\d*)\s*千',  # 1.5千
            r'(\d+\.?\d*)\s*百万',  # 1.5百万
            r'(\d+\.?\d*)\s*亿',  # 1.2亿
            r'(\d+)',  # 普通数字
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                num = float(match.group(1))
                
                # 转换单位
                if '万' in text:
                    num *= 10000
                elif '千' in text:
                    num *= 1000
                elif '百万' in text:
                    num *= 1000000
                elif '亿' in text:
                    num *= 100000000
                
                return int(num)
        
        return None
    
    def scrape_batch(self, urls: list, screenshot: bool = False) -> list:
        """批量抓取"""
        results = []
        for url in urls:
            result = self.scrape(url, screenshot=screenshot)
            results.append(result)
            time.sleep(2)  # 避免请求过快
        return results


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description='竞品数据抓取工具')
    parser.add_argument('--url', '-u', required=True, help='要抓取的页面URL')
    parser.add_argument('--platform', '-p', help='平台类型（自动检测）')
    parser.add_argument('--screenshot', '-s', action='store_true', help='是否截图')
    parser.add_argument('--output', '-o', help='输出文件路径')
    parser.add_argument('--headless', action='store_true', default=True, help='无头模式')
    
    args = parser.parse_args()
    
    with DataScraper(headless=args.headless) as scraper:
        result = scraper.scrape(
            url=args.url,
            platform=args.platform,
            screenshot=args.screenshot
        )
    
    # 输出结果
    output = json.dumps(result, ensure_ascii=False, indent=2)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"结果已保存: {args.output}")
    else:
        print(output)


if __name__ == '__main__':
    main()
