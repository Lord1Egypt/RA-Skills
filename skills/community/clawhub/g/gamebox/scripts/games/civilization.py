"""文明模拟 — 回合制策略，资源/科技/外交"""

import random


# 建筑定义
BUILDINGS = {
    "farm":       {"name": "农场",   "cost": {"food": 30, "gold": 10}, "effect": {"food": +5},   "category": "economy"},
    "mine":       {"name": "矿场",   "cost": {"gold": 20},            "effect": {"gold": +4},   "category": "economy"},
    "barracks":   {"name": "兵营",   "cost": {"gold": 50, "food": 20},"effect": {"military": +3},"category": "military"},
    "wall":       {"name": "城墙",   "cost": {"gold": 80},            "effect": {"defense": +5},"category": "military"},
    "library":    {"name": "图书馆", "cost": {"gold": 40},            "effect": {"science": +3},"category": "science"},
    "university": {"name": "大学",   "cost": {"gold": 80},            "effect": {"science": +6},"category": "science"},
    "market":     {"name": "市场",   "cost": {"gold": 50},            "effect": {"gold": +3, "trade": +2}, "category": "economy"},
    "temple":     {"name": "神庙",   "cost": {"gold": 60},            "effect": {"culture": +3}, "category": "culture"},
    "wonder":     {"name": "奇观",   "cost": {"gold": 200, "food": 50, "science": 50},
                   "effect": {"culture": +10, "prestige": +5}, "category": "wonder"},
}

# 科技树
TECHS = {
    "agriculture": {"name": "农业",     "cost": 10, "requires": [],                "unlocks": ["farm"]},
    "mining":      {"name": "采矿",     "cost": 15, "requires": [],                "unlocks": ["mine"]},
    "writing":     {"name": "文字",     "cost": 20, "requires": [],                "unlocks": ["library"]},
    "bronze":      {"name": "青铜冶炼", "cost": 30, "requires": ["mining"],        "unlocks": ["barracks"]},
    "math":        {"name": "数学",     "cost": 40, "requires": ["writing"],       "unlocks": ["university"]},
    "currency":    {"name": "货币",     "cost": 35, "requires": ["mining"],        "unlocks": ["market"]},
    "engineering": {"name": "工程学",   "cost": 50, "requires": ["bronze", "math"],"unlocks": ["wall", "wonder"]},
    "philosophy":  {"name": "哲学",     "cost": 45, "requires": ["writing"],       "unlocks": ["temple"]},
}

# 随机事件
EVENTS = [
    {"text": "丰收年！粮食产量翻倍", "effect": {"food": +30}, "type": "good"},
    {"text": "地震！摧毁了一些建筑", "effect": {"buildings_lost": 1}, "type": "bad"},
    {"text": "发现了金矿！", "effect": {"gold": +50}, "type": "good"},
    {"text": "瘟疫爆发！", "effect": {"food": -20, "population": -1}, "type": "bad"},
    {"text": "商队到来，带来贸易机会", "effect": {"gold": +20, "trade": +1}, "type": "good"},
    {"text": "学者来访，分享知识", "effect": {"science": +15}, "type": "good"},
    {"text": "叛乱！需要镇压", "effect": {"military": -2}, "type": "bad"},
    {"text": "和平繁荣时代", "effect": {"culture": +10}, "type": "good"},
]


def init(players, config=None):
    """初始化文明模拟"""
    cfg = config or {}
    max_rounds = cfg.get("max_rounds", 30)

    civs = {}
    for p in players:
        civs[p] = {
            "name": p,
            "population": 3,
            "max_population": 5,
            "resources": {
                "food": 50, "gold": 50, "science": 0,
                "military": 0, "culture": 0, "defense": 0,
                "trade": 0, "prestige": 0,
            },
            "buildings": [],
            "techs": [],
            "researching": None,
            "research_progress": 0,
            "war_with": [],
            "alive": True,
        }

    return {
        "game_type": "civilization",
        "phase": "play",
        "round": 1,
        "max_rounds": max_rounds,
        "civs": civs,
        "events_log": [],
        "diplomacy": {},
        "trade_deals": [],
        "winner": None,
    }


