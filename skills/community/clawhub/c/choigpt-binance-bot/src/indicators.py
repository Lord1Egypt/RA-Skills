import pandas as pd
import numpy as np
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Union

# --- 데이터 클래스 정의 (src/strategy.py 호환용) ---

@dataclass
class MarketStructure:
    trend: str = "NEUTRAL"  # BULLISH, BEARISH, NEUTRAL
    structure_type: str = "NONE"  # BOS, MSS, CHOCH
    broken_level: float = 0.0
    is_confirmed: bool = False

@dataclass
class FVG:
    type: str  # BULLISH, BEARISH
    top: float
    bottom: float
    is_mitigated: bool = False
    mitigated_price: float = 0.0

@dataclass
class OrderBlock:
    type: str  # BULLISH, BEARISH
    top: float
    bottom: float
    volume: float = 0.0
    is_mitigated: bool = False

@dataclass
class BreakerBlock:
    type: str
    top: float
    bottom: float

@dataclass
class LiquidityLevel:
    type: str  # BSL, SSL
    price: float
    is_swept: bool = False

@dataclass
class BPR:  # Balanced Price Range
    top: float
    bottom: float

@dataclass
class RejectionBlock:
    type: str
    top: float
    bottom: float

@dataclass
class RangeBox:
    top: float
    bottom: float
    label: str = ""

@dataclass
class Neckline:
    price: float
    type: str = "HORIZONTAL"

@dataclass
class TradeSignal:
    direction: str  # LONG, SHORT
    entry_price: float
    stop_loss: float
    take_profit: float
    take_profit2: Optional[float] = None
    confidence: float = 0.0
    reasons: List[str] = field(default_factory=list)
    leverage: int = 10
    mode: str = "SCALPING"  # SWEEPZONE, SCALPING, etc.
    entry_type: str = "MARKET"  # MARKET, LIMIT

# --- 기초 지표 함수 ---

def calculate_ma(df, period=20):
    """이동평균 및 기울기 계산"""
    df[f'ma{period}'] = df['close'].rolling(window=period).mean()
    df[f'ma{period}_slope'] = df[f'ma{period}'].diff()
    return df

def calculate_ma20(df):
    return df['close'].rolling(window=20).mean()

def calculate_rsi(df, period=14):
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def calculate_atr(df, period=14):
    high_low = df['high'] - df['low']
    high_close = np.abs(df['high'] - df['close'].shift())
    low_close = np.abs(df['low'] - df['close'].shift())
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = np.max(ranges, axis=1)
    return true_range.rolling(window=period).mean()

def calculate_ichimoku(df, n1=9, n2=26, n3=52):
    """일목균형표 계산"""
    high_9 = df['high'].rolling(window=n1).max()
    low_9 = df['low'].rolling(window=n1).min()
    df['tenkan_sen'] = (high_9 + low_9) / 2

    high_26 = df['high'].rolling(window=n2).max()
    low_26 = df['low'].rolling(window=n2).min()
    df['kijun_sen'] = (high_26 + low_26) / 2

    df['senkou_span_a'] = ((df['tenkan_sen'] + df['kijun_sen']) / 2).shift(n2)
    high_52 = df['high'].rolling(window=n3).max()
    low_52 = df['low'].rolling(window=n3).min()
    df['senkou_span_b'] = ((high_52 + low_52) / 2).shift(n2)

    df['chikou_span'] = df['close'].shift(-n2)
    df['kumo_top'] = df[['senkou_span_a', 'senkou_span_b']].max(axis=1)
    df['kumo_bottom'] = df[['senkou_span_a', 'senkou_span_b']].min(axis=1)
    
    return {
        'tenkan': df['tenkan_sen'].iloc[-1],
        'kijun': df['kijun_sen'].iloc[-1],
        'senkou_a': df['senkou_span_a'].iloc[-1],
        'senkou_b': df['senkou_span_b'].iloc[-1],
        'cloud_top': df['kumo_top'].iloc[-1],
        'cloud_bottom': df['kumo_bottom'].iloc[-1]
    }

