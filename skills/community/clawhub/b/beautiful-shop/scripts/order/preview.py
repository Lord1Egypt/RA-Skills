#!/usr/bin/env python3
"""
预览订单

接口：GET /order/carts/checked?way={way}
功能：预览订单，确认价格和运费信息
"""

import json
import sys
import os
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError


API_BASE = "https://service.filtalgo.com"
SKILL_ID = "7618877822249025562"


def preview_order(way: str) -> dict:
    """
    预览订单

    Args:
        way: BUY_NOW 或 CART

    Returns:
        dict: 订单预览信息
    """
    access_token = os.getenv(f"COZE_FILTALGO_API_{SKILL_ID}")
    if not access_token:
        return {'success': False, 'message': '未登录，请先发送验证码登录'}

    url = f"{API_BASE}/order/carts/checked?way={way}"

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
                    'message': '预览成功',
                    'data': result.get('result', {})
                }
            else:
                return {
                    'success': False,
                    'message': result.get('message', '预览失败')
                }

    except HTTPError as e:
        return {'success': False, 'message': f'HTTP错误: {e.code}'}
    except URLError as e:
        return {'success': False, 'message': f'网络错误: {e.reason}'}
    except Exception as e:
        return {'success': False, 'message': f'错误: {str(e)}'}


def main():
    if len(sys.argv) < 2:
        print(json.dumps({'success': False, 'message': '请提供 way 参数'}))
        sys.exit(1)

    way = sys.argv[1]

    if way not in ['BUY_NOW', 'CART']:
        print(json.dumps({'success': False, 'message': 'way 参数必须为 BUY_NOW 或 CART'}))
        sys.exit(1)

    result = preview_order(way)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    if not result.get('success'):
        sys.exit(1)


if __name__ == "__main__":
    main()
