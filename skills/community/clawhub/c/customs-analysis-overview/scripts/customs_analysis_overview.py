#!/usr/bin/env python3
"""
跨境魔方分析报告-概览查询
按国家维度统计概览数据，返回各国供应商/采购商数量等信息。
"""
import argparse
import sys
from common import make_request, print_json_output, cover_fee_info, parse_params


def get_analysis_overview(params: dict) -> dict:
    """
    根据查询参数获取分析报告概览数据。

    Args:
        params: 查询参数

    Returns:
        包含概览数据的API响应
    """
    response = make_request('/agent/customs/analysis/overview', params)
    return response


def main():
    parser = argparse.ArgumentParser(
        description='从跨境魔方开放平台获取分析报告-概览'
    )
    parser.add_argument(
        '--params',
        required=True,
        help='JSON格式的查询参数，如 \'{"cursor":"eyJpZCI6MX0="}\''
    )

    args = parser.parse_args()

    params = parse_params(args.params)

    response = get_analysis_overview(params)

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
