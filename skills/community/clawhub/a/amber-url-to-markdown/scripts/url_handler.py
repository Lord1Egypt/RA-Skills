#!/usr/bin/env python3
"""
Amber Url to Markdown - URL 链接类型识别处理器
支持可扩展的链接类型识别和定制化抓取策略

作者：小文
时间：2026-03-22
版本：V2.1
"""

import re
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass
from enum import Enum


class LinkType(Enum):
    """链接类型枚举"""
    WECHAT = "wechat"  # 微信公众号
    ZHIHU = "zhihu"  # 知乎
    JUEJIN = "juejin"  # 掘金
    CSDN = "csdn"  # CSDN
    GITHUB = "github"  # GitHub
    MEDIUM = "medium"  # Medium
    DOUBAO = "doubao"  # 豆包
    GENERAL = "general"  # 通用网页
    UNKNOWN = "unknown"  # 未知类型


@dataclass
class LinkConfig:
    """链接配置"""
    link_type: LinkType
    name: str
    domain: str
    content_selectors: List[str]  # 正文内容选择器列表（按优先级）
    title_selectors: List[str]  # 标题选择器列表
    image_selectors: List[str]  # 图片选择器列表
    headers: Dict[str, str]  # 自定义请求头
    wait_time: int = 3  # 等待时间（秒）
    needs_js: bool = True  # 是否需要执行 JavaScript
    extra_config: Dict = None  # 额外配置


