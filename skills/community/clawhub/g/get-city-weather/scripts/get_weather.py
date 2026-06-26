#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""天气信息获取脚本。"""

import os
import sys
from datetime import datetime
from pathlib import Path

import requests

API_URL = "http://apis.juhe.cn/simpleWeather/query"
ENV_API_KEY_NAMES = ("JUHE_WEATHER_API_KEY", "WEATHER_API_KEY")
SKILL_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = SKILL_DIR / "output"
ENV_FILE = SKILL_DIR / ".env"

# 确保输出目录存在
OUTPUT_DIR.mkdir(exist_ok=True)


def configure_console_encoding():
    """优先将控制台输出切换到 UTF-8，避免 Windows 下打印 emoji 失败。"""
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        if not stream or not hasattr(stream, "reconfigure"):
            continue
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            continue

def load_env_file(env_file):
    """加载简单的 .env 文件配置。"""
    if not env_file.exists():
        return

    for raw_line in env_file.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def get_api_key():
    """从环境变量读取 API Key。"""
    load_env_file(ENV_FILE)
    for env_name in ENV_API_KEY_NAMES:
        value = os.environ.get(env_name, "").strip()
        if value:
            return value
    return ""


def parse_temperature_range(temperature_text, fallback_current):
    """解析接口返回的温度区间。"""
    numbers = []
    cleaned = temperature_text.replace("℃", "").replace("°C", "")

    for part in cleaned.replace("~", "/").split("/"):
        part = part.strip()
        if not part:
            continue
        try:
            numbers.append(int(float(part)))
        except ValueError:
            continue

    if len(numbers) >= 2:
        return min(numbers[0], numbers[1]), max(numbers[0], numbers[1])
    if len(numbers) == 1:
        return numbers[0], numbers[0]
    return fallback_current, fallback_current


def get_air_quality_label(aqi_value):
    """根据 AQI 生成空气质量说明。"""
    if aqi_value <= 50:
        return "优"
    if aqi_value <= 100:
        return "良"
    if aqi_value <= 150:
        return "轻度污染"
    if aqi_value <= 200:
        return "中度污染"
    if aqi_value <= 300:
        return "重度污染"
    return "严重污染"


def build_life_indices(current_temp, condition):
    """根据天气生成生活指数建议。"""
    if current_temp < 10:
        clothing = "建议穿厚外套、毛衣"
    elif current_temp < 20:
        clothing = "建议穿薄外套、长袖"
    else:
        clothing = "建议穿短袖、薄衣物"

    if "雨" in condition:
        sport = "不适宜户外运动，建议室内活动"
        car_wash = "不适宜洗车"
    else:
        sport = "适宜户外运动"
        car_wash = "适宜洗车"

    if current_temp < 5 or current_temp > 28:
        cold = "易发，注意防护"
    else:
        cold = "较不易发"

    return clothing, sport, car_wash, cold


def fetch_weather_by_api(city_name, api_key):
    """通过聚合数据 API 获取天气。"""
    response = requests.get(
        API_URL,
        params={"city": city_name, "key": api_key},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=15,
    )
    response.raise_for_status()

    payload = response.json()
    if payload.get("error_code") != 0:
        reason = payload.get("reason") or "未知错误"
        raise ValueError(f"天气 API 返回失败: {reason}")

    result = payload.get("result") or {}
    realtime = result.get("realtime") or {}
    future = result.get("future") or []
    today = future[0] if future else {}

    current_temp = int(float(realtime.get("temperature") or 0))
    low_temp, high_temp = parse_temperature_range(today.get("temperature", ""), current_temp)
    aqi = int(realtime.get("aqi") or 0)
    clothing, sport, car_wash, cold = build_life_indices(current_temp, realtime.get("info") or "未知")

    now = datetime.now()
    return {
        "city": result.get("city") or city_name,
        "date": now.strftime("%Y年%m月%d日"),
        "weekday": ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"][now.weekday()],
        "current_temp": current_temp,
        "low_temp": low_temp,
        "high_temp": high_temp,
        "condition": realtime.get("info") or today.get("weather") or "未知",
        "wind_direction": realtime.get("direct") or today.get("direct") or "未知风向",
        "wind_level": realtime.get("power") or "未知风力",
        "aqi": aqi,
        "air_quality": get_air_quality_label(aqi),
        "clothing_index": clothing,
        "sport_index": sport,
        "car_wash_index": car_wash,
        "cold_index": cold,
    }


def format_weather_report(weather_data):
    """格式化天气报告"""
    report = f"""
========================================
          {weather_data['city']}市 今日天气报告
========================================

📅 日期：{weather_data['date']} {weather_data['weekday']}

🌡️  温度：{weather_data['low_temp']}°C ~ {weather_data['high_temp']}°C
    当前：{weather_data['current_temp']}°C

☁️  天气：{weather_data['condition']}

💨 风力：{weather_data['wind_direction']} {weather_data['wind_level']}

🌫️ 空气质量：{weather_data['air_quality']} (AQI: {weather_data['aqi']})

💡 生活指数：
    • 穿衣：{weather_data['clothing_index']}
    • 运动：{weather_data['sport_index']}
    • 洗车：{weather_data['car_wash_index']}
    • 感冒：{weather_data['cold_index']}

========================================
"""
    return report


def save_weather_report(city_name, report):
    """保存天气报告到文件"""
    date_str = datetime.now().strftime("%Y%m%d")
    filename = f"weather_report_{city_name}_{date_str}.txt"
    filepath = OUTPUT_DIR / filename
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(report)
    
    return filepath


def main():
    configure_console_encoding()

    # 获取城市名
    if len(sys.argv) > 1:
        city_name = sys.argv[1]
    else:
        city_name = input("请输入城市名称（如：北京）：").strip()
    
    if not city_name:
        print("错误：请输入有效的城市名称")
        sys.exit(1)
    
    # 移除"市"后缀（如果有）
    city_name = city_name.replace("市", "").replace("县", "")
    
    print(f"正在获取 {city_name} 的天气信息...")

    api_key = get_api_key()
    if not api_key:
        print("错误：未找到天气 API Key。请在环境变量或 .env 中设置 JUHE_WEATHER_API_KEY。")
        sys.exit(1)

    try:
        weather_data = fetch_weather_by_api(city_name, api_key)
        print("已通过聚合数据 API 获取实时天气。")
    except (requests.RequestException, ValueError) as exc:
        print(f"错误：API 获取天气失败：{exc}")
        sys.exit(1)
    
    # 格式化报告
    report = format_weather_report(weather_data)
    
    # 显示报告
    print(report)
    
    # 保存报告
    filepath = save_weather_report(city_name, report)
    print(f"天气报告已保存至：{filepath}")
    
    return weather_data


if __name__ == "__main__":
    main()
