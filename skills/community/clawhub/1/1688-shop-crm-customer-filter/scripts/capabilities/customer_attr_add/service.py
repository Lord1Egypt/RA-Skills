#!/usr/bin/env python3
"""自定义属性新增服务"""

from _http import api_post


def customer_attr_add(attr_key: str, attr_label: str, attr_type: str = "string", value: str = None) -> dict:
    """新增一列自定义属性"""
    body = {"attrKey": attr_key, "attrLabel": attr_label, "attrType": attr_type}
    if value is not None:
        body["value"] = value
    return api_post("/api/alibaba.1688.customer.attr.add.column/1.0.0", body)
