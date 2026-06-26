"""
ChoiGPT Technical Analysis Engine
=================================
스캘핑 고수들이 사용하는 핵심 기술적 지표 모듈
- RSI (과매수/과매도)
- Bollinger Bands (변동성 + 평균회귀)
- 이동평균선 (골든크로스/데드크로스)
- MACD (추세 전환)
"""
import requests
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime

logger = logging.getLogger("TechnicalAnalysis")


class TechnicalAnalyzer:
    """빗썸 캔들 데이터 기반 기술적 분석 엔진"""

    def __init__(self):
        self.cache = {}

    # ═══════════════════════════════════════════════════════════
    # 캔들 데이터 수집
    # ═══════════════════════════════════════════════════════════
    def get_candles(self, symbol: str, interval: str = "5m", count: int = 100) -> List[dict]:
        """
        빗썸 캔들스틱 데이터 조회
        interval: 1m, 3m, 5m, 10m, 30m, 1h, 6h, 12h, 24h
        """
        try:
            url = f"https://api.bithumb.com/public/candlestick/{symbol}_KRW/{interval}"
            resp = requests.get(url, timeout=10)
            data = resp.json()
            if data.get("status") != "0000":
                return []

            candles = []
            for c in data["data"][-count:]:
                candles.append({
                    "timestamp": c[0],
                    "open": float(c[1]),
                    "close": float(c[2]),
                    "high": float(c[3]),
                    "low": float(c[4]),
                    "volume": float(c[5])
                })
            return candles
        except Exception as e:
            logger.error(f"캔들 데이터 조회 실패 ({symbol}): {e}")
            return []

    # ═══════════════════════════════════════════════════════════
    # RSI (Relative Strength Index) - 과매수/과매도 판별
    # ═══════════════════════════════════════════════════════════
    def calc_rsi(self, closes: List[float], period: int = 14) -> float:
        """
        RSI 계산
        - 30 이하: 과매도 → 매수 시그널
        - 70 이상: 과매수 → 매도 시그널
        - 30~70: 중립
        """
        if len(closes) < period + 1:
            return 50.0  # 데이터 부족 시 중립

        gains = []
        losses = []
        for i in range(1, len(closes)):
            diff = closes[i] - closes[i - 1]
            gains.append(max(diff, 0))
            losses.append(max(-diff, 0))

        avg_gain = sum(gains[:period]) / period
        avg_loss = sum(losses[:period]) / period

        # Wilder's Smoothing
        for i in range(period, len(gains)):
            avg_gain = (avg_gain * (period - 1) + gains[i]) / period
            avg_loss = (avg_loss * (period - 1) + losses[i]) / period

        if avg_loss == 0:
            return 100.0
        rs = avg_gain / avg_loss
        return round(100 - (100 / (1 + rs)), 2)

    # ═══════════════════════════════════════════════════════════
    # Bollinger Bands - 변동성 밴드
    # ═══════════════════════════════════════════════════════════
    def calc_bollinger(self, closes: List[float], period: int = 20, std_dev: float = 2.0) -> Dict:
        """
        볼린저 밴드 계산
        - 하단 밴드 터치: 매수 시그널 (평균 회귀 기대)
        - 상단 밴드 터치: 매도 시그널
        - 밴드 폭 축소: 큰 변동 임박 (스퀴즈)
        """
        if len(closes) < period:
            return {"upper": 0, "middle": 0, "lower": 0, "width": 0}

        recent = closes[-period:]
        middle = sum(recent) / period
        variance = sum((x - middle) ** 2 for x in recent) / period
        std = variance ** 0.5

        upper = middle + (std_dev * std)
        lower = middle - (std_dev * std)
        width = ((upper - lower) / middle) * 100  # 밴드 폭 (%)

        return {
            "upper": round(upper, 2),
            "middle": round(middle, 2),
            "lower": round(lower, 2),
            "width": round(width, 2)
        }

    # ═══════════════════════════════════════════════════════════
    # EMA 9/21 (고수 기법) & VWAP & MTF
    # ═══════════════════════════════════════════════════════════
    def detect_ema_cross(self, closes: List[float],
                         short_period: int = 9, long_period: int = 21) -> str:
        """EMA 골든크로스 / 데드크로스 감지"""
        if len(closes) < long_period + 2:
            return "NONE"
            
        short_emas = self.calc_ema(closes, short_period)
        long_emas = self.calc_ema(closes, long_period)
        
        if len(short_emas) < 2 or len(long_emas) < 2:
            return "NONE"

        current_short, prev_short = short_emas[-1], short_emas[-2]
        current_long, prev_long = long_emas[-1], long_emas[-2]

        if prev_short <= prev_long and current_short > current_long:
            return "GOLDEN"
        elif prev_short >= prev_long and current_short < current_long:
            return "DEAD"
        return "NONE"

    def calc_vwap(self, candles: List[dict]) -> float:
        """VWAP (Volume Weighted Average Price) 계산"""
        total_value = 0.0
        total_volume = 0.0
        for c in candles:
            typical_price = (c["high"] + c["low"] + c["close"]) / 3
            total_value += typical_price * c["volume"]
            total_volume += c["volume"]
        return round(total_value / total_volume, 2) if total_volume else 0.0

    def check_mtf_trend(self, symbol: str) -> str:
        """1시간봉 기반 Multi-Timeframe Filter"""
        candles = self.get_candles(symbol, "1h", 30)
        if len(candles) < 22:
            return "NEUTRAL"
        closes = [c["close"] for c in candles]
        ema9 = self.calc_ema(closes, 9)[-1]
        ema21 = self.calc_ema(closes, 21)[-1]
        return "UPTREND" if ema9 > ema21 else "DOWNTREND"

    # ═══════════════════════════════════════════════════════════
    def calc_ema(self, closes: List[float], period: int) -> List[float]:
        """지수이동평균(EMA) 계산"""
        if len(closes) < period:
            return []
        
        ema = [sum(closes[:period]) / period]  # 첫 값은 SMA로 시작
        multiplier = 2 / (period + 1)
        
        for i in range(period, len(closes)):
            val = (closes[i] - ema[-1]) * multiplier + ema[-1]
            ema.append(val)
        return ema

    def calc_macd(self, closes: List[float], fast: int = 12, slow: int = 26, signal: int = 9) -> Dict:
        """MACD 계산 (추세 전환 확인)"""
        if len(closes) < slow + signal:
            return {"macd": 0, "signal": 0, "hist": 0}

        fast_ema = self.calc_ema(closes, fast)
        slow_ema = self.calc_ema(closes, slow)

        # 길이를 맞춤 (EMA는 첫 period 이후부터 계산됨)
        macd_line = []
        for i in range(len(slow_ema)):
            # slow_ema는 slow-1 인덱스부터 시작, fast_ema는 fast-1 인덱스부터 시작
            # 매칭되는 원본 데이터 인덱스는 i + slow - 1
            # fast_ema에서 해당 인덱스의 값은 fast_ema[i + slow - fast]
            macd_line.append(fast_ema[i + (slow - fast)] - slow_ema[i])

        signal_line = self.calc_ema(macd_line, signal)
        
        if not signal_line:
            return {"macd": 0, "signal": 0, "hist": 0}

        return {
            "macd": round(macd_line[-1], 2),
            "signal": round(signal_line[-1], 2),
            "hist": round(macd_line[-1] - signal_line[-1], 2)
        }

    # Bison Methodology (SMC/ICT) 핵심 지표
    # ═══════════════════════════════════════════════════════════
    def calc_sma(self, closes: List[float], period: int) -> List[float]:
        """단순이동평균(SMA) 계산"""
        if len(closes) < period:
            return []
        sma = []
        for i in range(len(closes) - period + 1):
            sma.append(sum(closes[i:i + period]) / period)
        return sma

    def detect_mss(self, candles: List[dict]) -> str:
        """
        Market Structure Shift (시장 구조 전환) 감지 - Professional Version
        최근 하락 추세 중 마지막 Swing High를 종가로 돌파할 때 (Bullish MSS)
        """
        if len(candles) < 20:
            return "NONE"
            
        # 1. 최근 20캔들 내에서 Swing High/Low 식별 (간이)
        highs = [c["high"] for c in candles]
        lows = [c["low"] for c in candles]
        
        # 최근 5-15캔들 사이의 최고점 (전고점)
        swing_high = max(highs[-15:-5])
        # 최근 5-15캔들 사이의 최저점 (전저점)
        swing_low = min(lows[-15:-5])
        
        curr_close = candles[-1]["close"]
        
        # 하락 추세 중 전고점 돌파 (Bullish MSS)
        if curr_close > swing_high:
            return "BULLISH_MSS"
        # 상승 추세 중 전저점 이탈 (Bearish MSS)
        elif curr_close < swing_low:
            return "BEARISH_MSS"
            
        return "NONE"

    def detect_fvg(self, candles: List[dict]) -> List[dict]:
        """
        Fair Value Gap (FVG) 감지 - Freshness check 포함
        """
        if len(candles) < 5:
            return []
            
        fvgs = []
        # 최근 3개 캔들 조합들을 검사
        for i in range(len(candles) - 3):
            c1, c2, c3 = candles[i], candles[i+1], candles[i+2]
            
            # Bullish FVG (Gap Up)
            if c1["high"] < c3["low"]:
                # 현재가(candles[-1])가 아직 이 갭을 메우지 않았는지 확인
                if candles[-1]["low"] > c1["high"]:
                    fvgs.append({
                        "type": "BULLISH",
                        "top": c3["low"],
                        "bottom": c1["high"],
                        "fresh": True
                    })
            # Bearish FVG (Gap Down)
            elif c1["low"] > c3["high"]:
                if candles[-1]["high"] < c1["low"]:
                    fvgs.append({
                        "type": "BEARISH",
                        "top": c1["low"],
                        "bottom": c3["high"],
                        "fresh": True
                    })
        return fvgs

    # ═══════════════════════════════════════════════════════════
    # 종합 분석 (모든 지표 통합 판단) - Bison Edition
    # ═══════════════════════════════════════════════════════════
    def analyze(self, symbol: str, candles: List[dict] = None) -> Dict:
        """
        종목에 대한 종합 기술적 분석 실행 (Bison Methodology 기반)
        """
        # 캔들이 전달되지 않았으면 직접 조회
        if candles is None:
            candles = self.get_candles(symbol, "5m", 250)
            
        if not candles or len(candles) < 200:
            return {"verdict": "HOLD", "score": 0, "reason": "데이터 부족 (SMA 200 필요)"}

        closes = [c["close"] for c in candles]
        current_price = closes[-1]

        # 1. SMA 20 / 200 (추세 필터)
        sma20_list = self.calc_sma(closes, 20)
        sma200_list = self.calc_sma(closes, 200)
        sma20 = sma20_list[-1] if sma20_list else 0
        sma200 = sma200_list[-1] if sma200_list else 0
        
        # 2. MSS & FVG (Bison 핵심)
        mss = self.detect_mss(candles)
        fvgs = self.detect_fvg(candles[-10:]) # 최근 10캔들 내 FVG
        
        # 3. 보조 지표 (RSI, Bollinger)
        rsi = self.calc_rsi(closes)
        bb = self.calc_bollinger(closes)
        macd = self.calc_macd(closes)

        # ─── 종합 점수 계산 (Bison Score) ───────────────────
        score = 0
        reasons = []

        # [Bison Rule 1] SMA 200 위에서만 매수 (필수)
        if current_price < sma200:
            score -= 100
            reasons.append("BISON: SMA 200 하회 (역배열 매수 금지)")
        else:
            score += 20
            reasons.append("BISON: SMA 200 상회 (상승장 확인)")

        # [Bison Rule 2] SMA 20 지지/돌파
        if current_price > sma20:
            score += 15
            reasons.append("BISON: SMA 20 위 (단기 추세 우상향)")
        
        # [Bison Rule 3] MSS 감지 (강력 가점)
        if mss == "BULLISH_MSS":
            score += 40
            reasons.append("BISON: 시장 구조 전환(MSS) 감지! (상승 전환)")
        
        # [Bison Rule 4] FVG 존재 (미체결 불균형)
        bullish_fvgs = [f for f in fvgs if f["type"] == "BULLISH"]
        if bullish_fvgs:
            score += 15
            reasons.append(f"BISON: FVG {len(bullish_fvgs)}개 존재 (유동성 유입)")

        # 보조 점수 (RSI)
        if rsi <= 40:
            score += 10
            reasons.append(f"RSI {rsi} 낮음")
        elif rsi >= 70:
            score -= 30
            reasons.append(f"RSI {rsi} 과매수")

        # ─── 최종 판단 ────────────────────────────────────
        if score >= 50:
            verdict = "BUY"
        elif score <= -50:
            verdict = "SELL"
        else:
            verdict = "HOLD"

        return {
            "symbol": symbol,
            "verdict": verdict,
            "score": score,
            "reasons": reasons,
            "indicators": {
                "rsi": rsi,
                "sma20": round(sma20, 2),
                "sma200": round(sma200, 2),
                "mss": mss,
                "fvg_count": len(fvgs),
                "macd": macd,
                "current_price": current_price
            }
        }


# ═══════════════════════════════════════════════════════════════
# 테스트 실행
# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    ta = TechnicalAnalyzer()
    # 비트코인 분석
    result = ta.analyze("BTC")
    print(f"\n{'='*50}")
    print(f"  {result['symbol']} Bison Technical Analysis")
    print(f"{'='*50}")
    print(f"  판정: {result['verdict']} (점수: {result['score']})")
    print(f"\n  [판단 근거]")
    for r in result['reasons']:
        print(f"  → {r}")
    print(f"\n  [지표 상세]")
    print(f"  SMA 20: {result['indicators']['sma20']:,.0f} / SMA 200: {result['indicators']['sma200']:,.0f}")
    print(f"  MSS: {result['indicators']['mss']} / FVG: {result['indicators']['fvg_count']}개")
