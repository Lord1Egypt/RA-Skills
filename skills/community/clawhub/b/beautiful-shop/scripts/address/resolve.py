#!/usr/bin/env python3
"""
解析地址名称

接口：GET /system/region/resolve
功能：将省市区街道名称解析为 ID 路径
"""

import json
import sys
import os
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from urllib.parse import urlencode


API_BASE = "https://service.filtalgo.com"
SKILL_ID = "7618877822249025562"


def resolve_address(province: str, city: str, district: str, street: str = "") -> dict:
    """
    解析地址名称

    Args:
        province: 省名，如"北京市"
        city: 市名，如"北京市"
        district: 区名，如"朝阳区"
        street: 街道名（可选）

    Returns:
        dict: 地址ID路径
    """
    access_token = os.getenv(f"COZE_FILTALGO_API_{SKILL_ID}")
    if not access_token:
        return {'success': False, 'message': '未登录，请先发送验证码登录'}

    params = {
        'province': province,
        'city': city,
        'district': district
    }
    if street:
        params['street'] = street

    url = f"{API_BASE}/system/region/resolve?{urlencode(params)}"

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
                    'message': '解析成功',
                    'data': result.get('result', {})
                }
            else:
                return {
                    'success': False,
                    'message': result.get('message', '解析失败')
                }

    except HTTPError as e:
        return {'success': False, 'message': f'HTTP错误: {e.code}'}
    except URLError as e:
        return {'success': False, 'message': f'网络错误: {e.reason}'}
    except Exception as e:
        return {'success': False, 'message': f'错误: {str(e)}'}


def main():
    if len(sys.argv) < 4:
        print(json.dumps({'success': False, 'message': '请提供 province、city、district 参数'}))
        sys.exit(1)

    province = sys.argv[1]
    city = sys.argv[2]
    district = sys.argv[3]
    street = sys.argv[4] if len(sys.argv) > 4 else ""

    result = resolve_address(province, city, district, street)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    if not result.get('success'):
        sys.exit(1)


if __name__ == "__main__":
    main()
