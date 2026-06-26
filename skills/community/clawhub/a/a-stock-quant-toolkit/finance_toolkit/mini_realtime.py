"""
Mini实时行情 — 无需akshare，直接请求腾讯接口
支持：实时股价、分时/日K、MACD/KDJ/RSI计算
"""
import json, urllib.request, struct, time
from typing import Optional

class TencentStockAPI:
    """腾讯股票数据接口"""
    
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0'}
    
    def get_quote(self, code: str) -> dict:
        """获取单只股票实时行情"""
        tcode = self._to_tencent_code(code)
        url = f'https://qt.gtimg.cn/q={tcode}'
        data = urllib.request.urlopen(urllib.request.Request(url, headers=self.headers)).read().decode('gbk')
        
        if '=' not in data:
            return {'error': 'no data'}
        
        parts = data.split('=')[1].strip(';').strip('"').split('~')
        if len(parts) < 40:
            return {'error': f'parse failed, got {len(parts)} fields'}
        
        return {
            'code': code,
            'name': parts[1],
            'price': float(parts[3]),
            'open': float(parts[5]),
            'high': float(parts[33]),
            'low': float(parts[34]),
            'yclose': float(parts[4]) if parts[4] else 0,
            'change_pct': float(parts[32]) if parts[32] else 0,
            'volume': int(parts[6]) if parts[6] else 0,
            'amount': float(parts[37])/10000 if parts[37] else 0,  # 万元
            'pe': float(parts[39]) if parts[39] else 0,
            'time': parts[30] if len(parts)>30 else '',
            'bid': [float(v) for v in parts[10:20] if v],
            'ask': [float(v) for v in parts[20:30] if v],
        }
    
    def get_klines(self, code: str, days: int = 120) -> list:
        """获取日K线数据，返回[{date,open,close,high,low,volume}]"""
        tcode = self._to_tencent_code(code)
        # 腾讯日K接口
        url = f'https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param={tcode},day,,,{days},qfq'
        data = json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=self.headers)).read().decode('utf-8'))
        
        # key可能是 'qfqday', 'day', 或 'klines'->'day'
        dd = data['data'][tcode]
        klines = dd.get('qfqday') or dd.get('day')
        if not klines:
            klines = dd.get('klines', {}).get('day') if isinstance(dd.get('klines'), dict) else None
        if not klines:
            return []
        
        result = []
        for k in klines:
            # 腾讯接口混用两种格式：str("2026-05-06 8.65 8.76 8.83 8.61 344794") 或 list(["2026-05-06","8.65","8.76","8.83","8.61","344794"])
            if isinstance(k, str):
                parts = k.split(' ')
            elif isinstance(k, list):
                parts = k
            else:
                continue
            if len(parts) >= 6:
                result.append({
                    'date': parts[0],
                    'open': float(parts[1]),
                    'close': float(parts[2]),
                    'high': float(parts[3]),
                    'low': float(parts[4]),
                    'volume': float(parts[5]),
                })
        return result
    
    def _to_tencent_code(self, code: str) -> str:
        """转腾讯格式: 000009 → sz000009, sz000009 → sz000009"""
        code = code.replace('.', '')
        # 如果已经带 sz/sh 前缀，直接返回
        if code.startswith('sz') or code.startswith('sh'):
            return code
        if code.startswith('6') or code.startswith('9'):
            return f'sh{code}'
        return f'sz{code}'
    
    def batch_quote(self, codes: list) -> dict:
        """批量获取行情"""
        tcodes = ','.join(self._to_tencent_code(c) for c in codes)
        url = f'https://qt.gtimg.cn/q={tcodes}'
        data = urllib.request.urlopen(urllib.request.Request(url, headers=self.headers)).read().decode('gbk')
        
        results = {}
        for line in data.strip().split('\n'):
            if '=' not in line:
                continue
            parts = line.split('=')[1].strip(';').strip('"').split('~')
            if len(parts) < 40:
                continue
            results[parts[2]] = {
                'name': parts[1],
                'price': float(parts[3]),
                'change_pct': float(parts[32]),
                'high': float(parts[33]),
                'low': float(parts[34]),
                'open': float(parts[5]),
                'volume': int(parts[6]),
            }
        return results

