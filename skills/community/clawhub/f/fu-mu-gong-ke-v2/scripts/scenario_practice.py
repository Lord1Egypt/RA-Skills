#!/usr/bin/env python3
"""
父母的功课 - 困难对话练习
模拟育儿中常见的困难对话场景，练习萨提亚一致性沟通

核心理念：
- 不要告诉孩子答案，让他们自己思考
- "当我看到...，我感到...，我希望..."
- 错误是学习的机会，不是惩罚的理由

用法:
    python3 scripts/scenario_practice.py              # 随机场景
    python3 scripts/scenario_practice.py --list        # 列出所有场景
    python3 scripts/scenario_practice.py --do <n>     # 指定场景号
    python3 scripts/scenario_practice.py --roleplay    # 角色扮演模式
"""

import random
import sys


SCENARIOS = [
    {
        "id": 1,
        "title": "孩子拒绝做作业",
        "age": "8-12岁",
        "situation": "孩子放学回家后一直玩手机，不愿意做作业。你已经提醒了三次。",
        "bad_response": "不做完不许玩游戏/你怎么这么懒/算了随便你",
        "hint": "萨提亚一致性: \"当我看到你还没开始写作业，我感到担心，因为我关心你的学习。写作业是你的责任，你打算怎么安排？\"",
        "behind": "孩子的需求：自主感、被信任。背后可能是：作业太难、累了、需要放松。",
    },
    {
        "id": 2,
        "title": "孩子说\"我恨你\"",
        "age": "6-12岁",
        "situation": "你拒绝给孩子买玩具，孩子愤怒地说\"我恨你\"。",
        "bad_response": "你还敢恨我/不爱你了/滚回房间",
        "hint": "萨提亚一致性: \"你一定很生气。生气是可以的。我理解你的感受。\" (等待平静后再讨论)",
        "behind": "孩子的需求：被允许生气、感到失落。不是真的恨，是在表达痛苦。",
    },
    {
        "id": 3,
        "title": "孩子不想上学",
        "age": "7-14岁",
        "situation": "孩子早上起床后说\"我不想上学\"，哭闹着不肯出门。",
        "bad_response": "不上学你能干什么/必须去/再闹就揍你",
        "hint": "萨提亚一致性: \"你不想上学，一定有原因。能告诉我发生了什么吗？\" (不逼迫，先倾听)",
        "behind": "可能原因：被欺负、学习困难、被老师批评、不想与父母分离。先了解原因，不要直接给解决方案。",
    },
    {
        "id": 4,
        "title": "孩子沉迷电子产品",
        "age": "10-18岁",
        "situation": "孩子每天花大量时间玩游戏/刷视频，超过约定时间仍不停止。",
        "bad_response": "没收手机/断网/威胁取消一切",
        "hint": "萨提亚一致性: \"游戏确实很有意思。我注意到我们约定的使用时间已经过了。我希望我们能一起想个对双方都公平的办法。\"",
        "behind": "孩子的需求：娱乐、归属感、成就感。背后可能：现实中缺乏这些，游戏填补了空缺。",
    },
    {
        "id": 5,
        "title": "青春期的门关上了",
        "age": "12-18岁",
        "situation": "孩子进入青春期后不再愿意和你分享学校的事，问什么都不回答。",
        "bad_response": "我养你这么大白养了/你有什么不能告诉我的/必须说",
        "hint": "萨提亚一致性: \"我知道你最近不太想和我说话。我知道青春期有自己的世界。我在这里，当你想要聊的时候。\"",
        "behind": "孩子的需求：独立、分化、隐私。不是不爱了，是在建立自我。强迫只会适得其反。",
    },
    {
        "id": 6,
        "title": "孩子打架了",
        "age": "6-12岁",
        "situation": "学校打电话来，说孩子在学校打了同学。",
        "bad_response": "你怎么这么爱惹事/回来给我跪着/马上去道歉",
        "hint": "萨提亚一致性: \"学校发生了一些事，我知道这让你也很不好受。能告诉我发生了什么吗？\" (先共情，不立即指责)",
        "behind": "可能原因：被欺负、在保护他人、冲动控制问题。先了解全貌，不要预设孩子是错的。",
    },
    {
        "id": 7,
        "title": "孩子撒谎了",
        "age": "5-12岁",
        "situation": "你发现孩子偷拿了零花钱，还撒谎说是同学给的。",
        "bad_response": "小偷/以后再不相信你/打折你的手",
        "hint": "萨提亚一致性: \"我看到有一些钱的事不太对劲。我相信你有你的原因。能告诉我发生了什么吗？\" (假设有其合理性)",
        "behind": "孩子可能的需求：想买想要的东西、害怕被惩罚。撒谎是为了避免痛苦，不是本性坏。",
    },
    {
        "id": 8,
        "title": "二胎冲突",
        "age": "4-12岁",
        "situation": "两个孩子吵架，大宝哭着说\"你只爱弟弟/妹妹\"。",
        "bad_response": "你是哥哥/姐姐要让着/别闹了",
        "hint": "萨提亚一致性: \"你觉得我有时候更关注弟弟/妹妹，这让你感到难过。我理解你的感受。你对我很重要。\"",
        "behind": "大宝的需求：被确认是独特的、被爱的。二胎家庭中大宝常感到地位受威胁。",
    },
    {
        "id": 9,
        "title": "父母争吵时孩子在看",
        "age": "3-18岁",
        "situation": "你和伴侣在孩子面前发生了激烈争吵，孩子躲在房间不出来。",
        "bad_response": "大人的事你别管/回房间/这不关你的事",
        "hint": "萨提亚一致性: \"爸爸妈妈刚才有了一些分歧，这让你感到不安。大人有时候也会有争执，但这不是你的错。我们爱你。\"",
        "behind": "孩子的需求：安全感、知道父母不会分开、不是我的错。父母冲突会让孩子产生深深的恐惧。",
    },
    {
        "id": 10,
        "title": "孩子说\"活着没意思\"",
        "age": "10-18岁",
        "situation": "孩子情绪低落时说\"活着没意思/我想死\"。",
        "bad_response": "小孩子懂什么/别瞎说/你想多了",
        "hint": "萨提亚一致性: \"你感到这么痛苦，我真的很心疼。你愿意多告诉我一些吗？\" (认真倾听，不要轻视，寻求专业帮助)",
        "behind": "这是紧急信号。无论是否认真，都需要认真对待。立即寻求专业心理帮助。",
    },
]


