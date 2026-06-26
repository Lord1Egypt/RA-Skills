"""
FFT频谱分析模块 — 供 monitor_v3 调用
对K线序列做傅里叶分析，识别主周期、能量分布
用于辅助策略参数优化
"""
import math

def fft(x):
    """Cooley-Tukey FFT (N=2^k)"""
    n = len(x)
    if n <= 1:
        return x
    # 填充到2的幂
    t = 1
    while t < n:
        t *= 2
    if t != n:
        x = list(x) + [0] * (t - n)
    return _fft_core(x)

def _fft_core(x):
    n = len(x)
    if n <= 1:
        return x
    even = _fft_core(x[0::2])
    odd = _fft_core(x[1::2])
    t = [complex(math.cos(-2*math.pi*k/n), math.sin(-2*math.pi*k/n)) * odd[k] for k in range(n//2)]
    return [even[k] + t[k] for k in range(n//2)] + [even[k] - t[k] for k in range(n//2)]

def detrend(x):
    """去线性趋势"""
    n = len(x)
    if n < 2:
        return x
    mx, my = sum(range(n))/n, sum(x)/n
    xy = sum(i*v for i,v in enumerate(x))
    xx = sum(i*i for i in range(n))
    slope = (xy - n*mx*my) / (xx - n*mx*mx)
    intercept = my - slope*mx
    return [x[i] - (slope*i + intercept) for i in range(n)]

def analyze_spectrum(signal, sample_count=None):
    """
    对信号做FFT并返回频谱分析结果
    
    参数:
        signal: list[float] — 时间序列
        sample_count: int — 采样点数量 (2的幂，默认实际长度)
    
    返回:
        dict: {
            'periods': [(周期天数, 幅度, 能量占比%), ...],  # Top8
            'energy': {'low': 低频占比, 'mid': 中频占比, 'high': 高频占比},
            'dominant_period': 主周期天数,
            'peak_ratio': 主峰/平均幅度比,
            'has_cycle': bool 是否有显著周期,
            'suggestion': str 建议
        }
    """
    n = sample_count or len(signal)
    if n > len(signal):
        n = len(signal)
    
    # 取最近n个点并去趋势
    trimmed = detrend(signal[-n:])
    
    # FFT
    freq = fft(trimmed)
    mags = [abs(v) for v in freq]
    half = len(mags) // 2
    mags = mags[:half]
    
    # 找主周期
    peaks = []
    for i in range(1, len(mags)):
        peaks.append((n / i, mags[i], 0.0))  # (period, amp, energy_pct)
    
    # 能量占比
    total_e = sum(m**2 for m in mags[1:]) or 1
    
    # 按幅度排序
    peaks.sort(key=lambda x: x[1], reverse=True)
    top_peaks = []
    for period, amp, _ in peaks[:8]:
        pct = amp / max(peaks[0][1], 1)  # 相对占比
        top_peaks.append((period, int(amp), round(pct*100, 1)))
    
    # 能量分频
    lo = sum(m**2 for m in mags[1:n//30]) / total_e if n > 30 else 0
    md = sum(m**2 for m in mags[n//30:n//5]) / total_e if n > 5 else 0
    hi = sum(m**2 for m in mags[n//5:]) / total_e
    
    # 判断是否有显著周期
    dom_amp = peaks[0][1] if peaks else 0
    avg_amp = sum(p[1] for p in peaks[1:]) / max(len(peaks)-1, 1)
    ratio = dom_amp / avg_amp if avg_amp else 0
    has_cycle = ratio > 2.5
    dom_period = round(peaks[0][0], 1) if peaks else 0
    
    # 建议
    if has_cycle:
        if dom_period < 10:
            suggestion = "短线操作，关注周期低点"
        elif dom_period < 30:
            suggestion = f"波段操作，按{round(dom_period)}天节奏"
        else:
            suggestion = "中线趋势，注意大级别拐点"
    else:
        suggestion = "频谱分散，趋势跟踪优于周期择时"
    
    return {
        'periods': top_peaks,
        'energy': {
            'low_pct': round(lo*100, 1),    # >30天
            'mid_pct': round(md*100, 1),    # 5-30天
            'high_pct': round(hi*100, 1),   # <5天
        },
        'dominant_period': dom_period,
        'peak_ratio': round(ratio, 1),
        'has_cycle': has_cycle,
        'suggestion': suggestion
    }

def get_strategy_hints(fft_result: dict, score: int) -> str:
    """
    根据频谱分析给出策略调参建议
    """
    hints = []
    e = fft_result['energy']
    
    # 能量分布 -> 操作周期建议
    if e['low_pct'] > 70:
        hints.append(f"长期趋势主导({e['low_pct']}%)，建议中线持仓")
    elif e['mid_pct'] > 30:
        hints.append(f"中频活跃({e['mid_pct']}%)，适合波段操作")
    elif e['high_pct'] > 15:
        hints.append(f"噪声偏高({e['high_pct']}%)，缩短周期参数")
    
    # 策略参数建议
    dom = fft_result.get('dominant_period', 0)
    if dom > 20:
        hints.append(f"MA周期可适当放大到MA{min(round(dom/2), 40)}")
    elif 5 < dom < 20:
        hints.append(f"适合快速MA(MA{round(dom//2)})")
    
    # 如果评分低但有周期
    if score < 20 and fft_result['has_cycle']:
        hints.append("当前评分低但存在周期，可能是调整末端")
    
    return '; '.join(hints) if hints else "频谱正常"

# ===== 直接运行时测试 =====
if __name__ == '__main__':
    # 用新浪接口拿数据测试
    import json, urllib.request
    url = 'http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol=sz000009&scale=240&ma=no&datalen=500'
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    resp = urllib.request.urlopen(req, timeout=10)
    data = json.loads(resp.read())
    closes = [float(d["close"]) for d in data]
    
    result = analyze_spectrum(closes, 256)
    print("频谱分析:")
    print(f"  主周期: {result['dominant_period']}天")
    print(f"  显著周期: {'✅' if result['has_cycle'] else '❌'}")
    print(f"  能量分布: 低频{result['energy']['low_pct']}% 中频{result['energy']['mid_pct']}% 高频{result['energy']['high_pct']}%")
    print(f"  Top3: {result['periods'][:3]}")
    print(f"  策略建议: {result['suggestion']}")
    print(f"  调参建议: {get_strategy_hints(result, 30)}")
