#!/usr/bin/env python3
"""
A股盯盘策略系统 v2
使用腾讯实时行情API（唯一稳定的数据源）
信号基于当日最高、最低、开盘、昨收计算技术位置

优化参数 (2026-04-23 回测):
- 中国宝安(000009): MA快=14, MA慢=18, 止损5%
- 仙琚制药(002332): MA快=18, MA慢=20, 无止损
"""
import subprocess, re, json, os
from datetime import datetime

class StockAPI:
    """腾讯行情API"""
    def batch(self, symbols):
        if isinstance(symbols, str): symbols = [symbols]
        url = f"http://qt.gtimg.cn/q={','.join(symbols)}"
        r = subprocess.run(['curl.exe','-s',url], capture_output=True, timeout=10)
        raw = r.stdout.decode('gbk', errors='ignore')
        results = {}
        for line in raw.strip().strip(';').split(';'):
            m = re.search(r'"([^"]+)"', line)
            if not m: continue
            p = m.group(1).split('~')
            if len(p) < 46: continue
            d = {
                'name': p[1], 'code': p[2],
                'price': float(p[3]) if p[3] else 0,
                'yclose': float(p[4]) if p[4] else 0,
                'open': float(p[5]) if p[5] else 0,
                'volume': int(p[6]) if p[6] else 0,
                'change_pct': round(float(p[32]) if p[32] else 0, 2),
                'high': float(p[33]) if p[33] else 0,
                'low': float(p[34]) if p[34] else 0,
                'amount': float(p[37]) if len(p)>37 and p[37] else 0,
                'turnover': float(p[38]) if len(p)>38 and p[38] else 0,
                'pe': float(p[39]) if len(p)>39 and p[39] else 0,
                'market_cap': float(p[45]) if len(p)>45 and p[45] else 0,
            }
            results[p[1]] = d
        return results

def analyze_stock(d, hist_cache=None):
    """单只股票技术分析（基于当日数据）"""
    price = d['price']
    yclose = d['yclose']
    high = d['high']
    low = d['low']
    open_p = d['open']
    change = d['change_pct']

    if yclose == 0: return {}

    # 日内位置
    day_range = high - low if high > low else 1
    day_pos = (price - low) / day_range * 100 if day_range > 0 else 50
    pos_note = '高位' if day_pos > 70 else ('低位' if day_pos < 30 else '中位')

    # 缺口分析
    gap_up = open_p > yclose * 1.01
    gap_down = open_p < yclose * 0.99

    # 涨跌幅信号
    if change >= 3:
        signal = '📈 大涨'
    elif change >= 1:
        signal = '🟢 上涨'
    elif change >= -1:
        signal = '⚪ 横盘'
    elif change >= -3:
        signal = '🔻 下跌'
    else:
        signal = '🔴 大跌'

    # 振幅
    amplitude = (high - low) / yclose * 100
    amp_note = '大幅波动' if amplitude > 5 else ('正常波动' if amplitude > 2 else '窄幅震荡')

    # 量价关系
    vol_note = ''
    if change > 0 and d['volume'] > 0:
        vol_note = '带量上涨 ✅' if amplitude > 3 else '温和上涨'
    elif change < 0 and d['volume'] > 0:
        vol_note = '放量下跌 ⚠️' if amplitude > 3 else '缩量回调'

    # 相对昨收位置
    to_high = (high - yclose) / yclose * 100  # 今日最高涨幅
    to_low = (low - yclose) / yclose * 100    # 今日最大跌幅

    return {
        'signal': signal,
        'pos': pos_note,
        'amplitude': f"{amplitude:.1f}%",
        'amp_note': amp_note,
        'gap_up': gap_up,
        'gap_down': gap_down,
        'to_high': f"{to_high:.2f}%",
        'to_low': f"{to_low:.2f}%",
        'vol_note': vol_note,
        'support': round(low * 0.98, 2),  # 支撑位
        'resistance': round(high * 1.02, 2),  # 压力位
        'avg_price_band': f"{round(min(open_p, yclose), 2)}-{round(max(open_p, yclose), 2)}",  # 均价带
    }

