# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd. and/or its affiliates.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#!/usr/bin/env python3
"""火山引擎短信发送 API - openclaw专用接口 (2026-01-01).

Version: 2026-01-01
分组: openclaw专用

6个接口:
    - send_sms: 发送短信
    - list_sms_send_log: 查询发送记录
    - list_sub_account: 查询消息组列表
    - list_signature: 查询签名列表
    - list_sms_template: 查询模板列表
    - list_total_send_count_stat: 查询发送统计

Usage:
    python volc_sms.py <action> [options]

Examples:
    # 发送短信
    python volc_sms.py send_sms \
        --sub-account 77da1acf --signature "火山引擎" --template-id "ST_xxx" \
        --mobiles "13800138000" --template-param '{"code":"123456"}'

    # 查询消息组
    python volc_sms.py list_sub_account

    # 查询签名
    python volc_sms.py list_signature --signature "火山引擎"

    # 查询模板
    python volc_sms.py list_sms_template --signatures "火山引擎"

    # 查询发送记录
    python volc_sms.py list_sms_send_log \
        --sub-account 77da1acf --from-time 1773113285 --to-time 1773213285

    # 查询发送统计
    python volc_sms.py list_total_send_count_stat \
        --start-time 1773113285 --end-time 1773213285
"""

import argparse
import json
import os
import sys

SERVICE = "volcSMS"
VERSION = "2026-01-01"


def get_credentials() -> tuple:
    api_key = os.getenv("ARK_SKILL_API_KEY")
    api_base = os.getenv("ARK_SKILL_API_BASE")
    if not api_key or not api_base:
        raise ValueError(
            "未找到凭证，请设置环境变量 ARK_SKILL_API_KEY 和 ARK_SKILL_API_BASE\n"
            "配置文件位置: /root/.openclaw/.env\n"
            "示例:\n"
            "  ARK_SKILL_API_KEY=sk-xxxx\n"
            "  ARK_SKILL_API_BASE=http://xxx"
        )
    return api_key, api_base


def call_api(action: str, body: dict) -> dict:
    try:
        import requests
    except ImportError:
        print("Error: requests not installed. Run: pip install requests", file=sys.stderr)
        sys.exit(1)

    api_key, api_base = get_credentials()
    
    api_base = api_base.rstrip("/")
    
    url = f"{api_base}?Action={action}&Version={VERSION}"
    
    headers = {
        "Content-Type": "application/json",
        "ServiceName": SERVICE,
        "Authorization": f"Bearer {api_key}",
    }
    
    body_str = json.dumps(body, ensure_ascii=False)
    
    response = requests.post(url, headers=headers, data=body_str.encode("utf-8"), timeout=30)
    response.raise_for_status()
    return response.json()


def send_sms(args) -> dict:
    """发送短信 (SendSmsForAgent).

    Request:
        "Account": "",
        "SubAccount": "",
        "Signature": "",
        "TemplateId": "",
        "Mobiles": "",
        "TemplateParam": ""

    Response:
        "MessageIds": ["xxx", "xxx"]
    """
    body = {
        "SubAccount": args.sub_account,
        "Signature": args.signature,
        "TemplateId": args.template_id,
        "Mobiles": args.mobiles,
    }

    if args.account:
        body["Account"] = args.account
    if args.template_param:
        body["TemplateParam"] = args.template_param

    return call_api("SendSmsForAgent", body)


def list_sms_send_log(args) -> dict:
    """查询发送记录 (ListSmsSendLogForAgent).

    Request:
        "SubAccount": "",
        "FromTime": 1773113285,
        "ToTime": 1773113285,
        "Mobile": "",
        "TemplateId": "",
        "Signature": "",
        "MessageId": "",
        "Page": 1,
        "PageSize": 100

    Response:
        "Total": 123,
        "List": [...]
    """
    body = {
        "SubAccount": args.sub_account,
        "Page": args.page,
        "PageSize": args.page_size,
    }

    if args.from_time:
        body["FromTime"] = args.from_time
    if args.to_time:
        body["ToTime"] = args.to_time
    if args.mobile:
        body["Mobile"] = args.mobile
    if args.template_id:
        body["TemplateId"] = args.template_id
    if args.signature:
        body["Signature"] = args.signature
    if args.message_id:
        body["MessageId"] = args.message_id

    return call_api("ListSmsSendLogForAgent", body)


def list_sub_account(args) -> dict:
    """查询消息组列表 (ListSubAccountForAgent).

    说明: 只返回审核通过的消息组

    Request:
        "SubAccountName": ""

    Response:
        "Total": 123,
        "List": [{"SubAccountName": "", "SubAccount": ""}]
    """
    body = {}
    if args.sub_account_name:
        body["SubAccountName"] = args.sub_account_name
    return call_api("ListSubAccountForAgent", body)


