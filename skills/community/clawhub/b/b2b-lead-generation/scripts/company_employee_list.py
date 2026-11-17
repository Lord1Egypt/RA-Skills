#!/usr/bin/env python3
"""
跨境魔方全球企业库员工列表查询
根据公司ID获取公司的员工信息，支持游标翻页。
"""
import argparse
import sys
from common import make_request, print_json_output, cover_fee_info


def get_employee_list(pid: str, cursor: str = None) -> dict:
    """
    根据公司ID获取员工列表。

    Args:
        pid: 公司ID
        cursor: 分页游标，首次请求不传，翻页时传入上一次响应返回的cursor

    Returns:
        包含员工列表的API响应
    """
    params = {'pid': pid}
    if cursor:
        params['cursor'] = cursor
    response = make_request('/agent/search/depth_company/company/employee/list', params)
    return response


def main():
    parser = argparse.ArgumentParser(
        description='从跨境魔方开放平台获取全球企业库公司员工列表'
    )
    parser.add_argument(
        '--pid',
        required=True,
        help='公司ID（如 US_12345）'
    )
    parser.add_argument(
        '--cursor',
        default=None,
        help='分页游标，首次查询不传，翻页时传入上一次响应返回的cursor'
    )

    args = parser.parse_args()

    # 获取员工列表
    response = get_employee_list(args.pid, args.cursor)

    # 从响应中提取数据
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
