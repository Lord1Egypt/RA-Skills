#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
融资适配研判引擎 · 离线规则引擎（零依赖，纯标准库）
用法：
    python match_engine.py profile.json
    python match_engine.py --demo
输出：双轨评分 + 分档判定 + 机构匹配清单 + 差距清单（JSON / 可读文本）

设计原则：所有判定规则显式可查、可改；不联网、不依赖第三方库；
         数据源为 data/institutions.json（由 references 蒸馏而来）。
"""
import json
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
REGISTRY = os.path.join(os.path.dirname(BASE), "data", "institutions.json")

# ---------------------------------------------------------------- 评分模型
# 权重固定写死，便于审计；改权重即改模型口径
VC_WEIGHTS = {
    "track_heat": 20,      # 赛道热度
    "team": 20,            # 团队背景
    "moat": 20,            # 技术壁垒
    "traction": 20,        # 商业化验证
    "ceiling": 10,         # 天花板
    "capital_path": 10,    # 资本路径
}
GOV_WEIGHTS = {
    "catalog": 25,         # 赛道目录匹配
    "location": 20,        # 注册地/落地意愿
    "rd_ip": 20,           # 研发与知识产权
    "team_qual": 15,       # 团队与资质
    "reflow": 10,          # 返投可行性
    "exit": 10,            # 退出预期
}

# 分档口径
BANDS = [
    (75, "强匹配", "现在就可以动手，优先接触名单已生成"),
    (60, "可争取", "能谈，但有明确短板，先补缺口再正式启动"),
    (45, "需补短板", "现在递了大概率被拒，先做 3–6 个月准备"),
    (0,  "暂不建议", "当前条件融资性价比低，建议走替代路径（见降级方案）"),
]

# 政策红利/冷宫赛道（与 references/03 保持一致；改这里即改判定）
# 注意：光伏/锂电的「过剩制造环节」已在 03 中列为冷宫，故此处不再把"光伏"当红利赛道。
HOT_TRACKS = [
    "半导体", "集成电路", "芯片", "EDA", "AI", "人工智能", "大模型", "具身智能",
    "机器人", "生物医药", "创新药", "医疗器械", "新能源", "储能", "钙钛矿",
    "低空经济", "eVTOL", "商业航天", "新材料", "高端装备", "工业母机",
    "量子", "光子", "合成生物", "智能驾驶", "半导体设备", "工业软件",
]
COLD_TRACKS = [
    "消费互联网", "O2O", "社区团购", "共享经济", "纯模式创新", "文化娱乐",
    "影视", "游戏", "教育培训", "房地产", "传统零售", "餐饮加盟",
    "光伏制造", "锂电制造", "硅料",
]

# 阶段序数：把机构阶段与项目阶段都映射到同一把尺子，用于阶段匹配过滤。
# 0=种子/天使  1=Pre-A  2=A轮  3=B轮  4=C轮及以后  5=成长期/Pre-IPO  6=并购
STAGE_WORDS = [
    (6, ("并购", "收购", "重组")),
    (5, ("pre-ipo", "preipo", "pre ipo", "成长期", "成长期至", "成熟期", "已上市")),
    (4, ("c轮", "d轮", "e轮", "后轮", "战略轮")),
    (3, ("b轮", "b+轮")),
    (2, ("a+轮", "a轮")),
    (1, ("pre-a", "prea", "pre a")),
    (0, ("天使", "种子", "seed", "概念", "极早期", "初创")),
]


def stage_ordinal(text):
    """把阶段描述文本映射为 0..6 的序数；无法识别返回 None。"""
    if not text:
        return None
    t = str(text).lower().replace("轮", "轮")
    hits = [n for n, words in STAGE_WORDS if any(w in t for w in words)]
    if not hits:
        return None
    return max(hits) if ("至" in t or "到" in t or "-" in t or "全覆盖" in t) else hits[0]


def stage_range(text):
    """机构覆盖阶段 → (min, max)。如 '天使至B轮' → (0, 3)。"""
    if not text or "全覆盖" in text:
        return (0, 5)
    t = str(text).lower()
    hits = [n for n, words in STAGE_WORDS if any(w in t for w in words)]
    if not hits:
        return (0, 5)
    return (min(hits), max(hits))


_SIZE_UNITS = {"亿": 10000.0, "万": 1.0}


def parse_size(text):
    """把机构单笔区间文本（如 '1000万-10亿元'）解析为 (min万, max万)；解析不出返回 None。"""
    if not text:
        return None
    import re as _re
    t = str(text).replace("人民币", "").replace("元", "").replace(" ", "")
    parts = _re.findall(r"(\d+(?:\.\d+)?)\s*(亿|万)?", t)
    vals = []
    for num, unit in parts:
        if not num:
            continue
        vals.append(float(num) * _SIZE_UNITS.get(unit, 1.0))
    if not vals:
        return None
    return (min(vals), max(vals))


def _band(score):
    for threshold, label, advice in BANDS:
        if score >= threshold:
            return label, advice
    return "暂不建议", ""


def score_vc(p):
    """市场化 VC 适配分。输入画像 dict，缺项按中性 0.5 计并记录缺失。"""
    missing = []
    s = {}

    # 赛道热度
    track = (p.get("track") or "").lower()
    if not track:
        missing.append("track（赛道）")
        s["track_heat"] = 0.5
    elif any(t.lower() in track or track in t.lower() for t in HOT_TRACKS):
        s["track_heat"] = 1.0
    elif any(t.lower() in track or track in t.lower() for t in COLD_TRACKS):
        s["track_heat"] = 0.15
    else:
        s["track_heat"] = 0.5

    # 团队背景：0-3 个加分项
    team = p.get("team") or {}
    if not team:
        missing.append("team（团队背景）")
        s["team"] = 0.4
    else:
        pts = 0
        if team.get("bigtech_or_topschool"):
            pts += 1
        if team.get("serial_founder"):
            pts += 1
        if team.get("industry_veteran"):
            pts += 1
        s["team"] = [0.15, 0.5, 0.8, 1.0][min(pts, 3)]

    # 技术壁垒
    moat = p.get("moat") or {}
    if not moat:
        missing.append("moat（技术壁垒）")
        s["moat"] = 0.4
    else:
        patents = int(moat.get("patents") or 0)
        soft = int(moat.get("copyrights") or 0)
        lead = bool(moat.get("tech_lead"))
        # 专利要分档，不能"有1项"和"有50项"同分
        if patents >= 10:
            pts = 1.5
        elif patents >= 3:
            pts = 1.0
        elif patents >= 1:
            pts = 0.5
        else:
            pts = 0.0
        if soft >= 3:
            pts += 1.0
        elif soft >= 1:
            pts += 0.5
        if lead:
            pts += 1.0
        s["moat"] = min(1.0, pts / 3.5)

    # 商业化验证
    tr = p.get("traction") or {}
    if not tr:
        missing.append("traction（商业化数据）")
        s["traction"] = 0.35
    else:
        rev = float(tr.get("revenue_wan") or 0)      # 年营收（万元）
        growth = float(tr.get("growth_pct") or 0)    # 同比增速 %
        paying = int(tr.get("paying_customers") or 0)
        pts = 0
        if rev >= 3000:
            pts += 2
        elif rev >= 500:
            pts += 1
        if growth >= 100:
            pts += 1
        elif growth >= 30:
            pts += 0.5
        if paying >= 10:
            pts += 1
        elif paying >= 3:
            pts += 0.5
        s["traction"] = min(1.0, pts / 4.0)

    # 天花板
    ceiling = p.get("market_size_yi")  # 可服务市场空间（亿元）
    if ceiling is None:
        missing.append("market_size_yi（市场空间）")
        s["ceiling"] = 0.5
    else:
        c = float(ceiling)
        s["ceiling"] = 1.0 if c >= 500 else 0.75 if c >= 100 else 0.45 if c >= 20 else 0.2

    # 资本路径
    path = (p.get("exit_path") or "").lower()
    if not path:
        missing.append("exit_path（退出路径）")
        s["capital_path"] = 0.4
    elif any(k in path for k in ("ipo", "上市", "科创板", "创业板", "北交所", "港股")):
        s["capital_path"] = 1.0
    elif any(k in path for k in ("并购", "收购", "被投")):
        s["capital_path"] = 0.75
    else:
        s["capital_path"] = 0.35

    total = sum(VC_WEIGHTS[k] * v for k, v in s.items())
    detail = {k: round(s[k], 2) for k in VC_WEIGHTS}
    return round(total, 1), detail, missing


def score_gov(p):
    """政府基金适配分。"""
    missing = []
    s = {}

    # 赛道目录匹配（权重最高）
    track = (p.get("track") or "").lower()
    if not track:
        missing.append("track（赛道）")
        s["catalog"] = 0.5
    elif any(t.lower() in track or track in t.lower() for t in HOT_TRACKS):
        s["catalog"] = 1.0
    elif any(t.lower() in track or track in t.lower() for t in COLD_TRACKS):
        s["catalog"] = 0.05
    else:
        s["catalog"] = 0.45

    # 注册地 / 落地意愿
    if p.get("willing_to_relocate") is True:
        s["location"] = 1.0
    elif p.get("locate_ok_in_zone") is True:
        s["location"] = 0.8
    elif p.get("willing_to_relocate") is False:
        s["location"] = 0.15
    else:
        missing.append("willing_to_relocate（是否愿迁址/落地）")
        s["location"] = 0.4

    # 研发与知识产权
    rd = p.get("rd") or {}
    if not rd:
        missing.append("rd（研发投入与知识产权）")
        s["rd_ip"] = 0.35
    else:
        ratio = float(rd.get("rd_ratio_pct") or 0)
        patents = int(rd.get("patents") or 0)
        soft = int(rd.get("copyrights") or 0)
        pts = 0
        if ratio >= 8:
            pts += 2
        elif ratio >= 4:
            pts += 1
        if patents >= 3:
            pts += 1
        if soft >= 2:
            pts += 1
        s["rd_ip"] = min(1.0, pts / 4.0)

    # 团队与资质
    qual = p.get("qualifications") or []
    team = p.get("team") or {}
    pts = 0
    if isinstance(qual, list):
        if any("高新" in str(q) for q in qual):
            pts += 1
        if any(("专精特新" in str(q)) or ("科技型" in str(q)) for q in qual):
            pts += 1
    if team.get("bigtech_or_topschool"):
        pts += 1
    if team.get("industry_veteran"):
        pts += 1
    s["team_qual"] = [0.15, 0.4, 0.65, 0.85, 1.0][min(pts, 4)]
    if not qual:
        missing.append("qualifications（高新/专精特新等资质）")

    # 返投可行性
    cap = p.get("local_capacity") or {}
    if not cap:
        missing.append("local_capacity（能否把产能/研发/订单落地）")
        s["reflow"] = 0.35
    else:
        pts = sum(1 for k in ("can_build", "can_hire", "can_order") if cap.get(k))
        s["reflow"] = [0.15, 0.45, 0.75, 1.0][min(pts, 3)]

    # 退出预期
    path = (p.get("exit_path") or "").lower()
    s["exit"] = 1.0 if any(k in path for k in ("ipo", "上市", "并购")) else 0.35

    total = sum(GOV_WEIGHTS[k] * v for k, v in s.items())
    detail = {k: round(s[k], 2) for k in GOV_WEIGHTS}
    return round(total, 1), detail, missing


# 反误报：这些字段属于"实质匹配项"。只命中尺寸/阶段类条件的，
# 不构成有效匹配（否则任何项目都会被"融资额在区间内"刷出名单）。
CORE_FIELDS = {
    "track", "moat.patents", "moat.copyrights", "moat.tech_lead",
    "traction.revenue_wan", "traction.growth_pct", "traction.paying_customers",
    "market_size_yi", "rd.rd_ratio_pct", "rd.patents", "rd.copyrights",
    "qualifications", "registered_in", "willing_to_relocate",
    "locate_ok_in_zone", "local_capacity.can_build",
    "local_capacity.can_hire", "local_capacity.can_order", "exit_path",
    "team.bigtech_or_topschool", "team.serial_founder", "team.industry_veteran",
}


def _is_core(cond):
    if isinstance(cond, str):
        return False
    return cond.get("field", "") in CORE_FIELDS


def match_institutions(p, kind):
    """从注册表匹配机构。kind: 'vc' | 'gov'。

    三级过滤（防误报）：
      ① 必须有 ≥1 条**实质条件**命中（赛道/技术/商业/资质/地域），否则不进名单；
      ② **阶段过滤**：项目所处阶段不在机构覆盖区间内的，单独归入"阶段不符"，
         不进推荐位（避免把天使基金和成长期基金同时推给同一个项目）；
      ③ **劝退项隔离**：命中任一 veto 信号的，一律不进推荐位，单独列出并说明原因。
    同时对 VC 做**单笔金额区间核对**，区间外的给出提示。
    """
    if not os.path.exists(REGISTRY):
        return None
    with open(REGISTRY, encoding="utf-8") as f:
        reg = json.load(f)
    pool = reg.get(kind) or []
    proj_stage = stage_ordinal(p.get("stage")) if kind == "vc" else None
    round_wan = p.get("round_size_wan")
    out = []
    for inst in pool:
        hits, met = 0, []
        core_hits = 0
        for cond in inst.get("match_signals", []):
            f_ok, desc = _eval_signal(cond, p)
            if f_ok:
                hits += 1
                if _is_core(cond):
                    core_hits += 1
                met.append(desc or (cond.get("label", "") if isinstance(cond, dict) else ""))
        veto = []
        for cond in inst.get("veto_signals", []):
            f_bad, desc = _eval_signal(cond, p)
            if f_bad:
                veto.append(desc or (cond.get("label", "") if isinstance(cond, dict) else ""))
        if not (hits and core_hits):
            continue

        # ② 阶段核对
        lo, hi = stage_range(inst.get("stage"))
        stage_ok = True
        stage_note = ""
        if proj_stage is not None:
            if proj_stage < lo:
                stage_ok = False
                stage_note = f"机构阶段为「{inst.get('stage')}」→ 你的项目偏早，此轮不在其射程"
            elif proj_stage > hi:
                stage_ok = False
                stage_note = f"机构阶段为「{inst.get('stage')}」→ 你的项目偏晚，早期基金接不住本轮体量"

        # ③ 金额核对（仅 VC，且只在阶段相符时提示）
        size_ok, size_note = True, ""
        if kind == "vc" and round_wan:
            rng = parse_size(inst.get("bet"))
            if rng:
                lo_s, hi_s = rng
                if float(round_wan) < lo_s * 0.5:
                    size_ok = False
                    size_note = f"机构单笔区间约 {inst.get('bet')} → 你的轮次偏小，可能达不到其起投线"
                elif float(round_wan) > hi_s * 2:
                    size_ok = False
                    size_note = f"机构单笔区间约 {inst.get('bet')} → 你的轮次偏大，需组合领投"

        tier = ("强" if core_hits >= 3 else "中" if core_hits == 2 else "弱") if stage_ok else "阶段不符"
        out.append({"name": inst.get("name"), "hits": hits,
                    "core_hits": core_hits, "tier": tier,
                    "met": met, "veto": veto,
                    "stage_ok": stage_ok, "stage_note": stage_note,
                    "size_ok": size_ok, "size_note": size_note,
                    "bank_stage": inst.get("stage"), "bet": inst.get("bet"),
                    "why": inst.get("why_you"), "gap": inst.get("what_you_lack"),
                    "apply": inst.get("apply_path")})
    out.sort(key=lambda x: (-x["core_hits"], -x["hits"], len(x["veto"])))
    return out


def split_matches(matches, limit=5):
    """四档归类，避免"一边推荐一边警示"：
      recommended —— 阶段相符、无劝退项、强/中匹配（进推荐位）
      conditional —— 命中但触发劝退项（说明原因，不进推荐位）
      weak        —— 弱相关（只提示，不作推荐）
      excluded    —— 阶段不符 / 金额明显不匹配（写明原因，省用户时间）
    """
    if not matches:
        return {"recommended": [], "conditional": [], "weak": [], "excluded": []}
    rec, cond, weak, excl = [], [], [], []
    for m in matches:
        if m.get("tier") == "阶段不符":
            excl.append(m)
        elif m["veto"]:
            cond.append(m)
        elif m["tier"] in ("强", "中") and not m.get("size_ok", True):
            # 阶段对、但有明确劝退项以外的硬伤（金额），降级为"有条件"
            cond.append(m)
        elif m["tier"] in ("强", "中"):
            rec.append(m)
        else:
            weak.append(m)
    return {"recommended": rec[:limit], "conditional": cond[:limit],
            "weak": weak[:limit], "excluded": excl[:limit]}


def _eval_signal(cond, p):
    """极简规则求值：{field, op, value}。field 支持点号取嵌套。"""
    if isinstance(cond, str):
        return False, cond
    field = cond.get("field", "")
    op = cond.get("op", "eq")
    val = cond.get("value")
    cur = p
    for part in field.split("."):
        if isinstance(cur, dict):
            cur = cur.get(part)
        else:
            cur = None
            break
    if cur is None:
        return False, cond.get("label", field)
    try:
        if op == "eq":
            return cur == val, cond.get("label", "")
        if op == "gte":
            return float(cur) >= float(val), cond.get("label", "")
        if op == "lte":
            return float(cur) <= float(val), cond.get("label", "")
        if op == "contains":
            return str(val).lower() in str(cur).lower(), cond.get("label", "")
        if op == "in":
            return any(str(v).lower() in str(cur).lower() for v in (val or [])), cond.get("label", "")
    except (TypeError, ValueError):
        return False, cond.get("label", field)
    return False, cond.get("label", "")


def diagnose(profile):
    vc_score, vc_detail, vc_missing = score_vc(profile)
    gov_score, gov_detail, gov_missing = score_gov(profile)
    vc_band, vc_advice = _band(vc_score)
    gov_band, gov_advice = _band(gov_score)

    def weakest(detail):
        return sorted(detail.items(), key=lambda kv: kv[1])[:3]

    return {
        "项目": profile.get("name") or "(未命名项目)",
        "市场化VC": {"得分": vc_score, "判定": vc_band, "建议": vc_advice,
                    "扣分最多": [k for k, _ in weakest(vc_detail)], "细项": vc_detail,
                    "缺失信息": vc_missing},
        "政府基金": {"得分": gov_score, "判定": gov_band, "建议": gov_advice,
                    "扣分最多": [k for k, _ in weakest(gov_detail)], "细项": gov_detail,
                    "缺失信息": gov_missing},
        "VC匹配清单": match_institutions(profile, "vc"),
        "政府基金匹配清单": match_institutions(profile, "gov"),
    }


DEMO = {
    "name": "某某智能——工业设备预测性维护",
    "track": "工业AI / 高端装备",
    "stage": "有收入成长期",
    "registered_in": "南宁",
    "willing_to_relocate": False,
    "locate_ok_in_zone": True,
    "team": {"bigtech_or_topschool": True, "serial_founder": False, "industry_veteran": True},
    "moat": {"patents": 6, "copyrights": 4, "tech_lead": True},
    "traction": {"revenue_wan": 1200, "growth_pct": 80, "paying_customers": 12},
    "market_size_yi": 300,
    "exit_path": "北交所 / 被产业方并购",
    "rd": {"rd_ratio_pct": 9, "patents": 6, "copyrights": 4},
    "qualifications": ["高新技术企业", "科技型中小企业"],
    "local_capacity": {"can_build": False, "can_hire": True, "can_order": True},
    "round_size_wan": 3000,
}


def main():
    if len(sys.argv) > 1 and sys.argv[1] != "--demo":
        with open(sys.argv[1], encoding="utf-8") as f:
            profile = json.load(f)
    else:
        profile = DEMO
    result = diagnose(profile)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
