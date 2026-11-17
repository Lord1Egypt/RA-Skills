"""
FactorLab Engine - Self-contained multi-factor analysis engine.

No GUI dependencies. Requires: pytdx (optional, falls back to simulation).

Based on open-source financial engineering research reports:
  - Factor Cutting Theory (因子切割论): 3-factor model (ideal reversal, ideal amplitude, long momentum)
"""

import json
import math
import random
import sys
from datetime import datetime, timedelta
from pathlib import Path

# ── Data fetching ──────────────────────────────────────────────

DEFAULT_POOL = [
    '000001', '000002', '000100', '000333', '000651', '000725',
    '000858', '002415', '002475', '002594', '300750', '600036',
    '600276', '600585', '600887', '600900', '601318', '000938',
    '002008', '002463', '002916', '300782', '600707', '603019',
    '603773', '000021', '002281', '300476', '603259', '688981',
    '688012', '688036', '600519', '601012', '601888', '601899',
]

DEFAULT_NAMES = {
    '000001': '平安银行', '000002': '万科A', '000100': 'TCL科技',
    '000333': '美的集团', '000651': '格力电器', '000725': '京东方A',
    '000858': '五粮液', '002415': '海康威视', '002475': '立讯精密',
    '002594': '比亚迪', '300750': '宁德时代', '600036': '招商银行',
    '600276': '恒瑞医药', '600519': '贵州茅台', '600585': '海螺水泥',
    '600887': '伊利股份', '600900': '长江电力', '601318': '中国平安',
    '000938': '紫光股份', '603019': '中科曙光', '688981': '中芯国际',
    '002008': '大族激光', '002463': '沪电股份', '002916': '深南电路',
    '300782': '卓胜微', '600707': '西藏药业', '603773': '三祥新材',
    '000021': '深科技', '002281': '光迅科技', '300476': '胜宏科技',
    '603259': '药明康德', '688012': '中微公司', '688036': '传音控股',
    '601012': '隆基绿能', '601888': '中国中免', '601899': '紫金矿业',
}

DEFAULT_SERVERS = [
    {'ip': '119.6.200.40', 'port': 7709, 'name': '主站1'},
    {'ip': '182.140.139.191', 'port': 7709, 'name': '主站2'},
    {'ip': '218.200.222.134', 'port': 7709, 'name': '主站3'},
    {'ip': '182.150.28.166', 'port': 7709, 'name': '主站4'},
]


def _config_path():
    p = Path(__file__).resolve().parent.parent / 'assets' / 'servers.json'
    if p.exists():
        return p
    # Fallback: project config
    p2 = Path(__file__).resolve().parent.parent.parent.parent / 'config' / 'servers.json'
    return p2 if p2.exists() else p


def load_config():
    path = _config_path()
    if not path.exists():
        return {'servers': DEFAULT_SERVERS, 'settings': {'refresh_seconds': 30, 'top_k': 30, 'min_score': 55, 'use_live_data': True}}
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception:
        return {'servers': DEFAULT_SERVERS, 'settings': {'refresh_seconds': 30, 'top_k': 30, 'min_score': 55, 'use_live_data': True}}


def load_settings():
    return load_config().get('settings', {})


# ── Math helpers ───────────────────────────────────────────────

def _safe_float(value, default=0.0):
    try:
        if value is None:
            return default
        value = float(value)
        if not math.isfinite(value):
            return default
        return value
    except Exception:
        return default


def ma(values, period):
    values = [_safe_float(v) for v in values]
    if not values:
        return 0.0
    if len(values) < period:
        return values[-1]
    return sum(values[-period:]) / period


# ── Factor Cutting Theory ──────────────────────────────────────

class CuttingEngine:
    """Factor cutting engine: object + knife -> high_minus_low."""

    def cut(self, target, knife, output='high_minus_low', high_pct=0.5):
        pairs = []
        for t, k in zip(target, knife):
            try:
                t = float(t)
                k = float(k)
            except Exception:
                continue
            if math.isfinite(t) and math.isfinite(k):
                pairs.append((k, t))
        if not pairs:
            return 0.0
        pairs.sort(key=lambda item: item[0])
        size = max(1, int(len(pairs) * high_pct))
        low_val = self._mean([item[1] for item in pairs[:size]])
        high_val = self._mean([item[1] for item in pairs[-size:]])
        if output == 'high':
            return high_val
        if output == 'low':
            return low_val
        if output == 'low_minus_high':
            return low_val - high_val
        return high_val - low_val

    @staticmethod
    def _mean(values):
        values = [v for v in values if isinstance(v, (int, float)) and math.isfinite(v)]
        return sum(values) / len(values) if values else 0.0


