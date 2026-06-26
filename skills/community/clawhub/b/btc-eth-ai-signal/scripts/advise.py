"""AI Trading Advisor - BTC/ETH technical analysis with actionable recommendations"""
from check import get_price, get_kline
from datetime import datetime
import json, urllib.request, math

def ema(data, period):
    k = 2 / (period + 1)
    result = [data[0]]
    for v in data[1:]:
        result.append(v * k + result[-1] * (1 - k))
    return result

def calc_rsi(closes, period=14):
    if len(closes) < period + 1:
        return 50
    gains, losses = 0, 0
    for i in range(-period, 0):
        diff = closes[i] - closes[i-1]
        if diff > 0: gains += diff
        else: losses -= diff
    if losses == 0: return 100
    rs = gains / period / (losses / period)
    return round(100 - 100 / (1 + rs), 1)

def calc_macd(closes):
    ema12 = ema(closes, 12)
    ema26 = ema(closes, 26)
    macd_line = [ema12[i] - ema26[i] for i in range(len(ema26))]
    signal = ema(macd_line, 9)
    histogram = round(macd_line[-1] - signal[-1], 2)
    return histogram, round(macd_line[-1], 2), round(signal[-1], 2)

def calc_bollinger(closes, period=20):
    if len(closes) < period:
        return None, None, None
    recent = closes[-period:]
    ma = sum(recent) / period
    variance = sum((x - ma) ** 2 for x in recent) / period
    std = math.sqrt(variance)
    return round(ma + 2 * std, 2), round(ma, 2), round(ma - 2 * std, 2)

def calc_atr(klines, period=14):
    if len(klines) < period + 1:
        return None
    trs = []
    for i in range(-period, 0):
        h = klines[i][2]
        l = klines[i][3]
        pc = klines[i-1][4]
        tr = max(h - l, abs(h - pc), abs(l - pc))
        trs.append(tr)
    return round(sum(trs) / period, 2)

def get_network_sentiment():
    """Fetch market sentiment data"""
    try:
        import urllib.request
        r = urllib.request.urlopen("https://api.gateio.ws/api/v4/futures/usdt/tickers?contract=BTC_USDT", timeout=5)
        d = json.loads(r.read())
        if isinstance(d, list) and len(d) > 0:
            return {"funding": float(d[0].get("funding_rate", 0)) * 100}
    except:
        pass
    return {}

def analyze_coin(symbol, klines_day, klines_4h, klines_1h):
    """Full technical analysis for one coin"""
    result = {}
    
    # Price data
    price = get_price(symbol)
    if not price:
        return None
    result["price_data"] = price
    
    # Daily analysis
    if klines_day and len(klines_day) > 15:
        closes = [k[2] for k in klines_day]
        highs = [k[2] for k in klines_day]
        lows = [k[3] for k in klines_day]
        
        result["rsi"] = calc_rsi(closes, 14)
        result["macd_hist"], result["macd_line"], result["macd_signal"] = calc_macd(closes)
        result["boll_upper"], result["boll_mid"], result["boll_lower"] = calc_bollinger(closes)
        result["atr"] = calc_atr(klines_day)
        
        # Moving averages
        result["ma7"] = sum(closes[-7:]) / min(7, len(closes))
        result["ma20"] = sum(closes[-20:]) / min(20, len(closes))
        result["ma50"] = sum(closes[-50:]) / min(50, len(closes)) if len(closes) >= 50 else None
        
        # Support/resistance from recent data
        result["resistance"] = max(highs[-5:])
        result["support"] = min(lows[-5:])
        # Current candle range
        result["today_high"] = max(highs[-2:])
        result["today_low"] = min(lows[-2:])
        
        # Volume analysis
        vols = [k[5] for k in klines_day[-10:]]
        avg_vol = sum(vols) / len(vols)
        result["vol_ratio"] = round(klines_day[-1][5] / avg_vol, 2) if avg_vol > 0 else 1
    
    return result

