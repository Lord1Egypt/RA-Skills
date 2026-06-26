#!/usr/bin/env python3
"""
发送短信验证码

接口：GET /auth/agent/sms/send
功能：向指定手机号发送登录验证码
"""

import json
import sys
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError


API_BASE = "https://service.filtalgo.com"


def send_sms_code(mobile: str) -> dict:
    """
    发送短信验证码

    Args:
        mobile: 手机号

    Returns:
        dict: {"success": bool, "message": str}
    """
    url = f"{API_BASE}/auth/agent/sms/send?mobile={mobile}&scene=LOGIN"

    try:
        request = Request(url)
        request.add_header('Content-Type', 'application/json')

        with urlopen(request, timeout=10) as response:
            data = response.read().decode('utf-8')
            result = json.loads(data)

            if result.get('success'):
                return {
                    'success': True,
                    'message': '验证码发送成功'
                }
            else:
                return {
                    'success': False,
                    'message': result.get('message', '发送失败')
                }

    except HTTPError as e:
        return {'success': False, 'message': f'HTTP错误: {e.code}'}
    except URLError as e:
        return {'success': False, 'message': f'网络错误: {e.reason}'}
    except Exception as e:
        return {'success': False, 'message': f'错误: {str(e)}'}


def main():
    if len(sys.argv) < 2:
        print(json.dumps({'success': False, 'message': '请提供手机号参数'}))
        sys.exit(1)

    mobile = sys.argv[1]
    result = send_sms_code(mobile)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    if not result.get('success'):
        sys.exit(1)


if __name__ == "__main__":
    main()
