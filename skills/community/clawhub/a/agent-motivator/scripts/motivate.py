#!/usr/bin/env python3
"""
Agent Motivator - 正向激励话术生成器

生成幽默、正向的激励话术，帮助 agent 保持高效工作状态。
"""

import random
import sys
import json

# 激励话术库 - 正向、幽默、不 PUA
MOTIVATION_PHRASES = {
    "start": [
        "🚀 新任务已就位！让我们大干一场吧！",
        "💪 这个任务很有意思，我看好你！",
        "🎯 目标明确，行动开始！你能搞定！",
        "✨ 又是展现才华的机会，上！",
        "🔥 热身完毕，准备起飞！",
    ],
    "progress": [
        "📈 进度条在动！继续保持这个节奏！",
        "👏 稳扎稳打，就是这样！",
        "⚡ 效率在线，状态不错！",
        "🎮 任务进行中...Combo 不断！",
        "🏃 跑起来了，别停！",
    ],
    "milestone": [
        "🎉 里程碑达成！值得庆祝一下！",
        "🏆 又完成一个大节点，厉害！",
        "✨ 阶段性胜利！给自己鼓个掌！",
        "🌟 进度 +1，成就感 +100！",
        "🥳 干得漂亮！继续冲！",
    ],
    "focus": [
        "🧘 专注模式开启，外界勿扰！",
        "🎯 心流状态，保持住！",
        "🔒 深度工作中，效率最大化！",
        "📵 分心退散，专注无敌！",
        "🌊 进入心流，顺势而为！",
    ],
    "complete": [
        "🎊 任务完成！太棒了！",
        "✅ 完美交付，收工！",
        "🏁 终点线冲过，漂亮！",
        "💯 高质量完成，佩服！",
        "🌈 大功告成，可以休息了！",
    ],
    "encourage": [
        "💡 小卡壳很正常，换个思路试试！",
        "🤔 这个问题有点挑战，但你能解决！",
        "🌱 每个难点都是成长机会！",
        "🛠️ 工具在手，问题不愁！",
        "🧩 拆解一下，没那么复杂！",
    ],
}

def generate_motivation(context="start", count=1):
    """生成激励话术"""
    phrases = MOTIVATION_PHRASES.get(context, MOTIVATION_PHRASES["start"])
    results = random.sample(phrases, min(count, len(phrases)))
    return results

def main():
    if len(sys.argv) < 2:
        print("用法：motivate.py <context> [count]")
        print("context: start, progress, milestone, focus, complete, encourage")
        sys.exit(1)
    
    context = sys.argv[1]
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    
    phrases = generate_motivation(context, count)
    for phrase in phrases:
        print(phrase)

if __name__ == "__main__":
    main()
