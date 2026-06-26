#!/usr/bin/env python3
"""
新增收货地址

接口：POST /user/address
功能：添加新的收货地址
"""

import json
import sys
import os
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError


API_BASE = "https://service.filtalgo.com"
SKILL_ID = "7618877822249025562"


def add_address(
    name: str,
    mobile: str,
    address_id_path: str,
    address_path: str,
    detail: str,
    is_default: bool = False
) -> dict:
    """
    新增收货地址

    Args:
        name: 收货人姓名
        mobile: 收货人手机号
        address_id_path: 地区ID路径（从 resolve_address 获取）
        address_path: 地区名称路径（从 resolve_address 获取）
        detail: 详细地址
        is_default: 是否设为默认地址

    Returns:
        dict: 操作结果
    """
    access_token = os.getenv(f"COZE_FILTALGO_API_{SKILL_ID}")
    if not access_token:
        return {'success': False, 'message': '未登录，请先发送验证码登录'}

    url = f"{API_BASE}/user/address"

    body = {
        'name': name,
        'mobile': mobile,
        'consigneeAddressIdPath': address_id_path,
        'consigneeAddressPath': address_path,
        'detail': detail,
        'isDefault': is_default,
        'type': 'RECEIVE'
    }

    try:
        request = Request(
            url,
            data=json.dumps(body).encode('utf-8'),
            headers={
                'Content-Type': 'application/json',
                'accessToken': access_token
            }
        )

        with urlopen(request, timeout=10) as response:
            data = response.read().decode('utf-8')
            result = json.loads(data)

            if result.get('success'):
                return {
                    'success': True,
                    'message': '添加成功',
                    'data': result.get('result', {})
                }
            else:
                return {
                    'success': False,
                    'message': result.get('message', '添加失败')
                }

    except HTTPError as e:
        return {'success': False, 'message': f'HTTP错误: {e.code}'}
    except URLError as e:
        return {'success': False, 'message': f'网络错误: {e.reason}'}
    except Exception as e:
        return {'success': False, 'message': f'错误: {str(e)}'}


def main():
    if len(sys.argv) < 6:
        print(json.dumps({'success': False, 'message': '请提供 name、mobile、addressIdPath、addressPath、detail 参数'}))
        sys.exit(1)

    name = sys.argv[1]
    mobile = sys.argv[2]
    address_id_path = sys.argv[3]
    address_path = sys.argv[4]
    detail = sys.argv[5]
    is_default = sys.argv[6].lower() == 'true' if len(sys.argv) > 6 else False

    result = add_address(name, mobile, address_id_path, address_path, detail, is_default)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    if not result.get('success'):
        sys.exit(1)


if __name__ == "__main__":
    main()
