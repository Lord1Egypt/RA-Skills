#!/usr/bin/env python3
"""
和风天气每日预报查询脚本

用法:
    python qweather-get-weather-daily.py <城市名> [--days 7] [--host API_HOST] [--token TOKEN]

环境变量:
    QWEATHER_API_HOST  和风天气 API Host（如 https://xxx.re.qweatherapi.com）
    QWEATHER_CITY      默认城市名称（可选）

Token 配置:
    默认从 ~/.myjwtkey/last-token.dat 读取，也可通过 --token 参数指定

示例:
    python qweather-get-weather-daily.py 北京                    # 查询7天预报
    python qweather-get-weather-daily.py 北京 --days 15          # 查询15天预报
    python qweather-get-weather-daily.py 上海 --days 30         # 查询30天预报
    python qweather-get-weather-daily.py 广州 --days 3           # 查询3天预报
"""

import sys
import os
import argparse
import datetime as dt

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
    uv_description,
)


# ============ 本地工具函数 ============

def format_weekday(date_str: str) -> str:
    """将 YYYY-MM-DD 格式的日期转换为星期几。"""
    try:
        dt_obj = dt.datetime.strptime(date_str, "%Y-%m-%d")
        weekdays = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        return weekdays[dt_obj.weekday()]
    except Exception:
        return ""


# ============ API 查询 ============

def get_weather_daily(host: str, token: str, location: str, days: str) -> dict:
    """
    调用每日天气预报 API（v7/weather/{days}）。
    location: 和风 LocationID（如 101010100）或 "经度,纬度"
    days: 预报天数，支持 3d/7d/10d/15d/30d
    """
    url = f"{host}/v7/weather/{days}?location={location}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }
    return api_get(url, headers, log_prefix="qweather-get-weather-daily")


# ============ 格式化输出 ============

def format_day_line(day: dict, index: int, total: int) -> str:
    """将单日预报格式化为一行。"""
    fx_date = day.get("fxDate", "")
    weekday = format_weekday(fx_date)
    temp_max = day.get("tempMax", "--")
    temp_min = day.get("tempMin", "--")
    icon_day = day.get("iconDay", "900")
    icon_night = day.get("iconNight", "900")
    text_day = day.get("textDay", "")
    text_night = day.get("textNight", "")
    wind_dir_day = day.get("windDirDay", "")
    wind_scale_day = day.get("windScaleDay", "")
    precip = day.get("precip", "0.0")
    uv_index = day.get("uvIndex", "")

    day_emoji = get_weather_emoji(icon_day)
    night_emoji = get_weather_emoji(icon_night)

    # 今天/明天/后天标记
    if index == 0:
        day_label = "今天"
    elif index == 1:
        day_label = "明天"
    elif index == 2:
        day_label = "后天"
    else:
        day_label = weekday

    # 日间图标 + 天气 + 夜间图标
    weather_str = f"{day_emoji}{text_day}"
    if text_night != text_day:
        weather_str += f"→{night_emoji}{text_night}"

    # 降水
    precip_float = float(precip) if precip not in ("", None) else 0.0
    if precip_float > 0:
        precip_str = f"🌧️{precip}mm"
    else:
        precip_str = "💧无降水"

    # 紫外线
    uv_str = f"紫外线: {uv_index}({uv_description(uv_index)})" if uv_index else ""

    parts = [
        f"{day_label} {fx_date[5:]}",
        weather_str,
        f"{temp_min}°C~{temp_max}°C",
        f"{wind_dir_day}{wind_scale_day}级",
        precip_str,
    ]
    if uv_str:
        parts.append(uv_str)

    return " | ".join(parts)


def format_output(city_name: str, lat: str, lon: str, daily_result: dict, days_label: str) -> str:
    """将完整查询结果格式化为最终输出文本。"""
    daily_list = daily_result.get("daily", [])
    refer = daily_result.get("refer", {})
    update_time = format_timestamp(daily_result.get("updateTime", ""))

    lines = [
        f"📅 {city_name} {days_label}天气预报",
        f"{'─' * 60}",
    ]

    # 每日详情
    for i, day in enumerate(daily_list):
        lines.append(format_day_line(day, i, len(daily_list)))
        lines.append("")

    # 日出日落 / 月相（只显示第一天的，因为后续可能重复）
    if daily_list:
        first = daily_list[0]
        sunrise = first.get("sunrise", "")
        sunset = first.get("sunset", "")
        moonrise = first.get("moonrise", "")
        moonset = first.get("moonset", "")
        moon_phase = first.get("moonPhase", "")
        lines.append(f"{'─' * 60}")
        astro_parts = []
        if sunrise and sunset:
            astro_parts.append(f"🌅 日出 {sunrise} / 日落 {sunset}")
        if moon_phase:
            astro_parts.append(f"🌙 {moon_phase}")
            if moonrise:
                astro_parts.append(f"   月升 {moonrise} / 月落 {moonset}")
        if astro_parts:
            lines.append("  ".join(astro_parts))

    # 数据来源
    sources = refer.get("sources", [])
    if sources:
        lines.append(f"{'─' * 60}")
        lines.append(f"📡 {', '.join(sources)} | 更新于 {update_time}")

    return "\n".join(lines)


# ============ 入口 ============

def main():
    # 注入脚本目录，用于确定缓存路径
    set_cache_dir(_SCRIPT_DIR)

    parser = argparse.ArgumentParser(
        description="和风天气每日预报查询工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("city", nargs="?", default=None, help="城市名称（如北京、上海）")
    parser.add_argument("--days", dest="days", default="7",
                        choices=["3", "7", "10", "15", "30"],
                        help="预报天数（3/7/10/15/30天，默认7天）")
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

    days_map = {"3": "3天", "7": "7天", "10": "10天", "15": "15天", "30": "30天"}
    days_label = days_map.get(args.days, "7天")

    print(f"正在查询城市: {city_name}（{days_label}预报）...", file=sys.stderr)

    result = resolve_city(city_name, host, token)
    if not result:
        sys.exit(1)
    _, lat, lon, full_city_name, location_id = result

    # API 的 days 参数格式
    api_days = args.days + "d"

    print(f"正在获取天气预报 ...", file=sys.stderr)
    weather_result = get_weather_daily(host, token, location_id, api_days)

    output = format_output(full_city_name, lat, lon, weather_result, days_label)
    print()
    print(output)


if __name__ == "__main__":
    main()