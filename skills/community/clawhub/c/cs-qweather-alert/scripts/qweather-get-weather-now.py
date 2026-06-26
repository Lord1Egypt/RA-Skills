#!/usr/bin/env python3
"""
和风天气实况查询脚本

用法:
    python qweather-get-weather-now.py <城市名> [API_HOST] [JWT_TOKEN]

环境变量:
    QWEATHER_API_HOST  和风天气 API Host（如 https://api.qweather.com）
    QWEATHER_CITY      默认城市名称（可选）

Token 配置:
    默认从 ~/.myjwtkey/last-token.dat 读取，也可通过 --token 参数指定

示例:
    python qweather-get-weather-now.py 北京
"""

import sys
import os
import argparse

# 将脚本所在目录加入 import 路径，确保从任意目录运行都能找到 qweather_utils
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)

# 导入公共模块
from qweather_utils import (
    get_token,
    get_host,
    api_get,
    resolve_city,
    format_timestamp,
    set_cache_dir,
    get_weather_emoji,
)


# ============ API 查询 ============

def get_weather_now(host: str, token: str, location_id: str) -> dict:
    """
    调用实时天气 API（v7/weather/now）。
    location_id: 和风 LocationID（如 101010100）
    """
    url = f"{host}/v7/weather/now?location={location_id}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }
    return api_get(url, headers, log_prefix="qweather-get-weather-now")


# ============ 格式化输出 ============

def format_wind_info(wind_dir: str, wind_scale: str, wind_speed: str) -> str:
    """格式化风力信息。"""
    return f"{wind_dir} {wind_scale}级 ({wind_speed} km/h)"


def format_output(city_name: str, lat: str, lon: str, weather_result: dict) -> str:
    """将完整查询结果格式化为最终输出文本。"""
    now = weather_result.get("now", {})
    refer = weather_result.get("refer", {})

    obs_time = format_timestamp(now.get("obsTime", ""))
    temp = now.get("temp", "--")
    feels_like = now.get("feelsLike", "--")
    icon_code = now.get("icon", "900")
    text = now.get("text", "未知")
    weather_emoji = get_weather_emoji(icon_code)
    wind_info = format_wind_info(
        now.get("windDir", "--"),
        now.get("windScale", "--"),
        now.get("windSpeed", "--")
    )
    humidity = now.get("humidity", "--")
    precip = now.get("precip", "--")
    pressure = now.get("pressure", "--")
    vis = now.get("vis", "--")
    cloud = now.get("cloud", "")
    dew = now.get("dew", "")
    update_time = format_timestamp(weather_result.get("updateTime", ""))

    lines = [
        f"🌤️  {city_name} 实时天气",
        f"🕐 {obs_time}  {weather_emoji} {text}  {temp}°C（体感 {feels_like}°C）",
        f"{'─' * 40}",
        "",
        f"💨 风力 ······ {wind_info}",
        f"💧 湿度 ······ {humidity}%",
    ]

    if precip and precip not in ("0.0", "0"):
        lines.append(f"🌧️  降水量 ···· {precip} mm")
    else:
        lines.append(f"🌧️  降水量 ···· 0 mm")

    lines.extend([
        f"🌡️  气压 ······ {pressure} hPa",
        f"👁️  能见度 ···· {vis} km",
    ])

    if cloud:
        lines.append(f"☁️  云量 ······ {cloud}%")
    if dew:
        lines.append(f"🌫️  露点 ······ {dew}°C")

    lines.append("")
    lines.append(f"{'─' * 40}")
    sources = refer.get("sources", [])
    if sources:
        lines.append(f"📡 {', '.join(sources)} | {update_time}")

    return "\n".join(lines)


# ============ 入口 ============

def main():
    # 注入脚本目录，用于确定缓存路径
    set_cache_dir(_SCRIPT_DIR)

    parser = argparse.ArgumentParser(
        description="和风天气实况查询工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("city", nargs="?", default=None, help="城市名称（如北京、上海）")
    parser.add_argument("--host", dest="host", default=None,
                        help="API Host（也可设置环境变量 QWEATHER_API_HOST）")
    parser.add_argument("--token", dest="token", default=None,
                        help="JWT Token（默认从 ~/.myjwtkey/last-token.dat 读取）")
    args = parser.parse_args()

    city_name = args.city or os.environ.get("QWEATHER_CITY", "").strip()
    if not city_name:
        print("错误: 请提供城市名称作为参数，或设置环境变量 QWEATHER_CITY", file=sys.stderr)
        sys.exit(1)

    host = get_host("QWEATHER_API_HOST", args.host, "API Host")
    token = get_token(args.token)

    print(f"正在查询城市: {city_name} ...", file=sys.stderr)

    result = resolve_city(city_name, host, token)
    if not result:
        sys.exit(1)
    _, lat, lon, full_city_name, location_id = result

    print(f"正在获取实时天气 ...", file=sys.stderr)
    weather_result = get_weather_now(host, token, location_id)

    output = format_output(full_city_name, lat, lon, weather_result)
    print()
    print(output)


if __name__ == "__main__":
    main()