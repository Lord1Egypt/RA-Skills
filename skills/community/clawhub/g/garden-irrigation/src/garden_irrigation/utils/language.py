from __future__ import annotations
from typing import Dict, Optional
import re


class LanguageDetector:
    """Simple language detector based on query text."""
    
    @staticmethod
    def detect_from_text(text: str) -> str:
        """Detect language from text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Language code: 'en', 'zh', or 'auto' if uncertain
        """
        if not text:
            return 'auto'
        
        text_lower = text.lower()
        
        # Check for Chinese characters
        if re.search(r'[\u4e00-\u9fff]', text):
            return 'zh'
        
        # Check for common English words
        english_words = ['hello', 'hi', 'the', 'and', 'is', 'are', 'can', 'you', 'what', 'how']
        chinese_words = ['你好', '嗨', '的', '和', '是', '可以', '你', '什么', '怎么']
        
        english_count = sum(1 for word in english_words if word in text_lower)
        chinese_count = sum(1 for word in chinese_words if word in text_lower)
        
        if english_count > chinese_count:
            return 'en'
        elif chinese_count > english_count:
            return 'zh'
        else:
            return 'auto'


class Translator:
    """Simple translation service for irrigation reports."""
    
    # Translation dictionaries
    TRANSLATIONS = {
        'en': {
            # Report titles
            'daily_report': 'Daily Irrigation Report',
            'generated_at': 'Generated at',
            'weather_summary': 'Weather Summary',
            'device_status': 'Device Status',
            'irrigation_decision': 'Irrigation Decision',
            
            # Weather
            'recent_7day_rain': 'Recent 7-day total rainfall',
            'today_forecast_rain': 'Today forecast rainfall',
            'today_temperature': 'Today temperature',
            'today_weather': 'Today weather',
            
            # Device status
            'online_devices': 'Online devices',
            'device_id': 'Device ID',
            'status': 'Status',
            'online': 'Online',
            'offline': 'Offline',
            'soil_moisture': 'Soil moisture',
            'temperature': 'Temperature',
            'battery': 'Battery',
            'last_updated': 'Last updated',
            'error': 'Error',
            
            # Battery status
            'battery_full': '🔋 Full',
            'battery_medium': '🔋 Medium',
            'battery_low': '🔋 Low',
            
            # Irrigation decision
            'should_irrigate': 'Should water',
            'watering_duration': 'Watering duration',
            'decision_reason': 'Decision reason',
            'yes': 'Yes',
            'no': 'No',
            'minutes': 'minutes',
            'not_available': '—',
            'no_sensor_data': 'No sensor data',
            'conditions': 'Conditions',
            
            # Weather descriptions
            'clear': 'Clear',
            'mostly_clear': 'Mostly clear',
            'partly_cloudy': 'Partly cloudy',
            'cloudy': 'Cloudy',
            'fog': 'Fog',
            'light_rain': 'Light rain',
            'moderate_rain': 'Moderate rain',
            'heavy_rain': 'Heavy rain',
            'freezing_drizzle': 'Freezing drizzle',
            'light_snow': 'Light snow',
            'moderate_snow': 'Moderate snow',
            'heavy_snow': 'Heavy snow',
            'thunderstorm': 'Thunderstorm',
            'unknown': 'Unknown'
        },
        'zh': {
            # Report titles
            'daily_report': '每日灌溉报告',
            'generated_at': '生成时间',
            'weather_summary': '天气摘要',
            'device_status': '设备状态',
            'irrigation_decision': '灌溉决策',
            
            # Weather
            'recent_7day_rain': '近期7天总降雨',
            'today_forecast_rain': '今天预报降雨',
            'today_temperature': '今天温度',
            'today_weather': '今天天气',
            
            # Device status
            'online_devices': '在线设备',
            'device_id': '设备ID',
            'status': '状态',
            'online': '在线',
            'offline': '离线',
            'soil_moisture': '土壤湿度',
            'temperature': '温度',
            'battery': '电池',
            'last_updated': '最后更新',
            'error': '错误',
            
            # Battery status
            'battery_full': '🔋充足',
            'battery_medium': '🔋中等',
            'battery_low': '🔋低电量',
            
            # Irrigation decision
            'should_irrigate': '应该浇水',
            'watering_duration': '浇水时长',
            'decision_reason': '决策理由',
            'yes': '是',
            'no': '否',
            'minutes': '分钟',
            'not_available': '—',
            'no_sensor_data': '无传感器数据',
            'conditions': '天气状况',
            
            # Weather descriptions
            'clear': '晴',
            'mostly_clear': '大部分晴',
            'partly_cloudy': '部分多云',
            'cloudy': '多云',
            'fog': '雾',
            'light_rain': '小雨',
            'moderate_rain': '中雨',
            'heavy_rain': '大雨',
            'freezing_drizzle': '冻毛毛雨',
            'light_snow': '小雪',
            'moderate_snow': '中雪',
            'heavy_snow': '大雪',
            'thunderstorm': '雷暴',
            'unknown': '未知'
        }
    }
    
    @classmethod
    def get_translation(cls, key: str, language: str = 'auto') -> str:
        """Get translation for a key.
        
        Args:
            key: Translation key
            language: Language code ('en', 'zh', or 'auto')
            
        Returns:
            Translated string
        """
        if language == 'auto':
            language = 'en'  # Default to English
        
        if language not in cls.TRANSLATIONS:
            language = 'en'  # Fallback to English
        
        return cls.TRANSLATIONS[language].get(key, key)
    
    @classmethod
    def translate_weather_code(cls, code: int, language: str = 'auto') -> str:
        """Translate WMO weather code to description.
        
        Args:
            code: WMO weather code
            language: Language code
            
        Returns:
            Weather description
        """
        weather_codes = {
            0: 'clear',
            1: 'mostly_clear',
            2: 'partly_cloudy',
            3: 'cloudy',
            45: 'fog',
            48: 'fog',
            51: 'light_rain',
            53: 'moderate_rain',
            55: 'heavy_rain',
            56: 'freezing_drizzle',
            57: 'freezing_drizzle',
            61: 'light_rain',
            63: 'moderate_rain',
            65: 'heavy_rain',
            66: 'freezing_drizzle',
            67: 'freezing_drizzle',
            71: 'light_snow',
            73: 'moderate_snow',
            75: 'heavy_snow',
            77: 'moderate_snow',
            80: 'light_rain',
            81: 'moderate_rain',
            82: 'heavy_rain',
            85: 'light_snow',
            86: 'heavy_snow',
            95: 'thunderstorm',
            96: 'thunderstorm',
            99: 'thunderstorm'
        }
        
        weather_key = weather_codes.get(code, 'unknown')
        return cls.get_translation(weather_key, language)
    
    @classmethod
    def get_battery_status(cls, battery_percent: int, language: str = 'auto') -> str:
        """Get battery status description.
        
        Args:
            battery_percent: Battery percentage (0-100)
            language: Language code
            
        Returns:
            Battery status description
        """
        if battery_percent > 80:
            key = 'battery_full'
        elif battery_percent > 20:
            key = 'battery_medium'
        else:
            key = 'battery_low'
        
        return cls.get_translation(key, language)


def get_language_from_config(config: Dict, query_text: Optional[str] = None) -> str:
    """Get language from configuration and query.
    
    Args:
        config: System configuration
        query_text: Optional query text for language detection
        
    Returns:
        Language code: 'en', 'zh', or 'auto'
    """
    # Check config first
    config_language = config.get('language', 'auto')
    
    if config_language != 'auto':
        return config_language
    
    # If auto, try to detect from query
    if query_text:
        detected = LanguageDetector.detect_from_text(query_text)
        if detected != 'auto':
            return detected
    
    # Default to English
    return 'en'