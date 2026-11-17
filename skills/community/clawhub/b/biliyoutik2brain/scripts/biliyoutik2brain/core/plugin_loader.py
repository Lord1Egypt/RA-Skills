"""
BiliYouTik2Brain — 插件加载器 (v4.0)

动态发现、验证、加载插件。
扫描顺序：
  1. 核心插件（core/plugins/）— 随技能内置
  2. 用户插件（plugins/）— 用户自定义
  3. 社区插件（~/.biliyoutik2brain/plugins/）— ClawHub 安装

加载时验证插件是否实现了必需方法，失败时跳过并警告。
"""

import os
import sys
import importlib
import importlib.util
from typing import Dict, List, Type, Optional, Any
from .plugin_base import PlatformPlugin, ASRPlugin, OutputPlugin, PluginMeta


# ═══════════════════════════════════════════════════════════
#  插件注册表
# ═══════════════════════════════════════════════════════════

_platform_plugins: Dict[str, Type[PlatformPlugin]] = {}
_asr_plugins: Dict[str, Type[ASRPlugin]] = {}
_output_plugins: Dict[str, Type[OutputPlugin]] = {}

_load_warnings: List[str] = []


# ═══════════════════════════════════════════════════════════
#  扫描 & 加载
# ═══════════════════════════════════════════════════════════

def _scan_directory(directory: str) -> List[str]:
    """扫描目录下的 Python 文件"""
    if not os.path.isdir(directory):
        return []

    modules = []
    for f in os.listdir(directory):
        if f.endswith(".py") and not f.startswith("_") and f != "plugin_base.py":
            modules.append(os.path.join(directory, f))
        elif os.path.isdir(os.path.join(directory, f)) and not f.startswith("_"):
            init = os.path.join(directory, f, "__init__.py")
            if os.path.exists(init):
                modules.append(os.path.join(directory, f))

    return modules


def _load_module_from_path(path: str) -> Optional[Any]:
    """从路径加载 Python 模块"""
    try:
        if os.path.isdir(path):
            # 目录 → 加载 __init__.py
            init_path = os.path.join(path, "__init__.py")
            if not os.path.exists(init_path):
                return None
            spec = importlib.util.spec_from_file_location(os.path.basename(path), init_path)
        else:
            spec = importlib.util.spec_from_file_location(
                os.path.splitext(os.path.basename(path))[0], path
            )

        if not spec or not spec.loader:
            return None

        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        _load_warnings.append(f"加载模块失败 {path}: {e}")
        return None


def _register_plugin(plugin_cls: Type, plugin_type: str):
    """注册单个插件

    Args:
        plugin_cls: 插件类
        plugin_type: 类型（platform / asr / output）
    """
    try:
        # 验证必需属性
        if not hasattr(plugin_cls, "meta"):
            _load_warnings.append(f"插件 {plugin_cls.__name__} 缺少 meta 属性")
            return

        meta = plugin_cls.meta
        if isinstance(meta, property):
            # 需要实例化才能获取 meta
            try:
                instance = plugin_cls()
                meta = instance.meta
            except Exception:
                meta = PluginMeta(name=plugin_cls.__name__, version="unknown")

        name = meta.name if isinstance(meta, PluginMeta) else plugin_cls.__name__

        if plugin_type == "platform":
            # 验证 PlatformPlugin 必需方法
            required = ["domain_regex", "get_video_info", "download_audio",
                       "download_video", "fetch_subtitles", "fetch_comments",
                       "get_anti_crawl_config"]
            for method in required:
                if not hasattr(plugin_cls, method):
                    _load_warnings.append(f"平台插件 {name} 缺少必需方法: {method}")
                    return
            _platform_plugins[name] = plugin_cls

        elif plugin_type == "asr":
            required = ["transcribe", "get_cost_per_minute", "is_available"]
            for method in required:
                if not hasattr(plugin_cls, method):
                    _load_warnings.append(f"ASR 插件 {name} 缺少必需方法: {method}")
                    return
            _asr_plugins[name] = plugin_cls

        elif plugin_type == "output":
            required = ["format_name", "render"]
            for method in required:
                if not hasattr(plugin_cls, method):
                    _load_warnings.append(f"输出插件 {name} 缺少必需方法: {method}")
                    return
            _output_plugins[name] = plugin_cls

    except Exception as e:
        _load_warnings.append(f"注册插件失败 {plugin_cls.__name__}: {e}")


