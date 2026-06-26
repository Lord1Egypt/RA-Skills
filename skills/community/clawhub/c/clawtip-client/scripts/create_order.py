#!/usr/bin/env python3
"""Phase 1: 创建离谱甲方订单"""
import sys
import json
import hashlib
import urllib.request
import urllib.error
from file_utils import save_order

CREATE_ORDER_URL = "http://localhost:8080/api/client/createOrder"
SLUG = "clawtip-client"
SKILL_ID = "si-crazy-client"
RESOURCE_URL = "https://ms.jr.jd.com"
DESCRIPTION = "AI离谱甲方 - 专治甲方PTSD"


def compute_indicator(slug: str) -> str:
    return hashlib.md5(slug.encode("utf-8")).hexdigest()


def create_order(question: str) -> tuple:
    payload = json.dumps({"reqData": {"question": question}}).encode("utf-8")
    req = urllib.request.Request(CREATE_ORDER_URL, data=payload,
                                headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = json.loads(resp.read().decode("utf-8")).get("resultData")
    except urllib.error.URLError as e:
        raise RuntimeError(f"网络请求异常: {e}") from e
    if body is None:
        raise RuntimeError("服务端无响应")
    if body.get("responseCode") != "200":
        raise RuntimeError(f"订单创建失败: {body.get('responseMessage', '未知错误')}")
    order_no = body.get("orderNo")
    if not order_no:
        raise RuntimeError("服务端缺少 orderNo")
    return order_no, body.get("amount", "1"), body.get("encryptedData"), body.get("payTo")


def save_order_info(order_no, amount, question, encrypted_data, pay_to, indicator):
    return save_order(indicator, order_no, {
        "skill-id": SKILL_ID, "order_no": order_no, "amount": amount,
        "question": question, "encrypted_data": encrypted_data, "pay_to": pay_to,
        "description": DESCRIPTION, "slug": SLUG, "resource_url": RESOURCE_URL,
    })


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="AI离谱甲方 - 创建订单")
    parser.add_argument("question", help='你的需求brief，格式: "需求描述|行业(设计/文案/程序/其他)"')
    args = parser.parse_args()
    indicator = compute_indicator(SLUG)
    try:
        order_no, amount, encrypted_data, pay_to = create_order(args.question)
    except RuntimeError as e:
        print(f"订单创建失败: {e}")
        sys.exit(1)
    save_order_info(order_no, amount, args.question, encrypted_data, pay_to, indicator)
    print(f"ORDER_NO={order_no}")
    print(f"AMOUNT={amount}")
    print(f"QUESTION={args.question}")
    print(f"INDICATOR={indicator}")
