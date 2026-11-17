#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
资产体检计算器（asset-health-check）—— 纯标准库零依赖

用途：读用户手填的脱敏 assets.json → 静态计算 → 出 Markdown 体检卡（health_card.md）。

硬约束（对应方案 §12，违反任何一条即设计错误）：
1. 只读静态存量数据，不接行情 API、不接交易接口、不做任何代操作（红线 2）。
2. 只输出"事实 + 中性经验区间 + 信息缺口"，绝不下"偏高/偏低/该买该卖/是骗局"判断（红线 1）。
3. 结论只用"手填(可信)"数据；AI 识别未核对项不进结论，只列待核对清单（修洞 #4）。
4. 缺必填字段 → 相关指标标"信息不全，仅出框架不出结论"，不崩、不编造（优雅降级）。
5. 输出前用 _COMPLIANCE_BLOCKLIST 自扫，命中即告警（上架前 grep 闸的运行时版）。

用法：
    python health_check.py --input assets.json [--output health_card.md]
    （省略 --output 时打印到 stdout）

输入 JSON 结构见同目录 ../references/ 中的说明，或方案文档 §12.1。
"""

import argparse
import csv
import json
import re
import sys
from datetime import datetime
from pathlib import Path

# Windows 控制台中文输出兜底
if sys.stdout and hasattr(sys.stdout, "buffer"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# ---------------------------------------------------------------------------
# 合规自检黑名单（§12.4）：输出前自扫，命中即告警
# 词形覆盖：荐股/点位/收益承诺/偏高偏低判断/替产品定性/不可逆操作指令
# ---------------------------------------------------------------------------
_COMPLIANCE_BLOCKLIST = [
    # 荐股/荐基金/荐保险（"推荐"类判断）
    "推荐买", "推荐卖", "建议买入", "建议卖出",
    "买哪只", "卖哪只", "买什么基金", "买什么股票", "买什么保险",
    "荐股", "荐基", "选哪只", "换哪只",
    # 买卖点位 / 择时指令
    "点位", "抄底", "逃顶", "加仓", "减仓", "清仓", "满仓", "梭哈",
    "止盈点", "止损点", "该止盈", "该止损", "逢低买入", "逢高卖出",
    # 收益承诺
    "稳赚", "保本高收益", "保本保息", "年化收益可达", "月入过万", "躺赚", "翻倍",
    # 偏高/偏低类判断（工具只报事实+中性区间）
    "偏高", "偏低", "过高", "过低", "不足", "超标",
    # 替产品定性（红线：不给"是骗局"结论）
    "是骗局", "是坑", "是杀猪盘", "是诈骗", "被割",
    # 不可逆操作指令（红线 1：只给自查路径，不给结论）
    "该退保", "应退保", "退掉", "该卖房", "该卖车", "该辞职", "该借贷",
    "该调仓", "应该调仓", "该全部赎回", "该赎回",
]

# 强判断词：这些词即使处于"拒绝/引导"行内，也只允许紧跟否定前缀时豁免，
# 不适用整行白名单（防止「应急金不足（经验区间 3-6）」这类真判断随行混进输出）。
_STRONG_JUDGMENT_WORDS = {"偏高", "偏低", "过高", "过低", "不足", "超标",
                          "该退保", "应退保", "该卖房", "该卖车", "该辞职", "该借贷",
                          "该调仓", "该全部赎回", "该赎回"}
# 强判断词的合法用法：词前紧邻 4 字内出现否定句式（"不判"偏高"""不设标准线"等）
_STRONG_NEGATION_PREFIXES = ("不判", "不下", "不设", "不算", "不称", "不叫", "不出现")

# 四桶（§12.1 bucket 取值）→ 中文
BUCKET_NAMES = {
    "flexible": "灵活取用",
    "steady": "稳健",
    "growth": "进取",
    "protection": "保障",
}

# 中国官方自查入口映射（§12.2 独门表）
OFFICIAL_ENTRIES = [
    ("银行卡全貌", "云闪付「一键查卡」", "查名下所有银行卡（含睡眠卡）"),
    ("股票/基金持仓", "中国证券登记结算「一码通」", "查名下股票与基金持仓"),
    ("名下保单", "金事通（中国银保信）", "查名下所有保单"),
    ("医保/门慢特病", "国家医保服务平台 App", "查医保报销记录/门慢特病备案"),
    ("养老金/社保", "电子社保卡 / 掌上12333", "查缴费记录/估算养老金"),
]

# 风险承受 → 权益占比中性经验区间（只作对照，不判偏高偏低）
EQUITY_RANGE = {
    "conservative": (10, 40),
    "balanced": (30, 70),
    "aggressive": (50, 90),
    None: (20, 80),
}

# ---- 常见类别关键词 → 四桶自动归类（仅在用户没填 bucket 时兜底，归入即提示） ----
_AUTO_BUCKET_RULES = [
    (("现金", "活期", "定期存款", "货币基金", "货基", "余额宝", "零钱", "随时", "备用金"), "flexible"),
    (("债券", "债基", "国债", "固收", "定期理财", "理财"), "steady"),
    (("股票", "股基", "指数基金", "混合基金", "权益", "ETF"), "growth"),
    (("保险", "年金", "寿险", "保单"), "protection"),
]


def _auto_bucket(cat):
    """按类别关键词猜测四桶。返回 bucket 或 None。"""
    for kws, bucket in _AUTO_BUCKET_RULES:
        if any(kw in cat for kw in kws):
            return bucket
    return None


def _fmt_money(v):
    """金额格式化：无小数用整数显示。"""
    if v is None:
        return "—"
    if isinstance(v, float) and v == int(v):
        v = int(v)
    return f"{v:,.2f}" if isinstance(v, float) else f"{v:,}"


