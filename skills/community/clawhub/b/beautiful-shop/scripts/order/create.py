#!/usr/bin/env python3
"""
创建订单

接口：POST /order/carts/create/trade
功能：创建订单，返回交易单号用于支付
"""

import json
import sys
import os
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError


API_BASE = "https://service.filtalgo.com"
SKILL_ID = "7618877822249025562"


def create_order(way: str) -> dict:
    """
    创建订单

    Args:
        way: BUY_NOW 或 CART

    Returns:
        dict: 订单创建结果，包含 trade_sn
    """
    access_token = os.getenv(f"COZE_FILTALGO_API_{SKILL_ID}")
    if not access_token:
        return {'success': False, 'message': '未登录，请先发送验证码登录'}

    url = f"{API_BASE}/order/carts/create/trade"

    try:
        request = Request(
            url,
            data=json.dumps({'way': way, 'client': 'AGENT'}).encode('utf-8'),
            headers={
                'Content-Type': 'application/json',
                'accessToken': access_token
            }
        )

        with urlopen(request, timeout=10) as response:
            data = response.read().decode('utf-8')
            result = json.loads(data)

            if result.get('success'):
                order_info = result.get('result', {})
                return {
                    'success': True,
                    'message': '订单创建成功',
                    'data': {
                        'trade_sn': order_info.get('sn'),
                        'flow_price': order_info.get('flowPrice'),
                        'order_status': order_info.get('orderStatus'),
                        'consignee_name': order_info.get('consigneeName'),
                        'consignee_address': order_info.get('consigneeAddressPath')
                    }
                }
            else:
                return {
                    'success': False,
                    'message': result.get('message', '创建失败')
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

    result = create_order(way)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    if not result.get('success'):
        sys.exit(1)


if __name__ == "__main__":
    main()
