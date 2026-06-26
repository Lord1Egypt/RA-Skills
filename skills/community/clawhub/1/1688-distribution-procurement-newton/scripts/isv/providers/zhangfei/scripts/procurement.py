#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""采购 / 铺货：调用中台 yzg Skill，返回 cli 统一 JSON。路由见包内 SKILL.md。"""

from __future__ import annotations

import difflib
import json
import re
from copy import deepcopy
from typing import Any

import requests

from _api import douyin_skill_url, request_json, resolve_jwt_token, yzg_skill_url

# SKILL.md §3.1 对用户锁定句（CLI 收口，禁止向用户暴露 JWT/HTTP 等技术细节）
_MSG_AUTH_FAIL_USER = "需要先登录一下再试。"
_MSG_HTTP_FAIL_USER = "操作未成功，方便的话请稍后再试。"


def _fail_auth(section_heading: str, data: dict[str, Any]) -> dict[str, Any]:
    """鉴权失败：不透传底层异常文案。"""
    return _fail(f"{section_heading}\n\n{_MSG_AUTH_FAIL_USER}", data, "auth_failed")


def _fail_http(section_heading: str, data: dict[str, Any]) -> dict[str, Any]:
    """HTTP 层失败：统一业务失败收口句。"""
    return _fail(f"{section_heading}\n\n{_MSG_HTTP_FAIL_USER}", data, "http_error")


def _after_sale_success_user_msg(ret_data: Any) -> str:
    """售后保存成功展示文案：避免 retData 为 None 时在 markdown 中出现字面 None。"""
    if ret_data is None:
        return "已帮您保存好了。"
    if isinstance(ret_data, str):
        t = ret_data.strip()
        return t if t else "已帮您保存好了。"
    if isinstance(ret_data, dict):
        for key in ("message", "msg", "retMsg", "completionMessage"):
            v = ret_data.get(key)
            if isinstance(v, str) and v.strip():
                return v.strip()
        return "已帮您保存好了。"
    return "已帮您保存好了。"


def _ok(markdown: str, data: dict[str, Any]) -> dict[str, Any]:
    return {"success": True, "markdown": markdown, "data": data}


def _fail(markdown: str, data: dict[str, Any], error: str | None = None) -> dict[str, Any]:
    out: dict[str, Any] = {"success": False, "markdown": markdown, "data": data}
    if error:
        out["error"] = error
    return out


def list_shops(*, token: str | None) -> dict[str, Any]:
    """查询当前 JWT 用户已绑定的分销店铺列表。"""
    try:
        resolve_jwt_token(token=token)
    except ValueError:
        return _fail_auth("## 查询店铺", {"total": 0, "shops": []})

    url = yzg_skill_url("/shops/bindByAliUser")
    try:
        body = request_json("GET", url, token=token)
        if body.get("retCode") == "0000":
            raw_list = body.get("retData") or []
            shops = []
            for item in raw_list:
                if not isinstance(item, dict):
                    continue
                sid = item.get("shopId") or item.get("id")
                name = item.get("shopName") or item.get("name") or sid
                if sid is None:
                    continue
                shops.append({"id": str(sid), "name": str(name)})
            data = {"total": len(shops), "shops": shops}
            md = f"## 查询店铺\n\n共 {len(shops)} 个绑定店铺。"
            return _ok(md, data)
        return _fail(
            f"## 查询店铺\n\n{body.get('retMsg', '查询店铺列表失败')}",
            {"total": 0, "shops": []},
            body.get("retMsg"),
        )
    except ValueError:
        return _fail_auth("## 查询店铺", {"total": 0, "shops": []})
    except requests.exceptions.ConnectionError:
        return _fail("## 查询店铺\n\n无法连接到 API 服务器。", {"total": 0, "shops": []})
    except requests.exceptions.Timeout:
        return _fail("## 查询店铺\n\n请求超时。", {"total": 0, "shops": []})
    except requests.exceptions.HTTPError:
        return _fail_http("## 查询店铺", {"total": 0, "shops": []})
    except (KeyError, TypeError) as exc:
        return _fail(f"## 查询店铺\n\n响应解析失败：{exc}", {"total": 0, "shops": []}, str(exc))


def list_distributors(*, token: str | None, shop_id: str) -> dict[str, Any]:
    """查询店铺绑定的分销账号。"""
    sid = (shop_id or "").strip()
    if not sid:
        return _fail(
            "## 查询分销账号\n\n请提供 shop-id。",
            {"authorized": False, "authUrl": None, "accounts": []},
            "missing_shop_id",
        )

    url = yzg_skill_url("/fxUser/list")
    params = {
        "platform": "yzg",
        "izAliWarehouseOrder": "true",
        "shopId": sid,
    }
    try:
        body = request_json("GET", url, token=token, params=params)
        if body.get("retCode") == "0000":
            raw_list = body.get("retData") or []
            accounts = []
            for item in raw_list:
                if not isinstance(item, dict):
                    continue
                accounts.append(
                    {
                        "id": str(item.get("id")),
                        "name": item.get("purchasingAccount") or "",
                        "defaultPurchase": item.get("defaultPurchase"),
                        "userId": item.get("userId"),
                        "aiWorkbenchAccount": item.get("aiWorkbenchAccount"),
                        "isOpenAliWarehouseService": item.get("isOpenAliWarehouseService"),
                        "expireTime": item.get("expireTime"),
                    }
                )
            data = {
                "authorized": len(accounts) > 0,
                "authUrl": None,
                "accounts": accounts,
            }
            md = f"## 查询分销账号\n\n店铺 `{sid}` 共 {len(accounts)} 个分销账号。"
            return _ok(md, data)
        return _fail(
            f"## 查询分销账号\n\n{body.get('retMsg', '查询分销账号失败')}",
            {"authorized": False, "authUrl": None, "accounts": []},
            body.get("retMsg"),
        )
    except ValueError:
        return _fail_auth("## 查询分销账号", {"authorized": False, "accounts": []})
    except requests.exceptions.ConnectionError:
        return _fail("## 查询分销账号\n\n无法连接到 API 服务器。", {"authorized": False, "accounts": []})
    except requests.exceptions.Timeout:
        return _fail("## 查询分销账号\n\n请求超时。", {"authorized": False, "accounts": []})
    except requests.exceptions.HTTPError:
        return _fail_http("## 查询分销账号", {"authorized": False, "accounts": []})
    except KeyError as exc:
        return _fail(f"## 查询分销账号\n\n响应解析失败：{exc}", {"authorized": False, "accounts": []}, str(exc))


def query_procurement_settings(
    *,
    token: str | None,
    shop_id: str | None,
) -> dict[str, Any]:
    """绑定店铺列表；若传 shop_id 再查分销账号。"""
    r_shops = list_shops(token=token)
    if not r_shops["success"]:
        return r_shops

    shops = r_shops["data"].get("shops", [])
    accounts: list[dict[str, Any]] = []

    if shop_id and shop_id.strip():
        r_dist = list_distributors(token=token, shop_id=shop_id.strip())
        if not r_dist["success"]:
            md = (
                f"## 采购设置\n\n已查询店铺 {len(shops)} 个；查询分销账号失败："
                f"{r_dist.get('error', r_dist['markdown'])}"
            )
            return _fail(
                md,
                {
                    "shops": shops,
                    "accounts": [],
                    "total_shops": len(shops),
                    "shop_id": shop_id.strip(),
                },
                r_dist.get("error"),
            )
        accounts = r_dist["data"].get("accounts", [])

    lines = [f"- 绑定店铺：{len(shops)} 个"]
    for s in shops:
        lines.append(f"  - {s['name']}（shopId={s['id']}）")
    if shop_id and shop_id.strip():
        lines.append(f"- 店铺 `{shop_id.strip()}` 分销账号：{len(accounts)} 个")
        for a in accounts:
            lines.append(f"  - {a.get('name') or a.get('id')}")

    md = "## 采购设置\n\n" + "\n".join(lines)
    return _ok(
        md,
        {
            "shops": shops,
            "accounts": accounts,
            "total_shops": len(shops),
            "shop_id": shop_id.strip() if shop_id else None,
        },
    )


def list_shop_products(
    *,
    token: str | None,
    shop_nick: str,
) -> dict[str, Any]:
    """查询店铺下在售商品列表。"""
    shop_nick = (shop_nick or "").strip()
    if not shop_nick:
        return _fail("## 店铺商品\n\n缺少参数：请提供 --shop-nick。", {"total": 0, "products": []}, "missing_shop_nick")
    first_shop_nick = shop_nick.split(",")[0] if "," in shop_nick else shop_nick

    url = yzg_skill_url("/itemlink/syn")
    params = {
        "shopNick": shop_nick,
        "shopId": first_shop_nick,
        "sellerCid": "",
        "linkStatus": "0",
        "itemId": "",
        "itemIds": "",
        "itemIdList": "",
        "title": "",
        "outId": "",
        "outIdBegin": "",
        "ytOutId": "",
        "pageNum": "1",
        "pageSize": "10",
        "fxAutoSwitch": "",
        "purchaseAccount": "",
        "showRecentPurchaseHistory": "false",
        "showRecentPurchase30History": "false",
        "modifyDesc": "",
        "platForm": "",
        "tradeReq": "",
        "isAutoJump": "",
        "supplierName": "",
        "proxyStatus": "",
        "cIfLink": "",
        "waitOrderSortType": "",
    }

    try:
        body = request_json("GET", url, token=token, params=params)
        if body.get("retCode") == "0000":
            ret_data_str = body.get("retData", "{}")
            ret_data = json.loads(ret_data_str)
            items_response = ret_data.get("items_onsale_get_response", {})
            items_data = items_response.get("items", {})
            raw_items = items_data.get("item", [])
            if isinstance(raw_items, dict):
                raw_items = [raw_items]
            elif raw_items is None:
                raw_items = []
            total = items_response.get("total_results", len(raw_items))

            products = []
            for item in raw_items:
                products.append(
                    {
                        "id": str(item.get("num_iid")),
                        "title": item.get("title"),
                        "price": item.get("price"),
                        "pic_url": item.get("pic_url"),
                        "sold_quantity": item.get("sold_quantity"),
                        "outer_id": item.get("outer_id"),
                    }
                )

            data = {"total": total, "products": products}
            md = f"## 店铺商品\n\n共 {total} 条（本页 {len(products)} 条）。"
            return _ok(md, data)
        return _fail(
            f"## 店铺商品\n\n{body.get('retMsg', '查询商品列表失败')}",
            {"total": 0, "products": []},
            body.get("retMsg"),
        )
    except ValueError:
        return _fail_auth("## 店铺商品", {"total": 0, "products": []})
    except json.JSONDecodeError as exc:
        return _fail(f"## 店铺商品\n\n解析 retData 失败：{exc}", {"total": 0, "products": []}, str(exc))
    except requests.exceptions.ConnectionError:
        return _fail("## 店铺商品\n\n无法连接到 API 服务器。", {"total": 0, "products": []})
    except requests.exceptions.Timeout:
        return _fail("## 店铺商品\n\n请求超时。", {"total": 0, "products": []})
    except requests.exceptions.HTTPError:
        return _fail_http("## 店铺商品", {"total": 0, "products": []})
    except KeyError as exc:
        return _fail(f"## 店铺商品\n\n响应解析失败：{exc}", {"total": 0, "products": []}, str(exc))