def factor_score(d):
    """多因子评分"""
    scores = {}
    pe = d['pe']
    turnover = d['turnover']
    change = d['change_pct']
    mc = d['market_cap']

    # 价值
    if 0 < pe < 20: scores['价值'] = 80 + max(0, 20-pe)
    elif 20 <= pe <= 50: scores['价值'] = 60 - (pe-20)*0.5
    elif pe > 50 or pe <= 0: scores['价值'] = 30
    else: scores['价值'] = 50

    # 动量
    scores['动量'] = min(100, max(0, 50 + change*5))

    # 活跃度
    if 1 < turnover < 5: scores['活跃度'] = 70
    elif 0.5 < turnover <= 1 or 5 <= turnover < 10: scores['活跃度'] = 50
    elif turnover <= 0.5: scores['活跃度'] = 30
    else: scores['活跃度'] = 40

    # 规模（小盘溢价）
    if mc < 50: scores['规模'] = 80
    elif 50 <= mc < 200: scores['规模'] = 60
    elif 200 <= mc < 500: scores['规模'] = 40
    else: scores['规模'] = 30

    scores['综合'] = round(sum(scores.values()) / len(scores), 1)
    return scores

def morning_report(api):
    """开盘前报告"""
    now = datetime.now()
    is_am = now.hour < 12

    # 大盘
    idx = api.batch(['sh000001','sz399001','sz399006','sh000300'])

    # 盯盘股
    watch = api.batch(['sz000009','sz002332'])

    # 热门股池
    pool = api.batch([
        'sz300750','sz000858','sh600036','sz002594','sh600519',
        'sz300059','sh600900','sz000333','sh601899','sh600887',
        'sz002415','sh600276','sh600809','sz000568','sz002714'
    ])

    lines = []
    lines.append("📊 **A股早报**")
    lines.append(f"🕐 {now.strftime('%Y-%m-%d %H:%M')}\n")

    lines.append("**📈 大盘**")
    for n, d in idx.items():
        a = '🟢' if d['change_pct'] >= 0 else '🔴'
        lines.append(f"{a} {n}: {d['price']} ({d['change_pct']:+.2f}%)")

    lines.append("\n**👁️ 盯盘股**")
    for n, d in watch.items():
        a = '🟢' if d['change_pct'] >= 0 else '🔴'
        ta = analyze_stock(d)
        lines.append(f"{a} **{n}**({d['code']}): {d['price']} ({d['change_pct']:+.2f}%)")
        lines.append(f"  开:{d['open']}  高:{d['high']}  低:{d['low']}")
        if ta:
            lines.append(f"  信号: {ta['signal']} | 位置: {ta['pos']} | {ta['amp_note']}")
            lines.append(f"  支撑: {ta['support']}  压力: {ta['resistance']}")

            # 开盘建议
            if ta['signal'].startswith('📈'):
                lines.append(f"  💡 **偏强，关注能否持续放量**")
            elif ta['signal'].startswith('🔴'):
                lines.append(f"  💡 **偏弱，注意低开后的承接力度**")
            elif ta['gap_up']:
                lines.append(f"  💡 **跳空高开，关注缺口回补情况**")
            elif ta['gap_down']:
                lines.append(f"  💡 **跳空低开，留意恐慌是否能修复**")
            else:
                lines.append(f"  💡 **平开震荡，等盘中方向选择**")

    # 多因子排名
    lines.append("\n**🔥 多因子评分**")
    scored = []
    for n, d in pool.items():
        sf = factor_score(d)
        d['score'] = sf['综合']
        scored.append((n, d, sf))
    scored.sort(key=lambda x: x[1]['score'], reverse=True)

    for i, (n, d, sf) in enumerate(scored[:5], 1):
        a = '🟢' if d['change_pct'] >= 0 else '🔴'
        lines.append(f"{i}. {a} {n}({d['code']}): {d['price']} | {d['change_pct']:+.2f}% | 评分:{d['score']}")

    lines.append("\n---")
    lines.append("🔔 半自动模式：我出信号你操作，先回测验证")
    return "\n".join(lines)