engine = CuttingEngine()


# ── Factor scoring functions ───────────────────────────────────

def score_ideal_reversal(value):
    value = _safe_float(value)
    if value < -0.03:
        return 100
    if value < -0.02:
        return 85
    if value < -0.01:
        return 70
    if value < 0:
        return 55
    if value < 0.01:
        return 40
    return 25


def score_ideal_amplitude(value):
    value = _safe_float(value)
    if value < -0.015:
        return 100
    if value < -0.008:
        return 80
    if value < -0.003:
        return 65
    if value < 0:
        return 50
    if value < 0.005:
        return 35
    return 20


def score_long_momentum(value):
    value = _safe_float(value)
    if value > 0.08:
        return 100
    if value > 0.05:
        return 85
    if value > 0.02:
        return 70
    if value > 0:
        return 55
    if value > -0.02:
        return 40
    return 25


def signal_for_score(score):
    score = _safe_float(score)
    if score >= 85:
        return '强势买入'
    if score >= 70:
        return '关注'
    if score >= 55:
        return '留意'
    return '回避'


def signal_icon(score):
    score = _safe_float(score)
    if score >= 85:
        return '🔥'
    if score >= 70:
        return '✅'
    if score >= 55:
        return '⚡'
    return '❌'


# ── Core factor computation ────────────────────────────────────

def _bar_value(bar, primary, fallback=None):
    if fallback is None:
        fallback = primary
    return _safe_float(bar.get(primary, bar.get(fallback, 0)))


def _bars_to_arrays(bars):
    closes = [_bar_value(b, 'c', 'close') for b in bars]
    highs = [_bar_value(b, 'h', 'high') for b in bars]
    lows = [_bar_value(b, 'l', 'low') for b in bars]
    vols = [max(_bar_value(b, 'v', 'vol'), 0.0) for b in bars]
    amounts = [_bar_value(b, 'a', 'amount') for b in bars]
    amounts = [a if a > 0 else c * v for a, c, v in zip(amounts, closes, vols)]
    return closes, highs, lows, vols, amounts


def compute_raw_factors(bars):
    bars = bars or []
    if not bars:
        return {'ideal_reversal': 0.0, 'ideal_amplitude': 0.0, 'long_momentum': 0.0, 'data_points': 0}
    closes, highs, lows, vols, amounts = _bars_to_arrays(bars)
    n = len(closes)
    result = {'ideal_reversal': 0.0, 'ideal_amplitude': 0.0, 'long_momentum': 0.0, 'data_points': n}
    if n >= 20:
        prev = [closes[i - 1] if i > 0 else closes[0] for i in range(n)]
        returns = [closes[i] / max(prev[i], 0.01) - 1 for i in range(n)]
        avg_trade = [amounts[i] / max(vols[i], 1) for i in range(n)]
        result['ideal_reversal'] = round(engine.cut(returns[-20:], avg_trade[-20:], 'high_minus_low', 0.5), 4)
        amps = [(highs[i] - lows[i]) / max(prev[i], 0.01) for i in range(n)]
        result['ideal_amplitude'] = round(engine.cut(amps[-20:], closes[-20:], 'high_minus_low', 0.25), 4)
    if n >= 160:
        prev = [closes[i - 1] if i > 0 else closes[0] for i in range(n)]
        daily_ret = [closes[i] / max(prev[i], 0.01) - 1 for i in range(n)]
        recent = daily_ret[-160:]
        mean_ret = sum(recent) / len(recent) if recent else 0.0
        alpha = [value - mean_ret for value in recent]
        amps = [(highs[i] - lows[i]) / max(prev[i], 0.01) for i in range(n)]
        result['long_momentum'] = round(engine.cut(alpha, amps[-160:], 'low_minus_high', 0.3), 4)
    return result


