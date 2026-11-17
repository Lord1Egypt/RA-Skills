#!/usr/bin/env python3
"""推荐渠道深度下钻服务"""

import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _http import api_post
from _errors import ServiceError


def get_recommend_channel_detail(query_date: str, login_id: str = None) -> dict:
    """推荐渠道深度下钻"""
    payload = {"query_date": query_date}
    if login_id:
        payload["NEWTON_SHOP_LOGIN_ID"] = login_id
    data = api_post("/api/alibaba.1688.get.recommend.channel.detail/1.0.0", payload)
    if not isinstance(data, dict):
        raise ServiceError("格式异常，请稍后重试")
    return data
