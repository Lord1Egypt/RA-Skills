#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""铺货执行服务 — 内置铺货接口调用"""

import json
import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')))
from scripts._sys._http import api_post


def _call_single(app_key: str, out_shop_list: list, offer_id: str) -> dict:
    """对单个商品调用铺货接口，返回解析后的 dict。"""
    inner = api_post(
        tool_name="distribute_offer",
        body={
            "appKey": app_key,
            "outShopListStr": json.dumps(out_shop_list, ensure_ascii=False),
            "offerIdList": offer_id,
        },
    )
    data_wrapper = inner.get("data", {})
    if isinstance(data_wrapper, dict):
        data_str = data_wrapper.get("data", "")
        error_code = data_wrapper.get("errorCode", "")
    else:
        data_str = data_wrapper if isinstance(data_wrapper, str) else ""
        error_code = inner.get("errorCode", "")

    try:
        data = json.loads(data_str) if data_str else {}
    except Exception:
        data = {}
    data["errorCode"] = error_code
    return data


def distribute_offer(
    app_key: str,
    out_shop_list: list,
    offer_id_list: str,
) -> dict:
    """
    执行铺货操作（内置铺货接口）。
    因 API 单次仅处理 1 个商品，多商品时逐个调用并汇总结果。

    :param app_key: 三方服务商唯一标识
    :param out_shop_list: 目标店铺列表，每项为 {"code": "店铺编码", "channel": "渠道"}
    :param offer_id_list: 商品 ID 字符串，多个用英文逗号分隔
    :return: 包含 errorCode、failCount、successCount、allCount、successOfferIds、failOfferIds 的 dict
    """
    ids = [x.strip() for x in offer_id_list.split(",") if x.strip()]

    # 单个商品直接调用
    if len(ids) <= 1:
        return _call_single(app_key, out_shop_list, ids[0] if ids else offer_id_list)

    # 多个商品逐个调用并汇总
    success_ids = []
    fail_ids = []
    brand_invalid_ids = []
    last_error_code = "0"
    last_app_key = app_key

    for oid in ids:
        try:
            r = _call_single(app_key, out_shop_list, oid)
            ec = str(r.get("errorCode", ""))
            sc = r.get("successCount", 0)
            if ec in ("200", "0") and sc > 0:
                success_ids.append(oid)
            else:
                fail_ids.append(oid)
                last_error_code = ec if ec not in ("200", "0") else last_error_code
            brand_invalid_ids.extend([str(x) for x in r.get("brandInvalidOfferIds", [])])
            last_app_key = r.get("appKey", app_key)
        except Exception:
            fail_ids.append(oid)

    all_count = len(ids)
    has_fail = len(fail_ids) > 0
    final_error_code = last_error_code if has_fail and last_error_code not in ("200", "0") else ("210" if has_fail else "0")

    return {
        "allCount": all_count,
        "successCount": len(success_ids),
        "failCount": len(fail_ids),
        "successOfferIds": success_ids,
        "failOfferIds": fail_ids,
        "brandInvalidOfferIds": brand_invalid_ids,
        "appKey": last_app_key,
        "errorCode": final_error_code,
    }
