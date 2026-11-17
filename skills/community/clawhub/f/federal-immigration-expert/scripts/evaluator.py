#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
federal-immigration-expert — 联邦移民通用算分引擎 (IRCC Express Entry, 本地, 不联网)
- CRS 1200 完整评分 + CEC/FSW/FST 三项目入池资格判定
- 输入: stdin 传 JSON profile (任意候选人), 或省略走示例
- 职业类别由 NOC 5位码首位自动推导
- 依据官方快照 data/snapshots/ircc-cec|fsw|fst-OFFICIAL.txt
"""
import json, sys

# ---- CRS 因子 (官方 CRS 评分网格, 2016年起结构稳定) ----
def age_points_single(a):
    if a is None: return None
    if 18 <= a <= 35: return 110
    a_map = {36:105,37:99,38:94,39:89,40:85,41:80,42:76,43:71,44:67,45:62,46:58,47:53,48:49,49:44,50:40}
    return a_map.get(a, 0)

def age_points_couple(a):
    if a is None: return None
    if 18 <= a <= 35: return 100
    a_map = {36:95,37:89,38:84,39:79,40:75,41:70,42:66,43:61,44:57,45:52,46:48,47:43,48:39,49:34,50:30}
    return a_map.get(a, 0)

def edu_points_single(edu):
    e = (edu or "").lower()
    if any(k in e for k in ("phd","doctor")): return 150
    if "master" in e: return 135
    if "bachelor" in e: return 120
    if "diploma" in e: return 98
    if "certificate" in e: return 90
    return 0

def canadian_exp_points(years):
    if years is None: return None
    y = int(years)
    if y < 1: return 0
    if y == 1: return 40
    if y == 2: return 53
    if y == 3: return 64
    if y >= 4: return 80
    return 40

def skill_transfer(profile):
    edu = (profile.get("highestEducation") or "").lower()
    clb = profile.get("lowestCLB")
    fy = profile.get("foreignYears") or 0
    total_pts = 0
    if clb is None: return 0, None
    st, stw = 0, None
    if clb >= 7:
        if fy >= 3: st = 50; stw = "学历+境外3年+CLB7+"
        elif fy >= 1: st = 25; stw = "学历+境外1年+CLB7+"
    elif clb >= 5:
        if fy >= 3: st = 50; stw = "学历+境外3年+CLB5/6+"
    total_pts = st
    return total_pts, stw

def additional_points(profile):
    pnp = profile.get("hasPNPNomination")
    fr = profile.get("hasFrenchCLB7")
    rel = profile.get("hasSiblingCanada")
    canedu = profile.get("canadianEducationYears")
    job = profile.get("hasJobOfferLMIA")
    pts = 0
    if pnp: pts += 600
    if fr: pts += 50
    if rel: pts += 15
    if canedu and canedu >= 2: pts += 15
    elif canedu == 1: pts += 0
    if job: pts += 50
    return pts

def evaluate_crs(profile):
    """returns (items, total, warnings). 仅核心因子 + 附加分."""
    it = []; total = 0; w = []
    age = profile.get("age")
    edu = profile.get("highestEducation")
    clb = profile.get("lowestCLB")
    fy = profile.get("foreignYears")
    cy = profile.get("canadaYears")
    spouse = profile.get("hasSpouse")

    # 核心
    ap_pts = age_points_couple(age) if spouse else age_points_single(age)
    it.append(("年龄(核心)", f"{age}岁", ap_pts, 110, "crs")); total += ap_pts or 0
    ep_pts = edu_points_single(edu)
    it.append(("学历(核心)", (edu or "缺").title(), ep_pts, 150, "crs")); total += ep_pts
    lw = {"speaking":36,"listening":32,"reading":34,"writing":32}  # CLB9 单项参考
    if clb is not None and clb >= 9:
        total_lang = 34+32+34+36
        it.append(("首官方语言(CLB9+)", "R/W/L/S 参考单项", total_lang, 136, "crs")); total += total_lang
    elif clb == 8:
        total_lang = 29+29+31+33
        it.append(("首官方语言(CLB8)", "R/W/L/S 参考单项", total_lang, 122, "crs")); total += total_lang
    elif clb == 7:
        total_lang = 25+25+27+28
        it.append(("首官方语言(CLB7)", "R/W/L/S 参考单项", total_lang, 105, "crs")); total += total_lang
    if cy is not None:
        cy_pts = canadian_exp_points(cy)
        it.append(("加拿大工作经验(核心)", f"{cy}年", cy_pts, 80, "crs")); total += (cy_pts or 0)
    # 技能转移
    st, stw_ = skill_transfer(profile)
    if st:
        it.append(("技能转移(交叉)", stw_ or "学历+境外工龄+CLB", st, 50, "crs")); total += st
    # 附加分
    add = additional_points(profile)
    if add:
        it.append(("附加分合计", "PNP/法语/亲属/加教育/job offer", add, 600, "crs")); total += add
    return it, total, w

def crs_framework(profile):
    """执行 CRS 估算并返回标准结构."""
    items, total, w = evaluate_crs(profile)
    return {"items": items, "total": total, "warnings": w,
            "note": "核心因子 + 附加分; 语言单项按官方 CRS 网格近似; 完整 CRS 1200 需配偶/交叉细分, 以 IRCC 官方计算器为准"}

# ================= 联邦三项目资格引擎 (CEC / FSW / FST) =================
# 依据: 官方快照 data/snapshots/ircc-cec|fsw|fst-OFFICIAL.txt (2026-08-21 抓取)

def _hours_ok(year_years, target_hours):
    """由年数(浮点)换算小时数判断是否达门槛."""
    if year_years is None:
        return None
    hours = year_years * 1560  # 1 全职年 ≈ 1560h
    return hours >= target_hours

def fsw_selection(profile):
    """FSW 67分选择因素表(官方). 返回 (items, total)."""
    it = []
    clb = profile.get("lowestCLB")
    fy = profile.get("foreignYears")
    cy = profile.get("canadaYears")
    age = profile.get("age")
    edu = (profile.get("highestEducation") or "").lower()
    job = profile.get("hasJobOfferLMIA")
    spouse_clb = profile.get("spouseCLB")
    has_sibling = profile.get("hasSiblingCanada")
    total = 0

    # 语言 (第一官方 + 第二官方)
    lang1 = {10:6, 9:6, 8:5, 7:4}.get(clb, 0) if clb is not None else 0
    lang_pts = lang1 * 4 if clb is not None else 0  # 4 abilities
    sec = 4 if (profile.get("secondLangCLB5", False)) else 0
    lang_pts += sec
    it.append(("语言(第一官方4项)", f"CLB {clb}", lang1*4 if clb is not None else None, 24, "fsw"))
    it.append(("语言(第二官方)", "CLB5+(4分)" if sec else "无", sec, 4, "fsw"))
    total += lang_pts

    # 学历 25
    edu_pts = {"phd":25, "master":23, "bachelor":21, "two":22, "diploma":15, "certificate":19}
    edu_key = None
    if "phd" in edu or "doctor" in edu: edu_key = "phd"
    elif "master" in edu: edu_key = "master"
    elif "bachelor" in edu: edu_key = "bachelor"
    elif "diploma" in edu: edu_key = "diploma"
    ep = edu_pts.get(edu_key, 0) if edu_key else 0
    it.append(("学历", (edu or "缺").title() if edu_key else "缺(需ECA认定)", ep if edu_key else None, 25, "fsw"))
    total += ep

    # 工种经验(取境内外较长) 15
    yrs = max([fy or 0, cy or 0])
    exp = 9 if yrs >= 1 else 0
    exp = 11 if yrs >= 2 else exp
    exp = 13 if yrs >= 4 else exp
    exp = 15 if yrs >= 6 else exp
    it.append(("技术工作经验", f"{yrs:.1f}年" if (fy is not None or cy is not None) else "缺", exp, 15, "fsw"))
    total += exp

    # 年龄 12
    age_map = {36:11,37:10,38:9,39:8,40:7,41:6,42:5,43:4,44:3,45:2,46:1}
    age_p = 12 if (age is not None and 18 <= age <= 35) else age_map.get(age, 0)
    it.append(("年龄", f"{age}岁" if age is not None else "缺", age_p, 12, "fsw"))
    total += age_p

    # 安排工作 10
    job_p = 10 if job else 0
    it.append(("安排就业(有效job offer)", "有" if job else "无", job_p, 10, "fsw"))
    total += job_p

    # 适应能力 10
    adapt = 0
    if spouse_clb and spouse_clb >= 4: adapt += 5
    if has_sibling: adapt += 5
    if job: adapt += 5
    it.append(("适应能力", f"{adapt}/10(配偶语言/加国经历/亲属等)", adapt, 10, "fsw"))
    total += adapt

    return it, total

def feed_eligibility(profile):
    """判定候选人对 CEC/FSW/FST 三项目的入池资格. 返回 (items, warnings)."""
    w = []
    it = []
    cy = profile.get("canadaYears")
    fy = profile.get("foreignYears")
    clb = profile.get("lowestCLB")
    teer = profile.get("teer")
    # 若给了NOC但没给teer, 自动推导
    noc = profile.get("noc")
    if teer is None and noc:
        n = str(noc).strip()
        if n.isdigit() and len(n) >= 2:
            teer = int(n[1])
    job = profile.get("hasJobOfferLMIA")
    coq = profile.get("hasCoq")
    is_trade = profile.get("isTrade", False)  # FST仅适用于技工类NOC

    # CEC
    can_h = _hours_ok(cy, 1560)
    clb_min_cec = 7 if (teer in (0,1)) else 5 if (teer in (2,3)) else None
    if clb is not None and clb_min_cec is not None:
        cec_ok_lang = clb >= clb_min_cec
        lang_s = f"达标(需≥{clb_min_cec})" if cec_ok_lang else f"未达标(需≥{clb_min_cec}, 现{clb})"
    else:
        cec_ok_lang = None; lang_s = f"缺CLB/缺TEER(需≥{clb_min_cec})" if clb_min_cec else "需先确认TEER"
    cec_ok = (can_h is True) and (cec_ok_lang is not False) and (teer in (0,1,2,3) or teer is None)
    it.append(("CEC 资格", "加国1,560h+语言+TEER0-3", "符合" if cec_ok else ("待核" if cec_ok is None else "不符"), "—", "ircc-cec-OFFICIAL"))
    it.append(("   ·CEC 工龄(1,560h/近3年)", f"{'达标' if can_h else ('缺' if can_h is None else '未达标')}", None, None, "cec"))
    it.append(("   ·CEC 语言(CLB)", lang_s, None, None, "cec"))

    # FSW
    fsw_items, fsw_67 = fsw_selection(profile)
    fsw_min = (fy is not None and fy >= 1) or (cy is not None and cy >= 1)
    fsw_lang = (clb is not None and clb >= 7)
    fsw_ok = fsw_min and fsw_lang and (fsw_67 is not None and fsw_67 >= 67)
    it.append(("FSW 资格", "1年技术工+CLB7+67分/100", "符合" if fsw_ok else "不符", "—", "ircc-fsw-OFFICIAL"))
    it.append(("   ·FSW 67分表", f"{fsw_67 if fsw_67 is not None else '缺数据'}/100", fsw_67 if isinstance(fsw_67,int) else None, 100, "fsw"))
    for sub in fsw_items:
        it.append(("      "+sub[0], sub[1], sub[2], sub[3], "fsw"))

    # FST (需技工类NOC + 3,120h(境内外均可) + 技工offer或资格证)
    fst_total = (fy or 0) + (cy or 0)
    fst_hours = _hours_ok(fst_total, 3120)
    has_offer_or_coq = bool(coq or job)
    if not is_trade:
        fst_ok = False
        fst_reason = "职业非技工类(NOC工单), FST不适用"
    else:
        fst_ok = (fst_hours is True) and has_offer_or_coq and (clb is not None and clb >= 4)
        fst_reason = ""
    it.append(("FST 资格", "3,120h技工+offer/技工证+语言", "符合" if fst_ok else "不符", "—", "ircc-fst-OFFICIAL"))
    it.append(("   ·FST 工时(3,120h)", f"{'达标' if fst_hours else ('缺' if fst_hours is None else '未达标')}", None, None, "fst"))
    it.append(("   ·技工 offer/证书", "有" if has_offer_or_coq else "无", None, None, "fst"))
    it.append(("   ·是否为技工NOC", "是" if is_trade else "否(软件工程师等非技工→FST不适用)", None, None, "fst"))
    return it, w

def main():
    raw = sys.stdin.read().strip()
    if raw:
        try:
            profile = json.loads(raw)
        except Exception as e:
            print(json.dumps({"error": f"JSON parse error: {e}"}, ensure_ascii=False)); sys.exit(1)
    else:
        # 示例候选人 (仅供演示)
        profile = {
            "age": 30, "hasSpouse": False,
            "noc": "21232",
            "lowestCLB": 9,
            "highestEducation": "Master",
            "foreignYears": 8, "canadaYears": 1.2,
            "hasJobOfferLMIA": True, "hasCoq": False,
            "secondLangCLB5": False, "spouseCLB": None, "hasSiblingCanada": False,
            "isTrade": False
        }

    result = crs_framework(profile)
    print("=" * 66)
    print("federal-immigration-expert — Express Entry CRS 估算 (满分1200)")
    print("=" * 66)
    for name, cond, p, mx, src in result["items"]:
        ps = str(p) if p is not None else "(缺)"
        print(f"{name:<26}{str(cond[:20]):<22}{ps:>4}{('/'+str(mx)):>7}")
    print("-" * 66)
    print(f"CRS 估算合计: {result['total']:>52}")
    for w in result["warnings"]:
        print("⚠", w)
    print("注:", result["note"])
    print()

    # 联邦三项目资格判定
    fed_items, fed_w = feed_eligibility(profile)
    print("=" * 66)
    print("联邦三项目资格判定 (CEC / FSW / FST)")
    print("-" * 66)
    for name, cond, p, mx, src in fed_items:
        ps = str(p) if p is not None else ("" if name.startswith(("   ","      ")) else "")
        pad_mx = ("" if mx is None else "/"+str(mx))
        print(f"{name:<30}{str(cond)[:22]:<24}{ps:>4}{pad_mx:>6}")
    for wv in fed_w:
        print("⚠", wv)
    print()
    print("### 以官方最终 IRCC 决定为准 ###")

if __name__ == "__main__":
    main()