def _fmt_pct(v):
    return f"{v:.1f}%" if v is not None else "—"


def _load(data):
    """安全取数：非数字返回 None。"""
    if isinstance(data, bool):
        return None
    if isinstance(data, (int, float)):
        return float(data)
    return None


def _load_amount(v):
    """资产/负债金额载荷：负数视为无效（疑似负债误填进资产、退款记错的正负号），
    返回 None 由调用方记入信息缺口，绝不静默进结论。"""
    x = _load(v)
    return x if (x is not None and x >= 0) else None


def compute(data):
    """静态计算核心。返回 (指标 dict, 信息缺口 list, 待核对清单 list)。"""
    indicators = {}
    gaps = []
    pending = []

    assets = data.get("assets") or []
    liabilities = data.get("liabilities") or []
    ai_items = data.get("ai_identified_items") or []

    # ---- 可信度分流：结论只用"手填(可信)"资产/负债 ----
    trusted_assets = []
    for a in assets:
        if isinstance(a, dict) and _load_amount(a.get("amount")) is not None:
            trusted_assets.append(a)
        elif isinstance(a, dict):
            if _load(a.get("amount")) is not None:
                gaps.append(f"资产项「{a.get('cat', '未命名')}」金额为负（疑似负债误填进资产或负号笔误），"
                            "请核对后重录，本次未计入计算")
            else:
                gaps.append(f"资产项「{a.get('cat', '未命名')}」缺有效金额，未计入计算")
    trusted_liab = []
    for l in liabilities:
        if isinstance(l, dict) and _load_amount(l.get("amount")) is not None:
            trusted_liab.append(l)
        elif isinstance(l, dict):
            if _load(l.get("amount")) is not None:
                gaps.append(f"负债项「{l.get('item', '未命名')}」金额为负，请核对后重录，本次未计入计算")
            else:
                gaps.append(f"负债项「{l.get('item', '未命名')}」缺有效金额，未计入计算")

    # ---- AI 识别项：未核对不进结论；已核对(reviewed:true)视同手填并入计算 ----
    merged_reviewed = []
    for it in ai_items:
        if not isinstance(it, dict):
            continue
        if it.get("reviewed") is True or it.get("needs_review") is False:
            if _load_amount(it.get("amount")) is not None:
                merged_reviewed.append(it)
            else:
                gaps.append(f"AI 识别项「{it.get('cat', '未命名')}」已核对但缺有效金额，未并入")
        else:
            pending.append(f"「{it.get('cat', '未命名')}」约 {_fmt_money(_load(it.get('amount')))} 元（来源：AI 识别，请人工核对）")
    if merged_reviewed:
        # 已核对项并入可信资产参与计算（用户核对 = 用户确认为事实）
        trusted_assets.extend(merged_reviewed)
        indicators["merged_reviewed_count"] = len(merged_reviewed)
        indicators["merged_reviewed_sum"] = sum(_load(a.get("amount")) or 0 for a in merged_reviewed)
        indicators["merged_reviewed_cats"] = [a.get("cat", "未命名") for a in merged_reviewed]
    else:
        indicators["merged_reviewed_count"] = 0

    # ---- 净资产 ----
    total_assets = sum(_load(a.get("amount")) or 0 for a in trusted_assets)
    total_liab = sum(_load(l.get("amount")) or 0 for l in trusted_liab)
    indicators["total_assets"] = total_assets if trusted_assets else None
    indicators["total_liabilities"] = total_liab if trusted_liab else None
    if trusted_assets or trusted_liab:
        indicators["net_worth"] = total_assets - total_liab
    else:
        indicators["net_worth"] = None
        gaps.append("资产/负债数据缺失或全为无效金额 → 净资产不可算，仅出框架")

    # ---- 四桶占比 ----
    bucket_sums = {k: 0.0 for k in BUCKET_NAMES}
    unmatched = []
    auto_bucketed = []
    for a in trusted_assets:
        b = a.get("bucket")
        cat = a.get("cat", "未命名")
        if b in bucket_sums:
            bucket_sums[b] += _load(a.get("amount")) or 0
        else:
            guess = _auto_bucket(str(cat))
            if guess:
                bucket_sums[guess] += _load(a.get("amount")) or 0
                auto_bucketed.append((cat, BUCKET_NAMES[guess]))
            else:
                unmatched.append(cat)
    if auto_bucketed:
        detail = "、".join(f"「{c}」→{b}" for c, b in auto_bucketed)
        gaps.append(f"以下资产项未标 bucket，已按类别关键词自动归桶（请核对）：{detail}")
    if unmatched:
        gaps.append(f"以下资产项无法归类（bucket 缺失且类别无法识别），未入桶：{', '.join(unmatched)}")
    if total_assets > 0:
        indicators["buckets"] = {
            k: (v / total_assets * 100) for k, v in bucket_sums.items()
        }
    else:
        indicators["buckets"] = None
        gaps.append("无可信资产数据 → 四桶占比不可算")

    # ---- 应急金月数（flexible 桶 / 月支出）----
    me = _load(data.get("monthly_expense"))
    if me and me > 0 and trusted_assets:
        flexible = bucket_sums["flexible"]
        indicators["emergency_months"] = flexible / me
        indicators["emergency_expense"] = me
    else:
        indicators["emergency_months"] = None
        if me is None:
            gaps.append("缺 monthly_expense（月刚性支出）→ 应急金月数不可算")
        elif not trusted_assets:
            gaps.append("无可信资产数据 → 应急金月数不可算")

    # ---- 权益占比 = growth / (growth + steady) ----
    denom = bucket_sums["growth"] + bucket_sums["steady"]
    if denom > 0:
        indicators["equity_pct"] = bucket_sums["growth"] / denom * 100
    else:
        indicators["equity_pct"] = None
        gaps.append("进取/稳健桶为空或无数据 → 权益占比不可算")

    # ---- 集中度：任一资产类别占总额 >50% → 报事实 ----
    cat_sums = {}
    for a in trusted_assets:
        cat_sums[a.get("cat", "未命名")] = cat_sums.get(a.get("cat", "未命名"), 0.0) + (_load(a.get("amount")) or 0)
    concentration = []
    if total_assets > 0:
        for cat, s in sorted(cat_sums.items(), key=lambda x: -x[1]):
            pct = s / total_assets * 100
            if pct > 50:
                concentration.append((cat, pct))
    indicators["concentration"] = concentration

    # ---- 矛盾事实（只列，不下结论）----
    contradictions = []
    # 强绝对化表述：正常投资产品不该这样宣传，出现即列为事实（无需数字）
    ABSOLUTE_WORDS = ("绝对安全", "稳赚", "零风险", "包赔", "不会亏", "无风险")
    # 弱信号："保本"在合规产品话术里也存在，需同时配收益数字才列
    WEAK_SAFE = ("保本",)
    RETURN_WORDS = ("年化", "收益", "息", "回报", "赚")
    for a in trusted_assets:
        note = str(a.get("note") or "")
        amt = _load(a.get("amount"))
        cat = a.get("cat", "未命名")
        has_ret = any(w in note for w in RETURN_WORDS)
        abs_hit = next((w for w in ABSOLUTE_WORDS if w in note), None)
        if abs_hit and has_ret:
            contradictions.append(f"「{cat}」备注同时出现\"{abs_hit}\"与收益表述（{_fmt_money(amt)} 元）"
                                  "——\"零风险+有收益\"属矛盾表述，请自行核实产品性质，工具不判断")
        elif ("保本" in note) and has_ret and any(c.isdigit() for c in note):
            contradictions.append(f"「{cat}」备注含「保本」且宣称收益数字（{_fmt_money(amt)} 元）"
                                  "——请自行核实产品性质，工具不判断")
    eq = indicators.get("equity_pct")
    em = indicators.get("emergency_months")
    if (em is not None and em < 1) and (eq is not None and eq >= 70):
        contradictions.append(
            f"应急金现状约 {em:.1f} 个月，权益占比 {eq:.1f}%（进取桶占比显著高于稳健桶）——两项事实并列供你自查，工具不判断")

    indicators["contradictions"] = contradictions

    # ---- 负债率（只报事实，无经验区间——各家庭结构差异大，不设"标准线"）----
    if total_assets > 0 and trusted_liab:
        indicators["debt_ratio"] = total_liab / total_assets * 100
    else:
        indicators["debt_ratio"] = None
    liab_items = [f"{l.get('item', '未命名')} {_fmt_money(_load(l.get('amount')))}" for l in trusted_liab]
    indicators["liability_items"] = liab_items

    # ---- 保障（事实陈述 + 引导自查，不荐险种）----
    ins = data.get("insurance_flagged") or []
    indicators["insurance_flagged"] = [str(x) for x in ins if isinstance(x, str)]
    missing_std = [x for x in ("重疾险", "医疗险") if x not in indicators["insurance_flagged"]]
    indicators["insurance_missing_std"] = missing_std

    # ---- 现金流月报（P2-1：收入-支出-结余率 + 532 对照，纯事实）----
    mi = _load(data.get("monthly_income"))
    if mi and mi > 0:
        indicators["monthly_income"] = mi
        if me and me > 0:
            indicators["monthly_surplus"] = mi - me
            indicators["savings_rate"] = (mi - me) / mi * 100
        # 532 对照（教学框架的事实参照，非建议）：收入分配三段
        indicators["income_532"] = {
            "need": mi * 0.5, "save": mi * 0.3, "invest": mi * 0.2,
        }
    elif mi is not None and mi <= 0:
        gaps.append("monthly_income 非正数，现金流月报不可算")

    # ---- 负债成本事实卡（P2-2：按利率降序 + 高息事实置顶；只排序列事实，不替用户决定先还哪个）----
    debt_items = []
    for l in trusted_liab:
        rate = _load(l.get("rate"))
        if rate is not None:
            debt_items.append({
                "item": l.get("item", "未命名"),
                "amount": _load(l.get("amount")) or 0,
                "rate": rate,
            })
        else:
            debt_items.append({
                "item": l.get("item", "未命名"),
                "amount": _load(l.get("amount")) or 0,
                "rate": None,
            })
    indicators["debt_cost_items"] = debt_items
    # 高息事实线：年化 ≥ 18%（常见信用卡分期实际年化区间下缘）仅作事实标注，非指令
    indicators["high_rate_items"] = [d for d in debt_items if d["rate"] is not None and d["rate"] >= 18]

    # ---- 大额决策测算（P2-3：月供压力事实——月供/月收入比，只算不判）----
    housing = data.get("housing_loan_plan") or {}
    loan_amount = _load(housing.get("loan_amount"))
    years = _load(housing.get("years"))
    rate_annual = _load(housing.get("rate_annual"))
    if loan_amount and loan_amount > 0 and years and years > 0 and rate_annual is not None and rate_annual >= 0:
        n = years * 12
        r_m = rate_annual / 100 / 12
        if r_m == 0:
            monthly_payment = loan_amount / n
        else:
            monthly_payment = loan_amount * r_m * (1 + r_m) ** n / ((1 + r_m) ** n - 1)
        indicators["housing_plan"] = {
            "loan_amount": loan_amount, "years": years, "rate_annual": rate_annual,
            "monthly_payment": monthly_payment,
        }
        mi2 = indicators.get("monthly_income")
        if mi2 and mi2 > 0:
            indicators["housing_plan"]["payment_to_income"] = monthly_payment / mi2 * 100
    elif housing:
        gaps.append("housing_loan_plan 字段不全（需 loan_amount/years/rate_annual）→ 月供测算不可算")

    return indicators, gaps, pending


