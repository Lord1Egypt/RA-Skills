#!/usr/bin/env python
"""
菜品推荐模块
根据饭点和口味偏好推荐菜品
"""
import datetime
from config_manager import get_config
from eleme_api import get_nearby_restaurants, recommend_foods


def get_current_meal_time():
    """获取当前应该推荐的餐次"""
    now = datetime.datetime.now()
    hour = now.hour

    # 早餐: 5-10点
    if 5 <= hour < 10:
        return "breakfast"
    # 午餐: 10-14点
    elif 10 <= hour < 14:
        return "lunch"
    # 晚餐: 16-21点
    elif 16 <= hour < 21:
        return "dinner"
    else:
        return None


def get_next_meal_time():
    """获取下一餐的时间配置"""
    config = get_config()
    now = datetime.datetime.now()
    current_hour = now.hour

    # 判断下一餐
    if current_hour < 10:
        return "breakfast", config.get('breakfast', '07:30')
    elif current_hour < 14:
        return "lunch", config.get('lunch', '11:30')
    elif current_hour < 18:
        return "dinner", config.get('dinner', '18:30')
    else:
        # 明天早餐
        return "breakfast", config.get('breakfast', '07:30')


def should_recommend():
    """检查是否应该进行推荐（在饭点前）"""
    config = get_config()
    now = datetime.datetime.now()

    meal_times = {
        "breakfast": config.get('breakfast', '07:30'),
        "lunch": config.get('lunch', '11:30'),
        "dinner": config.get('dinner', '18:30')
    }

    for meal, time_str in meal_times.items():
        try:
            hour, minute = map(int, time_str.split(':'))
            meal_time = now.replace(hour=hour, minute=minute, second=0)

            # 在饭点前30分钟到饭点之间推荐
            recommend_window = meal_time - datetime.timedelta(minutes=30)
            if recommend_window <= now <= meal_time:
                return True, meal
        except:
            continue

    return False, None


def generate_recommendation():
    """
    生成推荐结果

    Returns:
        推荐结果字典
    """
    config = get_config()

    # 检查配置
    if not config.get('cookie'):
        return {
            "error": "请先设置饿了么Cookie",
            "tip": "使用: python scripts/main.py set-config --cookie 'your_cookie'"
        }

    location = config.get('location', {})
    if not location.get('latitude') or not location.get('longitude'):
        return {
            "error": "请先设置定位信息",
            "tip": "使用: python scripts/main.py set-config --latitude 39.90 --longitude 116.40"
        }

    # 获取附近店铺
    latitude = location.get('latitude')
    longitude = location.get('longitude')

    restaurants_data = get_nearby_restaurants(latitude, longitude)

    if isinstance(restaurants_data, dict) and 'error' in restaurants_data:
        return restaurants_data

    # 提取店铺列表
    if isinstance(restaurants_data, dict):
        restaurants = restaurants_data.get('items', [])
    else:
        restaurants = restaurants_data[:20]  # 取前20家店

    if not restaurants:
        return {"error": "附近没有找到外卖店铺"}

    # 获取用户偏好
    flavor = config.get('flavor', '不限')
    count = config.get('recommend_count', 3)

    # 生成推荐
    recommendations = recommend_foods(restaurants, flavor, count)

    if not recommendations:
        return {
            "message": "附近店铺已找到，但暂无符合您口味偏好的菜品",
            "restaurants_count": len(restaurants),
            "flavor": flavor
        }

    # 获取当前/下一餐信息
    should_rec, meal_type = should_recommend()
    if not should_rec:
        next_meal, next_time = get_next_meal_time()
        meal_type = next_meal

    return {
        "meal_type": meal_type,
        "flavor": flavor,
        "recommend_count": count,
        "restaurants_count": len(restaurants),
        "recommendations": recommendations
    }


def get_meal_time_status():
    """获取饭点状态"""
    config = get_config()
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M")

    meal_times = {
        "breakfast": config.get('breakfast', '07:30'),
        "lunch": config.get('lunch', '11:30'),
        "dinner": config.get('dinner', '18:30')
    }

    status = []
    for meal, time_str in meal_times.items():
        status.append({
            "meal": meal,
            "time": time_str,
            "passed": time_str < current_time
        })

    return status
