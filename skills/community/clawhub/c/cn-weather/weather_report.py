#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
天气报告脚本 - 参考飞翔天气等开源项目设计
支持多种天气 API 数据源（和风天气、Open-Meteo 等）
可配置城市列表，支持邮件/Telegram 推送

灵感来源：
- 飞翔天气 (Feixiang Weather) - 简洁的天气预报
- 和风天气官方示例
- Open-Meteo 开源实现

🔐 安全说明：
- 所有敏感配置从 TOOLS.md 读取
- 本脚本不包含任何硬编码密钥
- TOOLS.md 应加入 .gitignore
"""

import sys
import io
import re
from pathlib import Path
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import requests

# ==================== 从 TOOLS.md 加载配置 ====================

def load_tools_config():
    """从 TOOLS.md 加载敏感配置"""
    workspace_root = Path(__file__).parent.parent.parent
    tools_path = workspace_root / "TOOLS.md"
    
    config = {
        "qweather_api_key": "",
        "qweather_enabled": False,
        "email_sender": "",
        "email_password": "",
        "email_smtp_server": "smtp.qq.com",
        "email_smtp_port": 465,
    }
    
    if not tools_path.exists():
        print("⚠️  警告：TOOLS.md 不存在，使用默认配置")
        return config
    
    content = tools_path.read_text(encoding='utf-8')
    
    # 提取和风天气 API Key
    match = re.search(r'### Weather API.*?- \*\*API Key\*\*: `([^`]+)`', content, re.DOTALL)
    if match:
        config["qweather_api_key"] = match.group(1).strip()
        config["qweather_enabled"] = True
        print("✅ 已加载和风天气 API Key")
    
    # 提取邮箱配置
    match = re.search(r'### Email.*?- \*\*发件人\*\*: ([^\n]+)', content, re.DOTALL)
    if match:
        config["email_sender"] = match.group(1).strip()
    
    match = re.search(r'- \*\*授权码\*\*: ([^\n]+)', content)
    if match:
        config["email_password"] = match.group(1).strip()
    
    if config["email_sender"] and config["email_password"]:
        print("✅ 已加载邮箱配置")
    
    return config

# 加载配置
TOOLS_CONFIG = load_tools_config()

# ==================== 配置区域 ====================

# 城市配置
CITIES = [
    {"name": "赣榆区", "lat": 34.83, "lon": 119.12, "qweather_id": "101190801"},
    {"name": "宿迁宿豫区", "lat": 33.95, "lon": 118.33, "qweather_id": "101191301"},
]

# 默认收件人
DEFAULT_RECIPIENT = "3282510774@qq.com"

# ==================== 天气代码转换 ====================

OPEN_METEO_CONDITIONS = {
    0: ("☀️", "晴朗"),
    1: ("🌤️", "主要晴朗"),
    2: ("⛅", "多云"),
    3: ("☁️", "阴天"),
    45: ("🌫️", "雾"),
    48: ("🌫️", "雾凇"),
    51: ("🌦️", "毛毛雨"),
    53: ("🌦️", "毛毛雨"),
    55: ("🌦️", "毛毛雨"),
    61: ("🌧️", "小雨"),
    63: ("🌧️", "中雨"),
    65: ("🌧️", "大雨"),
    66: ("🌧️", "冻雨"),
    67: ("🌧️", "冻雨"),
    71: ("🌨️", "小雪"),
    73: ("🌨️", "中雪"),
    75: ("🌨️", "大雪"),
    77: ("🌨️", "冰粒"),
    80: ("🌦️", "阵雨"),
    81: ("🌧️", "中阵雨"),
    82: ("⛈️", "强阵雨"),
    85: ("🌨️", "阵雪"),
    86: ("🌨️", "大阵雪"),
    95: ("⛈️", "雷雨"),
    96: ("⛈️", "雷阵雨"),
    99: ("⛈️", "强雷阵雨"),
}

QWEATHER_CONDITIONS = {
    "100": ("☀️", "晴"),
    "101": ("☁️", "多云"),
    "102": ("⛅", "少云"),
    "103": ("🌤️", "晴间多云"),
    "104": ("☁️", "阴"),
    "150": ("🌙", "晴（夜）"),
    "151": ("☁️", "多云（夜）"),
    "152": ("⛅", "少云（夜）"),
    "153": ("🌤️", "晴间多云（夜）"),
    "300": ("🌦️", "阵雨"),
    "301": ("🌧️", "强阵雨"),
    "302": ("⛈️", "雷阵雨"),
    "303": ("⛈️", "强雷阵雨"),
    "304": ("⛈️", "雷阵雨伴冰雹"),
    "305": ("🌧️", "小雨"),
    "306": ("🌧️", "中雨"),
    "307": ("🌧️", "大雨"),
    "308": ("🌧️", "极端降雨"),
    "309": ("🌦️", "毛毛雨/细雨"),
    "310": ("🌧️", "暴雨"),
    "311": ("🌧️", "大暴雨"),
    "312": ("🌧️", "特大暴雨"),
    "313": ("🌨️", "冻雨"),
    "314": ("🌧️", "小到中雨"),
    "315": ("🌧️", "中到大雨"),
    "316": ("🌧️", "大到暴雨"),
    "317": ("🌧️", "暴雨到大暴雨"),
    "318": ("🌧️", "大暴雨到特大暴雨"),
    "350": ("🌦️", "阵雨（夜）"),
    "351": ("🌧️", "强阵雨（夜）"),
    "399": ("🌧️", "雨"),
    "400": ("🌨️", "小雪"),
    "401": ("🌨️", "中雪"),
    "402": ("🌨️", "大雪"),
    "403": ("🌨️", "暴雪"),
    "404": ("🌨️", "雨夹雪"),
    "405": ("🌨️", "雨雪天气"),
    "406": ("🌨️", "阵雨夹雪"),
    "407": ("🌨️", "阵雪"),
    "408": ("🌨️", "小到中雪"),
    "409": ("🌨️", "中到大雪"),
    "410": ("🌨️", "大到暴雪"),
    "456": ("🌨️", "阵雨夹雪（夜）"),
    "457": ("🌨️", "阵雪（夜）"),
    "499": ("🌨️", "雪"),
    "500": ("🌫️", "薄雾"),
    "501": ("🌫️", "雾"),
    "502": ("😷", "霾"),
    "503": ("💨", "扬沙"),
    "504": ("💨", "浮尘"),
    "507": ("💨", "沙尘暴"),
    "508": ("💨", "强沙尘暴"),
    "509": ("🌫️", "浓雾"),
    "510": ("🌫️", "强浓雾"),
    "511": ("😷", "中度霾"),
    "512": ("😷", "重度霾"),
    "513": ("😷", "严重霾"),
    "514": ("🌫️", "大雾"),
    "515": ("🌫️", "特强浓雾"),
    "900": ("🥵", "热"),
    "901": ("🥶", "冷"),
    "999": ("❓", "未知"),
}

# ==================== 数据获取 ====================

class OpenMeteoAPI:
    """Open-Meteo API（免费，无需 Key）"""
    
    def get_weather(self, city):
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": city["lat"],
            "longitude": city["lon"],
            "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m,wind_direction_10m",
            "daily": "temperature_2m_max,temperature_2m_min,weather_code",
            "timezone": "Asia/Shanghai",
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            current = data.get("current", {})
            daily = data.get("daily", {})
            
            wmo_code = current.get("weather_code", -1)
            icon, condition = OPEN_METEO_CONDITIONS.get(wmo_code, ("❓", "未知"))
            
            forecast = []
            for i in range(min(3, len(daily.get("time", [])))):
                date = daily["time"][i]
                code = daily["weather_code"][i] if i < len(daily.get("weather_code", [])) else -1
                t_max = daily["temperature_2m_max"][i] if i < len(daily.get("temperature_2m_max", [])) else "N/A"
                t_min = daily["temperature_2m_min"][i] if i < len(daily.get("temperature_2m_min", [])) else "N/A"
                f_icon, f_cond = OPEN_METEO_CONDITIONS.get(code, ("❓", "未知"))
                forecast.append({
                    "date": date,
                    "icon": f_icon,
                    "condition": f_cond,
                    "temp_max": t_max,
                    "temp_min": t_min,
                })
            
            return {
                "source": "Open-Meteo",
                "name": city["name"],
                "temp": current.get("temperature_2m", "N/A"),
                "feels_like": "N/A",
                "humidity": current.get("relative_humidity_2m", "N/A"),
                "icon": icon,
                "condition": condition,
                "wind_speed": current.get("wind_speed_10m", "N/A"),
                "wind_dir": current.get("wind_direction_10m", "N/A"),
                "forecast": forecast,
                "update_time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            }
        except Exception as e:
            print(f"❌ Open-Meteo API 错误 ({city['name']}): {e}")
            return None

class QWeatherAPI:
    """和风天气 API（需要 API Key）"""
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://devapi.qweather.com/v7"
    
    def get_weather(self, city):
        if not self.api_key:
            return None
        
        location_id = city.get("qweather_id")
        if not location_id:
            print(f"⚠️  城市 {city['name']} 缺少和风天气 ID")
            return None
        
        try:
            url = f"{self.base_url}/weather/now?location={location_id}&key={self.api_key}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get("code") != "200":
                print(f"❌ 和风天气 API 错误：{data.get('msg', 'Unknown')}")
                return None
            
            now = data.get("now", {})
            code = now.get("icon", "999")
            icon, condition = QWEATHER_CONDITIONS.get(code, ("❓", "未知"))
            
            forecast_url = f"{self.base_url}/weather/3d?location={location_id}&key={self.api_key}"
            forecast_resp = requests.get(forecast_url, timeout=10)
            forecast_data = forecast_resp.json().get("daily", [])
            
            forecast = []
            for day in forecast_data[:3]:
                f_code = day.get("iconDay", "999")
                f_icon, f_cond = QWEATHER_CONDITIONS.get(f_code, ("❓", "未知"))
                forecast.append({
                    "date": day.get("fxDate", "N/A"),
                    "icon": f_icon,
                    "condition": f_cond,
                    "temp_max": day.get("tempMax", "N/A"),
                    "temp_min": day.get("tempMin", "N/A"),
                })
            
            return {
                "source": "和风天气",
                "name": city["name"],
                "temp": now.get("temp", "N/A"),
                "feels_like": now.get("feelsLike", "N/A"),
                "humidity": now.get("humidity", "N/A"),
                "icon": icon,
                "condition": condition,
                "wind_speed": now.get("windSpeed", "N/A"),
                "wind_dir": now.get("windDir", "N/A"),
                "pressure": now.get("pressure", "N/A"),
                "forecast": forecast,
                "update_time": now.get("obsTime", datetime.now().strftime("%Y-%m-%d %H:%M")),
            }
        except Exception as e:
            print(f"❌ 和风天气 API 错误 ({city['name']}): {e}")
            return None

# ==================== 报告生成 ====================

def generate_report(cities_data, date_str):
    lines = [
        "═══════════════════════════════════════",
        "🌤️  每日天气报告",
        f"📅 {date_str}",
        "═══════════════════════════════════════",
        "",
    ]
    
    for city_data in cities_data:
        if not city_data:
            continue
        
        lines.append(f"{city_data['icon']} {city_data['name']} ({city_data['source']})")
        lines.append(f"   更新：{city_data['update_time']}")
        lines.append(f"   温度：{city_data['temp']}°C" + (f" (体感 {city_data['feels_like']}°C)" if city_data['feels_like'] != "N/A" else ""))
        lines.append(f"   天气：{city_data['condition']}")
        lines.append(f"   湿度：{city_data['humidity']}%")
        lines.append(f"   风速：{city_data['wind_speed']} km/h {city_data.get('wind_dir', '')}")
        if city_data.get('pressure'):
            lines.append(f"   气压：{city_data['pressure']} hPa")
        
        if city_data.get('forecast'):
            lines.append("   预报：")
            for day in city_data['forecast']:
                lines.append(f"     {day['date']}: {day['temp_min']}~{day['temp_max']}°C {day['icon']}{day['condition']}")
        
        lines.append("")
    
    lines.extend([
        "═══════════════════════════════════════",
        "祝你有美好的一天！✨",
        "—— OpenClaw 自动发送",
        "═══════════════════════════════════════",
    ])
    
    return "\n".join(lines)

# ==================== 邮件发送 ====================

def send_email(recipient, subject, content):
    import smtplib
    from email.mime.text import MIMEText
    
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['From'] = TOOLS_CONFIG["email_sender"]
    msg['To'] = recipient
    msg['Subject'] = subject
    
    try:
        print(f"📧 正在发送邮件到 {recipient}...")
        server = smtplib.SMTP_SSL(TOOLS_CONFIG["email_smtp_server"], TOOLS_CONFIG["email_smtp_port"])
        server.login(TOOLS_CONFIG["email_sender"], TOOLS_CONFIG["email_password"])
        server.sendmail(TOOLS_CONFIG["email_sender"], [recipient, TOOLS_CONFIG["email_sender"]], msg.as_string())
        server.quit()
        print("✅ 邮件发送成功！")
        return True
    except Exception as e:
        print(f"❌ 邮件发送失败：{e}")
        return False

# ==================== 主函数 ====================

def main(recipient=None):
    from datetime import datetime
    
    if recipient is None:
        recipient = DEFAULT_RECIPIENT
    
    # 选择 API（优先和风天气，失败自动降级）
    use_qweather = TOOLS_CONFIG["qweather_enabled"] and TOOLS_CONFIG["qweather_api_key"]
    api = None
    
    if use_qweather:
        print("🌤️  尝试使用和風天气 API...")
        api = QWeatherAPI(TOOLS_CONFIG["qweather_api_key"])
        
        # 测试第一个城市
        test_weather = api.get_weather(CITIES[0])
        if test_weather:
            cities_data.append(test_weather)
        else:
            print("⚠️  和风天气 API 不可用，降级到 Open-Meteo")
            use_qweather = False
            api = OpenMeteoAPI()
    
    if not use_qweather:
        print("🌤️  使用 Open-Meteo API (免费)")
        api = OpenMeteoAPI()
        cities_data = []
    
    # 获取所有城市天气
    for city in CITIES:
        print(f"📍 获取 {city['name']} 天气...")
        weather = api.get_weather(city)
        if weather:
            cities_data.append(weather)
        else:
            print(f"⚠️  {city['name']} 天气获取失败")
    
    if not cities_data:
        print("❌ 所有城市天气获取失败，终止发送")
        return
    
    # 生成报告
    now = datetime.now()
    date_str = now.strftime("%Y 年 %m 月 %d 日 %A")
    report = generate_report(cities_data, date_str)
    
    # 打印报告
    print("\n" + report)
    
    # 发送邮件
    subject = f"每日天气报告 - {date_str}"
    send_email(recipient, subject, report)

if __name__ == "__main__":
    recipient = sys.argv[1] if len(sys.argv) > 1 else None
    main(recipient)