def _find_plugins_in_module(module: Any):
    """在模块中查找所有插件类"""
    for attr_name in dir(module):
        attr = getattr(module, attr_name)
        if not isinstance(attr, type):
            continue

        # 检查继承关系
        if issubclass(attr, PlatformPlugin) and attr is not PlatformPlugin:
            _register_plugin(attr, "platform")
        elif issubclass(attr, ASRPlugin) and attr is not ASRPlugin:
            _register_plugin(attr, "asr")
        elif issubclass(attr, OutputPlugin) and attr is not OutputPlugin:
            _register_plugin(attr, "output")


# ═══════════════════════════════════════════════════════════
#  公共 API
# ═══════════════════════════════════════════════════════════

def scan_and_load(scan_dirs: Optional[List[str]] = None):
    """扫描并加载所有插件

    Args:
        scan_dirs: 额外扫描目录
    """
    # 默认扫描目录
    dirs = []
    skill_dir = os.path.dirname(os.path.dirname(__file__))

    # 1. 核心插件（内置）
    core_dir = os.path.join(skill_dir, "core", "plugins")
    if os.path.isdir(core_dir):
        dirs.append(core_dir)

    # 2. 用户插件
    user_dir = os.path.join(skill_dir, "plugins")
    if os.path.isdir(user_dir):
        dirs.append(user_dir)

    # 3. 社区插件
    community_dir = os.path.expanduser("~/.biliyoutik2brain/plugins")
    if os.path.isdir(community_dir):
        dirs.append(community_dir)

    # 额外目录
    if scan_dirs:
        dirs.extend(scan_dirs)

    # 扫描
    for d in dirs:
        for path in _scan_directory(d):
            module = _load_module_from_path(path)
            if module:
                _find_plugins_in_module(module)


def register_platform_plugin(plugin_cls: Type[PlatformPlugin]):
    """手动注册平台插件（供内置平台使用）"""
    _register_plugin(plugin_cls, "platform")


def register_asr_plugin(plugin_cls: Type[ASRPlugin]):
    """手动注册 ASR 插件"""
    _register_plugin(plugin_cls, "asr")


def register_output_plugin(plugin_cls: Type[OutputPlugin]):
    """手动注册输出插件"""
    _register_plugin(plugin_cls, "output")


def get_platform_plugins() -> Dict[str, Type[PlatformPlugin]]:
    """获取所有平台插件"""
    return dict(_platform_plugins)


def get_asr_plugins() -> Dict[str, Type[ASRPlugin]]:
    """获取所有 ASR 插件"""
    return dict(_asr_plugins)


def get_output_plugins() -> Dict[str, Type[OutputPlugin]]:
    """获取所有输出插件"""
    return dict(_output_plugins)


def get_platform_for_url(url: str) -> Optional[Type[PlatformPlugin]]:
    """根据 URL 自动匹配平台插件"""
    import re
    for name, cls in _platform_plugins.items():
        try:
            pattern = cls.domain_regex
            if re.search(pattern, url):
                return cls
        except Exception:
            continue
    return None


def get_load_warnings() -> List[str]:
    """获取加载警告"""
    return list(_load_warnings)


def get_plugin_status() -> Dict:
    """获取插件状态概览"""
    return {
        "platform_plugins": {
            name: {
                "is_core": cls.meta.is_core if hasattr(cls, 'meta') else False,
                "version": cls.meta.version if hasattr(cls, 'meta') else "unknown",
            }
            for name, cls in _platform_plugins.items()
        },
        "asr_plugins": {
            name: {
                "is_local": cls.is_local if hasattr(cls, 'is_local') else True,
                "available": cls().is_available() if hasattr(cls, 'is_available') else False,
            }
            for name, cls in _asr_plugins.items()
        },
        "output_plugins": {
            name: {
                "format": cls.format_name if hasattr(cls, 'format_name') else name,
                "extension": cls().file_extension if hasattr(cls, 'file_extension') else ".md",
            }
            for name, cls in _output_plugins.items()
        },
        "warnings": _load_warnings,
    }