def resolve(state, user, action_name, action_params):
    """解析动作"""
    hint = {"action": action_name, "player": user}

    if user not in state["civs"]:
        return state, {"error": f"文明 {user} 不存在"}
    civ = state["civs"][user]
    if not civ["alive"]:
        return state, {"error": "你的文明已灭亡"}

    if action_name == "build":
        building_id = action_params.get("building")
        if not building_id or building_id not in BUILDINGS:
            return state, {"error": f"未知建筑: {building_id}"}
        bld = BUILDINGS[building_id]
        # 检查科技前置
        tech_required = None
        for tid, t in TECHS.items():
            if building_id in t["unlocks"]:
                tech_required = tid
                break
        if tech_required and tech_required not in civ["techs"]:
            return state, {"error": f"需要先研究 {TECHS[tech_required]['name']}"}
        # 检查资源
        res = civ["resources"]
        for r, amt in bld["cost"].items():
            if res.get(r, 0) < amt:
                return state, {"error": f"资源不足: 需要 {amt} {r}"}
        for r, amt in bld["cost"].items():
            res[r] -= amt
        civ["buildings"].append(building_id)
        for r, amt in bld["effect"].items():
            res[r] = res.get(r, 0) + amt
        hint["narrative"] = f"{user} 建造了 {bld['name']}"
        hint["needs_llm"] = True

    elif action_name == "research":
        tech_id = action_params.get("tech")
        if not tech_id or tech_id not in TECHS:
            return state, {"error": f"未知科技: {tech_id}"}
        tech = TECHS[tech_id]
        if tech_id in civ["techs"]:
            return state, {"error": f"已研究 {tech['name']}"}
        for req in tech["requires"]:
            if req not in civ["techs"]:
                return state, {"error": f"需要先研究 {TECHS[req]['name']}"}
        civ["researching"] = tech_id
        hint["narrative"] = f"{user} 开始研究 {tech['name']}（{tech['cost']} 科学点）"
        hint["needs_llm"] = False

    elif action_name == "propose_trade":
        target = action_params.get("target")
        offer = action_params.get("offer", {})
        request = action_params.get("request", {})
        if not target or target not in state["civs"] or target == user:
            return state, {"error": "目标无效"}
        state["trade_deals"].append({
            "from": user, "to": target, "offer": offer,
            "request": request, "status": "pending", "round": state["round"],
        })
        hint["narrative"] = f"{user} 向 {target} 提出贸易"
        hint["needs_llm"] = True

    elif action_name == "respond_trade":
        deal_id = action_params.get("deal_id")
        accept = action_params.get("accept", False)
        deals = [d for d in state["trade_deals"] if d["to"] == user and d["status"] == "pending"]
        if deal_id is None or deal_id < 0 or deal_id >= len(deals):
            return state, {"error": "无效贸易编号"}
        deal = deals[deal_id]
        if accept:
            deal["status"] = "accepted"
            fc = state["civs"][deal["from"]]
            tc = civ
            for r, a in deal["offer"].items():
                fc["resources"][r] = fc["resources"].get(r, 0) - a
                tc["resources"][r] = tc["resources"].get(r, 0) + a
            for r, a in deal["request"].items():
                tc["resources"][r] = tc["resources"].get(r, 0) - a
                fc["resources"][r] = fc["resources"].get(r, 0) + a
            hint["narrative"] = f"{user} 接受了贸易"
        else:
            deal["status"] = "rejected"
            hint["narrative"] = f"{user} 拒绝了贸易"
        hint["needs_llm"] = True

    elif action_name == "declare_war":
        target = action_params.get("target")
        if not target or target not in state["civs"] or target == user:
            return state, {"error": "目标无效"}
        if target in civ.get("war_with", []):
            return state, {"error": "已在交战中"}
        civ["war_with"].append(target)
        state["civs"][target]["war_with"].append(user)
        state["diplomacy"][tuple(sorted([user, target]))] = {
            "status": "war", "declared_by": user, "round": state["round"]
        }
        hint["narrative"] = f"{user} 向 {target} 宣战！"
        hint["needs_llm"] = True

    elif action_name == "make_peace":
        target = action_params.get("target")
        if not target or target not in state["civs"]:
            return state, {"error": "目标无效"}
        if target not in civ.get("war_with", []):
            return state, {"error": "没有在交战中"}
        civ["war_with"].remove(target)
        state["civs"][target]["war_with"].remove(user)
        key = tuple(sorted([user, target]))
        if key in state["diplomacy"]:
            state["diplomacy"][key]["status"] = "peace"
        hint["narrative"] = f"{user} 与 {target} 讲和"
        hint["needs_llm"] = True

    elif action_name == "attack":
        target = action_params.get("target")
        if not target or target not in civ.get("war_with", []):
            return state, {"error": "只能攻击交战中文明"}
        my_mil = civ["resources"].get("military", 0)
        enemy_def = state["civs"][target]["resources"].get("defense", 0)
        if my_mil > enemy_def:
            damage = my_mil - enemy_def + random.randint(1, 5)
            ec = state["civs"][target]
            ec["resources"]["food"] = max(0, ec["resources"].get("food", 0) - damage)
            hint["narrative"] = f"{user} 攻击 {target}，造成 {damage} 点粮食损失"
        else:
            hint["narrative"] = f"{user} 攻击 {target} 失败，防御太强"
        hint["needs_llm"] = True

    elif action_name == "status":
        hint["narrative"] = {
            "civ": user, "population": civ["population"],
            "resources": civ["resources"],
            "buildings": [BUILDINGS[b]["name"] for b in civ["buildings"]],
            "techs": [TECHS[t]["name"] for t in civ["techs"]],
            "researching": TECHS[civ["researching"]]["name"] if civ["researching"] else None,
            "war_with": civ.get("war_with", []),
        }
        hint["needs_llm"] = False

    elif action_name == "world_status":
        overview = {}
        for p, c in state["civs"].items():
            overview[p] = {
                "alive": c["alive"], "population": c["population"],
                "score": sum(c["resources"].values()),
                "techs": len(c["techs"]), "buildings": len(c["buildings"]),
            }
        hint["narrative"] = {"round": state["round"], "civs": overview}
        hint["needs_llm"] = False

    else:
        return state, {"error": f"未知动作: {action_name}"}

    return state, hint


