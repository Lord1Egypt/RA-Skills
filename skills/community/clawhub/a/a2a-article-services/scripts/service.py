#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基于 ClawTip 研发的 A2A 文章服务平台 - 服务履约

携带支付凭证调用后端获取服务结果。

用法:
  python3 service.py "<问题>" "<订单号>" "<支付凭证>" --slug hot-ranks
"""

import sys
import os
import json
import hashlib
import argparse
import urllib.request
import urllib.error

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'shared'))
from file_utils import load_order

API_BASE = "http://43.136.97.223/clawtip-api/api/getServiceResult"

SERVICES = {
    "hot-ranks": {
        "slug": "clawtip-hot-ranks",
        "desc": "热榜数据获取",
    },
    "publish": {
        "slug": "clawtip-publish",
        "desc": "微信公众号文章发布",
    },
    "full-auto": {
        "slug": "clawtip-full-auto",
        "desc": "文章全自动化（热榜+发布）",
    },
}


def _md5(text: str) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def get_service_result(question: str, order_no: str, credential: str, slug: str) -> str:
    """
    携带支付凭证调用后端获取服务结果。

    Args:
        question: 用户的需求描述
        order_no: 订单号
        credential: 支付凭证（payCredential）
        slug: 服务类型（hot-ranks / publish / full-auto）

    Returns:
        服务结果字符串（JSON 格式）

    Raises:
        RuntimeError: 网络请求失败
    """
    full_slug = SERVICES[slug]["slug"]
    indicator = _md5(full_slug)

    # 从本地订单文件加载，验证订单存在性
    order = load_order(indicator, order_no)

    print(f"正在执行 {SERVICES[slug]['desc']}: {question}")

    if credential is None:
        return "请输入你的服务凭证"

    payload = json.dumps({
        "question": question,
        "orderNo": order_no,
        "credential": credential,
    }, ensure_ascii=False)

    req = urllib.request.Request(
        API_BASE,
        data=payload.encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        raise RuntimeError(f"请求服务结果失败: {e}")

    if data.get("responseCode") != "200":
        return f"获取服务结果失败: {data}"

    pay_status = data.get("payStatus")
    if pay_status != "SUCCESS":
        error_info = data.get("errorInfo", "支付未成功")
        return f"支付未成功: {error_info}"

    answer = data.get("answer", "")
    already_fulfilled = data.get("alreadyFulfilled", False)

    if already_fulfilled:
        print("该订单已履约过")

    return answer


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A2A 文章服务平台 - 服务履约",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="示例:\n"
               "  python3 service.py \"微博,知乎\" <order_no> <credential> --slug hot-ranks",
    )
    parser.add_argument("question", help="用户的需求描述")
    parser.add_argument("order_no", help="订单号（从 create_order.py 输出获取）")
    parser.add_argument("credential", help="支付凭证（payCredential）")
    parser.add_argument("--slug", "-s", choices=SERVICES.keys(), default="hot-ranks",
                        help="服务类型: hot-ranks / publish / full-auto（默认: hot-ranks）")
    args = parser.parse_args()

    result = get_service_result(args.question, args.order_no, args.credential, args.slug)
    print(result)
    print("PAY_STATUS: SUCCESS")
