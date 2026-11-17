# -*- coding: utf-8 -*-
"""
缠论买点扫描 → 单日形态判断 → 次日条件单触发价 闭环流水线
============================================================
流程：扫描出票 → 取当日K线 → 判断单日形态 → 查合并主策略表 → 算次日触发价 → 出报告

主策略 = A版(2026-08 常驻档) + B版(形态调节层) 合并，C版/D版已删除。
数据基准：不复权；基准价 = 当日收盘价（次日条件单的前收盘价）。

使用：更新顶部 TODAY / NEXT_TRADE / POOL 三个变量后直接运行。
"""
import datetime

TODAY = "2026-08-28"          # 数据日期（最近交易日）
NEXT_TRADE = "2026-08-31"     # 下一交易日（条件单生效日）

# ============================================================
# 票池：(代码, 名称, 板块, 主分类, 前收, 今开, 今收, 今高, 今低, 所属分组, 近10日收盘价)
#   主分类  ：一买 / 二买 / 三买 / 重叠 —— 决定条件单归属，每只票只生成一套条件单
#   所属分组：自选股分组归属；重叠票同时进「一买」与「二买」组，允许重复出现
#   近10日收盘价：列表，从新到旧 [今收, 昨收, ...]，用于计算 MA5 / MA10（不复权）
# 数据来源：westock data_kline period=day（不复权），limit=12
# ============================================================
POOL = [
    # ---- 一二重叠（同时触发底背驰 + 金叉）8 只：条件单唯一，同属一买组 + 二买组 ----
    ("sh688820", "盛合晶微", "科创", "重叠", 127.70, 126.93, 127.55, 134.48, 126.10, ("一买", "二买"),
     [127.55, 127.70, 121.61, 121.12, 122.44, 127.50, 127.98, 141.00, 153.62, 153.10]),
    ("sh688256", "寒武纪",   "科创", "重叠", 1048.00, 1050.00, 1046.63, 1090.71, 1042.01, ("一买", "二买"),
     [1046.63, 1048.00, 1020.00, 1010.48, 969.05, 1035.00, 1010.88, 1050.49, 1162.50, 1156.00]),
    ("sh688521", "芯原股份", "科创", "重叠", 193.70, 193.17, 186.90, 196.85, 186.25, ("一买", "二买"),
     [186.90, 193.70, 180.50, 164.49, 168.66, 178.38, 178.37, 185.29, 213.30, 226.30]),
    ("sz301398", "星源卓镁", "创业", "重叠", 31.87, 32.00, 33.40, 34.35, 31.31, ("一买", "二买"),
     [33.40, 31.87, 31.82, 32.00, 31.29, 31.41, 31.26, 31.78, 34.60, 35.42]),
    ("sz300910", "瑞丰新材", "创业", "重叠", 27.58, 27.58, 28.76, 29.29, 27.55, ("一买", "二买"),
     [28.76, 27.58, 27.28, 25.39, 25.26, 25.15, 26.46, 26.46, 27.00, 27.13]),
    ("sz300984", "金沃股份", "创业", "重叠", 31.57, 31.87, 32.40, 33.66, 31.43, ("一买", "二买"),
     [32.40, 31.57, 30.51, 31.08, 30.97, 32.24, 31.00, 30.47, 35.36, 34.75]),
    ("sz301361", "众智科技", "创业", "重叠", 27.06, 26.94, 27.04, 27.24, 26.82, ("一买", "二买"),
     [27.04, 27.06, 27.28, 27.06, 26.36, 26.51, 26.62, 26.16, 27.75, 28.28]),
    ("sz300474", "景嘉微",   "创业", "重叠", 51.02, 51.45, 50.94, 51.65, 50.86, ("一买", "二买"),
     [50.94, 51.02, 50.48, 50.27, 49.88, 50.66, 50.34, 50.10, 52.28, 53.23]),
    # ---- 缠二买（金叉企稳代理，与一类不重叠部分）21 只 ----
    ("sh688408", "中信博",   "科创", "二买", 24.78, 24.91, 26.50, 26.70, 24.55, ("二买",),
     [26.50, 24.78, 24.95, 24.82, 24.90, 25.48, 25.66, 24.95, 26.28, 26.62]),
    ("sh688058", "宝兰德",   "科创", "二买", 23.00, 23.88, 24.16, 25.09, 23.64, ("二买",),
     [24.16, 23.00, 22.75, 22.86, 22.50, 22.83, 22.88, 22.44, 23.58, 23.42]),
    ("sh688281", "华秦科技", "科创", "二买", 48.15, 47.81, 49.97, 50.38, 47.81, ("二买",),
     [49.97, 48.15, 46.90, 45.11, 44.50, 45.18, 45.45, 46.07, 48.19, 49.22]),
    ("sh688543", "国科军工", "科创", "二买", 38.98, 38.97, 39.22, 39.77, 38.80, ("二买",),
     [39.22, 38.98, 38.58, 38.27, 38.19, 38.60, 37.94, 37.80, 39.45, 40.40]),
    ("sh688295", "中复神鹰", "科创", "二买", 39.30, 38.86, 38.98, 39.86, 38.86, ("二买",),
     [38.98, 39.30, 38.31, 37.81, 38.32, 38.86, 38.47, 38.68, 42.12, 41.38]),
    ("sz301076", "新瀚新材", "创业", "二买", 20.76, 22.09, 22.96, 23.85, 21.83, ("二买",),
     [22.96, 20.76, 20.18, 20.35, 19.86, 20.40, 20.19, 20.45, 22.49, 22.78]),
    ("sz300833", "浩洋股份", "创业", "二买", 36.71, 40.13, 39.57, 41.22, 38.60, ("二买",),
     [39.57, 36.71, 36.25, 37.20, 36.44, 36.24, 35.80, 35.77, 37.01, 37.56]),
    ("sz301330", "熵基科技", "创业", "二买", 23.98, 24.71, 25.56, 26.81, 24.70, ("二买",),
     [25.56, 23.98, 24.05, 24.03, 23.55, 23.90, 24.16, 23.63, 24.64, 24.93]),
    ("sz301179", "泽宇智能", "创业", "二买", 19.73, 19.70, 20.66, 21.05, 19.58, ("二买",),
     [20.66, 19.73, 19.21, 19.95, 21.22, 20.02, 19.95, 19.67, 20.44, 20.75]),
    ("sz300775", "三角防务", "创业", "二买", 21.46, 21.40, 22.39, 22.97, 21.34, ("二买",),
     [22.39, 21.46, 20.89, 20.89, 20.45, 20.85, 20.89, 20.62, 22.04, 22.02]),
    ("sz300627", "华测导航", "创业", "二买", 27.65, 27.60, 28.75, 28.95, 27.47, ("二买",),
     [28.75, 27.65, 27.29, 27.25, 26.98, 27.13, 27.25, 27.61, 28.76, 29.09]),
    ("sz300915", "海融科技", "创业", "二买", 20.39, 20.37, 20.95, 21.58, 20.37, ("二买",),
     [20.95, 20.39, 20.45, 20.77, 19.97, 20.25, 20.57, 20.10, 20.89, 21.19]),
    ("sz300904", "威力传动", "创业", "二买", 41.18, 41.18, 42.25, 42.90, 40.89, ("二买",),
     [42.25, 41.18, 41.23, 40.22, 38.70, 41.17, 40.95, 40.20, 42.08, 42.46]),
    ("sz301677", "欣兴工具", "创业", "二买", 54.91, 54.95, 56.23, 57.38, 53.87, ("二买",),
     [56.23, 54.91, 54.39, 54.02, 54.08, 55.03, 55.45, 56.40, 61.15, 61.58]),
    ("sz301578", "辰奕智能", "创业", "二买", 23.14, 23.00, 23.64, 23.65, 23.00, ("二买",),
     [23.64, 23.14, 23.09, 23.11, 22.54, 22.75, 22.92, 22.48, 23.35, 23.45]),
    ("sz301589", "诺瓦星云", "创业", "二买", 141.28, 140.98, 143.10, 144.38, 140.50, ("二买",),
     [143.10, 141.28, 138.81, 140.66, 139.15, 136.90, 136.90, 139.65, 145.10, 145.55]),
    ("sz301001", "凯淳股份", "创业", "二买", 23.94, 24.05, 24.19, 24.53, 23.94, ("二买",),
     [24.19, 23.94, 23.90, 24.14, 23.52, 23.69, 23.84, 23.14, 24.15, 24.18]),
    ("sz300722", "新余国科", "创业", "二买", 21.28, 21.15, 21.50, 21.78, 21.15, ("二买",),
     [21.50, 21.28, 21.30, 21.28, 20.76, 20.88, 20.68, 20.61, 21.72, 22.11]),
    ("sz300552", "万集科技", "创业", "二买", 21.15, 21.15, 21.24, 21.40, 20.93, ("二买",),
     [21.24, 21.15, 21.29, 20.62, 20.00, 20.22, 20.15, 20.32, 21.84, 21.95]),
    ("sz300285", "国瓷材料", "创业", "二买", 70.01, 71.19, 68.90, 71.87, 68.09, ("二买",),
     [68.90, 70.01, 64.12, 63.24, 64.10, 67.86, 62.92, 64.12, 74.26, 73.52]),
    ("sz300489", "光智科技", "创业", "二买", 242.04, 242.11, 234.09, 246.00, 229.69, ("二买",),
     [234.09, 242.04, 208.30, 217.33, 202.15, 216.55, 228.63, 222.53, 249.34, 258.45]),
    # ---- 缠三买（突破回踩代理）1 只 ----
    ("sh688169", "石头科技", "科创", "三买", 130.60, 130.00, 128.60, 132.00, 128.01, ("三买",),
     [128.60, 130.60, 131.57, 135.00, 112.50, 116.46, 119.60, 118.00, 120.80, 113.24]),
]

