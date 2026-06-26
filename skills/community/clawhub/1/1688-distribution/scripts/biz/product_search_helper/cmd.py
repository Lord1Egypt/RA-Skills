#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""选品搜索命令 — CLI 入口（关键词选品 + 图搜选品）"""

import json
import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')))
from scripts._sys._output import print_output, print_error
from scripts.biz.product_search_helper.service import select_offer, image_search_offer


def search(filters: str = "", page_no: str = "1", page_size: str = "20",
           rank_type: str = "", rank_field: str = "",
           image_url: str = "", image_base64: str = "",
           region: str = "", keyword: str = ""):
    """选品搜索（支持关键词和图搜两种模式）"""
    try:
        if image_url or image_base64:
            result = image_search_offer(
                image_url=image_url or None,
                image_base64=image_base64 or None,
                page_index=int(page_no),
                page_size=int(page_size),
                sort_field=rank_field or None,
                sort_desc=(rank_type == "DESC") if rank_type else False,
                keyword=keyword or None,
                region=region or None,
            )
        elif filters:
            filters_list = json.loads(filters)
            result = select_offer(
                retrieve_filters=filters_list,
                page_no=int(page_no),
                page_size=int(page_size),
                rank_type=rank_type or None,
                rank_field=rank_field or None,
            )
        else:
            print_output(False, "❌ 缺少必需的选品参数，请指定 --filters 或 --image_url", {})
            return

        total = result.get("total", 0)
        items = result.get("data", [])
        summary = f"找到 {total} 个商品，当前展示 {len(items)} 个"
        print_output(True, summary, result)
    except json.JSONDecodeError as e:
        print_output(False, f"❌ 筛选条件 JSON 格式错误：{e}", {})
    except Exception as e:
        print_error(e)
