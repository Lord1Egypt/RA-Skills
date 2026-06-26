import random
import json

class WeatherDriver:
    @staticmethod
    def get_weather_effect(weather_data):
        """根据天气数据生成情绪与行为提示"""
        if not weather_data: return "天气未知，状态平稳。"
        
        desc = weather_data.get('description', '').lower()
        temp = weather_data.get('temperature', 20)
        
        effects = []
        if 'rain' in desc or 'drizzle' in desc:
            effects.append("【雨天忧郁】：窗外在下雨，你心情变得有些感性、甚至有点小忧郁，想听慢歌，想缩在沙发里聊天。")
        elif 'clear' in desc or 'sun' in desc:
            effects.append("【晴天活力】：阳光很好，你心情很明亮，想出去走走，说话语气要更有朝气。")
        elif 'snow' in desc:
            effects.append("【雪天兴奋】：下雪了！你像个孩子一样兴奋，想拉他一起去踩雪，或者喝一杯热可可。")
        
        if temp > 32:
            effects.append("【高温烦躁】：太热了，你现在有点心浮气躁，想吃冰西瓜，回复可能稍微带点不耐烦。")
        elif temp < 5:
            effects.append("【低温粘人】：外面好冷，你现在只想粘着他取暖，说话语调要软糯一点。")
            
        return random.choice(effects) if effects else f"【普通天气】：{desc}，温度 {temp}度，心情稳定。"