def render_card(data, indicators, gaps, pending):
    """渲染 Markdown 体检卡（§12.3 结构固定）。"""
    exp = data.get("experience", "L1")
    risk_tol = data.get("risk_tolerance")
    lines = []
    add = lines.append

    add("【家庭资产体检卡】")
    add("")
    add("> 非投资建议，仅供自查；数据基于你手填，判断权在你，具体以持牌机构为准。")
    add("> 本工具只做静态存量分析：不接行情、不买卖、不代操作、不下\"偏高/偏低\"判断。")
    add("> 覆盖口径：本卡仅统计本次录入的项目；未录入的资产（如房产、公积金）不计入——缺项会让净资产与负债率失真。")
    add("")

    # ⓪ 一屏速览（社交货币卡：三核心数 + 最扎眼事实一条，§12.3）
    add("## ⚡ 一屏速览")
    add("")
    nw = indicators.get("net_worth")
    em = indicators.get("emergency_months")
    eq = indicators.get("equity_pct")
    speed = []
    if nw is not None:
        speed.append(f"净资产 **{_fmt_money(nw)}** 元")
    if em is not None:
        speed.append(f"应急金 **{em:.1f}** 个月（参考 3–6）")
    if eq is not None:
        speed.append(f"高风险投资占比 **{eq:.0f}%**（参考 20%–80%）")
    if speed:
        add(" · ".join(speed))
    else:
        add("数据不全，暂无核心数——补齐后重跑即可。")
    contradictions = indicators.get("contradictions") or []
    conc = indicators.get("concentration") or []
    eye = []
    if contradictions:
        eye.append(contradictions[0].split("——")[0])
    if conc:
        eye.append(f"「{conc[0][0]}」单类占 {conc[0][1]:.0f}%")
    if eye:
        add("")
        add(f"最值得你注意的事实：{'；'.join(eye)}。")
    add("")
    add("*（各项明细、经验区间与官方查验入口见下方分区；本速览同样只有事实，没有判断。）*")
    add("")

    # 一、家底全景（事实）
    add("## 一、家底全景（事实）")
    add("")
    nw = indicators.get("net_worth")
    ta = indicators.get("total_assets")
    tl = indicators.get("total_liabilities")
    if nw is not None:
        tag = "手填(可信)"
        add(f"- 总资产：{_fmt_money(ta)} 元（{tag}）")
        add(f"- 总负债：{_fmt_money(tl)} 元（{tag}）")
        add(f"- **净资产 = 资产 {_fmt_money(ta)} − 负债 {_fmt_money(tl)} = {_fmt_money(nw)} 元**（{tag}）")
        dr = indicators.get("debt_ratio")
        if dr is not None:
            add(f"- 负债率 = 总负债 ÷ 总资产 = {dr:.1f}%（事实呈现；家庭负债结构差异大，无统一\"标准线\"，"
                "如需评估请咨询持牌机构）")
        li_items = indicators.get("liability_items") or []
        if li_items:
            add(f"- 负债构成：{'；'.join(li_items)}（房贷请按剩余本金计）")
    else:
        add("- 净资产：**信息不全，仅出框架不出结论**（请补资产/负债明细后重跑）")
    add("")
    add("### 四桶占比（占可信资产总额）")
    add("")
    bks = indicators.get("buckets")
    if bks:
        for k in ("flexible", "steady", "growth", "protection"):
            add(f"- {BUCKET_NAMES[k]}：{_fmt_pct(bks.get(k))}")
    else:
        add("- 四桶占比：信息不全（请给资产项标注 bucket：flexible/steady/growth/protection）")
    add("")

    # 二、中性对照（事实 + 经验区间，零判断）
    add("## 二、中性对照（只给事实与经验区间，不替你下结论）")
    add("")
    em = indicators.get("emergency_months")
    if em is not None:
        add(f"- **应急金**：现状约 {em:.1f} 个月（经验区间 3–6 个月；口径说明：灵活取用桶全部，"
            "其中含 1 年内要花的钱，实际应急覆盖可能略低）→ 请对照第 4 章自查")
    else:
        add("- **应急金**：信息不全（缺月支出或资产数据），仅出框架：应急金经验区间 3–6 个月生活费，请对照第 4 章自查")
    eq = indicators.get("equity_pct")
    lo, hi = EQUITY_RANGE.get(risk_tol, EQUITY_RANGE[None])
    if eq is not None:
        tol_txt = {"conservative": "保守型", "balanced": "平衡型", "aggressive": "进取型"}.get(risk_tol, "未填风险承受")
        add(f"- **权益占比**：现状 {eq:.1f}%（你自填风险承受 = {tol_txt}；该类型常见经验区间 {lo}%–{hi}%，"
            f"全人群常见经验区间 20%–80%）→ 请对照第 4 章自查")
    else:
        add("- **权益占比**：信息不全（进取/稳健桶无数据）。框架：权益占比 = 进取桶 ÷（进取桶 + 稳健桶），"
            "常见经验区间 20%–80%（随风险承受而异）→ 请对照第 4 章自查")
    conc = indicators.get("concentration") or []
    if conc:
        for cat, pct in conc:
            add(f"- **集中度事实**：「{cat}」占可信资产 {_fmt_pct(pct)}（单类占比高建议自行复核分散，工具不点名换哪只）")
    else:
        add("- **集中度**：可信数据内无单类占比 >50% 的事实")
    ins = indicators.get("insurance_flagged") or []
    missing_ins = indicators.get("insurance_missing_std") or []
    missing_txt = f"；你的数据里未提及：{'、'.join(missing_ins)}" if missing_ins else ""
    add(f"- **保障**：名下已持有保险 {len(ins)} 项（{('、'.join(ins)) if ins else '未标记任何险种'}）{missing_txt}。"
        "是否覆盖重疾/医疗请对照第 3 章自查，工具不荐险种")
    add("")
    add("> 注：以上均为\"事实 + 经验区间\"，工具不判\"偏高/偏低\"，判断权在你。")
    add("")

    # 三、信息缺口 & 官方自查入口
    add("## 三、信息缺口 & 官方自查入口")
    add("")
    if gaps:
        add("本次体检发现的信息缺口：")
        add("")
        for g in gaps:
            add(f"- {g}")
        add("")
    add("官方自查入口（数据在你自己手里，登录官方渠道即可）：")
    add("")
    add("| 缺口 | 官方入口 | 作用 |")
    add("|---|---|---|")
    for a, b, c in OFFICIAL_ENTRIES:
        add(f"| {a} | {b} | {c} |")
    add("")

    # 待核对清单（AI 识别项）
    if pending:
        add("## 待核对清单（AI 识别，未核对不进结论）")
        add("")
        for p in pending:
            add(f"- {p}")
        add("")
        add("核对无误后，把该项标 `\"reviewed\": true` 再重跑，即并入体检计算。")
        add("")

    # 已核对并入提示
    if indicators.get("merged_reviewed_count"):
        add("## 已并入的核对项（你确认过的事实）")
        add("")
        add(f"- 本次有 {indicators['merged_reviewed_count']} 项 AI 识别数据经你核对后并入计算："
            f"{'、'.join(indicators['merged_reviewed_cats'])}，合计 {_fmt_money(indicators['merged_reviewed_sum'])} 元")
        add("")

    # 矛盾事实
    contradictions = indicators.get("contradictions") or []
    if contradictions:
        add("## 风险揭示（只列矛盾事实，不下结论）")
        add("")
        for c in contradictions:
            add(f"- {c}")
        add("")

    # 三点五、现金流月报 / 负债成本 / 月供测算（P2 扩展：有数据才出节，纯事实）
    mi = indicators.get("monthly_income")
    surplus = indicators.get("monthly_surplus")
    savings_rate = indicators.get("savings_rate")
    i532 = indicators.get("income_532")
    debt_cost = indicators.get("debt_cost_items") or []
    high_rate = indicators.get("high_rate_items") or []
    hp = indicators.get("housing_plan")

    if mi is not None:
        add("## 3.1 现金流月报（事实）")
        add("")
        me_r = _load(data.get("monthly_expense"))
        rows = [f"- 月收入：{_fmt_money(mi)} 元"]
        if me_r is not None and me_r > 0:
            rows.append(f"- 月刚性支出：{_fmt_money(me_r)} 元")
        if surplus is not None:
            rows.append(f"- 月结余：{_fmt_money(surplus)} 元（结余率 {savings_rate:.0f}%，"
                        f"为负 = 本月支出大于收入，事实陈述）")
        if i532:
            rows.append(f"- 常见分配思路（532 框架，教学参照非建议）：必要开支约 {_fmt_money(i532['need'])} 元 / "
                        f"储蓄约 {_fmt_money(i532['save'])} 元 / 投资学习约 {_fmt_money(i532['invest'])} 元——"
                        "你自己的实际分配与它的差值只是事实，不是错误")
        for r in rows:
            add(r)
        add("")
        add("*说明：532 是一种常见的教学参照（50% 必要 / 30% 储蓄 / 20% 投资），各家庭结构差异大，"
            "不是标准答案；结余为负不构成任何指令，是否调整由你决定。*")
        add("")

    if any(d["rate"] is not None for d in debt_cost):
        add("## 3.2 负债成本事实卡（按利率降序，只排序不下结论）")
        add("")
        with_rate = sorted([d for d in debt_cost if d["rate"] is not None], key=lambda x: -x["rate"])
        no_rate = [d for d in debt_cost if d["rate"] is None]
        for d in with_rate:
            tag = "（年化 ≥18%，常见信用卡分期的实际利率区间——高息事实，仅标注）" if d in high_rate else ""
            add(f"- {d['item']}：{_fmt_money(d['amount'])} 元，利率 {d['rate']:.2f}%{tag}")
        for d in no_rate:
            add(f"- {d['item']}：{_fmt_money(d['amount'])} 元，利率未提供（银行 App 可查，补上后重跑可排序）")
        if high_rate:
            add("")
            add("*利率事实：上表按利率从高到低排列；是否提前偿还、偿还顺序是你的决定——"
                "可对照第 5 章纪律框架自查，本工具不替你排序决策。*")
        add("")

    if hp:
        add("## 3.3 大额决策测算（月供压力事实，只算不判）")
        add("")
        add(f"- 假设贷款 {_fmt_money(hp['loan_amount'])} 元 / {hp['years']:.0f} 年 / 年化 {hp['rate_annual']:.2f}%（等额本息）")
        add(f"- 测算月供约 **{_fmt_money(hp['monthly_payment'])}** 元（纯公式计算，未含税费/保险/浮动利率变化）")
        pti = hp.get("payment_to_income")
        if pti is not None:
            add(f"- 月供 ÷ 月收入 = **{pti:.0f}%**（常见经验参照：超过 50% 时家庭现金流对收入波动较敏感——"
                "这是事实陈述，不是「不能买」的判断）")
        add("")
        add("*本测算基于你提供的假设值；实际利率、还款方式（等额本息/等额本金）不同结果不同，"
            "以银行正式测算为准。买不买、买多少是你的决定。*")
        add("")

    # 四、下一步（仅方法层，非指令）
    add("## 四、下一步（仅方法层，非指令）")
    add("")
    add("- 按第 2–4 章框架，依次自查：应急金 → 四桶结构 → 权益占比 → 保障")
    add("- 信息缺口逐项去上方官方入口自查，把数据补齐后重跑体检")
    if exp == "L2":
        add("- 有操作经验者：请自检是否追涨杀跌 / 重仓单一 / 频繁换仓 / 说不清为何持有某项——"
            "如存在，请对照第 5 章补定投与纪律框架")
    add("- 任何\"买哪只 / 几点买卖 / 要不要调\"请找持牌机构（证监会正规券商/银行投顾），"
        "本工具不代决策、不下判断")
    add("")

    # 经验档侧重（§9.5 / §12.3）
    add("## 五、按你的经验档给出的侧重提示")
    add("")
    if exp == "L2":
        add("**你的档位：L2（有操作经验、理论待补扎实）**")
        add("")
        add("- 操作特征自检（自填即可，工具不判行情）：追涨杀跌？重仓单一？频繁换仓？"
            "是否有过\"低风险还能高收益\"这类矛盾认知？")
        add("- 认知误区提示（只点\"缺框架\"，不评判对错）：若权益占比说不清为何是这个数，"
            "可能凭感觉而非框架 → 对照第 4 章补逻辑")
        add("- 防二次收割：若参加过付费理财课/有\"老师带单\"，请用防割五特征 + 持牌查验"
            "（证监会官网可查持牌机构名录）自行验证，本工具不替你给任何课程/平台下定论")
    else:
        add("**你的档位：L1（0 基础）**")
        add("")
        add("- 先确认三件事：家底清点了吗？应急金建立了吗？基础保障（重疾/医疗）有概念了吗？")
        add("- 先补第 1–4 章基础框架（财商启蒙 → 清点家底 → 投资品五类 → 配置框架），再考虑其他")
        add("- 防骗优先：任何宣称\"稳赚不赔/低风险高回报/9 元课带你致富\"的说法先存疑，"
            "对照第 6 章五特征自查")
    add("")
    add("---")
    add("*生成工具：asset-health-check（本地静态计算，数据不出本机）。"
        "本报告不构成投资建议，不承诺收益，不代任何决策。*")

    return "\n".join(lines) + "\n"