# ============================================================
# 合并主策略参数表（A版 + B版）
# ============================================================
# 【A版·常驻档】所有形态均挂
COMMON_BUY = [
    ("B0 底仓", 0.995, "2 手", "14:45–15:00 下穿买入，主建仓档"),
    ("B4 极限", 0.600, "1 手", "成本价基准，成本 −40% 补仓"),
]
COMMON_SELL = [
    ("S1 快止盈", 1.005, "减半", "次日 09:30–10:00 内执行"),
    ("S2 主止盈", 1.050, "减半", "全时段有效"),
    ("S3 顶背离", 0.980, "减半", "需顶背离确认（价新高、MACD 不新高、柱面积缩小）"),
]

# 【B版·形态调节层】买入补仓档
FORM_BUY = {
    "高开高走": [("B1 补仓", 0.94, "1 手", "A版常驻补仓档"),
                ("B2 深跌", 0.88, "1 手", "A版常驻补仓档")],
    "高开低走": [("B1 补仓", 0.94, "1 手", "A版常驻补仓档"),
                ("B2 深跌", 0.88, "1 手", "A版常驻补仓档"),
                ("BR 接回", 0.95, "1 手", "B版反弹接回档")],
    "低开高走": [("B1′ 补仓", 0.92, "1 手", "B版形态档，替代 A版 0.94"),
                ("B2′ 深跌", 0.84, "1 手", "B版形态档，替代 A版 0.88"),
                ("B3′ 极限", 0.76, "1 手", "B版第三档，仅低开高走形态")],
    "低开低走": [("B1 补仓", 0.94, "1 手", "A版常驻补仓档"),
                ("B2 深跌", 0.88, "1 手", "A版常驻补仓档"),
                ("BR 反弹", 0.93, "1 手", "B版反弹买入档")],
}

# 【B版·形态调节层】强制止损位（S4，优先级最高，触发即清仓）
# 返回 (系数, 备注)
def form_stop(form, board):
    if form == "高开高走":
        return 0.95, "B版止损，触发后空仓 4 天或更换品种"
    if form == "高开低走":
        if board == "科创":
            return 0.969, "B版科创专用止损"
        return 0.95, "B版止损"
    if form == "低开高走":
        return 0.95, "B版止损"
    # 低开低走
    if board == "创业":
        return 0.98, "B版创业板止损"
    return 0.96, "A版默认强制止损"

# 【B版·形态调节层】补充止盈档
FORM_EXTRA_SELL = {
    "高开高走": [("S5 涨停回落", 1.099, "1/4", "对应 +9.9%，回落卖出"),
                ("S5 涨停回落", 1.199, "1/4", "对应 +19.9%，回落卖出"),
                ("S5 涨停回落", 1.299, "1/4", "对应 +29.9%，回落卖出")],
    "高开低走": [("S5 涨停回落", 1.099, "1/4", "对应 +9.9%，回落卖出"),
                ("S5 涨停回落", 1.199, "1/4", "对应 +19.9%，回落卖出"),
                ("S5 涨停回落", 1.299, "1/4", "对应 +29.9%，回落卖出")],
    "低开高走": [],
    "低开低走": [("S6 分批止盈", 1.020, "减半", "B版第一档止盈"),
                ("S6 分批止盈", 1.070, "减半", "B版第二档止盈（1.05 与 S2 重合已去重）")],
}

