#!/usr/bin/env python3
"""
棱镜 金融数据分析引擎 v2.0
基于三层架构(执行层→分析层→决策层)设计
融合本轮学习的Multi-Agent量化知识
"""

import json
import os
import sys
from datetime import datetime

# 固定导入路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)

from fetcher import fetch_realtime, fetch_batch, fetch_kline, calc_indicators, eastmoney_kline, eastmoney_sector_flow

REPORT_DIR = os.path.join(BASE_DIR, "reports")
os.makedirs(REPORT_DIR, exist_ok=True)

# ============ Layer 1: 执行层（数据采集） ============

MARKET_WATCHLIST = {
    "大盘指数": ["000001","000002","000016","000300","000688","399001","399006"],
    "金融": ["600030","601318","601166","601398","601288","600036"],
    "科技": ["002415","002475","002594","300750","300059","688981","688256"],
    "消费": ["600519","600887","600809","000858","000568","002714"],
    "能源": ["601857","600028","600585","601088","601899"],
}

FOCUS_STOCKS = ["300042", "002897", "002285", "300285"]  # 朗科/意华/国瓷等常盯标的

def collect_sector_flow(top_n=15):
    """采集板块资金流向数据"""
    sectors = eastmoney_sector_flow(top_n)
    if isinstance(sectors, list):
        return {
            "sectors": sectors,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
    return {"error": "sector_flow_failed"}


def collect_market_data():
    """采集全市场数据"""
    all_codes = []
    for sector, codes in MARKET_WATCHLIST.items():
        all_codes.extend(codes)
    all_codes = list(set(all_codes))
    
    results = fetch_batch(all_codes)
    
    # 按板块分类
    sector_data = {}
    for sector, codes in MARKET_WATCHLIST.items():
        sector_data[sector] = [r for r in results if r.get("code") in codes and "error" not in r]
    
    # 关注标的
    focus_data = fetch_batch(FOCUS_STOCKS)
    
    return {
        "sectors": sector_data,
        "focus": focus_data,
        "raw": results,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

def collect_intraday_snapshot():
    """盘中快照：只取关注标的+大盘"""
    codes = FOCUS_STOCKS + ["000001","399001","399006","000688"]
    return fetch_batch(codes)

# ============ Layer 2: 分析层（因子计算） ============

def analyze_stock_factors(code):
    """对单只股票做因子分析（含多日趋势）"""
    data = fetch_realtime(code)
    if not data or "error" in data:
        return {"code": code, "error": "fetch_failed"}
    
    kline = fetch_kline(code, "daily", 120)
    indicators = calc_indicators(kline)
    
    factors = {}
    factors["price"] = data.get("price", 0)
    factors["change_pct"] = data.get("change_pct", 0)
    factors["amount_yi"] = data.get("amount_yi", 0)
    
    # 东方财富基础数据（换手率、量比、市值等）
    em_data = eastmoney_kline(code)
    if em_data and 'error' not in em_data:
        factors["turnover_pct"] = em_data.get("turnover_pct", 0)
        factors["volume_ratio_em"] = em_data.get("volume_ratio_em", 0)
        factors["total_market_cap_yi"] = em_data.get("total_market_cap_yi", 0)
        factors["pe"] = em_data.get("pe", 0)
    
    # 技术因子（含所有新增因子）
    if indicators:
        # 基础
        factors["ma20"] = indicators.get("ma20", 0)
        factors["ma60"] = indicators.get("ma60", 0)
        factors["ma5"] = indicators.get("ma5", 0)
        factors["ma10"] = indicators.get("ma10", 0)
        factors["deviation_ma20"] = indicators.get("deviation_ma20_pct", 0)
        factors["above_ma20"] = indicators.get("above_ma20", False)
        factors["above_ma60"] = indicators.get("above_ma60", False)
        factors["volume_ratio"] = indicators.get("volume_ratio", 0)
        factors["avg_volume_20d"] = indicators.get("avg_volume_20d", 0)
        factors["vol_trend"] = indicators.get("vol_trend", 0)
        # RSI
        factors["rsi6"] = indicators.get("rsi6", 50)
        factors["rsi14"] = indicators.get("rsi14", 50)
        # MACD
        factors["macd"] = indicators.get("macd", 0)
        factors["macd_signal"] = indicators.get("macd_signal", 0)
        factors["macd_histogram"] = indicators.get("macd_histogram", 0)
        factors["macd_bullish"] = indicators.get("macd_bullish", False)
        # KDJ
        factors["kdj_k"] = indicators.get("kdj_k", 50)
        factors["kdj_d"] = indicators.get("kdj_d", 50)
        factors["kdj_j"] = indicators.get("kdj_j", 50)
        factors["kdj_bullish"] = indicators.get("kdj_bullish", False)
        # 布林带
        factors["bb_upper"] = indicators.get("bb_upper", 0)
        factors["bb_lower"] = indicators.get("bb_lower", 0)
        factors["bb_position"] = indicators.get("bb_position", 0.5)
        # ICU
        factors["icu_score"] = indicators.get("icu_score", 0)
        factors["icu_bullish"] = indicators.get("icu_bullish", False)
        # 鳄鱼线
        factors["alligator_sleeping"] = indicators.get("alligator_sleeping", False)
        factors["alligator_eating"] = indicators.get("alligator_eating", False)
        # ADX
        factors["adx_strength"] = indicators.get("adx_strength", 50)
        factors["adx_signal"] = indicators.get("adx_signal", "震荡")
        # OBV
        factors["obv_trend"] = indicators.get("obv_trend", "平衡")
    
    # ========== 新增：多日趋势分析 ==========
    multi_day = analyze_multi_day_trend(code, kline)
    factors.update(multi_day)
    
    # 综合判断（使用多日信号）
    bullish_signals = []
    bearish_signals = []
    
    if factors.get("above_ma20"):
        bullish_signals.append("位于20日均线上方")
    if factors.get("above_ma60"):
        bullish_signals.append("位于60日均线上方")
    if factors.get("volume_ratio", 0) > 1.5:
        bullish_signals.append("放量(日均量1.5倍以上)")
    if factors.get("change_pct", 0) > 3:
        bullish_signals.append("当日涨幅超3%")
    # 多日趋势信号
    if factors.get("trend_3d", "") == "上涨":
        bullish_signals.append("近3日累计上涨")
    if factors.get("bullish_divergence", False):
        bullish_signals.append("缩量回调(假跌破形态)")
    if factors.get("bearish_divergence", False):
        bearish_signals.append("放量滞涨")
    
    if not factors.get("above_ma20"):
        bearish_signals.append("跌破20日均线")
    if factors.get("deviation_ma20", 0) > 20:
        bearish_signals.append("偏离20日线超20%(追高风险)")
    if factors.get("volume_ratio", 0) < 0.5:
        bearish_signals.append("缩量至日均量一半以下")
    if factors.get("change_pct", 0) < -3 and not factors.get("bullish_divergence", False):
        bearish_signals.append("当日跌幅超3%")
    
    factors["bullish_signals"] = bullish_signals
    factors["bearish_signals"] = bearish_signals
    factors["bullish_score"] = len(bullish_signals)
    factors["bearish_score"] = len(bearish_signals)
    
    return factors


def analyze_multi_day_trend(code, kline=None):
    """多日趋势分析
    解决"单日涨跌幅一刀切"的问题——
    一只股票今天跌5%但缩量不破MA20，可能是假跌破而非真弱势。
    """
    if not kline:
        kline = fetch_kline(code, "daily", 20)
    if not kline or len(kline) < 5:
        return {}
    
    result = {}
    
    # 取最近5个交易日
    recent = [float(k.get("close", 0)) for k in kline[-5:]]
    volumes = [float(k.get("volume", 0)) for k in kline[-5:]]
    
    if len(recent) < 5:
        return {}
    
    # 近3日累计涨跌幅
    d1 = recent[-1]
    d3 = recent[-3] if len(recent) >= 3 else recent[0]
    d5 = recent[0]
    
    chg_1d = round((recent[-1] - recent[-2]) / recent[-2] * 100, 2) if recent[-2] != 0 else 0
    chg_3d = round((d1 - d3) / d3 * 100, 2) if d3 != 0 else 0
    chg_5d = round((d1 - d5) / d5 * 100, 2) if d5 != 0 else 0
    
    result["change_1d"] = chg_1d
    result["change_3d"] = chg_3d
    result["change_5d"] = chg_5d
    
    # 趋势方向
    if chg_3d > 2:
        result["trend_3d"] = "上涨"
    elif chg_3d < -2:
        result["trend_3d"] = "下跌"
    else:
        result["trend_3d"] = "震荡"
    
    if chg_5d > 3:
        result["trend_5d"] = "上涨"
    elif chg_5d < -3:
        result["trend_5d"] = "下跌"
    else:
        result["trend_5d"] = "震荡"
    
    # ========== 关键：假跌破检测 ==========
    # 形态：前一天大涨 > 3% → 今天跌但缩量(量比<1) → 仍在MA20上方
    if len(kline) >= 3:
        prev_chg = round((float(kline[-2].get("close", 0)) - float(kline[-3].get("close", 0))) / float(kline[-3].get("close", 0)) * 100, 2) if float(kline[-3].get("close", 0)) != 0 else 0
        today_chg = chg_1d
        today_vol = volumes[-1] if len(volumes) >= 1 else 0
        prev_vol = volumes[-2] if len(volumes) >= 2 else 0
        vol_ratio_today = today_vol / prev_vol if prev_vol > 0 else 1
        
        if prev_chg > 3 and today_chg < 0 and vol_ratio_today < 1:
            result["bullish_divergence"] = True  # 缩量回调=假跌破
        
        # 放量滞涨检测
        if prev_chg < 0 and today_chg > 3 and vol_ratio_today < 1:
            pass  # 温和反弹，不判定为异常
        if prev_chg > 0 and today_chg > 0 and vol_ratio_today > 2:
            result["bearish_divergence"] = True  # 连续涨但量暴增=可能见顶
    
    # 回调深度：从近期最高点回撤了多少
    recent_high = max([float(k.get("high", 0)) for k in kline[-10:]])
    current = float(kline[-1].get("close", 0))
    pullback = round((recent_high - current) / recent_high * 100, 2) if recent_high > 0 else 0
    result["pullback_from_high"] = pullback
    
    # 如果回调 < 8% 且近5日整体上涨，算健康回调
    if pullback < 8 and chg_5d > 0:
        result["pullback_healthy"] = True
    else:
        result["pullback_healthy"] = False
    
    return result

# ============ Layer 3: 决策层（多空辩论辅助） ============

def debate_summary(code):
    """生成供AI多空辩论用的数据摘要"""
    factors = analyze_stock_factors(code)
    if "error" in factors:
        return {"error": factors["error"]}
    
    summary = {
        "code": code,
        "price": factors["price"],
        "change": factors["change_pct"],
        "ma20": factors.get("ma20"),
        "ma60": factors.get("ma60"),
        "偏离均线": f"{factors.get('deviation_ma20', 0):.1f}%",
        "放量缩量": "放量" if factors.get("volume_ratio", 0) > 1.2 else ("缩量" if factors.get("volume_ratio", 0) < 0.8 else "正常"),
        "多头信号": factors.get("bullish_signals", []),
        "空头信号": factors.get("bearish_signals", []),
        # 新增多日趋势字段
        "近3日涨跌": f"{factors.get('change_3d', 0):.1f}%",
        "近5日涨跌": f"{factors.get('change_5d', 0):.1f}%",
        "趋势": factors.get("trend_3d", "未知"),
        "回撤幅度": f"{factors.get('pullback_from_high', 0):.1f}%",
        "假跌破信号": factors.get("bullish_divergence", False),
    }
    return summary

# ============ Layer 4: 市场状态分类器（FINSABER启示） ============

def detect_market_regime():
    """检测当前市场状态：牛市/熊市/震荡
    基于大盘指数的MA60趋势+波动率判断。
    来源：FINSABER论文——LLM策略在牛市中保守、熊市中激进，必须明确市场状态。
    """
    index_codes = ["000001", "399001", "399006"]
    results = fetch_batch(index_codes)

    regimes = []
    for r in results:
        if "error" in r:
            continue
        kline = fetch_kline(r["code"], "daily", 60)
        if not kline or len(kline) < 60:
            continue
        indicators = calc_indicators(kline)
        close = r.get("price", 0)
        ma60 = indicators.get("ma60", 0)
        if ma60 == 0:
            continue
        above_ma60 = close > ma60
        deviation = (close - ma60) / ma60 * 100
        closes = [float(k.get("close", 0)) for k in kline[-20:]]
        avg_price = sum(closes) / len(closes) if closes else 1
        atr = max(closes) - min(closes)
        volatility = atr / avg_price * 100 if avg_price > 0 else 0

        if above_ma60 and deviation < 15 and volatility < 20:
            regimes.append("牛市")
        elif above_ma60 and deviation >= 15:
            regimes.append("强势牛市")
        elif above_ma60 and volatility >= 20:
            regimes.append("高波动牛市")
        elif not above_ma60 and deviation > -10:
            regimes.append("震荡市")
        elif not above_ma60 and deviation <= -10:
            regimes.append("熊市")
        else:
            regimes.append("震荡")

    bull_count = sum(1 for r in regimes if "牛市" in r)
    bear_count = sum(1 for r in regimes if "熊市" in r)

    if bull_count >= 2:
        regime = "牛市"
    elif bear_count >= 2:
        regime = "熊市"
    else:
        regime = "震荡市"

    return {"regime": regime, "details": regimes, "volatility_avg": 0}


# ============ Layer 5: 推荐回溯记录（StockBench启示） ============

TRADE_LOG_DIR = os.path.join(BASE_DIR, "trade_logs")
os.makedirs(TRADE_LOG_DIR, exist_ok=True)


# ============ 验证记录（Harness-1启示） ============

AUDIT_DIR = os.path.join(BASE_DIR, "audit_trails")
os.makedirs(AUDIT_DIR, exist_ok=True)


def record_audit_step(phase, code, content):
    """记录分析流程中每一步的中间状态
    phase: 阶段名称（regime/初筛/辩论/决策）
    code: 股票代码或市场代码
    content: 该步的关键信息（结构化）
    之后做回溯时可追溯到每一步的判断依据
    """
    from datetime import datetime
    now = datetime.now()
    date_str = now.strftime("%Y%m%d")
    
    # 以日为单位累积，一天一个文件
    fpath = os.path.join(AUDIT_DIR, f"trail_{date_str}.jsonl")
    
    record = {
        "timestamp": now.strftime("%H:%M:%S"),
        "date": date_str,
        "phase": phase,
        "code": code,
        "content": str(content)[:500],
        "model": "bailian/qwen-plus"  # 记录当时用的模型
    }
    
    with open(fpath, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
    
    return True


def review_audit_trail(date_str=None):
    """审查某一天的验证记录，分析哪一步判断有问题"""
    if not date_str:
        from datetime import datetime
        date_str = datetime.now().strftime("%Y%m%d")
    
    fpath = os.path.join(AUDIT_DIR, f"trail_{date_str}.jsonl")
    if not os.path.exists(fpath):
        return {"date": date_str, "steps": 0, "phases": [], "error": "no_audit"}
    
    entries = []
    with open(fpath, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                entries.append(json.loads(line))
    
    phases = set(e["phase"] for e in entries)
    codes = set(e.get("code","?") for e in entries)
    
    return {
        "date": date_str,
        "total_steps": len(entries),
        "phases": list(phases),
        "codes": list(codes)[:10],
        "entries": entries[-20:]  # 只返回最近20条
    }


def record_recommendation(code, direction, entry_price, stop_loss, take_profit, rationale):
    """记录一次推荐，供N天后回溯评估"""
    from datetime import timedelta
    now = datetime.now()
    record = {
        "code": code, "direction": direction, "entry_price": entry_price,
        "stop_loss": stop_loss, "take_profit": take_profit,
        "rationale": rationale[:200],
        "recommend_date": now.strftime("%Y-%m-%d"),
        "review_date": (now + timedelta(days=14)).strftime("%Y-%m-%d"),
        "status": "pending_review", "actual_return": None, "result": None
    }
    fpath = os.path.join(TRADE_LOG_DIR, f'recommend_{now.strftime("%Y%m%d_%H%M%S")}.json')
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    print(f"[记录] 推荐已保存: {fpath}")
    return fpath


def review_recommendations():
    """检查待评估的推荐，看后续走势"""
    from datetime import timedelta
    today = datetime.now().strftime("%Y-%m-%d")
    reviewed = []
    for fname in os.listdir(TRADE_LOG_DIR):
        if not fname.startswith("recommend_"):
            continue
        fpath = os.path.join(TRADE_LOG_DIR, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            record = json.load(f)
        if record.get("status") != "pending_review":
            continue
        review_date = record.get("review_date", "")
        if not review_date or review_date > today:
            continue
        code = record["code"]
        current = fetch_realtime(code)
        if not current or "error" in current:
            continue
        entry = record["entry_price"]
        now_price = current.get("price", entry)
        actual_return = round((now_price - entry) / entry * 100, 2)
        record["actual_return"] = actual_return
        record["status"] = "reviewed"
        if actual_return >= 10:
            record["result"] = "止盈"
        elif actual_return <= -5:
            record["result"] = "止损"
        elif actual_return > 0:
            record["result"] = "微盈"
        else:
            record["result"] = "亏损"
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(record, f, ensure_ascii=False, indent=2)
        reviewed.append(record)
    return reviewed


# ============ CLI入口 ============

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 analyzer.py [scan | report | debate <code>]")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "scan":
        data = collect_market_data()
        for sector, stocks in data["sectors"].items():
            print(f"\n📍 {sector}")
            for s in stocks[:5]:
                print(f"   {s['name']}({s['code']}): {s['price']} ({s['change_pct']}%)")
    
    elif cmd == "report":
        data = collect_market_data()
        lines = [f"# 📊 市场简报 | {data['timestamp']}", ""]
        for sector, stocks in data["sectors"].items():
            lines.append(f"## {sector}")
            lines.append("|名称|价格|涨跌幅|成交额(亿)|")
            lines.append("|---|---|---|---|")
            for s in stocks[:5]:
                lines.append(f"|{s['name']}|{s['price']}|{s['change_pct']}%|{s.get('amount_yi','N/A')}|")
            lines.append("")
        content = "\n".join(lines)
        filename = f"brief_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
        filepath = os.path.join(REPORT_DIR, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ 简报已保存: {filepath}")
    
    elif cmd == "regime":
        regime = detect_market_regime()
        print(f"📊 市场状态: {regime['regime']}")
        print(f"详情: {regime['details']}")
        record_audit_step("regime", "market", regime)
    
    elif cmd == "trail" and len(sys.argv) > 2:
        result = review_audit_trail(sys.argv[2])
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif cmd == "review":
        results = review_recommendations()
        if results:
            print(f"📈 回溯评估结果 ({len(results)}条):")
            for r in results:
                print(f"  {r['code']}: 入场{r['entry_price']}→当前 {r.get('actual_return','?')}% → {r['result']}")
        else:
            print("暂无待评估的推荐记录")
    
    elif cmd == "record" and len(sys.argv) > 5:
        record_recommendation(sys.argv[2], sys.argv[3], float(sys.argv[4]), float(sys.argv[5]), float(sys.argv[6]), " ".join(sys.argv[7:]) if len(sys.argv) > 7 else "")
    
    elif cmd == "debate" and len(sys.argv) > 2:
        summary = debate_summary(sys.argv[2])
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    
    else:
        print(f"未知命令: {cmd}")