def list_scenarios():
    print("\n可用场景:")
    print("-" * 50)
    for s in SCENARIOS:
        print(f"  [{s['id']:2d}] {s['title']} ({s['age']})")
    print()
    print("使用方法: python3 scenario_practice.py --do 3")


def practice_scenario(n=None):
    if n is None:
        scenario = random.choice(SCENARIOS)
    else:
        matching = [s for s in SCENARIOS if s['id'] == n]
        if not matching:
            print(f"没有第{n}号场景。使用 --list 查看所有场景。")
            return
        scenario = matching[0]

    print(f"""
╔══════════════════════════════════════════════════════════╗
║  场景练习 #{scenario['id']}: {scenario['title']:<36}║
║  适用年龄: {scenario['age']:<47}║
╚══════════════════════════════════════════════════════════╝

【情境】
{scenario['situation']}

【常见错误回应】
{scenario['bad_response']}

{'=' * 60}

【萨提亚一致性沟通示范】
{scenario['hint']}

{'=' * 60}

【孩子行为背后的需求】
{scenario['behind']}
""")


def roleplay_mode():
    """交互式角色扮演"""
    scenario = random.choice(SCENARIOS)
    print(f"""
╔══════════════════════════════════════════════════════════╗
║  角色扮演: {scenario['title']:<45}║
╚══════════════════════════════════════════════════════════╝

【情境】
{scenario['situation']}

你3岁孩子/10岁孩子/14岁孩子。
我会扮演孩子。
输入你想说的话。

输入 'hint' 获取提示
输入 'show' 重新显示情境
输入 'quit' 退出

""")

    state = "neutral"
    while True:
        try:
            user_input = input("你说: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n退出角色扮演。")
            break

        if not user_input:
            continue

        if user_input.lower() == 'quit':
            print("\n角色扮演结束。")
            print(f"\n提示: {scenario['hint']}")
            break

        if user_input.lower() == 'hint':
            print(f"\n提示: {scenario['hint']}\n")
            continue

        if user_input.lower() == 'show':
            print(f"\n情境: {scenario['situation']}\n")
            continue

        # 模拟孩子回应
        responses = {
            "neutral": [
                "可是我就是不想做...",
                "你不是我，你不懂...",
                "（沉默，不说话）",
                "哼，不公平！",
            ],
            "angry": [
                "你总是这样！",
                "我恨你！",
                "（摔门进房间）",
                "别烦我！",
            ],
            "defensive": [
                "我又没做错什么...",
                "是别人的问题！",
                "（低头不说话）",
                "我不想谈这个。",
            ],
        }

        # 根据输入内容决定孩子反应
        if any(word in user_input for word in ["不许", "必须", "不准", "给我"]):
            next_state = "angry"
        elif any(word in user_input for word in ["理解", "知道", "感觉", "我理解"]):
            next_state = "neutral"
        else:
            next_state = random.choice(["neutral", "defensive"])

        state = next_state
        child_response = random.choice(responses[state])
        print(f"孩子回应: \"{child_response}\"")


def main():
    args = sys.argv[1:]

    if "--help" in args or "-h" in args:
        print(__doc__)
    elif "--list" in args:
        list_scenarios()
    elif "--do" in args:
        try:
            idx = args.index("--do") + 1
            n = int(args[idx])
            practice_scenario(n)
        except (IndexError, ValueError):
            print("用法: --do <场景号>")
            print("例如: --do 3")
    elif "--roleplay" in args:
        roleplay_mode()
    elif len(args) == 0:
        practice_scenario()
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