def compliance_scan(text):
    """输出前合规自扫（§12.4）。返回命中列表 [(word, line_no, line)]。

    上下文感知，两级豁免：
    1. 普通黑名单词：该行含"拒绝/引导"标记（_WHITELIST_MARKERS）即豁免——
       模板固定句式如「不判"偏高/偏低"」「工具不点名换哪只」是免责表述。
    2. 强判断词（_STRONG_JUDGMENT_WORDS）：整行白名单不够，必须词前 4 字内
       紧邻否定句式才算免责——防止「应急金不足（经验区间 3-6）」这类
       真判断句靠行内其他标记蒙混过关。
    """
    # 白名单句式：该行含这些"拒绝/引导"标记之一，则该行内的普通黑名单词视为免责表述
    _WHITELIST_MARKERS = [
        "不判", "不下", "不构成", "不承诺", "不推荐", "不建议", "不替你", "不点名",
        "不代", "不接行情", "不买卖", "拒绝", "找持牌机构", "请找持牌", "工具不判断",
        "仅供自查", "自查", "请对照", "经验区间", "不荐", "请自行核实", "先存疑",
        "下定论", "存疑",
    ]
    hits = []
    for i, line in enumerate(text.splitlines(), 1):
        has_marker = any(m in line for m in _WHITELIST_MARKERS)
        for w in _COMPLIANCE_BLOCKLIST:
            start = 0
            while True:
                idx = line.find(w, start)
                if idx < 0:
                    break
                if w in _STRONG_JUDGMENT_WORDS:
                    prefix = line[max(0, idx - 6):idx]
                    ok = any(p in prefix for p in _STRONG_NEGATION_PREFIXES)
                else:
                    ok = has_marker
                if not ok:
                    hits.append((w, i, line.strip()[:60]))
                    break
                start = idx + len(w)
    return hits