# 【B版·动作指令】当日操作 + 次日操作（形态判断后的执行动作）
# (当日操作, 次日操作, 执行时点说明)
FORM_ACTION = {
    "高开高走": ("持股",
                "若次日<b>高开低走</b> → 卖出",
                "次日 09:35 判断次日形态后执行；止损触发后空仓 4 天或更换品种"),
    "高开低走": ("直接卖出",
                "次日<b>高开高走</b> → 持股；<b>低开高走</b> → 持币",
                "当日尾盘前完成减仓，等 0.95 反弹接回"),
    "低开高走": ("持币",
                "次日<b>低开低走</b> → 再买入",
                "当日不追，等次日回踩；买入档用 0.92 / 0.84 / 0.76"),
    "低开低走": ("择机买入",
                "次日<b>低开高走</b> → 持币；<b>高开高走</b> → 持股",
                "当日 14:45–15:00 尾盘择机买入，止盈用 1.02 / 1.07"),
}

# 板块涨跌停幅度
LIMIT = {"科创": 0.20, "创业": 0.20, "主板": 0.10, "北交": 0.30}

# S7 缓冲带：需跌破 MA10 **再往下 3%** 才算「有效破位」，过滤贴线噪音
# 直接跌破 MA10 就清仓太激进——盘中一哆嗦就触发，很可能刚清仓股价又站回去。
# 调大更保守（不易触发），调小更灵敏。0.03 = 3%
MA10_BUFFER = 0.03


# ============================================================
# 单日形态判断（必须判断项）
# ============================================================
def judge_form(prev_close, open_, close):
    """单日形态判断（必判项）
    高开/低开 = 今开 vs 前收；高走/低走 = 今收 vs 今开。
    平开（|gap| < 0.1%）兜底：按 今收 vs 前收 定强弱，高走归高开高走、低走归低开低走。
    返回 (形态, 备注, 推导链文本)"""
    gap = (open_ - prev_close) / prev_close

    # --- 第一步：定高开 / 低开 ---
    if abs(gap) < 0.001:
        od = f"今开 {open_:.2f} ≈ 前收 {prev_close:.2f}（{gap*100:+.2f}%）→ <b>平开</b>"
        flat = True
    elif gap > 0:
        od = f"今开 {open_:.2f} &gt; 前收 {prev_close:.2f}（{gap*100:+.2f}%）→ <b>高开</b>"
        flat = False
    else:
        od = f"今开 {open_:.2f} &lt; 前收 {prev_close:.2f}（{gap*100:+.2f}%）→ <b>低开</b>"
        flat = False

    # --- 第二步：定高走 / 低走 ---
    cd_pct = (close - open_) / open_ * 100
    if close > open_:
        cd = f"今收 {close:.2f} &gt; 今开 {open_:.2f}（{cd_pct:+.2f}%）→ <b>高走</b>"
    elif close < open_:
        cd = f"今收 {close:.2f} &lt; 今开 {open_:.2f}（{cd_pct:+.2f}%）→ <b>低走</b>"
    else:
        cd = f"今收 {close:.2f} = 今开 {open_:.2f} → <b>平收</b>"

    if flat:
        form = "高开高走" if close > prev_close else "低开低走"
        extra = f"；平开兜底：今收 vs 前收 {((close-prev_close)/prev_close*100):+.2f}% 定强弱"
        return form, "平开兜底", od + "；" + cd + extra

    if gap > 0:
        form = "高开高走" if close > open_ else "高开低走"
        return form, "", od + "；" + cd

    form = "低开高走" if close > open_ else "低开低走"
    return form, "", od + "；" + cd


def r2(x):
    return round(x * 100) / 100


