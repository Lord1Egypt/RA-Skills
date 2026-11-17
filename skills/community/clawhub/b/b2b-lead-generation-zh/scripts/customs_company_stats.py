#!/usr/bin/env python3
"""
跨境魔方海关公司贸易基础统计查询
根据公司ID和公司类型获取公司的贸易基础统计数据（交易次数、总重量、总数量、总金额等）。
"""
import argparse
import sys
from common import make_request, print_json_output, cover_fee_info


def get_company_stats(company_id: str, company_type: int) -> dict:
    """
    根据公司ID和公司类型获取公司贸易基础统计。

    Args:
        company_id: 公司ID
        company_type: 公司类型（1：供应商，2：采购商）

    Returns:
        包含贸易基础统计的API响应
    """
    params = {
        'companyId': company_id,
        'companyType': company_type
    }
    response = make_request('/agent/customs/company/stats', params)
    return response


def main():
    parser = argparse.ArgumentParser(
        description='从跨境魔方开放平台获取公司贸易基础统计'
    )
    parser.add_argument(
        '--companyId',
        required=True,
        help='公司ID（如 100001）'
    )
    parser.add_argument(
        '--companyType',
        required=True,
        type=int,
        help='公司类型（1：供应商，2：采购商）'
    )

    args = parser.parse_args()

    response = get_company_stats(args.companyId, args.companyType)

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
