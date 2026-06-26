#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
商品搜索API调用脚本
通过AlphaShop HTTP API调用1688遨虾AI选品系统的商品搜索服务
"""

import argparse
import json
import requests
import sys
import time
import os
import jwt

# AlphaShop API 配置
API_ENDPOINT = "https://api.alphashop.cn/ai.sel.global1688.productSearchApi/1.0"

# API 认证配置（需要从环境变量或配置文件获取）
APP_KEY = None  # 需要配置
APP_SECRET = None  # 需要配置

# 平台和区域映射
PLATFORM_REGIONS = {
    "amazon": ["US", "UK", "JP", "DE", "FR", "IT", "ES", "CA"],
    "tiktok": ["ES", "PH", "FR", "ID", "MX", "VN", "DE", "JP", "TH", "SG", "BR", "IT", "US", "GB", "MY"]
}

# 上架时间选项
LISTING_TIME_OPTIONS = [90, 180, 365]


def validate_params(args):
    """参数校验"""
    # 验证平台
    if args.platform not in PLATFORM_REGIONS:
        print(f"错误：不支持的平台 '{args.platform}'，支持的平台：{list(PLATFORM_REGIONS.keys())}")
        return False

    # 验证区域
    if args.region not in PLATFORM_REGIONS[args.platform]:
        print(f"错误：平台 '{args.platform}' 不支持区域 '{args.region}'")
        print(f"支持的区域：{PLATFORM_REGIONS[args.platform]}")
        return False

    # 验证价格区间
    if args.min_price and args.max_price and args.min_price > args.max_price:
        print(f"错误：最低价格({args.min_price})不能大于最高价格({args.max_price})")
        return False

    # 验证销量区间
    if args.min_sales and args.max_sales and args.min_sales > args.max_sales:
        print(f"错误：最低销量({args.min_sales})不能大于最高销量({args.max_sales})")
        return False

    # 验证评分区间
    if args.min_rating and (args.min_rating < 0 or args.min_rating > 5.0):
        print(f"错误：最低评分必须在0-5.0之间")
        return False

    if args.max_rating and (args.max_rating < 0 or args.max_rating > 5.0):
        print(f"错误：最高评分必须在0-5.0之间")
        return False

    if args.min_rating and args.max_rating and args.min_rating > args.max_rating:
        print(f"错误：最低评分({args.min_rating})不能大于最高评分({args.max_rating})")
        return False

    # 验证上架时间
    if args.listing_time and args.listing_time not in LISTING_TIME_OPTIONS:
        print(f"错误：上架时间必须是 {LISTING_TIME_OPTIONS} 之一")
        return False

    return True


def build_request(args):
    """构建请求参数"""
    request_data = {
        "keyword": args.keyword,
        "platform": args.platform,
        "region": args.region,
    }

    # 添加可选的筛选条件
    if args.min_price is not None:
        request_data["minPrice"] = args.min_price

    if args.max_price is not None:
        request_data["maxPrice"] = args.max_price

    if args.min_sales is not None:
        request_data["minSales"] = args.min_sales

    if args.max_sales is not None:
        request_data["maxSales"] = args.max_sales

    if args.min_rating is not None:
        request_data["minRating"] = args.min_rating

    if args.max_rating is not None:
        request_data["maxRating"] = args.max_rating

    if args.listing_time is not None:
        request_data["listingTime"] = str(args.listing_time)

    if args.count is not None:
        request_data["count"] = args.count

    return request_data


def get_jwt_token(access_key, secret_key):
    """生成 JWT token 用于 AlphaShop API 认证"""
    try:
        current_time = int(time.time())
        expired_at = current_time + 1800  # 30分钟后过期
        not_before = current_time - 5

        token = jwt.encode(
            payload={
                "iss": access_key,
                "exp": expired_at,
                "nbf": not_before
            },
            key=secret_key,
            algorithm="HS256",
            headers={"alg": "HS256"}
        )

        if isinstance(token, bytes):
            token = token.decode("utf-8")
        return token
    except Exception as e:
        raise ValueError(f"生成 JWT token 失败: {e}")


def call_api(request_data, user_id, access_key=None, secret_key=None):
    """调用 AlphaShop HTTP API"""
    endpoint = API_ENDPOINT

    # 添加用户ID到请求数据
    request_data["userId"] = user_id

    try:
        print(f"\n正在调用 AlphaShop API...")
        print(f"端点: {endpoint}")
        print(f"请求参数: {json.dumps(request_data, ensure_ascii=False, indent=2)}\n")

        # 构建请求头
        headers = {
            "Content-Type": "application/json"
        }

        # 如果提供了 access_key 和 secret_key，添加 JWT token 认证
        if access_key and secret_key:
            token = get_jwt_token(access_key, secret_key)
            headers["Authorization"] = f"Bearer {token}"

            print(f"认证方式: JWT Token")

        response = requests.post(
            endpoint,
            json=request_data,
            headers=headers,
            timeout=30
        )

        if response.status_code != 200:
            print(f"HTTP错误：{response.status_code}")
            print(f"响应内容：{response.text}")
            return None

        result = response.json()
        return result

    except requests.exceptions.Timeout:
        print("错误：请求超时（>30秒）")
        return None
    except requests.exceptions.RequestException as e:
        print(f"错误：网络请求失败 - {str(e)}")
        return None
    except json.JSONDecodeError:
        print(f"错误：响应不是有效的JSON - {response.text}")
        return None


def format_product(product, index):
    """格式化单个商品信息"""
    lines = []
    lines.append(f"\n{'='*80}")
    lines.append(f"商品 {index}")
    lines.append(f"{'='*80}")

    # 基本信息
    lines.append(f"ID: {product.get('productId', 'N/A')}")
    lines.append(f"标题: {product.get('title', 'N/A')}")

    # 价格
    price_min = product.get('sellingPriceMin', 'N/A')
    price_max = product.get('sellingPriceMax', 'N/A')
    if price_min and price_max and price_min != 'US$0.0':
        lines.append(f"价格: {price_min}" + (f" ~ {price_max}" if price_max != price_min else ""))
    else:
        lines.append(f"价格: {product.get('spItmMidPrice', 'N/A')}")

    # 评分和销量
    rating = product.get('ratingScore', 0)
    rating_count = product.get('ratingCount', 0)
    lines.append(f"评分: {rating:.1f}/5.0 ({rating_count} 条评价)")

    sold_cnt = product.get('soldCntLast30Days', 0)
    sold_amt = product.get('soldAmtLast30Days', 'N/A')
    lines.append(f"30天销量: {sold_cnt} 件")
    if sold_amt and sold_amt != 'US$0.0':
        lines.append(f"30天销售额: {sold_amt}")

    # 上架时间
    launch_time = product.get('launchTime', 'N/A')
    lines.append(f"上架时间: {launch_time}")

    # 机会分
    opp_score = product.get('migrateOppScore', 0)
    opp_percentile = product.get('improveOppScorePercentile', 'N/A')
    lines.append(f"机会分: {opp_score:.2f} (击败 {opp_percentile} 商品)")

    # 新品机会分
    new_opp = product.get('newProductOppScore', 0)
    new_opp_percentile = product.get('newProductOppScorePercentile', 'N/A')
    lines.append(f"新品机会分: {new_opp:.2f} (击败 {new_opp_percentile} 商品)")

    # 1688 供应商信息
    sp_price = product.get('sp1688ItmAvgPrice', '')
    if sp_price:
        lines.append(f"\n1688 同款参考价: {sp_price}")

    return "\n".join(lines)


def format_response(result):
    """格式化响应结果"""
    if not result:
        return

    # AlphaShop API 返回格式: {"resultCode": "SUCCESS", "result": {"success": true, "data": {...}}}
    # 先检查 resultCode
    if result.get('resultCode') not in ['SUCCESS', None]:
        print(f"\n接口调用失败:")
        print(f"ResultCode: {result.get('resultCode', 'UNKNOWN')}")
        print(f"RequestId: {result.get('requestId', 'N/A')}")
        print(f"Message: {result.get('message', 'N/A')}")
        return

    # 获取 result 内部数据
    api_result = result.get('result', {})
    if not api_result.get('success'):
        print(f"\n业务处理失败:")
        print(f"Success: {api_result.get('success', False)}")
        print(f"Message: {api_result.get('message', 'N/A')}")
        return

    # 获取商品数据
    response_data = api_result.get('data', {})
    total_count = response_data.get('totalCount', 0)
    products = response_data.get('productList', [])
    keyword = response_data.get('keyword', '')
    platform = response_data.get('platform', '')
    region = response_data.get('region', '')

    print(f"\n{'='*80}")
    print(f"搜索结果")
    print(f"{'='*80}")
    print(f"关键词: {keyword}")
    print(f"平台: {platform} | 区域: {region}")
    print(f"总计找到 {total_count} 个商品")
    print(f"返回 {len(products)} 个商品\n")

    # 输出每个商品
    for i, product in enumerate(products, 1):
        print(format_product(product, i))

    print(f"\n{'='*80}\n")


def main():
    parser = argparse.ArgumentParser(
        description="商品搜索API - 基于关键词搜索Amazon/TikTok平台商品",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 基础搜索
  python3 scripts/search.py --keyword "phone" --platform amazon --region US

  # 带认证的搜索
  python3 scripts/search.py --keyword "phone" --platform amazon --region US \\
    --app-key YOUR_APP_KEY --app-secret YOUR_APP_SECRET

  # 价格筛选
  python3 scripts/search.py --keyword "phone" --platform amazon --region US --min-price 10 --max-price 100

  # 综合筛选
  python3 scripts/search.py --keyword "phone" --platform amazon --region US \\
    --min-price 10 --max-price 100 --min-sales 100 --min-rating 4.0 --listing-time 90 --count 20
        """
    )

    # 必填参数
    parser.add_argument("--keyword", required=True, help="搜索关键词")
    parser.add_argument("--platform", required=True, choices=["amazon", "tiktok"], help="目标平台")
    parser.add_argument("--region", required=True, help="目标国家/地区代码（如US, UK, JP, ID, TH）")

    # 筛选条件（可选）
    parser.add_argument("--min-price", type=float, help="最低价格（美元）")
    parser.add_argument("--max-price", type=float, help="最高价格（美元）")
    parser.add_argument("--min-sales", type=int, help="最低30天销量")
    parser.add_argument("--max-sales", type=int, help="最高30天销量")
    parser.add_argument("--min-rating", type=float, help="最低评分（0-5.0）")
    parser.add_argument("--max-rating", type=float, help="最高评分（0-5.0）")
    parser.add_argument("--listing-time", type=int, choices=LISTING_TIME_OPTIONS, help="上架时间（天），可选: 90, 180, 365")

    # 其他参数
    parser.add_argument("--count", type=int, default=10, help="返回商品数量（默认10）")
    parser.add_argument("--user-id", default="123456", help="用户ID（默认123456）")
    parser.add_argument("--app-key", help="AlphaShop App Key（可选，用于认证）", default=os.environ.get("ALPHASHOP_ACCESS_KEY"))
    parser.add_argument("--app-secret", help="AlphaShop App Secret（可选，用于认证）", default=os.environ.get("ALPHASHOP_SECRET_KEY"))
    parser.add_argument("--output", help="输出结果到文件（JSON格式）")

    args = parser.parse_args()

    # 参数校验
    if not validate_params(args):
        sys.exit(1)

    # 构建请求
    request_data = build_request(args)

    # 调用接口
    result = call_api(request_data, args.user_id, args.app_key, args.app_secret)

    if not result:
        sys.exit(1)

    # 如果指定了输出文件，保存完整响应
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\n完整响应已保存到: {args.output}")

    # 格式化输出
    format_response(result)

    # 返回退出码
    if result.get('resultCode') == 'SUCCESS' and result.get('result', {}).get('success'):
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
