#!/usr/bin/env python3
"""中国天气查询脚本 - 基于中国天气网API
用法: python3 weather_query.py <城市名> [--days N] [--detail]
"""

import json
import os
import sys
import re
import urllib.request
import urllib.error

CITIES_FILE = None  # 由调用方注入，或自动查找

def load_cities():
    """加载城市编码表"""
    global CITIES_FILE
    # 基于脚本所在目录推导 skill 根目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    skill_dir = os.path.dirname(script_dir)  # scripts/ -> skill root
    search_paths = [
        os.path.join(skill_dir, 'references', 'cities.json'),
        "/root/.openclaw/workspace/skills/china-weather-query/references/cities.json",
        "/root/.openclaw/workspace/skills/china-weather/references/cities.json",
        "/root/.openclaw/workspace/china_weather_cities.json",
    ]
    if CITIES_FILE:
        search_paths.insert(0, CITIES_FILE)
    for path in search_paths:
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except:
            pass
    return None

def search_city(name):
    """搜索城市，返回编码"""
    cities = load_cities()
    if not cities:
        return None, None
    # 精确匹配
    for c in cities:
        if c['city'] == name:
            return c['code'], c['prov']
    # 模糊匹配
    for c in cities:
        if name in c['city'] or name in c['prov']:
            return c['code'], c['prov']
    return None, None

def fetch_weather(code):
    """从中国天气网获取天气数据"""
    url = f"http://d1.weather.com.cn/weather_index/{code}.html"
    req = urllib.request.Request(url)
    req.add_header('Referer', 'http://www.weather.com.cn/')
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = resp.read().decode('utf-8')
        return parse_weather(data)
    except Exception as e:
        return {"error": str(e)}

def parse_weather(data):
    """解析天气数据"""
    result = {}

    # 实况 dataSK
    m = re.search(r'var dataSK\s*=\s*(\{[^;]+)', data)
    if m:
        try:
            sk = json.loads(m.group(1))
            result['current'] = {
                'city': sk.get('cityname', ''),
                'temp': sk.get('temp', ''),
                'weather': sk.get('weather', ''),
                'weather_en': sk.get('weathere', ''),
                'wind_dir': sk.get('WD', ''),
                'wind_speed': sk.get('WS', ''),
                'humidity': sk.get('sd', ''),
                'aqi': sk.get('aqi', ''),
                'pm25': sk.get('aqi_pm25', ''),
                'visibility': sk.get('njd', ''),
                'pressure': sk.get('qy', ''),
                'rain': sk.get('rain', ''),
                'rain_24h': sk.get('rain24h', ''),
                'time': sk.get('time', ''),
                'date': sk.get('date', ''),
            }
        except:
            pass

    # 今日预报 cityDZ
    m = re.search(r'var cityDZ\s*=\s*(\{[^;]+)', data)
    if m:
        try:
            dz = json.loads(m.group(1))['weatherinfo']
            result['today'] = {
                'city': dz.get('cityname', ''),
                'temp_high': dz.get('temp', ''),
                'temp_low': dz.get('tempn', ''),
                'weather': dz.get('weather', ''),
                'wind': dz.get('wd', ''),
                'wind_level': dz.get('ws', ''),
            }
        except:
            pass

    # 5天预报 fc
    m = re.search(r'var fc\s*=\s*(\{[^;]+)', data)
    if m:
        try:
            fc = json.loads(m.group(1))
            forecasts = []
            for day in fc.get('f', []):
                forecasts.append({
                    'date': day.get('fi', ''),
                    'day_label': day.get('fj', ''),
                    'weather_day': weather_code_to_text(day.get('fa', '')),
                    'weather_night': weather_code_to_text(day.get('fb', '')),
                    'temp_high': day.get('fc', ''),
                    'temp_low': day.get('fd', ''),
                    'wind_day': day.get('fe', ''),
                    'wind_night': day.get('ff', ''),
                    'wind_level_day': day.get('fg', ''),
                    'wind_level_night': day.get('fh', ''),
                })
            result['forecast'] = forecasts
        except:
            pass

    # 生活指数 dataZS — 数据是扁平结构，key 格式为 {prefix}_name/{prefix}_hint/{prefix}_des_s
    m = re.search(r'var dataZS\s*=\s*(\{[^;]+)', data)
    if m:
        try:
            zs_outer = json.loads(m.group(1))
            zs_data = zs_outer.get('zs', zs_outer)  # 数据在 .zs 子对象里
            indices = {}
            index_names = {
                'ct': '穿衣', 'uv': '紫外线', 'ys': '雨伞', 'xc': '洗车',
                'gm': '感冒', 'tr': '旅游', 'yd': '运动', 'ac': '空调',
                'co': '舒适度', 'ls': '晾晒', 'xq': '心情', 'pj': '啤酒',
                'jt': '交通', 'yh': '约会', 'gl': '太阳镜', 'ag': '过敏',
                'lk': '路况', 'cl': '晨练', 'nl': '夜生活',
                'gj': '逛街', 'pl': '空气污染扩散', 'fs': '防晒',
                'pp': '化妆', 'gz': '干燥',
            }
            for k, name in index_names.items():
                if f'{k}_name' in zs_data:
                    indices[name] = {
                        'hint': zs_data.get(f'{k}_hint', ''),
                        'desc': zs_data.get(f'{k}_des_s', ''),
                    }
            result['indices'] = indices
        except:
            pass

    # 预警 alarmDZ
    m = re.search(r'var alarmDZ\s*=\s*(\{[^;]+)', data)
    if m:
        try:
            alarm = json.loads(m.group(1))
            if alarm.get('w'):
                result['alarms'] = alarm['w']
        except:
            pass

    return result