def generate_advice(sym, analysis):
    """Generate detailed trading advice from analysis data"""
    if not analysis:
        return f"\n{sym}: ❌ 数据不足"
    
    p = analysis["price_data"]
    price = p["price"]
    
    lines = []
    lines.append(f"\n── {sym} ──")
    lines.append(f"💰 ${price:,.2f}  {'📈' if p['change'] >= 0 else '📉'} {p['change']:+.2f}%")
    lines.append(f"📊 24h: ${p['low']:,.0f} ~ ${p['high']:,.0f}")
    
    rsi = analysis.get("rsi", 50)
    macd = analysis.get("macd_hist", 0)
    ma7 = analysis.get("ma7", 0)
    ma20 = analysis.get("ma20", 0)
    vol_ratio = analysis.get("vol_ratio", 1)
    atr = analysis.get("atr", 0)
    
    # Technical signals
    signals = []
    
    # RSI signal
    if rsi < 30:
        signals.append(("🟢", f"RSI超卖({rsi})"))
        rsi_bias = "超卖反弹"
    elif rsi < 40:
        signals.append(("🟢", f"RSI偏低({rsi})"))
        rsi_bias = "偏空但接近底部"
    elif rsi > 70:
        signals.append(("🔴", f"RSI超买({rsi})"))
        rsi_bias = "过热回调"
    elif rsi > 60:
        signals.append(("🔴", f"RSI偏高({rsi})"))
        rsi_bias = "偏多但接近顶部"
    else:
        signals.append(("⚪", f"RSI中性({rsi})"))
        rsi_bias = "方向不明"
    
    # MACD signal
    if macd > 0:
        signals.append(("🟢", f"MACD金叉({macd})"))
        macd_bias = "动能偏多"
    else:
        signals.append(("🔴", f"MACD死叉({macd})"))
        macd_bias = "动能偏空"
    
    # MA signal
    if ma7 > ma20:
        signals.append(("🟢", f"MA7({ma7:.0f}) > MA20({ma20:.0f})"))
        ma_bias = "多头排列"
    else:
        signals.append(("🔴", f"MA7({ma7:.0f}) < MA20({ma20:.0f})"))
        ma_bias = "空头排列"
    
    # Volume signal
    if vol_ratio > 1.5:
        signals.append(("⚡", f"成交量放大{vol_ratio}x"))
        vol_bias = "放量"
    elif vol_ratio < 0.5:
        signals.append(("💤", f"缩量({vol_ratio}x)"))
        vol_bias = "缩量"
    else:
        signals.append(("⚪", f"成交量正常({vol_ratio}x)"))
        vol_bias = "正常"
    
    for icon, text in signals:
        lines.append(f"  {icon} {text}")
    
    # Count bullish/bearish signals
    greens = sum(1 for s in signals if s[0] == "🟢")
    reds = sum(1 for s in signals if s[0] == "🔴")
    
    # Calculate support/resistance with ATR
    support = analysis.get("support", price * 0.95)
    resistance = analysis.get("resistance", price * 1.05)
    atr_value = atr if atr else price * 0.02
    
    lines.append("")
    
    # Prediction
    if greens >= 2:
        pred = "📈 短期看涨"
        if sym == "BTC":
            target1 = round(price + atr_value * 1.5, 2)
            target2 = round(price + atr_value * 3, 2)
        else:
            target1 = round(price + atr_value * 2, 2)
            target2 = round(price + atr_value * 4, 2)
        stop = round(price - atr_value * 1.5, 2)
        entry_zone = f"${price - atr_value * 0.5:,.2f} ~ ${price + atr_value * 0.5:,.2f}"
        direction = "做多"
    elif reds >= 2:
        pred = "📉 短期看跌"
        if sym == "BTC":
            target1 = round(price - atr_value * 1.5, 2)
            target2 = round(price - atr_value * 3, 2)
        else:
            target1 = round(price - atr_value * 2, 2)
            target2 = round(price - atr_value * 4, 2)
        stop = round(price + atr_value * 1.5, 2)
        entry_zone = f"${price - atr_value * 0.5:,.2f} ~ ${price + atr_value * 0.5:,.2f}"
        direction = "做空"
    else:
        pred = "⚪ 震荡整理"
        target1 = round(price + atr_value, 2)
        target2 = round(price - atr_value, 2)
        stop = round(price + atr_value * 2, 2)
        entry_zone = "观望"
        direction = "观望"
    
    lines.append(f"📋 AI分析:")
    lines.append(f"  判断: {pred}")
    lines.append(f"  建议方向: {direction}")
    lines.append(f"  入场区间: {entry_zone}")
    lines.append(f"  第一目标: ${target1:,.2f}")
    lines.append(f"  第二目标: ${target2:,.2f}")
    lines.append(f"  止损位: ${stop:,.2f}")
    
    if atr:
        rr = abs(target1 - price) / abs(stop - price) if abs(stop - price) > 0 else 0
        lines.append(f"  盈亏比: 1:{rr:.1f}")
    
    # Market sentiment analysis
    lines.append("")
    if rsi < 40 and macd < 0:
        lines.append(f"  💡 分析: {sym}处于弱势区域，RSI{rsi}偏低+MACD为负。")
        lines.append(f"  如果跌破支撑${support:,.0f}可能加速下跌，")
        lines.append(f"  但RSI接近超卖区(${'是' if rsi < 30 else '否'})，短线反弹风险存在。")
        lines.append(f"  建议等反弹到MA7(${ma7:,.0f})附近再做空，胜率更高。")
    elif rsi > 60 and macd > 0:
        lines.append(f"  💡 分析: {sym}处于强势区域，RSI{rsi}偏高+MACD为正。")
        lines.append(f"  趋势偏多但RSI已较高，追多风险大。")
        lines.append(f"  建议等回调到MA20(${ma20:,.0f})附近再做多。")
    elif abs(rsi - 50) < 10:
        lines.append(f"  💡 分析: {sym}处于震荡区间，多空力量平衡。")
        lines.append(f"  没有明确趋势信号，建议观望。")
        lines.append(f"  突破阻力${resistance:,.0f}可追多，跌破支撑${support:,.0f}可追空。")
    else:
        lines.append(f"  💡 分析: {sym}短期{rsi_bias}，{macd_bias}，{ma_bias}。")
        lines.append(f"  当前关键阻力${resistance:,.0f}，支撑${support:,.0f}。")
        lines.append(f"  建议在关键位附近操作，设好止损。")
    
    lines.append(f"  📌 小结: K线呈{ma_bias}，量能{vol_bias}，趋势{pred}")
    
    # Current price position vs Bollinger Bands
    bb_upper = analysis.get("boll_upper")
    bb_lower = analysis.get("boll_lower")
    bb_mid = analysis.get("boll_mid")
    if bb_upper and bb_lower and bb_mid:
        if price > bb_upper:
            lines.append(f"  📊 价格在布林带上轨之外({bb_upper:,.0f})，超买")
        elif price < bb_lower:
            lines.append(f"  📊 价格在布林带下轨之外({bb_lower:,.0f})，超卖")
        elif price > bb_mid:
            lines.append(f"  📊 价格在布林带中轨上方({bb_mid:,.0f}~{bb_upper:,.0f})")
        else:
            lines.append(f"  📊 价格在布林带中轨下方({bb_lower:,.0f}~{bb_mid:,.0f})")
    
    return "\n".join(lines)

