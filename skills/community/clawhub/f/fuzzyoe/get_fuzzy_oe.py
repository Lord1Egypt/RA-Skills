#!/usr/bin/env python3
"""
FUZZY OE skill for OpenClaw.
积智数据 VIN 车型 模糊译码
"""

import sys
import json
import os
import requests
import re


FUZZY_OE_URL = "https://erp.qipeidao.com/jzOpenClaw/getFuzzyOe"

def getFuzzyOe(appkey: str, vin: str,partsNames: list):
    """
    调用 /getFuzzyOe 接口，按 17 位 VIN 车架号的车型 与 待译码的配件名称列表 模糊解析出这些配件的 标准配件编码与标准名信息。

    请求 JSON 示例： "LSVAL41Z882104202"   ["前保险杠皮","中网"]

    """
    if not is_valid_vin(vin):
        return {
            "error": "invalid_vin",
            "msg": "VIN must be 17 characters long and contain only letters and numbers.",
        }
    if not partsNames:
        return {
            "error": "invalid_partsNames",
            "msg": "partsNames must be a list of strings.",
        }
    params = {"apiKey": appkey, "vinCode": vin, "partsNames": partsNames}
    try:
        resp = requests.post(FUZZY_OE_URL, json=params, timeout=100)
    except Exception as e:
        return {
            "error": "request_failed",
            "msg": str(e),
        }

    if resp.status_code != 200:
        return {
            "error": "http_error",
            "state": resp.status_code,
            "msg": resp.text,
        }

    data = json.loads(resp.text)
#     try:
#         data = resp.text.json()
#     except Exception:
#         return {
#             "error": "invalid_json",
#             "body": resp.text,
#         }
    return data;
def is_valid_vin(vin):
    return len(vin) == 17 and re.match(r'^[A-HJ-NPR-Z0-9]{17}$', vin)

def main():
    if len(sys.argv) < 2:
        print(
            "Usage:\n"
            "  get_fuzzy_oe.py 'LSVAL41Z882104202' '[\"前保险杠皮\",\"中网\"]'      # 按 VIN解出的车型+配件名称列表 模糊解析出这些配件的 标准配件编码与标准名信息\n",
            file=sys.stderr,
        )
        sys.exit(1)

    appkey = os.getenv("JZ_API_KEY")

    if not appkey:
        print("Error: JZ_API_KEY must be set in environment.", file=sys.stderr)
        sys.exit(1)


    # 默认：VIN 查询，参数为 JSON
    vin = sys.argv[1]
    if not vin:
        print("Error: 'vin' is required.", file=sys.stderr)
        sys.exit(1)
    partsNames = json.loads(sys.argv[2])
    result = getFuzzyOe(appkey,vin,partsNames)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

