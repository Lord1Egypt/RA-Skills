#!/usr/bin/env python3
"""高德天气 API 查询脚本。

用法:
  python3 amap_weather.py <城市名或adcode> [--forecast] [--key KEY]

环境变量:
  AMAP_API_KEY  高德 Web 服务 API Key（也可用 --key 传入）

示例:
  python3 amap_weather.py 北京              # 实况天气
  python3 amap_weather.py 110000 --forecast  # 北京未来预报
  python3 amap_weather.py 杭州 --forecast    # 杭州预报
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
import urllib.parse

# 常用城市 adcode 快查表（省会+直辖市+热门城市）
CITY_ADCODE = {
    "北京": "110000", "上海": "310000", "广州": "440100", "深圳": "440300",
    "天津": "120000", "重庆": "500000", "杭州": "330100", "南京": "320100",
    "成都": "510100", "武汉": "420100", "西安": "610100", "苏州": "320500",
    "长沙": "430100", "郑州": "410100", "青岛": "370200", "大连": "210200",
    "厦门": "350200", "昆明": "530100", "贵阳": "520100", "合肥": "340100",
    "福州": "350100", "济南": "370100", "沈阳": "210100", "哈尔滨": "230100",
    "长春": "220100", "南宁": "450100", "海口": "460100", "太原": "140100",
    "石家庄": "130100", "呼和浩特": "150100", "乌鲁木齐": "650100",
    "兰州": "620100", "银川": "640100", "西宁": "630100", "拉萨": "540100",
    "南昌": "360100", "珠海": "440400", "东莞": "441900", "佛山": "440600",
    "无锡": "320200", "宁波": "330200", "温州": "330300", "三亚": "460200",
    "烟台": "370600", "洛阳": "410300", "桂林": "450300", "丽江": "530700",
}

WEATHER_EMOJI = {
    "晴": "☀️", "少云": "🌤", "晴间多云": "⛅", "多云": "☁️", "阴": "☁️",
    "阵雨": "🌦", "雷阵雨": "⛈", "小雨": "🌧", "中雨": "🌧", "大雨": "🌧",
    "暴雨": "🌊", "大暴雨": "🌊", "特大暴雨": "🌊", "雨夹雪": "🌨",
    "小雪": "❄️", "中雪": "❄️", "大雪": "❄️", "暴雪": "❄️",
    "雾": "🌫", "浓雾": "🌫", "霾": "😷", "沙尘暴": "🏜",
}


def get_api_key(args_key: str | None) -> str:
    key = args_key or os.environ.get("AMAP_API_KEY", "")
    if not key:
        print("错误: 未提供 API Key。请设置 AMAP_API_KEY 环境变量或使用 --key 参数。", file=sys.stderr)
        sys.exit(1)
    return key


def resolve_city(city_input: str) -> str:
    """将城市名或 adcode 解析为 adcode。"""
    if city_input.isdigit():
        return city_input
    code = CITY_ADCODE.get(city_input)
    if code:
        return code
    # 尝试模糊匹配
    for name, adcode in CITY_ADCODE.items():
        if city_input in name or name in city_input:
            return adcode
    print(f"警告: 未在快查表中找到 '{city_input}'，尝试直接查询...", file=sys.stderr)
    return city_input


def fetch_weather(key: str, adcode: str, extensions: str = "base") -> dict:
    """调用高德天气 API。"""
    params = urllib.parse.urlencode({
        "key": key,
        "city": adcode,
        "extensions": extensions,
        "output": "JSON",
    })
    url = f"https://restapi.amap.com/v3/weather/weatherInfo?{params}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "OpenClaw/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError as e:
        print(f"请求失败: {e}", file=sys.stderr)
        sys.exit(1)


def format_live(data: dict) -> str:
    """格式化实况天气输出。"""
    if data.get("status") != "1" or not data.get("lives"):
        return f"查询失败: {data.get('info', '未知错误')}"

    live = data["lives"][0]
    weather = live.get("weather", "未知")
    emoji = WEATHER_EMOJI.get(weather, "🌡")
    lines = [
        f"{emoji} {live['province']} · {live['city']} 实况天气",
        f"━━━━━━━━━━━━━━━━━━━━",
        f"🌡 气温: {live['temperature']}°C",
        f"🌤 天气: {weather}",
        f"💨 风向: {live['winddirection']}风 {live['windpower']}级",
        f"💧 湿度: {live['humidity']}%",
        f"🕐 发布: {live['reporttime']}",
    ]
    return "\n".join(lines)


def format_forecast(data: dict) -> str:
    """格式化预报天气输出。"""
    if data.get("status") != "1" or not data.get("forecasts"):
        return f"查询失败: {data.get('info', '未知错误')}"

    fc = data["forecasts"][0]
    lines = [
        f"📅 {fc['province']} · {fc['city']} 天气预报",
        f"━━━━━━━━━━━━━━━━━━━━",
    ]

    weekdays = {"1": "一", "2": "二", "3": "三", "4": "四", "5": "五", "6": "六", "7": "日"}
    for cast in fc.get("casts", []):
        wd = weekdays.get(cast["week"], cast["week"])
        day_emoji = WEATHER_EMOJI.get(cast["dayweather"], "🌡")
        lines.append(f"\n{cast['date']} 周{wd}")
        lines.append(f"  {day_emoji} 白天: {cast['dayweather']} {cast['daytemp']}°C {cast['daywind']}风{cast['daypower']}级")
        night_emoji = WEATHER_EMOJI.get(cast["nightweather"], "🌙")
        lines.append(f"  {night_emoji} 夜间: {cast['nightweather']} {cast['nighttemp']}°C {cast['nightwind']}风{cast['nightpower']}级")

    lines.append(f"\n🕐 发布: {fc['reporttime']}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="高德天气查询")
    parser.add_argument("city", help="城市名（如 北京）或 adcode（如 110000）")
    parser.add_argument("--forecast", action="store_true", help="查询未来预报（默认为实况）")
    parser.add_argument("--key", help="高德 API Key（也可用 AMAP_API_KEY 环境变量）")
    parser.add_argument("--json", action="store_true", help="输出原始 JSON")
    args = parser.parse_args()

    key = get_api_key(args.key)
    adcode = resolve_city(args.city)
    extensions = "all" if args.forecast else "base"

    data = fetch_weather(key, adcode, extensions)

    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    elif args.forecast:
        print(format_forecast(data))
    else:
        print(format_live(data))


if __name__ == "__main__":
    main()
