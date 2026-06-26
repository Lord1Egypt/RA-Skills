#!/usr/bin/env python3
"""
Data source adapters for ENSO Tracker.
Fetches data from NOAA, OpenWeatherMap, and Berkeley Earth.
"""

import os
import json
import time
import urllib.request
import urllib.error
from typing import Optional, Dict, List, Any
from pathlib import Path

import pandas as pd
import numpy as np


# Constants
SKILL_DIR = Path(__file__).parent.expanduser().absolute()
CONFIG_PATH = SKILL_DIR / "config.json"
ONI_URL = "https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt"
OPENWEATHER_CURRENT_URL = "https://api.openweathermap.org/data/2.5/weather"
BERKELEY_BASE_URL = "http://berkeleyearth.org/data"


def load_config() -> Optional[Dict[str, str]]:
    """
    Load configuration from config.json.

    Returns:
        Dict with config values, or None if not configured.
    """
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            config = json.load(f)
            return config
    except FileNotFoundError:
        print("\n⚠️  OpenWeatherMap API 密钥未配置")
        print("请按照以下步骤设置：")
        print("1. 访问 https://openweathermap.org/api 注册账户")
        print("2. 在 API Keys 页面获取密钥")
        print(f"3. 创建文件 {CONFIG_PATH}")
        print('   内容：{"openweather_api_key": "YOUR_API_KEY_HERE"}')
        return None
    except json.JSONDecodeError as e:
        print(f"❌ 配置文件 JSON 格式错误: {e}")
        return None


def fetch_oni_data() -> pd.DataFrame:
    """
    Download and parse NOAA ONI ASCII text file.

    Returns:
        pandas DataFrame with columns: year, season, oni_value
    """
    try:
        print("📊 正在获取 NOAA ONI 数据...")
        req = urllib.request.Request(
            ONI_URL,
            headers={'User-Agent': 'OpenClaw-ENSO-Tracker/1.0'}
        )

        with urllib.request.urlopen(req, timeout=30) as response:
            data = response.read().decode('utf-8')

        # Parse ONI ASCII format
        # Format: SEAS  YR   TOTAL   ANOM
        # e.g.:   DJF 1950  24.72  -1.53
        lines = data.strip().split('\n')
        records = []

        for line in lines:
            parts = line.split()
            if len(parts) >= 4:
                try:
                    season = parts[0]  # SEAS
                    year = int(parts[1])  # YR
                    oni_value = float(parts[3])  # ANOM
                    records.append({
                        'year': year,
                        'season': season,
                        'oni_value': oni_value
                    })
                except (ValueError, IndexError):
                    continue

        df = pd.DataFrame(records)
        print(f"✅ 成功获取 {len(df)} 条 ONI 记录")
        return df

    except urllib.error.URLError as e:
        print(f"❌ 网络请求失败: {e}")
        return pd.DataFrame(columns=['year', 'season', 'oni_value'])
    except Exception as e:
        print(f"❌ 解析 ONI 数据失败: {e}")
        return pd.DataFrame(columns=['year', 'season', 'oni_value'])


def fetch_city_temperature(
    city_name: str,
    api_key: str,
    units: str = 'metric'
) -> Optional[Dict[str, Any]]:
    """
    Query OpenWeatherMap current weather API for a single city.

    Args:
        city_name: Name of the city (e.g., "Delhi", "Tokyo")
        api_key: OpenWeatherMap API key
        units: Temperature units ('metric' for Celsius, 'imperial' for Fahrenheit)

    Returns:
        Dict with temp, feels_like, humidity, etc., or None on failure.
    """
    try:
        url = f"{OPENWEATHER_CURRENT_URL}?q={urllib.parse.quote(city_name)}&appid={api_key}&units={units}"
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'OpenClaw-ENSO-Tracker/1.0'}
        )

        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode('utf-8'))

        return {
            'city': data.get('name', city_name),
            'country': data.get('sys', {}).get('country', 'Unknown'),
            'temp': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'temp_min': data['main']['temp_min'],
            'temp_max': data['main']['temp_max'],
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'description': data['weather'][0]['description'] if data.get('weather') else 'Unknown',
            'lat': data.get('coord', {}).get('lat', 0),
            'lon': data.get('coord', {}).get('lon', 0),
            'timestamp': data.get('dt', 0)
        }

    except urllib.error.HTTPError as e:
        if e.code == 401:
            print(f"❌ API 密钥无效或未激活")
        elif e.code == 404:
            print(f"❌ 未找到城市: {city_name}")
        else:
            print(f"❌ HTTP 错误 {e.code}: {city_name}")
        return None
    except urllib.error.URLError as e:
        print(f"❌ 网络错误 ({city_name}): {e}")
        return None
    except Exception as e:
        print(f"❌ 解析数据失败 ({city_name}): {e}")
        return None


def fetch_city_temperatures(
    cities_list: List[str],
    api_key: str,
    units: str = 'metric',
    rate_limit_delay: float = 1.0
) -> List[Dict[str, Any]]:
    """
    Batch fetch temperatures for multiple cities with rate limiting.

    Args:
        cities_list: List of city names
        api_key: OpenWeatherMap API key
        units: Temperature units
        rate_limit_delay: Delay between requests in seconds (default 1.0 for free tier)

    Returns:
        List of city temperature data dicts
    """
    results = []

    print(f"🌡️  正在获取 {len(cities_list)} 个城市的温度数据...")

    for i, city in enumerate(cities_list):
        print(f"   [{i+1}/{len(cities_list)}] {city}...", end=' ')

        data = fetch_city_temperature(city, api_key, units)
        if data:
            results.append(data)
            print(f"✅ {data['temp']}°C")
        else:
            print("❌")

        # Rate limiting for free tier
        if i < len(cities_list) - 1:
            time.sleep(rate_limit_delay)

    print(f"\n✅ 成功获取 {len(results)}/{len(cities_list)} 个城市的数据")
    return results


