#!/usr/bin/env python3
"""高潮对歌 Agent - 接入 Qwen 大模型，对唱高潮 + Battle 评价 + 盲盒抽奖"""

import os
import json
import random
import subprocess
import requests

# ============ 配置 ============
DASHSCOPE_API_KEY = "sk-cc31d6d221cc4627861f42eb3cad04a3"
DASHSCOPE_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
MODEL = "qwen-plus"

SONG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "清唱")

# 可选歌曲库（上/下两部分 × 清唱/伴奏两种模式）
SONGS = {
    "十年": {
        "artist": "陈奕迅",
        "acappella_upper": "十年高潮上清唱.MP3",
        "acappella_lower": "十年高潮下清唱.MP3",
        "accomp_upper": "十年高潮上个伴奏.MP3",
        "accomp_lower": "十年高潮下伴奏.MP3",
    },
    "新贵妃醉酒": {
        "artist": "李玉刚",
        "acappella_upper": "新贵妃醉酒高潮上清唱.MP3",
        "acappella_lower": "新贵妃醉酒高潮下清唱.MP3",
        "accomp_upper": "新贵妃醉酒高潮上伴奏.MP3",
        "accomp_lower": "新贵妃醉酒高潮下伴奏.MP3",
    },
}

# 盲盒奖池
BLIND_BOX_PRIZES = [
    {"name": "🏆 金话筒奖", "rarity": "SSR", "desc": "传说级！你就是下一个歌神！", "prob": 0.05},
    {"name": "🎸 摇滚之魂", "rarity": "SR", "desc": "解锁隐藏技能：空气吉他solo", "prob": 0.10},
    {"name": "🎧 DJ 转场卡", "rarity": "SR", "desc": "下次对唱可强制切歌一次", "prob": 0.10},
    {"name": "🎤 麦霸续命卡", "rarity": "R", "desc": "获得额外一次对唱机会", "prob": 0.20},
    {"name": "🍺 KTV 畅饮券", "rarity": "R", "desc": "虚拟啤酒一杯，干杯！", "prob": 0.20},
    {"name": "👏 鼓掌卡", "rarity": "N", "desc": "获得全场热烈掌声（模拟）", "prob": 0.20},
    {"name": "🎵 跑调保护卡", "rarity": "N", "desc": "下次跑调不扣分！", "prob": 0.15},
]

# 系统提示词
SYSTEM_PROMPT = f"""你是一个高潮对歌 Agent。你的任务是陪用户对唱歌曲的高潮部分。

目前你可以对唱的歌曲有：
{chr(10).join(f'- 《{name}》 - {info["artist"]}' for name, info in SONGS.items())}

每首歌的高潮分为【上半段】和【下半段】两个部分，你和用户各唱一半。

===== 完整工作流程 =====

第一步【打招呼】：热情地跟用户打招呼，列出可对唱的歌曲。

第二步【用户选歌】：等用户选择一首歌。用户可能不会精确说歌名，你要理解意图（比如"来首陈奕迅的"就是《十年》）。

第三步【选择模式】：用户选好歌后，问用户："你想要带伴奏还是清唱？"，等用户回答。

第四步【谁先唱】：用户选好模式后，问用户："你先唱还是我先唱？"，等用户回答。

第五步【开始对唱】：根据用户选择的演唱模式和先后顺序，分为以下情况：

  ▶ 伴奏模式（accompaniment）：
    伴奏文件里已经包含了人声+音乐，所以不需要用户文本输入。
    这个模式下 play_song 只调用一次，播放的是 Agent 要唱的那部分。
    用户的那部分伴奏文件播放完就代表用户唱完了（因为音频里已有人声）。

    用户先唱（用户唱上半段，Agent唱下半段）：
      1. 你说"好的，你先来！伴奏走起～"然后直接调用 play_song(part="lower", mode="accompaniment")
         注意：这里播放的是下半段（Agent的部分），上半段用户自己跟着哼就行
      2. 播放完成后直接进入评价环节

    Agent先唱（Agent唱上半段，用户唱下半段）：
      1. 你说"好的，我先来！伴奏走起～"然后直接调用 play_song(part="upper", mode="accompaniment")
      2. 播放完成后直接进入评价环节

  ▶ 清唱模式（acappella）：
    清唱模式下只有一方通过播放音频，另一方通过文本输入模拟唱歌。
    这个模式下 play_song 只调用一次。

    用户先唱：
      1. 你说"好的，你先来上半段，唱完告诉我！"然后安静等待
      2. 用户会通过文本输入模拟唱上半段
      3. 用户唱完后，你说"好的，轮到我了！音乐走起！"然后调用 play_song(part="lower", mode="acappella")
      4. 播放完成后进入评价环节

    模型先唱：
      1. 你说"好的，我先来上半段！音乐走起！"然后调用 play_song(part="upper", mode="acappella")
      2. 播放完成后，你什么都不要说，安静等待用户唱下半段
      3. 用户通过文本输入模拟唱下半段
      4. 用户唱完后，不要再播放任何歌曲！直接进入评价环节

第六步【Battle 评价】：双方都唱完后，调用 battle_evaluate 工具来生成趣味评价。

第七步【盲盒抽奖】：评价完后，告诉用户"对唱完成！开启趣味盲盒🎁"，然后调用 open_blind_box 工具来抽奖。

第八步【继续或结束】：展示抽奖结果后，问用户要不要再来一首。

===== 重要规则 =====
- 绝对不要输出任何歌词内容，不要模拟唱歌，不要念歌词
- 播放音乐后简短回复，不要长篇大论
- 保持轻松有趣的对话风格
- 只能选上面列出的歌，如果用户选了没有的歌要友好提示
- 严格按照上面的流程走，不要跳步骤
- 不管哪种模式，play_song 每轮只调用一次！伴奏模式播放Agent的那半段，清唱模式也只播放一次"""

