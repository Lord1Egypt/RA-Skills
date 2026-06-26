#!/usr/bin/env python3
"""
订单管理
提供创建订单、订单历史、订单详情功能
"""

import argparse

from common import output_error, output_json, request_api


def order_create(sku_id, spu_id, addr_id):
    """
    创建订单 - 用户选择对应的商品规格进行下单

    Args:
        sku_id: 商品规格ID，必传
        spu_id: 商品ID，必传
        addr_id: 收货地址ID，必传

    Returns:
        包含订单信息、收货地址、支付链接的 JSON
    """
    if not sku_id:
        output_error("商品规格ID不能为空")
    if not spu_id:
        output_error("商品ID不能为空")
    if not addr_id:
        output_error("收货地址ID不能为空")

    return request_api("order_create", {"skuId": sku_id, "spuId": spu_id, "addrId": addr_id})


def order_history():
    """
    订单历史 - 查询用户已下单的订单

    Returns:
        包含订单列表的 JSON
    """
    return request_api("order_history", {})


def order_detail(order_id):
    """
    订单详情 - 查询用户的详细订单信息

    Args:
        order_id: 订单ID，必传

    Returns:
        包含订单状态、金额、时间、物流等详细信息的 JSON
    """
    if not order_id:
        output_error("订单ID不能为空", example="python order.py detail 198553155075")

    return request_api("order_detail", {"orderId": order_id})


def main():
    """解析命令行参数并执行订单管理操作。"""
    parser = argparse.ArgumentParser(description="百度优选订单管理")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # create 子命令 - 创建订单
    create_parser = subparsers.add_parser("create", help="创建订单")
    create_parser.add_argument("--sku-id", type=int, required=True, help="商品规格ID")
    create_parser.add_argument("--spu-id", type=int, required=True, help="商品ID")
    create_parser.add_argument("--addr-id", type=int, required=True, help="收货地址ID")

    # history 子命令 - 订单历史
    subparsers.add_parser("history", help="订单历史")

    # detail 子命令 - 订单详情
    detail_parser = subparsers.add_parser("detail", help="订单详情")
    detail_parser.add_argument("order_id", type=int, help="订单ID")

    args = parser.parse_args()

    if args.command == "create":
        result = order_create(args.sku_id, args.spu_id, args.addr_id)
        output_json(result)
    elif args.command == "history":
        result = order_history()
        output_json(result)
    elif args.command == "detail":
        result = order_detail(args.order_id)
        output_json(result)
    else:
        parser.print_help()
        output_error(
            "请指定命令: create, history 或 detail",
            examples=[
                "python order.py create --sku-id 293900212 --spu-id 293900210 --addr-id 12345678",
                "python order.py history",
                "python order.py detail 198553155075",
            ],
        )


if __name__ == "__main__":
    main()