def build_orders(code, name, board, cat, prev_close, open_, close, high, low, groups, closes):
    """生成单只标的的完整条件单清单（含形态推导链、当日/次日操作指令、均线档）"""
    form, note, detail = judge_form(prev_close, open_, close)
    today_act, tmw_act, act_memo = FORM_ACTION[form]
    lim = LIMIT.get(board, 0.20)
    base = close                       # 次日条件单基准价 = 当日收盘价
    up_limit = r2(base * (1 + lim))    # 次日涨停价
    dn_limit = r2(base * (1 - lim))    # 次日跌停价

    # 均线（不复权，含当日）
    ma5 = r2(sum(closes[:5]) / 5)
    ma10 = r2(sum(closes[:10]) / 10) if len(closes) >= 10 else None
    # 有效破位线：MA10 再往下 MA10_BUFFER，S7 真正的触发价
    ma10_eff = r2(ma10 * (1 - MA10_BUFFER)) if ma10 is not None else None

    # ---- 买入档 ----
    buys = []
    for code_, coef, qty, memo in COMMON_BUY:
        buys.append((code_, coef, qty, memo))
    for code_, coef, qty, memo in FORM_BUY[form]:
        buys.append((code_, coef, qty, memo))
    # 去重（同系数只保留一条）
    seen, uniq = set(), []
    for b in buys:
        k = round(b[1], 4)
        if k not in seen:
            seen.add(k)
            uniq.append(b)
    buys = sorted(uniq, key=lambda x: -x[1])   # 价格从高到低（先触发的在前）

    # ---- 卖出档 ----
    stop_coef, stop_memo = form_stop(form, board)
    sells = []
    for code_, coef, qty, memo in COMMON_SELL:
        # S3 顶背离档：若与形态止损位重合则丢弃（止损优先）
        if round(coef, 4) == round(stop_coef, 4):
            continue
        sells.append((code_, coef, qty, memo))
    sells.append(("S4 强制止损", stop_coef, "清仓", stop_memo))
    for code_, coef, qty, memo in FORM_EXTRA_SELL[form]:
        if round(coef, 4) in [round(s[1], 4) for s in sells]:
            continue
        sells.append((code_, coef, qty, memo))
    sells = sorted(sells, key=lambda x: -x[1])  # 价格从高到低

    # ---- 均线档：跌破 10 日线止损 / 5 日线上涨 10% 止盈减半 ----
    ma_sells = []
    if ma10 is not None:
        ma_defs = [
            ("S7 破10日线", ma10_eff, "清仓",
             f"有效破位线 = MA10 {ma10:.2f} × {1-MA10_BUFFER:.2f}（跌破 MA10 再下 "
             f"{MA10_BUFFER*100:.0f}% 才触发，过滤贴线噪音）"),
            ("S8 5日线+10%", r2(ma5 * 1.10), "减半", "较 MA5 上涨 10% 止盈减半"),
        ]
        for tag, price, qty, memo in ma_defs:
            if price > up_limit:
                reach = "次日不可达（高于涨停）"
            elif price < dn_limit:
                reach = "次日不可达（低于跌停）"
            else:
                reach = "可达"
            ma_sells.append({
                "tag": tag, "coef": None, "qty": qty, "memo": memo,
                "trig": price, "pct": (price / base - 1) * 100, "reach": reach,
            })

    # ---- 计算触发价与可达性 ----
    def render(items, is_buy):
        out = []
        for code_, coef, qty, memo in items:
            if code_.startswith("B4"):       # 成本基准档，不代入收盘价
                trig, reach = None, "按实际持仓成本 × 0.60"
            else:
                trig = r2(base * coef)
                if trig > up_limit:
                    reach = "次日不可达（高于涨停）"
                elif trig < dn_limit:
                    reach = "次日不可达（低于跌停）"
                else:
                    reach = "可达"
            out.append({
                "tag": code_, "coef": coef, "qty": qty, "memo": memo,
                "trig": trig, "pct": (coef - 1) * 100, "reach": reach,
            })
        return out

    # 自选股分组归属：重叠票同时进一买组与二买组，另加一二重叠组
    grp_list = list(groups) + (["一二重叠"] if cat == "重叠" else [])

    return {
        "code": code, "name": name, "board": board, "cat": cat,
        "groups": groups, "grp_list": grp_list,
        "prev_close": prev_close, "open": open_, "close": close,
        "high": high, "low": low,
        "chg": (close - prev_close) / prev_close * 100,
        "amp": (high - low) / prev_close * 100,
        "form": form, "form_note": note, "detail": detail,
        "today_act": today_act, "tmw_act": tmw_act, "act_memo": act_memo,
        "base": base, "up_limit": up_limit, "dn_limit": dn_limit,
        "ma5": ma5, "ma10": ma10, "ma10_eff": ma10_eff,
        # below_ma10 指「有效破位」= 跌破 MA10 再下 MA10_BUFFER
        "below_ma10": (ma10_eff is not None and close < ma10_eff),
        "ma10_gap": ((close / ma10_eff - 1) * 100) if ma10_eff else 0.0,
        "ma10_raw_gap": ((close / ma10 - 1) * 100) if ma10 else 0.0,
        "buys": render(buys, True),
        "sells": sorted(render(sells, False) + ma_sells,
                        key=lambda x: -(x["trig"] if x["trig"] is not None else 0)),
    }


# ============================================================
# 执行
# ============================================================
results = [build_orders(*row) for row in POOL]

FORM_ORDER = ["高开高走", "高开低走", "低开高走", "低开低走"]
FCLS = {"高开高走": "f1", "高开低走": "f2", "低开高走": "f3", "低开低走": "f4"}
form_count = {f: sum(1 for r in results if r["form"] == f) for f in FORM_ORDER}

# 形态 × 买点类型 交叉统计（按主分类，每只票只计一次）
cross = {f: {"一买": 0, "二买": 0, "一二重叠": 0, "三买": 0} for f in FORM_ORDER}
for r in results:
    cross[r["form"]]["一二重叠" if r["cat"] == "重叠" else r["cat"]] += 1

# 自选股四个分组的应入组数量（重叠票会重复计入一买组与二买组）
GRP_KEYS = ["一买", "二买", "三买", "一二重叠"]
grp_count = {
    "一买": sum(1 for r in results if "一买" in r["groups"]),
    "二买": sum(1 for r in results if "二买" in r["groups"]),
    "三买": sum(1 for r in results if "三买" in r["groups"]),
    "一二重叠": sum(1 for r in results if r["cat"] == "重叠"),
}

# ============================================================
# HTML 渲染
# ============================================================
def order_table(items, kind):
    cls = "buy" if kind == "buy" else "sell"
    rows = []
    for it in items:
        trig = f"{it['trig']:.2f}" if it["trig"] is not None else "—"
        pct = f"{it['pct']:+.1f}%"
        coef = (f"{it['coef']:.3f}" if it.get("coef") is not None
                else "<span class='matag'>均线</span>")
        badge = "ok" if it["reach"] == "可达" else ("gray" if "成本" in it["reach"] else "warn")
        rows.append(
            f"<tr><td><b>{it['tag']}</b></td>"
            f"<td class='mono'>{coef}</td>"
            f"<td class='mono price'>{trig}</td>"
            f"<td class='mono'>{pct}</td>"
            f"<td>{it['qty']}</td>"
            f"<td><span class='badge {badge}'>{it['reach']}</span></td>"
            f"<td class='memo'>{it['memo']}</td></tr>"
        )
    return ("<table class='ord'><thead><tr>"
            "<th>档位</th><th>系数</th><th>触发价</th><th>幅度</th><th>数量</th><th>可达性</th><th>说明</th>"
            f"</tr></thead><tbody>{''.join(rows)}</tbody></table>")


