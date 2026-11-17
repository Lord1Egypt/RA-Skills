#!/usr/bin/env python3
"""多店铺商品诊断汇总服务

遍历用户绑定的多个店铺，逐个查询异常商品列表并汇总输出。
通过 NEWTON_SHOP_LOGIN_ID 参数指定店铺，由服务端切换登录态。
支持通过 shop_name 模糊匹配指定单个店铺查询。

改造说明：
- 新增 lite 参数透传给 get_abnormal_offers，开启 valueMap 裁剪
- 新增 max_total_rows 参数，多店汇总后按跌幅绝对值排序截断
- 截断时注入 truncation_info 供 Agent 展示截断提示
- 截断后每条 item 注入 shop_name 和 loginId 永久字段
"""

from capabilities.get_bindlist.service import get_bindlist
from capabilities.get_abnormal_offers.service import get_abnormal_offers

# 硬性封顶最大值，不可绕过
MAX_TOTAL_ROWS_HARD_LIMIT = 20


def _get_cycle_crc_abs(item: dict) -> float:
    """获取 payAmt.cycleCrc 的绝对值用于排序，字段不存在时返回 -1 排末尾。"""
    value_map = item.get("valueMap")
    if not isinstance(value_map, dict):
        return -1.0
    pay_amt = value_map.get("payAmt")
    if not isinstance(pay_amt, dict):
        return -1.0
    crc = pay_amt.get("cycleCrc")
    if crc is None:
        return -1.0
    try:
        return abs(float(crc))
    except (TypeError, ValueError):
        return -1.0


def run_multi_shop_product_analysis(
    shop_name: str = None,
    date_type: str = "RECENT_7",
    device: str = "ALL",
    max_total_rows: int = 20,
    lite: bool = True,
) -> dict:
    """批量查询多店铺异常商品并汇总。

    Args:
        shop_name: 指定店铺名称（模糊匹配 companyName），不传则查询所有绑定店铺。
        date_type: 日期类型，可选 RECENT_7 / RECENT_30。
        device:    设备筛选，可选 ALL / PC / APP。
        max_total_rows: 多店汇总后全局硬封顶行数，超出则按跌幅绝对值排序后从尾部裁掉。
                        硬性最大值 20，即使传入 > 20 也会被强制截到 20。
        lite:      是否开启 lite 裁剪模式（默认开启），透传给 get_abnormal_offers。

    Returns:
        包含各店铺异常商品的汇总 dict，结构为 {"shops": [...], "truncation_info": ...}.
        truncation_info 仅在发生截断时注入。
    """
    # 硬性封顶：即使 CLI 传入 > 20 也强制截到 20
    effective_max = min(max_total_rows, MAX_TOTAL_ROWS_HARD_LIMIT)

    # 1. 获取所有绑定店铺
    shops = get_bindlist()

    # 2. 无绑定店铺 → 不传 login_id，使用当前登录态（兼容改造前行为）
    #    无绑定店铺降级分支：不排序截断，但需透传 lite
    if not shops:
        items = get_abnormal_offers(date_type=date_type, device=device, lite=lite)
        return {
            "shops": [{
                "shop_name": "当前店铺",
                "is_current": True,
                "count": len(items),
                "items": items,
            }]
        }

    # 3. 确定目标店铺
    if shop_name:
        matched = [s for s in shops if shop_name in s.get("companyName", "")]
        if not matched:
            return {"error": f"未找到名称包含「{shop_name}」的店铺", "shops": []}
        target_shops = matched
    else:
        target_shops = shops

    # 4. 遍历执行 — 通过 login_id 参数指定店铺，透传 lite
    results = []
    shops_with_items = []  # 记录成功调用且返回 len(items) > 0 的店铺名（按遍历顺序）

    for shop in target_shops:
        name = shop.get("companyName", "未知店铺")
        is_current = shop.get("isOwner", False)
        login_id = shop.get("loginId")

        try:
            items = get_abnormal_offers(
                date_type=date_type,
                device=device,
                login_id=login_id,
                lite=lite,
            )
            # 给每条 item 打上临时标记，用于汇总排序和分组写回
            for item in items:
                item["_shop_name"] = name
                item["_login_id"] = login_id

            result_entry = {
                "shop_name": name,
                "is_current": is_current,
                "loginId": login_id,
                "count": len(items),
                "items": items,
            }

            if len(items) > 0:
                shops_with_items.append(name)

            results.append(result_entry)
        except Exception as e:
            results.append({
                "shop_name": name,
                "is_current": is_current,
                "loginId": login_id,
                "error": str(e),
                "count": 0,
                "items": [],
            })

    # 5. 汇总排序 + 截断（只要有绑定店铺、且汇总后总条数 > effective_max 就执行）
    all_items = []
    for result_entry in results:
        if "error" not in result_entry:
            all_items.extend(result_entry["items"])

    total_before_truncation = len(all_items)

    if total_before_truncation > effective_max:
        # 5a. 排序：按 payAmt.cycleCrc 绝对值从大到小（绝对值越大跌幅越严重排越前）
        all_items.sort(key=_get_cycle_crc_abs, reverse=True)

        # 5b. 截断
        all_items = all_items[:effective_max]
        total_after_truncation = len(all_items)

        # 5c. 分组写回：按原始对象归属更新各店铺，店铺名称并不保证唯一。
        kept_item_ids = {id(item) for item in all_items}

        for result_entry in results:
            if "error" in result_entry:
                continue
            kept_items = [
                item for item in result_entry["items"]
                if id(item) in kept_item_ids
            ]

            # 注入永久字段 shop_name 和 loginId，删除临时标记 _shop_name 和 _login_id
            for item in kept_items:
                item["shop_name"] = item["_shop_name"]
                item["loginId"] = item["_login_id"]
                del item["_shop_name"]
                del item["_login_id"]

            result_entry["items"] = kept_items
            result_entry["count"] = len(kept_items)

        # 5d. 移除 count=0 且无 error 的店铺（避免返回空壳数据）
        results = [
            r for r in results
            if "error" in r or r.get("count", 0) > 0
        ]

        # 5e. 截断提示注入
        truncation_info = {
            "total_before_truncation": total_before_truncation,
            "total_after_truncation": total_after_truncation,
            "shops_with_items": shops_with_items,
            "truncated": True,
        }

        return {
            "truncation_info": truncation_info,
            "shops": results,
        }
    else:
        # 无截断：清除临时标记，注入永久字段
        for result_entry in results:
            if "error" in result_entry:
                continue
            for item in result_entry["items"]:
                item["shop_name"] = item["_shop_name"]
                item["loginId"] = item["_login_id"]
                del item["_shop_name"]
                del item["_login_id"]

        # 无截断时不注入 truncation_info
        return {"shops": results}