def compute_all_factors(price, last_close, vol, b_vol, s_vol, bars):
    """Compute factor cutting theory factors + factorlab_score."""
    price = _safe_float(price)
    last_close = _safe_float(last_close)
    change_pct = (price - last_close) / last_close * 100 if last_close else 0.0
    raw = compute_raw_factors(bars)
    reversal_score = score_ideal_reversal(raw['ideal_reversal'])
    amplitude_score = score_ideal_amplitude(raw['ideal_amplitude'])
    momentum_score = score_long_momentum(raw['long_momentum'])
    factorlab_score = round(reversal_score * 0.35 + amplitude_score * 0.30 + momentum_score * 0.35, 2)
    features = {
        'factorlab_score': factorlab_score,
        'change_pct': round(change_pct, 2),
        'ideal_reversal': raw['ideal_reversal'],
        'ideal_reversal_score': reversal_score,
        'ideal_reversal_ok': '✅' if raw['ideal_reversal'] < -0.02 else '❌',
        'ideal_amplitude': raw['ideal_amplitude'],
        'ideal_amplitude_score': amplitude_score,
        'ideal_amplitude_ok': '✅' if raw['ideal_amplitude'] < -0.008 else '❌',
        'long_momentum': raw['long_momentum'],
        'long_momentum_score': momentum_score,
        'long_momentum_ok': '✅' if raw['long_momentum'] > 0.05 else '❌',
        'data_points': raw['data_points'],
        'signal': signal_for_score(factorlab_score),
        'signal_icon': signal_icon(factorlab_score),
        'volume': _safe_float(vol),
        'buy_volume': _safe_float(b_vol),
        'sell_volume': _safe_float(s_vol),
    }
    features['score_details'] = [
        f'理想反转 {raw["ideal_reversal"]:+.4f} -> {reversal_score}分 x 35%',
        f'理想振幅 {raw["ideal_amplitude"]:+.4f} -> {amplitude_score}分 x 30%',
        f'长端动量 {raw["long_momentum"]:+.4f} -> {momentum_score}分 x 35%',
        f'综合评分 {factorlab_score:.2f} -> {features["signal"]}',
    ]
    return features


# ── Buy recommendation engine ──────────────────────────────────

def generate_recommendation(factors, quote=None):
    """
    Generate a buy recommendation based solely on FactorLab score (因子切割论).

    Returns a dict with:
      - verdict: '强烈推荐买入' / '建议买入' / '观望' / '不建议买入'
      - confidence: 0-100
      - reasons: list of supporting reasons
      - risks: list of risk factors
      - action: specific action text
    """
    fl_score = factors.get('factorlab_score', 0)
    data_points = factors.get('data_points', 0)

    reasons = []
    risks = []

    # Factor analysis reasons
    if factors.get('ideal_reversal_ok') == '✅':
        reasons.append(f'理想反转因子 {factors["ideal_reversal"]:+.4f}，反转效应显著，低成交额组涨跌幅远高于高成交额组')
    else:
        risks.append(f'理想反转因子 {factors["ideal_reversal"]:+.4f} 未达阈值，反转效应不明显')

    if factors.get('ideal_amplitude_ok') == '✅':
        reasons.append(f'理想振幅因子 {factors["ideal_amplitude"]:+.4f}，高价股振幅小于低价股，符合理想振幅结构')
    else:
        risks.append(f'理想振幅因子 {factors["ideal_amplitude"]:+.4f} 未达阈值，振幅结构不理想')

    if factors.get('long_momentum_ok') == '✅':
        reasons.append(f'长端动量因子 {factors["long_momentum"]:+.4f}，低振幅日Alpha收益显著为正，动量持续性强')
    else:
        risks.append(f'长端动量因子 {factors["long_momentum"]:+.4f} 未达阈值，动量不足')

    # Count how many factors are positive
    positive_count = sum([
        1 if factors.get('ideal_reversal_ok') == '✅' else 0,
        1 if factors.get('ideal_amplitude_ok') == '✅' else 0,
        1 if factors.get('long_momentum_ok') == '✅' else 0,
    ])

    if positive_count == 3:
        reasons.append('三因子共振，多维度验证一致看多')
    elif positive_count == 0:
        risks.append('三因子均未达标，因子面全面偏空')

    change_pct = factors.get('change_pct', 0)
    if change_pct < -3:
        risks.append(f'当日跌幅 {change_pct:+.2f}%，短期承压')

    # Data sufficiency
    if data_points < 160:
        risks.append(f'历史数据仅 {data_points} 根K线，长端动量因子无法计算（需160根），评分可靠性降低')

    # Determine verdict based solely on factorlab_score
    if fl_score >= 80:
        verdict = '强烈推荐买入'
        confidence = min(95, int(fl_score + 10))
        action = '因子切割论三因子共振看多，可逢低布局'
    elif fl_score >= 65:
        verdict = '建议买入'
        confidence = min(80, int(fl_score))
        action = '因子评分偏多，可小仓位试探性买入，设好止损'
    elif fl_score >= 50:
        verdict = '观望'
        confidence = min(60, int(fl_score))
        action = '因子信号中性，建议等待更明确的买入信号'
    else:
        verdict = '不建议买入'
        confidence = min(90, int(100 - fl_score + 20))
        action = '因子评分偏低，风险大于收益，暂回避'

    return {
        'verdict': verdict,
        'confidence': confidence,
        'factorlab_score': fl_score,
        'reasons': reasons,
        'risks': risks,
        'action': action,
        'positive_factors': positive_count,
    }