def weather_code_to_text(code):
    """天气代码转文字"""
    codes = {
        '00': '晴', '01': '多云', '02': '阴', '03': '阵雨',
        '04': '雷阵雨', '05': '雷阵雨并伴有冰雹', '06': '雨夹雪',
        '07': '小雨', '08': '中雨', '09': '大雨', '10': '暴雨',
        '11': '大暴雨', '12': '特大暴雨', '13': '阵雪', '14': '小雪',
        '15': '中雪', '16': '大雪', '17': '暴雪', '18': '雾',
        '19': '冻雨', '20': '沙尘暴', '21': '小到中雨', '22': '中到大雨',
        '23': '大到暴雨', '24': '暴雨到大暴雨', '25': '大暴雨到特大暴雨',
        '26': '小到中雪', '27': '中到大雪', '28': '大到暴雪',
        '29': '浮尘', '30': '扬沙', '31': '强沙尘暴', '53': '霾',
        '99': '无',
    }
    return codes.get(code, '未知')

def format_output(data, days=1, detail=False):
    """格式化输出"""
    lines = []

    if 'error' in data:
        lines.append(f"❌ 查询失败: {data['error']}")
        return '\n'.join(lines)

    # 实况
    if 'current' in data:
        cur = data['current']
        lines.append(f"📍 {cur['city']} · {cur['date']} {cur['time']}")
        lines.append(f"🌡️ 实时气温: {cur['temp']}°C | {cur['weather']}")
        lines.append(f"💨 {cur['wind_dir']} {cur['wind_speed']} | 湿度 {cur['humidity']}")
        if cur.get('aqi') and cur['aqi'] != '':
            aqi = int(cur['aqi'])
            if aqi <= 50: aqi_label = '优 ✅'
            elif aqi <= 100: aqi_label = '良 🟡'
            elif aqi <= 150: aqi_label = '轻度污染 🟠'
            elif aqi <= 200: aqi_label = '中度污染 🔴'
            else: aqi_label = '重度污染 🟤'
            lines.append(f"📊 AQI: {aqi} ({aqi_label}) | PM2.5: {cur['pm25']}")
        if cur.get('visibility'):
            vis = cur.get('visibility', '').replace('km','')
            lines.append(f"👁️ 能见度: {vis}km | 气压: {cur['pressure']}hPa")

    # 预报
    if 'forecast' in data:
        fc = data['forecast'][:days]
        lines.append(f"\n📅 未来{len(fc)}天预报:")
        for day in fc:
            lines.append(f"\n  📆 {day['day_label']} ({day['date']})")
            lines.append(f"  🌤️ {day['weather_day']} 转 {day['weather_night']}")
            lines.append(f"  🌡️ {day['temp_high']}°C / {day['temp_low']}°C")
            lines.append(f"  💨 {day['wind_day']} {day['wind_level_day']}")

    # 生活指数
    if detail and 'indices' in data:
        lines.append(f"\n📋 生活指数:")
        for name, info in data['indices'].items():
            lines.append(f"  {name}: {info['hint']} — {info['desc']}")

    # 预警
    if 'alarms' in data and data['alarms']:
        lines.append(f"\n⚠️ 天气预警:")
        for alarm in data['alarms']:
            w_type = alarm.get('w5', '')
            w_level = alarm.get('w7', '')
            w_time = alarm.get('w8', '')
            w_title = alarm.get('w13', '')
            lines.append(f"  [{w_type}{w_level}预警] {w_title} ({w_time})")

    return '\n'.join(lines)

def main():
    if len(sys.argv) < 2:
        print("用法: python3 weather_query.py <城市名> [--days N] [--detail] [--json]")
        print("示例: python3 weather_query.py 上海")
        print("      python3 weather_query.py 北京 --days 3 --detail")
        print("      python3 weather_query.py 杭州 --json")
        sys.exit(1)

    city_name = sys.argv[1]
    days = 1
    detail = False
    json_output = False

    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == '--days' and i + 1 < len(sys.argv):
            days = int(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == '--detail':
            detail = True
            i += 1
        elif sys.argv[i] == '--json':
            json_output = True
            i += 1
        else:
            i += 1

    # 搜索城市
    code, prov = search_city(city_name)
    if not code:
        # 尝试直接用输入作为编码
        if re.match(r'^\d{9}$', city_name):
            code = city_name
        else:
            print(f"❌ 未找到城市: {city_name}")
            sys.exit(1)

    if prov:
        print(f"🔍 匹配到: {prov} - {city_name if city_name != prov else ''}", file=sys.stderr)

    # 查询天气
    data = fetch_weather(code)

    if json_output:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(format_output(data, days=days, detail=detail))

if __name__ == '__main__':
    main()
