#!/usr/bin/env python3
"""
跨境魔方海关公司贸易伙伴趋势查询
根据公司ID和公司类型获取公司的贸易伙伴趋势数据（金额、数量、重量、月度趋势、HS编码分布、产品分布等）。
"""
import argparse
import sys
from common import make_request, print_json_output, cover_fee_info, parse_params


def get_company_partner_stats(params: dict) -> dict:
    """
    根据查询参数获取公司贸易伙伴趋势。

    Args:
        params: 查询参数（包含companyId、companyType等）

    Returns:
        包含贸易伙伴趋势数据的API响应
    """
    response = make_request('/agent/customs/company/partner/stats', params)
    return response


def main():
    parser = argparse.ArgumentParser(
        description='从跨境魔方开放平台获取公司贸易伙伴趋势'
    )
    parser.add_argument(
        '--params',
        required=True,
        help='JSON格式的查询参数，如 \'{"companyId":"100001","companyType":1,"dateStart":1700000000000,"dateEnd":1735689599999}\''
    )

    args = parser.parse_args()

    params = parse_params(args.params)

    # 验证必要参数
    if 'companyId' not in params:
        print("错误：params中缺少companyId", file=sys.stderr)
        sys.exit(1)
    if 'companyType' not in params:
        print("错误：params中缺少companyType", file=sys.stderr)
        sys.exit(1)

    response = get_company_partner_stats(params)

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