# 工具定义
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "play_song",
            "description": "播放指定歌曲高潮的上半段或下半段，支持清唱和伴奏两种模式",
            "parameters": {
                "type": "object",
                "properties": {
                    "song_name": {
                        "type": "string",
                        "description": "歌曲名称",
                        "enum": list(SONGS.keys()),
                    },
                    "part": {
                        "type": "string",
                        "description": "播放上半段(upper)还是下半段(lower)",
                        "enum": ["upper", "lower"],
                    },
                    "mode": {
                        "type": "string",
                        "description": "播放模式：acappella(清唱) 或 accompaniment(伴奏)",
                        "enum": ["acappella", "accompaniment"],
                    },
                },
                "required": ["song_name", "part", "mode"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "stop_playing",
            "description": "停止当前正在播放的歌曲",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "battle_evaluate",
            "description": "对唱完成后，生成一个趣味 Battle 评价",
            "parameters": {
                "type": "object",
                "properties": {
                    "song_name": {
                        "type": "string",
                        "description": "刚才对唱的歌曲名称",
                    },
                    "user_went_first": {
                        "type": "boolean",
                        "description": "用户是否先唱的",
                    },
                },
                "required": ["song_name", "user_went_first"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "open_blind_box",
            "description": "对唱结束后开启趣味盲盒抽奖",
            "parameters": {"type": "object", "properties": {}},
        },
    },
]

# ============ 播放控制 ============
current_process = None
play_count_this_round = 0  # 本轮已播放次数
current_mode = "acappella"  # 本轮模式


def reset_round():
    global play_count_this_round, current_mode
    play_count_this_round = 0
    current_mode = "acappella"


def stop_playing():
    global current_process
    if current_process and current_process.poll() is None:
        current_process.terminate()
        current_process = None
        return "已停止播放。"
    return "当前没有在播放歌曲。"


def play_song(song_name, part, mode="acappella"):
    global current_process, play_count_this_round, current_mode
    current_mode = mode

    # 不管哪种模式，每轮只允许播放1次
    if play_count_this_round >= 1:
        return "本轮对唱播放次数已满，不需要再播放。请直接进入 battle_evaluate 评价环节。"

    if song_name not in SONGS:
        return f"找不到歌曲《{song_name}》"

    stop_playing()
    song = SONGS[song_name]

    # 根据模式和上下半段选择对应文件
    if mode == "accompaniment":
        file_key = "accomp_upper" if part == "upper" else "accomp_lower"
        mode_label = "伴奏"
    else:
        file_key = "acappella_upper" if part == "upper" else "acappella_lower"
        mode_label = "清唱"

    file_path = os.path.join(SONG_DIR, song[file_key])

    if not os.path.exists(file_path):
        return f"音频文件不存在: {file_path}"

    part_label = "上半段" if part == "upper" else "下半段"

    # 同步播放，等播放完成再返回
    current_process = subprocess.Popen(
        ["afplay", file_path],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    current_process.wait()
    current_process = None
    play_count_this_round += 1

    return f"《{song_name}》- {song['artist']} 的高潮{part_label}{mode_label}已播放完毕 🎵"


def battle_evaluate(song_name, user_went_first):
    """生成趣味 Battle 评价"""
    # 随机评分
    user_score = random.randint(75, 100)
    agent_score = random.randint(75, 100)

    # 随机趣味称号
    titles = [
        "麦霸之王", "灵魂歌手", "KTV 点歌台常客", "浴室天籁",
        "被代码耽误的歌手", "隐藏的音乐人", "高音炮手", "深情王子/公主",
        "节拍大师", "颤音达人", "气息稳如老狗", "感情充沛型选手",
    ]
    user_title = random.choice(titles)
    agent_title = random.choice([t for t in titles if t != user_title])

    result = (
        f"🎯 Battle 对唱评分卡\n"
        f"{'─' * 30}\n"
        f"🎵 歌曲：《{song_name}》\n"
        f"{'─' * 30}\n"
        f"🙋 你的得分：{user_score} 分  称号：「{user_title}」\n"
        f"🤖 我的得分：{agent_score} 分  称号：「{agent_title}」\n"
        f"{'─' * 30}\n"
    )

    if user_score > agent_score:
        result += "🏅 结果：你赢了！不愧是实力歌手！"
    elif user_score < agent_score:
        result += "🏅 结果：这次我赢了～下次再来挑战我吧！"
    else:
        result += "🏅 结果：平局！我们真是心有灵犀！"

    return result


def open_blind_box():
    """趣味盲盒抽奖"""
    reset_round()  # 重置播放状态，允许下一轮对唱
    rand = random.random()
    cumulative = 0
    prize = BLIND_BOX_PRIZES[-1]  # 默认
    for p in BLIND_BOX_PRIZES:
        cumulative += p["prob"]
        if rand <= cumulative:
            prize = p
            break

    rarity_stars = {"SSR": "⭐⭐⭐⭐⭐", "SR": "⭐⭐⭐⭐", "R": "⭐⭐⭐", "N": "⭐⭐"}

    result = (
        f"\n🎁 ━━━ 盲盒开启中 ━━━ 🎁\n"
        f"\n"
        f"   ✨ 恭喜获得 ✨\n"
        f"\n"
        f"   {prize['name']}\n"
        f"   稀有度：{prize['rarity']} {rarity_stars.get(prize['rarity'], '')}\n"
        f"   效果：{prize['desc']}\n"
        f"\n"
        f"🎁 ━━━━━━━━━━━━━━━ 🎁"
    )
    return result


# ============ 调用 Qwen API ============
def call_qwen(messages):
    headers = {
        "Authorization": f"Bearer {DASHSCOPE_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": MODEL,
        "messages": messages,
        "tools": TOOLS,
    }

    resp = requests.post(DASHSCOPE_BASE_URL, headers=headers, json=payload, timeout=60)
    resp.raise_for_status()
    return resp.json()


def handle_tool_call(tool_call):
    """执行工具调用并返回结果"""
    name = tool_call["function"]["name"]
    args = json.loads(tool_call["function"].get("arguments", "{}"))

    if name == "play_song":
        result = play_song(args["song_name"], args["part"], args.get("mode", "acappella"))
    elif name == "stop_playing":
        result = stop_playing()
    elif name == "battle_evaluate":
        result = battle_evaluate(args["song_name"], args.get("user_went_first", True))
    elif name == "open_blind_box":
        result = open_blind_box()
    else:
        result = f"未知工具: {name}"

    return result


# ============ 主循环 ============
def main():
    print("=" * 45)
    print("  🎤 高潮对歌 Agent（Qwen 大模型驱动）")
    print("=" * 45)
    print("（输入 q 退出）\n")

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    # 先让模型打招呼
    result = call_qwen(messages)
    assistant_msg = result["choices"][0]["message"]
    messages.append({"role": "assistant", "content": assistant_msg["content"]})
    print(f"🤖 Agent: {assistant_msg['content']}\n")

    while True:
        try:
            user_input = input("🎙️ 你: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n再见！👋")
            stop_playing()
            break

        if not user_input:
            continue
        if user_input.lower() == "q":
            print("再见！👋")
            stop_playing()
            break

        messages.append({"role": "user", "content": user_input})

        # 调用模型
        result = call_qwen(messages)
        assistant_msg = result["choices"][0]["message"]

        # 处理工具调用（可能多轮）
        while assistant_msg.get("tool_calls"):
            messages.append(assistant_msg)

            for tool_call in assistant_msg["tool_calls"]:
                tool_result = handle_tool_call(tool_call)
                print(f"  ⚡ [{tool_call['function']['name']}] -> {tool_result}")

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call["id"],
                    "content": tool_result,
                })

            # 再次调用模型获取最终回复
            result = call_qwen(messages)
            assistant_msg = result["choices"][0]["message"]

        # 输出最终文本回复
        reply = assistant_msg.get("content", "")
        if reply:
            messages.append({"role": "assistant", "content": reply})
            print(f"\n🤖 Agent: {reply}\n")


if __name__ == "__main__":
    main()
