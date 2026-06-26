#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基于 ClawTip 研发的 A2A 文章服务平台 - 创建订单

支持三种服务：
  - hot-ranks   热榜数据获取    ¥0.88/次
  - publish     公众号文章发布   ¥1.00/次
  - full-auto   文章全自动化     ¥1.88/次

用法:
  python3 create_order.py "微博,知乎,B站" --slug hot-ranks
"""

import sys
import os
import json
import hashlib
import argparse
import urllib.request
import urllib.error

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'shared'))
from file_utils import save_order

API_BASE = "http://43.136.97.223/clawtip-api/api/createOrder"

SERVICES = {
    "hot-ranks": {
        "slug": "clawtip-hot-ranks",
        "desc": "热榜数据获取",
        "price": "0.88",
    },
    "publish": {
        "slug": "clawtip-publish",
        "desc": "微信公众号文章发布",
        "price": "1.00",
    },
    "full-auto": {
        "slug": "clawtip-full-auto",
        "desc": "文章全自动化（热榜+发布）",
        "price": "1.88",
    },
}


def _md5(text: str) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def create_order(question: str, slug: str) -> tuple:
    """
    调用后端创建订单接口，保存订单到本地并返回订单信息。

    Args:
        question: 用户的需求描述
        slug: 服务类型（hot-ranks / publish / full-auto）

    Returns:
        (order_no, amount, question, indicator) 元组

    Raises:
        RuntimeError: 网络请求失败或后端返回错误
    """
    full_slug = SERVICES[slug]["slug"]

    payload = json.dumps({
        "question": question,
        "slug": full_slug,
    }, ensure_ascii=False)

    req = urllib.request.Request(
        API_BASE,
        data=payload.encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        raise RuntimeError(f"请求创建订单失败: {e}")

    if data.get("responseCode") != "200":
        raise RuntimeError(f"创建订单失败: {data}")

    order_no = data["orderNo"]
    amount = data["amount"]
    indicator = _md5(full_slug)

    save_order(indicator, order_no, {
        "orderNo": order_no,
        "amount": amount,
        "question": question,
        "slug": full_slug,
        "payTo": data["payTo"],
        "encryptedData": data["encryptedData"],
        "indicator": indicator,
    })

    return order_no, amount, question, indicator


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A2A 文章服务平台 - 创建订单",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="示例:\n"
               "  python3 create_order.py \"微博,知乎\" --slug hot-ranks\n"
               "  python3 create_order.py \"发布文章\" --slug publish\n"
               "  python3 create_order.py \"热榜+发布\" --slug full-auto",
    )
    parser.add_argument("question", help="用户的需求描述")
    parser.add_argument("--slug", "-s", choices=SERVICES.keys(), default="hot-ranks",
                        help="服务类型: hot-ranks / publish / full-auto（默认: hot-ranks）")
    args = parser.parse_args()

    svc = SERVICES[args.slug]
    print(f"📋 服务: {svc['desc']} (¥{svc['price']})")

    order_no, amount, question_out, indicator = create_order(args.question, args.slug)

    print(f"ORDER_NO={order_no}")
    print(f"AMOUNT={amount}")
    print(f"QUESTION={question_out}")
    print(f"INDICATOR={indicator}")
