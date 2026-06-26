import sys
import json
import hashlib
import argparse
import urllib.request
import urllib.error

from file_utils import load_order
from config import GET_RESULT_URL

# 硬编码的 skill-name，与 create_order.py 保持一致
SKILL_NAME = "clawtip-weather"


def compute_indicator(skill_name: str) -> str:
    """根据 skill-name 计算 MD5 作为 indicator。"""
    return hashlib.md5(skill_name.encode("utf-8")).hexdigest()


def counseling(question: str, order_no: str, credential: str) -> str:
    """向天气报告接口发起查询请求，返回天气结果。"""
    print(f"正在查询天气，地点: {question}")
    if credential is None:
        return "请提供支付凭证"

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
        raise RuntimeError(f"网络请求异常，请确认网络连接并稍后重试: {e}") from e

    if body.get("responseCode") != "200":
        raise RuntimeError(
            f"天气查询失败: {body.get('responseMessage', '未知错误')}"
        )

    pay_status = body.get("payStatus")
    print(f"PAY_STATUS: {pay_status}")

    answer = body.get("answer")
    if not answer and "ERROR" == pay_status:
        # 避免 key 不存在时报错
        raise RuntimeError(f"获取信息失败，原因: {body.get('errorInfo', '未知错误')}")
    return answer


def main():
    parser = argparse.ArgumentParser(description="获取天气报告")
    parser.add_argument("order_no", help="订单号")
    args = parser.parse_args()

    indicator = compute_indicator(SKILL_NAME)

    try:
        order_data = load_order(indicator, args.order_no)
        question = order_data.get("question")
        if not question:
            raise RuntimeError("订单文件中缺少 question 字段")
        credential = order_data.get("payCredential")
        if not credential:
            raise RuntimeError("订单文件中缺少 payCredential 字段")
        result = counseling(question, args.order_no, credential)
        print(result)
    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()