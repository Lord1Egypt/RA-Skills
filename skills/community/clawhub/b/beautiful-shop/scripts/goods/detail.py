#!/usr/bin/env python3
"""
获取商品详情

接口：GET /goods/sku/vo/{goodsId}/{skuId}
功能：获取商品详细信息，包含规格和SKU列表
"""

import json
import sys
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError


API_BASE = "https://service.filtalgo.com"


def get_goods_detail(goods_id: str, sku_id: str) -> dict:
    """
    获取商品详情

    Args:
        goods_id: 商品ID（搜索结果的 goodsId 字段）
        sku_id: SKU ID（搜索结果的 id 字段）

    Returns:
        dict: 商品详细信息
    """
    url = f"{API_BASE}/goods/sku/vo/{goods_id}/{sku_id}"

    try:
        request = Request(url)
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
    if len(sys.argv) < 3:
        print(json.dumps({'success': False, 'message': '请提供 goodsId 和 skuId 参数'}))
        sys.exit(1)

    goods_id = sys.argv[1]
    sku_id = sys.argv[2]
    result = get_goods_detail(goods_id, sku_id)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    if not result.get('success'):
        sys.exit(1)


if __name__ == "__main__":
    main()
