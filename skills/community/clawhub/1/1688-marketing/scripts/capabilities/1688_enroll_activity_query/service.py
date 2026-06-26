#!/usr/bin/env python3
"""1688招商活动查询服务"""

from _http import api_post
from _errors import ServiceError


def query_enroll_activities(page_no: int = 1, page_size: int = 10, keyword: str = "") -> dict:
    """
    查询1688招商活动列表

    Args:
        page_no: 当前分页，默认1
        page_size: 分页大小，默认10
        keyword: 活动Id或名称，可选

    Returns:
        包含 total, pageNo, pageSize, data 的字典
    """
    body = {
        "pageNo": page_no,
        "pageSize": page_size,
    }
    if keyword:
        body["keyword"] = keyword

    result = api_post("/api/1688_enroll_activity_query/1.0.0", body)

    if not isinstance(result, dict):
        raise ServiceError("格式异常，请稍后重试")
    return result
