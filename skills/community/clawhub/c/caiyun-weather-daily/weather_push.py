#!/usr/bin/env python3
"""
weather_push.py — 彩云天气每日推送

用法:
    python3 weather_push.py                    # 使用环境变量配置
    python3 weather_push.py --token xxx --lng 116.4 --lat 39.9

环境变量:
    CAIYUN_TOKEN - 彩云天气 API Token（必需）
    LNG          - 经度（必需）
    LAT          - 纬度（必需）
    LOCATION_NAME - 位置名称（可选，默认"当前位置"）
    PUSH_CHANNEL  - 推送渠道（可选，默认 wechat）
"""

import os
import sys
import json
import argparse
import subprocess
from datetime import datetime
from urllib.request import urlopen
from urllib.error import URLError

# 默认配置（通过环境变量设置）
DEFAULT_TOKEN = os.environ.get('CAIYUN_TOKEN', '')
DEFAULT_LNG = os.environ.get('LNG', '')
DEFAULT_LAT = os.environ.get('LAT', '')
DEFAULT_LOCATION = os.environ.get('LOCATION_NAME', '当前位置')
DEFAULT_CHANNEL = os.environ.get('PUSH_CHANNEL', 'wechat')

API_BASE = "https://api.caiyunapp.com/v2.6"


def fetch_weather(token: str, lng: str, lat: str) -> dict:
    """获取综合天气数据"""
    url = f"{API_BASE}/{token}/{lng},{lat}/weather?lang=zh_CN&unit=metric&alert=true"
    
    try:
        with urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            if data.get('status') != 'ok':
                raise Exception(f"API error: {data.get('error', 'unknown')}")
            return data['result']
    except URLError as e:
        raise Exception(f"Network error: {e}")


def parse_weather_data(result: dict) -> dict:
    """解析天气数据"""
    realtime = result.get('realtime', {})
    daily = result.get('daily', {})
    minutely = result.get('minutely', {})
    
    # 实时数据
    temp = realtime.get('temperature', '--')
    feels_like = realtime.get('apparent_temperature', '--')
    humidity = int(realtime.get('humidity', 0) * 100)
    wind_speed = realtime.get('wind', {}).get('speed', '--')
    skycon = realtime.get('skycon', 'UNKNOWN')
    
    # 今日气温范围
    temp_data = daily.get('temperature', [{}])
    temp_max = temp_data[0].get('max', '--') if temp_data else '--'
    temp_min = temp_data[0].get('min', '--') if temp_data else '--'
    
    # 今日天气状况
    skycon_data = daily.get('skycon', [{}])
    today_skycon = skycon_data[0].get('value', 'UNKNOWN') if skycon_data else 'UNKNOWN'
    
    # 今日是否降雨
    rain_types = ['RAIN', 'LIGHT_RAIN', 'MODERATE_RAIN', 'HEAVY_RAIN', 'STORM_RAIN', 'DRIZZLE_RAIN']
    has_rain_today = any(r in today_skycon for r in rain_types)
    
    # 2小时内降雨概率
    precipitation_2h = minutely.get('precipitation_2h', [])
    has_rain_2h = any(p > 0.03 for p in precipitation_2h) if precipitation_2h else False
    
    # 天气描述
    skycon_desc = {
        'CLEAR': '晴', 'CLEAR_DAY': '晴', 'CLEAR_NIGHT': '晴',
        'PARTLY_CLOUDY': '多云', 'PARTLY_CLOUDY_DAY': '多云', 'PARTLY_CLOUDY_NIGHT': '多云',
        'CLOUDY': '阴',
        'LIGHT_RAIN': '小雨', 'MODERATE_RAIN': '中雨', 'HEAVY_RAIN': '大雨',
        'RAIN': '雨', 'STORM_RAIN': '暴雨', 'DRIZZLE_RAIN': '毛毛雨',
        'SNOW': '雪', 'LIGHT_SNOW': '小雪', 'MODERATE_SNOW': '中雪', 'HEAVY_SNOW': '大雪',
        'FOG': '雾', 'HAZE': '霾', 'SAND': '沙尘',
    }
    weather_desc = skycon_desc.get(skycon, skycon)
    
    return {
        'temp': temp,
        'feels_like': feels_like,
        'humidity': humidity,
        'wind_speed': wind_speed,
        'temp_max': temp_max,
        'temp_min': temp_min,
        'weather': weather_desc,
        'has_rain_today': has_rain_today,
        'has_rain_2h': has_rain_2h,
    }


def format_message(data: dict, location: str) -> str:
    """格式化天气消息"""
    rain_today = "是 ⚠️" if data['has_rain_today'] else "否"
    rain_2h = "是 ⚠️" if data['has_rain_2h'] else "否"
    
    msg = f"""🌤 {location} 今日天气

🌡 气温：{data['temp_min']}°C ~ {data['temp_max']}°C
🤔 体感：{data['feels_like']}°C
💧 湿度：{data['humidity']}%
🌬 风速：{data['wind_speed']} m/s
☁ 天气：{data['weather']}
🌧 今日降雨：{rain_today}
⏱ 2小时内降雨：{rain_2h}

📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}"""
    
    return msg


def send_message(msg: str, channel: str = 'wechat') -> bool:
    """发送消息到指定渠道"""
    # 尝试通过 OpenClaw CLI 发送
    cli_paths = [
        '/Applications/QClaw.app/Contents/Resources/openclaw/bin/openclaw',
        '/Applications/QClaw.app/Contents/Resources/openclaw/bin/cli.js',
    ]
    
    for cli_path in cli_paths:
        if os.path.exists(cli_path):
            try:
                cmd = [cli_path, 'message', 'send', '--channel', channel, msg]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                if result.returncode == 0:
                    print(f"✅ 消息已发送到 {channel}")
                    return True
            except Exception as e:
                print(f"⚠️ 发送失败 ({cli_path}): {e}")
                continue
    
    # 如果 CLI 发送失败，打印消息
    print("❌ 无法发送消息，请手动复制：")
    print("-" * 40)
    print(msg)
    print("-" * 40)
    return False


def main():
    parser = argparse.ArgumentParser(description='彩云天气每日推送')
    parser.add_argument('--token', default=DEFAULT_TOKEN, help='彩云天气 API Token')
    parser.add_argument('--lng', default=DEFAULT_LNG, help='经度')
    parser.add_argument('--lat', default=DEFAULT_LAT, help='纬度')
    parser.add_argument('--location', default=DEFAULT_LOCATION, help='位置名称')
    parser.add_argument('--channel', default=DEFAULT_CHANNEL, help='推送渠道')
    parser.add_argument('--dry-run', action='store_true', help='仅打印消息，不发送')
    
    args = parser.parse_args()
    
    # 检查必需参数
    if not args.token or not args.lng or not args.lat:
        print("❌ 错误: 请提供 --token, --lng, --lat 参数或设置环境变量")
        print("示例: python3 weather_push.py --token YOUR_TOKEN --lng 116.4 --lat 39.9")
        return 1
    
    try:
        print(f"🔄 获取天气数据: {args.location} ({args.lng}, {args.lat})")
        
        # 获取天气数据
        result = fetch_weather(args.token, args.lng, args.lat)
        
        # 解析数据
        data = parse_weather_data(result)
        
        # 格式化消息
        msg = format_message(data, args.location)
        
        if args.dry_run:
            print(msg)
        else:
            # 发送消息
            send_message(msg, args.channel)
        
        return 0
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
