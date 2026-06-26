#!/usr/bin/env python3
"""1688招商活动报名 CLI入口"""

COMMAND_NAME = "1688_enroll_submit_item"
COMMAND_DESC = "提交招商活动报名（报品同时报商）"

import importlib
import json
import os
import sys
import argparse

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _auth import get_ak_raw
from _output import make_output, print_output, print_error
_service = importlib.import_module("capabilities.1688_enroll_submit_item.service")
submit_enroll_item = _service.submit_enroll_item


def main():
    if not get_ak_raw():
        print_output(make_output(
            success=False,
            markdown="❌ AK 未配置，无法提交报名。\n\n运行: `cli.py configure YOUR_AK`",
            data={"data": {}},
        ))
        return

    parser = argparse.ArgumentParser(description="1688招商活动报名")
    parser.add_argument("--activityId", "-a", type=int, required=True, help="活动Id")
    parser.add_argument("--itemId", "-i", type=int, required=True, help="商品Id")
    parser.add_argument("--fillFormDataList", "-f", type=str, required=True,
                        help='价格等表单填充数据列表，JSON格式')
    args = parser.parse_args()

    try:
        fill_form_data_list = json.loads(args.fillFormDataList)
    except json.JSONDecodeError:
        print_output(make_output(success=False, markdown="❌ fillFormDataList 参数格式错误，请传入合法的 JSON 数组", data={"data": {}}))
        return

    if not isinstance(fill_form_data_list, list):
        print_output(make_output(success=False, markdown="❌ fillFormDataList 必须是 JSON 数组", data={"data": {}}))
        return

    try:
        result = submit_enroll_item(args.activityId, args.itemId, fill_form_data_list)
        is_success = result.get("success", False)
        record_id = result.get("recordId", "")
        message = result.get("message", "")

        if is_success:
            markdown = f"✅ 报名成功！记录ID: {record_id}"
        else:
            markdown = f"❌ 报名失败：{message}"

        print_output(make_output(success=is_success, markdown=markdown, data=result))
    except Exception as exc:
        print_error(exc, {"data": {}})


if __name__ == "__main__":
    main()
