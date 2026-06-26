#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
业务模块模板 - 请根据实际需求修改

功能：
1. 功能点 1
2. 功能点 2
"""

import os
import sys
from typing import Dict, Optional

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')))
from scripts._sys._http import api_post


def your_function(param1: str, param2: Optional[str] = None) -> Dict:
    """
    你的业务函数 - 请根据实际需求修改

    参数：
    - param1: 必填参数说明
    - param2: 选填参数说明

    返回：
        api_post 解包后的业务数据（dict）
    异常：
        AuthError / ParamError / ServiceError 等（由 _http.py 统一抛出）
    """
    body = {}
    if param1:
        body["param1"] = param1
    if param2:
        body["param2"] = param2

    # 调用 1688 API
    # tool_name 为源舟平台注册的工具 code
    # 注册地址：https://pre-1688bot.alibaba-inc.com/#/tool/list
    return api_post(tool_name="your_api_name", body=body)
