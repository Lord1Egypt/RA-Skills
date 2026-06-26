"""文字冒险 RPG — LLM 当地牢主，脚本管状态"""

from common import gen_id


def init(players, config=None):
    """初始化 RPG 世界状态"""
    cfg = config or {}
    setting = cfg.get("setting", "fantasy")  # fantasy / scifi / modern / horror

    templates = {
        "fantasy": {
            "world_name": "艾尔德兰大陆",
            "description": "一片充满魔法与冒险的奇幻大陆",
            "locations": ["新手村", "幽暗森林", "矿洞深处", "王城", "龙巢"],
        },
        "scifi": {
            "world_name": "银河联邦空间站",
            "description": "漂浮在未知星系的巨大空间站",
            "locations": ["船员舱", "实验室", "引擎室", "指挥台", "未知区域"],
        },
        "modern": {
            "world_name": "迷雾城市",
            "description": "一座被迷雾笼罩的神秘都市",
            "locations": ["咖啡馆", "图书馆", "地下室", "天台", "废弃工厂"],
        },
        "horror": {
            "world_name": "无尽宅邸",
            "description": "一座不断变化的恐怖宅邸",
            "locations": ["玄关", "走廊", "卧室", "地下室", "阁楼"],
        },
    }

    tpl = templates.get(setting, templates["fantasy"])

    # 每个玩家初始状态
    player_states = {}
    for p in players:
        player_states[p] = {
            "hp": 100,
            "max_hp": 100,
            "mp": 50,
            "max_mp": 50,
            "location": tpl["locations"][0],
            "inventory": [],
            "equipped": {},
            "quests": [],
            "stats": {"str": 10, "dex": 10, "int": 10, "cha": 10},
            "level": 1,
            "xp": 0,
            "gold": 0,
        }

    # 世界状态
    world = {
        "time": 1,  # 游戏内时间单位
        "weather": "晴朗",
        "events_log": [],
        "npcs": {},  # 位置 → NPC 列表
        "items_on_ground": {},  # 位置 → 物品列表
    }

    return {
        "game_type": "rpg",
        "setting": setting,
        "world_name": tpl["world_name"],
        "description": tpl["description"],
        "locations": tpl["locations"],
        "players": player_states,
        "world": world,
        "phase": "exploration",  # exploration / combat / dialogue / event
    }


def resolve(state, user, action_name, action_params):
    """
    解析动作，返回 (new_state, narrative_hint)
    narrative_hint 是给 LLM 的提示，让 LLM 生成叙事描述
    """
    players = state["players"]
    if user not in players:
        return state, {"error": f"玩家 {user} 不在游戏中"}

    p = players[user]
    hint = {"action": action_name, "player": user}
    new_state = state  # 尽量原地修改

    if action_name == "move":
        target = action_params.get("target", "")
        if not target:
            hint["error"] = "移动目标未指定"
            return new_state, hint
        if target not in state["locations"]:
            hint["error"] = f"未知地点: {target}"
            return new_state, hint
        old = p["location"]
        p["location"] = target
        hint["narrative"] = f"{user} 从 {old} 移动到 {target}"
        hint["needs_llm"] = True

    elif action_name == "look":
        loc = p["location"]
        hint["narrative"] = f"{user} 观察了 {loc} 的周围"
        hint["location"] = loc
        hint["needs_llm"] = True

    elif action_name == "take":
        item = action_params.get("item", "")
        loc = p["location"]
        ground = state["world"].get("items_on_ground", {}).get(loc, [])
        if item in ground:
            ground.remove(item)
            p["inventory"].append(item)
            hint["narrative"] = f"{user} 捡起了 {item}"
        else:
            hint["narrative"] = f"{user} 没有找到 {item}"
        hint["needs_llm"] = True

    elif action_name == "use":
        item = action_params.get("item", "")
        target_obj = action_params.get("target", "")
        if item in p["inventory"]:
            p["inventory"].remove(item)
            hint["narrative"] = f"{user} 使用了 {item}" + (f" 对 {target_obj}" if target_obj else "")
        else:
            hint["narrative"] = f"{user} 没有这个物品"
        hint["needs_llm"] = True

    elif action_name == "talk":
        npc = action_params.get("npc", "")
        topic = action_params.get("topic", "")
        hint["narrative"] = f"{user} 和 {npc} 交谈" + (f"，话题: {topic}" if topic else "")
        hint["needs_llm"] = True

    elif action_name == "fight":
        enemy = action_params.get("enemy", "")
        skill = action_params.get("skill", "普通攻击")
        hint["narrative"] = f"{user} 对 {enemy} 发动 {skill}"
        hint["needs_llm"] = True
        # 简化战斗：随机扣血，LLM 生成战斗描述
        import random
        dmg = random.randint(5, 20)
        hint["damage"] = dmg

    elif action_name == "rest":
        p["hp"] = min(p["max_hp"], p["hp"] + 30)
        p["mp"] = min(p["max_mp"], p["mp"] + 10)
        hint["narrative"] = f"{user} 休息了一会儿，恢复了体力"
        hint["needs_llm"] = True

    else:
        hint["error"] = f"未知动作: {action_name}"

    return new_state, hint


def check_win(state):
    """RPG 无明确胜负，始终返回 None（持续进行）"""
    return None
