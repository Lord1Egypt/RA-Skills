#!/usr/bin/env python3
"""
URL 处理器基类 - 定义统一的接口和规范
所有网站专用处理器都继承此基类
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass


@dataclass
class FetchResult:
    """抓取结果数据结构"""
    success: bool
    title: str
    content: str  # Markdown 格式
    html: str  # 原始 HTML
    images: List[Dict]  # 图片信息列表
    metadata: Dict[str, Any]  # 额外元数据
    error: Optional[str] = None


class BaseURLHandler(ABC):
    """URL 处理器基类"""
    
    # 类变量：网站类型标识
    SITE_TYPE: str = "base"
    SITE_NAME: str = "Base Site"
    DOMAIN: str = ""
    
    # 配置项（子类可覆盖）
    config = {
        "needs_js": True,  # 是否需要 JS 渲染
        "wait_time": 3,  # 基础等待时间（秒）
        "scroll_count": 0,  # 滚动次数
        "scroll_delay": 1.0,  # 滚动间隔（秒）
        "anti_detection": False,  # 是否启用反检测
        "use_persistent_context": False,  # 是否使用持久化上下文
        "content_selectors": ["body"],  # 内容选择器列表
        "title_selectors": ["title", "h1"],  # 标题选择器列表
        "headers": {},  # 自定义请求头
    }
    
    def __init__(self, url: str):
        self.url = url
        self.result = FetchResult(
            success=False,
            title="",
            content="",
            html="",
            images=[],
            metadata={}
        )
    
    @abstractmethod
    def fetch(self, page: Any) -> FetchResult:
        """
        抓取页面内容（核心方法）
        
        Args:
            page: Playwright page 对象
        
        Returns:
            FetchResult: 抓取结果
        """
        pass
    
    def extract_title(self, page: Any) -> str:
        """
        提取页面标题
        
        Args:
            page: Playwright page 对象
        
        Returns:
            str: 标题
        """
        for selector in self.config.get("title_selectors", ["title"]):
            try:
                if selector == "title":
                    title = page.title()
                else:
                    element = page.query_selector(selector)
                    if element:
                        title = element.inner_text().strip()
                    else:
                        continue
                
                if title and len(title.strip()) > 0 and len(title) < 200:
                    return title.strip()
            except:
                continue
        
        return "未命名文章"
    
    def extract_content(self, page: Any) -> Tuple[str, str]:
        """
        提取页面内容
        
        Args:
            page: Playwright page 对象
        
        Returns:
            Tuple[str, str]: (HTML 内容，文本内容)
        """
        for selector in self.config.get("content_selectors", ["body"]):
            try:
                element = page.query_selector(selector)
                if element:
                    html = element.inner_html()
                    text = element.inner_text()
                    return html, text
            except:
                continue
        
        return "", ""
    
    def get_wait_timeout(self) -> int:
        """获取等待超时时间（毫秒）"""
        return self.config.get("wait_time", 3) * 1000
    
    def get_scroll_config(self) -> Dict:
        """获取滚动配置"""
        return {
            "count": self.config.get("scroll_count", 0),
            "delay": self.config.get("scroll_delay", 1.0),
            "height": 600  # 每次滚动高度
        }
    
    def should_use_persistent_context(self) -> bool:
        """是否需要持久化上下文"""
        return self.config.get("use_persistent_context", False)
    
    def get_headers(self) -> Dict:
        """获取自定义请求头"""
        return self.config.get("headers", {})
    
    def __str__(self):
        return f"{self.SITE_NAME} Handler ({self.SITE_TYPE})"


# 处理器注册表
_handler_registry = {}


def register_handler(handler_class):
    """装饰器：注册 URL 处理器"""
    if handler_class.DOMAIN:
        _handler_registry[handler_class.DOMAIN] = handler_class
    return handler_class


def get_handler(url: str) -> BaseURLHandler:
    """
    根据 URL 获取对应的处理器
    
    Args:
        url: 目标 URL
    
    Returns:
        BaseURLHandler: 对应的处理器实例
    """
    from urllib.parse import urlparse
    
    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    
    # 移除 www.
    if domain.startswith("www."):
        domain = domain[4:]
    
    # 精确匹配
    if domain in _handler_registry:
        return _handler_registry[domain](url)
    
    # 模糊匹配（子域名）
    for registered_domain, handler_class in _handler_registry.items():
        if domain.endswith(registered_domain):
            return handler_class(url)
    
    # 默认返回通用处理器
    from handlers.general_handler import GeneralHandler
    return GeneralHandler(url)


def list_handlers() -> List[Dict]:
    """列出所有已注册的处理器"""
    return [
        {
            "type": cls.SITE_TYPE,
            "name": cls.SITE_NAME,
            "domain": cls.DOMAIN,
        }
        for cls in _handler_registry.values()
    ]