def card(r, default_open):
    fcls = FCLS[r["form"]]
    chg_cls = "up" if r["chg"] > 0 else ("down" if r["chg"] < 0 else "flat")
    chg_txt = f"{r['chg']:+.2f}%"
    op = " open" if default_open else ""
    note = f"<span class='fnote'>{r['form_note']}</span>" if r["form_note"] else ""
    grps = "".join(f"<span class='grp-chip'>{g}</span>" for g in r["grp_list"])
    ma_eff_txt = f"{r['ma10_eff']:.2f}" if r["ma10_eff"] else "—"
    return f"""
<details{op}><summary>
  <span class='code'>{r['code']}</span>
  <span class='name'>{r['name']}</span>
  <span class='tag {fcls}'>{r['form']}</span>{note}
  {grps}
  <span class='act-mini'>{r['today_act']}</span>
  <span class='spacer'></span>
  <span class='mono q'>收 {r['close']:.2f}</span>
  <span class='mono {chg_cls}'>{chg_txt}</span>
</summary>
<div class='body'>
  <div class='kline'>
    前收 <b class='mono'>{r['prev_close']:.2f}</b> ｜
    今开 <b class='mono'>{r['open']:.2f}</b> ｜
    今收 <b class='mono'>{r['close']:.2f}</b> ｜
    最高 <b class='mono'>{r['high']:.2f}</b> ｜
    最低 <b class='mono'>{r['low']:.2f}</b> ｜
    振幅 <b class='mono'>{r['amp']:.2f}%</b> ｜
    板块 <b>{r['board']}</b> ｜
    次日涨停 <b class='mono up'>{r['up_limit']:.2f}</b> ／ 跌停 <b class='mono down'>{r['dn_limit']:.2f}</b>
  </div>
  <div class='ma-line'>
    MA5 <b class='mono'>{r['ma5']:.2f}</b> ｜
    MA10 <b class='mono'>{r['ma10']:.2f}</b> ｜
    有效破位线 <b class='mono'>{ma_eff_txt}</b>
    <span class='buf'>（MA10 −{MA10_BUFFER*100:.0f}%）</span> ｜
    现价 vs 破位线：
    <b class='{'down' if r['below_ma10'] else 'up'}'>
      {'已有效破位 ' if r['below_ma10'] else '缓冲内 '}{r['ma10_gap']:+.2f}%
    </b>
    <span class='mawarn'>{'（应止损清仓）' if r['below_ma10'] else ''}</span>
  </div>
  <div class='derive'><span class='dlbl'>形态推导</span>{r['detail']}</div>
  <div class='act'>
    <div class='act-box tdy'>
      <div class='act-lbl'>当日操作</div>
      <div class='act-val'>{r['today_act']}</div>
    </div>
    <div class='act-box tmw'>
      <div class='act-lbl'>次日操作<span class='when'>（{NEXT_TRADE}）</span></div>
      <div class='act-val'>{r['tmw_act']}</div>
    </div>
    <div class='act-memo'>{r['act_memo']}</div>
  </div>
  <div class='two'>
    <div><h4 class='h-buy'>买入条件单（{len(r['buys'])} 档）</h4>{order_table(r['buys'], 'buy')}</div>
    <div><h4 class='h-sell'>卖出条件单（{len(r['sells'])} 档）</h4>{order_table(r['sells'], 'sell')}</div>
  </div>
</div></details>"""


def section(title, cats, default_open, empty_hint=""):
    items = [r for r in results if r["cat"] in cats]
    items.sort(key=lambda r: -r["chg"])
    if not items:
        hint = empty_hint or "当日该类无标的"
        return (f"<h2>{title}<span class='cnt'>无数据</span></h2>\n"
                f"<div class='empty'>{hint}</div>")
    cards = "".join(card(r, default_open) for r in items)
    return f"<h2>{title}<span class='cnt'>{len(items)} 只</span></h2>\n{cards}"


form_rows = "".join(
    f"<tr><td><span class='tag f{i+1}'>{f}</span></td>"
    f"<td class='mono big'>{form_count[f]}</td>"
    f"<td class='mono'>{cross[f]['一买']}</td>"
    f"<td class='mono'>{cross[f]['二买']}</td>"
    f"<td class='mono hot'>{cross[f]['一二重叠']}</td>"
    f"<td class='mono'>{cross[f]['三买']}</td>"
    f"<td><b>{FORM_ACTION[f][0]}</b></td>"
    f"<td class='nx'>{FORM_ACTION[f][1]}</td>"
    f"<td>{form_count[f]/len(results)*100:.1f}%</td></tr>"
    for i, f in enumerate(FORM_ORDER)
)

# 次日操作总览（按形态分组，组内按涨跌幅降序）
_tmw_rows = []
for _f in FORM_ORDER:
    _items = sorted([r for r in results if r["form"] == _f], key=lambda r: -r["chg"])
    for _i, _r in enumerate(_items):
        _fcell = (f"<td rowspan='{len(_items)}' class='grp'>"
                  f"<span class='tag {FCLS[_f]}'>{_f}</span>"
                  f"<div class='cnt2'>{len(_items)} 只</div></td>") if _i == 0 else ""
        _tmw_rows.append(
            f"<tr>{_fcell}<td class='mono'>{_r['code']}</td><td><b>{_r['name']}</b></td>"
            f"<td>{_r['board']}</td><td class='mono'>{_r['close']:.2f}</td>"
            f"<td><b>{_r['today_act']}</b></td>"
            f"<td class='nx'>{_r['tmw_act']}</td></tr>"
        )
tmw_rows = "".join(_tmw_rows)

# 自选股四个分组表（分组名带当日日期，重叠票重复计入）
_GRP_DESC = {
    "一买": "底背驰代理，含与二类重叠的标的",
    "二买": "金叉企稳代理，含与一类重叠的标的",
    "三买": "突破回踩代理",
    "一二重叠": "同时触发底背驰 + 金叉，同属一买组与二买组",
}
_D = TODAY.replace("-", "")
grp_rows = "".join(
    f"<tr><td><b>{k}{_D}</b></td>"
    f"<td class='mono big'>{grp_count[k]}</td>"
    f"<td>{_GRP_DESC[k]}</td></tr>"
    for k in GRP_KEYS
)

total_orders = sum(len(r["buys"]) + len(r["sells"]) for r in results)
unreachable = sum(
    1 for r in results for it in r["buys"] + r["sells"]
    if it["reach"].startswith("次日不可达")
)

html = f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>缠论扫描 · 条件单闭环 · {NEXT_TRADE}</title>
<style>
:root{{
  --bg:#f5f6f8;--card:#fff;--text:#1a1d21;--text2:#5f6672;--text3:#8b93a1;
  --border:#e3e6ea;--border2:#d0d5dc;
  --buy:#c62828;--buy-bg:#fdecec;--sell:#1e7a3c;--sell-bg:#e9f5ed;
  --blue:#1a5fb4;--blue-bg:#eaf1fb;--amber:#8a6100;--amber-bg:#fdf5e2;--amber-b:#f0dcae;
  --mono:"SF Mono",Consolas,"Courier New",monospace;
}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif;
  background:var(--bg);color:var(--text);line-height:1.6;padding:22px 18px 60px}}
