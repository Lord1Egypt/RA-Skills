#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""选品搜索服务 — 关键词选品 + 图搜选品"""

import json
import os
import sys
from typing import List, Optional

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')))
from scripts._sys._http import api_post
from scripts._sys._errors import ServiceError


# ── 关键词选品 ────────────────────────────────────────────────────────────────

def select_offer(
    retrieve_filters: list,
    page_no: int = 1,
    page_size: int = 20,
    rank_type: str = None,
    rank_field: str = None,
) -> dict:
    """
    调用选品工具，根据筛选条件检索适合铺货的商品。
    当单页返回不足 page_size 且 total 表明还有更多商品时，自动请求后续页补齐。

    :param retrieve_filters: 筛选条件列表，每项格式为
        {"code": "字段key", "value": [...], "queryType": "操作符"}
    :param page_no: 页码，从 1 开始，默认 1
    :param page_size: 每页数量，默认 20，最大 50
    :param rank_type: 排序方向，"ASC" 升序 / "DESC" 降序
    :param rank_field: 排序字段，如 "df_price"、"fx_ord_cnt_30d" 等
    :return: 包含 data（商品数组）和 total（总数）的 dict
    """
    result = _fetch_one_page(retrieve_filters, page_no, page_size, rank_type, rank_field)
    items = result["data"]
    total = result["total"]

    # 自动补页：当返回不足且后端还有更多数据时，继续请求下一页补齐
    max_extra_pages = 3  # 最多额外请求 3 页，防止无限循环
    current_page = page_no
    while len(items) < page_size and len(items) < total and max_extra_pages > 0:
        current_page += 1
        max_extra_pages -= 1
        extra = _fetch_one_page(retrieve_filters, current_page, page_size, rank_type, rank_field)
        extra_items = extra["data"]
        if not extra_items:
            break  # 后端无更多数据
        items.extend(extra_items)

    # 截断到用户请求的数量
    if len(items) > page_size:
        items = items[:page_size]

    return {"data": items, "total": total}


def _fetch_one_page(
    retrieve_filters: list,
    page_no: int,
    page_size: int,
    rank_type: str = None,
    rank_field: str = None,
) -> dict:
    """请求单页选品数据。"""
    params = {
        "sceneType": "agenticSelection",
        "retrieveFilters": retrieve_filters,
        "pageNo": page_no,
        "pageSize": page_size,
    }
    if rank_type:
        params["rankType"] = rank_type
    if rank_field:
        params["rankField"] = rank_field

    inner = api_post(
        tool_name="distribution_select_offer",
        body={"params": json.dumps(params, ensure_ascii=False)},
    )
    data_field = inner.get("data", {})
    if isinstance(data_field, dict):
        return {
            "data": data_field.get("data", []),
            "total": data_field.get("total", 0),
        }
    return {
        "data": data_field if isinstance(data_field, list) else [],
        "total": inner.get("total", 0),
    }


# ── 图搜选品 ─────────────────────────────────────────────────────────────────

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
    :param keyword: 辅助关键词（可选）
    :param region: 主体圈选区域坐标（可选，如 "100,100,300,400"）
    :return: 包含 data（商品数组）、total（总数）等的 dict
    """
    if not image_url and not image_base64:
        raise ServiceError("图搜需要提供图片链接（image_url）或图片 Base64 编码（image_base64），至少传一个")

    image_param = {}
    if image_url:
        image_param["imageAddress"] = image_url
    if image_base64:
        image_param["imageBase64"] = image_base64
    if region:
        image_param["region"] = region

    params = {
        "searchMode": "IMAGE_SEARCH",
        "sceneCode": "fxyx",
        "imageParam": image_param,
        "pageIndex": page_index,
        "pageSize": page_size,
        "filter": filters or [],
        "terminal": "PC",
    }
    if keyword:
        params["keyword"] = keyword
    if sort_field:
        params["sortModel"] = {"field": sort_field, "desc": sort_desc}

    inner = api_post(
        tool_name="same_img_offer_search",
        body={"sceneSearchParamStr": json.dumps(params, ensure_ascii=False)},
        timeout=60,
    )

    return _parse_image_search_result(inner)


def _parse_image_search_result(inner: dict) -> dict:
    """解析图搜返回结果。"""
    data_wrapper = inner.get("data", inner)
    if isinstance(data_wrapper, dict) and "bizSuccess" in data_wrapper:
        payload = data_wrapper
    else:
        payload = inner

    biz_success = payload.get("bizSuccess", True)
    if biz_success is False:
        biz_msg = payload.get("bizMsg", "图搜失败")
        raise ServiceError(f"图搜失败：{biz_msg}")

    items = payload.get("data", []) or []
    return {
        "data": items,
        "total": payload.get("total", len(items)),
        "pageNum": payload.get("pageNum", 1),
        "totalPage": payload.get("totalPage", 1),
        "extendInfo": payload.get("extendInfo", {}),
    }
