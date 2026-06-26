#!/usr/bin/env python3
"""
cn-smart-reply: 智能回复生成器
支持微信/邮件/知乎/小红书/短信等多场景的智能回复建议
用法: python smart_reply.py <场景> <原消息内容>
"""

import sys
import random

SCENARIOS = {
    "感谢": {
        "examples": [
            "太感谢了！真的帮了我大忙，欠你一个人情~",
            "谢谢谢谢！你也太靠谱了，我都不知道怎么感谢好",
            "收到！感谢感谢，有机会一定请你喝咖啡☕",
        ]
    },
    "道歉": {
        "examples": [
            "抱歉抱歉！是我考虑不周，真的不好意思🙏",
            "啊不好意思！我不是故意的，抱歉抱歉",
            "对不起对不起，下次一定注意，给你添麻烦了",
        ]
    },
    "确认": {
        "examples": [
            "收到收到，我这边没问题！",
            "好的好的，我明白了，随时可以开始",
            "没问题！收到，我记下来了",
        ]
    },
    "拒绝": {
        "examples": [
            "不好意思，这次实在抽不开身，下次有机会一定！",
            "谢谢你的好意，但我这边可能不太方便，改天再约？",
            "抱歉啊，这个我帮不上忙，你看看找别人？",
        ]
    },
    "催促": {
        "examples": [
            "你好，请问上次说的事情有进展了吗？方便的话回一下~",
            "冒昧问一下，这个什么时候能搞定呀？急用，谢谢！",
            "你好，打扰了，上次的项目还顺利吗？",
        ]
    },
    "安慰": {
        "examples": [
            "别太自责了，谁没踩过坑呢，下次会更好的！",
            "没事没事，过程比结果重要，你已经很努力了💪",
            "这不算什么，谁还没遇到过挫折呢，加油！",
        ]
    },
    "祝贺": {
        "examples": [
            "恭喜恭喜！真的太棒了，实至名归！🎉",
            "哇太厉害了！恭喜恭喜！",
            "太牛了！真替你高兴，必须庆祝一下！",
        ]
    },
    "请教": {
        "examples": [
            "想请教一下，你是怎么做到的？方便的话分享一下经验呗",
            "不好意思打扰了，有个问题想请教你，方便吗？",
            "有个地方想请教你，不知道方便吗？",
        ]
    },
    "介绍": {
        "examples": [
            "给你介绍下，这是我的朋友XXX，在XXX方面很有经验",
            "这位是XXX，你们可以认识一下，说不定有合作机会",
            "来认识一下！XXX是我的老朋友，在行业里很资深",
        ]
    },
    "回复知乎": {
        "examples": [
            "泻药。亲身经历来说，这个问题的关键在于...个人经验仅供参考",
            "作为一个...的人，我觉得这个问题要从几个角度来看...以上希望能帮到你",
            "根据我的经验...不过每个人的情况不同，仅供参考",
        ]
    },
    "回复小红书": {
        "examples": [
            "同问！蹲一个答案～",
            "已收藏！感觉很有用，谢谢姐妹分享💕",
            "姐妹这个也太详细了吧！已保存！",
        ]
    }
}


def generate_reply(scenario, topic=""):
    """生成回复建议"""
    if scenario not in SCENARIOS:
        available = ', '.join(SCENARIOS.keys())
        return f"未知场景。可用场景：{available}"
    
    replies = SCENARIOS[scenario]["examples"]
    reply = random.choice(replies)
    
    if topic:
        return f"💬 {reply}\n\n📝 场景：{scenario} | 话题：{topic}"
    return f"💬 {reply}\n\n📝 场景：{scenario}"


def list_scenarios():
    print("📋 可用场景：")
    for i, name in enumerate(SCENARIOS.keys(), 1):
        print(f"  {i}. {name}")
    print("\n💡 用法:")
    print('  python smart_reply.py 感谢')
    print('  python smart_reply.py 催促 "关于项目进度"')
    print('  python smart_reply.py 回复知乎 "关于学习方法"')
    print('  python smart_reply.py 回复小红书')


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ['--help', '-h', 'help']:
        list_scenarios()
        sys.exit(0)
    
    scenario = sys.argv[1]
    topic = sys.argv[2] if len(sys.argv) > 2 else ""
    
    print(generate_reply(scenario, topic))


if __name__ == '__main__':
    main()