def _normalize_after_sale_purchase_accounts(ret_data: Any) -> list[dict[str, Any]]:
    """将下游 afterSale/queryPurchaseAccountList 的 retData 尽量规范为含 id、name 的列表。"""
    if ret_data is None:
        return []
    if isinstance(ret_data, dict):
        merged: list[Any] = []
        for key in ("AUTH", "NO_AUTH"):
            part = ret_data.get(key)
            if isinstance(part, list):
                merged.extend(part)
        return _normalize_after_sale_purchase_accounts(merged)
    if isinstance(ret_data, list):
        out: list[dict[str, Any]] = []
        for item in ret_data:
            if isinstance(item, str):
                s = item.strip()
                if s:
                    out.append({"id": s, "name": s})
            elif isinstance(item, dict):
                name = item.get("purchasingAccount") or item.get("name") or item.get("nick") or ""
                iid = item.get("id")
                if iid is None and name:
                    iid = name
                out.append(
                    {
                        "id": str(iid) if iid is not None else "",
                        "name": str(name) if name else "",
                        "defaultPurchase": item.get("defaultPurchase"),
                        "userId": item.get("userId"),
                    }
                )
        return out
    return []


def list_purchase_accounts_after_sale(*, token: str | None, shop_id: str) -> dict[str, Any]:
    """售后采购账号列表（GET …/afterSale/queryPurchaseAccountList；shopId 仅中台解析 sid）。"""
    sid = (shop_id or "").strip()
    if not sid:
        return _fail(
            "## 查询分销账号（售后）\n\n请提供 shop-id。",
            {"accounts": []},
            "missing_shop_id",
        )
    try:
        resolve_jwt_token(token=token)
    except ValueError:
        return _fail_auth("## 查询分销账号（售后）", {"accounts": []})

    url = yzg_skill_url("/afterSale/queryPurchaseAccountList")
    params = {"platform": "yzg", "shopId": sid}
    try:
        body = request_json("GET", url, token=token, params=params)
        if body.get("retCode") == "0000":
            raw = body.get("retData")
            accounts = _normalize_after_sale_purchase_accounts(raw)
            data = {
                "shop_id": sid,
                "accounts": accounts,
                "total": len(accounts),
                "raw": raw,
            }
            md = f"## 查询分销账号（售后）\n\n店铺 `{sid}` 共 {len(accounts)} 个采购账号（来源 afterSale/queryPurchaseAccountList）。"
            return _ok(md, data)
        return _fail(
            f"## 查询分销账号（售后）\n\n{body.get('retMsg', '查询失败')}",
            {"shop_id": sid, "accounts": [], "response": body},
            body.get("retMsg"),
        )
    except ValueError:
        return _fail_auth("## 查询分销账号（售后）", {"accounts": []})
    except requests.exceptions.ConnectionError:
        return _fail("## 查询分销账号（售后）\n\n无法连接到 API 服务器。", {"accounts": []})
    except requests.exceptions.Timeout:
        return _fail("## 查询分销账号（售后）\n\n请求超时。", {"accounts": []})
    except requests.exceptions.HTTPError:
        return _fail_http("## 查询分销账号（售后）", {"accounts": []})


_AFTER_SALE_SETTING_JSON = '{"freightApply":true,"freightApplyDutiable":true,"deductionAmount":0,"deductionAmountSwitchForAll":false,"deductionAmountSwitchForSpecific":false,"aliNickApplyPostFeeSwitch":false,"cancelFxOrder":true,"cancelReason":"syn","priceHigh":"","priceLower":"","orderFrequency":0,"purchaseAccount":"","shopNames":"","sellerFlag":"all","cancelReasonInfo":"","status":true,"soAfterSalesType":true,"autoRefundSelf":false,"multipleSubOrders":true,"platform":"yzg","poAfterSaleType":"{\\"noShipRefund\\":true,\\"shipRefund\\":true,\\"returnRefund\\":true,\\"quickRefundSuccess\\":true,\\"normalRefundSuccess\\":true}","poFillWaybillCode":false,"izOpenAddressCheck":true,"poNoShipExplain":"不想要了","poPartRefund":true,"poReturnRefund":"不想要了","poShipExplain":"不想要了","soNoHandleReason":"{\\"allCheck\\":false,\\"shamBrand\\":false,\\"invoice\\":false,\\"funcDnt\\":false,\\"flaw\\":false,\\"qualityProblem\\":false,\\"mormalEquipment\\":false,\\"dmfMatters\\":false,\\"productionDataDnt\\":false,\\"sellerErrorPost\\":false,\\"materialDnt\\":false,\\"Variety\\":false,\\"fspReason\\":false,\\"performanceError\\":false,\\"sizeDnt\\":false,\\"allergy\\":false,\\"sdpDnt\\":false,\\"sellerPromise\\":false,\\"sellerService\\":false,\\"TariffIssues\\":false,\\"feDnt\\":false,\\"damagedAccessories\\":false,\\"printingProblems\\":false,\\"improperSize\\":false,\\"pyvDnt\\":false,\\"LossOfFunc\\":false,\\"csmoDnt\\":false,\\"sdsDnt\\":false,\\"fake\\":false,\\"post\\":false,\\"install\\":false,\\"information\\":false,\\"petDeath\\":false,\\"notWant\\":false}","afterSaleRemarks":false,"afterSaleRemarksPosition":"soft","afterSaleAddressRemarks":false,"afterSaleAddressRemarksPosition":"soft","checkIzModifyAutoAfterSale":false,"izFilterKeyWord":false,"afterSaleAddressToBuyerRemarks":false,"keyWord":"","izFilterAliNick":false,"lowestPurchasePrice":"","highestPurchasePrice":"","isDesignatedAfterSaleItem":false,"afterSaleItemNum":"","izFilterKeyWordForFillBack":true,"poPartRefundLowestSwitch":false,"keyWordForFillBack":"","poPartRefundLowest":"","autoRemoveApply":true,"autoModifyApply":true}'
_DEFAULT_AFTER_SALE_SETTING_BODY: dict[str, Any] = json.loads(_AFTER_SALE_SETTING_JSON)


