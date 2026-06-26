#!/usr/bin/env python3
"""
和风天气预警查询脚本

用法:
    python qweather-get-weather-alert.py <城市名> [API_HOST] [JWT_TOKEN]

环境变量:
    QWEATHER_API_HOST  和风天气 API Host（如 https://api.qweather.com）
    QWEATHER_CITY      默认城市名称（可选）

Token 配置:
    默认从 ~/.myjwtkey/last-token.dat 读取，也可通过 --token 参数指定

示例:
    python qweather-get-weather-alert.py 北京
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
)

# ============ 预警 Emoji 映射（预警专用）=============

SEVERITY_EMOJI = {
    "extreme": "🔴",
    "severe":   "🟠",
    "moderate": "🟡",
    "minor":    "🔵",
    "unknown":  "⚪",
}

SEVERITY_NAME = {
    "extreme": "极严重",
    "severe":   "严重",
    "moderate": "中等",
    "minor":    "轻微",
    "unknown":  "未知",
}

EVENT_TYPE_EMOJI = {
    "1006": "💨",  # 大风
    "2001": "🌡️", # 高温
    "2002": "🌀", # 台风
    "2003": "🌧️", # 暴雨
    "2004": "❄️",  # 暴雪
    "2005": "🥶",  # 寒潮
    "2006": "🌫️", # 大雾
    "2007": "😷", # 霾
    "2008": "⚡", # 雷电
    "2009": "🧊", # 冰雹
    "2010": "🌪️", # 沙尘暴
    "2011": "🏜️", # 干旱
    "2013": "🌊", # 洪涝
    "2014": "💧", # 渍涝
    "2015": "🏙️", # 城市高温
    "5001": "⛰️", # 地质灾害
    "5002": "🏞️", # 洪水
    "5003": "🪨", # 崩塌
    "5004": "⛰️", # 滑坡
    "5005": "🌋", # 泥石流
    "5006": "💦", # 水文
    "5007": "🏜️", # 干旱
    "6001": "🔥", # 森林火险
    "6002": "🔥", # 草原火险
    "6003": "🧊", # 冰冻
    "6004": "🥶", # 低温冻害
    "6005": "❄️",  # 雪灾
}

DEFAULT_EVENT_EMOJI = "⚠️"


# ============ API 查询 ============

def get_weather_alerts(host: str, token: str, lat: str, lon: str) -> dict:
    """调用天气预警 API。"""
    url = f"{host}/weatheralert/v1/current/{lat}/{lon}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }
    return api_get(url, headers, log_prefix="qweather-get-weather-alert")


# ============ 格式化输出 ============

def get_event_emoji(event_code: str) -> str:
    """根据事件代码获取 emoji。"""
    return EVENT_TYPE_EMOJI.get(event_code, DEFAULT_EVENT_EMOJI)


def get_severity_emoji(severity: str) -> str:
    """根据严重程度获取 emoji。"""
    return SEVERITY_EMOJI.get(severity.lower(), SEVERITY_EMOJI["unknown"])


def format_alert(alert: dict) -> str:
    """将单条预警格式化为易读文本。"""
    severity_emoji = get_severity_emoji(alert.get("severity", "unknown"))
    severity_name = SEVERITY_NAME.get(alert.get("severity", "unknown"), "未知")
    event_code = alert.get("eventType", {}).get("code", "")
    event_name = alert.get("eventType", {}).get("name", "未知预警")
    event_emoji = get_event_emoji(event_code)

    headline = alert.get("headline", "无标题")
    description = alert.get("description", "无详细描述")
    instruction = alert.get("instruction", "")
    sender = alert.get("senderName", "未知来源")
    effective = format_timestamp(alert.get("effectiveTime", ""))
    expire = format_timestamp(alert.get("expireTime", ""))

    lines = [
        f"{severity_emoji} {event_emoji} 【{event_name}】{severity_emoji}",
        f"{'─' * 40}",
        f"⚡ 预警级别: {severity_name}",
        f"📢 预警标题: {headline}",
        "",
    ]

    if description and description != "无详细描述":
        lines.append(f"📋 详情: {description}")
        lines.append("")

    if instruction:
        instr_lines = instruction.strip().split("\n")
        formatted_instr = "\n".join(f"   • {l.strip()}" for l in instr_lines if l.strip())
        lines.append(f"🛡️  防御指南:")
        lines.append(formatted_instr)
        lines.append("")

    lines.append(f"🏛️  发布机构: {sender}")
    if effective:
        lines.append(f"⏰ 生效时间: {effective}")
    if expire:
        lines.append(f"⏰ 失效时间: {expire}")

    return "\n".join(lines)


def format_output(city_name: str, lat: str, lon: str, alert_result: dict) -> str:
    """将完整查询结果格式化为最终输出文本。"""
    metadata = alert_result.get("metadata", {})
    zero_result = metadata.get("zeroResult", False)

    header = [
        f"🌤️  {city_name} 天气预警",
        f"坐标: {lat}, {lon}",
        f"{'─' * 40}",
    ]

    if zero_result:
        header.append("✅ 目前没有天气预警")
        attr = metadata.get("attributions", [])
        if attr:
            header.append("")
            header.append(f"📡 数据来源: {attr[0] if attr else '和风天气'}")
        return "\n".join(header)

    alerts = alert_result.get("alerts", [])
    if not alerts:
        header.append("✅ 目前没有天气预警")
        return "\n".join(header)

    header.append(f"⚠️  共 {len(alerts)} 条预警")
    header.append("")

    lines = header[:]
    for i, alert in enumerate(alerts, 1):
        lines.append(f"【预警 {i}/{len(alerts)}】")
        lines.append(format_alert(alert))
        lines.append("")

    attr = metadata.get("attributions", [])
    if attr:
        lines.append(f"{'─' * 40}")
        for a in attr:
            lines.append(f"📡 {a}")

    return "\n".join(lines)


# ============ 入口 ============

def main():
    # 注入脚本目录，用于确定缓存路径
    set_cache_dir(_SCRIPT_DIR)

    parser = argparse.ArgumentParser(
        description="和风天气预警查询工具",
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
    _, lat, lon, full_city_name, _ = result

    print(f"正在获取天气预警 ...", file=sys.stderr)
    alert_result = get_weather_alerts(host, token, lat, lon)

    output = format_output(full_city_name, lat, lon, alert_result)
    print()
    print(output)


if __name__ == "__main__":
    main()