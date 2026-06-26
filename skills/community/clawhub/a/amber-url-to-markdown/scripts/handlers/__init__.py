"""
URL 处理器包 - 支持可扩展的网站分类处理

使用方法：
    from handlers import get_handler
    
    handler = get_handler(url)
    result = handler.fetch(page)
"""

from .base_handler import (
    BaseURLHandler,
    FetchResult,
    register_handler,
    get_handler,
    list_handlers
)

# 自动导入所有处理器（注册到全局注册表）
from .general_handler import GeneralHandler
from .doubao_handler import DoubaoHandler
from .wechat_handler import WeChatHandler
from .zhihu_handler import ZhihuHandler
from .juejin_handler import JuejinHandler

# 导出所有处理器类
__all__ = [
    'BaseURLHandler',
    'FetchResult',
    'register_handler',
    'get_handler',
    'list_handlers',
    'GeneralHandler',
    'DoubaoHandler',
    'WeChatHandler',
    'ZhihuHandler',
    'JuejinHandler',
]

# 打印已注册的处理器（调试用）
def _print_registered_handlers():
    handlers = list_handlers()
    print(f"已注册 {len(handlers)} 个 URL 处理器:")
    for h in handlers:
        print(f"  - {h['name']} ({h['type']}): {h['domain']}")

# 模块加载时自动打印
# _print_registered_handlers()
