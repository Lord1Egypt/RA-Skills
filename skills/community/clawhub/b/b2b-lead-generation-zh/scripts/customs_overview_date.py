#!/usr/bin/env python3
"""
跨境魔方国家贸易概览-日期相关查询
返回去年年份、上月月份、去年当月月份等日期参考信息（无业务请求参数）。
"""
import argparse
import sys
from common import make_request, print_json_output, cover_fee_info, parse_params


def get_overview_date(params: dict) -> dict:
    """
    获取日期参考信息。

    Args:
        params: 查询参数（无业务字段，可传空对象）

    Returns:
        包含日期参考信息的API响应
    """
    response = make_request('/agent/customs/overview/date', params)
    return response


def main():
    parser = argparse.ArgumentParser(
        description='从跨境魔方开放平台获取国家贸易概览日期参考信息'
    )
    parser.add_argument(
        '--params',
        required=True,
        help='JSON格式的查询参数，可传空对象：\'{}\''
    )

    args = parser.parse_args()

    params = parse_params(args.params)

    response = get_overview_date(params)

    if response.get('code') in (0, 200):
        data = response.get('data', {})
        print_json_output({
            "data": data,
            "fee": cover_fee_info(response.get('fee', {})),
            "requestId": response.get('requestId')
        })
    else:
        print(f"错误：{response.get('msg', '未知错误')}", file=sys.stderr)
        if response.get('requestId'):
            print(f"requestId：{response.get('requestId')}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
