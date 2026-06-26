# -*- coding: utf-8 -*-
"""
科力普采购助手 - 非交互式下单
用于 AI Agent 直接调用：搜索 → 展示 → 用户选编号 → 确认下单
"""
import sys
import json
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from colipu_client import ColipuClient

def _err(msg):
    print(f"\n[X] {msg}\n", flush=True)

def _ok(msg):
    print(f"[OK] {msg}", flush=True)

def _info(msg):
    print(f"[i] {msg}", flush=True)

def search_products_only(keyword, max_price=None, province_id=2):
    """只搜索商品，返回商品列表"""
    client = ColipuClient()

    if not client.config.login_name or not client.config.password:
        _err("缺少凭据：请设置环境变量 COLIPU_LOGIN_NAME / COLIPU_PASSWORD")
        return None

    login_result = client.login()
    if login_result.get("code") != 1:
        _err("登录失败，账号或密码可能不对")
        return None

    search_result = client.search_products(keyword=keyword, province_id=province_id, page_size=50)
    all_products = search_result.get("Data", [])

    if not all_products:
        _err(f"没有找到「{keyword}」，换个关键词试试")
        return None

    products = all_products
    if max_price:
        before = len(products)
        products = [p for p in products if p.get("SalePrice", 0) <= max_price]
        if not products:
            _err(f"没有找到 {max_price}元 以内的「{keyword}」")
            return None
        _info(f"在 {before} 个商品中，筛选出 {len(products)} 个 ≤ {max_price}元 的商品")

    return products, client


def place_order(client, selected_products):
    """确认并下单"""
    receivers = client.get_receivers()
    cost_centers = client.get_valid_cost_centers()
    receiver = receivers[0] if receivers else {}
    cost_center = cost_centers[0] if cost_centers else {}

    items = [
        client.build_order_item(
            item_sku_id=p.get("ItemId") or p.get("ProductSkuId"),
            sale_price=p.get("SalePrice", 0),
            sale_qty=1
        )
        for p in selected_products
    ]

    pre_result = client.pre_create_order(
        receiver_id=receiver.get("ReceiverId"),
        cost_center_id=cost_center.get("CostCenterId"),
        items=items
    )

    if not pre_result.get("Data", {}).get("Success"):
        msg = pre_result.get("Data", {}).get("Message", "")
        _err(f"预提交失败：{msg}")
        return None

    guid = pre_result.get("Data", {}).get("Message")

    confirm_result = client.confirm_order(guid=guid)

    if confirm_result.get("Code") == 200 and confirm_result.get("Data", {}).get("Success"):
        so_id = client.wait_order_create_result(guid, timeout=30) or "异步生成中（稍后到订单列表查询）"

        total = sum(p.get("SalePrice", 0) for p in selected_products)
        names = " / ".join([p.get("ItemFullName", "")[:25] for p in selected_products])

        print(f"\n{'=' * 50}", flush=True)
        print(f"[OK] 下单成功！", flush=True)
        print(f"{'=' * 50}", flush=True)
        print(f"  订单号：{so_id}", flush=True)
        print(f"  商品：{names}", flush=True)
        print(f"  总价：{total:.2f}元", flush=True)
        print(f"  收件人：{receiver.get('ContactName', '')} | {receiver.get('Area', '')}", flush=True)
        print(f"  成本中心：{cost_center.get('CostCenterName', '')}", flush=True)
        print(f"  状态：待成本中心审批", flush=True)
        return so_id
    else:
        msg = confirm_result.get("Data", {}).get("Message", "")
        _err(f"下单失败：{msg}")
        return None


if __name__ == "__main__":
    # 搜索 A4 打印纸
    print("=" * 55, flush=True)
    print("搜索 A4 打印纸（价格 ≤ 200元）", flush=True)
    print("=" * 55, flush=True)

    result = search_products_only("A4打印纸", max_price=200)
    if not result:
        sys.exit(1)

    products, client = result

    print(f"\n找到 {len(products)} 个商品，随机展示前 10 个：", flush=True)
    for i, p in enumerate(products[:10], 1):
        name = p.get("ItemFullName", "")[:42]
        price = p.get("SalePrice", 0)
        item_id = p.get("ItemId") or p.get("ProductSkuId")
        print(f"  {i}. {name} ... {price}元 (ID: {item_id})", flush=True)

    print(f"\n（如需指定商品，请告诉我编号，如：1 3）", flush=True)
