#!/usr/bin/env python3
"""88查招投标搜索服务"""

from _http import api_post
from _errors import ServiceError


def bid_search(keyword: str, pageNo: int, pageSize: int,
               provinces: list = None, cities: list = None,
               regions: list = None,
               startTime: int = None, endTime: int = None) -> dict:
    """根据关键词搜索招投标公告信息

    Args:
        startTime: 起始时间戳（毫秒），筛选发布日期 >= startTime 的记录
        endTime: 截止时间戳（毫秒），筛选发布日期 <= endTime 的记录
    """
    params = {"keyword": keyword, "pageNo": pageNo, "pageSize": pageSize}
    if provinces:
        params["provinces"] = provinces
    if cities:
        params["cities"] = cities
    if regions:
        params["regions"] = regions
    if startTime is not None:
        params["startTime"] = startTime
    if endTime is not None:
        params["endTime"] = endTime
    data = api_post("/api/bidSearch/1.0.0", params)

    if not isinstance(data, dict):
        raise ServiceError("格式异常，请稍后重试")
    return data