# ── Data fetcher ───────────────────────────────────────────────

class RealtimeFetcher:
    def __init__(self, prefer_live=None):
        settings = load_settings()
        self.prefer_live = settings.get('use_live_data', True) if prefer_live is None else prefer_live
        self.config = load_config()
        self.api = None
        self.security_names = {}

    def connect(self):
        if not self.prefer_live:
            return False
        if self.api is not None:
            return True
        try:
            from pytdx.hq import TdxHq_API
        except Exception:
            return False
        for server in self.config.get('servers', []):
            api = TdxHq_API(raise_exception=False)
            try:
                ok = api.connect(server.get('ip'), int(server.get('port', 7709)), time_out=1.5)
            except Exception:
                ok = False
            if ok:
                self.api = api
                return True
        return False

    def disconnect(self):
        if self.api is not None:
            try:
                self.api.disconnect()
            except Exception:
                pass
        self.api = None

    def _market(self, code):
        code = str(code).zfill(6)
        if code.startswith(('5', '6', '9')):
            return 1
        return 0

    def get_stock_name(self, code):
        code = str(code).zfill(6)
        return self.security_names.get(code) or DEFAULT_NAMES.get(code, code)

    def get_quote(self, code):
        code = str(code).zfill(6)
        if self.connect():
            try:
                data = self.api.get_security_quotes([(self._market(code), code)])
                if data:
                    return self._normalize_quote(data[0], code)
            except Exception:
                pass
        return self._simulate_quote(code)

    def batch_quotes(self, codes):
        codes = [str(c).zfill(6) for c in codes]
        if not codes:
            return []
        if self.connect():
            results = []
            try:
                pairs = [(self._market(c), c) for c in codes]
                for start in range(0, len(pairs), 80):
                    chunk = pairs[start:start + 80]
                    data = self.api.get_security_quotes(chunk) or []
                    for item, code in zip(data, codes[start:start + len(data)]):
                        results.append(self._normalize_quote(item, code))
                found = {r.get('code') for r in results}
                for code in codes:
                    if code not in found:
                        results.append(self._simulate_quote(code))
                return results
            except Exception:
                pass
        return [self._simulate_quote(code) for code in codes]

    def get_kline(self, code, count=220):
        code = str(code).zfill(6)
        count = max(20, int(count))
        if self.connect():
            try:
                data = self.api.get_security_bars(9, self._market(code), code, 0, count) or []
                bars = [self._normalize_bar(item) for item in data]
                bars = [b for b in bars if b.get('c', 0) > 0]
                if len(bars) >= 20:
                    bars.sort(key=lambda b: b.get('date', ''))
                    return bars[-count:]
            except Exception:
                pass
        return self._simulate_bars(code, count)

    def _normalize_quote(self, item, code):
        price = float(item.get('price') or item.get('close') or 0)
        last_close = float(item.get('last_close') or item.get('pre_close') or price or 0)
        return {
            'code': str(item.get('code') or code).zfill(6),
            'name': self.get_stock_name(code),
            'price': price,
            'last_close': last_close,
            'change_pct': round((price - last_close) / last_close * 100, 2) if last_close else 0,
            'high': float(item.get('high') or price),
            'low': float(item.get('low') or price),
            'volume': float(item.get('vol') or item.get('volume') or 0),
            'amount': float(item.get('amount') or 0),
            'b_vol': float(item.get('b_vol') or 0),
            's_vol': float(item.get('s_vol') or 0),
            'time': datetime.now().strftime('%H:%M:%S'),
        }

    def _normalize_bar(self, item):
        year = int(item.get('year') or 1970)
        month = int(item.get('month') or 1)
        day = int(item.get('day') or 1)
        return {
            'date': f'{year:04d}-{month:02d}-{day:02d}',
            'o': float(item.get('open') or 0),
            'h': float(item.get('high') or 0),
            'l': float(item.get('low') or 0),
            'c': float(item.get('close') or 0),
            'v': float(item.get('vol') or item.get('volume') or 0),
            'a': float(item.get('amount') or 0),
        }

    def _seed(self, code):
        return sum((i + 1) * ord(ch) for i, ch in enumerate(str(code)))

    def _simulate_bars(self, code, count=220):
        rng = random.Random(self._seed(code))
        base = 4 + (self._seed(code) % 900) / 30
        price = base
        bars = []
        start = datetime.now() - timedelta(days=count * 2)
        for i in range(count):
            drift = 0.0006 * math.sin(i / 17) + rng.uniform(-0.018, 0.02)
            open_price = max(0.5, price * (1 + rng.uniform(-0.008, 0.008)))
            close_price = max(0.5, price * (1 + drift))
            high = max(open_price, close_price) * (1 + rng.uniform(0.003, 0.035))
            low = min(open_price, close_price) * (1 - rng.uniform(0.003, 0.03))
            volume = int(500000 + rng.random() * 5000000 + i * 800)
            amount = volume * close_price
            bars.append({
                'date': (start + timedelta(days=i)).strftime('%Y-%m-%d'),
                'o': round(open_price, 2), 'h': round(high, 2),
                'l': round(low, 2), 'c': round(close_price, 2),
                'v': volume, 'a': round(amount, 2),
            })
            price = close_price
        return bars

    def _simulate_quote(self, code):
        bars = self._simulate_bars(code, 220)
        last = bars[-2]['c'] if len(bars) > 1 else bars[-1]['c']
        price = bars[-1]['c']
        volume = bars[-1]['v']
        return {
            'code': str(code).zfill(6),
            'name': self.get_stock_name(code),
            'price': price, 'last_close': last,
            'change_pct': round((price - last) / last * 100, 2) if last else 0,
            'high': bars[-1]['h'], 'low': bars[-1]['l'],
            'volume': volume, 'amount': bars[-1]['a'],
            'b_vol': int(volume * 0.52), 's_vol': int(volume * 0.48),
            'time': datetime.now().strftime('%H:%M:%S'),
        }


