"""
监控脚本增强 v3.1 — FFT频谱分析整合版
实时行情 + 技术指标 + 信号评分(60分) + 频谱分析 → 策略调参
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from mini_realtime import TencentStockAPI, calc_sma, calc_rsi, calc_kdj, calc_macd
from fourier_analyzer import analyze_spectrum, get_strategy_hints
import json
from datetime import datetime

# 监控股票
WATCH_LIST = [
    {'code': '000009', 'name': '中国宝安', 'cost': None},  # 羽确认后填
    {'code': '002332', 'name': '仙琚制药', 'cost': None},
]

def score_stock(code: str, api: TencentStockAPI) -> dict:
    """60分评分体系"""
    q = api.get_quote(code)
    klines = api.get_klines(code, 60)
    if not klines or not q:
        return {'error': 'no data'}
    
    closes = [k['close'] for k in klines]
    highs = [k['high'] for k in klines]
    lows = [k['low'] for k in klines]
    
    score = 0
    signals = []
    price = q['price']
    
    # 1. MA位置 (10分)
    ma5 = calc_sma(closes, 5)[-1]
    ma10 = calc_sma(closes, 10)[-1]
    ma20 = calc_sma(closes, 20)[-1]
    if price > ma20: score += 5; signals.append('↑MA20')
    elif price > ma10: score += 3
    if price > ma5: score += 3; signals.append('↑MA5')
    if ma5 > ma10 > ma20: score += 2; signals.append('多头排列')
    
    # 2. 布林带位置 (10分)
    mid = calc_sma(closes, 20)[-1]
    std = (sum((c-mid)**2 for c in closes[-20:])/20)**0.5
    upper = mid + 2*std; lower = mid - 2*std
    bb_width = (upper - lower) / mid * 100  # 宽度百分比
    if price <= lower: score += 8; signals.append('触下轨⚡')
    elif price <= mid: score += 4; signals.append('中轨下方')
    elif price > upper: score += 2
    
    # 3. RSI (10分)
    rsis = calc_rsi(closes)
    r = rsis[-1]
    if r < 25: score += 10; signals.append('RSI超卖')
    elif r < 35: score += 6; signals.append('RSI偏低')
    elif 35 <= r <= 65: score += 5; signals.append('RSI中性')
    elif r > 75: score += 2; signals.append('RSI超买')
    
    # 4. KDJ (10分)
    k, d, j = calc_kdj(highs, lows, closes)
    jv = j[-1]
    if jv < 0: score += 10; signals.append('J<0超卖')
    elif jv < 20: score += 6; signals.append('J值偏低')
    elif jv > 100: signal = 'J>100超买'
    
    # 5. MACD (10分)
    dif, dea, macd = calc_macd(closes)
    if dif[-1] > dea[-1]:
        score += 6; signals.append('MACD金叉')
        if dif[-2] <= dea[-2]: score += 4; signals.append('金叉刚形成')
    else:
        if dif[-2] >= dea[-2]: score -= 2; signals.append('死叉刚形成')
    
    # 6. 涨跌幅趋势 (10分)
    if q['change_pct'] > 0: score += 3
    if q['change_pct'] > 2: score += 3; signals.append('涨幅>2%')
    if len(closes) > 5:
        trend_5d = closes[-1] - closes[-5]
        if trend_5d > 0: score += 4; signals.append('5日上涨趋势')
    
    # 方向判定
    if score >= 40: direction = '强烈看多 ✅✅'
    elif score >= 30: direction = '看多 ✅'
    elif score >= 20: direction = '中性 ➖'
    elif score >= 10: direction = '看空 ❌'
    else: direction = '强烈看空 ❌❌'
    
    return {
        'code': code,
        'name': q['name'],
        'price': price,
        'change_pct': q['change_pct'],
        'score': score,
        'direction': direction,
        'signals': signals,
        'ma5': round(ma5,2), 'ma10': round(ma10,2), 'ma20': round(ma20,2),
        'rsi': round(r,1),
        'kdj': f'K={k[-1]:.0f} D={d[-1]:.0f} J={j[-1]:.0f}',
        'macd': f'DIF={dif[-1]:.3f} DEA={dea[-1]:.3f}',
        'bb': f'{lower:.2f}-{upper:.2f}',
        'pe': q['pe'],
        'fft': None,  # 频谱分析，由 enrich_with_spectrum() 填充
    }

def enrich_spectrum(code: str, api: TencentStockAPI = None) -> dict:
    """对股票做频谱分析"""
    if api is None:
        api = TencentStockAPI()
    klines = api.get_klines(code, 500)
    if not klines or len(klines) < 30:
        return None
    closes = [k['close'] for k in klines]
    return analyze_spectrum(closes, 256)

def all_quotes():
    """批量获取所有监控股票行情 + 频谱"""
    api = TencentStockAPI()
    codes = [w['code'] for w in WATCH_LIST]
    results = []
    for code in codes:
        r = score_stock(code, api)
        if 'error' not in r:
            # 加频谱
            try:
                r['fft'] = enrich_spectrum(code, api)
                r['fft_hint'] = get_strategy_hints(r['fft'], r['score']) if r['fft'] else ''
            except Exception:
                r['fft'] = None
                r['fft_hint'] = ''
            results.append(r)
    return results

def format_report(results: list) -> str:
    """格式化报告（含频谱）"""
    now = datetime.now().strftime('%H:%M')
    lines = [f'📊 实盘监控 + FFT频谱 | {datetime.now().strftime("%Y-%m-%d")} {now}']
    lines.append('=' * 50)
    
    for r in results:
        lines.append(f"\n{'🟢' if r['change_pct']>=0 else '🔴'} {r['name']} {r['code']}")
        lines.append(f"  现价: {r['price']} ({r['change_pct']:+.2f}%) | 评分: {r['score']}/60")
        lines.append(f"  方向: {r['direction']}")
        lines.append(f"  MA: {r['ma5']}/{r['ma10']}/{r['ma20']} | RSI: {r['rsi']}")
        lines.append(f"  {r['kdj']} | {r['macd']}")
        lines.append(f"  布林: {r['bb']}")
        if r['signals']:
            lines.append(f"  信号: {' '.join(r['signals'])}")
        
        # FFT频谱部分
        fft = r.get('fft')
        if fft:
            e = fft['energy']
            top3 = fft['periods'][:3]
            top3_strs = [f'{p:.0f}d({a})' for p, a, _ in top3]
            lines.append(f"  📈 频谱: 主周期{fft['dominant_period']}d | 峰比{fft['peak_ratio']}x{'✅' if fft['has_cycle'] else '❌'}")
            lines.append(f"         能量: 低频{e['low_pct']}% 中频{e['mid_pct']}% 高频{e['high_pct']}%")
            lines.append(f"         周期: {' '.join(top3_strs)}")
            lines.append(f"         建议: {fft['suggestion']}")
            hint = r.get('fft_hint', '')
            if hint:
                lines.append(f"         调参: {hint}")
    
    return '\n'.join(lines)

def check_alerts(prev_scores: dict = None) -> list:
    """检查止损/买入机会"""
    api = TencentStockAPI()
    alerts = []
    
    for w in WATCH_LIST:
        q = api.get_quote(w['code'])
        if not q:
            continue
        
        # 止损检查（如果有成本）
        if w['cost']:
            loss_pct = (q['price'] - w['cost']) / w['cost'] * 100
            if loss_pct <= -12:
                alerts.append({'type': '强制止损', 'stock': w['name'], 'msg': f'{loss_pct:.1f}% 亏损, 现价{q["price"]}'})
            elif loss_pct <= -8:
                alerts.append({'type': '止损', 'stock': w['name'], 'msg': f'{loss_pct:.1f}% 亏损, 现价{q["price"]}'})
            elif loss_pct <= -5:
                alerts.append({'type': '预警', 'stock': w['name'], 'msg': f'{loss_pct:.1f}% 亏损'})
        
        # 买入机会
        r = score_stock(w['code'], api)
        if r.get('score', 0) >= 45:
            alerts.append({'type': '买入机会', 'stock': w['name'], 'msg': f'评分{r["score"]}/60, 现价{q["price"]}'})
    
    return alerts

if __name__ == '__main__':
    results = all_quotes()
    print(format_report(results))
    print()
    
    alerts = check_alerts()
    if alerts:
        print('🚨 警报:')
        for a in alerts:
            print(f'  {a["type"]}: {a["stock"]} — {a["msg"]}')
    else:
        print('✅ 无警报')
    
    # 总线通知 — 集成到系统通信
    try:
        import sys, os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
        from system_bridge import SystemBridge
        if alerts:
            SystemBridge.monitor_notify_knowledge(alerts)
            print('📨 警报已同步到知识库')
    except ImportError:
        pass
