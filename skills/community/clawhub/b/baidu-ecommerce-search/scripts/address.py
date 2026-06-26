#!/usr/bin/env python3
"""
地址管理
提供地址列表、地址识别、地址添加功能
"""

import argparse

from common import output_error, output_json, request_api


def address_list():
    """
    地址列表 - 获取用户地址列表

    Returns:
        包含地址ID、收货人姓名、手机号、地址详情等信息的 JSON
        若用户未登录或地址列表为空，则返回空列表
    """
    return request_api("address_list", {})


def address_recognise(address_text):
    """
    地址识别 - 识别用户输入的地址文本

    Args:
        address_text: 地址信息文本，必传

    Returns:
        包含识别结果的 JSON
    """
    if not address_text:
        output_error("地址信息不能为空", example="python address.py recognise '王大海 北京市百度科技园K1 15612345678'")

    return request_api("address_recognise", {"addressText": address_text})


def address_add(recognise_id):
    """
    地址添加 - 根据识别ID添加地址

    Args:
        recognise_id: 地址识别返回的ID，必传
        调用前必须先调用 address_recognise 获取 recogniseId

    Returns:
        包含新增地址信息的 JSON
    """
    if not recognise_id:
        output_error("识别ID不能为空", example="python address.py add 12345678")

    return request_api("address_add", {"recogniseId": recognise_id})


def main():
    """解析命令行参数并执行地址管理操作。"""
    parser = argparse.ArgumentParser(description="百度优选地址管理")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # list 子命令 - 地址列表
    subparsers.add_parser("list", help="地址列表")

    # recognise 子命令 - 地址识别
    recognise_parser = subparsers.add_parser("recognise", help="地址识别")
    recognise_parser.add_argument("address_text", help="地址信息文本")

    # add 子命令 - 地址添加
    add_parser = subparsers.add_parser("add", help="地址添加")
    add_parser.add_argument("recognise_id", type=int, help="地址识别返回的ID")

    args = parser.parse_args()

    if args.command == "list":
        result = address_list()
        output_json(result)
    elif args.command == "recognise":
        result = address_recognise(args.address_text)
        output_json(result)
    elif args.command == "add":
        result = address_add(args.recognise_id)
        output_json(result)
    else:
        parser.print_help()
        output_error(
            "请指定命令: list, recognise 或 add",
            examples=[
                "python address.py list",
                "python address.py recognise '王大海 北京市百度科技园K1 15612345678'",
                "python address.py add 12345678",
            ],
        )


if __name__ == "__main__":
    main()
