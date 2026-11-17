#!/usr/bin/env python3
"""客户列表查询服务"""

from typing import List

from _http import api_post


def customer_list(
    filters: List[dict] = None,
    sorts: List[dict] = None,
    page_num: int = 1,
    page_size: int = 20,
) -> dict:
    """分页查询客户列表（支持多条件筛选 + 排序）"""
    body = {"pageSize": page_size, "pageNum": page_num}
    if filters:
        body["filters"] = filters
    if sorts:
        body["sorts"] = sorts

    return api_post("/api/alibaba.1688.customer.list/1.0.0", body)
