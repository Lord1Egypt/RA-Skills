#!/usr/bin/env python3
"""
商品检索和详情
提供商品列表搜索和商品详情查询功能
"""

import argparse

from common import output_error, output_json, request_api


def spu_list(keyword):
    """
    商品检索 - 根据query词搜索商品标题信息

    Args:
        keyword: 搜索关键词，必传

    Returns:
        包含商品信息和规格信息的 JSON
    """
    if not keyword:
        output_error("关键词不能为空", example="python spu.py list '智能涌现'")

    return request_api("spu_list", {"query": keyword})


def spu_detail(spu_id):
    """
    商品详情 - 查询商品的详细信息

    Args:
        spu_id: 商品ID，必传

    Returns:
        包含商品详细信息的 JSON（价格、图片、规格、店铺等）
    """
    if not spu_id:
        output_error("商品ID不能为空", example="python spu.py detail 531833605")

    return request_api("spu_detail", {"spuId": spu_id})


def main():
    """解析命令行参数并执行商品检索或详情查询。"""
    parser = argparse.ArgumentParser(description="百度优选商品检索和详情")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # list 子命令 - 商品检索
    list_parser = subparsers.add_parser("list", help="商品检索")
    list_parser.add_argument("keyword", help="搜索关键词")

    # detail 子命令 - 商品详情
    detail_parser = subparsers.add_parser("detail", help="商品详情")
    detail_parser.add_argument("spu_id", type=int, help="商品ID")

    args = parser.parse_args()

    if args.command == "list":
        result = spu_list(args.keyword)
        output_json(result)
    elif args.command == "detail":
        result = spu_detail(args.spu_id)
        output_json(result)
    else:
        parser.print_help()
        output_error(
            "请指定命令: list 或 detail", examples=["python spu.py list '智能涌现'", "python spu.py detail 531833605"]
        )


if __name__ == "__main__":
    main()
