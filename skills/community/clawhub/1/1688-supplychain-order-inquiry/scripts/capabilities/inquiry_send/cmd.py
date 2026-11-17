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
                        help="订单 ID 列表，逗号分隔，如 '5116391244078005116,5116391244078005117'")
    parser.add_argument("--question", "-q", required=True,
                        help="询盘问题，单个字符串，如 '什么时候能发货'")
    parser.add_argument("--image", default="",
                        help="本地图片路径，多个用逗号分隔（可选，自动上传获取URL）")
    parser.add_argument("--image-url", default="",
                        help="图片URL，多个用逗号分隔（可选，已有在线链接时使用）")
    parser.add_argument("--orders-status", "-s", default="",
                        help='订单状态集合，JSON 字符串数组（可不传），如 \'["WAIT_SELLER_SEND_GOODS"]\'')
    parser.add_argument("--order-single-round", choices=["true", "false"], default=None,
                        help="单轮对话开关（三态，默认不传）。用户明确表达不需要自动回复/不需要多轮对话/不需要AI对话/只需要单轮对话时传 true；明确表达需要自动回复/需要多轮对话/需要AI对话时传 false；未提及则不带此参数")
    parser.add_argument("--ext", default="",
                        help='扩展字段 ext，JSON 字符串 map（可不传）。sessionId、chat_id 由 CLI 自动从运行时环境变量（NEWTON_SESSION_ID、NEWTON_REPLY_ID）注入，通常无需手写；仅在需要额外/覆盖字段时显式传，显式值优先级更高，如 \'{"bizTag":"vip"}\'')
    parser.add_argument("--timeout", type=int, default=None,
                        help='询盘超时时间，单位分钟（正整数）。用户明确表达"设置询盘超时时间为 X 分钟/X 小时"等意图时，由 agent 换算成分钟整数传入（如 2 小时→120），会注入 ext.timeout 透传给接口；未提及则不带此参数')
    parser.add_argument("--is-price-negotiation", choices=["true", "false"], default=None,
                        help="是否改价/议价意图（布尔值）。由 workflow 意图解析层识别用户意图后传入，注入 ext.isPriceNegotiation 透传给接口；未提及则不带此参数")
    parser.add_argument("--orders-detail", default="",
                        help='按订单维度指定附件，JSON 字符串数组（可不传）。每个元素为 {"order_id":"xxx","image_urls":["..."],"file_urls":["..."]}。'
                             '传入时按订单维度循环调用 gateway，返回 wwTaskId 列表；未传入则走原有单次调用逻辑')
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

        # 单轮对话开关三态：true/false → bool；未传 → None（不下发）
        order_single_round = None
        if args.order_single_round is not None:
            order_single_round = args.order_single_round == "true"

        # 解析 ext（JSON map，可不传）
        ext = None
        if args.ext:
            try:
                ext = json.loads(args.ext)
            except json.JSONDecodeError as e:
                print_output(False, "ext 参数 JSON 格式错误: {}".format(e), {})
                return
            if not isinstance(ext, dict):
                print_output(False, "ext 参数必须是 JSON 对象（map）", {})
                return

        # 解析 orders_detail（按订单维度附件，JSON 数组，可不传）
        orders_detail = None
        if args.orders_detail:
            try:
                orders_detail = json.loads(args.orders_detail)
            except json.JSONDecodeError as e:
                print_output(False, "orders-detail 参数 JSON 格式错误: {}".format(e), {})
                return
            if not isinstance(orders_detail, list):
                print_output(False, "orders-detail 参数必须是 JSON 数组", {})
                return

        # 改价/议价意图标识：true/false → bool；未传 → None（不下发）
        is_price_negotiation = None
        if args.is_price_negotiation is not None:
            is_price_negotiation = args.is_price_negotiation == "true"

        result = inquiry_send(
            order_ids=order_ids,
            question=args.question,
            local_images=local_images,
            image_urls=image_urls,
            orders_status=orders_status,
            order_single_round=order_single_round,
            ext=ext,
            inquiry_timeout=args.timeout,
            orders_detail=orders_detail,
            is_price_negotiation=is_price_negotiation,
        )

        # 根据返回结构区分：orders_detail 模式返回 results 列表，原模式返回单个 wwTaskId
        if "results" in result:
            # orders_detail 模式：按订单维度的结果列表
            results_list = result.get("results", [])
            success_count = result.get("success_count", 0)
            fail_count = result.get("fail_count", 0)
            message = "询盘已触发，成功 {}/{}，耗时 {}s".format(
                success_count, success_count + fail_count, result.get("elapsed_seconds", ""))
            output_data = {
                "results": results_list,
                "success_count": success_count,
                "fail_count": fail_count,
                "elapsed_seconds": result.get("elapsed_seconds", 0),
            }
        else:
            # 原模式：单个 wwTaskId
            message = "询盘已触发，订单数={}，耗时 {}s。询盘任务编号：{}，可凭此编号查询商家回复。".format(
                len(order_ids),
                result.get("elapsed_seconds", ""),
                result.get("wwTaskId", ""),
            )
            output_data = {
                "suc": result.get("suc", False),
                "errorMsg": result.get("errorMsg", ""),
                "wwTaskId": result.get("wwTaskId", ""),
                "elapsed_seconds": result.get("elapsed_seconds", 0),
            }
        print_output(True, message, output_data)
    except KeyboardInterrupt:
        print_output(False, "用户中断操作", {})
    except Exception as e:
        print_error(e, {})


if __name__ == "__main__":
    main()
