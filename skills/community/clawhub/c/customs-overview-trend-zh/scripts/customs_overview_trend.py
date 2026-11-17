#!/usr/bin/env python3
"""
跨境魔方国家贸易概览-进出口趋势查询
按月份维度返回指定时间范围内的进出口贸易总量趋势数据，支持游标分页。
"""
import argparse
import sys
from common import make_request, print_json_output, cover_fee_info, parse_params


def get_overview_trend(params: dict) -> dict:
    """
    根据查询参数获取进出口趋势数据。

    Args:
        params: 查询参数（包含startDate、endDate等）

    Returns:
        包含趋势数据的API响应
    """
    response = make_request('/agent/customs/overview/trend', params)
    return response


def main():
    parser = argparse.ArgumentParser(
        description='从跨境魔方开放平台获取国家贸易概览进出口趋势'
    )
    parser.add_argument(
        '--params',
        required=True,
        help='JSON格式的查询参数，如 \'{"originCountryCode":"CN","arrivalCountryCode":"US","startDate":202501,"endDate":202512}\''
    )

    args = parser.parse_args()

    params = parse_params(args.params)

    # 验证必要参数
    if 'startDate' not in params:
        print("错误：params中缺少startDate", file=sys.stderr)
        sys.exit(1)
    if 'endDate' not in params:
        print("错误：params中缺少endDate", file=sys.stderr)
        sys.exit(1)

    response = get_overview_trend(params)

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
