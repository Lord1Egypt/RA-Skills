#!/usr/bin/env python3
"""客户筛选配置查询服务"""

from _http import api_post
from _errors import ServiceError


def customer_field_config() -> dict:
    """获取当前商家可用的筛选维度（自定义属性 + 标签）"""
    return api_post("/api/alibaba.1688.customer.attr.field.config/1.0.0", {})
