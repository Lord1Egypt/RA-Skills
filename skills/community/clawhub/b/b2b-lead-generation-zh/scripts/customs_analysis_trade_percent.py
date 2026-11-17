#!/usr/bin/env python3
"""
跨境魔方分析报告-贸易占比查询
查询指定HS编码下各公司的贸易占比数据。
"""
import argparse
import sys
from common import make_request, print_json_output, cover_fee_info, parse_params


def get_analysis_trade_percent(params: dict) -> dict:
    """
    根据查询参数获取贸易占比数据。

    Args:
        params: 查询参数（包含hscode, countryType, recentMonths等）

    Returns:
        包含贸易占比数据的API响应
    """
    response = make_request('/agent/customs/analysis/trade-percent', params)
    return response


def main():
    parser = argparse.ArgumentParser(
        description='从跨境魔方开放平台获取分析报告-贸易占比'
    )
    parser.add_argument(
        '--params',
        required=True,
        help='JSON格式的查询参数，如 \'{"hscode":"04021000","countryType":1,"recentMonths":12}\''
    )

    args = parser.parse_args()

    params = parse_params(args.params)

    # 验证必要参数
    if 'hscode' not in params:
        print("错误：params中缺少hscode", file=sys.stderr)
        sys.exit(1)
    if 'countryType' not in params:
        print("错误：params中缺少countryType", file=sys.stderr)
        sys.exit(1)
    if 'recentMonths' not in params:
        print("错误：params中缺少recentMonths", file=sys.stderr)
        sys.exit(1)

    response = get_analysis_trade_percent(params)

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
