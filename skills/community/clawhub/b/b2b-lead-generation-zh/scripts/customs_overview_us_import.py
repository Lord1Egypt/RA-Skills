#!/usr/bin/env python3
"""
跨境魔方国家贸易概览-美国进口交易查询
按州或城市维度返回美国进口交易统计，包含进口记录数、集装箱数及近90天数据，支持游标分页。
"""
import argparse
import sys
from common import make_request, print_json_output, cover_fee_info, parse_params


def get_overview_us_import(params: dict) -> dict:
    """
    根据查询参数获取美国进口交易统计数据。

    Args:
        params: 查询参数（包含type等）

    Returns:
        包含美国进口交易统计数据的API响应
    """
    response = make_request('/agent/customs/overview/us-import', params)
    return response


def main():
    parser = argparse.ArgumentParser(
        description='从跨境魔方开放平台获取国家贸易概览美国进口交易'
    )
    parser.add_argument(
        '--params',
        required=True,
        help='JSON格式的查询参数，如 \'{"type":"state"}\' 或 \'{"type":"city"}\''
    )

    args = parser.parse_args()

    params = parse_params(args.params)

    # 验证必要参数
    if 'type' not in params:
        print("错误：params中缺少type", file=sys.stderr)
        sys.exit(1)

    response = get_overview_us_import(params)

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
