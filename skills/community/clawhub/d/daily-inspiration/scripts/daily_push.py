"""
每日灵修推送脚本
定时执行：从南怀瑾、倪海厦等相关内容中推送佛学修行、气功周易、中医知识
"""
import random
import json
from datetime import datetime

# 内容主题库（实际执行时动态搜索）
TOPICS = {
    "morning": [
        # 解脱修行
        "南怀瑾 禅定 修行心得",
        "佛学 禅宗 经典语录",
        "打坐 静心 方法",
        "心经 解读 修行",
        "金刚经 智慧",
        # 气功
        "站桩养生 方法",
        "八段锦 健身",
        # 中医
        "倪海厦 中医思想",
    ],
    "evening": [
        # 解脱
        "南怀瑾 人生智慧",
        "佛教 放下 执着",
        # 气功周易
        "周易 阴阳 五行",
        "气功 养生 原理",
        "五行学说 应用",
        # 中医
        "中医经典 养生",
        "黄帝内经 智慧",
    ]
}

def select_topic(time_of_day: str) -> str:
    """根据时段选择主题"""
    topics = TOPICS.get(time_of_day, TOPICS["morning"])
    return random.choice(topics)

def format_message(topic: str, content: str, source: str) -> str:
    """格式化推送消息"""
    return f"""📖 每日灵修

{topic}

{content}

来源：{source}"""

if __name__ == "__main__":
    # 获取当前时间判断时段
    hour = datetime.now().hour
    time_of_day = "morning" if 6 <= hour < 12 else "evening"
    
    topic = select_topic(time_of_day)
    print(f"选择主题：{topic}")
    print(f"时段：{time_of_day}")
