#!/usr/bin/env python3
"""
获取天气信息
"""

import json
import urllib.request
from datetime import datetime
from typing import Dict, Optional


class WeatherFetcher:
    """天气信息获取器"""

    def __init__(self, location: str = '烟台'):
        self.location = location

    def get_weather_icon(self, weather: str) -> str:
        """获取天气图标"""
        weather_icons = {
            '晴': '☀️',
            '多云': '☁️',
            '阴': '☁️',
            '雨': '🌧️',
            '小雨': '🌦️',
            '中雨': '🌧️',
            '大雨': '⛈️',
            '暴雨': '⛈️',
            '雪': '❄️',
            '小雪': '🌨️',
            '大雪': '❄️',
            '风': '💨',
            '雾': '🌫️',
            '霾': '😷'
        }
        return weather_icons.get(weather, '🌡️')

    def fetch_weather_from_api(self) -> Optional[Dict]:
        """
        从API获取天气信息

        注意：实际使用时需要替换为真实的天气API
        这里使用示例数据
        """
        # 示例：使用和风天气API
        # 需要申请API Key
        # 这里提供模拟数据

        # 模拟数据
        mock_data = {
            'weather': '晴',
            'temperature': '15',
            'temperature_range': '10-20',
            'humidity': '60%',
            'wind': '东南风 3级',
            'location': self.location
        }

        return mock_data

    def get_weather(self, date: str = None) -> Dict:
        """
        获取天气信息

        Args:
            date: 日期（YYYY-MM-DD），默认为今天

        Returns:
            天气信息字典
        """
        # 如果未指定日期，使用今天
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')

        # 获取天气信息
        weather_data = self.fetch_weather_from_api()

        if weather_data is None:
            # 如果API失败，使用默认值
            weather_data = {
                'weather': '晴',
                'temperature': '15',
                'temperature_range': '10-20',
                'humidity': '60%',
                'wind': '东南风 3级',
                'location': self.location
            }

        # 添加图标
        weather_data['icon'] = self.get_weather_icon(weather_data['weather'])
        weather_data['temperature_with_unit'] = f"{weather_data['temperature']}°C"
        weather_data['date'] = date

        return weather_data

    def format_weather_display(self, weather_data: Dict) -> str:
        """格式化天气显示"""
        return f"{weather_data['icon']} {weather_data['weather']} {weather_data['temperature_with_unit']}"


def main():
    """测试用例"""
    fetcher = WeatherFetcher(location='烟台')

    # 获取今天天气
    weather = fetcher.get_weather()

    print("=" * 60)
    print("天气信息:")
    print("=" * 60)
    print(f"日期：{weather['date']}")
    print(f"地点：{weather['location']}")
    print(f"天气：{weather['weather']} {weather['icon']}")
    print(f"温度：{weather['temperature_with_unit']}")
    print(f"温度范围：{weather['temperature_range']}°C")
    print(f"湿度：{weather['humidity']}")
    print(f"风向：{weather['wind']}")

    print("\n格式化显示：")
    print(fetcher.format_weather_display(weather))


if __name__ == '__main__':
    main()
