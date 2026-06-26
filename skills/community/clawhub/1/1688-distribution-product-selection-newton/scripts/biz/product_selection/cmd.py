#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
选品命令层 - 关键词选品 + 图搜选品
"""

import json
import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')))
from scripts._sys._output import print_output, print_error
from scripts.biz.product_selection.service import (
    fx_keyword_search_selection as _fx_keyword_search_selection,
    image_search_offer as _image_search_offer,
)

def fx_keyword_search_selection(retrieve_filters: str = "", page_no: str = "1", page_size: str = "20", rank_type: str = "", rank_field: str = ""):
    """关键词选品 - 根据筛选条件检索适合铺货的商品"""
    try:
        if not retrieve_filters:
            print_output(False, "❌ 缺少必填参数 retrieve_filters，格式：JSON 数组字符串", {})
            return
        
        # 解析 JSON 格式的筛选条件
        try:
            filters = json.loads(retrieve_filters)
            if not isinstance(filters, list):
                raise ValueError("retrieve_filters 必须是 JSON 数组")
        except json.JSONDecodeError as e:
            print_output(False, f"❌ retrieve_filters 格式错误：{e}", {})
            return
        
        page_no_int = int(page_no) if page_no else 1
        page_size_int = int(page_size) if page_size else 20
        
        result = _fx_keyword_search_selection(
            retrieve_filters=filters,
            page_no=page_no_int,
            page_size=page_size_int,
            rank_type=rank_type or None,
            rank_field=rank_field or None,
        )
        print_output(True, "✅ 关键词选品完成", result)
    except Exception as e:
        print_error(e)

def image_search_offer(image_url: str = "", image_base64: str = "", page_index: str = "1", page_size: str = "20", filters: str = "", sort_field: str = "", sort_desc: str = "false", keyword: str = "", region: str = ""):
    """图搜选品 - 通过图片搜索相似的分销商品"""
    try:
        if not image_url and not image_base64:
            print_output(False, "❌ 缺少必填参数：需要提供 image_url 或 image_base64 至少一个", {})
            return
        
        page_index_int = int(page_index) if page_index else 1
        page_size_int = int(page_size) if page_size else 20
        sort_desc_bool = sort_desc.lower() == "true" if sort_desc else False
        
        # 解析可选的 filters 参数
        filters_list = None
        if filters:
            try:
                filters_list = json.loads(filters)
                if not isinstance(filters_list, list):
                    raise ValueError("filters 必须是 JSON 数组")
            except json.JSONDecodeError as e:
                print_output(False, f"❌ filters 格式错误：{e}", {})
                return
        
        result = _image_search_offer(
            image_url=image_url or None,
            image_base64=image_base64 or None,
            page_index=page_index_int,
            page_size=page_size_int,
            filters=filters_list,
            sort_field=sort_field or None,
            sort_desc=sort_desc_bool,
            keyword=keyword or None,
            region=region or None,
        )
        print_output(True, "✅ 图搜选品完成", result)
    except Exception as e:
        print_error(e)