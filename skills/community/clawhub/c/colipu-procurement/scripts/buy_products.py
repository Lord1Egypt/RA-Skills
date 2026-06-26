# -*- coding: utf-8 -*-
"""
科力普采购助手 - 一站式下单脚本
搜索 → 展示 → 用户选号 → 用户确认(y) → 下单
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from colipu_client import ColipuClient

if os.name == "nt":
    os.system("chcp 65001 >nul 2>&1")

def _err(msg):
    print(f"\n[X] {msg}\n")

def _ok(msg):
    print(f"[OK] {msg}")

def format_products(products):
    """格式化商品列表为易读文本"""
    lines = []
    for i, p in enumerate(products, 1):
        name = p.get("ItemFullName", "")[:40]
        price = p.get("SalePrice", 0)
        item_id = p.get("ItemId") or p.get("ProductSkuId")
        lines.append(f"  {i}. {name} ... {price}元 (ID: {item_id})")
    return "\n".join(lines)


def search_and_select(keyword, max_price=None, num_items=1, province_id=2):
    """
    搜索商品并让用户选择，确认后保存选择结果
    
    Args:
        keyword: 搜索关键词
        max_price: 单品价格上限
        num_items: 最多选几个商品
        province_id: 省份 ID
    """
    client = ColipuClient()

    if not client.config.login_name or not client.config.password:
        _err("缺少凭据：请设置环境变量 COLIPU_LOGIN_NAME / COLIPU_PASSWORD")
        return None

    login_result = client.login()
    if login_result.get("code") != 1:
        _err("登录失败，账号或密码可能不对")
        return None
    _ok("登录成功")

    # 搜索
    search_result = client.search_products(keyword=keyword, province_id=province_id, page_size=50)
    all_products = search_result.get("Data", [])

    if not all_products:
        _err(f"没有找到「{keyword}」，换个关键词试试")
        return None

    # 价格过滤
    products = all_products
    if max_price:
        products = [p for p in products if p.get("SalePrice", 0) <= max_price]
        if not products:
            _err(f"没有找到 {max_price}元 以内的「{keyword}」")
            return None

    price_hint = f"价格 ≤ {max_price}元" if max_price else "价格不限"
    print(f"\n找到 {len(products)} 个商品（{price_hint}），随机展示 {min(num_items, len(products))} 个：")
    print(format_products(products[:num_items]))
    print()

    # 用户选择
    print("-" * 55)
    print("请输入要购买的商品编号（支持多选，用空格分隔，如：1 3）：")
    selected_input = input("> ").strip()

    if not selected_input:
        _err("未选择商品，退出")
        return None

    try:
        selected_indices = [int(x) - 1 for x in selected_input.split()]
    except ValueError:
        _err("输入格式错误，请输入数字编号")
        return None

    selected = []
    for idx in selected_indices:
        if 0 <= idx < len(products):
            selected.append(products[idx])

    if not selected:
        _err("没有有效的商品被选中")
        return None

    # 获取收货地址 & 成本中心（用于展示）
    receivers = client.get_receivers()
    cost_centers = client.get_valid_cost_centers()
    receiver = receivers[0] if receivers else {}
    cost_center = cost_centers[0] if cost_centers else {}

    total = sum(p.get("SalePrice", 0) for p in selected)
    names = " / ".join([p.get("ItemFullName", "")[:20] for p in selected])

    # 展示确认信息
    print(f"\n{'=' * 55}")
    print("【待确认订单】")
    print(f"{'=' * 55}")
    for i, p in enumerate(selected, 1):
        name = p.get("ItemFullName", "")[:40]
        price = p.get("SalePrice", 0)
        item_id = p.get("ItemId") or p.get("ProductSkuId")
        print(f"  {i}. {name} ... {price}元 (ID: {item_id})")
    print(f"\n  合计：{total:.2f}元")
    print(f"  收件人：{receiver.get('ContactName', '')} | {receiver.get('Area', '')}")
    print(f"  成本中心：{cost_center.get('CostCenterName', '')}")
    print(f"\n{'=' * 55}")
    confirm = input("确认提交此订单吗？(y/N): ").strip().lower()
    print(f"{'=' * 55}")

    if confirm != "y":
        print("已取消下单")
        return None

    items = [
        client.build_order_item(
            item_sku_id=p.get("ItemId") or p.get("ProductSkuId"),
            sale_price=p.get("SalePrice", 0),
            sale_qty=1
        )
        for p in selected
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

        print(f"\n{'=' * 50}")
        _ok(f"下单成功！")
        print(f"{'=' * 50}")
        print(f"  订单号：{so_id}")
        print(f"  商品：{names}")
        print(f"  总价：{total:.2f}元")
        print(f"  状态：待成本中心审批")
        return so_id
    else:
        msg = confirm_result.get("Data", {}).get("Message", "")
        _err(f"下单失败：{msg}")
        return None


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="buy_products.py",
        description="科力普一站式下单：搜索 → 选号 → 用户确认(y) → 下单",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("keyword", nargs="?", default="黑色保温杯", help="搜索关键词")
    parser.add_argument("max_price", nargs="?", type=float, default=200.0, help="单品价格上限（元），0 或负数表示不限")
    parser.add_argument("num_items", nargs="?", type=int, default=10, help="展示前 N 个候选商品")
    parser.add_argument("--province-id", type=int, default=2, help="搜索时的省份 ID")
    parser.add_argument("--keyword", dest="keyword_kw", help="搜索关键词（与位置参数二选一）")
    parser.add_argument("--max-price", dest="max_price_kw", type=float, help="价格上限（与位置参数二选一）")
    parser.add_argument("--num-items", dest="num_items_kw", type=int, help="展示数量（与位置参数二选一）")
    return parser


def main(argv=None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    keyword = args.keyword_kw or args.keyword
    max_price = args.max_price_kw if args.max_price_kw is not None else args.max_price
    num_items = args.num_items_kw if args.num_items_kw is not None else args.num_items

    if max_price is not None and max_price <= 0:
        max_price = None

    result = search_and_select(
        keyword=keyword,
        max_price=max_price,
        num_items=num_items,
        province_id=args.province_id,
    )
    return 0 if result else 1


if __name__ == "__main__":
    sys.exit(main())
