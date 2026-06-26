#!/usr/bin/env python3
"""
售后服务
查询订单是否可以售后，若能售后返回售后链接
"""

import sys

from common import output_error, output_json, request_api


def after_service(order_id):
    """
    售后服务 - 查询用户订单是否可以售后

    Args:
        order_id: 订单ID，必传

    Returns:
        包含售后状态和售后链接的 JSON
        - canRefund: 是否可申请售后
        - reason: 如果不可售后，说明原因
        - refundUrl: 如果可售后，提供售后申请链接
    """
    if not order_id:
        output_error("订单ID不能为空", example="python after_service.py 198522025249")

    return request_api("after_service", {"orderId": order_id})


def main():
    """解析命令行参数并执行售后服务查询。"""
    # 检查命令行参数是否提供
    if len(sys.argv) < 2:
        output_error("用法: python after_service.py <订单ID>", example="python after_service.py 198522025249")

    # 解析订单ID，确保为数字
    try:
        order_id = int(sys.argv[1])
    except ValueError:
        output_error("订单ID必须是数字", example="python after_service.py 198522025249")

    # 调用售后接口并输出结果
    result = after_service(order_id)
    output_json(result)


if __name__ == "__main__":
    main()
