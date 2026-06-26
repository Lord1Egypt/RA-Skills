#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""关联货源助手命令"""

import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')))
from scripts._sys._output import print_output, print_error
from scripts.biz.link_supply_helper.service import link_supply as _link_supply


def link_supply(
    downstream_item_id: str = "",
    downstream_sku_id: str = "",
    offer_id: str = "",
    sku_id: str = "",
    isv_app_key: str = "",
    platform: str = "",
):
    """关联货源 - 将下游商品与1688商品建立关联

    用法：
        python3 scripts/cli.py link_supply_helper link_supply --downstream_item_id=xxx --offer_id=xxx
        python3 scripts/cli.py link_supply_helper link_supply --downstream_item_id=xxx --downstream_sku_id=xxx --offer_id=xxx --sku_id=xxx
        python3 scripts/cli.py link_supply_helper link_supply --downstream_item_id=xxx --offer_id=xxx --isv_app_key=9018264 --platform=douyin
    """
    try:
        if not downstream_item_id:
            print_output(False, "❌ 缺少必填参数 downstream_item_id", {})
            return

        result = _link_supply(
            downstream_item_id=downstream_item_id,
            downstream_sku_id=downstream_sku_id if downstream_sku_id else None,
            offer_id=offer_id if offer_id else None,
            sku_id=sku_id if sku_id else None,
            isv_app_key=isv_app_key if isv_app_key else None,
            platform=platform if platform else None,
        )

        print_output(True, "## 关联货源成功", result)
    except Exception as e:
        print_error(e)