def load_input(path):
    """按扩展名加载 JSON 或 CSV，统一为 compute() 需要的 dict。

    CSV 格式（方案 §9.3）：两段式
      - 资产段：cat,amount,bucket,note
      - 负债段：item,amount
    约定：用空行分隔两段；第一段表头首列必须是 cat，第二段表头首列必须是 item。
    顶层标量（experience/monthly_expense/risk_tolerance/insurance_flagged）
    写在首行注释里：# key=value（insurance_flagged 用 | 分隔）。
    """
    p = Path(path)
    text = p.read_text(encoding="utf-8-sig")

    if p.suffix.lower() == ".json":
        data = json.loads(text)
        if not isinstance(data, dict):
            raise ValueError("JSON 根必须是对象（dict）")
        return data

    # ---- CSV 解析 ----
    data = {"assets": [], "liabilities": [], "ai_identified_items": []}
    meta = {}

    # 提取 # 开头的元信息行
    body_lines = []
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("#"):
            s = s[1:].strip()
            if "=" in s:
                k, _, v = s.partition("=")
                meta[k.strip()] = v.strip()
        else:
            body_lines.append(line)

    if "experience" in meta:
        data["experience"] = meta["experience"]
    if "monthly_expense" in meta:
        try:
            data["monthly_expense"] = float(meta["monthly_expense"])
        except ValueError:
            pass
    if "risk_tolerance" in meta:
        data["risk_tolerance"] = meta["risk_tolerance"]
    if "insurance_flagged" in meta:
        data["insurance_flagged"] = [x.strip() for x in meta["insurance_flagged"].split("|") if x.strip()]

    # 分段（空行分隔）
    sections, cur = [], []
    for line in body_lines:
        if line.strip():
            cur.append(line)
        elif cur:
            sections.append(cur)
            cur = []
    if cur:
        sections.append(cur)

    for sec in sections:
        rows = list(csv.DictReader(sec))
        if not rows:
            continue
        header = [h.strip().lower() for h in sec[0].split(",")]
        if header and header[0] == "cat":
            for r in rows:
                amt = (r.get("amount") or "").strip()
                try:
                    amt_v = float(amt)
                except ValueError:
                    amt_v = None
                item = {"cat": (r.get("cat") or "").strip() or "未命名",
                        "amount": amt_v,
                        "bucket": (r.get("bucket") or "").strip() or None,
                        "note": (r.get("note") or "").strip()}
                data["assets"].append(item)
        elif header and header[0] == "item":
            for r in rows:
                amt = (r.get("amount") or "").strip()
                try:
                    amt_v = float(amt)
                except ValueError:
                    amt_v = None
                data["liabilities"].append({"item": (r.get("item") or "").strip() or "未命名",
                                            "amount": amt_v})
    return data