def generate_full_report():
    """Generate complete report for BTC and ETH"""
    btc_day = get_kline("BTC", "1day", 50)
    btc_4h = get_kline("BTC", "4hour", 30)
    btc_1h = get_kline("BTC", "1hour", 24)
    
    eth_day = get_kline("ETH", "1day", 50)
    eth_4h = get_kline("ETH", "4hour", 30)
    eth_1h = get_kline("ETH", "1hour", 24)
    
    btc_analysis = analyze_coin("BTC", btc_day, btc_4h, btc_1h) if btc_day else None
    eth_analysis = analyze_coin("ETH", eth_day, eth_4h, eth_1h) if eth_day else None
    
    sentiment = get_network_sentiment()
    funding = sentiment.get("funding", 0)
    
    now = datetime.now().strftime("%m/%d %H:%M")
    
    lines = [f"🤖 AI 交易分析  {now}"]
    lines.append("")
    if funding != 0:
        lines.append(f"永续资金费率: {'%+.4f%%' % funding}")
    else:
        lines.append(f"永续资金费率: 获取失败")
    lines.append("")
    lines.append("── 市场概况 ──")
    
    # Summary line
    if btc_analysis and eth_analysis:
        bp = btc_analysis["price_data"]["price"]
        ep = eth_analysis["price_data"]["price"]
        eth_btc = ep / bp * 100
        lines.append(f"ETH/BTC: {eth_btc:.4f}%")
    
    if btc_analysis:
        lines.append(generate_advice("BTC", btc_analysis))
    
    if eth_analysis:
        lines.append(generate_advice("ETH", eth_analysis))
    
    lines.append("")
    lines.append("⚠️ 仅供参考，不构成投资建议")
    
    return "\n".join(lines)

if __name__ == "__main__":
    print(generate_full_report())
