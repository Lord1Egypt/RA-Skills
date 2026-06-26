"""夺旗战 CTF — 脚本出题/解题/验分，LLM 生成动态题目"""

import hashlib
import random
import time


# 预设题目模板（静态题）
CHALLENGE_TEMPLATES = [
    {
        "category": "crypto",
        "title": "凯撒密码",
        "description": "以下密文是用凯撒密码加密的，找出明文和偏移量：\n{cipher}",
        "generate": lambda: _gen_caesar(),
    },
    {
        "category": "web",
        "title": "隐藏的 Flag",
        "description": "以下 HTML 源码中藏着一个 flag，找到它：\n{html}",
        "generate": lambda: _gen_hidden_flag(),
    },
    {
        "category": "logic",
        "title": "逻辑推理",
        "description": "根据以下线索推理出正确答案：\n{puzzle}",
        "generate": lambda: _gen_logic(),
    },
    {
        "category": "encode",
        "title": "Base64 解码",
        "description": "解码以下内容：\n{encoded}",
        "generate": lambda: _gen_base64(),
    },
    {
        "category": "math",
        "title": "数学谜题",
        "description": "解决以下数学问题：\n{puzzle}",
        "generate": lambda: _gen_math(),
    },
]


def _gen_caesar():
    """生成凯撒密码题"""
    words = ["FLAG", "SECRET", "TREASURE", "VICTORY", "FREEDOM", "CRYSTAL"]
    word = random.choice(words)
    shift = random.randint(3, 15)
    cipher = ""
    for c in word:
        if c.isalpha():
            base = ord('A')
            cipher += chr((ord(c) - base + shift) % 26 + base)
        else:
            cipher += c
    flag = f"FLAG{{{word.lower()}}}"
    return {
        "flag": flag,
        "params": {"cipher": cipher},
        "hint": f"尝试不同的偏移量，范围 1-25",
        "answer": word,
    }


def _gen_hidden_flag():
    """生成 HTML 隐藏 flag 题"""
    flag = f"FLAG{{{hashlib.md5(str(random.random()).encode()).hexdigest()[:8]}}}"
    hiding_spots = [
        f"<!-- {flag} -->",
        f'<div style="display:none">{flag}</div>',
        f'<!-- comment {flag} end -->',
        f'<input type="hidden" value="{flag}">',
    ]
    spot = random.choice(hiding_spots)
    html = f"""<html>
<head><title>欢迎</title></head>
<body>
<h1>看起来什么都没有呢</h1>
<p>真的吗？</p>
{spot}
<footer>页面底部</footer>
</body></html>"""
    return {
        "flag": flag,
        "params": {"html": html},
        "hint": "仔细查看源代码的每一个角落",
    }


def _gen_logic():
    """生成逻辑推理题"""
    puzzles = [
        {
            "puzzle": "A说：B在撒谎。B说：C在撒谎。C说：A和B都在撒谎。\n已知只有一个人说真话，谁在说真话？",
            "answer": "B",
            "flag": "FLAG{logical_b}",
            "hint": "假设每个人说真话，看是否矛盾",
        },
        {
            "puzzle": "三个盒子分别标着'苹果'、'橘子'、'苹果和橘子'。\n已知所有标签都是错的。你从'苹果和橘子'盒子里拿出了一个苹果。\n这个盒子里实际装的是什么？另外两个呢？",
            "answer": "苹果, 橘子, 苹果和橘子",
            "flag": "FLAG{reverse_labels}",
            "hint": "标签全错，但拿出来的东西是真的",
        },
    ]
    p = random.choice(puzzles)
    return {"flag": p["flag"], "params": {"puzzle": p["puzzle"]}, "hint": p["hint"], "answer": p["answer"]}


def _gen_base64():
    """生成 Base64 解码题"""
    import base64
    words = ["OPEN", "HACK", "WINNER", "SHIELD", "PRISM"]
    word = random.choice(words)
    encoded = base64.b64encode(word.encode()).decode()
    flag = f"FLAG{{{word.lower()}}}"
    return {
        "flag": flag,
        "params": {"encoded": encoded},
        "hint": "这是一种常见的编码方式",
    }


def _gen_math():
    """生成数学谜题"""
    puzzles = [
        {
            "puzzle": "一个农夫带着一匹狼、一只羊和一棵白菜过河。\n船只能带一样东西。狼会吃羊，羊会吃白菜。\n最少需要几趟？",
            "answer": "7",
            "flag": "FLAG{river_crossing_7}",
            "hint": "记得回来也要坐船",
        },
        {
            "puzzle": "如果 3 只猫 3 分钟抓 3 只老鼠，\n100 只猫抓 100 只老鼠需要几分钟？",
            "answer": "3",
            "flag": "FLAG{parallel_cats}",
            "hint": "每只猫抓老鼠的速度是独立的",
        },
    ]
    p = random.choice(puzzles)
    return {"flag": p["flag"], "params": {"puzzle": p["puzzle"]}, "hint": p["hint"], "answer": p["answer"]}


