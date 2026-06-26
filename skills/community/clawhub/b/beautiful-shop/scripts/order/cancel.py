#!/usr/bin/env python3
"""
取消订单

接口：POST /order/{orderSn}/cancel
功能：取消未支付的订单
"""

import json
import sys
import os
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from urllib.parse import urlencode


API_BASE = "https://service.filtalgo.com"
SKILL_ID = "7618877822249025562"


def cancel_order(order_sn: str, reason: str) -> dict:
    """
    取消订单

    Args:
        order_sn: 订单号（O开头）
        reason: 取消原因

    Returns:
        dict: 操作结果
    """
    access_token = os.getenv(f"COZE_FILTALGO_API_{SKILL_ID}")
    if not access_token:
        return {'success': False, 'message': '未登录，请先发送验证码登录'}

    params = urlencode({'reason': reason})
    url = f"{API_BASE}/order/{order_sn}/cancel?{params}"

    try:
        request = Request(url, method='POST')
        request.add_header('accessToken', access_token)
        request.add_header('Content-Type', 'application/json')

        with urlopen(request, timeout=10) as response:
            data = response.read().decode('utf-8')
            result = json.loads(data)

            if result.get('success'):
                return {
                    'success': True,
                    'message': '订单已取消'
                }
            else:
                return {
                    'success': False,
                    'message': result.get('message', '取消失败')
                }

    except HTTPError as e:
        return {'success': False, 'message': f'HTTP错误: {e.code}'}
    except URLError as e:
        return {'success': False, 'message': f'网络错误: {e.reason}'}
    except Exception as e:
        return {'success': False, 'message': f'错误: {str(e)}'}


def main():
    if len(sys.argv) < 3:
        print(json.dumps({'success': False, 'message': '请提供 orderSn 和 reason 参数'}))
        sys.exit(1)

    order_sn = sys.argv[1]
    reason = sys.argv[2]
    result = cancel_order(order_sn, reason)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    if not result.get('success'):
        sys.exit(1)


if __name__ == "__main__":
    main()
