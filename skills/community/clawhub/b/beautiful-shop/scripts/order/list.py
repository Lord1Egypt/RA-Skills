#!/usr/bin/env python3
"""
查询订单列表

接口：GET /order
功能：获取用户的订单列表
"""

import json
import sys
import os
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from urllib.parse import urlencode


API_BASE = "https://service.filtalgo.com"
SKILL_ID = "7618877822249025562"


def get_order_list(
    order_status: str = "",
    page_number: int = 1,
    page_size: int = 10
) -> dict:
    """
    获取订单列表

    Args:
        order_status: 订单状态（UNPAID/UNDELIVERED/DELIVERED/COMPLETED/CANCELLED）
        page_number: 页码，默认1
        page_size: 每页数量，默认10

    Returns:
        dict: 订单列表
    """
    access_token = os.getenv(f"COZE_FILTALGO_API_{SKILL_ID}")
    if not access_token:
        return {'success': False, 'message': '未登录，请先发送验证码登录'}

    params = {'pageNumber': page_number, 'pageSize': page_size}
    if order_status:
        params['orderStatus'] = order_status

    url = f"{API_BASE}/order?{urlencode(params)}"

    try:
        request = Request(url)
        request.add_header('accessToken', access_token)
        request.add_header('Content-Type', 'application/json')

        with urlopen(request, timeout=10) as response:
            data = response.read().decode('utf-8')
            result = json.loads(data)

            if result.get('success'):
                return {
                    'success': True,
                    'message': '获取成功',
                    'data': result.get('result', {})
                }
            else:
                return {
                    'success': False,
                    'message': result.get('message', '获取失败')
                }

    except HTTPError as e:
        return {'success': False, 'message': f'HTTP错误: {e.code}'}
    except URLError as e:
        return {'success': False, 'message': f'网络错误: {e.reason}'}
    except Exception as e:
        return {'success': False, 'message': f'错误: {str(e)}'}


def main():
    order_status = ""
    page_number = 1
    page_size = 10

    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == '--status' and i + 1 < len(sys.argv):
            order_status = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == '--page' and i + 1 < len(sys.argv):
            page_number = int(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == '--size' and i + 1 < len(sys.argv):
            page_size = int(sys.argv[i + 1])
            i += 2
        else:
            i += 1

    result = get_order_list(order_status, page_number, page_size)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    if not result.get('success'):
        sys.exit(1)


if __name__ == "__main__":
    main()
