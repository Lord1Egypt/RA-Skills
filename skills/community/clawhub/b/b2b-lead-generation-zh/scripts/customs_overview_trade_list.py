#!/usr/bin/env python3
"""
跨境魔方国家贸易概览-国家贸易列表查询
按国家维度返回贸易列表，支持游标分页。
"""
import argparse
import sys
from common import make_request, print_json_output, cover_fee_info, parse_params


def get_overview_trade_list(params: dict) -> dict:
    """
    根据查询参数获取国家贸易列表。

    Args:
        params: 查询参数（包含originCountryCode、arrivalCountryCode、year等）

    Returns:
        包含国家贸易列表数据的API响应
    """
    response = make_request('/agent/customs/overview/trade-list', params)
    return response


def main():
    parser = argparse.ArgumentParser(
        description='从跨境魔方开放平台获取国家贸易概览国家贸易列表'
    )
    parser.add_argument(
        '--params',
        required=True,
        help='JSON格式的查询参数，如 \'{"originCountryCode":"CN","arrivalCountryCode":"US","year":2025}\''
    )

    args = parser.parse_args()

    params = parse_params(args.params)

    # 验证必要参数
    if 'year' not in params:
        print("错误：params中缺少year", file=sys.stderr)
        sys.exit(1)

    response = get_overview_trade_list(params)

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
