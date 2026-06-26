#!/usr/bin/env python3
"""
设为默认地址

接口：PUT /user/address/default/{addressId}
功能：将指定地址设为默认收货地址
"""

import json
import sys
import os
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError


API_BASE = "https://service.filtalgo.com"
SKILL_ID = "7618877822249025562"


def set_default_address(address_id: str) -> dict:
    """
    设为默认地址

    Args:
        address_id: 地址ID

    Returns:
        dict: 操作结果
    """
    access_token = os.getenv(f"COZE_FILTALGO_API_{SKILL_ID}")
    if not access_token:
        return {'success': False, 'message': '未登录，请先发送验证码登录'}

    url = f"{API_BASE}/user/address/default/{address_id}"

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
    if len(sys.argv) < 2:
        print(json.dumps({'success': False, 'message': '请提供 addressId 参数'}))
        sys.exit(1)

    address_id = sys.argv[1]
    result = set_default_address(address_id)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    if not result.get('success'):
        sys.exit(1)


if __name__ == "__main__":
    main()
