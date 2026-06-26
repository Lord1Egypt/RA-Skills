#!/usr/bin/env python3
"""
设置收货地址

接口：PUT /order/carts/shippingAddress
功能：设置订单的收货地址
"""

import json
import sys
import os
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from urllib.parse import urlencode


API_BASE = "https://service.filtalgo.com"
SKILL_ID = "7618877822249025562"


def set_shipping_address(address_id: str, way: str) -> dict:
    """
    设置收货地址

    Args:
        address_id: 收货地址ID
        way: BUY_NOW 或 CART

    Returns:
        dict: 操作结果
    """
    access_token = os.getenv(f"COZE_FILTALGO_API_{SKILL_ID}")
    if not access_token:
        return {'success': False, 'message': '未登录，请先发送验证码登录'}

    params = urlencode({'way': way, 'shippingAddressId': address_id})
    url = f"{API_BASE}/order/carts/shippingAddress?{params}"

    try:
        request = Request(url, method='PUT')
        request.add_header('accessToken', access_token)
        request.add_header('Content-Type', 'application/json')

        with urlopen(request, timeout=10) as response:
            data = response.read().decode('utf-8')
            result = json.loads(data)

            if result.get('success'):
                return {
                    'success': True,
                    'message': '设置成功'
                }
            else:
                return {
                    'success': False,
                    'message': result.get('message', '设置失败')
                }

    except HTTPError as e:
        return {'success': False, 'message': f'HTTP错误: {e.code}'}
    except URLError as e:
        return {'success': False, 'message': f'网络错误: {e.reason}'}
    except Exception as e:
        return {'success': False, 'message': f'错误: {str(e)}'}


def main():
    if len(sys.argv) < 3:
        print(json.dumps({'success': False, 'message': '请提供 addressId 和 way 参数'}))
        sys.exit(1)

    address_id = sys.argv[1]
    way = sys.argv[2]

    if way not in ['BUY_NOW', 'CART']:
        print(json.dumps({'success': False, 'message': 'way 参数必须为 BUY_NOW 或 CART'}))
        sys.exit(1)

    result = set_shipping_address(address_id, way)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    if not result.get('success'):
        sys.exit(1)


if __name__ == "__main__":
    main()