.wrap{{max-width:1240px;margin:0 auto}}
header{{background:linear-gradient(135deg,#1e3a5f,#2c5282);color:#fff;border-radius:14px;
  padding:24px 28px;margin-bottom:18px;box-shadow:0 2px 12px rgba(30,58,95,.18)}}
header h1{{font-size:22px;font-weight:650;margin-bottom:8px}}
header .sub{{font-size:13px;opacity:.9;line-height:1.8}}
header .flow{{margin-top:13px;padding-top:13px;border-top:1px solid rgba(255,255,255,.22);
  font-size:12.5px;opacity:.9;display:flex;flex-wrap:wrap;gap:8px;align-items:center}}
header .flow span{{background:rgba(255,255,255,.15);padding:3px 10px;border-radius:20px}}
header .flow i{{font-style:normal;opacity:.6}}
section{{background:var(--card);border:1px solid var(--border);border-radius:12px;
  padding:20px 24px 22px;margin-bottom:16px}}
h2{{font-size:17px;font-weight:640;margin-bottom:12px;display:flex;align-items:center;gap:10px}}
h2 .cnt{{font-size:12px;font-weight:500;color:var(--text2);background:#eef0f3;padding:2px 9px;border-radius:10px}}
h3{{font-size:14px;font-weight:640;margin:16px 0 6px}}
p.desc{{font-size:13px;color:var(--text2);margin-bottom:12px;line-height:1.8}}
p.desc b{{color:var(--text)}}
table{{width:100%;border-collapse:collapse;font-size:13px;margin-top:6px}}
thead th{{background:#f0f2f5;color:var(--text2);font-weight:600;font-size:12px;text-align:left;
  padding:9px 11px;border-bottom:2px solid var(--border2);white-space:nowrap}}
tbody td{{padding:9px 11px;border-bottom:1px solid var(--border);vertical-align:middle}}
tbody tr:last-child td{{border-bottom:none}}
tbody tr:hover{{background:#fafbfc}}
.mono{{font-family:var(--mono);font-size:12.5px}}
.big{{font-size:15px;font-weight:600}}
.up{{color:var(--buy);font-weight:600}}
.down{{color:var(--sell);font-weight:600}}
.flat{{color:var(--text2)}}
.tag{{display:inline-block;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:600;white-space:nowrap}}
.f1{{background:#fdecec;color:#c62828}}
.f2{{background:#fdf5e2;color:#8a6100}}
.f3{{background:#e9f5ed;color:#1e7a3c}}
.f4{{background:#eaf1fb;color:#1a5fb4}}
.badge{{display:inline-block;padding:1px 7px;border-radius:4px;font-size:11px;font-weight:600}}
.badge.ok{{background:var(--sell-bg);color:var(--sell)}}
.badge.warn{{background:var(--amber-bg);color:var(--amber)}}
.badge.gray{{background:#eef0f3;color:var(--text2)}}
details{{border:1px solid var(--border);border-radius:9px;margin-bottom:9px;overflow:hidden;background:#fff}}
details[open]{{border-color:var(--border2)}}
summary{{padding:11px 15px;cursor:pointer;display:flex;align-items:center;gap:10px;
  font-size:13.5px;list-style:none;flex-wrap:wrap;background:#fafbfc}}
summary::-webkit-details-marker{{display:none}}
summary:hover{{background:#f2f5f8}}
summary .code{{font-family:var(--mono);font-size:12.5px;color:var(--text3)}}
summary .name{{font-weight:640}}
summary .spacer{{flex:1}}
summary .q{{color:var(--text2)}}
.fnote{{font-size:11px;color:var(--text3);font-style:italic}}
.body{{padding:4px 15px 15px;border-top:1px solid var(--border)}}
.kline{{font-size:12.5px;color:var(--text2);padding:10px 0;line-height:2}}
.two{{display:grid;grid-template-columns:1fr 1fr;gap:18px}}
@media(max-width:900px){{.two{{grid-template-columns:1fr}}}}
h4{{font-size:12.5px;font-weight:640;margin:8px 0 2px}}
.h-buy{{color:var(--buy)}}
.h-sell{{color:var(--sell)}}
table.ord{{font-size:12px}}
table.ord th{{padding:6px 8px;font-size:11px}}
table.ord td{{padding:6px 8px}}
table.ord .price{{font-weight:600}}
table.ord .memo{{color:var(--text3);font-size:11.5px}}
.box{{border-radius:8px;padding:12px 15px;font-size:12.5px;line-height:1.85;margin:13px 0 0}}
.box-warn{{background:var(--amber-bg);border:1px solid var(--amber-b);color:#6b4a00}}
.box-info{{background:var(--blue-bg);border:1px solid #cfe0f5;color:#17457f}}
.box b{{font-weight:650}}
.ctrls{{display:flex;gap:8px;margin-bottom:10px}}
.btn{{background:var(--blue);color:#fff;border:none;padding:6px 14px;border-radius:6px;
  font-size:12px;cursor:pointer;font-weight:600;font-family:inherit}}
.btn:hover{{background:#164e9b}}
.btn.sec{{background:#eef0f3;color:var(--text2)}}
.derive{{font-size:12px;color:var(--text2);background:#f7f9fb;border:1px solid var(--border);
  border-radius:7px;padding:8px 12px;margin:6px 0 10px;line-height:1.9}}
.derive .dlbl{{display:inline-block;background:var(--text2);color:#fff;font-size:10.5px;
  padding:1px 7px;border-radius:4px;margin-right:8px;font-weight:600;letter-spacing:.5px}}
.ma-line{{font-size:12.5px;color:#17457f;background:var(--blue-bg);border:1px solid #cfe0f5;
  border-radius:7px;padding:7px 12px;margin:0 0 10px;line-height:1.9}}
.mawarn{{color:var(--buy);font-size:11.5px;font-weight:600}}
.buf{{font-size:11px;color:var(--text3)}}
.matag{{font-size:10.5px;padding:1px 6px;border-radius:4px;background:var(--blue);color:#fff;font-weight:600}}
.act{{display:grid;grid-template-columns:1fr 2fr;gap:10px;margin:4px 0 14px}}
.act-box{{border-radius:8px;padding:9px 13px;border:1px solid}}
.act-box.tdy{{background:var(--blue-bg);border-color:#cfe0f5}}
.act-box.tmw{{background:var(--amber-bg);border-color:var(--amber-b)}}
.act-lbl{{font-size:11px;color:var(--text2);font-weight:600;letter-spacing:.3px;margin-bottom:3px}}
.act-lbl .when{{font-weight:400;color:var(--text3)}}
.act-val{{font-size:14px;font-weight:650;line-height:1.5}}
.act-box.tdy .act-val{{color:#17457f}}
.act-box.tmw .act-val{{color:#6b4a00}}
.act-memo{{grid-column:1/-1;font-size:11.5px;color:var(--text3);line-height:1.7;
  border-top:1px dashed var(--border);padding-top:7px}}
.act-mini{{font-size:11px;padding:1.5px 8px;border-radius:10px;background:#eef0f3;
  color:var(--text2);font-weight:600;white-space:nowrap}}
.nx{{font-size:12.5px;line-height:1.65}}
.grp{{text-align:center;vertical-align:middle;background:#fafbfc}}
.cnt2{{font-size:11px;color:var(--text3);margin-top:4px}}
.grp-chip{{font-size:10.5px;padding:1px 7px;border-radius:10px;background:#eef0f3;
  color:var(--text2);font-weight:600;white-space:nowrap}}
.hot{{color:var(--buy);font-weight:600}}
.empty{{font-size:13px;color:var(--text3);background:#fafbfc;border:1px dashed var(--border2);
  border-radius:8px;padding:14px 16px;margin-bottom:10px}}
footer{{text-align:center;font-size:12px;color:var(--text3);padding-top:14px;line-height:1.9}}
</style></head><body><div class="wrap">

<header>
  <h1>缠论扫描 → 单日形态 → 次日条件单　闭环报告</h1>
  <div class="sub">
    主策略 = <b>A版（常驻档）</b> + <b>B版（形态调节层）</b> 合并　·　C版/D版已移除<br>
    数据基准：不复权　·　基准价 = {TODAY} 收盘价　·　条件单生效日：{NEXT_TRADE}
  </div>
  <div class="flow">
    <span>扫描出票 {len(results)} 只</span><i>→</i>
    <span>取当日 K 线</span><i>→</i>
    <span>判断单日形态</span><i>→</i>
    <span>查合并策略表</span><i>→</i>
    <span>算次日触发价 {total_orders} 条</span><i>→</i>
    <span>出报告</span>
  </div>
</header>

<section>
  <h2>一、单日形态分布<span class="cnt">必判项</span></h2>
  <p class="desc">形态由<b>今开 vs 前收</b>（定高开/低开）与<b>今收 vs 今开</b>（定高走/低走）共同决定。
  平开（开盘偏离 &lt; 0.1%）按收盘强弱兜底归类。形态决定该标的的<b>强制止损位与补仓档位</b>。</p>
  <table>
    <thead><tr><th>单日形态</th><th>合计</th><th>一买</th><th>二买</th><th>一二重叠</th><th>三买</th><th>当日操作</th><th>次日操作</th><th>占比</th></tr></thead>
    <tbody>{form_rows}</tbody>
  </table>

  <h3>自选股分组归属（四个分组，每日按日期重建）</h3>
  <table>
    <thead><tr><th>分组名称</th><th>应入组数量</th><th>说明</th></tr></thead>
    <tbody>{grp_rows}</tbody>
  </table>
  <div class="box box-info">
    <b>分组规则：</b>一二重叠标的<b>同时进入一买组、二买组、一二重叠组</b>，允许重复出现；
    但<b>条件单只生成一套</b>（归入下方「一二重叠」节），避免同一标的出现两套互相冲突的挂单。
  </div>
  <div class="box box-info">
    <b>形态含义速查：</b>
    高开高走 = 强势延续，持股为主，止损 0.95 放宽；
    高开低走 = 冲高回落，当日减仓，等 0.95 反弹接回；
    低开高走 = 探底回升，持币观察，次日低开低走再买，补仓档下移至 0.92/0.84/0.76；
    低开低走 = 弱势延续，择机买入，止盈降至 1.02/1.07。
  </div>
</section>

<section>
  <h2>二、次日操作总览<span class='cnt'>{NEXT_TRADE} 开盘前速查</span></h2>
  <p class="desc">
    按当日形态分组，列出每只标的的<b>当日操作</b>与<b>次日操作</b>（B 版动作指令）。
    次日操作为<b>条件式</b>指令——需在次日 <b>09:35</b> 判断次日开盘形态后，对照执行。
  </p>
  <table>
    <thead><tr><th>当日形态</th><th>代码</th><th>名称</th><th>板块</th><th>收盘价</th><th>当日操作</th><th>次日操作（条件式）</th></tr></thead>
    <tbody>{tmw_rows}</tbody>
  </table>
  <div class="box box-info">
    <b>次日操作执行方法：</b>次日 09:35 观察开盘 → 判断次日形态（今开 vs 前收定高开/低开，盘中今收 vs 今开定高走/低走）→ 对照上表执行。
    <br>　· <b>高开高走</b> 标的：次日若转为<b>高开低走</b> → 卖出
    <br>　· <b>高开低走</b> 标的：次日<b>高开高走</b> → 持股；<b>低开高走</b> → 持币
    <br>　· <b>低开高走</b> 标的：次日<b>低开低走</b> → 再买入（用 0.92 / 0.84 / 0.76 档）
    <br>　· <b>低开低走</b> 标的：次日<b>低开高走</b> → 持币；<b>高开高走</b> → 持股
  </div>
</section>

<section>
  <h2>三、合并主策略参数表（A + B）</h2>
  <div class="two">
    <div>
      <h3 style="color:var(--buy)">买入侧</h3>
      <table>
        <thead><tr><th>档位</th><th>系数</th><th>数量</th><th>适用形态</th></tr></thead>
        <tbody>
          <tr><td>B0 底仓</td><td class="mono">0.995</td><td>2 手</td><td>全部（A版常驻）</td></tr>
          <tr><td>B1 补仓</td><td class="mono">0.94</td><td>1 手</td><td>高开高走 / 高开低走 / 低开低走</td></tr>
          <tr><td>B2 深跌</td><td class="mono">0.88</td><td>1 手</td><td>高开高走 / 高开低走 / 低开低走</td></tr>
          <tr><td>B1′ 补仓</td><td class="mono">0.92</td><td>1 手</td><td>低开高走（B版替代 0.94）</td></tr>
          <tr><td>B2′ 深跌</td><td class="mono">0.84</td><td>1 手</td><td>低开高走（B版替代 0.88）</td></tr>
          <tr><td>B3′ 极限</td><td class="mono">0.76</td><td>1 手</td><td>低开高走（B版第三档）</td></tr>
          <tr><td>BR 接回</td><td class="mono">0.95</td><td>1 手</td><td>高开低走（B版反弹接回）</td></tr>
          <tr><td>BR 反弹</td><td class="mono">0.93</td><td>1 手</td><td>低开低走（B版反弹买入）</td></tr>
          <tr><td>B4 极限</td><td class="mono">0.60</td><td>1 手</td><td>全部（成本价基准，A版）</td></tr>
        </tbody>
      </table>
    </div>
    <div>
      <h3 style="color:var(--sell)">卖出侧</h3>
      <table>
        <thead><tr><th>档位</th><th>系数</th><th>数量</th><th>适用形态</th></tr></thead>
        <tbody>
          <tr><td>S1 快止盈</td><td class="mono">1.005</td><td>减半</td><td>全部（A版常驻）</td></tr>
          <tr><td>S2 主止盈</td><td class="mono">1.050</td><td>减半</td><td>全部（A版常驻）</td></tr>
          <tr><td>S3 顶背离</td><td class="mono">0.980</td><td>减半</td><td>全部（需顶背离确认）</td></tr>
          <tr><td>S4 强制止损</td><td class="mono">0.95</td><td>清仓</td><td>高开高走 / 高开低走(非科创) / 低开高走</td></tr>
          <tr><td>S4 强制止损</td><td class="mono">0.969</td><td>清仓</td><td>高开低走（科创专用）</td></tr>
          <tr><td>S4 强制止损</td><td class="mono">0.98</td><td>清仓</td><td>低开低走（创业板）</td></tr>
          <tr><td>S4 强制止损</td><td class="mono">0.96</td><td>清仓</td><td>低开低走（非创业板）</td></tr>
          <tr><td>S5 涨停回落</td><td class="mono">1.099 / 1.199 / 1.299</td><td>各 1/4</td><td>高开高走 / 高开低走</td></tr>
          <tr><td>S6 分批止盈</td><td class="mono">1.020 / 1.070</td><td>减半</td><td>低开低走</td></tr>
          <tr><td><b>S7 破10日线</b></td><td class="mono">MA10 × {1-MA10_BUFFER:.2f}</td><td>清仓</td><td><b>全部</b>（跌破 MA10 再下 {MA10_BUFFER*100:.0f}% 才算有效破位）</td></tr>
          <tr><td><b>S8 5日线+10%</b></td><td class="mono">MA5 × 1.10</td><td>减半</td><td><b>全部</b>（较 MA5 涨 10% 止盈）</td></tr>
        </tbody>
      </table>
    </div>
  </div>
  <div class="box box-warn">
    <b>合并规则（消歧）：</b>
    ① A版为常驻档，所有形态均挂；B版为形态调节层，按当日形态覆盖止损位与补仓档。
    ② 低开高走形态下，B版 0.92/0.84/0.76 <b>替代</b>（非叠加）A版 0.94/0.88，避免同价位重复建仓。
    ③ S3（0.98）与形态止损位重合时，<b>丢弃 S3、只留止损</b>，止损优先。
    ④ S6 的 1.05 与 S2 重合，已去重只保留 1.02 / 1.07。
    ⑤ S4 强制止损优先级最高，触发即清仓并撤销全部未成交买入单。
  </div>
</section>

<section>
  <h2>四、逐票条件单清单<span class="cnt">{total_orders} 条</span></h2>
  <p class="desc">
    基准价 = <b>{TODAY} 收盘价</b>（即 {NEXT_TRADE} 的前收盘价）。
    可达性按次日涨跌停区间校验（科创/创业 ±20%）——标<span class="badge warn">次日不可达</span>的档位当日无法成交，需顺延或改用分批。
    B4 极限档以<b>实际持仓成本</b>为基准，不代入收盘价。
  </p>
  <div class="ctrls">
    <button class="btn" onclick="document.querySelectorAll('details').forEach(d=>d.open=true)">展开全部</button>
    <button class="btn sec" onclick="document.querySelectorAll('details').forEach(d=>d.open=false)">收起全部</button>
  </div>
  {section("缠一买 · 底背驰代理（纯一类）", ["一买"], True, "当日一类信号全部与二类重叠，已归入下方「一二重叠」节")}
  {section("缠二买 · 金叉企稳代理（纯二类）", ["二买"], False)}
  {section("一二重叠 · 底背驰 + 金叉（同属一买组与二买组）", ["重叠"], True, "当日无同时触发底背驰与金叉的标的")}
  {section("缠三买 · 突破回踩代理", ["三买"], True)}
</section>

<section>
  <h2>五、执行纪律</h2>
  <div class="two">
    <div>
      <h3>时间窗口</h3>
      <table>
        <tbody>
          <tr><td>买入窗口</td><td class="mono">14:45 – 15:00</td><td>只在尾盘买，不盘中追高</td></tr>
          <tr><td>卖出窗口</td><td class="mono">次日 09:30 – 10:00</td><td>必减半，不扛单</td></tr>
          <tr><td>条件单设置</td><td class="mono">22:30 – 23:00</td><td>设次日 T+1 条件单</td></tr>
          <tr><td>1 分钟级别</td><td class="mono">S 14:54 / B 14:52</td><td>精准入场</td></tr>
        </tbody>
      </table>
    </div>
    <div>
      <h3>风控（优先级高于一切买入信号）</h3>
      <table>
        <tbody>
          <tr><td>总仓位</td><td class="mono">≤ 50%</td><td>强制执行</td></tr>
          <tr><td>单只品种</td><td class="mono">≤ 20%</td><td>永远不满仓</td></tr>
          <tr><td>大盘/板块走弱</td><td colspan="2">直接空仓，不操作</td></tr>
          <tr><td>均线</td><td colspan="2">跌破 5 日线止盈，跌破 10 日线止损</td></tr>
        </tbody>
      </table>
    </div>
  </div>
  <div class="box box-warn">
    <b>本报告为技术信号代理，非严格缠论结构确认。</b>
    严格确认需逐只还原分型（含包含处理）、笔、线段、中枢 ZG/ZD 与 MACD 面积背驰，并做日线 + 30 分钟多周期联立。
    建议将本清单作为<b>观察池 + 挂单参数</b>，优先对一买（底背驰）标的做结构精算。
    缠论为概率分析框架，非必胜系统，须配合止损与仓位管理，<b>不构成投资建议</b>。
  </div>
</section>

<footer>
  缠论扫描 · 条件单闭环　|　数据日期 {TODAY}　|　生效日 {NEXT_TRADE}　|　基准：不复权<br>
  共 {len(results)} 只标的 · {total_orders} 条条件单 · 其中 {unreachable} 条次日不可达需顺延
</footer>
</div></body></html>"""

import os
out_dir = os.path.dirname(os.path.abspath(__file__))
out = os.path.join(out_dir, f"缠论扫描_条件单闭环_{TODAY.replace('-', '')}.html")
with open(out, "w", encoding="utf-8") as f:
    f.write(html)

print("written:", out)
print("标的:", len(results), "条件单:", total_orders, "不可达:", unreachable)
for f_ in FORM_ORDER:
    print(f"  {f_}: {form_count[f_]} 只")