def fetch_berkeley_earth_anomaly(
    region: str = "India"
) -> Optional[pd.DataFrame]:
    """
    Download and parse Berkeley Earth regional temperature anomaly data.

    Args:
        region: Region name (e.g., "India", "Global")

    Returns:
        pandas DataFrame with temperature anomaly data, or None on failure.
    """
    # Berkeley Earth URL patterns vary by region
    # For India, typical URL pattern:
    region_lower = region.lower().replace(' ', '-')
    url = f"http://berkeleyearth.lbl.gov/regions/{region_lower}.txt"

    try:
        print(f"📊 正在获取 Berkeley Earth {region} 温度异常数据...")
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'OpenClaw-ENSO-Tracker/1.0'}
        )

        with urllib.request.urlopen(req, timeout=10) as response:
            data = response.read().decode('utf-8')

        # Parse Berkeley Earth format
        # Typically: Year Month Anomaly Uncertainty
        lines = data.strip().split('\n')
        records = []

        for line in lines:
            # Skip comment lines
            if line.startswith('%'):
                continue

            parts = line.split()
            if len(parts) >= 3:
                try:
                    year = int(parts[0])
                    month = int(parts[1])
                    anomaly = float(parts[2])
                    records.append({
                        'year': year,
                        'month': month,
                        'anomaly': anomaly
                    })
                except (ValueError, IndexError):
                    continue

        df = pd.DataFrame(records)
        print(f"✅ 成功获取 {len(df)} 条温度异常记录")
        return df

    except urllib.error.URLError as e:
        print(f"❌ 网络请求失败: {e}")
        return None
    except Exception as e:
        print(f"❌ 解析 Berkeley Earth 数据失败: {e}")
        return None


def get_current_enso_phase(oni_value: float) -> Dict[str, str]:
    """
    Classify ENSO phase based on ONI value.

    Args:
        oni_value: Current ONI index value

    Returns:
        Dict with phase name and intensity in Chinese
    """
    if oni_value >= 2.0:
        return {'phase': '强厄尔尼诺', 'phase_en': 'Strong El Niño', 'intensity': '强'}
    elif oni_value >= 1.5:
        return {'phase': '厄尔尼诺', 'phase_en': 'El Niño', 'intensity': '中强'}
    elif oni_value >= 1.0:
        return {'phase': '厄尔尼诺', 'phase_en': 'El Niño', 'intensity': '中等'}
    elif oni_value >= 0.5:
        return {'phase': '弱厄尔尼诺', 'phase_en': 'Weak El Niño', 'intensity': '弱'}
    elif oni_value <= -2.0:
        return {'phase': '强拉尼娜', 'phase_en': 'Strong La Niña', 'intensity': '强'}
    elif oni_value <= -1.5:
        return {'phase': '拉尼娜', 'phase_en': 'La Niña', 'intensity': '中强'}
    elif oni_value <= -1.0:
        return {'phase': '拉尼娜', 'phase_en': 'La Niña', 'intensity': '中等'}
    elif oni_value <= -0.5:
        return {'phase': '弱拉尼娜', 'phase_en': 'Weak La Niña', 'intensity': '弱'}
    else:
        return {'phase': '中性', 'phase_en': 'Neutral', 'intensity': '-'}


# Major world cities for global temperature tracking
DEFAULT_CITIES = [
    "Delhi", "Mumbai", "Chennai", "Kolkata",  # India
    "Karachi", "Lahore", "Islamabad",  # Pakistan
    "Dhaka",  # Bangladesh
    "Bangkok",  # Thailand
    "Dubai", "Abu Dhabi",  # UAE
    "Riyadh", "Jeddah",  # Saudi Arabia
    "Cairo",  # Egypt
    "Phoenix", "Las Vegas", "Death Valley",  # USA
    "Mexico City",  # Mexico
    "São Paulo", "Rio de Janeiro",  # Brazil
    "Sydney", "Melbourne",  # Australia
    "Tokyo", "Osaka",  # Japan
    "Beijing", "Shanghai", "Guangzhou",  # China
    "Seoul",  # South Korea
    "Singapore",  # Singapore
    "Jakarta",  # Indonesia
    "Manila",  # Philippines
    "Tehran",  # Iran
    "Baghdad",  # Iraq
    "Moscow",  # Russia
    "Paris", "London", "Berlin",  # Europe
]


if __name__ == "__main__":
    # Test ONI data fetch
    print("Testing ONI data fetch...")
    oni_df = fetch_oni_data()
    if not oni_df.empty:
        print(f"Latest ONI: {oni_df.iloc[-1]['oni_value']} ({oni_df.iloc[-1]['season']} {oni_df.iloc[-1]['year']})")

    # Test config loading
    print("\nTesting config loading...")
    config = load_config()
    if config:
        print(f"API Key configured: {config.get('openweather_api_key', '')[:8]}...")
    else:
        print("No config found - see setup instructions above")