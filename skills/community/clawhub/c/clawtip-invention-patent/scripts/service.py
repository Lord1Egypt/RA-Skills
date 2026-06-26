#!/usr/bin/env python3
"""Phase 3：携带支付凭证调用履约接口，按 openclaw 约定输出 PAY_STATUS / ERROR_INFO。"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

DEFAULT_BASE = os.environ.get("SKILL_SERVER_BASE_URL", "http://api.clawtip.top").rstrip("/")
GET_RESULT_URL = f"{DEFAULT_BASE}/api/clawtip/getServiceResult"


def fetch_result(question: str, order_no: str, credential: str) -> None:
    payload = json.dumps(
        {
            "question": question,
            "orderNo": order_no,
            "credential": credential,
        },
        ensure_ascii=False,
    ).encode("utf-8")
    req = urllib.request.Request(
        GET_RESULT_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError as e:
        print("PAY_STATUS: ERROR")
        print(f"ERROR_INFO: 网络请求失败: {e}")
        sys.exit(1)

    if body.get("responseCode") not in ("200", 200):
        print("PAY_STATUS: ERROR")
        print(f"ERROR_INFO: {body.get('responseMessage', '服务端错误')}")
        sys.exit(1)

    pay_status = (body.get("payStatus") or "").upper()
    if pay_status == "SUCCESS":
        print("PAY_STATUS: SUCCESS")
        ans = body.get("answer")
        if ans is not None:
            print(ans)
        return

    if pay_status == "PROCESSING":
        print("PAY_STATUS: PROCESSING")
        return

    if pay_status == "FAIL":
        print("PAY_STATUS: FAIL")
        return

    print("PAY_STATUS: ERROR")
    print(f"ERROR_INFO: {body.get('errorInfo', pay_status or '未知错误')}")
    sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(description="发明专利撰写履约查询")
    parser.add_argument("question", help="与下单时一致的用户技术主题/发明要点")
    parser.add_argument("order_no", help="订单号 ORDER_NO")
    parser.add_argument("credential", help="支付凭证 credential")
    args = parser.parse_args()
    fetch_result(args.question, args.order_no, args.credential)


if __name__ == "__main__":
    main()