def list_signature(args) -> dict:
    """查询签名列表 (ListSignatureForAgent).

    说明: 返回审核通过的签名

    Request:
        "Signature": "qm",
        "SubAccounts": ["a", "b"],
        "Page": 1,
        "PageSize": 2

    Response:
        "Total": 100,
        "List": [{"Signature": "", "Description": "", "Status": 1, ...}]
    """
    body = {
        "Page": args.page,
        "PageSize": args.page_size,
    }

    if args.signature:
        body["Signature"] = args.signature
    if args.sub_accounts:
        body["SubAccounts"] = args.sub_accounts.split(",")

    return call_api("ListSignatureForAgent", body)


def list_sms_template(args) -> dict:
    """查询模板列表 (ListSmsTemplateForAgent).

    说明: 返回审核通过的模板信息

    Request:
        "TemplateId": "qm",
        "SubAccounts": ["a", "b"],
        "Signatures": ["aqm", "bqm"],
        "Page": 1,
        "PageSize": 2

    Response:
        "Total": 100,
        "List": [{"TemplateId": "", "SecondTemplateId": "", ...}]
    """
    body = {
        "Page": args.page,
        "PageSize": args.page_size,
    }

    if args.template_id:
        body["TemplateId"] = args.template_id
    if args.sub_accounts:
        body["SubAccounts"] = args.sub_accounts.split(",")
    if args.signatures:
        body["Signatures"] = args.signatures.split(",")

    return call_api("ListSmsTemplateForAgent", body)


def list_total_send_count_stat(args) -> dict:
    """查询发送统计 (ListTotalSendCountStatForAgent).

    Request:
        "StartTime": 16934224000,
        "EndTime": 16934224000,
        "SubAccount": "",
        "ChannelType": "",
        "Signature": "",
        "TemplateId": ""

    Response:
        "TotalSendCount": 1122,
        "TotalSendSuccessCount": 120,
        "TotalAllSendCount": 123,
        "TotalReceiptSuccessCount": 123,
        "TotalReceiptFailureCount": 123,
        "TotalSendSuccessRate": 0.87,
        "TotalReceiptSuccessRate": 0.99
    """
    body = {
        "StartTime": args.start_time,
        "EndTime": args.end_time,
    }

    if args.sub_account:
        body["SubAccount"] = args.sub_account
    if args.channel_type:
        body["ChannelType"] = args.channel_type
    if args.signature:
        body["Signature"] = args.signature
    if args.template_id:
        body["TemplateId"] = args.template_id

    return call_api("ListTotalSendCountStatForAgent", body)


def main():
    parser = argparse.ArgumentParser(
        description="火山引擎短信发送 API (openclaw专用)\nVersion: 2026-01-01",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument("action", help="操作: send_sms, list_sms_send_log, list_sub_account, list_signature, list_sms_template, list_total_send_count_stat")

    # send_sms 参数
    parser.add_argument("--account", help="账号")
    parser.add_argument("--sub-account", help="子账号/消息组ID")
    parser.add_argument("--signature", help="短信签名")
    parser.add_argument("--template-id", help="短信模板ID")
    parser.add_argument("--mobiles", help="手机号(逗号分隔)")
    parser.add_argument("--template-param", help="模板参数JSON")

    # list_sms_send_log 参数
    parser.add_argument("--from-time", type=int, help="开始时间戳")
    parser.add_argument("--to-time", type=int, help="结束时间戳")
    parser.add_argument("--mobile", help="手机号")
    parser.add_argument("--message-id", help="消息ID")
    parser.add_argument("--page", type=int, default=1, help="页码")
    parser.add_argument("--page-size", type=int, default=100, help="每页数量")

    # list_sub_account 参数
    parser.add_argument("--sub-account-name", help="消息组名称(模糊匹配)")

    # list_signature 参数
    parser.add_argument("--sub-accounts", help="子账号列表(逗号分隔)")

    # list_sms_template 参数
    parser.add_argument("--signatures", help="签名列表(逗号分隔)")

    # list_total_send_count_stat 参数
    parser.add_argument("--start-time", type=int, help="开始时间戳")
    parser.add_argument("--end-time", type=int, help="结束时间戳")
    parser.add_argument("--channel-type", help="通道类型")

    args = parser.parse_args()

    action_map = {
        "send_sms": send_sms,
        "list_sms_send_log": list_sms_send_log,
        "list_sub_account": list_sub_account,
        "list_signature": list_signature,
        "list_sms_template": list_sms_template,
        "list_total_send_count_stat": list_total_send_count_stat,
    }

    if args.action not in action_map:
        print(f"Error: 未知的操作 {args.action}", file=sys.stderr)
        print(f"支持的操作为: {', '.join(action_map.keys())}", file=sys.stderr)
        sys.exit(1)

    try:
        result = action_map[args.action](args)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
    except Exception as exc:
        response = getattr(exc, "response", None)
        if response is not None:
            print(f"HTTP Error: {exc}", file=sys.stderr)
            response_text = getattr(response, "text", None)
            if response_text:
                print(response_text, file=sys.stderr)
        else:
            print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
