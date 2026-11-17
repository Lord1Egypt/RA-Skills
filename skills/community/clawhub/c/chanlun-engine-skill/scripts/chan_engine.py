#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
chan_engine.py — 单股缠论结构计算，输出 chanlun_structure_v1 JSON 契约
引擎: Vespa314/chan.py 已打包于 ../engine/chanpy (commit 429d6ed, MIT) | 口径: structure_proxy(日-周两级)
用法:
  python chan_engine.py --csv path.csv --symbol 600519.SH            # CSV: date,open,high,low,close,volume[,amount]
  python chan_engine.py --duckdb data/market.duckdb --symbol 600519.SH [--start 2023-01-01]
  python chan_engine.py --stdin-json --symbol X                      # stdin 传 [{date,open,high,low,close,volume},...]
引擎路径: 默认用打包的 ../engine/chanpy, 可用环境变量 CHANPY_PATH 覆盖
输出: stdout 单个 JSON(chanlun_structure_v1), 含结构/summary成品句/verdict四态操作判定(确定性规则映射)。
"""
import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timedelta

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")  # Windows 控制台默认GBK, 钉死UTF-8

# ---------- vendor 挂载 ----------
_HERE = os.path.dirname(os.path.abspath(__file__))
_CANDIDATES = ([os.environ["CHANPY_PATH"]] if os.environ.get("CHANPY_PATH") else []) + [
    os.path.join(_HERE, "..", "engine", "chanpy"),   # 随技能打包的内置引擎(默认)
    os.path.join(_HERE, "..", "vendor", "chanpy"),   # 旧版外置 vendor 兼容
]
CHANPY = next((os.path.abspath(p) for p in _CANDIDATES if os.path.isdir(p)), None)
if not CHANPY:
    print(json.dumps({"error": "缠论引擎目录缺失(engine/chanpy), 技能包不完整, 请重新安装本技能"}, ensure_ascii=False))
    sys.exit(2)
sys.path.insert(0, CHANPY)

from Chan import CChan                              # noqa: E402
from ChanConfig import CChanConfig                  # noqa: E402
from Common.CEnum import AUTYPE, DATA_SRC, KL_TYPE  # noqa: E402
from Common.CTime import CTime                      # noqa: E402
from Common.CEnum import DATA_FIELD                 # noqa: E402
from KLine.KLine_Unit import CKLine_Unit            # noqa: E402
from DataAPI.CommonStockAPI import CCommonStockApi  # noqa: E402

ENGINE_TAG = "chan.py@429d6ed(bundled)"
CONTRACT = "chanlun_structure_v1"

# ---------- 钉死的引擎配置(README 默认值不可信, 全部显式) ----------
CHAN_CONFIG = {
    "bi_strict": True,            # 严格笔(老笔)
    "bi_fx_check": "strict",
    "seg_algo": "chan",           # 特征序列线段(正统)
    "zs_algo": "normal",          # 段内中枢
    "zs_combine": True,
    "divergence_rate": 0.9,       # !! 开源版默认 inf=不判背驰, 必须显式
    "min_zs_cnt": 1,
    "max_bs2_rate": 0.618,
    "macd_algo": "peak",          # 24课: MACD 仅"辅助判断"
    "bs_type": "1,1p,2,2s,3a,3b",
    "print_warning": False,
    "kl_data_check": False,       # 周线由日K合成, 关闭父子逐根强校验(自行保证对齐)
    "gap_as_kl": False,           # README 写 True, 代码实际 False — 显式钉死
}
CONFIG_HASH = hashlib.md5(json.dumps(CHAN_CONFIG, sort_keys=True).encode()).hexdigest()[:8]

_ROWS: list = []  # 进程内传递给自定义数据源


def _weekly_from_daily(rows):
    """日K合成周K(ISO周), 每周取 first open/max high/min low/last close/sum vol"""
    out, cur, key = [], None, None
    for r in rows:
        d = datetime.fromisoformat(r["date"])
        k = d.isocalendar()[:2]
        if k != key:
            if cur:
                out.append(cur)
            cur = dict(r)
            key = k
        else:
            cur["high"] = max(cur["high"], r["high"])
            cur["low"] = min(cur["low"], r["low"])
            cur["close"] = r["close"]
            cur["volume"] = cur.get("volume", 0) + r.get("volume", 0)
            cur["date_end"] = r["date"]
    if cur:
        out.append(cur)
    return out


class CMemDay(CCommonStockApi):
    """内存行 → chan.py 数据源。K_DAY 用原始行, K_WEEK 用合成周K(时间取该周最后交易日)"""
    def __init__(self, code, k_type=KL_TYPE.K_DAY, begin_date=None, end_date=None, autype=None):
        super().__init__(code, k_type, begin_date, end_date, autype)

    def get_kl_data(self):
        rows = _ROWS if self.k_type == KL_TYPE.K_DAY else _weekly_from_daily(_ROWS)
        for r in rows:
            d = r.get("date_end", r["date"])
            fields = {
                DATA_FIELD.FIELD_TIME: CTime(int(d[:4]), int(d[5:7]), int(d[8:10]), 0, 0),
                DATA_FIELD.FIELD_OPEN: float(r["open"]),
                DATA_FIELD.FIELD_HIGH: float(r["high"]),
                DATA_FIELD.FIELD_LOW: float(r["low"]),
                DATA_FIELD.FIELD_CLOSE: float(r["close"]),
            }
            if r.get("volume") is not None:
                fields[DATA_FIELD.FIELD_VOLUME] = float(r["volume"])
            if r.get("amount") is not None:
                fields[DATA_FIELD.FIELD_TURNOVER] = float(r["amount"])
            yield CKLine_Unit(fields)

    def SetBasciInfo(self):
        pass

    @classmethod
    def do_init(cls):
        pass

    @classmethod
    def do_close(cls):
        pass


def _t(ct) -> str:
    return f"{ct.year:04d}-{ct.month:02d}-{ct.day:02d}"


def _ma(closes, n):
    if len(closes) < n:
        return None
    return round(sum(closes[-n:]) / n, 3)


def extract_level(kl_list, last_close, tail_bi=8, tail_seg=4, tail_zs=3, tail_bsp=6):
    bis = [{
        "i": b.idx, "dir": str(b.dir).split(".")[-1], "sure": bool(b.is_sure),
        "b": _t(b.get_begin_klu().time), "e": _t(b.get_end_klu().time),
        "bv": round(b.get_begin_val(), 3), "ev": round(b.get_end_val(), 3),
    } for b in list(kl_list.bi_list)[-tail_bi:]]
    segs = [{
        "i": s.idx, "dir": str(s.dir).split(".")[-1], "sure": bool(s.is_sure),
        "b": _t(s.start_bi.get_begin_klu().time), "e": _t(s.end_bi.get_end_klu().time),
        "zs_n": len(s.zs_lst),
    } for s in list(kl_list.seg_list)[-tail_seg:]]
    zss = [{
        "b": _t(z.begin.time), "e": _t(z.end.time), "sure": bool(z.is_sure),
        "zg": round(z.high, 3), "zd": round(z.low, 3),
        "gg": round(z.peak_high, 3), "dd": round(z.peak_low, 3), "bi_n": len(z.bi_lst),
    } for z in list(kl_list.zs_list.zs_lst)[-tail_zs:]]
    bsps = [{
        "d": _t(p.klu.time), "bs": "B" if p.is_buy else "S", "type": p.type2str(),
        "px": round(p.klu.close, 3), "sure": bool(p.bi.is_sure),
    } for p in kl_list.bs_point_lst.getSortedBspList()[-tail_bsp:]]

    pos = None
    if zss:
        z = zss[-1]
        pos = ("above_zs" if last_close > z["zg"] else
               "below_zs" if last_close < z["zd"] else "in_zs")
    return {"bi": bis, "seg": segs, "zs": zss, "bsp": bsps, "pos_vs_last_zs": pos}


def invalidation_for(bsp, day_zss, low_by_date=None):
    """给最新买卖点写失效价位(脚本给数值, LLM 只引用)"""
    t = bsp["type"]
    if not day_zss:
        return None
    z = day_zss[-1]
    if "3a" in t or "3b" in t:
        return {"rule": "跌回中枢上沿(ZG)之下则三买失效", "px": z["zg"]}
    if "1" in t and bsp["bs"] == "B":
        px = (low_by_date or {}).get(bsp["d"])
        return {"rule": "跌破一买当日K线低点则背驰段延伸,候选失效",
                "px": round(px, 3) if px is not None else None}
    if "2" in t and bsp["bs"] == "B":
        return {"rule": "跌破前低(dd)则二买失效", "px": z["dd"]}
    return None


def run(symbol, rows, tail_days=2):
    global _ROWS
    _ROWS = rows
    import DataAPI  # 动态注册内存源
    mod = sys.modules.setdefault("DataAPI.MEM_API", type(sys)("DataAPI.MEM_API"))
    mod.CMemDay = CMemDay
    setattr(DataAPI, "MEM_API", mod)

    config = CChanConfig(dict(CHAN_CONFIG))
    chan = CChan(code=symbol, begin_time=None, end_time=None,
                 data_src="custom:MEM_API.CMemDay",
                 lv_list=[KL_TYPE.K_WEEK, KL_TYPE.K_DAY],
                 config=config, autype=AUTYPE.NONE)  # 复权在数据侧(v_daily_qfq)完成

    day = chan[KL_TYPE.K_DAY]
    week = chan[KL_TYPE.K_WEEK]
    closes = [r["close"] for r in rows]
    last_close = closes[-1]
    last_date = rows[-1]["date"]

    day_x = extract_level(day, last_close)
    week_x = extract_level(week, last_close, tail_bi=6, tail_seg=3, tail_zs=2, tail_bsp=4)

    # 最近 tail_days 根K内的新鲜买卖点 = 选股信号
    recent_dates = {r["date"] for r in rows[-tail_days:]}
    fresh = [b for b in day_x["bsp"] if b["d"] in recent_dates]
    # 周-日粗糙区间套: 周线最近bsp的笔时间窗内是否有日线bsp
    confluence = []
    for wb in week_x["bsp"][-2:]:
        for db in day_x["bsp"]:
            if abs((datetime.fromisoformat(db["d"]) - datetime.fromisoformat(wb["d"])).days) <= 40 \
                    and wb["bs"] == db["bs"]:
                confluence.append({"week": wb, "day": db})
                break

    mas = {f"ma{n}": _ma(closes, n) for n in (5, 10, 20, 60)}
    ma_state = None
    if mas["ma20"] and mas["ma60"]:
        spread = abs(mas["ma5"] - mas["ma20"]) / last_close if mas["ma5"] else None
        ma_state = {
            "long": bool(mas["ma5"] and mas["ma5"] > mas["ma20"] > mas["ma60"]),
            "entangled": bool(spread is not None and spread < 0.02),  # 均线缠绕近似(11-14课"吻")
        }

    invalidations = [
        {"bsp": b, "invalidation": invalidation_for(
            b, day_x["zs"], {r["date"]: r["low"] for r in rows[-10:]})} for b in fresh
    ]
    verdict = make_verdict(day_x, fresh, last_close, invalidations)
    summary = make_summary(symbol, last_date, last_close, day_x, week_x, fresh,
                           confluence, mas, ma_state)
    summary["verdict"] = verdict_sentence(verdict)

    out = {
        "contract": CONTRACT,
        "meta": {
            "symbol": symbol, "asof": last_date, "bars_day": len(rows),
            "engine": ENGINE_TAG, "config_hash": CONFIG_HASH,
            "adjust": "input_side(qfq expected)", "stance": "structure_proxy",
        },
        "day": day_x,
        "week": week_x,
        "ma": {"values": mas, "state": ma_state},
        "signals": {
            "fresh_bsp": fresh,
            "week_day_confluence": confluence,
            "actionable_date": "次一交易日(信号基于已收盘K线, 防前视)",
        },
        "verdict": verdict,
        "invalidations": invalidations,
        "summary": summary,
        "caveats": [
            "日-周两级近似缠论(structure_proxy): 无分钟K, 无次级别确认, 日线笔为最小结构单元",
            "最新笔/买卖点 sure=false 属'当前帧'语义, 次日新K可能使其消失或位移",
            "背驰=MACD peak 法 rate<0.9, 是24课'辅助判断'的量化近似, 非原文力度定义",
            "本输出仅结构事实, 不构成任何操作指令",
        ],
    }
    return out


_POS_TXT = {"above_zs": "中枢上方", "in_zs": "中枢区间内", "below_zs": "中枢下方"}
_DIR_TXT = {"UP": "向上", "DOWN": "向下"}


def make_verdict(day_x, fresh, last_close, invalidations):
    """四态操作判定(确定性规则, 缠论买卖点即操作点): 买入候选/持有/卖出减仓/等待观察
    持仓者与空仓者分别给答案; 每个判定带止损或触发条件。脚本算判定, LLM 只转述。"""
    zs = day_x["zs"][-1] if day_x["zs"] else None
    bi_dir = day_x["bi"][-1]["dir"] if day_x["bi"] else None
    pos = day_x["pos_vs_last_zs"]
    buys = [b for b in fresh if b["bs"] == "B"]
    sells = [b for b in fresh if b["bs"] == "S"]
    stop = None
    for iv in invalidations:
        if iv.get("invalidation") and iv["invalidation"].get("px") is not None:
            stop = iv["invalidation"]["px"]
            break

    if sells:
        t = ",".join(b["type"] for b in sells)
        return {"action": "卖出/减仓",
                "for_holder": f"出现{t}类卖点, 按缠论规则应减仓或离场",
                "for_watcher": "不介入",
                "stop_px": None,
                "watch": [f"若后续放量收复并站稳中枢上沿 {zs['zg'] if zs else '前高'} 之上, 重新评估"]}
    if buys:
        t = ",".join(b["type"] for b in buys)
        sure = all(b["sure"] for b in buys)
        return {"action": "买入候选",
                "for_holder": "已持有则继续持有, 止损上移至失效价位",
                "for_watcher": f"出现{t}类买点{'(已确认)' if sure else '(未确认, 次日可能消失)'}, "
                               f"可考虑介入, 严格以失效价位为止损",
                "stop_px": stop,
                "watch": ["次日大幅低开(超过3%)则放弃本信号",
                          f"跌破失效价位 {stop if stop is not None else '(见invalidations)'} 即认错离场"]}
    if pos == "above_zs" and zs:
        if bi_dir == "UP":
            return {"action": "持有",
                    "for_holder": f"结构健康(中枢上方且笔向上), 持有, 止损设中枢上沿 {zs['zg']}",
                    "for_watcher": "此位置追高无新买点依据, 等回踩中枢上沿企稳(类三买)再考虑",
                    "stop_px": zs["zg"],
                    "watch": [f"回落跌破 {zs['zg']} 则离场(回中枢=三买逻辑失效)"]}
        return {"action": "持有(警惕)",
                "for_holder": f"中枢上方但最近一笔向下, 持有但收紧止损至 {zs['zg']}",
                "for_watcher": "等待方向明确",
                "stop_px": zs["zg"],
                "watch": [f"收盘跌破 {zs['zg']} 转卖出", "缩量企稳后重新走强则解除警惕"]}
    if pos == "in_zs" and zs:
        return {"action": "等待观察",
                "for_holder": f"中枢内震荡, 持有观察, 底线是中枢下沿 {zs['zd']}",
                "for_watcher": "中枢内不动手, 等方向选择",
                "stop_px": zs["zd"],
                "watch": [f"放量站上中枢上沿 {zs['zg']} 转看多(三买候选)",
                          f"收盘跌破中枢下沿 {zs['zd']} 转看空, 持仓离场"]}
    # below_zs 或无中枢
    if bi_dir == "DOWN":
        return {"action": "等待观察(弱势)",
                "for_holder": "弱势结构, 反弹到中枢下沿附近减仓" if zs else "弱势结构, 反弹减仓",
                "for_watcher": "空仓等待, 不接下落中的刀",
                "stop_px": None,
                "watch": ["等底分型出现且下跌出现背驰(一买候选)再评估",
                          (f"收复中枢下沿 {zs['zd']} 之上才算转强" if zs else "站上前中枢区间才算转强")]}
    return {"action": "等待观察(反抽)",
            "for_holder": f"下跌后的反抽, 能否收复 {zs['zd'] if zs else '前低区间'} 是关键, 反抽无力则减仓",
            "for_watcher": "反抽不追, 等站稳或回落出背驰再说",
            "stop_px": None,
            "watch": [(f"放量收复 {zs['zd']} 并站稳看反转" if zs else "放量收复前中枢看反转"),
                      "反抽缩量衰竭则顺势回避"]}


def verdict_sentence(v):
    parts = [f"操作判定: {v['action']}"]
    parts.append(f"持仓者: {v['for_holder']}")
    parts.append(f"空仓者: {v['for_watcher']}")
    if v.get("stop_px") is not None:
        parts.append(f"关键价位: {v['stop_px']}")
    if v.get("watch"):
        parts.append("观察条件: " + "; ".join(v["watch"]))
    return "。".join(parts) + "。"


def make_summary(symbol, last_date, last_close, day_x, week_x, fresh, confluence, mas, ma_state):
    """确定性拼装成品结论句 — 弱模型可整句照抄, 保底平均水平输出"""
    s = {}
    # 日线一句话
    parts = []
    if day_x["bi"]:
        b = day_x["bi"][-1]
        parts.append(f"最近一笔{_DIR_TXT.get(b['dir'], b['dir'])}"
                     f"({b['b']}起, {'已确认' if b['sure'] else '未确认·当前帧'})")
    if day_x["zs"]:
        z = day_x["zs"][-1]
        parts.append(f"现价{last_close}位于最近中枢[{z['zd']}, {z['zg']}]的"
                     f"{_POS_TXT.get(day_x['pos_vs_last_zs'], '未知位置')}")
    if day_x["bsp"]:
        p = day_x["bsp"][-1]
        parts.append(f"最近{'买' if p['bs'] == 'B' else '卖'}点为{p['d']}的{p['type']}类"
                     f"({'已确认' if p['sure'] else '未确认'})")
    s["day"] = f"{symbol} 日线({last_date}): " + ("; ".join(parts) if parts else "结构要素不足")
    # 周线一句话
    wp = []
    if week_x["seg"]:
        g = week_x["seg"][-1]
        wp.append(f"当前线段{_DIR_TXT.get(g['dir'], g['dir'])}")
    if week_x["zs"]:
        z = week_x["zs"][-1]
        wp.append(f"周线中枢[{z['zd']}, {z['zg']}]")
    if week_x["bi"]:
        b = week_x["bi"][-1]
        wp.append(f"最近周线笔{_DIR_TXT.get(b['dir'], b['dir'])}")
    s["week"] = "周线: " + ("; ".join(wp) if wp else "结构要素不足(历史太短)")
    # 信号一句话
    if fresh:
        kinds = ", ".join(f"{b['d']}出现{b['type']}类{'买' if b['bs'] == 'B' else '卖'}点"
                          f"({'已确认' if b['sure'] else '未确认·次日可能消失'})" for b in fresh)
        s["signal"] = f"新鲜信号: {kinds}。属候选而非确认, 失效价位见 invalidations。"
    else:
        s["signal"] = "最近交易日无新鲜买卖点。"
    if confluence:
        s["signal"] += f" 周-日同向共振{len(confluence)}处(粗糙区间套)。"
    # 均线一句话
    if ma_state:
        m = []
        m.append("均线多头排列(5>20>60)" if ma_state["long"] else "均线非多头排列")
        if ma_state["entangled"]:
            m.append("5-20缠绕(乖离<2%, 变盘观察)")
        s["ma"] = "; ".join(m)
    return s


def load_csv(path):
    import csv as _csv
    rows = []
    with open(path, encoding="utf-8") as f:
        rd = _csv.DictReader(f)
        for r in rd:
            rows.append({"date": r["date"][:10], "open": float(r["open"]), "high": float(r["high"]),
                         "low": float(r["low"]), "close": float(r["close"]),
                         "volume": float(r.get("volume") or 0) or None,
                         "amount": float(r.get("amount") or 0) or None})
    return rows


def load_duckdb(db, symbol, start=None):
    import duckdb
    con = duckdb.connect(db, read_only=True)
    q = "SELECT date, open, high, low, close, volume, turnover FROM v_daily_qfq WHERE thscode = ?"
    if start:
        q += " AND date >= ?"
    q += " ORDER BY date"
    args = [symbol] + ([start] if start else [])
    rows = [{"date": str(r[0])[:10], "open": float(r[1]), "high": float(r[2]), "low": float(r[3]),
             "close": float(r[4]), "volume": float(r[5] or 0) or None, "amount": float(r[6] or 0) or None}
            for r in con.execute(q, args).fetchall()]
    con.close()
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--symbol", required=True)
    ap.add_argument("--csv")
    ap.add_argument("--duckdb")
    ap.add_argument("--stdin-json", action="store_true")
    ap.add_argument("--start")
    ap.add_argument("--tail-days", type=int, default=2)
    ap.add_argument("--out", help="把JSON写到文件(缺省打到stdout)")
    a = ap.parse_args()
    if a.csv:
        rows = load_csv(a.csv)
    elif a.duckdb:
        rows = load_duckdb(a.duckdb, a.symbol, a.start)
    elif a.stdin_json:
        rows = json.load(sys.stdin)
    else:
        ap.error("需要 --csv / --duckdb / --stdin-json 之一")
    if len(rows) < 120:
        print(json.dumps({"error": f"K线不足120根({len(rows)}), 结构不可靠, 拒绝计算"}, ensure_ascii=False))
        sys.exit(1)
    result = json.dumps(run(a.symbol, rows, a.tail_days), ensure_ascii=False)
    if a.out:
        open(a.out, "w", encoding="utf-8").write(result)
        print(json.dumps({"written": a.out}, ensure_ascii=False))
    else:
        print(result)


if __name__ == "__main__":
    main()