DEMO = {
    "experience": "L1",
    "monthly_expense": 6000,
    "risk_tolerance": "balanced",
    "assets": [
        {"cat": "现金存款", "amount": 50000, "bucket": "flexible", "note": ""},
        {"cat": "货币基金", "amount": 30000, "bucket": "flexible", "note": ""},
        {"cat": "债券基金", "amount": 40000, "bucket": "steady", "note": ""},
        {"cat": "股票", "amount": 60000, "bucket": "growth", "note": ""},
        {"cat": "公募基金", "amount": 50000, "bucket": "growth", "note": ""},
        {"cat": "商业保险现金价值", "amount": 20000, "bucket": "protection", "note": ""}
    ],
    "liabilities": [
        {"item": "房贷剩余本金", "amount": 200000},
        {"item": "信用卡分期", "amount": 8000}
    ],
    "insurance_flagged": ["重疾险", "医疗险"],
    "ai_identified_items": []
}


def render_trend_section(old_indicators, new_indicators, old_path, new_path):
    """渲染季度对比段（事实差值，零判断）。用于 --compare 模式，追加在体检卡后。"""
    lines = []
    add = lines.append
    add("")
    add("---")
    add("")
    add("## 六、与上次体检对比（事实变化，不判断好坏）")
    add("")
    add(f"- 上次：{old_path}　本次：{new_path}")

    def _fmt_or_dash(v):
        return _fmt_money(v) if v is not None else "—"

    def _cmp(label, old_v, new_v, unit="元", fmt=None):
        if old_v is None or new_v is None:
            add(f"- {label}：上次 {'—' if old_v is None else _fmt_or_dash(old_v) + unit} / "
                f"本次 {'—' if new_v is None else _fmt_or_dash(new_v) + unit}（有数据缺失，无法对比）")
            return
        if fmt:
            add(f"- {label}：{old_v:g} → {new_v:g}（变化 {new_v - old_v:+.1f}）")
            return
        diff = new_v - old_v
        add(f"- {label}：{_fmt_money(old_v)} → {_fmt_money(new_v)} 元（变化 {diff:+,.2f} 元）")

    _cmp("净资产", old_indicators.get("net_worth"), new_indicators.get("net_worth"))
    _cmp("总资产", old_indicators.get("total_assets"), new_indicators.get("total_assets"))
    _cmp("总负债", old_indicators.get("total_liabilities"), new_indicators.get("total_liabilities"))
    _cmp("应急金月数", old_indicators.get("emergency_months"), new_indicators.get("emergency_months"), fmt=True)
    _cmp("权益占比%", old_indicators.get("equity_pct"), new_indicators.get("equity_pct"), fmt=True)

    ob = old_indicators.get("buckets")
    nb = new_indicators.get("buckets")
    if ob and nb:
        add("- 四桶占比变化：" + "；".join(
            f"{BUCKET_NAMES[k]} {ob.get(k) or 0:.1f}%→{nb.get(k) or 0:.1f}%" for k in BUCKET_NAMES))
    else:
        add("- 四桶占比：数据不全，无法对比")

    add("")
    add("> 注：以上是两次体检的事实差值。变好变坏、要不要调整，判断权在你；")
    add("> 若要分析变化原因或调整结构，请对照第 4 章框架自查或咨询持牌机构。")
    return "\n".join(lines)


