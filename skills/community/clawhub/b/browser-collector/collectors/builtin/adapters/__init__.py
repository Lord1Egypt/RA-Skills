"""
collectors/builtin/adapters/ - 站点适配器（兼容层）

⚠️ DEPRECATED: 
    新版适配器已迁移到 collectors/adapters/ 目录
    - collectors/adapters/base.py - 新基类 DocAdapter
    - collectors/adapters/builtin/cloud_docs/ - 云厂商文档
    - collectors/adapters/builtin/api_docs/ - API文档
    - collectors/adapters/builtin/social/ - 社交媒体
    
    此目录仅为向后兼容保留，不再维护。
    新功能请使用 collectors.adapters 模块。

真实适配器位置:
    collectors/adapters/builtin/
    ├── cloud_docs/      # 云厂商文档 (aliyun, tencent, volcengine, coze)
    ├── api_docs/        # API文档 (kimi, minimax)
    └── social/          # 社交媒体 (github, zhihu, juejin, csdn)

Usage:
    # 新版（推荐）
    from collectors.adapters.builtin.cloud_docs import AliyunDocAdapter
    from collectors.adapters import get_registry
    
    # 旧版（兼容）
    from collectors.builtin.adapters import GitHubAdapter
"""

# 向后兼容导入 - 尝试从新路径导入
# 注意：旧文件（base.py, github.py, zhihu.py等）已不存在
# 只从新路径导入

try:
    from collectors.adapters.builtin.social.github import GitHubAdapter
except (ImportError, TypeError):
    GitHubAdapter = None

try:
    from collectors.adapters.builtin.social.zhihu import ZhihuAdapter
except (ImportError, TypeError):
    ZhihuAdapter = None

try:
    from collectors.adapters.builtin.social.juejin import JuejinAdapter
except (ImportError, TypeError):
    JuejinAdapter = None

try:
    from collectors.adapters.builtin.social.csdn import CsdnAdapter
except (ImportError, TypeError):
    CsdnAdapter = None

try:
    from collectors.adapters.builtin.cloud_docs.aliyun import AliyunDocAdapter
except (ImportError, TypeError):
    AliyunDocAdapter = None

# BaseAdapter 和 AdapterRegistry（向后兼容）
try:
    from collectors.adapters.base import BaseAdapter, AdapterRegistry
except ImportError:
    BaseAdapter = None
    AdapterRegistry = None

# AliyunAdapter（旧版占位，不可用）
AliyunAdapter = None

__all__ = [
    'BaseAdapter',
    'AdapterRegistry',
    'GitHubAdapter',
    'ZhihuAdapter',
    'JuejinAdapter',
    'CsdnAdapter',
    'AliyunAdapter',
    'AliyunDocAdapter',
]

# 便捷映射（推荐使用新版）
ADAPTERS = {
    'github': GitHubAdapter,
    'zhihu': ZhihuAdapter,
    'juejin': JuejinAdapter,
    'csdn': CsdnAdapter,
    'aliyun': AliyunAdapter,
}

CLOUD_DOC_ADAPTERS = {
    'aliyun_doc': AliyunDocAdapter,
}