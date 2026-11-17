#!/usr/bin/env python3
"""图片制作高级版权限校验服务"""

import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _http import api_post
from _errors import ServiceError


def verify_permission():
    """
    校验当前商家的图片制作高级版权限。
    商家身份由 AK 网关签名自动识别，无需传 userId。

    Returns:
        dict: {isAi, digitalModel, faceFix}
            isAi          - 是否高级版
            digitalModel  - 是否有数字模特权限
            faceFix       - 是否有脸部修复权限（暂未使用）
    """
    data = api_post("/api/alibaba.1688.image.generate.vertify.permission/1.0.0", {})
    if not isinstance(data, dict):
        raise ServiceError("权限校验返回格式异常，请稍后重试")
    return data