class URLHandler:
    """URL 处理器"""
    
    def __init__(self):
        self.domain_map: Dict[str, LinkType] = {}
        self.configs: Dict[LinkType, LinkConfig] = {}
        self._init_builtin_configs()
    
    def _init_builtin_configs(self):
        """初始化内置配置"""
        
        # 微信公众号
        self.register_config(LinkConfig(
            link_type=LinkType.WECHAT,
            name="WeChat Official Account",
            domain="mp.weixin.qq.com",
            content_selectors=[
                "#js_content",
                ".rich_media_content",
                "article",
                "body"
            ],
            title_selectors=[
                "meta[property='og:title']",
                "#activity-name",
                "h1",
                "title"
            ],
            image_selectors=["img"],
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Referer": "https://mp.weixin.qq.com/",
            },
            wait_time=3,
            needs_js=True
        ))
        
        # 知乎
        self.register_config(LinkConfig(
            link_type=LinkType.ZHIHU,
            name="Zhihu",
            domain="zhihu.com",
            content_selectors=[
                ".Post-RichText",
                ".RichText",
                "article",
                "[data-zhihu='post-content']",
                "body"
            ],
            title_selectors=[
                "meta[property='og:title']",
                "h1.Post-Title",
                "h1",
                "title"
            ],
            image_selectors=["img"],
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Referer": "https://www.zhihu.com/",
            },
            wait_time=3,
            needs_js=True
        ))
        
        # 掘金
        self.register_config(LinkConfig(
            link_type=LinkType.JUEJIN,
            name="Juejin",
            domain="juejin.cn",
            content_selectors=[
                ".article-content",
                "article",
                "body"
            ],
            title_selectors=[
                "meta[property='og:title']",
                "h1.article-title",
                "h1",
                "title"
            ],
            image_selectors=["img"],
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Referer": "https://juejin.cn/",
            },
            wait_time=3,
            needs_js=True
        ))
        
        # CSDN
        self.register_config(LinkConfig(
            link_type=LinkType.CSDN,
            name="CSDN",
            domain="blog.csdn.net",
            content_selectors=[
                "#content_views",
                ".article_content",
                "article",
                "body"
            ],
            title_selectors=[
                "meta[property='og:title']",
                "h1.title-article",
                "h1",
                "title"
            ],
            image_selectors=["img"],
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Referer": "https://blog.csdn.net/",
            },
            wait_time=3,
            needs_js=True
        ))
        
        # GitHub
        self.register_config(LinkConfig(
            link_type=LinkType.GITHUB,
            name="GitHub",
            domain="github.com",
            content_selectors=[
                ".markdown-body",
                "article",
                "body"
            ],
            title_selectors=[
                "meta[property='og:title']",
                "h1",
                "title"
            ],
            image_selectors=["img"],
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Referer": "https://github.com/",
            },
            wait_time=2,
            needs_js=False  # GitHub 静态内容多
        ))
        
        # Medium
        self.register_config(LinkConfig(
            link_type=LinkType.MEDIUM,
            name="Medium",
            domain="medium.com",
            content_selectors=[
                "article",
                ".postArticle-content",
                "body"
            ],
            title_selectors=[
                "meta[property='og:title']",
                "h1",
                "title"
            ],
            image_selectors=["img"],
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Referer": "https://medium.com/",
            },
            wait_time=3,
            needs_js=True
        ))
        
        # 豆包 - 使用 Playwright 方案（需要完整 Headers + JS 渲染）
        self.register_config(LinkConfig(
            link_type=LinkType.DOUBAO,
            name="Doubao Thread",
            domain="doubao.com",
            content_selectors=[
                "[class*='message']",  # 豆包消息容器（优先级最高）
                ".thread-content",
                ".conversation-content",
                "[class*='content']",
                ".markdown-body",
                "body"  # 最后使用 body 作为后备
            ],
            title_selectors=[
                "meta[property='og:title']",
                ".thread-title",
                "title",
                "h1"
            ],
            image_selectors=["img"],
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
                "Referer": "https://www.doubao.com/",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
            },
            wait_time=5,
            needs_js=True,  # 需要 JS 渲染
            extra_config={
                "anti_detection": True,
                "scroll_delay": 1.5,
                "random_mouse_move": False,
                "viewport_delay": 3
            }
        ))
        
        # 通用网页
        self.register_config(LinkConfig(
            link_type=LinkType.GENERAL,
            name="General Web Page",
            domain="*",
            content_selectors=[
                "article",
                "[role='article']",
                ".post-content",
                ".article-content",
                ".entry-content",
                ".content",
                "main",
                "body"
            ],
            title_selectors=[
                "meta[property='og:title']",
                "meta[name='title']",
                "h1",
                "title"
            ],
            image_selectors=["img"],
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            },
            wait_time=2,
            needs_js=False
        ))
    
    def register_config(self, config: LinkConfig):
        """注册链接配置"""
        self.configs[config.link_type] = config
        self.domain_map[config.domain] = config.link_type
    
    def identify_link_type(self, url: str) -> LinkType:
        """识别链接类型"""
        from urllib.parse import urlparse
        
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        
        # 移除 www.
        if domain.startswith("www."):
            domain = domain[4:]
        
        # 精确匹配
        if domain in self.domain_map:
            return self.domain_map[domain]
        
        # 模糊匹配（子域名）
        for registered_domain, link_type in self.domain_map.items():
            if domain.endswith(registered_domain):
                return link_type
        
        # 默认返回通用类型
        return LinkType.GENERAL
    
    def get_config(self, url: str) -> LinkConfig:
        """获取链接配置"""
        link_type = self.identify_link_type(url)
        return self.configs.get(link_type, self.configs[LinkType.GENERAL])
    
    def add_custom_config(self, config: LinkConfig):
        """添加自定义配置（用于扩展）"""
        self.register_config(config)
        print(f"[INFO] 已添加自定义配置：{config.name}")
    
    def list_supported_types(self) -> List[Dict]:
        """列出支持的链接类型"""
        return [
            {
                "type": config.link_type.value,
                "name": config.name,
                "domain": config.domain,
                "selectors": config.content_selectors[:3],  # 只显示前 3 个
            }
            for config in self.configs.values()
        ]


# 全局单例
url_handler = URLHandler()


# 快捷函数
def identify_url(url: str) -> LinkType:
    """识别链接类型"""
    return url_handler.identify_link_type(url)


def get_url_config(url: str) -> LinkConfig:
    """获取链接配置"""
    return url_handler.get_config(url)


def register_custom_link(config: LinkConfig):
    """注册自定义链接类型"""
    url_handler.add_custom_config(config)


if __name__ == "__main__":
    # 测试
    test_urls = [
        "https://mp.weixin.qq.com/s/xxx",
        "https://zhuanlan.zhihu.com/p/xxx",
        "https://juejin.cn/post/xxx",
        "https://blog.csdn.net/xxx/xxx",
        "https://github.com/xxx/xxx",
        "https://medium.com/@xxx/xxx",
        "https://example.com/article",
    ]
    
    print("=" * 60)
    print("URL 链接类型识别测试")
    print("=" * 60)
    
    for url in test_urls:
        link_type = identify_url(url)
        config = get_url_config(url)
        print(f"\nURL: {url}")
        print(f"类型：{link_type.value} ({config.name})")
        print(f"正文选择器：{config.content_selectors[:3]}")