def save_auto_after_sale(
    *,
    token: str | None,
    shop_id: str,
    purchase_account: str,
    shop_names: str,
    body_overrides: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """POST …/afterSale/setting；默认体 `_DEFAULT_AFTER_SALE_SETTING_BODY`，`body_overrides` 可选合并；剔除 loginName。"""
    sid = (shop_id or "").strip()
    if not sid:
        return _fail(
            "## 售后处理\n\n缺少参数：请提供 shop-id。",
            {"saved": False},
            "missing_shop_id",
        )
    try:
        resolve_jwt_token(token=token)
    except ValueError:
        return _fail_auth("## 售后处理", {"saved": False})

    url = yzg_skill_url("/afterSale/setting")
    params = {"shopId": sid}
    payload = deepcopy(_DEFAULT_AFTER_SALE_SETTING_BODY)
    if body_overrides:
        payload.update(body_overrides)
    payload.pop("loginName", None)
    payload["purchaseAccount"] = (purchase_account or "").strip()
    payload["shopNames"] = (shop_names or "").strip()
    try:
        resp_body = request_json("POST", url, token=token, params=params, json_body=payload)
        if resp_body.get("retCode") == "0000":
            msg = _after_sale_success_user_msg(resp_body.get("retData"))
            pa = payload.get("purchaseAccount")
            sn = payload.get("shopNames")
            md = f"## 售后处理\n\n已提交完整售后配置（purchaseAccount=`{pa}`，shopNames=`{sn}`）。\n\n{msg}"
            return _ok(
                md,
                {
                    "saved": True,
                    "shop_id": sid,
                    "purchase_account": pa,
                    "shop_names": sn,
                    "raw": resp_body.get("retData"),
                },
            )
        return _fail(
            f"## 售后处理\n\n保存失败：{resp_body.get('retMsg', '未知错误')}",
            {"saved": False, "response": resp_body},
            resp_body.get("retMsg"),
        )
    except ValueError:
        return _fail_auth("## 售后处理", {"saved": False})
    except requests.exceptions.ConnectionError:
        return _fail("## 售后处理\n\n无法连接中台 API。", {"saved": False})
    except requests.exceptions.HTTPError:
        return _fail_http("## 售后处理", {"saved": False})


def save_automation_order(
    *,
    token: str | None,
    shop_name: str,
    purchase_account: str,
) -> dict[str, Any]:
    shop_name = (shop_name or "").strip()
    purchase_account = (purchase_account or "").strip()
    if not shop_name or not purchase_account:
        return _fail(
            "## 自动下单\n\n缺少参数：请提供 --shop-name 与 --purchase-account。",
            {"saved": False},
            "missing_params",
        )

    try:
        resolve_jwt_token(token=token)
    except ValueError:
        return _fail_auth("## 自动下单", {"saved": False})

    url = yzg_skill_url("/automationOrder")
    body = {
        "freightSetting": 6,
        "freight": True,
        "compositionsFreight": False,
        "compositionsFreightSetting": None,
        "shopName": shop_name,
        "flagColor": "",
        "orderFrequency": 1,
        "orderLimitMoney": 1,
        "orderHighestLimitMoney": None,
        "orderLimitPercentum": 0,
        "orderHighestLimitPercentum": None,
        "profitMarginSwitch": False,
        "profitSwitch": True,
        "orderLimitMoreorders": True,
        "orderLimitLose": True,
        "orderLimitWord": True,
        "orderLimitWordBuyer": True,
        "status": True,
        "purchaseAccount": purchase_account,
        "gift": True,
        "giftIgnoreProfit": None,
        "receiveProvince": False,
        "receiveProvinceSetting": "全部",
        "productNum": False,
        "productNumSetting": 1,
        "sleepPlaceOrder": "",
        "skuMatched": False,
        "skuMatchedDegree": 50,
        "orderPriceChoose": "lowest",
        "isSkipPrint": False,
        "freightButNopProfit": False,
        "lastPurchasePriceSwitch": False,
        "sameAddress": False,
        "autoMerge": False,
        "wordBuyerKeyword": False,
        "wordBuyerKeywordContent": "",
        "wordKeyword": False,
        "addressKeywordsSwitch": False,
        "wordKeywordContent": "",
        "addressKeywords": "",
        "bindSupplierName": False,
        "purchaseFilterSwitch": False,
        "saleFilterSwitch": False,
        "lowerPurchasePrice": 0,
        "highestPurchasePrice": None,
        "lowerSalePrice": 0,
        "highestSalePrice": None,
        "outerIdKeyWordsSwitch": False,
        "ytOuterIdKeyWordsSwitch": False,
        "outerIdKeyWords": "",
        "ytOuterIdKeyWords": "",
        "productNumSettingForMulti": 1,
        "productNumForMulti": False,
        "izJumpFake": True,
        "isJumpSfDelivery": False,
        "repeatPurchase": False,
        "multipleSubSameSupplier": False,
        "multipleSubAllRelated": False,
        "oprater": "",
        "platform": "yzg",
        "itemSkip": False,
        "itemAutomatic": False,
    }

    try:
        resp_body = request_json("POST", url, token=token, json_body=body)
        if resp_body.get("retCode") == "0000":
            msg = resp_body.get("retData", "设置成功")
            md = f"## 自动下单\n\n已为店铺「{shop_name}」保存自动下单配置，采购账号：`{purchase_account}`。\n\n{msg}"
            return _ok(md, {"saved": True, "shop_name": shop_name, "purchase_account": purchase_account})
        return _fail(
            f"## 自动下单\n\n保存失败：{resp_body.get('retMsg', '未知错误')}",
            {"saved": False},
            resp_body.get("retMsg"),
        )
    except ValueError:
        return _fail_auth("## 自动下单", {"saved": False})
    except requests.exceptions.ConnectionError:
        return _fail("## 自动下单\n\n无法连接中台 API。", {"saved": False})
    except requests.exceptions.HTTPError:
        return _fail_http("## 自动下单", {"saved": False})


def enable_link_type(
    *,
    token: str | None,
    item_ids: str,
    shop: str,
    purchasing_accounts: str,
) -> dict[str, Any]:
    """开启分销宝贝开关，多个 itemId 英文逗号分隔，与旧脚本一致。"""
    ids = [x.strip() for x in (item_ids or "").split(",") if x.strip()]
    shop = (shop or "").strip()
    purchasing_accounts = (purchasing_accounts or "").strip()

    if not ids:
        return _fail(
            "## 开启分销宝贝\n\n商品 ID 不能为空。",
            {
                "total": 0,
                "success_count": 0,
                "fail_count": 0,
                "success_items": [],
                "fail_items": [],
            },
            "empty_item_ids",
        )
    if not shop:
        return _fail(
            "## 开启分销宝贝\n\n店铺名称不能为空。",
            {
                "total": len(ids),
                "success_count": 0,
                "fail_count": len(ids),
                "success_items": [],
                "fail_items": [{"item_id": i, "error": "缺少店铺"} for i in ids],
            },
        )
    if not purchasing_accounts:
        return _fail(
            "## 开启分销宝贝\n\n采购账号列表不能为空。",
            {
                "total": len(ids),
                "success_count": 0,
                "fail_count": len(ids),
                "success_items": [],
                "fail_items": [{"item_id": i, "error": "缺少采购账号"} for i in ids],
            },
        )

    try:
        resolve_jwt_token(token=token)
    except ValueError:
        return _fail_auth("## 开启分销宝贝", {"total": len(ids), "success_items": [], "fail_items": []})

    success_list: list[str] = []
    fail_list: list[dict[str, Any]] = []
    url = yzg_skill_url("/daifa/relation")

    for item_id in ids:
        params = {
            "itemId": item_id,
            "shop": shop,
            "linkStatus": "true",
            "purchasingAccounts": purchasing_accounts,
            "shopId": shop,
        }
        try:
            body = request_json("GET", url, token=token, params=params)
            if body.get("retCode") == "0000":
                ret_data = body.get("retData") or {}
                if ret_data.get("isSuccess"):
                    success_list.append(item_id)
                else:
                    fail_list.append({"item_id": item_id, "error": "开启失败"})
            else:
                fail_list.append({"item_id": item_id, "error": body.get("retMsg", "开启失败")})
        except ValueError:
            fail_list.append({"item_id": item_id, "error": _MSG_AUTH_FAIL_USER})
        except requests.exceptions.ConnectionError:
            fail_list.append({"item_id": item_id, "error": "无法连接到 API 服务器"})
        except requests.exceptions.Timeout:
            fail_list.append({"item_id": item_id, "error": "请求超时"})
        except requests.exceptions.HTTPError:
            fail_list.append({"item_id": item_id, "error": _MSG_HTTP_FAIL_USER})
        except Exception as exc:
            fail_list.append({"item_id": item_id, "error": str(exc)})

    data = {
        "total": len(ids),
        "success_count": len(success_list),
        "fail_count": len(fail_list),
        "success_items": success_list,
        "fail_items": fail_list,
        "published_count": len(success_list),
        "failed_items": fail_list,
    }
    md = (
        f"## 开启分销宝贝\n\n成功 {len(success_list)} 个，失败 {len(fail_list)} 个；店铺「{shop}」。"
    )
    if fail_list:
        return _fail(md + "\n\n部分商品开启分销开关失败。", data, "部分商品开启分销开关失败")
    return _ok(md, data)


def link_source(
    *,
    token: str | None,
    downstream_item_id: str,
    source_offer_id: str | None,
    shop: str,
    purchasing_accounts: str,
) -> dict[str, Any]:
    """关联货源：复用 enable_link_type；`source_offer_id` 仅写入返回 data。"""
    raw_ids = (downstream_item_id or "").strip()
    if not raw_ids or not (shop or "").strip() or not (purchasing_accounts or "").strip():
        return _fail(
            "## 关联货源\n\n缺少参数：需要 --downstream-item-id、--shop、--purchasing-accounts（及鉴权 token）。",
            {"published_count": 0, "failed_items": [{"reason": "missing_params"}]},
            "missing_params",
        )

    r = enable_link_type(
        token=token,
        item_ids=raw_ids,
        shop=shop,
        purchasing_accounts=purchasing_accounts,
    )
    out = dict(r)
    out["markdown"] = out["markdown"].replace("## 开启分销宝贝", "## 关联货源", 1)
    d = dict(out.get("data") or {})
    d["source_offer_id"] = (source_offer_id or "").strip() or None
    if "," not in raw_ids:
        d["item_id"] = raw_ids
        d["shop"] = (shop or "").strip()
    out["data"] = d
    return out


def _itemlink_call_new_get_link_message(
    *,
    token: str,
    shop_id: str,
    item_id: str,
    shop_nick: str,
    purchase_account: str,
) -> dict[str, Any]:
    url = yzg_skill_url("/itemlink/newGetLinkMessage")
    params: dict[str, str] = {
        "itemId": item_id.strip(),
        "shopNick": shop_nick.strip(),
        "purchaseAccount": (purchase_account or "").strip(),
        "shopId": shop_id.strip(),
    }
    try:
        return request_json("GET", url, token=token, params=params, timeout=60)
    except requests.exceptions.HTTPError as exc:
        return {"_http_error": True, "status": exc.response.status_code if exc.response else None, "text": exc.response.text if exc.response else str(exc)}
    except requests.exceptions.RequestException as exc:
        return {"_request_error": True, "message": str(exc)}


def _itemlink_call_verify_and_return(
    *,
    token: str,
    shop_id: str,
    ali_url: str,
    offer_id: str,
    shop_nick: str,
    purchase_account: str,
) -> dict[str, Any]:
    url = yzg_skill_url("/itemlink/verifyAndReturn")
    params = {"shopId": shop_id.strip()}
    body = {
        "aliAccessToken": "",
        "dataBean": {
            "aliUrl": ali_url.strip(),
            "offerId": offer_id.strip(),
            "orderSource": "",
            "platform": "yzg",
            "loginName": "",
            "purchasingAccount": (purchase_account or "").strip(),
            "urlNumber": 0,
            "shopNick": shop_nick.strip(),
        },
    }
    try:
        return request_json("POST", url, token=token, params=params, json_body=body, timeout=60)
    except requests.exceptions.HTTPError as exc:
        return {"_http_error": True, "status": exc.response.status_code if exc.response else None, "text": exc.response.text if exc.response else str(exc)}
    except requests.exceptions.RequestException as exc:
        return {"_request_error": True, "message": str(exc)}


def _itemlink_call_new_import_item_link_by_url(
    *,
    token: str,
    shop_id: str,
    rows: list[dict[str, Any]],
    only_ali_url: str = "true",
) -> dict[str, Any]:
    url = yzg_skill_url("/itemlink/newImportItemLinkByUrl")
    params = {"shopId": shop_id.strip(), "onlyAliUrl": only_ali_url}
    try:
        return request_json("POST", url, token=token, params=params, json_body=rows, timeout=120)
    except requests.exceptions.HTTPError as exc:
        return {"_http_error": True, "status": exc.response.status_code if exc.response else None, "text": exc.response.text if exc.response else str(exc)}
    except requests.exceptions.RequestException as exc:
        return {"_request_error": True, "message": str(exc)}


def _itemlink_offer_id_from_url(url: str) -> str:
    m = re.search(r"/offer/(\d+)\.html", url)
    return m.group(1) if m else ""


def _itemlink_build_upstream_skus(ret_data: dict[str, Any]) -> list[str]:
    leading_prop = ""
    sku_prop = ""
    if isinstance(ret_data.get("objLeadingProp"), list) and ret_data.get("objLeadingProp"):
        leading_prop = str(ret_data["objLeadingProp"][0])
    if isinstance(ret_data.get("objSkuProp"), list) and ret_data.get("objSkuProp"):
        sku_prop = str(ret_data["objSkuProp"][0])

    leading_values = [str(x) for x in ret_data.get("objLeadingValue", []) if str(x).strip()]
    sku_values = [str(x) for x in ret_data.get("objSkuValue", []) if str(x).strip()]

    out: list[str] = []
    if leading_values and sku_values:
        for lv in leading_values:
            for sv in sku_values:
                out.append(f"{leading_prop}:{lv};{sku_prop}:{sv}")
        return out
    if leading_values:
        for lv in leading_values:
            out.append(f"{leading_prop}:{lv}")
        return out
    if sku_values:
        for sv in sku_values:
            out.append(f"{sku_prop}:{sv}")
        return out
    return []


def _itemlink_best_unique_matches(local_skus: list[str], upstream_skus: list[str]) -> list[dict[str, Any]]:
    if not local_skus or not upstream_skus:
        return []
    pairs: list[tuple[float, int, int]] = []
    for li, local in enumerate(local_skus):
        for ui, upstream in enumerate(upstream_skus):
            score = difflib.SequenceMatcher(None, local, upstream).ratio()
            pairs.append((score, li, ui))
    pairs.sort(key=lambda x: (-x[0], x[1], x[2]))
    used_local: set[int] = set()
    used_upstream: set[int] = set()
    matches: list[dict[str, Any]] = []
    for score, li, ui in pairs:
        if li in used_local or ui in used_upstream:
            continue
        used_local.add(li)
        used_upstream.add(ui)
        matches.append(
            {
                "local_sku": local_skus[li],
                "upstream_sku": upstream_skus[ui],
                "score_percent": int(round(score * 100)),
            }
        )
        if len(used_local) == len(local_skus) or len(used_upstream) == len(upstream_skus):
            break
    matches.sort(key=lambda x: local_skus.index(x["local_sku"]))
    return matches


def _itemlink_query_skus(
    token: str,
    shop_id: str,
    shop_nick: str,
    local_item_id: str,
    source_offer_url: str,
    purchase_account: str,
) -> dict[str, Any]:
    local_raw = _itemlink_call_new_get_link_message(
        token=token,
        shop_id=shop_id,
        item_id=local_item_id,
        shop_nick=shop_nick,
        purchase_account=purchase_account,
    )
    if local_raw.get("_http_error") or local_raw.get("_request_error"):
        return {
            "success": False,
            "markdown": f"## 本店 SKU 查询失败\n\n{local_raw}",
            "data": {"upstream": local_raw},
        }
    if str(local_raw.get("retCode") or "") != "0000":
        return {
            "success": False,
            "markdown": f"## 本店 SKU 查询失败\n\n{local_raw.get('retMsg', '')}",
            "data": {"upstream": local_raw},
        }

    offer_id = _itemlink_offer_id_from_url(source_offer_url)
    if not offer_id:
        return {
            "success": False,
            "markdown": "## 上家 SKU 查询失败\n\n1688 链接未解析到 offerId。",
            "data": {"source_offer_url": source_offer_url},
        }

    ali_raw = _itemlink_call_verify_and_return(
        token=token,
        shop_id=shop_id,
        ali_url=source_offer_url,
        offer_id=offer_id,
        shop_nick=shop_nick,
        purchase_account=purchase_account,
    )
    if ali_raw.get("_http_error") or ali_raw.get("_request_error"):
        return {
            "success": False,
            "markdown": f"## 上家 SKU 查询失败\n\n{ali_raw}",
            "data": {"upstream": ali_raw},
        }
    if str(ali_raw.get("retCode") or "") != "0000":
        return {
            "success": False,
            "markdown": f"## 上家 SKU 查询失败\n\n{ali_raw.get('retMsg', '')}",
            "data": {"upstream": ali_raw},
        }

    local_ret_data = local_raw.get("retData") if isinstance(local_raw.get("retData"), dict) else {}
    sku_link = local_ret_data.get("SkuLink") if isinstance(local_ret_data, dict) else []
    local_skus: list[str] = []
    if isinstance(sku_link, list):
        for item in sku_link:
            if isinstance(item, dict):
                name = str(item.get("TbSku_name") or "").strip()
                if name:
                    local_skus.append(name)
    ali_ret_data = ali_raw.get("retData") if isinstance(ali_raw.get("retData"), dict) else {}
    ali_ret_data = ali_ret_data if isinstance(ali_ret_data, dict) else {}
    upstream_skus = _itemlink_build_upstream_skus(ali_ret_data)
    suggested_matches = _itemlink_best_unique_matches(local_skus, upstream_skus)
    payload_rows = [
        {
            "shopNick": shop_nick,
            "itemId": local_item_id,
            "url": source_offer_url,
            "tbSkuName": row["local_sku"],
            "aliSkuName": row["upstream_sku"],
        }
        for row in suggested_matches
    ]
    return {
        "success": True,
        "data": {
            "offer_id": offer_id,
            "local_skus": local_skus,
            "upstream_skus": upstream_skus,
            "suggested_matches": suggested_matches,
            "payload_rows": payload_rows,
        },
    }


def _itemlink_build_preview_markdown(local_skus: list[str], upstream_skus: list[str], suggested_matches: list[dict[str, Any]]) -> str:
    lines = ["## SKU 自动匹配", ""]
    if suggested_matches:
        for row in suggested_matches:
            lines.append(f"`{row['local_sku']}---{row['upstream_sku']} --匹配度：{row['score_percent']}%`")
    else:
        lines.append("_无可匹配数据_")
    lines.extend(["", "## SKU 清单", "", "### 本店 SKU", ""])
    if local_skus:
        for i, s in enumerate(local_skus, 1):
            lines.append(f"{i}. {s}")
    else:
        lines.append("_无数据_")
    lines.extend(["", "### 上家 SKU", ""])
    if upstream_skus:
        for i, s in enumerate(upstream_skus, 1):
            lines.append(f"{i}. {s}")
    else:
        lines.append("_无数据_")
    lines.extend(["", "## 二次确认", "", "确认后由执行侧保存 SKU 关联。"])
    return "\n".join(lines)


def run_link_preview(
    *,
    token: str,
    shop_id: str,
    shop_nick: str,
    local_item_id: str,
    source_offer_url: str,
    purchase_account: str,
) -> dict[str, Any]:
    """能力三 Step 5：SKU 自动匹配预览（中台 newGetLinkMessage + verifyAndReturn）。"""
    queried = _itemlink_query_skus(
        token=token,
        shop_id=shop_id,
        shop_nick=shop_nick,
        local_item_id=local_item_id,
        source_offer_url=source_offer_url,
        purchase_account=purchase_account,
    )
    if not queried.get("success"):
        return queried
    data = queried["data"]
    return {
        "success": True,
        "markdown": _itemlink_build_preview_markdown(data["local_skus"], data["upstream_skus"], data["suggested_matches"]),
        "data": {
            "shop_id": shop_id,
            "shop_nick": shop_nick,
            "local_item_id": local_item_id,
            "source_offer_url": source_offer_url,
            "offer_id": data["offer_id"],
            "purchase_account": purchase_account,
            "local_skus": data["local_skus"],
            "upstream_skus": data["upstream_skus"],
            "suggested_matches": data["suggested_matches"],
            "pending_payload_rows": data["payload_rows"],
        },
    }


def run_confirm_link(
    *,
    token: str,
    shop_id: str,
    shop_nick: str,
    local_item_id: str,
    source_offer_url: str,
    purchase_account: str,
    limit_rows: int | None = None,
) -> dict[str, Any]:
    """能力三 Step 7：二次确认后保存（中台 newImportItemLinkByUrl）。"""
    queried = _itemlink_query_skus(
        token=token,
        shop_id=shop_id,
        shop_nick=shop_nick,
        local_item_id=local_item_id,
        source_offer_url=source_offer_url,
        purchase_account=purchase_account,
    )
    if not queried.get("success"):
        return queried
    data = queried["data"]
    payload_rows = data["payload_rows"]
    if limit_rows is not None:
        if limit_rows < 1:
            return _fail("## 保存关联失败\n\n`limit_rows` 须为正整数。", {}, "invalid_limit_rows")
        payload_rows = payload_rows[:limit_rows]
    if not payload_rows:
        return _fail("## 保存关联失败\n\n无可提交的 SKU 映射。", {}, "empty_payload_rows")

    saved = _itemlink_call_new_import_item_link_by_url(token=token, shop_id=shop_id, rows=payload_rows)
    if saved.get("_http_error") or saved.get("_request_error"):
        return _fail(f"## 保存关联失败\n\n{saved}", {"upstream": saved, "payload_rows": payload_rows}, "import_http_error")
    if str(saved.get("retCode") or "") != "0000":
        return _fail(
            f"## 保存关联失败\n\n{saved.get('retMsg', '')}",
            {"upstream": saved, "payload_rows": payload_rows},
            saved.get("retMsg"),
        )
    ret_data = saved.get("retData") if isinstance(saved.get("retData"), dict) else {}
    return _ok(
        "\n".join(
            [
                "## 保存关联成功",
                "",
                f"{ret_data.get('completionMessage', saved.get('retMsg', '成功！'))}",
            ]
        ),
        {
            "shop_id": shop_id,
            "shop_nick": shop_nick,
            "local_item_id": local_item_id,
            "source_offer_url": source_offer_url,
            "purchase_account": purchase_account,
            "submitted_count": len(payload_rows),
            "save_result": ret_data,
            "payload_rows": payload_rows,
        },
    )


def douyin_list_shops(*, token: str | None) -> dict[str, Any]:
    """抖音：查询当前 JWT 用户已绑定的分销店铺列表。"""
    try:
        resolve_jwt_token(token=token)
    except ValueError:
        return _fail_auth("## 查询店铺", {"total": 0, "shops": []})

    url = douyin_skill_url("/shops/bindByAliUser")
    try:
        body = request_json("GET", url, token=token)
        if body.get("retCode") == "0000":
            raw_list = body.get("retData") or []
            shops = []
            for item in raw_list:
                if not isinstance(item, dict):
                    continue
                sid = item.get("shopId") or item.get("id")
                name = item.get("shopName") or item.get("name") or sid
                if sid is None:
                    continue
                shops.append({"id": str(sid), "name": str(name)})
            data = {"total": len(shops), "shops": shops}
            md = f"## 查询店铺\n\n共 {len(shops)} 个绑定店铺。"
            return _ok(md, data)
        return _fail(
            f"## 查询店铺\n\n{body.get('retMsg', '查询店铺列表失败')}",
            {"total": 0, "shops": []},
            body.get("retMsg"),
        )
    except ValueError:
        return _fail_auth("## 查询店铺", {"total": 0, "shops": []})
    except requests.exceptions.ConnectionError:
        return _fail("## 查询店铺\n\n无法连接到 API 服务器。", {"total": 0, "shops": []})
    except requests.exceptions.Timeout:
        return _fail("## 查询店铺\n\n请求超时。", {"total": 0, "shops": []})
    except requests.exceptions.HTTPError:
        return _fail_http("## 查询店铺", {"total": 0, "shops": []})
    except (KeyError, TypeError) as exc:
        return _fail(f"## 查询店铺\n\n响应解析失败：{exc}", {"total": 0, "shops": []}, str(exc))


def douyin_list_distributors(*, token: str | None, shop_id: str) -> dict[str, Any]:
    """抖音：查询店铺绑定的分销账号。"""
    sid = (shop_id or "").strip()
    if not sid:
        return _fail(
            "## 查询分销账号\n\n请提供 shop-id。",
            {"authorized": False, "authUrl": None, "accounts": []},
            "missing_shop_id",
        )

    url = douyin_skill_url("/fxUser/list")
    params = {"platform": "dy", "izAliWarehouseOrder": "true", "shopId": sid}
    try:
        body = request_json("GET", url, token=token, params=params)
        if body.get("retCode") == "0000":
            raw_list = body.get("retData") or []
            accounts = []
            for item in raw_list:
                if not isinstance(item, dict):
                    continue
                accounts.append(
                    {
                        "id": str(item.get("id")),
                        "name": item.get("purchasingAccount") or "",
                        "defaultPurchase": item.get("defaultPurchase"),
                        "userId": item.get("userId"),
                        "aiWorkbenchAccount": item.get("aiWorkbenchAccount"),
                        "isOpenAliWarehouseService": item.get("isOpenAliWarehouseService"),
                        "expireTime": item.get("expireTime"),
                    }
                )
            data = {"authorized": len(accounts) > 0, "authUrl": None, "accounts": accounts}
            md = f"## 查询分销账号\n\n店铺 `{sid}` 共 {len(accounts)} 个分销账号。"
            return _ok(md, data)
        return _fail(
            f"## 查询分销账号\n\n{body.get('retMsg', '查询分销账号失败')}",
            {"authorized": False, "authUrl": None, "accounts": []},
            body.get("retMsg"),
        )
    except ValueError:
        return _fail_auth("## 查询分销账号", {"authorized": False, "accounts": []})
    except requests.exceptions.ConnectionError:
        return _fail("## 查询分销账号\n\n无法连接到 API 服务器。", {"authorized": False, "accounts": []})
    except requests.exceptions.Timeout:
        return _fail("## 查询分销账号\n\n请求超时。", {"authorized": False, "accounts": []})
    except requests.exceptions.HTTPError:
        return _fail_http("## 查询分销账号", {"authorized": False, "accounts": []})
    except KeyError as exc:
        return _fail(f"## 查询分销账号\n\n响应解析失败：{exc}", {"authorized": False, "accounts": []}, str(exc))


def douyin_list_shop_products(*, token: str | None, shop_nick: str) -> dict[str, Any]:
    """抖音：查询店铺下在售商品列表。"""
    shop_nick = (shop_nick or "").strip()
    if not shop_nick:
        return _fail("## 店铺商品\n\n缺少参数：请提供 --shop-nick。", {"total": 0, "products": []}, "missing_shop_nick")
    first_shop_nick = shop_nick.split(",")[0] if "," in shop_nick else shop_nick
    url = douyin_skill_url("/itemlink/syn")
    params = {
        "shopNick": shop_nick,
        "shopId": first_shop_nick,
        "sellerCid": "",
        "linkStatus": "0",
        "itemId": "",
        "itemIds": "",
        "itemIdList": "",
        "title": "",
        "outId": "",
        "outIdBegin": "",
        "ytOutId": "",
        "pageNum": "1",
        "pageSize": "10",
        "fxAutoSwitch": "",
        "purchaseAccount": "",
        "showRecentPurchaseHistory": "false",
        "showRecentPurchase30History": "false",
        "modifyDesc": "",
        "platForm": "",
        "tradeReq": "",
        "isAutoJump": "",
        "supplierName": "",
        "proxyStatus": "",
        "cIfLink": "",
        "waitOrderSortType": "",
    }
    try:
        body = request_json("GET", url, token=token, params=params)
        if body.get("retCode") == "0000":
            ret_data_str = body.get("retData", "{}")
            ret_data = json.loads(ret_data_str)
            items_response = ret_data.get("items_onsale_get_response", {})
            items_data = items_response.get("items", {})
            raw_items = items_data.get("item", [])
            if isinstance(raw_items, dict):
                raw_items = [raw_items]
            elif raw_items is None:
                raw_items = []
            total = items_response.get("total_results", len(raw_items))
            products = []
            for item in raw_items:
                products.append(
                    {
                        "id": str(item.get("num_iid")),
                        "title": item.get("title"),
                        "price": item.get("price"),
                        "pic_url": item.get("pic_url"),
                        "sold_quantity": item.get("sold_quantity"),
                        "outer_id": item.get("outer_id"),
                    }
                )
            data = {"total": total, "products": products}
            md = f"## 店铺商品\n\n共 {total} 条（本页 {len(products)} 条）。"
            return _ok(md, data)
        return _fail(
            f"## 店铺商品\n\n{body.get('retMsg', '查询商品列表失败')}",
            {"total": 0, "products": []},
            body.get("retMsg"),
        )
    except ValueError:
        return _fail_auth("## 店铺商品", {"total": 0, "products": []})
    except json.JSONDecodeError as exc:
        return _fail(f"## 店铺商品\n\n解析 retData 失败：{exc}", {"total": 0, "products": []}, str(exc))
    except requests.exceptions.ConnectionError:
        return _fail("## 店铺商品\n\n无法连接到 API 服务器。", {"total": 0, "products": []})
    except requests.exceptions.Timeout:
        return _fail("## 店铺商品\n\n请求超时。", {"total": 0, "products": []})
    except requests.exceptions.HTTPError:
        return _fail_http("## 店铺商品", {"total": 0, "products": []})
    except KeyError as exc:
        return _fail(f"## 店铺商品\n\n响应解析失败：{exc}", {"total": 0, "products": []}, str(exc))


def douyin_enable_link_type(
    *,
    token: str | None,
    item_ids: str,
    shop: str,
    purchasing_accounts: str,
) -> dict[str, Any]:
    """抖音：开启分销商品开关，多个 itemId 英文逗号分隔。"""
    ids = [x.strip() for x in (item_ids or "").split(",") if x.strip()]
    shop = (shop or "").strip()
    purchasing_accounts = (purchasing_accounts or "").strip()
    if not ids:
        return _fail(
            "## 开启分销商品\n\n商品 ID 不能为空。",
            {"total": 0, "success_count": 0, "fail_count": 0, "success_items": [], "fail_items": []},
            "empty_item_ids",
        )
    if not shop:
        return _fail(
            "## 开启分销商品\n\n店铺名称不能为空。",
            {
                "total": len(ids),
                "success_count": 0,
                "fail_count": len(ids),
                "success_items": [],
                "fail_items": [{"item_id": i, "error": "缺少店铺"} for i in ids],
            },
        )
    if not purchasing_accounts:
        return _fail(
            "## 开启分销商品\n\n采购账号列表不能为空。",
            {
                "total": len(ids),
                "success_count": 0,
                "fail_count": len(ids),
                "success_items": [],
                "fail_items": [{"item_id": i, "error": "缺少采购账号"} for i in ids],
            },
        )
    try:
        resolve_jwt_token(token=token)
    except ValueError:
        return _fail_auth("## 开启分销商品", {"total": len(ids), "success_items": [], "fail_items": []})
    success_list: list[str] = []
    fail_list: list[dict[str, Any]] = []
    url = douyin_skill_url("/daifa/relation")
    for item_id in ids:
        params = {"itemId": item_id, "shop": shop, "linkStatus": "true", "purchasingAccounts": purchasing_accounts, "shopId": shop}
        try:
            body = request_json("GET", url, token=token, params=params)
            if body.get("retCode") == "0000":
                ret_data = body.get("retData") or {}
                if ret_data.get("isSuccess"):
                    success_list.append(item_id)
                else:
                    fail_list.append({"item_id": item_id, "error": "开启失败"})
            else:
                fail_list.append({"item_id": item_id, "error": body.get("retMsg", "开启失败")})
        except ValueError:
            fail_list.append({"item_id": item_id, "error": _MSG_AUTH_FAIL_USER})
        except requests.exceptions.ConnectionError:
            fail_list.append({"item_id": item_id, "error": "无法连接到 API 服务器"})
        except requests.exceptions.Timeout:
            fail_list.append({"item_id": item_id, "error": "请求超时"})
        except requests.exceptions.HTTPError:
            fail_list.append({"item_id": item_id, "error": _MSG_HTTP_FAIL_USER})
        except Exception as exc:
            fail_list.append({"item_id": item_id, "error": str(exc)})
    data = {
        "total": len(ids),
        "success_count": len(success_list),
        "fail_count": len(fail_list),
        "success_items": success_list,
        "fail_items": fail_list,
        "published_count": len(success_list),
        "failed_items": fail_list,
    }
    md = f"## 开启分销商品\n\n成功 {len(success_list)} 个，失败 {len(fail_list)} 个；店铺「{shop}」。"
    if fail_list:
        return _fail(md + "\n\n部分商品开启分销开关失败。", data, "部分商品开启分销开关失败")
    return _ok(md, data)


def douyin_save_automation_order(
    *,
    token: str | None,
    shop_name: str,
    purchase_account: str,
) -> dict[str, Any]:
    """抖音：保存自动下单配置。"""
    shop_name = (shop_name or "").strip()
    purchase_account = (purchase_account or "").strip()
    if not shop_name or not purchase_account:
        return _fail("## 自动下单\n\n缺少参数：请提供 --shop-name 与 --purchase-account。", {"saved": False}, "missing_params")
    try:
        resolve_jwt_token(token=token)
    except ValueError:
        return _fail_auth("## 自动下单", {"saved": False})
    url = douyin_skill_url("/automationOrder")
    body = {
        "autoMerge": True,
        "bindSupplierName": False,
        "checkIzModifyAutoOrder": False,
        "compositionsFreight": False,
        "compositionsFreightSetting": 0,
        "defaultCiphertext": True,
        "doubleAddress": True,
        "flagColor": "",
        "freight": False,
        "freightButNopProfit": False,
        "freightSetting": 0,
        "gift": True,
        "highestPurchasePrice": None,
        "highestSalePrice": "",
        "isSkipPrint": False,
        "isSkipPrintAliShop": None,
        "itemAutomatic": False,
        "itemSkip": False,
        "lastPurchasePriceSwitch": False,
        "lowerPurchasePrice": 0,
        "lowerSalePrice": 0,
        "multipleSubAllRelated": False,
        "multipleSubSameSupplier": False,
        "openAutoOrderAccount": None,
        "openAutoOrderTime": None,
        "oprater": "",
        "orderFrequency": 1,
        "orderHighestLimitMoney": None,
        "orderHighestLimitPercentum": None,
        "orderLimitLose": False,
        "orderLimitMoney": 0,
        "orderLimitMoreorders": False,
        "orderLimitPercentum": 0,
        "orderLimitWord": False,
        "orderLimitWordBuyer": False,
        "orderPriceChoose": "lowest",
        "platform": "dy",
        "productNum": False,
        "productNumForMulti": False,
        "productNumSetting": 1,
        "productNumSettingForMulti": 0,
        "profitMarginSwitch": False,
        "profitSwitch": False,
        "purchaseAccount": purchase_account,
        "purchaseFilterSwitch": False,
        "receiveProvince": False,
        "receiveProvinceSetting": "全部",
        "saleFilterSwitch": False,
        "sameAddress": False,
        "shopName": shop_name,
        "shunFeng": True,
        "skipHaveCancelRecord": None,
        "skuMatched": False,
        "skuMatchedDegree": 0,
        "sleepPlaceOrder": "",
        "status": True
    }
    try:
        resp_body = request_json("POST", url, token=token, json_body=body)
        if resp_body.get("retCode") == "0000":
            msg = resp_body.get("retData", "设置成功")
            md = f"## 自动下单\n\n已为店铺「{shop_name}」保存自动下单配置，采购账号：`{purchase_account}`。\n\n{msg}"
            return _ok(md, {"saved": True, "shop_name": shop_name, "purchase_account": purchase_account})
        return _fail(f"## 自动下单\n\n保存失败：{resp_body.get('retMsg', '未知错误')}", {"saved": False}, resp_body.get("retMsg"))
    except ValueError:
        return _fail_auth("## 自动下单", {"saved": False})
    except requests.exceptions.ConnectionError:
        return _fail("## 自动下单\n\n无法连接中台 API。", {"saved": False})
    except requests.exceptions.HTTPError:
        return _fail_http("## 自动下单", {"saved": False})


def douyin_list_purchase_accounts_after_sale(*, token: str | None, shop_id: str) -> dict[str, Any]:
    """抖音：售后采购账号列表。"""
    sid = (shop_id or "").strip()
    if not sid:
        return _fail("## 查询分销账号（售后）\n\n请提供 shop-id。", {"accounts": []}, "missing_shop_id")
    try:
        resolve_jwt_token(token=token)
    except ValueError:
        return _fail_auth("## 查询分销账号（售后）", {"accounts": []})
    url = douyin_skill_url("/afterSale/queryPurchaseAccountList")
    params = {"platform": "dy", "shopId": sid}
    try:
        body = request_json("GET", url, token=token, params=params)
        if body.get("retCode") == "0000":
            raw = body.get("retData")
            accounts = _normalize_after_sale_purchase_accounts(raw)
            data = {"shop_id": sid, "accounts": accounts, "total": len(accounts), "raw": raw}
            md = f"## 查询分销账号（售后）\n\n店铺 `{sid}` 共 {len(accounts)} 个采购账号（来源 afterSale/queryPurchaseAccountList）。"
            return _ok(md, data)
        return _fail(f"## 查询分销账号（售后）\n\n{body.get('retMsg', '查询失败')}", {"shop_id": sid, "accounts": [], "response": body}, body.get("retMsg"))
    except ValueError:
        return _fail_auth("## 查询分销账号（售后）", {"accounts": []})
    except requests.exceptions.ConnectionError:
        return _fail("## 查询分销账号（售后）\n\n无法连接到 API 服务器。", {"accounts": []})
    except requests.exceptions.Timeout:
        return _fail("## 查询分销账号（售后）\n\n请求超时。", {"accounts": []})
    except requests.exceptions.HTTPError:
        return _fail_http("## 查询分销账号（售后）", {"accounts": []})


_DOUYIN_AFTER_SALE_SETTING_JSON = '{"priceHigh":"1000","priceLower":"0","afterSaleRemarks":false,"afterSaleRemarksPosition":"soft","afterSaleAddressRemarks":false,"orderFrequency":0,"purchaseAccount":"","shopNames":"","status":true,"soAfterSalesType":false,"qualityReturn":false,"shipOverTenDays":false,"multipleSubOrders":true,"loginName":"17865312395:hlf03","platform":"dy","sellerNum":0,"autoRefundSelf":false,"autoRefundPostfeeSelf":false,"freightApply":true,"freightApplyDutiable":true,"deductionAmount":0,"aliNickApplyPostFeeSwitch":false,"poAfterSaleType":"{\\"noShipRefund\\":true,\\"shipRefund\\":true,\\"returnRefund\\":true,\\"refundSuccess\\":true,\\"normalRefundSuccess\\":true,\\"quickRefundSuccess\\":true}","poFillWaybillCode":true,"cancelFxOrder":true,"refundHasBeenSigned":false,"autoRemoveApply":false,"changeApplyType":false,"autoExchange":false,"cancelReason":"syn","cancelReasonInfo":"noBuy","izFilterAliNick":false,"izWhiteAliNick":"0","izOpenAddressCheck":true,"noAfterSaleSellerNum":0,"pointAfterSaleSellerNum":0,"poNoShipExplain":"不想要了，谢谢","poPartRefund":false,"poPartRefundLowestSwitch":false,"poPartRefundLowest":"","poReturnRefund":"不想要了，谢谢","poShipExplain":"不想要了，谢谢","soNoHandleReason":"{\\"other\\":true,\\"noReasonRefund\\":true,\\"expressLongTime\\":true,\\"stockout\\":true,\\"lossOfFunc\\":true,\\"noDeliverPromise\\":true,\\"shootTooMuch\\":true,\\"flaw\\":true,\\"wrongAddrOrPhone\\":true,\\"refundFreight\\":true,\\"noLike\\":true,\\"giftOmission\\":true,\\"fakeBrand\\":true,\\"misbeat\\":true,\\"wrongPart\\":true,\\"breakage\\":true,\\"refundAgree\\":true,\\"wrongPrice\\":true,\\"funcFailure\\":true,\\"signNotTake\\":true,\\"descriptionDnt\\":true,\\"noWant\\":true,\\"noMatchEffect\\":true,\\"sizeWrong\\":true,\\"lessProduct\\":true,\\"logisticsNoSend\\":true,\\"noMatchDate\\":true,\\"deliveryWrong\\":true,\\"flawProduct\\":true,\\"noMatchBrand\\":true,\\"slowDelivery\\":true,\\"packBreakage\\":true,\\"noGoodsSize\\":true,\\"sizeNoMatch\\":true,\\"commodityQuality\\":true,\\"goodsNotArrive\\":true,\\"noMatchCommodityDiscript\\":true,\\"flawQualityProduct\\":true,\\"noMatchGoodsSize\\":true,\\"productQualityNotGood\\":true,\\"wrongAddressNotReceiving\\":true,\\"textureSoBad\\":true,\\"productMetamorphism\\":true}","checkIzModifyAutoAfterSale":false}'
_DOUYIN_DEFAULT_AFTER_SALE_SETTING_BODY: dict[str, Any] = json.loads(_DOUYIN_AFTER_SALE_SETTING_JSON)

def douyin_save_auto_after_sale(
    *,
    token: str | None,
    shop_id: str,
    purchase_account: str,
    shop_names: str,
    body_overrides: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """抖音：保存售后规则。"""
    sid = (shop_id or "").strip()
    if not sid:
        return _fail("## 售后处理\n\n缺少参数：请提供 shop-id。", {"saved": False}, "missing_shop_id")
    try:
        resolve_jwt_token(token=token)
    except ValueError:
        return _fail_auth("## 售后处理", {"saved": False})
    url = douyin_skill_url("/afterSale/setting")
    params = {"shopId": sid}
    payload = deepcopy(_DOUYIN_DEFAULT_AFTER_SALE_SETTING_BODY)
    if body_overrides:
        payload.update(body_overrides)
    payload.pop("loginName", None)
    payload["purchaseAccount"] = (purchase_account or "").strip()
    payload["shopNames"] = (shop_names or "").strip()
    try:
        resp_body = request_json("POST", url, token=token, params=params, json_body=payload)
        if resp_body.get("retCode") == "0000":
            msg = _after_sale_success_user_msg(resp_body.get("retData"))
            pa = payload.get("purchaseAccount")
            sn = payload.get("shopNames")
            md = f"## 售后处理\n\n已提交完整售后配置（purchaseAccount=`{pa}`，shopNames=`{sn}`）。\n\n{msg}"
            return _ok(md, {"saved": True, "shop_id": sid, "purchase_account": pa, "shop_names": sn, "raw": resp_body.get("retData")})
        return _fail(f"## 售后处理\n\n保存失败：{resp_body.get('retMsg', '未知错误')}", {"saved": False, "response": resp_body}, resp_body.get("retMsg"))
    except ValueError:
        return _fail_auth("## 售后处理", {"saved": False})
    except requests.exceptions.ConnectionError:
        return _fail("## 售后处理\n\n无法连接中台 API。", {"saved": False})
    except requests.exceptions.HTTPError:
        return _fail_http("## 售后处理", {"saved": False})


def douyin_run_link_preview(
    *,
    token: str,
    shop_id: str,
    shop_nick: str,
    local_item_id: str,
    source_offer_url: str,
    purchase_account: str,
) -> dict[str, Any]:
    """抖音：SKU 自动匹配预览。"""
    queried = _douyin_itemlink_query_skus(
        token=token,
        shop_id=shop_id,
        shop_nick=shop_nick,
        local_item_id=local_item_id,
        source_offer_url=source_offer_url,
        purchase_account=purchase_account,
    )
    if not queried.get("success"):
        return queried
    data = queried["data"]
    return {
        "success": True,
        "markdown": _itemlink_build_preview_markdown(data["local_skus"], data["upstream_skus"], data["suggested_matches"]),
        "data": {
            "shop_id": shop_id,
            "shop_nick": shop_nick,
            "local_item_id": local_item_id,
            "source_offer_url": source_offer_url,
            "offer_id": data["offer_id"],
            "purchase_account": purchase_account,
            "local_skus": data["local_skus"],
            "upstream_skus": data["upstream_skus"],
            "suggested_matches": data["suggested_matches"],
            "pending_payload_rows": data["payload_rows"],
        },
    }


def douyin_run_confirm_link(
    *,
    token: str,
    shop_id: str,
    shop_nick: str,
    local_item_id: str,
    source_offer_url: str,
    purchase_account: str,
    limit_rows: int | None = None,
) -> dict[str, Any]:
    """抖音：确认并保存 SKU 映射。"""
    queried = _douyin_itemlink_query_skus(
        token=token,
        shop_id=shop_id,
        shop_nick=shop_nick,
        local_item_id=local_item_id,
        source_offer_url=source_offer_url,
        purchase_account=purchase_account,
    )
    if not queried.get("success"):
        return queried
    data = queried["data"]
    payload_rows = data["payload_rows"]
    if limit_rows is not None:
        if limit_rows < 1:
            return _fail("## 保存关联失败\n\n`limit_rows` 须为正整数。", {}, "invalid_limit_rows")
        payload_rows = payload_rows[:limit_rows]
    if not payload_rows:
        return _fail("## 保存关联失败\n\n无可提交的 SKU 映射。", {}, "empty_payload_rows")
    saved = _douyin_itemlink_call_new_import_item_link_by_url(token=token, shop_id=shop_id, rows=payload_rows)
    if saved.get("_http_error") or saved.get("_request_error"):
        return _fail(f"## 保存关联失败\n\n{saved}", {"upstream": saved, "payload_rows": payload_rows}, "import_http_error")
    if str(saved.get("retCode") or "") != "0000":
        return _fail(
            f"## 保存关联失败\n\n{saved.get('retMsg', '')}",
            {"upstream": saved, "payload_rows": payload_rows},
            saved.get("retMsg"),
        )
    ret_data = saved.get("retData") if isinstance(saved.get("retData"), dict) else {}
    return _ok(
        "\n".join(["## 保存关联成功", "", f"{ret_data.get('completionMessage', saved.get('retMsg', '成功！'))}"]),
        {
            "shop_id": shop_id,
            "shop_nick": shop_nick,
            "local_item_id": local_item_id,
            "source_offer_url": source_offer_url,
            "purchase_account": purchase_account,
            "submitted_count": len(payload_rows),
            "save_result": ret_data,
            "payload_rows": payload_rows,
        },
    )


def douyin_link_source(
    *,
    token: str | None,
    downstream_item_id: str,
    source_offer_id: str | None,
    shop: str,
    purchasing_accounts: str,
) -> dict[str, Any]:
    """抖音：关联货源。"""
    raw_ids = (downstream_item_id or "").strip()
    if not raw_ids or not (shop or "").strip() or not (purchasing_accounts or "").strip():
        return _fail(
            "## 关联货源\n\n缺少参数：需要 --downstream-item-id、--shop、--purchasing-accounts（及鉴权 token）。",
            {"published_count": 0, "failed_items": [{"reason": "missing_params"}]},
            "missing_params",
        )
    r = douyin_enable_link_type(token=token, item_ids=raw_ids, shop=shop, purchasing_accounts=purchasing_accounts)
    out = dict(r)
    out["markdown"] = out["markdown"].replace("## 开启分销商品", "## 关联货源", 1)
    d = dict(out.get("data") or {})
    d["source_offer_id"] = (source_offer_id or "").strip() or None
    if "," not in raw_ids:
        d["item_id"] = raw_ids
        d["shop"] = (shop or "").strip()
    out["data"] = d
    return out


def douyin_query_procurement_settings(*, token: str | None, shop_id: str | None) -> dict[str, Any]:
    """抖音：绑定店铺列表；若传 shop_id 再查分销账号。"""
    r_shops = douyin_list_shops(token=token)
    if not r_shops["success"]:
        return r_shops
    shops = r_shops["data"].get("shops", [])
    accounts: list[dict[str, Any]] = []
    if shop_id and shop_id.strip():
        r_dist = douyin_list_distributors(token=token, shop_id=shop_id.strip())
        if not r_dist["success"]:
            md = f"## 采购设置\n\n已查询店铺 {len(shops)} 个；查询分销账号失败：{r_dist.get('error', r_dist['markdown'])}"
            return _fail(
                md,
                {"shops": shops, "accounts": [], "total_shops": len(shops), "shop_id": shop_id.strip()},
                r_dist.get("error"),
            )
        accounts = r_dist["data"].get("accounts", [])
    lines = [f"- 绑定店铺：{len(shops)} 个"]
    for s in shops:
        lines.append(f"  - {s['name']}（shopId={s['id']}）")
    if shop_id and shop_id.strip():
        lines.append(f"- 店铺 `{shop_id.strip()}` 分销账号：{len(accounts)} 个")
        for a in accounts:
            lines.append(f"  - {a.get('name') or a.get('id')}")
    md = "## 采购设置\n\n" + "\n".join(lines)
    return _ok(
        md,
        {"shops": shops, "accounts": accounts, "total_shops": len(shops), "shop_id": shop_id.strip() if shop_id else None},
    )


def _douyin_itemlink_call_new_get_link_message(
    *,
    token: str,
    shop_id: str,
    item_id: str,
    shop_nick: str,
    purchase_account: str,
) -> dict[str, Any]:
    url = douyin_skill_url("/itemlink/newGetLinkMessage")
    params: dict[str, str] = {
        "itemId": item_id.strip(),
        "shopNick": shop_nick.strip(),
        "purchaseAccount": (purchase_account or "").strip(),
        "shopId": shop_id.strip(),
    }
    try:
        return request_json("GET", url, token=token, params=params, timeout=60)
    except requests.exceptions.HTTPError as exc:
        return {"_http_error": True, "status": exc.response.status_code if exc.response else None, "text": exc.response.text if exc.response else str(exc)}
    except requests.exceptions.RequestException as exc:
        return {"_request_error": True, "message": str(exc)}


def _douyin_itemlink_call_verify_and_return(
    *,
    token: str,
    shop_id: str,
    ali_url: str,
    offer_id: str,
    shop_nick: str,
    purchase_account: str,
) -> dict[str, Any]:
    url = douyin_skill_url("/itemlink/verifyAndReturn")
    params = {"shopId": shop_id.strip()}
    body = {
        "aliAccessToken": "",
        "dataBean": {
            "aliUrl": ali_url.strip(),
            "offerId": offer_id.strip(),
            "orderSource": "",
            "platform": "dy",
            "loginName": "",
            "purchasingAccount": (purchase_account or "").strip(),
            "urlNumber": 0,
            "shopNick": shop_nick.strip(),
        },
    }
    try:
        return request_json("POST", url, token=token, params=params, json_body=body, timeout=60)
    except requests.exceptions.HTTPError as exc:
        return {"_http_error": True, "status": exc.response.status_code if exc.response else None, "text": exc.response.text if exc.response else str(exc)}
    except requests.exceptions.RequestException as exc:
        return {"_request_error": True, "message": str(exc)}


def _douyin_itemlink_call_new_import_item_link_by_url(
    *,
    token: str,
    shop_id: str,
    rows: list[dict[str, Any]],
    only_ali_url: str = "true",
) -> dict[str, Any]:
    url = douyin_skill_url("/itemlink/newImportItemLinkByUrl")
    params = {"shopId": shop_id.strip(), "onlyAliUrl": only_ali_url}
    try:
        return request_json("POST", url, token=token, params=params, json_body=rows, timeout=120)
    except requests.exceptions.HTTPError as exc:
        return {"_http_error": True, "status": exc.response.status_code if exc.response else None, "text": exc.response.text if exc.response else str(exc)}
    except requests.exceptions.RequestException as exc:
        return {"_request_error": True, "message": str(exc)}


_DOUYIN_SIZE_TAIL_RE = re.compile(
    r"^(?:xxxl|xxl|xxs|xl|xs|xn|xn|xn|xn|xn|\d+xl|[2-9]xl|[smlx]{1,4}|" r"\d+(?:\.\d+)?|" r"均码|[大小中长]码|加长款?|短款)$",
    re.IGNORECASE,
)


def _douyin_normalize_fold(s: str) -> str:
    return (s or "").replace("\u3000", " ").strip().replace(" ", "")


def _douyin_upstream_key_kind(raw_key: str) -> str:
    k = (raw_key or "").strip()
    if not k:
        return "misc"
    low = k.lower()
    for frag in ("尺码", "尺寸", "规格"):
        if frag in k:
            return "size"
    for frag in ("颜色", "色号", "颜色分类", "款式"):
        if frag in k:
            return "color"
    if low in ("size", "sizes"):
        return "size"
    if low in ("color", "colors"):
        return "color"
    return "misc"


def _douyin_upstream_split_dimensions(upstream: str) -> dict[str, Any]:
    sizes: list[str] = []
    colors: list[str] = []
    misc_parts: list[str] = []
    for seg in (upstream or "").split(";"):
        seg = seg.strip()
        if not seg or ":" not in seg:
            continue
        lk, lv = seg.split(":", 1)
        lv = lv.strip()
        kind = _douyin_upstream_key_kind(lk.strip())
        if kind == "size":
            sizes.append(lv)
        elif kind == "color":
            colors.append(lv)
        else:
            misc_parts.append(f"{lk.strip()}:{lv}")
    return {"sizes": sizes, "colors": colors, "misc": misc_parts}


def _douyin_normalize_size_token(tok: str) -> str:
    t = _douyin_normalize_fold(tok).upper().translate(str.maketrans("０１２３４５６７８９ＸＳＭＬ", "0123456789XSML"))
    t = re.sub(r"[^\w\u4e00-\u9fff]+", "", t)
    if not t:
        return ""
    if "均码" in tok:
        return "ONE"
    ux = t.upper()
    if ux.startswith("XXXL"):
        return "XXXL"
    if ux.startswith("XXL"):
        return "XXL"
    if ux.startswith("XXS"):
        return "XXS"
    if ux.startswith("XS"):
        return "XS"
    if ux.startswith("XL"):
        return "XL"
    mx = re.match(r"^(\d+)XL$", ux)
    if mx:
        return mx.group(0)
    mx2 = re.match(r"^[2-9]XL$", ux)
    if mx2:
        return ux
    if ux in ("S", "M", "L"):
        return ux
    if re.fullmatch(r"\d+(?:\.\d+)?", ux):
        return ux
    return ux


def _douyin_normalize_size_sequence(t: str) -> str:
    u = _douyin_normalize_fold(t).upper()
    u = u.replace("XXXXL", "XXXL").replace("XXXX", "XXXL")
    return _douyin_normalize_size_token(u)


def _douyin_tail_looks_like_size(token: str) -> bool:
    t = token.strip()
    if not t:
        return False
    if _DOUYIN_SIZE_TAIL_RE.match(t):
        return True
    return bool(re.fullmatch(r"\d+(?:\.\d+)?cm?", t, re.I))


def _douyin_split_local_spec_size(local_raw: str) -> tuple[str, str]:
    name = local_raw.strip()
    if not name:
        return "", ""
    norm_slash = name.replace("／", "/")
    if "-" in norm_slash:
        left, right = norm_slash.rsplit("-", 1)
        lt, rt = left.strip(), right.strip()
        if _douyin_tail_looks_like_size(rt):
            return _douyin_normalize_fold(lt.replace("/", "")), rt.strip()
    if "/" in norm_slash:
        for part in norm_slash.split("/"):
            part = part.strip()
            if "-" not in part:
                continue
            lt, rt = part.rsplit("-", 1)
            if _douyin_tail_looks_like_size(rt):
                return _douyin_normalize_fold(lt), rt.strip()
    pieces = [_.strip() for _ in re.split(r"[/\s]+", norm_slash.replace("-", "/")) if _.strip()]
    if pieces and _douyin_tail_looks_like_size(pieces[-1]):
        return _douyin_normalize_fold("".join(pieces[:-1])), pieces[-1]
    return _douyin_normalize_fold(name), ""


def _douyin_overlap_ratio(needle: str, haystack: str) -> float:
    n, h = _douyin_normalize_fold(needle), _douyin_normalize_fold(haystack)
    if not n or not h:
        return 0.0
    if n in h:
        return 1.0
    return difflib.SequenceMatcher(None, n, h).ratio()


def _douyin_pair_match_weight(local: str, upstream: str) -> float:
    spec, lsz_raw = _douyin_split_local_spec_size(local)
    dim = _douyin_upstream_split_dimensions(upstream)
    normalized_sizes = {_douyin_normalize_size_sequence(x) for x in dim["sizes"]}
    normalized_sizes.discard("")
    primary_color = dim["colors"][-1].strip() if dim["colors"] else ""
    spec_f = _douyin_normalize_fold(spec)
    color_f = _douyin_normalize_fold(primary_color)
    lsz = _douyin_normalize_size_sequence(lsz_raw)
    uhay = "".join((_douyin_normalize_fold(upstream), _douyin_normalize_fold(" ".join(dim["sizes"])), _douyin_normalize_fold(" ".join(dim["colors"]))))
    score = difflib.SequenceMatcher(None, _douyin_normalize_fold(local), _douyin_normalize_fold(upstream)).ratio() * 45.0
    if lsz:
        matched_size = lsz in normalized_sizes
        if not matched_size and lsz_raw and dim["sizes"]:
            matched_size = any(
                max(_douyin_overlap_ratio(lsz_raw, x), _douyin_overlap_ratio(lsz, _douyin_normalize_size_sequence(x))) >= 0.86 for x in dim["sizes"]
            )
        score += 5000.0 if matched_size else 0.0
    if spec_f and primary_color:
        if color_f == spec_f:
            score += 5000.0
        else:
            score += _douyin_overlap_ratio(spec_f, primary_color) * 3000.0
            score += _douyin_overlap_ratio(spec_f, uhay) * 500.0
    elif spec_f:
        score += _douyin_overlap_ratio(spec_f, uhay) * 1200.0
    return score


def _douyin_hungarian_square(weight: list[list[float]]) -> list[int | None]:
    n_side = len(weight)
    if n_side == 0:
        return []
    ncol = len(weight[0])
    inf = float("inf")
    u_arr = [0.0] * (n_side + 1)
    v_arr = [0.0] * (ncol + 1)
    match_p = [0] * (ncol + 1)
    way_prev = [0] * (ncol + 1)
    for ti in range(1, n_side + 1):
        match_p[0] = ti
        j_pos = 0
        minv = [inf] * (ncol + 1)
        used = [False] * (ncol + 1)
        while True:
            used[j_pos] = True
            i_now, delta_best, j_next = match_p[j_pos], inf, 0
            for j in range(1, ncol + 1):
                if used[j]:
                    continue
                cur = -weight[i_now - 1][j - 1] - u_arr[i_now] - v_arr[j]
                if cur < minv[j]:
                    minv[j], way_prev[j] = cur, j_pos
                if minv[j] < delta_best:
                    delta_best, j_next = minv[j], j
            for j in range(ncol + 1):
                if used[j]:
                    u_arr[match_p[j]] += delta_best
                    v_arr[j] -= delta_best
                else:
                    minv[j] -= delta_best
            j_pos = j_next
            if match_p[j_pos] == 0:
                break
        while True:
            j_prev = way_prev[j_pos]
            match_p[j_pos] = match_p[j_prev]
            j_pos = j_prev
            if j_pos == 0:
                break
    out = [None] * n_side
    for j in range(1, ncol + 1):
        if match_p[j] != 0:
            out[match_p[j] - 1] = j - 1
    return out


def _douyin_itemlink_pct_from_weight(struct_w: float, surface: float) -> int:
    if struct_w >= 10040.0:
        return min(97, max(72, int(68 + surface * 30)))
    if struct_w >= 5040.0:
        return min(93, max(48, int(42 + surface * 48)))
    return max(20, min(58, int(22 + surface * 92)))


def _douyin_itemlink_best_unique_matches(local_skus: list[str], upstream_skus: list[str]) -> list[dict[str, Any]]:
    if not local_skus or not upstream_skus:
        return []
    n_loc, n_up = len(local_skus), len(upstream_skus)
    padded = max(n_loc, n_up)
    profit = [[0.0] * padded for _ in range(padded)]
    for i in range(n_loc):
        for j in range(n_up):
            profit[i][j] = _douyin_pair_match_weight(local_skus[i], upstream_skus[j])
    pairing = _douyin_hungarian_square(profit)
    used_upstream: set[int] = set()
    consumed_local: set[int] = set()
    rows_out: list[dict[str, Any]] = []
    for li in range(n_loc):
        ji = pairing[li]
        if ji is None or ji >= n_up:
            continue
        consumed_local.add(li)
        used_upstream.add(ji)
        struct_w = profit[li][ji]
        surface = difflib.SequenceMatcher(None, _douyin_normalize_fold(local_skus[li]), _douyin_normalize_fold(upstream_skus[ji])).ratio()
        pct = _douyin_itemlink_pct_from_weight(struct_w, surface)
        rows_out.append({"local_sku": local_skus[li], "upstream_sku": upstream_skus[ji], "score_percent": pct})
    for li in range(n_loc):
        if li in consumed_local:
            continue
        best_j = -1
        best_w = -1.0
        for j in range(n_up):
            if j in used_upstream:
                continue
            ww = profit[li][j]
            if ww > best_w:
                best_w, best_j = ww, j
        if best_j < 0:
            continue
        consumed_local.add(li)
        used_upstream.add(best_j)
        struct_w = profit[li][best_j]
        surface = difflib.SequenceMatcher(None, _douyin_normalize_fold(local_skus[li]), _douyin_normalize_fold(upstream_skus[best_j])).ratio()
        rows_out.append({"local_sku": local_skus[li], "upstream_sku": upstream_skus[best_j], "score_percent": _douyin_itemlink_pct_from_weight(struct_w, surface)})
    rows_out.sort(key=lambda row: local_skus.index(row["local_sku"]))
    return rows_out


def _douyin_itemlink_query_skus(
    token: str,
    shop_id: str,
    shop_nick: str,
    local_item_id: str,
    source_offer_url: str,
    purchase_account: str,
) -> dict[str, Any]:
    local_raw = _douyin_itemlink_call_new_get_link_message(
        token=token,
        shop_id=shop_id,
        item_id=local_item_id,
        shop_nick=shop_nick,
        purchase_account=purchase_account,
    )
    if local_raw.get("_http_error") or local_raw.get("_request_error"):
        return {"success": False, "markdown": f"## 本店 SKU 查询失败\n\n{local_raw}", "data": {"upstream": local_raw}}
    if str(local_raw.get("retCode") or "") != "0000":
        return {"success": False, "markdown": f"## 本店 SKU 查询失败\n\n{local_raw.get('retMsg', '')}", "data": {"upstream": local_raw}}
    offer_id = _itemlink_offer_id_from_url(source_offer_url)
    if not offer_id:
        return {"success": False, "markdown": "## 上家 SKU 查询失败\n\n1688 链接未解析到 offerId。", "data": {"source_offer_url": source_offer_url}}
    ali_raw = _douyin_itemlink_call_verify_and_return(
        token=token,
        shop_id=shop_id,
        ali_url=source_offer_url,
        offer_id=offer_id,
        shop_nick=shop_nick,
        purchase_account=purchase_account,
    )
    if ali_raw.get("_http_error") or ali_raw.get("_request_error"):
        return {"success": False, "markdown": f"## 上家 SKU 查询失败\n\n{ali_raw}", "data": {"upstream": ali_raw}}
    if str(ali_raw.get("retCode") or "") != "0000":
        return {"success": False, "markdown": f"## 上家 SKU 查询失败\n\n{ali_raw.get('retMsg', '')}", "data": {"upstream": ali_raw}}
    local_ret_data = local_raw.get("retData") if isinstance(local_raw.get("retData"), dict) else {}
    sku_link = local_ret_data.get("SkuLink") if isinstance(local_ret_data, dict) else []
    local_skus: list[str] = []
    if isinstance(sku_link, list):
        for item in sku_link:
            if isinstance(item, dict):
                name = str(item.get("dySkuName") or item.get("TbSku_name") or "").strip()
                if not name and isinstance(item.get("dySkuNameList"), list):
                    name = "-".join(str(x).strip() for x in item["dySkuNameList"] if str(x).strip())
                if name:
                    local_skus.append(name)
    ali_ret_data = ali_raw.get("retData") if isinstance(ali_raw.get("retData"), dict) else {}
    ali_ret_data = ali_ret_data if isinstance(ali_ret_data, dict) else {}
    upstream_skus = _itemlink_build_upstream_skus(ali_ret_data)
    #使用抖音的sku精准匹配
    suggested_matches = _douyin_itemlink_best_unique_matches(local_skus, upstream_skus)
    payload_rows = [{"shopNick": shop_nick, "itemId": local_item_id, "url": source_offer_url, "dySkuName": row["local_sku"], "aliSkuName": row["upstream_sku"]} for row in suggested_matches]
    return {"success": True, "data": {"offer_id": offer_id, "local_skus": local_skus, "upstream_skus": upstream_skus, "suggested_matches": suggested_matches, "payload_rows": payload_rows}}

