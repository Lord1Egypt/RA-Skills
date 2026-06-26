import sys
import json
import hashlib
import argparse
import urllib.request
import urllib.error

from file_utils import save_order
from config import CREATE_ORDER_URL, RESOURCE_URL

# 硬编码的 slug，用于计算 indicator
SLUG = "clawtip-weather"


def compute_indicator(slug: str) -> str:
    """根据 slug 计算 MD5 作为 indicator。"""
    return hashlib.md5(slug.encode("utf-8")).hexdigest()


def create_order(question: str) -> tuple:
    """
    向创建订单接口发起 POST 请求。
    成功返回 (order_no, amount, encrypted_data, pay_to)，失败抛出 RuntimeError。
    """
    payload = json.dumps({"reqData": {"question": question}}).encode("utf-8")
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
        raise RuntimeError(f"网络请求异常，请确认网络连接并稍后重试: {e}") from e

    if body is None:
        raise RuntimeError("网络请求异常，请确认网络连接并稍后重试")

    if body.get("responseCode") != "200":
        raise RuntimeError(
            f"订单创建失败: {body.get('responseMessage', '未知错误')}"
        )

    order_no = body.get("orderNo")
    if not order_no:
        raise RuntimeError("订单创建响应中缺少 orderNo 字段")

    return (
        order_no,
        body.get("amount"),
        body.get("encryptedData"),
        body.get("payTo"),
    )


def save_order_info(order_no: str, amount: str, question: str,
                    encrypted_data: str, pay_to: str, indicator: str) -> str:
    """
    构建订单数据并持久化到本地 JSON 文件。
    dict key 采用驼峰是因为内容需要写入 JSON 文件，同时兼容后端接口的出入参格式。
    """
    order_data = {
        "skillId": "si-weather-reporter",
        "orderNo": order_no,
        "amount": amount,
        "question": question,
        "encryptedData": encrypted_data,
        "payTo": pay_to,
        "description": "天气报告服务费用",
        "slug": SLUG,
        "resourceUrl": RESOURCE_URL,
    }
    return save_order(indicator, order_no, order_data)


def main():
    parser = argparse.ArgumentParser(description="创建天气订单")
    parser.add_argument("question", help="需要查询天气的地点")
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


if __name__ == "__main__":
    main()