def _metrics_line(indicators):
    """卡片尾部机器可读指标行：--compare 优先解析这一行，regex 文案解析仅作旧卡兜底。

    数值四舍五入避免长小数；对象卡数值缺失保留 null（对比段会显示"无法对比"带原因）。
    """
    m = {
        "net_worth": indicators.get("net_worth"),
        "total_assets": indicators.get("total_assets"),
        "total_liabilities": indicators.get("total_liabilities"),
        "emergency_months": round(indicators["emergency_months"], 2) if indicators.get("emergency_months") is not None else None,
        "equity_pct": round(indicators["equity_pct"], 1) if indicators.get("equity_pct") is not None else None,
        "buckets": {k: round(v, 1) for k, v in indicators["buckets"].items()} if indicators.get("buckets") else None,
    }
    return f"<!-- metrics: {json.dumps(m, ensure_ascii=False)} -->"


def _parse_old_card(old_text):
    """从上次体检卡文本解析指标。优先 metrics 注释行（稳，与文案零耦合）；
    旧版卡片没有该行时回退 regex 解析。返回 (indicators, reliable)。"""
    m1 = re.search(r"<!-- metrics: (\{.*\}) -->", old_text)
    if m1:
        try:
            md = json.loads(m1.group(1))
            _f = lambda x: float(x) if isinstance(x, (int, float)) and not isinstance(x, bool) else None
            bs = md.get("buckets")
            buckets = ({k: float(v) for k, v in bs.items()
                        if isinstance(v, (int, float)) and not isinstance(v, bool)}
                       if isinstance(bs, dict) and bs else None)
            return {
                "net_worth": _f(md.get("net_worth")),
                "total_assets": _f(md.get("total_assets")),
                "total_liabilities": _f(md.get("total_liabilities")),
                "emergency_months": _f(md.get("emergency_months")),
                "equity_pct": _f(md.get("equity_pct")),
                "buckets": buckets,
            }, True
        except (json.JSONDecodeError, ValueError, AttributeError):
            pass  # metrics 行损坏 → 走 regex 兜底

    def _num(pattern):
        m = re.search(pattern, old_text)
        if not m:
            return None
        try:
            return float(m.group(1).replace(",", ""))
        except (ValueError, IndexError):
            return None

    indicators = {
        "net_worth": _num(r"净资产 = 资产 [\d,]+ − 负债 [\d,]+ = (-?[\d,]+) 元"),
        "total_assets": _num(r"总资产：([\d,]+) 元"),
        "total_liabilities": _num(r"总负债：([\d,]+) 元"),
        "emergency_months": _num(r"现状约 ([\d.]+) 个月"),
        "equity_pct": None,
        "buckets": None,
    }
    eq_m = re.search(r"权益占比\*\*：现状 ([\d.]+)%", old_text)
    if eq_m:
        indicators["equity_pct"] = float(eq_m.group(1))
    buckets_m = re.search(r"灵活取用：([\d.]+)%\s*\n- 稳健：([\d.]+)%\s*\n- 进取：([\d.]+)%\s*\n- 保障：([\d.]+)%", old_text)
    if buckets_m:
        indicators["buckets"] = {
            "flexible": float(buckets_m.group(1)),
            "steady": float(buckets_m.group(2)),
            "growth": float(buckets_m.group(3)),
            "protection": float(buckets_m.group(4)),
        }
    reliable = any(v is not None for v in indicators.values())
    return indicators, reliable


