#!/usr/bin/env python3
"""
collectors/adapters - 文档适配器系统

提供统一的文档适配器接口和结构化提取能力。

目录结构:
    adapters/
    ├── __init__.py           # 本模块（自动导入所有适配器）
    ├── base.py               # DocAdapter基类和注册表
    │
    ├── builtin/              # 内置适配器
    │   ├── cloud_docs/       # 云厂商文档
    │   │   ├── aliyun.py     # 阿里云文档
    │   │   ├── tencent.py    # 腾讯云文档
    │   │   ├── volcengine.py # 火山引擎文档
    │   │   └── coze.py       # Coze文档
    │   ├── api_docs/         # API文档
    │   │   ├── kimi.py       # Kimi API
    │   │   └── minimax.py    # MiniMax API
    │   └── social/            # 社交媒体
    │       ├── github.py     # GitHub
    │       ├── zhihu.py      # 知乎
    │       ├── juejin.py     # 掘金
    │       └── csdn.py       # CSDN
    │
    └── extraction/           # 提取能力
        ├── structure.py      # 结构化数据模型
        └── spawait.py        # 动态等待

自动导入: 导入本模块时自动注册所有内置适配器
    from collectors.adapters import get_registry
    registry = get_registry()  # 已包含所有适配器

Usage:
    from collectors.adapters import DocAdapter, AdapterRegistry

    # 获取适配器（自动注册所有内置适配器）
    registry = get_registry()
    adapter = registry.get_for_url('https://help.aliyun.com/doc')
    
    # 提取文档
    doc = adapter.extract(page, url)
"""

from .base import (
    # 基类
    BaseAdapter,
    DocAdapter,
    
    # 注册表
    AdapterRegistry,
    get_registry,
    register_adapter,
    detect_adapter,
    
    # 选择器
    DEFAULT_SELECTORS,
)

from .extraction.structure import (
    DocumentItem,
    HeadingItem,
    CodeBlock,
    TableItem,
    ImageItem,
    ApiEndpoint,
    ModelInfo,
)

# ==================== 自动导入并注册所有内置适配器 ====================
# 确保导入本模块时，所有适配器都已注册到全局注册表

# 云厂商文档适配器
try:
    from .builtin.cloud_docs import (
        AliyunDocAdapter,
        TencentDocAdapter,
        VolcengineDocAdapter,
        CozeDocAdapter,
    )
    # 注册到全局注册表
    register_adapter('aliyun', AliyunDocAdapter())
    register_adapter('tencent', TencentDocAdapter())
    register_adapter('volcengine', VolcengineDocAdapter())
    register_adapter('coze', CozeDocAdapter())
except ImportError:
    pass

# API文档适配器
try:
    from .builtin.api_docs import (
        KimiApiAdapter,
        MiniMaxApiAdapter,
    )
    # 注册到全局注册表
    register_adapter('kimi', KimiApiAdapter())
    register_adapter('minimax', MiniMaxApiAdapter())
except ImportError:
    pass

# 社交媒体适配器
try:
    from .builtin.social import (
        GitHubAdapter,
        ZhihuAdapter,
        JuejinAdapter,
        CsdnAdapter,
    )
    # 注册到全局注册表
    register_adapter('github', GitHubAdapter())
    register_adapter('zhihu', ZhihuAdapter())
    register_adapter('juejin', JuejinAdapter())
    register_adapter('csdn', CsdnAdapter())
except ImportError:
    pass

# 向后兼容：旧路径导入
from .base import DocAdapter as DocAdapterBase
from .base import AdapterRegistry as AdapterRegistryBase

__all__ = [
    # 基类
    'BaseAdapter',
    'DocAdapter',
    
    # 注册表
    'AdapterRegistry',
    'get_registry',
    'register_adapter',
    'detect_adapter',
    
    # 选择器
    'DEFAULT_SELECTORS',
    
    # 结构化数据
    'DocumentItem',
    'HeadingItem',
    'CodeBlock',
    'TableItem',
    'ImageItem',
    'ApiEndpoint',
    'ModelInfo',
    
    # 向后兼容
    'DocAdapterBase',
    'AdapterRegistryBase',
]

# 版本信息
__version__ = '1.2.0'