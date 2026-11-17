#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
profit_guard.py — 持仓保护与第7步后续批次监控

交易日11:20检查已持仓保护；14:40检查已持仓保护与未执行的第2/3批。
所有提醒只提供信息，不代表用户买卖决定；脚本不下单。
行情使用 fetch_kline.py 的 Eastmoney→Tencent 双源、重试与 OHLC 校验。
台账中用户确认的风控参数缺失时返回 NEED_DATA，不用默认值代替。
"""
import argparse
import json
import os
import re
import sys
import tempfile
import urllib.request
from datetime import datetime, timezone, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data_guard import FetchResult, fetch_status
from trading_day import is_trading_day as _is_trading_day
# ── 数据根目录（环境变量；未设置即报错，不回落任何具体路径）──────────────
_D = os.environ.get("STOCK_DATA_DIR", "").rstrip("/")
if not _D:
    raise SystemExit(
        "🔴 未设置环境变量 STOCK_DATA_DIR（你的股票数据根目录）。\n"
        '   例：export STOCK_DATA_DIR="$HOME/stock_data"\n'
        "   目录结构见 README「数据目录约定」。"
    )

# ── Hermes 主目录（可选；未设置时依赖它的功能跳过，不报错）──────────────
_H = os.environ.get("HERMES_HOME", "").rstrip("/")


TZ = timezone(timedelta(hours=8))

# ── 持仓清单＝扫「持仓中/」目录（建仓即纳入，清仓即移出，不维护手工清单）──
#    🔴 原来这里写死持仓代码→名称→交易所前缀三元组 —— 新增/清仓都要改代码，
#       忘改＝监控范围与实际持仓漂移。现改为单来源：以目录里实际存在的台账为准。
#    名称从台账文件名取（{名称}_{代码}_跟踪台账.md），交易所前缀由代码规则推。
HOLD_DIR = _D + "/股票台账/持仓中"
# 🔴 已退役的旧价格线：禁止出现在输出里（你自己的旧线填这里；没有就留空）。
#    作用是拦截过期数字被当现价引用 —— 留空时该检查自动无事可做。
FORBIDDEN = []
ATR_PERIOD = 20
ATR_MULT = 2.0

# 台账路径（读取以台账为准）
LEDGER_DIR = _D + "/股票台账"


def _exchange_pre(code):
    """代码→交易所前缀（纯规则，无需配置）。未知号段返回 None（调用方跳过并注明）。"""
    if code[:2] in ("60", "68", "90"):
        return "sh"
    if code[:2] in ("00", "30", "20"):
        return "sz"
    if code[:1] in ("4", "8"):
        return "bj"
    return None


def scan_holdings():
    """扫 持仓中/*_跟踪台账.md → [(代码, 名称)]。目录不存在/为空→返回 []（调用方报 SILENT/说明）。"""
    import glob as _glob
    import os as _os
    import re as _re
    if not _os.path.isdir(HOLD_DIR):
        return []
    out = []
    for path in sorted(_glob.glob(HOLD_DIR + "/*_跟踪台账.md")):
        m = _re.search(r"([^/\\_]+)_(\d{6})_跟踪台账\.md$", path)
        if m:
            out.append((m.group(2), m.group(1)))
    return out


def ledger_path_for(code, name):
    return f"{HOLD_DIR}/{name}_{code}_跟踪台账.md"


def _get(url, timeout=15):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    return urllib.request.urlopen(req, timeout=timeout).read()


def fetch_realtime(pre_code):
    """腾讯实时行情。返回 FetchResult（OK / FETCH_FAIL）。

    🔴 原来失败时返回 {"error": ...}，靠下游 isinstance 判断 ——
    「取数失败」和「业务上的空」在同一个类型里，迟早有人当成后者处理。
    """
    def _do():
        txt = _get(f"https://qt.gtimg.cn/q={pre_code}").decode("gbk", errors="ignore")
        seg = txt.split('"')
        if len(seg) < 2:
            raise ValueError(f"响应结构异常：{txt[:80]!r}")
        f = seg[1].split("~")
        if len(f) < 31:
            raise ValueError(f"字段数不足（{len(f)} < 31）")
        return {"price": float(f[3]), "prev_close": float(f[4]),
                "time": f[30], "name": f[1]}

    return fetch_status(_do, tries=2, delay=0.5)


def fetch_kline(pre_code, n=320):
    """Use the shared Eastmoney→Tencent fetcher with OHLC and volume checks."""
    try:
        from fetch_kline import fetch_one
        code = pre_code[2:] if pre_code.startswith(("sh", "sz")) else pre_code
        source, bars = fetch_one(code, n)
        rows = [[b["d"], b["o"], b["c"], b["h"], b["l"], b["v"]] for b in bars]
        return FetchResult("OK", {"source": source, "bars": rows})
    except Exception as exc:
        return FetchResult("FETCH_FAIL", error=f"fetch_kline.py: {type(exc).__name__}: {exc}")


def wilder_atr(kl, period=ATR_PERIOD):
    """Wilder ATR(period)。需 period+1 根以上K线。"""
    if not isinstance(kl, list) or len(kl) < period + 1:
        return None
    trs = []
    for i in range(1, len(kl)):
        h, l, pc = float(kl[i][3]), float(kl[i][4]), float(kl[i - 1][2])
        trs.append(max(h - l, abs(h - pc), abs(l - pc)))
    a = sum(trs[:period]) / period
    for t in trs[period:]:
        a = (a * (period - 1) + t) / period
    return a


def detect_ex_dividend(kl, atr):
    """
    除权/送转机械检测：比较最近一个交易日与前一日的涨跌幅。
    若单日跌幅远超正常波动（且非涨跌停），疑似除权跳变。
    返回 (是否疑似, 说明)
    """
    if not isinstance(kl, list) or len(kl) < 3 or not atr:
        return False, ""
    last, prev = kl[-1], kl[-2]
    lc, pc = float(last[2]), float(prev[2])
    chg = (lc - pc) / pc if pc else 0
    # 正常日波动通常不超过 2*ATR/价格；留足余量
    limit = (2.5 * atr / pc) if pc else 0.05
    if abs(chg) > max(limit, 0.06):
        return True, (f"单日{chg*100:+.2f}%（{prev[0]}→{last[0]}）"
                      f"超出正常波动阈值{max(limit,0.06)*100:.2f}%，疑似除权/送转")
    return False, ""


def _read_ledger_field(code, keys, want_num=False, want_unit=False):
    """🔴 从台账 0.1 全景表读字段值。

    want_num  → 返回 float（回撤档等纯数值）
    want_unit → 按单位归一化并返回 (数值, 标签)，标签后缀标出单位：
                「10,000 股」→ (10000.0, "(股)")   股数上限
                「140 万元」  → (1400000.0, "(元)") 金额上限（按市值比）
                「30%」       → (0.30, "(%)")      组合占比

    🔴 三种单位含义完全不同，混用会让加仓模块算出荒谬的「还能买多少」。
       金额上限的好处：股价下跌时市值变小，自动腾出加仓空间；
       股数上限则是死的，涨到天上也加不了。
    """
    import re
    _hits = scan_holdings()
    _names = [n for c, n in _hits if c == code]
    if not _names:
        return None, "持仓目录里没有该标的台账（已清仓或未建仓）"
    path = ledger_path_for(code, _names[0])
    try:
        with open(path, encoding="utf-8", errors="ignore") as f:
            lines = f.read().splitlines()
    except Exception as exc:
        return None, f"台账不可读({type(exc).__name__})"

    start = None
    for i, l in enumerate(lines):
        if "0.1" in l or ("当前阶段" in l and "档案类型" in lines[min(i+1, len(lines)-1)]):
            start = i
            break
    if start is None:
        return None, "台账无 0.1 全景信息表"

    for l in lines[start:]:
        if l.strip().startswith("## ") and "0.1" not in l:
            break                        # 出了全景表
        if not l.strip().startswith("|"):
            continue
        cells = [c.strip() for c in l.strip().strip("|").split("|")]
        if len(cells) < 5:
            continue
        label = cells[1].replace("**", "").replace("*", "").strip()
        if label not in keys:
            continue
        # 🔴 取**末格**，不是第 5 格。台账行结构是
        #    | 第7步 | 字段名 | 第7步 | 状态 | 值 |
        #    第 5 格是状态标记（✅/⬜/⚠️），值在末格 —— 取错格会把状态当参数。
        val = cells[-1]
        val = val.replace("**", "").replace("*", "").strip()
        if want_num:
            # 🔴 防「从描述文字里抓数字当参数」。台账里同一格常同时写着
            # 「待商定（通用默认 成本×92%）｜实算 ¥64.58」—— 若宽松取数，
            # 会把 64.58 当成回撤百分比、或把参考数字当成用户设定值。
            # 判定：清洗后必须**以数字开头**（允许 ¥/空格/百分号），
            # 且不得含「待商定/待补充/参考/缺/未/建议」等占位或参考词。
            clean = val
            for bad in ("待商定", "待补充", "待确认", "参考", "未设", "未设定",
                        "建议", "通用默认", "实算", "锚点", "前置条件"):
                if bad in clean:
                    return None, f"「{label}」尚未由用户设定（台账值：{val[:50]}…）"
            if not re.match(r"^[¥￥]?\s*\d", clean):
                return None, f"「{label}」不是以数值开头的设定值（台账值：{val[:50]}…）"
            m = re.search(r"\d[\d,]*(?:\.\d+)?", clean)
            if not m:
                return None, f"「{label}」值无法解析：{val[:40]}"
            # 🔴 必须连逗号一起吃：台账写「10,000 股」，旧正则 \d+(?:\.\d+)? 只吃 "19"，
            #    渲染出「仓位上限 19 股」—— 少了两位数还看不出错。
            num = float(m.group().replace(",", ""))
            if want_unit:
                # 🔴 台账三种写法语义完全不同：
                #    「10,000 股」→ 股数上限（死的，涨到天上也加不了）
                #    「140 万元」  → 金额上限（按**市值**比，股价跌了自动腾出空间）
                #    「30%」       → 组合占比
                #    万元要 ×10000，否则「140万」被当成 140 元，差 4 个数量级。
                if "万" in clean:
                    num *= 10000
                    return num, label + "(元)"
                if "亿" in clean:
                    num *= 100000000
                    return num, label + "(元)"
                if "股" in clean:
                    return num, label + "(股)"
                if "元" in clean or "¥" in clean or "￥" in clean:
                    return num, label + "(元)"
                return (num / 100.0), label + "(%)"
            return num, label
        return val, label
    return None, f"全景表里找不到字段 {'/'.join(keys)}"


def judge_modules(cost, px, peak, peak_drawdown, loss_warn, loss_stop,
                  cap_weight, peak_note="未提供", cap_unit="%", shares=0):
    """🔴 三模块纯算术判定（本工作流裁定）。

    返回 dict，含各模块 status 与建议动作。**不给投资建议，只报状态。**
    - 模块一 盈利保护：锚【峰值】。判定不只看现价 vs 成本（见下方 223-225 行注释）；
      仅当峰值不可得时才按「现价 < 成本 → 归模块二」归口
    - 模块二 亏损保护：锚【成本】。−8% 预警 / −15% 决策点
    - 模块三 加仓建议：需仓位上限；缺上限直接报缺参，不猜
    """
    out = {}
    pnl_pct = (px / cost - 1) * 100

    # ── 模块一：盈利保护（峰值回撤）
    #    🔴 判定不能只看「现价 vs 成本」。峰值回撤保护的是**浮盈退潮**，
    #    即使现价已跌回成本下方，只要曾有可观浮盈、现在从峰值大幅回落，
    #    就仍然要报 —— 否则「涨过又跌回」这段最该提醒的区间会静默。
    if peak_drawdown is None or len(peak_drawdown) != 2 or any(v is None or v <= 0 for v in peak_drawdown):
        out["profit"] = {"status": "NEED_DATA", "reason": "盈利保护回撤档未由用户确认"}
    elif peak is None:
        # 峰值现在由脚本从日K自算，peak_note 携带真实失败原因；
        # 🔴 别再写「台账未设定」—— 台账里根本没这个字段，那是旧设计的遗留文案。
        out["profit"] = (
            {"status": "NEED_DATA",
             "reason": f"峰值无法自算（{peak_note}）—— 需先核对台账《交易记录》的首次买入日期"}
            if px >= cost else
            {"status": "N/A", "reason": f"现价 {px:.2f} < 成本 {cost:.2f}"
                    f"（浮亏 {pnl_pct:+.1f}%），无峰值回撤可言 → 归入亏损保护"}
        )
    else:
        dd = (px / peak - 1) * 100
        lines = [round(peak * (1 - peak_drawdown[0] / 100), 2),
                 round(peak * (1 - peak_drawdown[1] / 100), 2)]
        if dd <= -peak_drawdown[1]:
            st, act = "RED", "已达盈利保护二档提醒线；是否处置由用户决定"
        elif dd <= -peak_drawdown[0]:
            st, act = "YELLOW", "已达盈利保护一档提醒线；是否处置由用户决定"
        elif px < cost:
            st, act = "RED", "峰值回撤已吃光浮盈且现价低于成本；请用户复核，不构成卖出指令"
        else:
            st, act = "OK", (f"距一档线 {lines[0]:.2f} 还差 "
                    f"{abs(-dd - peak_drawdown[0]):.1f}pt（当前回撤 {dd:.1f}%）")
        out["profit"] = {
            "status": st, "drawdown_pct": round(dd, 2), "peak": peak, "lines": lines,
            "suggest": act,
        }

    # ── 模块二：亏损保护（成本锚）
    if loss_warn is None or loss_stop is None or loss_warn <= 0 or loss_stop <= 0:
        out["loss"] = {"status": "NEED_DATA", "reason": "亏损保护两档未由用户确认"}
    else:
        warn_line, stop_line = cost * (1 - loss_warn / 100), cost * (1 - loss_stop / 100)
        if pnl_pct <= -loss_stop:
            st, act = "RED", "已达亏损保护止损提醒线；请用户自行判断并决定，不授权卖出"
        elif pnl_pct <= -loss_warn:
            st, act = "YELLOW", f"已达亏损保护预警线（{pnl_pct:+.1f}%），距离止损提醒线 {stop_line:.2f}"
        else:
            st, act = "OK", f"距预警线 {warn_line:.2f} 还有 {pnl_pct + loss_warn:.1f}pt（当前 {pnl_pct:+.1f}%）"
        out["loss"] = {
            "status": st, "pnl_pct": round(pnl_pct, 2),
            "warn_line": round(warn_line, 2), "stop_line": round(stop_line, 2),
            "suggest": act,
        }

    # ── 模块三：加仓前置（只报能不能给建议，不主动推加仓）
    #     三种上限（本工作流）：
    #     「股」→ 股数上限，与当前持仓比，得出 FULL / 还可加 N 股（**死的**）
    #     「元」→ 金额上限，与当前**市值**比；股价下跌自动腾出空间（**活的**）
    #     「%」 → 组合占比（需账户总额才能折算股数，脚本无从得知 → 只报上限本身）
    if cap_weight is None:
        out["add"] = {"status": "NEED_DATA", "reason": "台账未设定单股仓位上限 → 无法计算还能买多少，不猜"}
    elif cap_unit == "股":
        room = cap_weight - shares
        if room <= 0:
            out["add"] = {
                "status": "FULL", "cap_shares": cap_weight, "shares": shares,
                "note": (f"仓位上限 {cap_weight:,.0f} 股 ＝ 当前持仓 {shares:,.0f} 股，"
                         f"**已满仓，无加仓空间**"),
                "suggest": "已到仓位上限 —— 模块三所有加仓场景（A–F）一律不适用",
            }
        else:
            out["add"] = {
                "status": "READY", "cap_shares": cap_weight, "shares": shares,
                "room_shares": room,
                "note": f"仓位上限 {cap_weight:,.0f} 股，当前 {shares:,.0f} 股，尚可加 {room:,.0f} 股",
                "suggest": ("加仓前置条件具备，但**本脚本不主动推加仓** —— "
                            "需按技能 9.3 的 A–F 场景逐条人工判定（含组合层检查）"),
            }
    elif cap_unit == "元":
        mkt_val = shares * px if px and shares else None
        if mkt_val is None:
            out["add"] = {"status": "NEED_DATA",
                          "reason": "有现价或持仓数缺失，无法算当前市值与金额上限比较"}
        else:
            room_mv = cap_weight - mkt_val
            if room_mv <= 0:
                out["add"] = {
                    "status": "FULL", "cap_value": cap_weight, "mkt_value": mkt_val,
                    "note": (f"金额上限 {cap_weight/10000:,.0f} 万元 ≤ 当前市值 "
                             f"{mkt_val/10000:,.0f} 万元（{shares:,.0f} 股 ×{px:.2f}），"
                             f"**已超/满仓，无加仓空间**"),
                    "suggest": "已到金额上限 —— 模块三所有加仓场景（A–F）一律不适用",
                }
            else:
                # 金额上限是「活」的：可用金额 ÷ 现价 = 理论上还能买多少股
                room_sh = room_mv / px if px else None
                out["add"] = {
                    "status": "READY", "cap_value": cap_weight, "mkt_value": mkt_val,
                    "room_value": room_mv, "room_shares_est": room_sh,
                    "note": (f"金额上限 {cap_weight/10000:,.0f} 万元，当前市值 "
                             f"{mkt_val/10000:,.0f} 万元，尚可加 {room_mv/10000:,.2f} 万元"
                             f"（≈{room_sh:,.0f} 股，按现价 {px:.2f} 估算）"),
                    "suggest": ("加仓前置条件具备，但**本脚本不主动推加仓** —— "
                                "需按技能 9.3 的 A–F 场景逐条人工判定（含组合层检查）"),
                }
    else:
        out["add"] = {
            "status": "READY",
            "cap": cap_weight,
            "note": f"仓位上限 {cap_weight:.1%}（组合占比）。🔴 折算股数需账户总额，"
                    f"脚本无从得知 → 只报上限，不估算还能买多少股",
            "suggest": "加仓前置条件具备，但**本脚本不主动推加仓** —— "
                       "需按技能 9.3 的 A–F 场景逐条人工判定（含组合层检查）",
        }
    return out


def read_ledger_trades(code):
    """🔴 本工作流裁定重写。

    台账只存**交易事实**（日期/方向/成交价/数量）。两件事全部由脚本算：
      · 加权成本  = Σ(成交价×数量) / Σ数量      —— 含手续费口径即用户券商App口径
      · 峰值起点  = 首次买入交易日

    之前设计让用户手填「持仓期最高价」，是错的：峰值是市场数据、能算就不该人填，
    而且会随每次新高过期，混在台账里分不清哪些是客观数据、哪些是风控边界。

    🔴 绝不从正文说明性文字里抓数字（那些行含"成交价"字样但不是成交记录）。
    🔴 解析失败**不回落内置基线** —— 读不到就报 NEED_DATA。
    返回 (trades, source)；trades=None 表示不可得。
    trades = [{"date":ISO, "side":"买入|卖出", "price":float, "qty":int}, ...]
    """
    import re
    _hits = scan_holdings()
    _names = [n for c, n in _hits if c == code]
    if not _names:
        return None, "持仓目录里没有该标的台账（已清仓或未建仓）"
    path = ledger_path_for(code, _names[0])
    try:
        with open(path, encoding="utf-8", errors="ignore") as f:
            lines = f.read().splitlines()
    except Exception as exc:
        return None, f"🔴台账不可读({type(exc).__name__})"

    # 只在「交易记录」表区域内解析：表头含 序号|日期|方向|成交价|数量
    start = None
    for i, l in enumerate(lines):
        if "序号" in l and "成交价" in l and "数量" in l:
            start = i
            break
    if start is None:
        return None, "🔴台账无交易记录表"

    trades = []
    for l in lines[start + 1:]:
        if not l.strip().startswith("|"):
            break                      # 表格结束
        cells = [c.strip() for c in l.strip().strip("|").split("|")]
        if len(cells) < 6:
            continue
        _, date_c, direction, price_c, qty_c = cells[0], cells[1], cells[2], cells[3], cells[4]
        side = "买入" if any(k in direction for k in ("买入", "加仓", "补仓")) else (
               "卖出" if any(k in direction for k in ("卖出", "减仓", "止盈", "止损")) else None)
        if side is None:
            continue
        # 日期取前 10 位（台账写 "2026-09-30 尾盘（约14:40）"，只取日期部分）
        md = re.search(r"(\d{4}-\d{2}-\d{2})", date_c)
        mp = re.search(r"[\d.]+", price_c)
        mq = re.search(r"([\d,]+)", qty_c)
        if not (md and mp and mq):
            continue
        qty = int(mq.group().replace(",", ""))
        if qty <= 0:
            continue
        batch_match = re.search(r"第([123])批", direction)
        trades.append({"date": md.group(1), "side": side,
                       "price": float(mp.group()), "qty": qty,
                       "batch": int(batch_match.group(1)) if batch_match else None})

    if not trades:
        return None, "🔴台账交易记录表无有效成交行"
    return trades, "台账交易记录"


def weighted_cost(trades):
    """🔴 从逐笔交易算当前加权成本 —— 不是「成本线」，是**持仓均价**。

    卖出按剩余仓位口径处理：卖出只让持仓量减少，不改变剩余股份的原始成本
    （券商App的「摊薄成本」与此一致），除非台账显式记录了「卖出即摊薄」。
    🔴 因此只按**买入/加仓**累计；卖出笔数用于校验数量，不参与均价。
    """
    buys = [t for t in trades if t["side"] == "买入"]
    if not buys:
        return None
    total_q = sum(t["qty"] for t in buys)
    if total_q <= 0:
        return None
    return sum(t["price"] * t["qty"] for t in buys) / total_q


def compute_peak(kl, since_date):
    """🔴 本工作流裁定：**持仓以来的日最高价**，峰值起点＝台账首次买入交易日。

    为什么由脚本算而不是用户填：
      · 峰值是**市场客观数据**，能算就不该让人手填；
      · 手填会随每次新高过期，而监控每天都要用；
      · 混在台账里分不清哪些是客观行情、哪些是用户风控边界。

    与「持仓多少」无关：加仓/减仓都不改变峰值口径（本工作流明确）。
    口径细节：
      · 用**日K最高价**，不使用盘中实时最高 —— 避免观察时点落在盘中导致
        峰值基准在 11:20 / 14:40 两点间不一致；
      · **含买入当日**（当日高点即持仓期间的一部分）；
      · 前复权价序列内部一致即可算回撤率；但本函数返回的是**复权口径**的峰���，
        与当日现价同源，可直接相除。
    返回 (peak, peak_date, note)；不可得返回 (None, None, 原因)。
    """
    if not kl or not since_date:
        return None, None, "无K线或无首次买入日期"
    # 🔴 腾讯 qfqday 每行是 **[日期, 开, 收, 高, 低, 量]** 的列表，不是 dict。
    #   早先按 dict 取 r["date"]/r["high"] → 恒为 None，峰值永远算不出来。
    rows = []
    for r in kl:
        if len(r) < 4:
            continue
        d, hi = r[0], r[3]
        if d >= since_date:
            rows.append((d, float(hi)))
    if not rows:
        return None, None, (f"K线无 {since_date} 及之后的交易日"
                            f"（台账首次买入日可能过新，或早于当前取数窗口起点）")
    # 🔴 rows 是 (日期, 最高价)，max 按第二个元素排序 —— 解包要 (peak_at, peak)，
    #    写反的话 peak 会拿到日期字符串，随后 px / peak 直接 TypeError。
    peak_at, peak = max(rows, key=lambda x: x[1])
    return peak, peak_at, f"持仓首日 {since_date} 起共 {len(rows)} 个交易日日K最高"


def current_shares(trades):
    """当前持仓量 = Σ买入量 − Σ卖出量（台账《交易记录》＝唯一权威源）。

    🔴 持仓清单以「持仓中/」目录为准 —— 写死在代码里是第二来源，会漂移。
    算不出（无交易记录）返回 None，由调用方报故障，**不猜**。
    """
    if not trades:
        return None
    b = sum(t["qty"] for t in trades if t["side"] == "买入")
    s = sum(t["qty"] for t in trades if t["side"] == "卖出")
    return b - s


def first_buy_date(trades):
    buys = [t for t in trades if t["side"] == "买入"]
    if not buys:
        return None
    return min(t["date"] for t in buys)


def is_trading_day(now, probe="sh600000"):
    """🔴 改用 trading_day 模块正式判定（探针＝首只持仓代码；无持仓时用默认高流动性探针）。

    原实现只判「周一至周五 = 交易日」—— **实测会错**：
    长假期间（如国庆 10-01~10-07 休市，工作日但不出K线）会被粗判当成交易日。
    影响面：休市日运行会拿旧收盘价当现价做判断，或让用户误以为当天有行情。

    返回 (是否交易日, 说明)；判定失败按「非交易日」处理 —— 宁可不判，不错判。
    """
    from trading_day import is_trading_day as _td
    d = now.strftime("%Y-%m-%d")
    try:
        ok, note, _src = _td(d, pre_code=probe)
        return ok, note
    except Exception as exc:
        return False, f"🔴 交易日判定失败({type(exc).__name__})→ 按非交易日处理"


def _ledger_batch_rule(code, name, batch_no):
    """Read explicit batch metadata from the holding ledger; never guess conditions."""
    path = ledger_path_for(code, name)
    try:
        lines = open(path, encoding="utf-8").read().splitlines()
    except OSError as exc:
        return None, "", f"台账不可读：{exc}"
    for line in lines:
        if f"batch={batch_no}" not in line:
            continue
        m = re.search(r"monitor_rule=([A-Z0-9_]+)", line)
        if m:
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            return m.group(1), (cells[-1] if cells else ""), ""
    return None, "", f"第{batch_no}批缺机器可读规则标记；须先确认规则后再运行监控"


def _ema(values, span):
    alpha = 2.0 / (span + 1.0)
    out = [values[0]]
    for value in values[1:]:
        out.append(alpha * value + (1 - alpha) * out[-1])
    return out


def _macd_values(closes):
    if len(closes) < 35:
        return None
    diffs = [a - b for a, b in zip(_ema(closes, 12), _ema(closes, 26))]
    return diffs, _ema(diffs, 9)


def _batch_state_path():
    return os.path.join(_D, ".profit_guard_batch_state.json")


def _evaluate_batches(code, name, kl, trades, slot, live_price=None):
    """Step 7 checks pending batches only at 14:40; alerts never authorize orders."""
    if slot != "14:40":
        return []
    if not kl:
        return [{"batch": None, "status": "FAULT_ONCE", "reason": "K线不可用"}]
    alerts = []
    for batch_no in (2, 3):
        rule, ledger_status, error = _ledger_batch_rule(code, name, batch_no)
        if error:
            alerts.append({"batch": batch_no, "status": "NEED_CONFIRM", "reason": error})
            continue
        if any(token in ledger_status for token in ("已成交", "已执行", "已放弃", "风险暂停")):
            alerts.append({"batch": batch_no, "status": "DONE"})
            continue
        if rule == "B2_MACD_VOL_1_5":
            closes = [float(row[2]) for row in kl]
            volumes = [float(row[5]) for row in kl]
            macd = _macd_values(closes)
            if macd is None or len(volumes) < 21:
                alerts.append({"batch": batch_no, "status": "NEED_DATA", "reason": "MACD或20日均量样本不足"})
                continue
            dif, dea = macd
            base = sum(volumes[-21:-1]) / 20
            ratio = volumes[-1] / base if base else 0.0
            if dif[-2] <= dea[-2] and dif[-1] > dea[-1] and ratio >= 1.5:
                alerts.append({"batch": batch_no, "status": "REVIEW", "rule": rule,
                               "dif": round(dif[-1], 5), "dea": round(dea[-1], 5),
                               "volume_ratio": round(ratio, 3), "bar_date": kl[-1][0],
                               "note": "MACD事件金叉且量比≥1.5；仅提醒，待用户决定"})
            else:
                alerts.append({"batch": batch_no, "status": "SILENT"})
        elif rule == "B3_CLOSE_MA60_FLAT_ANTICHASE":
            if len(kl) < 61 or live_price is None:
                alerts.append({"batch": batch_no, "status": "NEED_DATA", "reason": "MA60样本或14:40实时价缺失"})
                continue
            closes = [float(row[2]) for row in kl]
            today = datetime.now(TZ).date().isoformat()
            prior = closes[:-1] if str(kl[-1][0])[:10] == today else closes
            if len(prior) < 60:
                alerts.append({"batch": batch_no, "status": "NEED_DATA", "reason": "当日MA60有效样本不足"})
                continue
            ma_now = (sum(prior[-59:]) + float(live_price)) / 60
            ma_prev = sum(prior[-60:]) / 60
            price = float(live_price)
            if price >= ma_now and ma_now >= ma_prev:
                buys = [trade for trade in (trades or []) if trade["side"] == "买入"]
                b2 = [trade for trade in buys if trade.get("batch") == 2]
                b1 = [trade for trade in buys if trade.get("batch") == 1]
                base_trades = b2 or b1
                if not base_trades:
                    alerts.append({"batch": batch_no, "status": "NEED_CONFIRM", "rule": rule,
                                   "reason": "防追高基准缺失：交易记录须标注所属批次"})
                    continue
                baseline = sum(t["price"] * t["qty"] for t in base_trades) / sum(t["qty"] for t in base_trades)
                gain = (price / baseline - 1) * 100
                if gain > 25:
                    action = "预设防追高分档为跳过（保留现金）；是否继续等待由用户决定"
                elif gain > 15:
                    action = "预设防追高分档为半额；是否执行由用户决定"
                else:
                    action = "预设防追高分档为全额；是否执行由用户决定"
                alerts.append({"batch": batch_no, "status": "REVIEW", "rule": rule,
                               "price": round(price, 3), "ma60": round(ma_now, 3),
                               "ma60_prev": round(ma_prev, 3), "gain_pct": round(gain, 2),
                               "baseline": round(baseline, 3), "bar_date": kl[-1][0],
                               "note": action})
            else:
                alerts.append({"batch": batch_no, "status": "SILENT"})
        else:
            alerts.append({"batch": batch_no, "status": "NEED_CONFIRM", "rule": rule,
                           "reason": "规则标记未支持；不按近似条件判定"})
    return alerts


def _dedupe_batch_alerts(code, alerts):
    """Alert each continuously true rule once; re-arm after it becomes false."""
    path = _batch_state_path()
    try:
        state = json.loads(open(path, encoding="utf-8").read())
        if not isinstance(state, dict):
            state = {}
    except (OSError, ValueError):
        state = {}
    output = []
    for alert in alerts:
        batch = alert.get("batch")
        key = f"{code}:{batch}"
        if alert.get("status") == "REVIEW":
            if key not in state:
                state[key] = datetime.now(TZ).date().isoformat()
                output.append(alert)
        else:
            if batch is not None and alert.get("status") not in ("NEED_CONFIRM", "NEED_DATA", "FAULT_ONCE"):
                state.pop(key, None)
            output.append(alert)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    os.replace(tmp, path)
    return output


def main():
    ap = argparse.ArgumentParser()
    # 🔴 cron 的 no_agent 只能跑 `python3 profit_guard.py`，无法传参。
    # 因此 --slot 必须可选 —— 缺省时按当前时间就近归入 11:20 / 14:40 两个观察点。
    ap.add_argument("--slot", choices=["11:20", "14:40"], default=None,
                    help="留空则按当前时间自动判定（<13:00 → 11:20，否则 14:40）")
    # 🔴🔴 安全修复：cron 的 no_agent 只能跑 `python3 profit_guard.py`，
    # **无法传 --no-agent**。若缺省为 False，完整 JSON（含 cost/price/ATR）会进 stdout，
    # 而 no_agent 的 stdout 会被原样投递到飞书 → 持仓数字泄漏。
    # 因此这里默认 True（安全侧），只有显式 --with-json 才输出完整 JSON。
    ap.add_argument("--with-json", dest="no_agent", action="store_false",
                    help="输出完整 JSON 到 stdout（含持仓数字，仅限本机手动排查用）")
    ap.set_defaults(no_agent=True)
    ap.add_argument("--json-out", default=None)
    # ⭐ 本工作流确认：盈利保护通知**照发邮件**（飞书＋邮件双通道）。
    # 邮件内容与飞书一致，含具体数值 —— 隐私边界只针对飞书云文档，不针对自己的邮件。
    ap.add_argument("--mail", action="store_true", help="REVIEW/FAULT 时另发一封邮件")
    # ⭐ 14:40 收盘确认模式（本工作流规定）：与 11:20 的职责不同 ——

    ap.add_argument("--mail-to", default=None, help="覆盖收件人（默认取 smtp.json）")
    
    args = ap.parse_args()

    now = datetime.now(TZ)
    _holdings_probe = scan_holdings()
    _probe = (_exchange_pre(_holdings_probe[0][0]) or "sh") + _holdings_probe[0][0] \
        if _holdings_probe and _exchange_pre(_holdings_probe[0][0]) else "sh600000"
    ok_day, day_note = is_trading_day(now, _probe)
    result = {
        "slot": args.slot or _auto_slot(now),
        "run_at": now.isoformat(),
        "trading_day": ok_day,
        "day_note": day_note,
        "threshold_formula": "盈利保护=持仓期峰值×(1−用户确认回撤档)｜亏损保护=加权成本×(1−用户确认回撤档)｜缺少用户参数时 NEED_DATA，不回落默认值",
        "forbidden_lines": FORBIDDEN,
        "results": [],
        "batch_alerts": [],
        "anomalies": [],
        "action": "SILENT",
        "reason": "",
    }

    result["_no_agent"] = bool(args.no_agent)
    result["_mail"] = bool(args.mail)
    if not ok_day:
        result["reason"] = f"非交易日（{day_note}），不做价格判断"
        _emit(result, args.json_out)
        return

    holdings = _holdings_probe
    if not holdings:
        result["reason"] = "持仓目录为空（无持仓台账），无标的可监控"
        _emit(result, args.json_out)
        return
    for code, name in holdings:
        pre = _exchange_pre(code)
        if not pre:
            result.setdefault("skipped", []).append(f"{code}：未知号段，无法确定交易所前缀，已跳过")
            continue
        pre_code = pre + code
        trades, trade_src = read_ledger_trades(code)
        cost = weighted_cost(trades) if trades else None
        cost_src = f"{trade_src}·脚本自算（Σ价×量/Σ量）" if cost else trade_src
        rt_r = fetch_realtime(pre_code)
        kl_r = fetch_kline(pre_code)
        rt = rt_r.value if rt_r.ok else None
        kline_payload = kl_r.value if kl_r.ok else None
        kl = kline_payload["bars"] if kline_payload else None
        kline_source = kline_payload["source"] if kline_payload else None

        batch_alerts = _evaluate_batches(
            code, name, kl, trades, result["slot"],
            live_price=(rt.get("price") if rt else None))
        batch_alerts = _dedupe_batch_alerts(code, batch_alerts)
        for alert in batch_alerts:
            alert["kline_source"] = kline_source
            alert["checked_at"] = rt.get("time") if rt else result["run_at"]
        result["batch_alerts"].append({"code": code, "name": name, "alerts": batch_alerts})
        for alert in batch_alerts:
            if alert["status"] not in ("SILENT", "DONE"):
                result["anomalies"].append(
                    f"{name} {code}【第{alert.get('batch') or '?'}批买入监控】"
                    f"{alert['status']}｜{alert.get('note') or alert.get('reason') or ''}")

        item = {
            "code": code, "name": name,
            "cost": cost, "cost_source": cost_src,
            "_kl": kl,
        }

        # 🔴 成本不可得 → 阈值算不出来，绝不能用内置基线凑一个数出来
        if cost is None:
            item["status"] = "data_failed"
            item["detail"] = f"成本不可得：{cost_src}"
            result["results"].append(item)
            result["anomalies"].append(
                f"{name} {code} 成本读取失败（{cost_src}）→ 阈值无法计算")
            continue

        if rt_r.failed:
            item["status"] = "data_failed"
            item["detail"] = f"实时行情取数失败：{rt_r.error}"
            result["results"].append(item)
            result["anomalies"].append(f"{name} {code} 实时价获取失败")
            continue

        if kl_r.failed:
            item["status"] = "data_failed"
            item["detail"] = f"K线取数失败：{kl_r.error}"
            result["results"].append(item)
            result["anomalies"].append(f"{name} {code} K线获取失败")
            continue

        atr = wilder_atr(kl)
        if not atr:
            item["status"] = "data_failed"
            item["detail"] = "atr_insufficient_klines"
            result["results"].append(item)
            result["anomalies"].append(f"{name} {code} K线不足，ATR无法计算")
            continue

        px = rt["price"]
        exd, exd_note = detect_ex_dividend(kl, atr)

        # 🔴 三模块判定。
        #    峰值＝脚本从日K自算（持仓以来日最高价，起始日＝台账首次买入日）——
        #    本工作流明确：峰值是客观行情，不由人手填。
        #    🔴 唯一需要你手填的是「你的风控边界」：两档回撤 + 单股仓位上限。
        peak_date = first_buy_date(trades) if trades else None
        # 🔴 compute_peak 返回 (peak, peak_at, note) 三元组 —— 解包顺序必须对上，
        #   否则 peak_at(日期字符串) 会落进 peak_src 甚至当数值用（曾致 TypeError）。
        peak, peak_at, peak_note = compute_peak(kl, peak_date)
        peak_src = (f"🔴{peak_note}" if peak is None
                    else f"K线自算：{peak_note}，峰值日 {peak_at}")
        cap, cap_src = _read_ledger_field(code, ("单股仓位上限",), want_num=True,
                                        want_unit=True)
        # 🔴 台账三种写法：「10,000 股」股数 / 「140 万元」金额 / 「30%」组合占比
        cap_unit = ("股" if cap_src.endswith("(股)") else
                    "元" if cap_src.endswith("(元)") else "%")
        loss_warn, _ = _read_ledger_field(code, ("亏损保护预警回撤", "亏损保护预警档"), want_num=True)
        loss_stop, _ = _read_ledger_field(code, ("亏损保护止跌回撤", "亏损保护止跌档"), want_num=True)
        pd1, _ = _read_ledger_field(code, ("盈利保护一档回撤",), want_num=True)
        pd2, _ = _read_ledger_field(code, ("盈利保护二档回撤",), want_num=True)
        # Parameters are user risk boundaries: missing values must fail closed, never default.
        PEAK_DD = (pd1, pd2)
        LOSS_W = loss_warn
        LOSS_S = loss_stop
        # 🔴 台账可能写「10,000 股」（已满仓）或「30%」（组合占比）。
        #    _read_ledger_field(want_shares=True) 已按单位分别归一化：
        #    股 → 原值(10000)、% → 0.30。**这里不要再除 100** ——
        #    旧写法 cap/100 会把 10000 股变成 100，「已满仓」被误判成「还能加 9900 股」。
        cap_w = cap

        # 🔴 持仓量由台账《交易记录》算（Σ买−Σ卖），不在代码里写死持仓；
        #    并与台账 §持仓汇总表的「当前持仓数量」交叉核对 —— 不一致说明台账内部打架。
        shares = current_shares(trades)
        if shares is None:
            result["anomalies"].append(
                f"🔴 {name} {code} 台账无交易记录，持仓量算不出（模块三将报 NEED_DATA）")
        else:
            led_sh, _ = _read_ledger_field(code, ("当前持仓数量",), want_num=True)
            if led_sh is not None and abs(shares - led_sh) > 0.5:
                result["anomalies"].append(
                    f"🔴 {name} {code} 台账自相矛盾：《交易记录》算出 {shares:,.0f} 股，"
                    f"§持仓汇总写 {led_sh:,.0f} 股 —— 需人工核对")

        mods = judge_modules(cost, px, peak, PEAK_DD, LOSS_W, LOSS_S, cap_w,
                            peak_note if peak is None else '已自算',
                            cap_unit, shares or 0)

        item.update({
            "price": px,
            "price_time": rt["time"],
            "kline_last_date": kl[-1][0],
            "atr20": round(atr, 4),
            "modules": mods,
            "params": {
                "cost": cost, "cost_source": cost_src,
                "peak": peak, "peak_source": peak_src,
                "peak_date": peak_at, "peak_since": peak_date,
                "trades_n": len(trades) if trades else 0,
                "shares": shares,
                "shares_source": "台账《交易记录》Σ买−Σ卖",
                "peak_drawdown": list(PEAK_DD),
                "loss_warn": LOSS_W, "loss_stop": LOSS_S,
                "cap_weight": cap_w, "cap_source": cap_src,
                "from_ledger": bool(peak and cap_w and loss_warn and loss_stop),
            },
            # 保留旧字段名以兼容既有渲染/校验
            "threshold": mods.get("loss", {}).get("warn_line"),
            "gap_to_threshold": (round(mods["loss"]["warn_line"] - px, 4)
                                 if mods.get("loss", {}).get("warn_line") else None),
            "triggered": any(m.get("status") in ("YELLOW", "RED") for m in mods.values()),
            "ex_dividend_suspect": exd,
            "ex_dividend_note": exd_note,
        })
        result["results"].append(item)

        if exd:
            result["anomalies"].append(
                f"{name} {code}疑似除权/送转：{exd_note} — 需大模型确认成本/价格口径是否需调整")
        for key, label in (("profit", "盈利保护"), ("loss", "亏损保护"), ("add", "加仓前置")):
            m = mods.get(key, {})
            if m.get("status") in ("YELLOW", "RED"):
                result["anomalies"].append(f"{name} {code}【{label}】{m.get('status')}｜{m.get('suggest')}")
            elif m.get("status") == "NEED_DATA":
                result["anomalies"].append(f"{name} {code}【{label}】缺参数：{m.get('reason')}")

    # 决定是否需要大模型
    # 🔴 优先级：全部失败 → FAULT_ONCE（按规则只报一次简讯，避免重复报同一故障）
    # 部分失败但有一只可算 → REVIEW（需报告失败那只，避免漏掉风险）
    valid = [r for r in result["results"] if r.get("status") != "data_failed"]
    failed = [r for r in result["results"] if r.get("status") == "data_failed"]
    triggered = [r for r in valid if r.get("triggered")]

    batch_notices = [a for g in result.get("batch_alerts", []) for a in g.get("alerts", [])
                    if a.get("status") in ("REVIEW", "NEED_CONFIRM", "NEED_DATA", "FAULT_ONCE")]
    if batch_notices:
        result["action"] = "FAULT_ONCE" if all(a.get("status") == "FAULT_ONCE" for a in batch_notices) else "REVIEW"
        result["reason"] = "第7步后续批次监控需要提醒或人工核验"
    elif not valid and failed:
        result["action"] = "FAULT_ONCE"
        result["reason"] = "全部标的行情/ATR获取失败 → 不得报告触发；按规则报一次简讯，避免重复报同一故障"
    elif result["anomalies"]:
        result["action"] = "REVIEW"
        result["reason"] = "触发或存在异常，需复核后决定是否通知"
    else:
        result["action"] = "SILENT"
        result["reason"] = "三模块与后续批次条件均未触发，且数据有效 → 静默"

    _emit(result, args.json_out)


def _auto_slot(now):
    """cron 不传 --slot 时，按当前时间归入最近的观察点（11:20 / 14:40）。"""
    return "11:20" if now.hour < 13 else "14:40"


def _render_for_delivery(result, with_numbers=True):
    """生成可直接投递到飞书/邮件的成稿。

    ⭐ 本工作流确认：**消息/邮件里直接写清楚数值**（成本、现价、ATR、阈值、差距）。
    隐私边界只针对 **飞书云文档**（台账同步），那里由 sync_ledgers_to_feishu.py 硬排除第7步。
    with_numbers=False 时退化为无数值版，供云端文档场景使用。
    SILENT → 返回空字符串（no_agent 静默成功）。
    """
    act = result.get("action")
    if act == "SILENT":
        return ""
    L = [f"**第7步持仓与分批监控 · {result.get('slot')} · {result.get('run_at','')[:10]}**", ""]
    n = with_numbers

    if act == "FAULT_ONCE":
        L += ["⚠️ 本次无法确认持仓保护状态（行情或数据获取异常）。", "",
              f"原因：{result.get('reason','')}", ""]
        for group in result.get("batch_alerts", []):
            for alert in group.get("alerts", []):
                if alert.get("status") not in ("SILENT", "DONE"):
                    L.append(f"- {group.get('name')}（{group.get('code')}）第{alert.get('batch') or '?'}批：{alert.get('reason') or alert.get('note') or alert['status']}")
        L += ["", "🔴 数据不可验证时不报告买入触发，不做推断。"]
        return "\n".join(L)

    trig = [r for r in result.get("results", []) if r.get("triggered")]
    need = [r for r in result.get("results", [])
            if any(m.get("status") == "NEED_DATA" for m in (r.get("modules") or {}).values())]
    sus = [r for r in result.get("results", []) if r.get("ex_dividend_suspect")]
    failed = [r for r in result.get("results", []) if r.get("status") == "data_failed"]

    L += ["**判定口径**（🔴 锚点不可混用）：",
          "| 模块 | 锚点 | 触发线 |",
          "|---|---|---|",
          "| 盈利保护 | 持仓期峰值 | 峰值 × (1−回撤档) |",
          "| 亏损保护 | 加权成本 | 成本 × (1−档位) |",
          "| 加仓建议 | 仓位空间 | 需先有单股仓位上限 |", ""]

    for r in trig:
        mods = r.get("modules") or {}
        L += [f"🔔 **{r.get('name')}（{r.get('code')}）**", ""]
        if n:
            L.append(f"- 现价 **{r.get('price')}**｜加权成本 **{r.get('cost')}**｜"
                     f"数据时点 {r.get('price_time') or '—'}")

        p = mods.get("profit", {})
        if p.get("status") == "N/A":
            L.append(f"- **盈利保护**｜{p.get('reason')}")
        elif p.get("status") in ("YELLOW", "RED"):
            lines = p.get("lines") or []
            L.append(f"- 🔴/🟡 **盈利保护 {p.get('status')}**｜峰值 **{p.get('peak')}**"
                     f"｜当前回撤 **{p.get('drawdown_pct')}%**"
                     + (f"｜一档线 {lines[0]}／二档线 {lines[1]}" if len(lines) == 2 else ""))
            L.append(f"  → {p.get('suggest')}")

        ls = mods.get("loss", {})
        if ls.get("status") in ("YELLOW", "RED"):
            L.append(f"- 🔴/🟡 **亏损保护 {ls.get('status')}**｜浮盈亏 **{ls.get('pnl_pct')}%**"
                     f"｜预警线 {ls.get('warn_line')}／止跌线 {ls.get('stop_line')}")
            L.append(f"  → {ls.get('suggest')}")
            L.append("  🔴 **需同时核实公司端证据**：是纯价格波动，还是有硬信号（现金流/扣非转负、逻辑走弱）。"
                     "这一区分决定「割」还是「扛」。")

        ad = mods.get("add", {})
        if ad.get("status") == "NEED_DATA":
            L.append(f"- ⚠️ **加仓建议**｜{ad.get('reason')}")
        elif ad.get("status") == "FULL":
            # 🔴 FULL 也带 note（上限股数/当前持仓/无空间），别只打一句空话
            L.append(f"- 🔒 **加仓建议：已满仓**｜{ad.get('note')}")
        elif ad.get("status") == "READY":
            L.append(f"- ℹ️ **加仓前置就绪**｜{ad.get('note')}")
        L += ["", "ⓘ **仅通知，不构成卖出或买入授权。** 买卖由你本人决定并执行。"]

    for r in need:
        if r in trig:
            continue
        mods = r.get("modules") or {}
        miss = [f"{k}: {m.get('reason')}" for k, m in mods.items() if m.get("status") == "NEED_DATA"]
        if not miss:
            continue
        L += [f"⚠️ **{r.get('name')}（{r.get('code')}）：参数缺失，相关模块未判定**", ""]
        for m in miss:
            L.append(f"- {m}")
        L += ["", "🔴 缺参数时**不回落默认值**（那是替你设定风控边界），"
                  "所以这些模块本次不给结论。补台账后下次运行即生效。"]

    for r in sus:
        L += [f"⚠️ **{r.get('name')}（{r.get('code')}）：疑似除权除息，结论暂不可用**", ""]
        if n:
            seg = [f"现价 **{r.get('price')}**"]
            if r.get("cost") is not None:
                seg.append(f"加权成本 **{r.get('cost')}**")
            if r.get("atr20") is not None:
                seg.append(f"20日ATR **{r.get('atr20')}**")
            if r.get("threshold") is not None:
                seg.append(f"阈值 **{r.get('threshold')}**")
            L.append("- " + "｜".join(seg))
            if r.get("cost_source"):
                L.append(f"- 成本来源：{r.get('cost_source')}")
        L += [f"- {r.get('ex_dividend_note') or '需核实公司是否分红/送转'}",
              "- 🔴 必须先核实成本与价格口径是否需调整，**不得直接采信脚本结论**。"]

    for r in failed:
        # 🔴 必须把 detail 打出来 —— 只说「未能核实」等于让用户自己猜，
        # 而成本读不到 / 行情取数失败是完全不同的处置动作。
        L += [f"❌ **{r.get('name')}（{r.get('code')}）：本次未能核实**",
              "- 不静默略过，特此说明。"]
        detail = r.get("detail") or r.get("reason")
        if detail:
            L.append(f"- 原因：{detail}")
        # 成本来源只在与「原因」不同时补，避免同一句话印两遍
        src = r.get("cost_source")
        if n and src and src not in (detail or ""):
            L.append(f"- 成本来源：{src}")

    for group in result.get("batch_alerts", []):
        for alert in group.get("alerts", []):
            if alert.get("status") in ("SILENT", "DONE"):
                continue
            L += [f"**{group.get('name')}（{group.get('code')}）｜第{alert.get('batch') or '?'}批买入监控：{alert['status']}**"]
            if alert.get("rule"):
                L.append(f"- 规则：`{alert['rule']}`")
            if alert.get("kline_source"):
                L.append(f"- K线来源：{alert['kline_source']}｜判定时点：{alert.get('checked_at') or '—'}｜日K：{alert.get('bar_date') or '—'}")
            metrics = [f"{key}={alert[key]}" for key in ("dif", "dea", "volume_ratio", "price", "ma60", "ma60_prev", "gain_pct", "baseline") if key in alert]
            if metrics:
                L.append("- 核验值：" + "；".join(metrics))
            if alert.get("note") or alert.get("reason"):
                L.append("- " + str(alert.get("note") or alert.get("reason")))
            L.append("- 仅提醒；是否继续、调整或执行由用户决定，不自动买入。")
            L.append("")

    if result.get("anomalies") and not (trig or sus or failed):
        L += ["⚠️ 检测到数据异常，需复核：", ""]
        for a in result["anomalies"]:
            L.append(f"- {a}")
    return "\n".join(L)


MAILER = _H + "/skills/email/hermes-stock-mail/scripts/mailer.py"



def _num(v):
    """腾讯 K 线返回的数字常是字符串，统一转 float；不可转则返回 None。"""
    try:
        return float(v)
    except (TypeError, ValueError):
        return None




def _send_mail(result, rendered, mail_to=None):
    """⭐ 本工作流确认：飞书＋邮件双通道，邮件内容与飞书一致（含数值）。
    发送失败只记录、不抛出 —— 邮件失败绝不能阻塞飞书投递。
    """
    import subprocess
    if not _H or not os.path.exists(MAILER):
        # 没装 Hermes（未设 HERMES_HOME）→ 没有 mailer，邮件通道跳过，不影响飞书。
        print(f"[profit_guard] 未配置邮件发送器（HERMES_HOME={_H or '未设置'}）"
              f"，本次跳过邮件", file=sys.stderr)
        return
    body = rendered + f"\n\n---\n判定口径：{result.get('threshold_formula','')}\n"
    f = os.path.join(tempfile.gettempdir(),
                     f"guard_mail_{result.get('slot','').replace(':','')}_{datetime.now(TZ):%Y%m%d_%H%M%S}.md")
    try:
        with open(f, "w", encoding="utf-8") as fh:
            fh.write(body)
        act = result.get("action")
        head = {"REVIEW": "盈利保护启动条件已满足",
                "FAULT_ONCE": "监控异常"}.get(act, "盈利保护监控")
        names = "、".join(r.get("name", "") for r in result.get("results", [])
                          if r.get("triggered") or r.get("ex_dividend_suspect")
                          or r.get("status") == "data_failed")
        if not names:
            names = "、".join(r.get("name", "") for r in result.get("results", [])) or "持仓"
        subprocess.run(["python3", MAILER, "--subject",
                        f"持仓盈利保护 {result.get('slot')} · {result.get('run_at','')[:10]} · {names} · {head}",
                        "--body-file", f],
                       capture_output=True, text=True, timeout=120)
        return True
    except Exception as e:
        print(f"[profit_guard] mail failed: {e}", file=sys.stderr)
        return False


def _emit(result, json_out=None):
    now = datetime.now(TZ)
    default = os.path.join(tempfile.gettempdir(),
                           f"guard_{result['slot'].replace(':','')}_{now.strftime('%Y%m%d')}.json")
    out = json_out or default
    try:
        with open(out, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        result["json_path"] = out
    except Exception:
        pass

    if result.get("_no_agent"):
        # 🔴 只投递成稿；SILENT → 空 stdout → Hermes 判定为静默成功
        # ⭐ 必须 strip 后再判空，否则单独一个换行也会让 Hermes 认为有输出而误投递
        rendered = _render_for_delivery(result).strip()
        if rendered:
            print(rendered)
        if result.get("_mail") and rendered:
            # 🔴 静默（rendered 为空）时不得发邮件 —— 否则邮件正文只剩追加的口径行，
            #    用户收到一封没有数值的"提醒"。飞书静默则邮件也静默，两者一致。
            _send_mail(result, rendered)
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"\n[profit_guard] json -> {out}", file=sys.stderr)
    print(f"[profit_guard] action={result['action']} reason={result['reason']}", file=sys.stderr)


if __name__ == "__main__":
    main()