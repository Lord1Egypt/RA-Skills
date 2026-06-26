#!/usr/bin/env python3
"""
天气查询脚本
使用 wttr.in 或 Open-Meteo API 查询目的地天气预报
"""

import sys
import json
import argparse
import urllib.request
import urllib.error
from datetime import datetime, timedelta

# 城市坐标对照表（Open-Meteo API 使用）
CITY_COORDINATES = {
    "北京": {"lat": 39.9042, "lon": 116.4074},
    "上海": {"lat": 31.2304, "lon": 121.4737},
    "广州": {"lat": 23.1291, "lon": 113.2644},
    "深圳": {"lat": 22.5431, "lon": 114.0579},
    "杭州": {"lat": 30.2741, "lon": 120.1551},
    "成都": {"lat": 30.5728, "lon": 104.0668},
    "西安": {"lat": 34.3416, "lon": 108.9398},
    "南京": {"lat": 32.0603, "lon": 118.7969},
    "三亚": {"lat": 18.2528, "lon": 109.5122},
    "重庆": {"lat": 29.4316, "lon": 106.9123},
    "苏州": {"lat": 31.2989, "lon": 120.5853},
    "武汉": {"lat": 30.5928, "lon": 114.3055},
    "天津": {"lat": 39.0842, "lon": 117.2009},
    "青岛": {"lat": 36.0671, "lon": 120.3826},
    "厦门": {"lat": 24.4798, "lon": 118.0894},
}

# 天气代码对照表（Open-Meteo WMO代码）
WEATHER_CODES = {
    0: "晴",
    1: "晴",
    2: "多云",
    3: "阴",
    45: "雾",
    48: "雾",
    51: "小雨",
    53: "小雨",
    55: "中雨",
    61: "小雨",
    63: "中雨",
    65: "大雨",
    71: "小雪",
    73: "中雪",
    75: "大雪",
    80: "阵雨",
    81: "阵雨",
    82: "暴雨",
    95: "雷阵雨",
    96: "雷阵雨",
    99: "雷阵雨",
}


