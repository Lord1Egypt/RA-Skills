"""
BiliYouTik2Brain — 平台注册中心（v4.0 插件化改造）

兼容旧版注册方式 + 支持新版插件系统。
平台插件既可以通过 PluginLoader 动态加载，也可以通过 register() 手动注册。

**使用示例**:
    # 新版：插件自动加载
    from .plugin_loader import get_platform_for_url
    plugin = get_platform_for_url(url)

    # 旧版：手动注册（向后兼容）
    from .registry import PlatformRegistry
    PlatformRegistry.register(MyExtractor)
    cls = PlatformRegistry.identify(url)
"""

from typing import Dict, Type, Optional
import re as _re

from ..core.schemas import Platform
from ..platforms.base import BaseExtractor
from ..core.plugin_loader import get_platform_plugins, get_platform_for_url as _plugin_identify


class PlatformRegistry:
    """平台适配器注册中心（向后兼容）"""

    _extractors: Dict[Platform, Type[BaseExtractor]] = {}
    _url_matchers: list = []

    @classmethod
    def register(cls, extractor_cls: Type[BaseExtractor]):
        """注册一个平台适配器"""
        platform = extractor_cls.platform
        cls._extractors[platform] = extractor_cls
        cls._url_matchers.append((extractor_cls.domain_regex, platform))
        cls._url_matchers.sort(key=lambda x: len(x[0]), reverse=True)

    @classmethod
    def identify(cls, url: str) -> Optional[Type[BaseExtractor]]:
        """识别 URL 对应的平台适配器

        优先从插件系统查找，回退到旧版注册表。
        """
        # 1. 先尝试插件系统
        plugin_cls = _plugin_identify(url)
        if plugin_cls:
            # 插件插件 → 包装为 BaseExtractor 兼容层
            return cls._wrap_plugin(plugin_cls, url)

        # 2. 回退旧版
        for regex, platform in cls._url_matchers:
            try:
                if _re.search(regex, url):
                    return cls._extractors.get(platform)
            except _re.error:
                continue

        return None

    @classmethod
    def _wrap_plugin(cls, plugin_cls, url: str):
        """将插件类包装为 BaseExtractor 兼容层（简化版）"""
        # 注意：这里只做最小兼容，完整迁移需要各平台适配器实现
        # 目前返回 None，让调用方直接使用插件接口
        return None

    @classmethod
    def get(cls, platform: Platform) -> Optional[Type[BaseExtractor]]:
        return cls._extractors.get(platform)

    @classmethod
    def list_platforms(cls) -> list:
        """列出所有已注册平台"""
        # 合并旧版和新版
        platforms = list(cls._extractors.keys())
        plugin_platforms = list(get_platform_plugins().keys())
        # 去重
        seen = set()
        result = []
        for p in platforms + plugin_platforms:
            name = str(p) if not isinstance(p, str) else p
            if name not in seen:
                seen.add(name)
                result.append(p)
        return result


# ─── 初始化 ──────────────────────────────────────────────────

def _init_registry():
    """导入所有 platform 模块（旧版兼容）"""
    import importlib
    import pkgutil
    try:
        pkg = importlib.import_module("biliyoutik2brain.platforms")
        for importer, modname, ispkg in pkgutil.iter_modules(pkg.__path__):
            if modname != "__init__":
                try:
                    importlib.import_module(f"biliyoutik2brain.platforms.{modname}")
                except Exception:
                    pass
    except Exception:
        pass


_init_registry()
