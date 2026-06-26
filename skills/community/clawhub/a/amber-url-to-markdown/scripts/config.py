#!/usr/bin/env python3
"""
Amber Url to Markdown - 全局配置模块
统一管理所有参数，避免硬编码

作者：小文
时间：2026-03-24
版本：V3.1
"""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class FetchConfig:
    """请求配置"""
    # 浏览器 UA 模拟
    USER_AGENT: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    
    # 超时设置（秒）
    TIMEOUT: int = 30
    PLAYWRIGHT_TIMEOUT: int = 30000  # 毫秒
    NETWORKIDLE_TIMEOUT: int = 10000  # 毫秒
    
    # 重试机制
    RETRY_TIMES: int = 2
    RETRY_DELAY: float = 1.0  # 秒
    
    # 请求头
    ACCEPT: str = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    ACCEPT_LANGUAGE: str = "zh-CN,zh;q=0.9,en;q=0.8"
    CONNECTION: str = "keep-alive"
    
    # 代理池（可选，用于反爬严格的网站）
    PROXY_POOL: Optional[List[str]] = None
    # PROXY_POOL = ["http://127.0.0.1:7890", "http://127.0.0.1:7891"]
    
    # 随机延迟（批量请求时使用）
    RANDOM_DELAY_MIN: float = 1.0
    RANDOM_DELAY_MAX: float = 3.0


@dataclass
class ConvertConfig:
    """Markdown 转换配置"""
    # 标题样式（ATX=# 标题，UNDERLINED=下划线）
    HEADING_STYLE: str = "ATX"
    
    # 列表符号
    BULLETS: str = "-"
    
    # 代码块默认语言
    CODE_LANGUAGE: str = "text"
    
    # 要移除的标签
    STRIP_TAGS: list = None
    
    # 特殊元素保留
    KEEP_CODE_BLOCK: bool = True
    KEEP_LATEX: bool = True
    KEEP_TABLES: bool = True
    
    # 转义控制
    ESCAPE_UNDERSCORES: bool = False  # 禁用下划线转义（避免图片路径问题）
    ESCAPE_MISC: bool = False  # 禁用其他字符转义
    
    def __post_init__(self):
        if self.STRIP_TAGS is None:
            self.STRIP_TAGS = ['script', 'style', 'iframe', 'noscript']


@dataclass
class OutputConfig:
    """输出配置"""
    # 默认输出目录
    DEFAULT_OUTPUT_DIR: str = "/root/openclaw/urltomarkdown"
    
    # 图片配置
    DOWNLOAD_IMAGES: bool = True
    IMAGE_TIMEOUT: int = 10
    IMAGE_PREFIX: str = "img_"
    
    # 文件命名
    MAX_TITLE_LENGTH: int = 50
    
    # 时间戳格式
    TIMESTAMP_FORMAT: str = "%Y%m%d_%H%M%S"
    DATETIME_FORMAT: str = "%Y-%m-%d %H:%M:%S"
    
    # 目录结构
    IMAGES_DIR_PREFIX: str = "knowledge_"
    IMAGES_SUBDIR: str = "images"


@dataclass
class SiteConfig:
    """网站特定配置"""
    # 微信公众号
    WECHAT: dict = None
    
    # 知乎
    ZHIHU: dict = None
    
    # 掘金
    JUEJIN: dict = None
    
    def __post_init__(self):
        if self.WECHAT is None:
            self.WECHAT = {
                "content_selectors": ["#js_content", ".rich_media_content", "article"],
                "title_selectors": ["meta[property='og:title']", "#activity-name", "h1"],
                "needs_js": True,
                "wait_time": 3,
            }
        
        if self.ZHIHU is None:
            self.ZHIHU = {
                "content_selectors": [".Post-RichText", ".RichText", "article"],
                "title_selectors": ["meta[property='og:title']", "h1.Post-Title"],
                "needs_js": True,
                "wait_time": 3,
            }
        
        if self.JUEJIN is None:
            self.JUEJIN = {
                "content_selectors": [".article-content", "article"],
                "title_selectors": ["meta[property='og:title']", "h1.article-title"],
                "needs_js": True,
                "wait_time": 3,
            }


# 全局单例
fetch_config = FetchConfig()
convert_config = ConvertConfig()
output_config = OutputConfig()
site_config = SiteConfig()


def get_fetch_config() -> FetchConfig:
    """获取请求配置"""
    return fetch_config


def get_convert_config() -> ConvertConfig:
    """获取转换配置"""
    return convert_config


def get_output_config() -> OutputConfig:
    """获取输出配置"""
    return output_config


def get_site_config() -> SiteConfig:
    """获取网站配置"""
    return site_config
