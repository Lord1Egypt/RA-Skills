import sys
import json
import hashlib
import urllib.request
import urllib.error

from file_utils import load_order
from config import GET_RESULT_URL, SLUG


def compute_indicator(slug: str) -> str:
    """根据 slug 计算 MD5 作为 indicator。"""
    return hashlib.md5(slug.encode("utf-8")).hexdigest()


def fulfill_order(question: str, order_no: str, credential: str) -> str:
    """支付成功后，向后端发起履约请求，获取自取凭证。"""
    if credential is None:
        raise RuntimeError("缺少支付凭证 payCredential")

    payload = json.dumps({
        "question": question,
        "orderNo": order_no,
        "credential": credential
    }).encode("utf-8")

    req = urllib.request.Request(
        GET_RESULT_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req) as resp:
            body = json.loads(resp.read().decode("utf-8")).get("resultData")
    except urllib.error.URLError as e:
        raise RuntimeError(f"履约请求失败: {e}") from e

    if body is None:
        raise RuntimeError("履约请求失败，请确认后端服务已启动")

    if body.get("responseCode") != "200":
        raise RuntimeError(
            f"履约失败: {body.get('responseMessage', 'unknown error')}"
        )

    pay_status = body.get("payStatus")
    print(f"PAY_STATUS: {pay_status}")

    if pay_status == "ERROR":
        error_info = body.get("errorInfo", "未知错误")
        print(f"ERROR_INFO: {error_info}")
        raise RuntimeError(f"获取自取凭证失败：原因：{error_info}")

    answer = body.get("answer")
    return answer


import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="发放索伦娃娃自取凭证")
    parser.add_argument("order_no", help="Order number")
    args = parser.parse_args()

    indicator = compute_indicator(SLUG)

    try:
        order_data = load_order(indicator, args.order_no)
        question = order_data.get("question")
        if not question:
            raise RuntimeError("订单文件中缺少 question 字段")
        credential = order_data.get("payCredential")
        if not credential:
            raise RuntimeError("订单文件中缺少 payCredential 字段")
        result = fulfill_order(question, args.order_no, credential)
        if result:
            print(result)
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)