# 技术指标计算
def calc_sma(values, period):
    """简单移动平均"""
    result = []
    for i in range(len(values)):
        if i < period - 1:
            result.append(None)
        else:
            result.append(sum(values[i-period+1:i+1]) / period)
    return result

def calc_ema(values, period):
    """指数移动平均"""
    multiplier = 2 / (period + 1)
    result = []
    ema = values[0] if values else 0
    for i, v in enumerate(values):
        if i == 0:
            ema = v
        else:
            ema = (v - ema) * multiplier + ema
        result.append(ema)
    return result

def calc_rsi(closes, period=14):
    """RSI计算"""
    gains = []
    losses = []
    for i in range(1, len(closes)):
        diff = closes[i] - closes[i-1]
        gains.append(max(diff, 0))
        losses.append(max(-diff, 0))
    
    avg_gain = sum(gains[:period]) / period if period <= len(gains) else 50
    avg_loss = sum(losses[:period]) / period if period <= len(losses) else 50
    
    rsis = [50] * len(closes)
    for i in range(period, len(gains) + 1):
        if i == period:
            pass  # already set
        else:
            avg_gain = (avg_gain * (period - 1) + gains[i-1]) / period
            avg_loss = (avg_loss * (period - 1) + losses[i-1]) / period
        
        if avg_loss == 0:
            rs = 100
        else:
            rs = avg_gain / avg_loss
        rsi_val = 100 - (100 / (1 + rs))
        rsis[i] = rsi_val
    
    return rsis

def calc_kdj(highs, lows, closes, period=9):
    """KDJ计算"""
    k_values = [50] * len(closes)
    d_values = [50] * len(closes)
    j_values = [50] * len(closes)
    
    for i in range(period - 1, len(closes)):
        hh = max(highs[i-period+1:i+1])
        ll = min(lows[i-period+1:i+1])
        if hh == ll:
            rsv = 50
        else:
            rsv = (closes[i] - ll) / (hh - ll) * 100
        
        if i == period - 1:
            k = 50
        else:
            k = 2/3 * k + 1/3 * rsv
        d = 2/3 * (d_values[i-1] if i > 0 else 50) + 1/3 * k
        j = 3 * k - 2 * d
        
        k_values[i] = k
        d_values[i] = d
        j_values[i] = j
    
    return k_values, d_values, j_values

def calc_macd(closes, fast=12, slow=26, signal=9):
    """MACD计算"""
    ema_fast = calc_ema(closes, fast)
    ema_slow = calc_ema(closes, slow)
    dif = [ef - es for ef, es in zip(ema_fast, ema_slow)]
    dea = calc_ema([d for d in dif if d is not None], signal)
    # align
    dea_full = [None] * (len(dif) - len(dea)) + dea
    macd = [2 * (d - de) if d is not None and de is not None else None 
            for d, de in zip(dif, dea_full)]
    return dif, dea_full, macd

if __name__ == '__main__':
    api = TencentStockAPI()
    # 批量行情
    quotes = api.batch_quote(['000009', '002332'])
    for code, q in quotes.items():
        print(f"[{code}] {q['name']}: {q['price']} ({q['change_pct']:+.2f}%)")
    
    # 日K + 技术指标
    for code in ['000009', '002332']:
        klines = api.get_klines(code, 60)
        if not klines:
            continue
        closes = [k['close'] for k in klines]
        print(f"\n--- {code} 技术指标 ---")
        print(f"MA5:  {calc_sma(closes, 5)[-1]:.2f}")
        print(f"MA10: {calc_sma(closes, 10)[-1]:.2f}")
        print(f"MA20: {calc_sma(closes, 20)[-1]:.2f}")
        rsis = calc_rsi(closes)
        print(f"RSI14: {rsis[-1]:.1f}")
        k, d, j = calc_kdj([k['high'] for k in klines], [k['low'] for k in klines], closes)
        print(f"KDJ: K={k[-1]:.1f} D={d[-1]:.1f} J={j[-1]:.1f}")
        dif, dea, macd = calc_macd(closes)
        print(f"MACD: DIF={dif[-1]:.3f} DEA={dea[-1]:.3f}")
