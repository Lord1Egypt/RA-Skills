#!/usr/bin/env python3
"""
跨境魔方分析报告-HS编码搜索
根据产品名称和HS编码关键字搜索匹配的HS编码列表。
"""
import argparse
import sys
from common import make_request, print_json_output, cover_fee_info, parse_params


def search_hscode(params: dict) -> dict:
    """
    根据查询参数搜索HS编码。

    Args:
        params: 查询参数（包含product, hscode等）

    Returns:
        包含HS编码搜索结果的API响应
    """
    response = make_request('/agent/customs/analysis/hscode/search', params)
    return response


def main():
    parser = argparse.ArgumentParser(
        description='从跨境魔方开放平台搜索HS编码'
    )
    parser.add_argument(
        '--params',
        required=True,
        help='JSON格式的查询参数，如 \'{"product":"milk powder","hscode":"0402"}\''
    )

    args = parser.parse_args()

    params = parse_params(args.params)

    # 验证必要参数
    if 'product' not in params:
        print("错误：params中缺少product", file=sys.stderr)
        sys.exit(1)
    if 'hscode' not in params:
        print("错误：params中缺少hscode", file=sys.stderr)
        sys.exit(1)

    response = search_hscode(params)

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
