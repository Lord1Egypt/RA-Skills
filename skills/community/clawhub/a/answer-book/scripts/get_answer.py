#!/usr/bin/env python3
"""
The Answer Book / 答案之书 — flip to a random page and reveal a philosophical answer.

Usage:
    python3 get_answer.py [--lang en|zh] [page]

Default language: en
"""

import argparse
import json
import random
import sys

ANSWERS_EN = [
    "Yes.",
    "No.",
    "Absolutely.",
    "Without a doubt.",
    "Don't count on it.",
    "Trust your instincts.",
    "The time is right.",
    "Not yet.",
    "Try again later.",
    "Without question.",
    "It is certain.",
    "Doubtful.",
    "Better not tell you now.",
    "Focus on something else.",
    "Follow your heart.",
    "Remain patient.",
    "Take action now.",
    "Let it go.",
    "Investigate further.",
    "Listen more, speak less.",
    "Embrace the change.",
    "Make peace with the past.",
    "It will be worth the wait.",
    "Pursue it with passion.",
    "Walk away from it.",
    "Give it your all.",
    "Wait for a sign.",
    "The answer lies within.",
    "Trust the process.",
    "Speak from the heart.",
    "Definitely not.",
    "It's a clear yes.",
    "Forget about it.",
    "It's worth fighting for.",
    "Move on, gracefully.",
    "Take the leap.",
    "Stay where you are.",
    "Look for an alternative.",
    "Don't even think about it.",
    "Yes, but be cautious.",
    "Unquestionably.",
    "Reconsider your motives.",
    "Have faith.",
    "Be true to yourself.",
    "Now is not the time.",
    "Go ahead, be bold.",
    "It's time to let go.",
    "Persistence will pay off.",
    "Slow down.",
    "Speed it up.",
    "Trust the timing.",
    "Look beyond the obvious.",
    "Take the road less traveled.",
    "Yes, with a condition.",
    "It's only just begun.",
    "Beyond your wildest dreams.",
    "Less is more.",
    "The truth will set you free.",
    "There is no escape from it.",
    "Get a second opinion.",
    "Make a list of pros and cons.",
    "Set new goals.",
    "Compromise.",
    "Be brave.",
    "Smile, and the world smiles with you.",
    "Sleep on it.",
    "Take a deep breath.",
    "Save your strength.",
    "Choose a different path.",
    "Action speaks louder than words.",
    "Don't ask for permission.",
    "It's none of your business.",
    "Set your priorities.",
    "Stop, look, and listen.",
    "Have no fear.",
    "Resist the urge.",
    "Be grateful.",
    "Apologize.",
    "Ask a friend for advice.",
    "Forgive yourself.",
    "Be patient.",
    "Surrender, then begin again.",
    "Travel more.",
    "Finish what you started.",
    "Start over.",
    "Don't change a thing.",
    "It's not your concern.",
    "You already know the answer.",
    "Try a different approach.",
    "Believe in yourself.",
    "Risk it.",
    "Play it safe.",
    "Keep it simple.",
    "Consider the consequences.",
    "Good things take time.",
    "Be honest with yourself.",
    "Live in the moment.",
    "Make your own luck.",
    "There is no try, only do.",
    "Silence is golden.",
    "Let go of expectations.",
    "Yes, if you make it so.",
]

ANSWERS_ZH = [
    "是的。",
    "不是。",
    "毫无疑问。",
    "绝对可以。",
    "千万不要。",
    "顺其自然。",
    "时机已到。",
    "再等一等。",
    "改天再问。",
    "无需多虑。",
    "一定如此。",
    "希望渺茫。",
    "现在还不能告诉你。",
    "把注意力放在别处。",
    "听从你的心。",
    "保持耐心。",
    "立刻行动。",
    "放下吧。",
    "再深入了解一下。",
    "多听少说。",
    "拥抱改变。",
    "与过去和解。",
    "值得等待。",
    "请全心投入。",
    "转身离开。",
    "全力以赴。",
    "等一个信号。",
    "答案在你心里。",
    "相信过程。",
    "用心去说。",
    "完全不行。",
    "答案是肯定的。",
    "忘了它吧。",
    "值得为之奋斗。",
    "优雅地走开。",
    "勇敢地跳出去。",
    "原地不动。",
    "另寻他法。",
    "想都别想。",
    "可以，但要谨慎。",
    "毋庸置疑。",
    "重新审视你的动机。",
    "请保持信念。",
    "忠于自己。",
    "时机未到。",
    "大胆去做。",
    "是时候放手了。",
    "坚持终有回报。",
    "慢一点。",
    "再快一点。",
    "相信时间。",
    "看穿表象。",
    "走少有人走的路。",
    "可以，但有条件。",
    "一切才刚刚开始。",
    "超乎你的想象。",
    "少即是多。",
    "真相会让你自由。",
    "你逃不掉的。",
    "听一听别人的意见。",
    "把利弊列出来。",
    "重新设定目标。",
    "学会妥协。",
    "勇敢一点。",
    "微笑面对世界。",
    "睡一觉再说。",
    "深呼吸。",
    "保留实力。",
    "换一条路走。",
    "行动胜于言语。",
    "不必请示别人。",
    "这与你无关。",
    "理清优先级。",
    "停下来，看一看，听一听。",
    "无需畏惧。",
    "克制冲动。",
    "心存感激。",
    "去道个歉吧。",
    "找朋友聊聊。",
    "请原谅自己。",
    "耐心等待。",
    "先放下，再重来。",
    "去远方走走。",
    "把开始的事做完。",
    "重头再来。",
    "保持原样。",
    "这事不归你管。",
    "你早已知道答案。",
    "换个思路。",
    "相信你自己。",
    "冒险一试。",
    "稳妥一点。",
    "保持简单。",
    "想想后果。",
    "好事多磨。",
    "对自己诚实。",
    "活在当下。",
    "运气要靠自己。",
    "只管去做，无所谓试。",
    "沉默是金。",
    "放下期待。",
    "你愿意，便可以。",
]

LOCALES = {
    "en": {
        "answers": ANSWERS_EN,
        "title": "📖 The Answer Book — Page {page}",
        "footer": "Close the book gently. Trust the answer.",
        "page_error": "page must be an integer between 1 and {n}",
    },
    "zh": {
        "answers": ANSWERS_ZH,
        "title": "📖 答案之书 · 第 {page} 页",
        "footer": "轻轻合上书。相信这个答案。",
        "page_error": "页码必须是 1 到 {n} 之间的整数",
    },
}


def main() -> None:
    parser = argparse.ArgumentParser(description="The Answer Book / 答案之书")
    parser.add_argument("--lang", choices=["en", "zh"], default="en",
                        help="answer language (en or zh, default: en)")
    parser.add_argument("page", nargs="?", type=int, default=None,
                        help="optional page number; random if omitted")
    args = parser.parse_args()

    locale = LOCALES[args.lang]
    answers = locale["answers"]
    total = len(answers)

    if args.page is not None:
        if not 1 <= args.page <= total:
            print(json.dumps(
                {"error": locale["page_error"].format(n=total)},
                ensure_ascii=False,
            ))
            sys.exit(1)
        page = args.page
    else:
        page = random.randint(1, total)

    answer = answers[page - 1]
    title = locale["title"].format(page=page)
    display = f"{title}\n\n  ✦  {answer}  ✦\n\n{locale['footer']}"

    print(json.dumps(
        {
            "lang": args.lang,
            "page": page,
            "total_pages": total,
            "answer": answer,
            "display": display,
        },
        ensure_ascii=False,
        indent=2,
    ))


if __name__ == "__main__":
    main()
