#!/usr/bin/env python3
"""
Module Forge 子技能 CLI — 功能二：按需求自动生成模组骨架（带 CR 平衡）

输入：玩家人数 / 等级 / 时长档 / 冒险类型 / 设定 / 基调
输出：带 CR 平衡预算的模组骨架 JSON（派系 / NPC / 分幕遭遇 / 钩子）

数据来源：
  - data/module_paradigms.json ：59 篇官方模组范式（选结构/节奏模板）
  - DMG 标准表：XP 阈值（按角色等级）、怪物 XP（按 CR）、多怪乘数
    （机制参考数据，用于平衡，怪物名可按费伦设定替换）

用法：
  python module_forge.py --players 4 --level 5 --duration medium --type 都市寻宝 \
                         --setting "被遗忘的国度/深水城" --tone 悬疑
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

SKILL_SCRIPTS = Path(__file__).resolve().parent.parent.parent / "scripts"
sys.path.insert(0, str(SKILL_SCRIPTS))

DATA_DIR = os.environ.get("DND_LENS_DATA") or (Path(__file__).resolve().parent.parent.parent / "data")
PARADIGMS = DATA_DIR / "module_paradigms.json"

# ---------------------------------------------------------------------------
# DMG 标准表（机制参考）
# ---------------------------------------------------------------------------
# XP 阈值（每角色·每场），索引 = 等级 1..20 → [Easy, Medium, Hard, Deadly]
XP_THRESHOLDS = {
    1: [25, 50, 75, 100], 2: [50, 100, 150, 200], 3: [75, 150, 225, 400],
    4: [125, 250, 375, 500], 5: [250, 500, 750, 1100], 6: [300, 600, 900, 1400],
    7: [350, 750, 1100, 1700], 8: [450, 900, 1400, 2100], 9: [550, 1100, 1600, 2400],
    10: [600, 1200, 1900, 2800], 11: [800, 1600, 2400, 3600], 12: [1000, 2000, 3000, 4500],
    13: [1100, 2200, 3400, 5100], 14: [1250, 2500, 3800, 5700], 15: [1400, 2800, 4300, 6400],
    16: [1600, 3200, 4800, 7200], 17: [2000, 3900, 5900, 8800], 18: [2100, 4200, 6300, 9500],
    19: [2400, 4900, 7200, 10900], 20: [2700, 5700, 8300, 12700],
}
DIFF = ["Easy", "Medium", "Hard", "Deadly"]
DIFF_CN = {"Easy": "轻松", "Medium": "中等", "Hard": "困难", "Deadly": "致命"}

# 怪物 XP（按 CR）。CR 用分数键：0.125=1/8, 0.25=1/4, 0.5=1/2
MONSTER_XP = {
    0: 10, 0.125: 25, 0.25: 50, 0.5: 100, 1: 200, 2: 450, 3: 700, 4: 1100,
    5: 1800, 6: 2300, 7: 2900, 8: 3900, 9: 5000, 10: 5900, 11: 7200, 12: 8400,
    13: 10000, 14: 11500, 15: 13000, 16: 15000, 17: 18000, 18: 20000, 19: 22000,
    20: 25000, 21: 33000, 22: 41000, 23: 50000, 24: 62000, 25: 75000, 26: 90000,
}

# 多怪乘数（DMG）
def count_multiplier(n: int) -> float:
    if n <= 1: return 1.0
    if n == 2: return 1.5
    if n <= 6: return 2.0
    if n <= 10: return 2.5
    if n <= 14: return 3.0
    return 4.0

# 建议怪物花名册（SRD / 常见，CR 为键；可按费伦设定替换）
ROSTER = {
    0.125: ["强盗 Bandit", "狗头人 Kobold", "巨鼠 Giant Rat"],
    0.25: ["哥布林 Goblin", "狼 Wolf", "骷髅 Skeleton", "僵尸 Zombie"],
    0.5: ["兽人 Orc", "侦察兵 Scout"],
    1: ["恐狼 Dire Wolf", "食尸鬼 Ghoul", "大地精 Hobgoblin", "幽影 Specter"],
    2: ["食人魔 Ogre", "巨鹰 Giant Eagle"],
    3: ["枭熊 Owlbear", "狼人 Werewolf", "骑士 Knight"],
    4: ["双头巨人 Ettin"],
    5: ["巨魔 Troll", "丘陵巨人 Hill Giant"],
    7: ["石化蜥蜴 Basilisk"],
    8: ["刺客 Assassin"],
    10: ["幼年红龙 Young Red Dragon"],
    17: ["成年红龙 Adult Red Dragon"],
}

DURATION_MAP = {"short": 2, "medium": 3, "long": 5}      # 分幕数
DURATION_ENCOUNTERS = {"short": (2, 3), "medium": (4, 6), "long": (8, 10)}


# ---------------------------------------------------------------------------
# 选取范式
# ---------------------------------------------------------------------------
def load_paradigms():
    with open(PARADIGMS, encoding="utf-8") as f:
        return json.load(f)


def level_overlap(range_val, level):
    """range_val 形如 '1-5' / '1–5' / '5+' 或含这些字符串的列表；返回是否与 level 重叠。"""
    if not range_val:
        return True
    candidates = range_val if isinstance(range_val, list) else [range_val]
    for range_str in candidates:
        if not isinstance(range_str, str):
            continue
        m = re.match(r"(\d+)\s*[-–]\s*(\d+)", range_str)
        if m:
            lo, hi = int(m.group(1)), int(m.group(2))
            if lo <= level <= hi or abs(level - (lo + hi) / 2) <= 2:
                return True
        m = re.match(r"(\d+)\s*\+", range_str)
        if m and level >= int(m.group(1)):
            return True
    return False


def pick_paradigms(paradigms, level, adv_type, duration, k=3):
    scored = []
    for p in paradigms:
        s = 0
        if level_overlap(p.get("level_range"), level):
            s += 2
        at = p.get("adventure_type") or []
        if adv_type and any(adv_type in (t or "") for t in at):
            s += 2
        if p.get("duration_tier") and duration in p["duration_tier"]:
            s += 1
        # 时长档语义匹配
        if p.get("duration_tier"):
            dt = p["duration_tier"]
            if ("短" in dt and duration == "short") or ("中" in dt and duration == "medium") \
               or ("长" in dt and duration == "long") or ("战役" in dt and duration == "long"):
                s += 1
        scored.append((s, p))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [p for _, p in scored[:k]]


# ---------------------------------------------------------------------------
# CR 平衡
# ---------------------------------------------------------------------------
def party_threshold(level, players, diff_idx):
    per = XP_THRESHOLDS.get(level, XP_THRESHOLDS[20])[diff_idx]
    return per * players


def suggest_encounter(target_xp, level, climax=False):
    """在 [level-4, level+(3 if climax else 2)] 的 CR 窗口内，选出利用率最高的怪物组合。"""
    cr_floor = max(0.0, level - 4)
    cr_ceiling = level + (3 if climax else 2)
    candidates = [(cr, xp) for cr, xp in MONSTER_XP.items()
                  if cr_floor <= cr <= cr_ceiling]
    best = None
    for cr, xp in candidates:
        for count in (1, 2, 3, 4, 5, 6):
            adj = int(xp * count * count_multiplier(count))
            if adj <= target_xp:
                # 利用率越高越好，且偏好更接近目标
                util = adj / target_xp
                score = util
                if best is None or score > best[0]:
                    best = (score, cr, count, adj)
    if not best:
        return None
    _, cr, count, adj = best
    names = ROSTER.get(cr, [f"CR{cr} 怪物"])
    # 同一 CR 用一种代表性怪物重复（如「5 匹恐狼」），更符合遭遇直觉
    monsters = [names[0]] * count
    return {"cr": cr, "count": count, "adjusted_xp": adj, "xp_total": adj,
            "monsters": monsters, "xp_each": MONSTER_XP[cr]}


# ---------------------------------------------------------------------------
# 组装模组
# ---------------------------------------------------------------------------
def build_module(args):
    paradigms = load_paradigms()
    level = args.level
    players = args.players
    duration = args.duration
    acts_n = DURATION_MAP[duration]
    enc_min, enc_max = DURATION_ENCOUNTERS[duration]
    total_enc = (enc_min + enc_max) // 2

    # 注入经历映射草稿（功能三 → 功能二串联）：覆盖 title/premise/npcs/factions/locations
    draft = {}
    draft_path = getattr(args, "draft", None)
    if draft_path:
        p = Path(draft_path)
        if p.exists():
            try:
                draft = json.loads(p.read_text(encoding="utf-8")) or {}
            except json.JSONDecodeError:
                draft = {}
    title = draft.get("title") or f"《{args.setting or '费伦'}·未命名冒险》"
    premise = draft.get("premise", "")
    npcs = draft.get("npcs", [])
    factions = draft.get("factions", [])
    locations = draft.get("locations", [])

    refs = pick_paradigms(paradigms, level, args.type, duration)
    ref_titles = [r["title"] for r in refs]

    # 分幕：每幕分配遭遇，最后一幕为致命高潮
    acts = []
    enc_per_act = max(1, round(total_enc / acts_n))
    diff_plan = []
    for i in range(acts_n):
        if i == acts_n - 1:
            diff_plan.append(3)          # 致命高潮
        elif i == 0:
            diff_plan.append(1)          # 开场中等偏易
        else:
            diff_plan.append(2)          # 中段困难
    # 若幕数多于计划，补齐
    while len(diff_plan) < acts_n:
        diff_plan.insert(-1, 2)

    for i, d in enumerate(diff_plan):
        budget = party_threshold(level, players, d)
        enc = suggest_encounter(budget, level, climax=(d == 3))
        scene = {
            "act": i + 1,
            "beat": "探索/社交" if i % 2 == 0 else "潜入/调查",
            "encounter": {
                "difficulty": DIFF[d],
                "difficulty_cn": DIFF_CN[DIFF[d]],
                "party_budget_xp": budget,
                "suggested": enc,
            } if enc else {"difficulty": DIFF[d], "party_budget_xp": budget,
                           "suggested": None, "note": "无合适花名册怪物，请人工指定"},
        }
        acts.append(scene)

    # 锚点（可选：用 world-lore 检索地点/派系）
    anchors = []
    if args.anchor:
        try:
            from lens_rag import WorldLens
            lens = WorldLens()
            cards = lens.search(args.anchor, top_k=3,
                                types=["location", "faction"])
            anchors = [{"title": c["title"], "type": c["type"],
                        "source": c["source_file"]} for c in cards]
        except Exception:
            pass

    module = {
        "title": title,
        "premise": premise,
        "meta": {
            "players": players,
            "level": level,
            "duration_tier": duration,
            "adventure_type": args.type,
            "setting": args.setting,
            "tone": args.tone,
        },
        "paradigm_reference": ref_titles,
        "party_cr_budget_per_encounter": {
            DIFF[d]: party_threshold(level, players, d) for d in range(4)
        },
        "acts": acts,
        "npcs": npcs,
        "factions": factions,
        "locations": locations,
        "anchors": anchors,
        "hook": f"（由 DM 据基调「{args.tone or '未知'}」撰写开篇钩子；参考范式：{', '.join(ref_titles)}）",
        "notes": "怪物为 CR 平衡建议，可按费伦原生怪物替换；用 world-lore 子技能检索地点/派系锚点以保证设定一致性。",
    }
    return module


def main():
    p = argparse.ArgumentParser(description="Module Forge 子技能 CLI（功能二）")
    p.add_argument("--players", type=int, required=True, help="玩家人数")
    p.add_argument("--level", type=int, required=True, help="队伍等级（取起始等级）")
    p.add_argument("--duration", choices=["short", "medium", "long"], required=True,
                   help="时长档：short(2-3场)/medium(4-6场)/long(8-10场·战役级)")
    p.add_argument("--type", default="", help="冒险类型（如 都市寻宝/地城探险/恐怖）")
    p.add_argument("--setting", default="被遗忘的国度/费伦", help="设定（默认费伦）")
    p.add_argument("--tone", default="", help="基调（如 悬疑/史诗/黑色幽默）")
    p.add_argument("--anchor", default="", help="可选：检索设定锚点的关键词")
    p.add_argument("--draft", default="", help="可选：注入经历映射草稿 JSON（覆盖 title/premise/npcs/factions/locations）")
    p.add_argument("--json", action="store_true", help="输出紧凑 JSON")
    args = p.parse_args()

    mod = build_module(args)
    if args.json:
        print(json.dumps(mod, ensure_ascii=False))
    else:
        print(json.dumps(mod, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