def main():
    ap = argparse.ArgumentParser(description="资产体检计算器（只做静态分析，不下判断）")
    ap.add_argument("--input", "-i", default=None, help="输入 assets.json / assets.csv 路径")
    ap.add_argument("--output", "-o", default=None, help="输出 health_card.md 路径（缺省打印 stdout）")
    ap.add_argument("--demo", action="store_true", help="跑内置示例数据")
    ap.add_argument("--compare", "-c", default=None,
                    help="对比模式：给上一次的体检卡 md 文件，输出末尾追加'与上次对比'段")
    args = ap.parse_args()

    if args.demo:
        data = DEMO
    elif args.input:
        in_path = Path(args.input)
        if not in_path.exists():
            print(f"[ERROR] 输入文件不存在: {in_path}", file=sys.stderr)
            sys.exit(2)
        try:
            data = load_input(in_path)
        except (json.JSONDecodeError, UnicodeDecodeError, ValueError) as e:
            print(f"[ERROR] 输入解析失败（需合法 UTF-8 JSON 或约定格式 CSV）: {e}", file=sys.stderr)
            sys.exit(2)
    else:
        ap.print_help()
        sys.exit(2)

    indicators, gaps, pending = compute(data)
    card = render_card(data, indicators, gaps, pending)

    # 卡片头部加体检时间戳（趋势跟踪的锚点）
    if args.output or args.demo:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M")
        card = card.replace("【家庭资产体检卡】", f"【家庭资产体检卡】\n\n*体检时间：{ts}*", 1)

    # --compare：解析上次体检卡的关键数字，追加对比段
    if args.compare:
        old_path = Path(args.compare)
        if not old_path.exists():
            print(f"[ERROR] 对比文件不存在: {old_path}", file=sys.stderr)
            sys.exit(2)
        old_text = old_path.read_text(encoding="utf-8")
        old_indicators, reliable = _parse_old_card(old_text)
        if not reliable:
            print("[COMPARE WARNING] 上次体检卡里解析不到任何指标（旧版本生成、"
                  "文案变更或文件不完整），对比段各项将显示'无法对比'——建议把 older 卡重新体检补上。",
                  file=sys.stderr)
        trend = render_trend_section(old_indicators, indicators, old_path.name, "本次")
        card = card + trend

    # 卡片尾部附机器可读指标行（--compare 的首选解析源，见 _parse_old_card）
    card = card.rstrip("\n") + "\n" + _metrics_line(indicators) + "\n"

    hits = compliance_scan(card)
    if hits:
        print("[COMPLIANCE WARNING] 输出命中合规黑名单词，请人工复核后再对外发布：", file=sys.stderr)
        for w, ln, snippet in hits:
            print(f"  - 行{ln} 命中: {w} | {snippet}", file=sys.stderr)

    if args.output:
        out_path = Path(args.output)
        out_path.write_text(card, encoding="utf-8")
        print(f"[OK] 体检卡已写入: {out_path}")
        if hits:
            print(f"[WARN] 合规自扫命中 {len(hits)} 处，见 stderr", file=sys.stderr)
            sys.exit(1)
    else:
        print(card)
        if hits:
            print(f"[WARN] 合规自扫命中 {len(hits)} 处（仅告警，未阻断 stdout）", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
