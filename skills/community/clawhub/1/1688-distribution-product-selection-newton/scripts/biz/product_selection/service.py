#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
选品搜索服务 — 关键词选品 + 图搜选品
"""

import json
import os
import sys
from typing import Dict, List, Optional

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')))
from scripts._sys._http import api_post
from scripts._sys._errors import ServiceError

# ══════════════════════════════════════════════════════════════════════════════
# 核心选品搜索功能
# ══════════════════════════════════════════════════════════════════════════════

def fx_keyword_search_selection(
    retrieve_filters: list,
    page_no: int = 1,
    page_size: int = 20,
    rank_type: str = None,
    rank_field: str = None,
) -> Dict:
    """
    关键词选品 - 根据筛选条件检索适合铺货的商品
    
    参数：
        retrieve_filters: 筛选条件列表，每项格式为
            {"code": "字段key", "value": [...], "queryType": "操作符"}
        page_no: 页码，从 1 开始，默认 1
        page_size: 每页数量，默认 20，最大 50
        rank_type: 排序方向，"ASC" 升序 / "DESC" 降序
        rank_field: 排序字段，如 "df_price"、"fx_ord_cnt_30d" 等
    
    返回：
        包含 data（商品数组）和 total（总数）的 dict
    """
    params = {
        "retrieveFilters": retrieve_filters,
        "pageNo": page_no,
        "pageSize": page_size,
    }
    if rank_type:
        params["rankType"] = rank_type
    if rank_field:
        params["rankField"] = rank_field

    inner = api_post(
        tool_name="fx_keyword_search_selection",
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
) -> Dict:
    """
    图搜选品 - 通过图片搜索相似的分销商品
    
    参数：
        image_url: 图片 URL 地址（与 image_base64 二选一）
        image_base64: 图片 Base64 编码（与 image_url 二选一）
        page_index: 页码，从 1 开始，默认 1
        page_size: 每页数量，默认 20，最大 50
        filters: 筛选条件列表（IndicatorModel 格式）
        sort_field: 排序字段
        sort_desc: 是否降序，默认 False
        keyword: 辅助关键词（可选）
        region: 主体圈选区域坐标（可选，如 "100,100,300,400"）
    
    返回：
        包含 data（商品数组）、total（总数）等的 dict
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

    # 图搜接口的参数名是 sceneSearchParamStr
    inner = api_post(
        tool_name="same_img_offer_search",
        body={"sceneSearchParamStr": json.dumps(params, ensure_ascii=False)},
    )

    return _parse_image_search_result(inner)


def _parse_image_search_result(inner: Dict) -> Dict:
    """
    解析图搜返回结果
    
    图搜接口返回 MtopPageResult 格式（bizSuccess/bizMsg），
    与关键词选品的返回格式不同，需要单独适配
    """
    # 外层网关可能包装了一层 data
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