def query_weather_wttr(city, days=4, timeout=10):
    """
    使用 wttr.in API 查询天气
    
    Args:
        city: 城市名（中文或英文）
        days: 查询天数
        timeout: 超时时间（秒）
    
    Returns:
        dict: 天气数据
    """
    try:
        url = f"https://wttr.in/{city}?format=j1"
        req = urllib.request.Request(url, headers={'User-Agent': 'curl'})
        
        with urllib.request.urlopen(req, timeout=timeout) as response:
            data = json.loads(response.read().decode('utf-8'))
        
        # 解析天气数据
        weather_list = []
        for i, day in enumerate(data.get('weather', [])[:days]):
            weather_list.append({
                'date': day.get('date'),
                'weather': day.get('hourly', [{}])[0].get('weatherDesc', [{}])[0].get('value', '未知'),
                'max_temp': day.get('maxtempC'),
                'min_temp': day.get('mintempC'),
                'avg_temp': day.get('avgtempC'),
                'rain_chance': day.get('hourly', [{}])[0].get('chanceofrain', '0'),
            })
        
        return {
            'success': True,
            'source': 'wttr.in',
            'data': weather_list
        }
    
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def query_weather_openmeteo(city, start_date, end_date, timeout=10):
    """
    使用 Open-Meteo API 查询天气
    
    Args:
        city: 城市名（中文）
        start_date: 开始日期 (YYYY-MM-DD)
        end_date: 结束日期 (YYYY-MM-DD)
        timeout: 超时时间（秒）
    
    Returns:
        dict: 天气数据
    """
    if city not in CITY_COORDINATES:
        return {
            'success': False,
            'error': f'城市 {city} 不在坐标表中'
        }
    
    coords = CITY_COORDINATES[city]
    
    try:
        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={coords['lat']}"
            f"&longitude={coords['lon']}"
            f"&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max"
            f"&timezone=Asia/Shanghai"
            f"&start_date={start_date}"
            f"&end_date={end_date}"
        )
        
        with urllib.request.urlopen(url, timeout=timeout) as response:
            data = json.loads(response.read().decode('utf-8'))
        
        # 解析天气数据
        daily = data.get('daily', {})
        weather_list = []
        
        dates = daily.get('time', [])
        weather_codes = daily.get('weather_code', [])
        max_temps = daily.get('temperature_2m_max', [])
        min_temps = daily.get('temperature_2m_min', [])
        rain_chances = daily.get('precipitation_probability_max', [])
        
        for i in range(len(dates)):
            weather_code = weather_codes[i] if i < len(weather_codes) else 0
            weather_list.append({
                'date': dates[i],
                'weather': WEATHER_CODES.get(weather_code, '未知'),
                'max_temp': str(int(max_temps[i])) if i < len(max_temps) else '未知',
                'min_temp': str(int(min_temps[i])) if i < len(min_temps) else '未知',
                'rain_chance': str(rain_chances[i]) if i < len(rain_chances) else '0',
            })
        
        return {
            'success': True,
            'source': 'Open-Meteo',
            'data': weather_list
        }
    
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def generate_weather_markdown(city, weather_data, season_feature=None):
    """
    生成 Markdown 格式的天气预报
    
    Args:
        city: 城市名
        weather_data: 天气数据（从 query_weather_* 返回）
        season_feature: 季节特点描述（可选）
    
    Returns:
        str: Markdown 格式的天气预报
    """
    if not weather_data.get('success'):
        return f"> ⚠️ 天气查询失败：{weather_data.get('error', '未知错误')}，天气信息基于气候数据估算。"
    
    data = weather_data.get('data', [])
    source = weather_data.get('source', '未知')
    
    # 生成 Markdown
    md = f"## 🌤️ 天气预报\n\n"
    
    if season_feature:
        md += f"**{city}天气特点：** {season_feature}\n\n"
    
    md += "| 日期 | 天气 | 温度 | 降雨概率 | 穿衣建议 |\n"
    md += "|------|------|------|----------|----------|\n"
    
    for day in data:
        date_str = day.get('date', '未知')
        # 简化日期显示
        if '-' in date_str:
            parts = date_str.split('-')
            date_str = f"{parts[1]}月{parts[2]}日"
        
        max_temp = day.get('max_temp', '未知')
        min_temp = day.get('min_temp', '未知')
        temp_range = f"{min_temp}-{max_temp}℃" if max_temp != '未知' else '未知'
        
        weather = day.get('weather', '未知')
        rain_chance = f"{day.get('rain_chance', '0')}%" if day.get('rain_chance') else '0%'
        
        # 根据温度生成穿衣建议
        try:
            max_t = int(max_temp) if max_temp != '未知' else 20
            if max_t >= 30:
                clothing = "夏装"
            elif max_t >= 20:
                clothing = "夏装+薄外套"
            elif max_t >= 10:
                clothing = "长袖+外套"
            else:
                clothing = "厚外套"
        except:
            clothing = "根据温度调整"
        
        md += f"| {date_str} | {weather} | {temp_range} | {rain_chance} | {clothing} |\n"
    
    md += f"\n**💡 温馨提示：**\n"
    md += f"- 数据来源：{source}\n"
    md += f"- 建议出行前再次查询实时天气\n"
    
    return md


def main():
    parser = argparse.ArgumentParser(description='查询目的地天气预报')
    parser.add_argument('--city', '-c', required=True, help='城市名')
    parser.add_argument('--start-date', '-s', help='开始日期 (YYYY-MM-DD)')
    parser.add_argument('--end-date', '-e', help='结束日期 (YYYY-MM-DD)')
    parser.add_argument('--days', '-d', type=int, default=4, help='查询天数')
    parser.add_argument('--format', '-f', choices=['json', 'markdown'], default='markdown', help='输出格式')
    parser.add_argument('--timeout', '-t', type=int, default=10, help='超时时间（秒）')
    
    args = parser.parse_args()
    
    # 设置默认日期
    if not args.start_date:
        args.start_date = datetime.now().strftime('%Y-%m-%d')
    if not args.end_date:
        args.end_date = (datetime.now() + timedelta(days=args.days-1)).strftime('%Y-%m-%d')
    
    # 优先使用 Open-Meteo API
    result = query_weather_openmeteo(args.city, args.start_date, args.end_date, args.timeout)
    
    # 如果 Open-Meteo 失败，尝试 wttr.in
    if not result.get('success'):
        result = query_weather_wttr(args.city, args.days, args.timeout)
    
    # 输出结果
    if args.format == 'json':
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(generate_weather_markdown(args.city, result))


if __name__ == '__main__':
    main()