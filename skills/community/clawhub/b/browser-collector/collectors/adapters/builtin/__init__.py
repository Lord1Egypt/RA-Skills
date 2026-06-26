#!/usr/bin/env python3
"""
collectors/adapters/builtin - 内置适配器

提供各类网站/平台的专用适配器。

支持的适配器:
    云厂商文档:
    - AliyunDocAdapter: 阿里云文档 (help.aliyun.com)
    - TencentDocAdapter: 腾讯云文档 (cloud.tencent.com)
    - VolcengineDocAdapter: 火山引擎文档 (volcengine.com)
    - CozeDocAdapter: Coze扣子文档 (coze.com, coze.cn)

    API文档:
    - KimiApiAdapter: Kimi API文档 (platform.kimi.com)
    - MiniMaxApiAdapter: MiniMax API文档 (platform.minimaxi.com)

    社交媒体:
    - GitHubAdapter: GitHub (github.com)
    - ZhihuAdapter: 知乎 (zhihu.com)
    - JuejinAdapter: 掘金 (juejin.cn)
    - CsdnAdapter: CSDN (csdn.net)

Usage:
    # 推荐方式
    from collectors.adapters.builtin.cloud_docs import AliyunDocAdapter
    from collectors.adapters.builtin.api_docs import KimiApiAdapter
    from collectors.adapters.builtin.social import GitHubAdapter

    # 或者从 builtin 包导入
    from collectors.adapters.builtin import AliyunDocAdapter, KimiApiAdapter
"""

from .cloud_docs import AliyunDocAdapter, TencentDocAdapter, VolcengineDocAdapter, CozeDocAdapter
from .api_docs import KimiApiAdapter, MiniMaxApiAdapter
from .social import GitHubAdapter, ZhihuAdapter, JuejinAdapter, CsdnAdapter

__all__ = [
    # 云厂商文档
    'AliyunDocAdapter',
    'TencentDocAdapter',
    'VolcengineDocAdapter',
    'CozeDocAdapter',
    # API文档
    'KimiApiAdapter',
    'MiniMaxApiAdapter',
    # 社交媒体
    'GitHubAdapter',
    'ZhihuAdapter',
    'JuejinAdapter',
    'CsdnAdapter',
]