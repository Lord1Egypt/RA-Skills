#!/usr/bin/env python
"""
饿了么API模块
获取附近外卖店和菜品推荐
"""
import json
import urllib.request
import urllib.parse
import ssl
from config_manager import get_config


def create_ssl_context():
    """创建SSL上下文"""
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


def get_nearby_restaurants(latitude, longitude, offset=0, limit=20):
    """
    获取附近的外卖店

    Args:
        latitude: 纬度
        longitude: 经度
        offset: 偏移量
        limit: 返回数量

    Returns:
        店铺列表
    """
    config = get_config()
    cookie = config.get('cookie', '')

    if not cookie:
        return {"error": "请先设置饿了么Cookie，使用: python scripts/main.py set-config --cookie 'your_cookie'"}

    # 饿了么附近店铺API
    url = "https://www.ele.me/restapi/shopping/v3/restaurants"

    params = {
        'latitude': latitude,
        'longitude': longitude,
        'offset': offset,
        'limit': limit,
        'extras[]': 'activities',
        'extra_filters': 'home'
    }

    query_string = urllib.parse.urlencode(params)
    full_url = f"{url}?{query_string}"

    try:
        req = urllib.request.Request(full_url)
        req.add_header('Cookie', cookie)
        req.add_header('User-Agent', 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.0')
        req.add_header('Referer', 'https://www.ele.me/')

        ctx = create_ssl_context()
        with urllib.request.urlopen(req, timeout=10, context=ctx) as response:
            data = json.loads(response.read())
            return data
    except Exception as e:
        return {"error": str(e), "message": "获取附近店铺失败，请检查Cookie是否有效"}


def get_restaurant_foods(restaurant_id):
    """
    获取店铺的菜品列表

    Args:
        restaurant_id: 店铺ID

    Returns:
        菜品列表
    """
    config = get_config()
    cookie = config.get('cookie', '')

    if not cookie:
        return {"error": "请先设置饿了么Cookie"}

    url = f"https://www.ele.me/restapi/shopping/v2/menu?restaurant_id={restaurant_id}"

    try:
        req = urllib.request.Request(url)
        req.add_header('Cookie', cookie)
        req.add_header('User-Agent', 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.0')
        req.add_header('Referer', 'https://www.ele.me/')

        ctx = create_ssl_context()
        with urllib.request.urlopen(req, timeout=10, context=ctx) as response:
            data = json.loads(response.read())
            return data
    except Exception as e:
        return {"error": str(e)}


def recommend_foods(restaurants, flavor, count):
    """
    根据口味偏好推荐菜品

    Args:
        restaurants: 店铺列表
        flavor: 口味偏好
        count: 推荐数量

    Returns:
        推荐菜品列表
    """
    recommendations = []

    # 口味关键词映射
    flavor_keywords = {
        "清淡": ["清淡", "少油", "少盐", "蒸", "煮", "炖"],
        "重口": ["重口味", "麻辣", "香辣", "爆炒", "红烧"],
        "微辣": ["微辣", "小辣"],
        "中辣": ["中辣", "麻辣"],
        "辣": ["麻辣", "香辣", "辣"],
        "甜": ["甜", "糖醋", "蜜汁"],
        "酸": ["酸", "酸辣", "醋"],
    }

    keywords = flavor_keywords.get(flavor, [flavor])

    for restaurant in restaurants:
        restaurant_id = restaurant.get('id')
        foods = get_restaurant_foods(restaurant_id)

        if isinstance(foods, dict) and 'error' in foods:
            continue

        # 遍历菜单分类
        for category in foods:
            for food in category.get('foods', []):
                food_name = food.get('name', '')
                description = food.get('description', '')

                # 检查是否匹配口味
                matched = False
                for keyword in keywords:
                    if keyword in food_name or keyword in description:
                        matched = True
                        break

                if matched or flavor == "不限":
                    item = {
                        'restaurant_name': restaurant.get('name', ''),
                        'restaurant_id': restaurant_id,
                        'food_name': food_name,
                        'description': description,
                        'price': food.get('price', 0),
                        'image': food.get('image_path', ''),
                        'rating': food.get('rating', 0),
                        'month_sales': food.get('month_sales', 0)
                    }
                    recommendations.append(item)

                    if len(recommendations) >= count:
                        break

            if len(recommendations) >= count:
                break

        if len(recommendations) >= count:
            break

    return recommendations[:count]
