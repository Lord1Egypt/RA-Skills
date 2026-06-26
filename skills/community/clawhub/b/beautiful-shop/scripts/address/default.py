#!/usr/bin/env python3
"""
获取默认收货地址

接口：GET /user/address/default
功能：获取用户的默认收货地址
"""

import json
import sys
import os
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError


API_BASE = "https://service.filtalgo.com"
SKILL_ID = "7618877822249025562"


def get_default_address() -> dict:
    """
    获取默认地址

    Returns:
        dict: 默认地址信息
    """
    access_token = os.getenv(f"COZE_FILTALGO_API_{SKILL_ID}")
    if not access_token:
        return {'success': False, 'message': '未登录，请先发送验证码登录'}

    url = f"{API_BASE}/user/address/default"

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
    result = get_default_address()
    print(json.dumps(result, ensure_ascii=False, indent=2))

    if not result.get('success'):
        sys.exit(1)


if __name__ == "__main__":
    main()