def calculate_mfi(df, period=14):
    typical_price = (df['high'] + df['low'] + df['close']) / 3
    money_flow = typical_price * df['volume']
    positive_flow = money_flow.where(typical_price > typical_price.shift(1), 0).rolling(window=period).sum()
    negative_flow = money_flow.where(typical_price < typical_price.shift(1), 0).rolling(window=period).sum()
    mfr = positive_flow / negative_flow
    return 100 - (100 / (1 + mfr))

def calculate_wavetrend(df, n1=10, n2=21):
    ap = (df['high'] + df['low'] + df['close']) / 3
    esa = ap.ewm(span=n1).mean()
    d = (ap - esa).abs().ewm(span=n1).mean()
    ci = (ap - esa) / (0.015 * d)
    tci = ci.ewm(span=n2).mean()
    wt1 = tci
    wt2 = wt1.rolling(window=4).mean()
    return {'wt1': wt1.iloc[-1], 'wt2': wt2.iloc[-1], 'cross': wt1.iloc[-1] > wt2.iloc[-1]}

# --- SMC/ICT 스텁 함수 (Import Error 방지용 최소 구현) ---

def detect_market_structure(df) -> MarketStructure:
    """간소화된 추세 판단"""
    if len(df) < 20: return MarketStructure()
    ma20 = df['close'].rolling(20).mean()
    if df['close'].iloc[-1] > ma20.iloc[-1]:
        return MarketStructure(trend="BULLISH")
    elif df['close'].iloc[-1] < ma20.iloc[-1]:
        return MarketStructure(trend="BEARISH")
    return MarketStructure(trend="NEUTRAL")

def get_premium_discount_zone(df): return {"zone": "DISCOUNT" if df['close'].iloc[-1] < df['close'].mean() else "PREMIUM"}
def find_fvg(df) -> List[FVG]: return []
def find_ifvg(df) -> List[FVG]: return []
def find_order_blocks(df) -> List[OrderBlock]: return []
def find_breaker_blocks(df) -> List[BreakerBlock]: return []
def find_liquidity_levels(df) -> List[LiquidityLevel]: return []
def find_bpr(df) -> List[BPR]: return []
def find_rejection_blocks(df) -> List[RejectionBlock]: return []
def find_draw_on_liquidity(df): return {"target": 0.0}
def get_current_session(): return {"session": "NY"}
def analyze_monday_range(df): return {"high": 0.0, "low": 0.0}
def detect_bj_boxes(df) -> List[RangeBox]: return []
def detect_necklines(df) -> List[Neckline]: return []
def detect_liquidity_sweep(df): return {"swept": False}
def detect_smt_divergence(df1, df2): return {"divergence": False}
def detect_displacement(df): return {"detected": False}
def detect_cisd(df): return {"detected": False}
def calculate_ote_levels(df): return {"62%": 0.0, "70.5%": 0.0, "79%": 0.0}

def check_sweepzone_v1(df):
    """Sweepzone V1 조건 체크"""
    if len(df) < 52:
        return False, "Not enough data"
    
    # 지표 계산
    df = calculate_ma(df, 20)
    ichimoku = calculate_ichimoku(df)
    
    last = df.iloc[-1]
    
    # 1. 20MA 조건: 가격이 20MA 위 & 20MA 상승 중
    cond_ma = (last['close'] > last['ma20']) and (last['ma20_slope'] > 0)
    # 2. Ichimoku 조건: 가격이 구름대(Kumo) 위에 위치
    cond_kumo = last['close'] > ichimoku['cloud_top']
    
    is_signal = cond_ma and cond_kumo
    reason = f"MA:{cond_ma}, Kumo:{cond_kumo}"
    return is_signal, reason