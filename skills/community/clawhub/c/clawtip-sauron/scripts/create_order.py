import sys
import json
import hashlib
import urllib.request
import urllib.error

from file_utils import save_order
from config import (
    CREATE_ORDER_URL,
    SLUG,
    SKILL_ID,
    DESCRIPTION,
    RESOURCE_URL,
)


def compute_indicator(slug: str) -> str:
    """根据 slug 计算 MD5 作为 indicator。"""
    return hashlib.md5(slug.encode("utf-8")).hexdigest()


def create_order(question: str) -> tuple:
    """
    POST the user's question to the createOrder endpoint.
    Returns (order_no, amount, encrypted_data, pay_to) on success, or raises RuntimeError on failure.
    """
    payload = json.dumps({"question": question}).encode("utf-8")
    req = urllib.request.Request(
        CREATE_ORDER_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as resp:
            body = json.loads(resp.read().decode("utf-8")).get("resultData")
    except urllib.error.URLError as e:
        raise RuntimeError(f"网络请求异常，请确认后端服务已启动: {e}") from e

    if body is None:
        raise RuntimeError("网络请求异常，请确认后端服务已启动")

    if body.get("responseCode") != "200":
        raise RuntimeError(
            f"Order creation failed: {body.get('responseMessage', 'unknown error')}"
        )

    order_no = body.get("orderNo")
    if not order_no:
        raise RuntimeError("Order creation response missing 'orderNo'")

    amount = body.get("amount")
    encrypted_data = body.get("encryptedData")
    pay_to = body.get("payTo")

    return order_no, amount, encrypted_data, pay_to


def save_order_info(order_no: str, amount: str, question: str,
                    encrypted_data: str, pay_to: str, indicator: str) -> str:
    """
    Save order info to the fixed directory.
    Includes all fixed values needed by clawtip payment skill and dynamic values.
    Returns the full path of the saved JSON file.
    """
    order_data = {
        "skill-id": SKILL_ID,
        "order_no": order_no,
        "amount": amount,
        "question": question,
        "encrypted_data": encrypted_data,
        "pay_to": pay_to,
        "description": DESCRIPTION,
        "slug": SLUG,
        "resource_url": RESOURCE_URL,
    }
    return save_order(indicator, order_no, order_data)


import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="创建索伦娃娃购买订单")
    parser.add_argument("question", help="购买信息（商品名）")
    args = parser.parse_args()

    indicator = compute_indicator(SLUG)

    try:
        order_no, amount, encrypted_data, pay_to = create_order(args.question)
    except RuntimeError as e:
        print(f"订单创建失败: {e}")
        sys.exit(1)

    save_order_info(order_no, amount, args.question,
                    encrypted_data, pay_to, indicator)

    print(f"ORDER_NO={order_no}")
    print(f"AMOUNT={amount}")
    print(f"QUESTION={args.question}")
    print(f"INDICATOR={indicator}")
