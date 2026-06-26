#!/usr/bin/env python3
"""
短信登录

接口：POST /auth/agent/smsLogin
功能：使用手机号和验证码登录，获取 accessToken 和 refreshToken
"""

import json
import sys
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError


API_BASE = "https://service.filtalgo.com"


def sms_login(mobile: str, code: str) -> dict:
    """
    短信登录

    Args:
        mobile: 手机号
        code: 验证码（测试环境固定 111111）

    Returns:
        dict: {"success": bool, "message": str, "accessToken": str, "refreshToken": str}
    """
    url = f"{API_BASE}/auth/agent/smsLogin"

    try:
        request = Request(
            url,
            data=json.dumps({'mobile': mobile, 'code': code}).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )

        with urlopen(request, timeout=10) as response:
            data = response.read().decode('utf-8')
            result = json.loads(data)

            if result.get('success'):
                tokens = result.get('result', {})
                return {
                    'success': True,
                    'message': '登录成功',
                    'accessToken': tokens.get('accessToken'),
                    'refreshToken': tokens.get('refreshToken')
                }
            else:
                return {
                    'success': False,
                    'message': result.get('message', '登录失败')
                }

    except HTTPError as e:
        return {'success': False, 'message': f'HTTP错误: {e.code}'}
    except URLError as e:
        return {'success': False, 'message': f'网络错误: {e.reason}'}
    except Exception as e:
        return {'success': False, 'message': f'错误: {str(e)}'}


def main():
    if len(sys.argv) < 3:
        print(json.dumps({'success': False, 'message': '请提供手机号和验证码参数'}))
        sys.exit(1)

    mobile = sys.argv[1]
    code = sys.argv[2]
    result = sms_login(mobile, code)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    if not result.get('success'):
        sys.exit(1)


if __name__ == "__main__":
    main()
