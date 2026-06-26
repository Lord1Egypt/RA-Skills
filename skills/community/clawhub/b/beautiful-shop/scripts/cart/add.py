#!/usr/bin/env python3
"""
加入购物车

接口：POST /order/carts/json
功能：将商品加入购物车或立即购买
"""

import json
import sys
import os
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError


API_BASE = "https://service.filtalgo.com"
SKILL_ID = "7618877822249025562"


def add_to_cart(sku_id: str, num: int, way: str) -> dict:
    """
    加入购物车

    Args:
        sku_id: SKU ID
        num: 数量
        way: BUY_NOW=立即购买, CART=加入购物车

    Returns:
        dict: 操作结果
    """
    access_token = os.getenv(f"COZE_FILTALGO_API_{SKILL_ID}")
    if not access_token:
        return {'success': False, 'message': '未登录，请先发送验证码登录'}

    url = f"{API_BASE}/order/carts/json"

    try:
        request = Request(
            url,
            data=json.dumps({'skuId': sku_id, 'num': num, 'way': way}).encode('utf-8'),
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
                    'message': '操作成功'
                }
            else:
                return {
                    'success': False,
                    'message': result.get('message', '操作失败')
                }

    except HTTPError as e:
        return {'success': False, 'message': f'HTTP错误: {e.code}'}
    except URLError as e:
        return {'success': False, 'message': f'网络错误: {e.reason}'}
    except Exception as e:
        return {'success': False, 'message': f'错误: {str(e)}'}


def main():
    if len(sys.argv) < 4:
        print(json.dumps({'success': False, 'message': '请提供 skuId、num 和 way 参数'}))
        sys.exit(1)

    sku_id = sys.argv[1]
    num = int(sys.argv[2])
    way = sys.argv[3]

    if way not in ['BUY_NOW', 'CART']:
        print(json.dumps({'success': False, 'message': 'way 参数必须为 BUY_NOW 或 CART'}))
        sys.exit(1)

    result = add_to_cart(sku_id, num, way)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    if not result.get('success'):
        sys.exit(1)


if __name__ == "__main__":
    main()