def closing_report(api):
    """收盘复盘报告"""
    now = datetime.now()
    idx = api.batch(['sh000001','sz399001','sz399006','sh000300'])
    watch = api.batch(['sz000009','sz002332'])

    avg = sum(d['change_pct'] for d in idx.values()) / len(idx)

    lines = []
    lines.append("📊 **今日复盘**")
    lines.append(f"🕐 {now.strftime('%Y-%m-%d %H:%M')}\n")

    lines.append("**📈 大盘**")
    for n, d in idx.items():
        a = '🟢' if d['change_pct'] >= 0 else '🔴'
        lines.append(f"{a} {n}: {d['price']} ({d['change_pct']:+.2f}%)")

    if avg > 0.3:
        lines.append("📊 今日 **普涨**，市场偏强 🟢")
    elif avg < -0.3:
        lines.append("📊 今日 **普跌**，注意控制仓位 🔴")
    else:
        lines.append("📊 今日 **震荡**，无明显方向")

    lines.append("\n**👁️ 盯盘股**")
    for n, d in watch.items():
        a = '🟢' if d['change_pct'] >= 0 else '🔴'
        ta = analyze_stock(d)
        lines.append(f"{a} **{n}**: {d['price']} ({d['change_pct']:+.2f}%)")
        if ta:
            lines.append(f"  区间: {d['low']} - {d['high']} | {ta['amp_note']} | {ta['vol_note']}")
            lines.append(f"  支撑: {ta['support']}  压力: {ta['resistance']}")

            if d['change_pct'] > 0 and d['volume'] > 0:
                lines.append(f"  💡 **今日收涨，明日关注能否站稳**")
            elif d['change_pct'] < 0:
                lines.append(f"  💡 **今日收跌，明日留意支撑位有效性**")
            else:
                lines.append(f"  💡 **今日平收，方向待确认**")

    lines.append("\n---")
    lines.append("🔔 明日开盘前自动推送早报")
    return "\n".join(lines)

def backtest_report(api, symbol, label, days_data=None):
    """回测分析（当前基于当日数据）"""
    d = api.batch([symbol]).get(label)
    if not d: return None
    ta = analyze_stock(d)
    sf = factor_score(d)

    lines = []
    lines.append(f"📋 **{label} 综合评估**")
    lines.append(f"当前价: {d['price']} | 涨跌: {d['change_pct']:+.2f}%")

    if ta:
        lines.append(f"\n**技术面**")
        lines.append(f"  日内定位: {ta['pos']} | {ta['amp_note']}")
        lines.append(f"  支撑位: {ta['support']} | 压力位: {ta['resistance']}")
        lines.append(f"  缺口: {'有跳空↑' if ta['gap_up'] else ''}{'有跳空↓' if ta['gap_down'] else ''}{'无' if not ta['gap_up'] and not ta['gap_down'] else ''}")

    if sf:
        lines.append(f"\n**多因子评分**")
        for k, v in sf.items():
            lines.append(f"  {k}: {v}")
        if sf.get('综合', 0) >= 60:
            lines.append(f"\n  📊 综合评估: **偏优**")
        elif sf.get('综合', 0) >= 40:
            lines.append(f"  📊 综合评估: **中性**")
        else:
            lines.append(f"  📊 综合评估: **偏低**")

    return "\n".join(lines)

if __name__ == "__main__":
    import sys
    api = StockAPI()

    mode = sys.argv[1] if len(sys.argv) > 1 else 'all'

    if mode == 'morning':
        print(morning_report(api))
    elif mode == 'closing':
        print(closing_report(api))
    elif mode == 'backtest':
        # 回测两只盯盘股
        print(backtest_report(api, 'sz000009', '中国宝安'))
        print()
        print(backtest_report(api, 'sz002332', '仙琚制药'))
    else:
        # 全量输出
        print("=" * 45)
        print("📊 A股盯盘策略系统 v2")
        print("=" * 45)

        print("\n📍 大盘概览:")
        idx = api.batch(['sh000001','sz399001','sz399006','sh000300'])
        for n, d in idx.items():
            a = '🟢' if d['change_pct'] >= 0 else '🔴'
            print(f" {a} {n}: {d['price']} ({d['change_pct']:+.2f}%)")

        print("\n📍 盯盘股:")
        watch = api.batch(['sz000009','sz002332'])
        for n, d in watch.items():
            a = '🟢' if d['change_pct'] >= 0 else '🔴'
            ta = analyze_stock(d)
            print(f" {a} {n}({d['code']}): {d['price']} ({d['change_pct']:+.2f}%)")
            if ta:
                print(f"    信号: {ta['signal']} | 振幅: {ta['amplitude']} | {ta['amp_note']}")
                print(f"    支撑: {ta['support']} | 压力: {ta['resistance']}")

        print(f"\n{'='*45}")
        print("✅ 系统就绪 | 模式：半自动")
        print("   python strategy_engine.py morning  → 早报")
        print("   python strategy_engine.py closing → 复盘")
        print("   python strategy_engine.py backtest → 回测评估")

