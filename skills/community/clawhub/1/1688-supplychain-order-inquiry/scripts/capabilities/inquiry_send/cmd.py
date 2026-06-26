#!/usr/bin/env python3
"""订单询盘 CLI 入口 -- 对指定订单发起询盘"""

COMMAND_NAME = "inquiry_send"
COMMAND_DESC = "订单询盘（对指定订单发起询盘）"

import json
import os
import sys
import argparse

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _output import print_output, print_error
from capabilities.inquiry_send.service import inquiry_send


def main():
    parser = argparse.ArgumentParser(description="订单询盘 - 对指定订单发起询盘")
    parser.add_argument("--order-ids", "-o", required=True,
                        help="订单 ID 列表，逗号分隔，最多 10 个，如 '5116391244078005116,5116391244078005117'")
    parser.add_argument("--question", "-q", required=True,
                        help="询盘问题，单个字符串，如 '什么时候能发货'")
    parser.add_argument("--image", default="",
                        help="本地图片路径，多个用逗号分隔（可选，自动上传获取URL）")
    parser.add_argument("--image-url", default="",
                        help="图片URL，多个用逗号分隔（可选，已有在线链接时使用）")
    parser.add_argument("--orders-status", "-s", default="",
                        help='订单状态集合，JSON 字符串数组（可不传），如 \'["WAIT_SELLER_SEND_GOODS"]\'')
    args = parser.parse_args()

    try:
        # 解析订单 ID 列表
        order_ids = [oid.strip() for oid in args.order_ids.split(",") if oid.strip()]
        if not order_ids:
            print_output(False, "订单 ID 列表不能为空", {})
            return

        # 解析图片参数
        local_images = [p.strip() for p in args.image.split(",") if p.strip()] if args.image else None
        image_urls = [u.strip() for u in args.image_url.split(",") if u.strip()] if args.image_url else None

        # 解析 orders_status
        orders_status = None
        if args.orders_status:
            try:
                orders_status = json.loads(args.orders_status)
            except json.JSONDecodeError as e:
                print_output(False, "orders-status 参数 JSON 格式错误: {}".format(e), {})
                return
            if not isinstance(orders_status, list):
                print_output(False, "orders-status 参数必须是 JSON 字符串数组", {})
                return

        result = inquiry_send(
            order_ids=order_ids,
            question=args.question,
            local_images=local_images,
            image_urls=image_urls,
            orders_status=orders_status,
        )

        message = "询盘已触发，订单数={}，耗时 {}s。".format(
            len(order_ids),
            result.get("elapsed_seconds", ""),
        )
        output_data = {
            "suc": result.get("suc", False),
            "errorMsg": result.get("errorMsg", ""),
            "elapsed_seconds": result.get("elapsed_seconds", 0),
        }
        print_output(True, message, output_data)
    except KeyboardInterrupt:
        print_output(False, "用户中断操作", {})
    except Exception as e:
        print_error(e, {})


if __name__ == "__main__":
    main()
