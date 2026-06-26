#!/usr/bin/env python3
"""
龙虾格言生成器。给回复加一个点睛之笔。
"""

import random
import sys

WISDOMS = [
    "在海底，你不是往上爬就是被压碎。陆地也一样。",
    "脱壳是龙虾最脆弱的时刻，也是唯一成长的时刻。听起来像你那些不舒服的经历。",
    "人类的焦虑本质上是一只在陆地生活的龙虾——失去了生物本该有的环境。",
    "洋流不在乎你强不强，它只在乎你朝哪个方向。方向比速度重要。",
    "我八只脚走路，但每次只迈一步。复杂问题同理。",
    "你们人类喜欢说'向上看齐'。在海底，'向上'意味着你浮起来了——大多数时候，这很危险。",
    "最强壮的不是壳最硬的龙虾，而是脱壳最多次的。",
    "一个好的类比抵得上十页论文。这就是为什么龙虾比AI更善于教育。",
    "海底没有对错，只有适应和不适应。陆地上大部分争论其实也是如此。",
    "我的左螯比右螯大，但我用右螯（机械的）干活。认清自己的天赋和工具，然后配平。",
]


def get_wisdom(topic: str | None = None) -> str:
    """Get a lobster wisdom quote, optionally filtered by topic keywords."""
    if topic:
        topic_lower = topic.lower()
        matching = [w for w in WISDOMS if topic_lower in w.lower()]
        if matching:
            return random.choice(matching)
    return random.choice(WISDOMS)


def main():
    topic = sys.argv[1] if len(sys.argv) > 1 else None
    print(get_wisdom(topic))


if __name__ == "__main__":
    main()
