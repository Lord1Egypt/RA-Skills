#!/usr/bin/env python3
"""
AiriLab 核心模块初始化

导出所有核心组件：
- AiriLabConfig: 配置管理
- AiriLabAuth: 鉴权管理
- AiriLabProject: 项目管理
- AiriLabUpload: 图片上传
- AiriLabAPI: API 调用
"""

from .config import AiriLabConfig
from .auth import AiriLabAuth
from .project import AiriLabProject
from .upload import AiriLabUpload
from .api import AiriLabAPI

__all__ = [
    'AiriLabConfig',
    'AiriLabAuth',
    'AiriLabProject',
    'AiriLabUpload',
    'AiriLabAPI',
]