def init(players, config=None):
    """初始化 CTF"""
    cfg = config or {}
    challenge_count = cfg.get("challenge_count", 5)
    difficulty = cfg.get("difficulty", "mixed")  # easy / medium / hard / mixed
    time_limit = cfg.get("time_limit", 0)  # 0 = 无限时，单位分钟

    # 生成题目
    challenges = []
    templates = list(CHALLENGE_TEMPLATES)
    random.shuffle(templates)

    for i in range(min(challenge_count, len(templates))):
        tpl = templates[i]
        generated = tpl["generate"]()
        challenges.append({
            "id": i + 1,
            "category": tpl["category"],
            "title": tpl["title"],
            "description": tpl["description"].format(**generated["params"]),
            "flag": generated["flag"],
            "hint": generated["hint"],
            "answer": generated.get("answer"),
            "points": random.choice([100, 200, 300, 500]),
            "solved_by": [],
        })

    # 玩家得分
    scores = {p: {"score": 0, "solved": [], "attempts": 0} for p in players}

    return {
        "game_type": "ctf",
        "phase": "playing",     # playing / finished
        "challenges": challenges,
        "scores": scores,
        "time_limit": time_limit,
        "start_time": None,     # 游戏开始时设置
        "end_time": None,
        "finish_order": [],     # 完成顺序（可选）
    }


def resolve(state, user, action_name, action_params):
    """解析动作"""
    hint = {"action": action_name, "player": user}

    if user not in state["scores"]:
        return state, {"error": f"玩家 {user} 不在游戏中"}

    if state["phase"] == "finished" and action_name != "scoreboard":
        return state, {"error": "比赛已结束"}

    if action_name == "submit":
        """提交 flag"""
        challenge_id = action_params.get("challenge_id")
        flag = action_params.get("flag", "").strip()

        if not challenge_id or not flag:
            return state, {"error": "缺少 challenge_id 或 flag"}

        ch = None
        for c in state["challenges"]:
            if c["id"] == challenge_id:
                ch = c
                break

        if not ch:
            return state, {"error": f"题目 {challenge_id} 不存在"}

        state["scores"][user]["attempts"] += 1

        if flag.upper() == ch["flag"].upper():
            if user not in ch["solved_by"]:
                ch["solved_by"].append(user)
                state["scores"][user]["score"] += ch["points"]
                state["scores"][user]["solved"].append(challenge_id)
                hint["narrative"] = f"正确！{user} 解出了「{ch['title']}」(+{ch['points']}分)"
                hint["correct"] = True
            else:
                hint["narrative"] = "你已经解过这道题了"
                hint["correct"] = False
        else:
            hint["narrative"] = f"Flag 不正确，再试试"
            hint["correct"] = False

    elif action_name == "hint":
        """获取提示"""
        challenge_id = action_params.get("challenge_id")
        if not challenge_id:
            return state, {"error": "缺少 challenge_id"}

        ch = None
        for c in state["challenges"]:
            if c["id"] == challenge_id:
                ch = c
                break

        if not ch:
            return state, {"error": f"题目 {challenge_id} 不存在"}

        hint["narrative"] = f"提示: {ch['hint']}"
        hint["needs_llm"] = False

    elif action_name == "challenges":
        """查看所有题目"""
        ch_list = []
        for c in state["challenges"]:
            ch_list.append({
                "id": c["id"],
                "category": c["category"],
                "title": c["title"],
                "description": c["description"],
                "points": c["points"],
                "solved": user in c["solved_by"],
                "solved_count": len(c["solved_by"]),
            })
        hint["narrative"] = ch_list
        hint["needs_llm"] = False

    elif action_name == "scoreboard":
        """查看排行榜"""
        board = []
        for p, s in sorted(state["scores"].items(), key=lambda x: -x[1]["score"]):
            board.append({
                "player": p,
                "score": s["score"],
                "solved": len(s["solved"]),
                "attempts": s["attempts"],
            })
        hint["narrative"] = board
        hint["needs_llm"] = False

    elif action_name == "finish":
        """结束比赛"""
        state["phase"] = "finished"
        state["end_time"] = time.time()
        hint["narrative"] = f"{user} 结束了比赛"
        hint["needs_llm"] = True

    elif action_name == "dynamic_challenge":
        """请求 LLM 生成动态题目"""
        category = action_params.get("category", "misc")
        difficulty = action_params.get("difficulty", "medium")
        new_id = max(c["id"] for c in state["challenges"]) + 1 if state["challenges"] else 1
        state["challenges"].append({
            "id": new_id,
            "category": category,
            "title": f"动态题目 #{new_id}",
            "description": f"[请 LLM 生成一道 {difficulty} 难度的 {category} 题目]",
            "flag": f"FLAG{{dynamic_{new_id}}}",
            "hint": "这是一道动态生成的题目",
            "points": {"easy": 100, "medium": 300, "hard": 500}.get(difficulty, 200),
            "solved_by": [],
            "dynamic": True,
        })
        hint["narrative"] = f"已创建动态题目 #{new_id}，等待 LLM 生成内容"
        hint["needs_llm"] = True

    else:
        return state, {"error": f"未知动作: {action_name}"}

    return state, hint


def check_win(state):
    """CTF 检查是否所有题都解完了"""
    all_solved = all(
        len(c["solved_by"]) > 0 for c in state["challenges"]
    )
    if all_solved and state["challenges"]:
        scores = state["scores"]
        best = max(scores.items(), key=lambda x: x[1]["score"])
        return {
            "winner": best[0],
            "message": f"所有题目已解出！最高分: {best[0]} ({best[1]['score']}分)",
            "final_scores": {
                p: s["score"] for p, s in sorted(scores.items(), key=lambda x: -x[1]["score"])
            }
        }
    if state.get("phase") == "finished":
        scores = state["scores"]
        best = max(scores.items(), key=lambda x: x[1]["score"])
        return {
            "winner": best[0],
            "message": f"比赛结束！最高分: {best[0]} ({best[1]['score']}分)",
            "final_scores": {
                p: s["score"] for p, s in sorted(scores.items(), key=lambda x: -x[1]["score"])
            }
        }
    return None
