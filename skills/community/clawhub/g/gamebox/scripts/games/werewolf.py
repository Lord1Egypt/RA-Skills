"""狼人杀 — 社交推理游戏"""

import random


# 角色定义
ROLES = {
    "werewolf": {"team": "wolf", "name": "狼人", "count_range": (1, 4)},
    "seer":     {"team": "good", "name": "预言家", "count_range": (1, 1)},
    "witch":    {"team": "good", "name": "女巫", "count_range": (0, 1)},
    "hunter":   {"team": "good", "name": "猎人", "count_range": (0, 1)},
    "guard":    {"team": "good", "name": "守卫", "count_range": (0, 1)},
    "villager": {"team": "good", "name": "村民", "count_range": (0, 99)},
}


def _assign_roles(player_count, config=None):
    """根据人数分配角色"""
    cfg = config or {}
    custom_roles = cfg.get("roles")  # 自定义角色配置

    if custom_roles:
        # 验证自定义配置
        total = sum(custom_roles.values())
        if total != player_count:
            return None, f"角色总数 {total} 不等于玩家数 {player_count}"
        roles = []
        for role, count in custom_roles.items():
            if role not in ROLES:
                return None, f"未知角色: {role}"
            roles.extend([role] * count)
        random.shuffle(roles)
        return roles, None

    # 自动分配
    wolf_count = max(1, player_count // 3)
    roles = ["werewolf"] * wolf_count
    remaining = player_count - wolf_count

    # 特殊角色
    specials = []
    if remaining >= 4:
        specials.append("seer")
        remaining -= 1
    if remaining >= 4:
        specials.append("witch")
        remaining -= 1
    if remaining >= 5:
        specials.append("hunter")
        remaining -= 1

    roles.extend(specials)
    roles.extend(["villager"] * remaining)
    random.shuffle(roles)
    return roles, None


def init(players, config=None):
    """初始化狼人杀"""
    cfg = config or {}
    player_count = len(players)

    roles, err = _assign_roles(player_count, cfg)
    if err:
        return {"error": err}

    # 分配角色给玩家
    player_roles = {}
    player_alive = {}
    for i, p in enumerate(players):
        player_roles[p] = roles[i]
        player_alive[p] = True

    # 女巫药水状态
    witch_state = {
        "antidote": True,   # 解药
        "poison": True,     # 毒药
    }

    return {
        "game_type": "werewolf",
        "phase": "night",           # night / day / vote
        "round": 1,
        "player_roles": player_roles,  # 用户名 → 角色（公开后可见）
        "player_alive": player_alive,
        "role_revealed": {p: False for p in players},  # 是否已公开角色
        "night_actions": {},       # 夜晚行动记录
        "vote_record": {},         # 投票记录 {round: {voter: target}}
        "deaths": {},              # 死亡记录 {round: [players]}
        "witch": witch_state,
        "guard_target": None,      # 本夜守卫保护对象
        "winner": None,
        "narrative_log": [],       # LLM 叙事日志
    }


def resolve(state, user, action_name, action_params):
    """解析动作"""
    hint = {"action": action_name, "player": user}

    if user not in state["player_alive"]:
        return state, {"error": "你已死亡，无法行动"}

    if not state["player_alive"][user]:
        return state, {"error": "你已死亡，无法行动"}

    phase = state["phase"]

    if action_name == "kill" and phase == "night":
        """狼人夜晚杀人"""
        if state["player_roles"][user] != "werewolf":
            return state, {"error": "只有狼人可以在夜晚杀人"}
        target = action_params.get("target")
        if not target or target not in state["player_alive"]:
            return state, {"error": "目标无效"}
        if not state["player_alive"][target]:
            return state, {"error": "目标已死亡"}
        if target == user:
            return state, {"error": "不能杀自己"}
        state["night_actions"][user] = {"action": "kill", "target": target}
        hint["narrative"] = f"狼人选择了猎杀目标"
        hint["needs_llm"] = False  # 夜晚动作不公开

    elif action_name == "check" and phase == "night":
        """预言家查验"""
        if state["player_roles"][user] != "seer":
            return state, {"error": "只有预言家可以查验"}
        target = action_params.get("target")
        if not target or target not in state["player_alive"]:
            return state, {"error": "目标无效"}
        role = state["player_roles"][target]
        is_wolf = ROLES[role]["team"] == "wolf"
        state["night_actions"][user] = {"action": "check", "target": target}
        hint["narrative"] = f"查验结果: {target} 是 {'狼人' if is_wolf else '好人'}"
        hint["secret"] = True  # 仅预言家可见
        hint["result"] = {"target": target, "is_wolf": is_wolf}

    elif action_name == "save" and phase == "night":
        """女巫救人"""
        if state["player_roles"][user] != "witch":
            return state, {"error": "只有女巫可以救人"}
        if not state["witch"]["antidote"]:
            return state, {"error": "解药已用完"}
        target = action_params.get("target")
        state["night_actions"][user] = {"action": "save", "target": target}
        state["witch"]["antidote"] = False
        hint["secret"] = True

    elif action_name == "poison" and phase == "night":
        """女巫毒人"""
        if state["player_roles"][user] != "witch":
            return state, {"error": "只有女巫可以毒人"}
        if not state["witch"]["poison"]:
            return state, {"error": "毒药已用完"}
        target = action_params.get("target")
        state["night_actions"][user] = {"action": "poison", "target": target}
        state["witch"]["poison"] = False
        hint["secret"] = True

    elif action_name == "protect" and phase == "night":
        """守卫保护"""
        if state["player_roles"][user] != "guard":
            return state, {"error": "只有守卫可以保护"}
        target = action_params.get("target", user)
        state["night_actions"][user] = {"action": "protect", "target": target}
        state["guard_target"] = target
        hint["secret"] = True

    elif action_name == "vote" and phase == "vote":
        """投票放逐"""
        target = action_params.get("target")
        if not target or target not in state["player_alive"]:
            return state, {"error": "目标无效"}
        rnd = state["round"]
        if str(rnd) not in state["vote_record"]:
            state["vote_record"][str(rnd)] = {}
        state["vote_record"][str(rnd)][user] = target
        hint["narrative"] = f"{user} 投票放逐 {target}"
        hint["needs_llm"] = True

    elif action_name == "speak":
        """发言（白天讨论）"""
        content = action_params.get("content", "")
        if not content:
            return state, {"error": "发言内容为空"}
        hint["narrative"] = f"{user}: {content}"
        hint["needs_llm"] = False

    elif action_name == "reveal_role":
        """公开自己的角色"""
        claimed = action_params.get("role", state["player_roles"][user])
        state["role_revealed"][user] = claimed
        hint["narrative"] = f"{user} 声称自己是 {ROLES.get(claimed, {}).get('name', claimed)}"
        hint["needs_llm"] = True

    else:
        phase_hint = f"当前阶段: {phase}"
        return state, {"error": f"无效动作 '{action_name}'。{phase_hint}"}

    return state, hint


def check_win(state):
    """检查胜负条件"""
    alive = {p: r for p, r in state["player_roles"].items() if state["player_alive"][p]}
    wolves = [p for p, r in alive.items() if ROLES[r]["team"] == "wolf"]
    goods = [p for p, r in alive.items() if ROLES[r]["team"] == "good"]

    if not wolves:
        return {"winner": "good", "message": "所有狼人已被消灭，好人胜利！"}
    if len(wolves) >= len(goods):
        return {"winner": "wolf", "message": "狼人数量不少于好人，狼人胜利！"}
    return None
