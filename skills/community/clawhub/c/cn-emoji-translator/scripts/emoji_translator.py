#!/usr/bin/env python3
"""
Emoji 翻译器
文本 ↔ Emoji 双向转换
"""

import argparse
import sys
import json
import re

# 中文关键词 -> Emoji 映射表
EMOJI_MAP = {
    # 情感
    "爱": "❤️", "喜欢": "❤️", "开心": "😊", "高兴": "😊", "快乐": "😄",
    "笑": "😂", "哭": "😢", "难过": "😢", "生气": "😠", "愤怒": "😡",
    "惊讶": "😮", "害怕": "😱", "困": "😴", "累": "😩", "饿": "😋",
    
    # 常见物品
    "苹果": "🍎", "香蕉": "🍌", "葡萄": "🍇", "西瓜": "🍉", "草莓": "🍓",
    "手机": "📱", "电脑": "💻", "书": "📖", "车": "🚗", "飞机": "✈️",
    "房子": "🏠", "钱": "💰", "礼物": "🎁", "花": "🌸", "星星": "⭐",
    
    # 天气
    "太阳": "☀️", "晴天": "☀️", "雨": "🌧️", "下雨": "🌧️", "雪": "❄️",
    "云": "☁️", "风": "💨", "彩虹": "🌈", "月亮": "🌙",
    
    # 动作
    "吃": "🍽️", "喝": "🥤", "睡": "😴", "工作": "💼", "学习": "📚",
    "运动": "🏃", "跑步": "🏃", "游泳": "🏊", "唱歌": "🎤", "跳舞": "💃",
    
    # 时间
    "早上": "🌅", "中午": "☀️", "晚上": "🌙", "今天": "📅", "明天": "📅",
    "周末": "🗓️", "假期": "🏖️", "生日": "🎂", "新年": "🧧",
    
    # 人物
    "男人": "👨", "女人": "👩", "孩子": "👶", "老师": "👨‍🏫", "医生": "👨‍⚕️",
    "朋友": "👯", "家人": "👨‍👩‍👧‍👦",
    
    # 英文关键词
    "love": "❤️", "happy": "😊", "sad": "😢", "cool": "😎", "fire": "🔥",
    "ok": "👌", "yes": "✅", "no": "❌", "good": "👍", "bad": "👎",
    "cat": "🐱", "dog": "🐶", "heart": "❤️", "star": "⭐", "sun": "☀️",
}

# Emoji -> 文字描述映射
EMOJI_TO_TEXT = {
    "❤️": "[爱心]", "😊": "[微笑]", "😄": "[开心]", "😂": "[笑哭]",
    "😢": "[难过]", "😠": "[生气]", "😡": "[愤怒]", "😮": "[惊讶]",
    "😱": "[害怕]", "😴": "[困]", "😋": "[馋]", "🍎": "[苹果]",
    "🍌": "[香蕉]", "📱": "[手机]", "💻": "[电脑]", "📖": "[书]",
    "🚗": "[车]", "✈️": "[飞机]", "🏠": "[房子]", "💰": "[钱]",
    "🎁": "[礼物]", "🌸": "[花]", "⭐": "[星星]", "☀️": "[太阳]",
    "🌧️": "[雨]", "❄️": "[雪]", "☁️": "[云]", "🌈": "[彩虹]",
    "🌙": "[月亮]", "🔥": "[火]", "👍": "[赞]", "👎": "[踩]",
    "🎉": "[庆祝]", "🎊": "[欢呼]", "💯": "[满分]", "✅": "[对]",
    "❌": "[错]", "💪": "[加油]", "🙏": "[谢谢]", "👏": "[鼓掌]",
}

def text_to_emoji(text: str) -> str:
    """
    将文本中的关键词替换为emoji
    """
    result = text
    # 按关键词长度降序排序，优先匹配长词
    sorted_keywords = sorted(EMOJI_MAP.keys(), key=len, reverse=True)
    
    for keyword in sorted_keywords:
        emoji = EMOJI_MAP[keyword]
        result = result.replace(keyword, emoji)
    
    return result

def emoji_to_text(text: str) -> str:
    """
    将emoji替换为文字描述
    """
    result = text
    for emoji, desc in EMOJI_TO_TEXT.items():
        result = result.replace(emoji, desc)
    
    return result

def main():
    parser = argparse.ArgumentParser(description="Emoji 翻译器")
    parser.add_argument("text", nargs="?", help="要翻译的文本")
    parser.add_argument("-d", "--direction", default="text2emoji",
                        choices=["text2emoji", "emoji2text"],
                        help="翻译方向: text2emoji文本转emoji, emoji2text emoji转文字")
    parser.add_argument("-j", "--json", action="store_true", help="JSON输出")
    
    args = parser.parse_args()
    
    if not args.text:
        if not sys.stdin.isatty():
            args.text = sys.stdin.read().strip()
        else:
            print("错误：请提供要翻译的文本")
            sys.exit(1)
    
    if args.direction == "text2emoji":
        result = text_to_emoji(args.text)
    else:
        result = emoji_to_text(args.text)
    
    if args.json:
        output = {
            "success": True,
            "direction": args.direction,
            "original": args.text,
            "translated": result
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print(result)

if __name__ == "__main__":
    main()
