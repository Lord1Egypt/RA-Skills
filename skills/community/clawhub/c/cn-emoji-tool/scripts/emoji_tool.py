#!/usr/bin/env python3
"""Emoji翻译与搜索工具"""
import argparse
import json
import sys

# 内置Emoji数据库
EMOJI_DATA = {
    "🔥": {"name": "火", "en": "fire", "keywords": ["热门", "火爆", "厉害", "火"]},
    "❤️": {"name": "红心", "en": "red heart", "keywords": ["爱", "喜欢", "心", "感谢"]},
    "😂": {"name": "笑哭", "en": "face with tears of joy", "keywords": ["好笑", "搞笑", "开心", "哈哈"]},
    "👍": {"name": "点赞", "en": "thumbs up", "keywords": ["赞", "好", "同意", "支持"]},
    "🎉": {"name": "庆祝", "en": "party popper", "keywords": ["庆祝", "恭喜", "成功", "开心"]},
    "💪": {"name": "加油", "en": "flexed biceps", "keywords": ["加油", "力量", "努力", "奋斗"]},
    "🌟": {"name": "星星", "en": "glowing star", "keywords": ["优秀", "棒", "明星", "亮点"]},
    "💰": {"name": "钱袋", "en": "money bag", "keywords": ["钱", "财富", "赚钱", "收入"]},
    "📱": {"name": "手机", "en": "mobile phone", "keywords": ["手机", "电话", "通讯"]},
    "💻": {"name": "电脑", "en": "laptop", "keywords": ["电脑", "办公", "工作"]},
    "🏠": {"name": "房子", "en": "house", "keywords": ["家", "房子", "住所"]},
    "🚗": {"name": "汽车", "en": "car", "keywords": ["车", "出行", "交通"]},
    "☀️": {"name": "太阳", "en": "sun", "keywords": ["晴天", "阳光", "天气好"]},
    "🌧️": {"name": "下雨", "en": "cloud with rain", "keywords": ["下雨", "雨天", "天气不好"]},
    "😊": {"name": "微笑", "en": "smiling face", "keywords": ["开心", "高兴", "微笑", "友好"]},
    "😢": {"name": "难过", "en": "crying face", "keywords": ["难过", "伤心", "不开心"]},
    "🤔": {"name": "思考", "en": "thinking face", "keywords": ["思考", "疑惑", "想"]},
    "👍": {"name": "好", "en": "thumbs up", "keywords": ["好", "行", "可以", "同意"]},
    "👎": {"name": "差", "en": "thumbs down", "keywords": ["差", "不行", "不好", "反对"]},
    "✅": {"name": "完成", "en": "check mark", "keywords": ["完成", "成功", "对", "确认"]},
    "❌": {"name": "错误", "en": "cross mark", "keywords": ["错误", "失败", "不对", "取消"]},
    "⚡": {"name": "闪电", "en": "lightning", "keywords": ["快", "迅速", "电力", "能量"]},
    "🎯": {"name": "目标", "en": "bullseye", "keywords": ["目标", "精准", "命中"]},
    "📈": {"name": "上涨", "en": "chart increasing", "keywords": ["上涨", "增长", "进步"]},
    "📉": {"name": "下跌", "en": "chart decreasing", "keywords": ["下跌", "减少", "退步"]},
}

def query_emoji(emoji):
    """查询Emoji含义"""
    if emoji in EMOJI_DATA:
        data = EMOJI_DATA[emoji]
        return {"emoji": emoji, "name": data["name"], "en": data["en"], "keywords": data["keywords"]}
    return {"error": f"未找到Emoji: {emoji}"}

def search_emoji(keyword):
    """关键词搜索Emoji"""
    results = []
    for emoji, data in EMOJI_DATA.items():
        if keyword in data["keywords"] or keyword in data["name"]:
            results.append({"emoji": emoji, "name": data["name"]})
    return results if results else [{"error": f"未找到关键词: {keyword}"}]

def text_to_emoji(text):
    """文本Emoji化"""
    result = text
    for emoji, data in EMOJI_DATA.items():
        for kw in data["keywords"]:
            if kw in result and kw not in ["火", "心"]:  # 避免过度替换常用词
                result = result.replace(kw, emoji, 1)
    return result

def main():
    parser = argparse.ArgumentParser(description="Emoji翻译与搜索工具")
    parser.add_argument("--query", help="查询Emoji含义")
    parser.add_argument("--search", help="关键词搜索Emoji")
    parser.add_argument("--text", help="文本Emoji化")
    parser.add_argument("--json", action="store_true", help="输出JSON格式")
    args = parser.parse_args()
    
    result = None
    if args.query:
        result = query_emoji(args.query)
    elif args.search:
        result = search_emoji(args.search)
    elif args.text:
        result = {"original": args.text, "emoji_text": text_to_emoji(args.text)}
    else:
        parser.print_help()
        return
    
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if isinstance(result, list):
            for r in result:
                if "emoji" in r:
                    print(f"{r['emoji']} {r['name']}")
                else:
                    print(r.get("error", r))
        else:
            for k, v in result.items():
                print(f"{k}: {v}")

if __name__ == "__main__":
    main()
