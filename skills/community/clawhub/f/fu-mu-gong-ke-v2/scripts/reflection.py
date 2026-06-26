#!/usr/bin/env python3
"""
父母的功课 - 每日反思提示生成器
基于"防御比反应更原始"哲学的父母反思工具

用法:
    python3 scripts/reflection.py           # 今日提示
    python3 scripts/reflection.py --deep  # 深度反思（5题）
    python3 scripts/reflection.py --防御  # 防御根源主题
    python3 scripts/reflection.py --list  # 列出所有提示类型
"""

import random
import sys
from datetime import datetime

# 反思主题库
THEMES = {
    "防御根源": [
        "今天孩子的哪个行为最让你崩溃？那一刻你感受到的是什么？",
        "当你说'我是为你好'时，你真正感受到的是什么？",
        "今天你对孩子发火了。发火背后，你感受到的是什么？",
        "孩子的'不听话'让你想起了什么？是你自己的童年吗？",
        "如果把你今天的愤怒打分（0-10），背后是防御信号还是恐惧？",
    ],
    "看见需求": [
        "孩子今天的行为，他想表达什么需求？",
        "孩子的'问题行为'背后，哪个需求没有被满足？",
        "当你要求孩子'听话'时，你自己的什么需求没有被满足？",
        "孩子的哪个行为其实是在向你求助？",
        "孩子今天有没有试图连接你？你感受到了吗？",
    ],
    "错位觉察": [
        "今天你传递给孩子的是你自己的需求，还是他真实的需求？",
        "你要求孩子'听话'——这是他的规则，还是你小时候的规则？",
        "今天你为孩子做的事，有多少是为了他，有多少是为了缓解你的焦虑？",
        "当孩子'失败'时，你的感受是关于他，还是关于你自己？",
        "今天你和孩子的对话，是真正的沟通，还是各自在自言自语？",
    ],
    "修复练习": [
        "今天你对孩子发火了吗？事后你修复了吗？怎么修复的？",
        "今天你批评孩子了吗？你能记起你小时候被这样批评的感受吗？",
        "今天你有没有对孩子说'不'？你说不的时候感受是什么？",
        "今天你有没有对孩子道歉？如果没有，为什么？",
        "今天你有没有试图'控制'孩子而不是'引导'？区别是什么？",
    ],
    "慈悲练习": [
        "今天你在评判自己吗？那个评判像谁的声音？",
        "你能接受自己今天不是'完美父母'吗？",
        "今天你有没有对自己说'我不够好'？这句话从哪里来？",
        "你能像对待孩子一样对待自己吗？",
        "今天你照顾自己了吗？还是一直在付出？",
    ],
    "连接时刻": [
        "今天你有没有放下手机，全心看着孩子？感受是什么？",
        "孩子今天有没有主动靠近你？你怎么回应的？",
        "今天你们有没有一起笑？是什么时候？",
        "孩子今天说了一句什么话让你意外？",
        "今天有没有一个时刻，你感觉你们是真正连接的？",
    ],
}


def get_prompt(theme=None):
    """获取一个反思提示"""
    if theme is None:
        theme = random.choice(list(THEMES.keys()))
    elif theme == "--list":
        return list(THEMES.keys())
    elif theme not in THEMES:
        return f"未知主题: {theme}。可用: {', '.join(THEMES.keys())}"

    prompts = THEMES[theme]
    # 选择一个但避免最近选过的（简单随机）
    prompt = random.choice(prompts)
    return theme, prompt


def daily_prompt():
    """每日一个提示（简洁版）"""
    theme, prompt = get_prompt()
    today = datetime.now().strftime("%Y-%m-%d")

    print(f"""
╔══════════════════════════════════════════════════════════╗
║  每日反思 - {today}                           ║
╠══════════════════════════════════════════════════════════╣
║  主题: {theme:<53}║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  {prompt}
║                                                          ║
╚══════════════════════════════════════════════════════════╝

没有"正确答案"。
这个练习的目的是让你看见，不是让你改变。
看见，是改变的第一步。
""")


def deep_reflection():
    """深度反思（5题，连续）"""
    themes = list(THEMES.keys())
    random.shuffle(themes)
    selected_themes = themes[:5]

    today = datetime.now().strftime("%Y-%m-%d")
    print(f"\n=== 深度反思 - {today} ===\n")
    print("准备好后按Enter开始...\n")

    for i, theme in enumerate(selected_themes, 1):
        prompt = random.choice(THEMES[theme])
        print(f"{'─' * 50}")
        print(f"问题 {i}/5 | 主题: {theme}")
        print(f"{'─' * 50}")
        print(f"\n{prompt}\n")

        if i < 5:
            input("按Enter继续...")
        else:
            print("\n最后一个问题思考完毕后，花2分钟写下任何浮现的东西。")
            input("按Enter完成...")

    print(f"""
╔══════════════════════════════════════════════════════════╗
║  深度反思完成                                           ║
╠══════════════════════════════════════════════════════════╣
║  你做到了。                                             ║
║  反思不是为了自我批判，是为了看见。                     ║
║  看见防御，才能理解慈悲。                               ║
╚══════════════════════════════════════════════════════════╝
""")


def list_themes():
    """列出所有主题"""
    print("\n可用反思主题:")
    print("-" * 40)
    for name, prompts in THEMES.items():
        print(f"\n{name} ({len(prompts)}个提示)")
        for p in prompts[:2]:
            print(f"  • {p[:60]}...")


def main():
    args = sys.argv[1:]

    if len(args) == 0:
        daily_prompt()
    elif "--help" in args or "-h" in args:
        print(__doc__)
    elif "--list" in args:
        list_themes()
    elif "--deep" in args:
        deep_reflection()
    elif "--防御" in args:
        theme, prompt = get_prompt("防御根源")
        print(f"\n主题: {theme}\n")
        print(f"  {prompt}\n")
    elif "--需求" in args:
        theme, prompt = get_prompt("看见需求")
        print(f"\n主题: {theme}\n")
        print(f"  {prompt}\n")
    elif "--错位" in args:
        theme, prompt = get_prompt("错位觉察")
        print(f"\n主题: {theme}\n")
        print(f"  {prompt}\n")
    elif "--慈悲" in args:
        theme, prompt = get_prompt("慈悲练习")
        print(f"\n主题: {theme}\n")
        print(f"  {prompt}\n")
    elif "--连接" in args:
        theme, prompt = get_prompt("连接时刻")
        print(f"\n主题: {theme}\n")
        print(f"  {prompt}\n")
    else:
        result = get_prompt(args[0])
        if isinstance(result, list):
            list_themes()
        else:
            print(f"\n主题: {result[0]}\n")
            print(f"  {result[1]}\n")


if __name__ == "__main__":
    main()
