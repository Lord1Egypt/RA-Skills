#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""图片搜索服务 — 以图搜商品

从 1688-distribution-distribute-offer 复制并适配 procurement 项目的 api_post。
"""

import json
import os
import sys
from typing import List, Optional

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')))
from scripts._sys._http import api_post
from scripts._sys._errors import ServiceError


def image_search_offer(
    image_url: str = None,
    image_base64: str = None,
    page_index: int = 1,
    page_size: int = 20,
    filters: Optional[List[dict]] = None,
    sort_field: str = None,
    sort_desc: bool = False,
    keyword: str = None,
    region: str = None,
) -> dict:
    """
    以图搜商品 — 通过图片搜索相似的分销商品。

    :param image_url: 图片 URL 地址（与 image_base64 二选一）
    :param image_base64: 图片 Base64 编码（与 image_url 二选一）
    :param page_index: 页码，从 1 开始，默认 1
    :param page_size: 每页数量，默认 20，最大 50
    :param filters: 筛选条件列表（IndicatorModel 格式）
    :param sort_field: 排序字段
    :param sort_desc: 是否降序，默认 False
    :param keyword: 辅助关键词（可选，无图片时也可作为纯关键词搜索）
    :param region: 主体圈选区域坐标（可选，如 "100,100,300,400"）
    :return: 包含 data（商品数组）、total（总数）等的 dict
    """
    if not image_url and not image_base64 and not keyword:
        raise ServiceError("图搜需要提供图片链接（image_url）、图片 Base64（image_base64）或关键词（keyword），至少传一个")

    image_param = {}
    if image_url:
        image_param["imageAddress"] = image_url
    if image_base64:
        image_param["imageBase64"] = image_base64
    if region:
        image_param["region"] = region

    params = {
        "searchMode": "IMAGE_SEARCH" if (image_url or image_base64) else "KEYWORD_SEARCH",
        "sceneCode": "fxyx",
        "pageIndex": page_index,
        "pageSize": page_size,
        "filter": filters or [],
        "terminal": "PC",
    }

    if image_param:
        params["imageParam"] = image_param
    if keyword:
        params["keyword"] = keyword
    if sort_field:
        params["sortModel"] = {"field": sort_field, "desc": sort_desc}

    result = api_post(
        tool_name="same_img_offer_search",
        body={"sceneSearchParamStr": json.dumps(params, ensure_ascii=False)},
        timeout=60,
    )

    return _parse_image_search_result(result)


def _parse_image_search_result(result: dict) -> dict:
    """
    解析图搜返回结果。

    procurement 项目的 api_post 已解包网关层，result 直接为业务数据。
    """
    if not isinstance(result, dict):
        raise ServiceError("图搜返回格式异常：期望 dict 类型")

    items = result.get("data", []) or []
    return {
        "data": items,
        "total": result.get("total", len(items)),
        "pageNum": result.get("pageNum", 1),
        "totalPage": result.get("totalPage", 1),
        "extendInfo": result.get("extendInfo", {}),
    }