# ── High-level analysis API ────────────────────────────────────

def analyze_stock(code, prefer_live=True):
    """
    Analyze a single stock and return full factor report + buy recommendation.

    Returns dict with keys:
      - code, name, price, change_pct
      - factors (all computed factors)
      - recommendation (verdict, confidence, reasons, risks, action)
      - data_source ('live' or 'simulated')
    """
    fetcher = RealtimeFetcher(prefer_live=prefer_live)
    code = str(code).strip().zfill(6)
    name = fetcher.get_stock_name(code)
    quote = fetcher.get_quote(code)
    bars = fetcher.get_kline(code, 220)
    fetcher.disconnect()

    if not quote or not bars:
        return {'error': f'无法获取 {code} 的数据'}

    factors = compute_all_factors(
        quote['price'], quote['last_close'],
        quote['volume'], quote.get('b_vol', 0), quote.get('s_vol', 0),
        bars,
    )
    recommendation = generate_recommendation(factors, quote)

    data_source = 'live' if fetcher.api is not None else 'simulated'

    return {
        'code': code,
        'name': name,
        'price': quote['price'],
        'change_pct': factors['change_pct'],
        'factors': factors,
        'recommendation': recommendation,
        'data_source': data_source,
        'analyze_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }


def batch_scan(codes=None, min_score=55, top_k=30, prefer_live=True):
    """
    Batch scan multiple stocks, return ranked results.

    Args:
        codes: list of stock codes. If None, uses DEFAULT_POOL.
        min_score: minimum factorlab_score to include.
        top_k: return top K results.
        prefer_live: use live data if available.

    Returns list of dicts with code, name, score, factors, recommendation.
    """
    if codes is None:
        codes = DEFAULT_POOL

    fetcher = RealtimeFetcher(prefer_live=prefer_live)
    pool = [str(c).strip().zfill(6) for c in codes if str(c).strip()]
    quotes = fetcher.batch_quotes(pool)

    results = []
    for quote in quotes:
        code = quote.get('code', '')
        bars = fetcher.get_kline(code, 220)
        factors = compute_all_factors(
            quote.get('price', 0), quote.get('last_close', 0),
            quote.get('volume', 0), quote.get('b_vol', 0), quote.get('s_vol', 0),
            bars,
        )
        fl_score = factors.get('factorlab_score', 0)
        if fl_score >= min_score:
            rec = generate_recommendation(factors, quote)
            results.append({
                'code': code,
                'name': fetcher.get_stock_name(code) or quote.get('name', code),
                'price': quote.get('price', 0),
                'change_pct': factors.get('change_pct', 0),
                'factorlab_score': fl_score,
                'signal': factors.get('signal', ''),
                'recommendation': rec,
            })

    fetcher.disconnect()
    results.sort(key=lambda r: r.get('factorlab_score', 0), reverse=True)
    return results[:top_k]
