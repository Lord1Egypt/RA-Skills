"""
collectors/adapters/builtin/social/ - 社交媒体适配器

提供社交媒体平台的结构化数据提取适配器。

支持的适配器:
- GitHubAdapter: GitHub仓库、Issue、用户页
- ZhihuAdapter: 知乎问题、文章、用户页
- JuejinAdapter: 掘金文章
- CsdnAdapter: CSDN博客文章

所有适配器继承自 DocAdapter，返回 DocumentItem（完整结构化数据）。

Usage:
    from collectors.adapters.builtin.social import (
        GitHubAdapter, ZhihuAdapter, JuejinAdapter, CsdnAdapter
    )
"""

from .github import GitHubAdapter
from .zhihu import ZhihuAdapter
from .juejin import JuejinAdapter
from .csdn import CsdnAdapter

__all__ = [
    'GitHubAdapter',
    'ZhihuAdapter',
    'JuejinAdapter',
    'CsdnAdapter',
]

# 社交媒体适配器映射
SOCIAL_ADAPTERS = {
    'github': GitHubAdapter,
    'zhihu': ZhihuAdapter,
    'juejin': JuejinAdapter,
    'csdn': CsdnAdapter,
}