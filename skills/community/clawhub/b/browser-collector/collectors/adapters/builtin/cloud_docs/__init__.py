#!/usr/bin/env python3
"""
collectors/adapters/builtin/cloud_docs - 云厂商文档适配器

支持:
- AliyunDocAdapter: 阿里云文档 (help.aliyun.com)
- TencentDocAdapter: 腾讯云文档 (cloud.tencent.com)
- VolcengineDocAdapter: 火山引擎文档 (volcengine.com)
- CozeDocAdapter: Coze扣子文档 (coze.com, coze.cn)
"""

from .aliyun import AliyunDocAdapter
from .tencent import TencentDocAdapter
from .volcengine import VolcengineDocAdapter
from .coze import CozeDocAdapter

__all__ = ['AliyunDocAdapter', 'TencentDocAdapter', 'VolcengineDocAdapter', 'CozeDocAdapter']