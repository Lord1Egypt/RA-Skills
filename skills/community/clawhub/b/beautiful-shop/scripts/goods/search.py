#!/usr/bin/env python3
"""
搜索商品

接口：GET /goods/elasticsearch/es
功能：全文搜索商品，支持关键词、分类、价格区间、分页、排序
"""

import json
import sys
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from urllib.parse import urlencode


API_BASE = "https://service.filtalgo.com"


def search_goods(
    keyword: str = "",
    category_id: str = "",
    brand_id: str = "",
    price_min: float = None,
    price_max: float = None,
    page_number: int = 1,
    page_size: int = 10,
    sort: str = ""
) -> dict:
    """
    搜索商品

    Args:
        keyword: 搜索关键词
        category_id: 分类ID
        brand_id: 品牌ID
        price_min: 最低价格
        price_max: 最高价格
        page_number: 页码，默认1
        page_size: 每页数量，默认10
        sort: 排序（PRICE_ASC/PRICE_DESC/SALE_DESC）

    Returns:
        dict: 包含商品列表和分页信息
    """
    params = {'pageNumber': page_number, 'pageSize': page_size}

    if keyword:
        params['keyword'] = keyword
    if category_id:
        params['categoryId'] = category_id
    if brand_id:
        params['brandId'] = brand_id
    if price_min is not None:
        params['priceMin'] = price_min
    if price_max is not None:
        params['priceMax'] = price_max
    if sort:
        params['sort'] = sort

    url = f"{API_BASE}/goods/elasticsearch/es?{urlencode(params)}"

    try:
        request = Request(url)
        request.add_header('Content-Type', 'application/json')

        with urlopen(request, timeout=10) as response:
            data = response.read().decode('utf-8')
            result = json.loads(data)

            if result.get('success'):
                return {
                    'success': True,
                    'message': '搜索成功',
                    'data': result.get('result', {})
                }
            else:
                return {
                    'success': False,
                    'message': result.get('message', '搜索失败')
                }

    except HTTPError as e:
        return {'success': False, 'message': f'HTTP错误: {e.code}'}
    except URLError as e:
        return {'success': False, 'message': f'网络错误: {e.reason}'}
    except Exception as e:
        return {'success': False, 'message': f'错误: {str(e)}'}


def main():
    keyword = ""
    page_number = 1
    page_size = 10
    sort = ""

    # 解析命令行参数
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == '--keyword' and i + 1 < len(sys.argv):
            keyword = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == '--page' and i + 1 < len(sys.argv):
            page_number = int(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == '--size' and i + 1 < len(sys.argv):
            page_size = int(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == '--sort' and i + 1 < len(sys.argv):
            sort = sys.argv[i + 1]
            i += 2
        else:
            i += 1

    result = search_goods(
        keyword=keyword,
        page_number=page_number,
        page_size=page_size,
        sort=sort
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))

    if not result.get('success'):
        sys.exit(1)


if __name__ == "__main__":
    main()