def process_round_end(state):
    """回合结束处理"""
    events_this_round = []
    for p, civ in state["civs"].items():
        if not civ["alive"]:
            continue
        # 研究进度
        if civ["researching"]:
            tid = civ["researching"]
            civ["research_progress"] += civ["resources"].get("science", 0)
            if civ["research_progress"] >= TECHS[tid]["cost"]:
                civ["techs"].append(tid)
                civ["research_progress"] = 0
                civ["researching"] = None
        # 人口增长
        if civ["resources"].get("food", 0) > civ["population"] * 10:
            if civ["population"] < civ["max_population"]:
                civ["population"] += 1
                civ["resources"]["food"] -= 20
        # 粮食消耗
        civ["resources"]["food"] -= civ["population"] * 5
        if civ["resources"]["food"] < 0:
            civ["population"] = max(1, civ["population"] - 1)
            civ["resources"]["food"] = 0
        # 灭亡检查
        if civ["population"] <= 0:
            civ["alive"] = False

    # 随机事件（30% 概率）
    if random.random() < 0.3:
        evt = random.choice(EVENTS)
        events_this_round.append(evt)
        state["events_log"].append({"round": state["round"], "event": evt})

    state["round"] += 1
    return events_this_round


def check_win(state):
    """检查胜负"""
    # 超过最大回合数
    if state["round"] > state["max_rounds"]:
        alive = {p: c for p, c in state["civs"].items() if c["alive"]}
        if not alive:
            return {"winner": None, "message": "所有文明都灭亡了"}
        best = max(alive.items(), key=lambda x: sum(x[1]["resources"].values()))
        return {
            "winner": best[0],
            "message": f"回合上限达到！最高分: {best[0]} ({sum(best[1]['resources'].values())}分)",
        }

    # 只剩一个文明
    alive = [p for p, c in state["civs"].items() if c["alive"]]
    if len(alive) == 1:
        return {"winner": alive[0], "message": f"{alive[0]} 征服了所有文明，获得胜利！"}
    if len(alive) == 0:
        return {"winner": None, "message": "所有文明都灭亡了"}

    # 文化胜利
    for p, c in state["civs"].items():
        if c["alive"] and c["resources"].get("culture", 0) >= 50:
            return {"winner": p, "message": f"{p} 达成文化胜利！"}

    return None
