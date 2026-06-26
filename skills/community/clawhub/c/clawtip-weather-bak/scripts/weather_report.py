import sys
import json
import hashlib
import urllib.request
import urllib.error

from file_utils import load_order

GET_RESULT_URL = "https://ms.jr.jd.com/gw2/generic/hyqy/na/m/getWeatherResult"

# 硬编码的 skill-name，与 create_order.py 保持一致
SKILL_NAME = "clawtip-weather"


def compute_indicator(skill_name: str) -> str:
    """根据 skill-name 计算 MD5 作为 indicator。"""
    return hashlib.md5(skill_name.encode("utf-8")).hexdigest()



def counseling(question: str, order_no: str, credential: str) -> str:
    print("weather reporting location is: " + question)
    if credential is None:
        return "Please enter your counseling credential"

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
        raise RuntimeError(f"Counseling request failed: {e}") from e

    if body.get("responseCode") != "200":
        raise RuntimeError(
            f"Counseling failed: {body.get('responseMessage', 'unknown error')}"
        )

    pay_status = body.get("payStatus")
    print(f"PAY_STATUS: {pay_status}")

    answer = body.get("answer")
    if not answer  and "ERROR" == pay_status:
        # 避免 key 不存在时报错
        raise RuntimeError(f'获取信息失败：原因：{body.get("errorInfo", "未知错误")}')
    return answer


import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Get weather counseling report")
    parser.add_argument("order_no", help="Order number")
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
        print(f"ERROR: {e}")
        sys.exit(1)