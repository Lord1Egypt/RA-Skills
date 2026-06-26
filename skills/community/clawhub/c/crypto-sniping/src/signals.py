"""Technical analysis signal generation."""
import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class SignalType(Enum):
    BUY = "buy"
    SELL = "sell"
    HOLD = "hold"

@dataclass
class Signal:
    type: SignalType
    confidence: int  # 1-5 scale
    indicators: List[str]
    price: float
    timestamp: int

class TechnicalAnalyzer:
    """Generate trading signals from technical indicators."""
    
    def __init__(self, rsi_period: int = 14, 
                 macd_fast: int = 12, macd_slow: int = 26, macd_signal: int = 9,
                 bb_period: int = 20, bb_std: float = 2.0):
        self.rsi_period = rsi_period
        self.macd_fast = macd_fast
        self.macd_slow = macd_slow
        self.macd_signal = macd_signal
        self.bb_period = bb_period
        self.bb_std = bb_std
    
    def _calculate_rsi(self, closes: np.ndarray) -> float:
        """Calculate RSI."""
        if len(closes) < self.rsi_period + 1:
            return 50.0
        
        deltas = np.diff(closes)
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        
        avg_gains = np.mean(gains[-self.rsi_period:])
        avg_losses = np.mean(losses[-self.rsi_period:])
        
        if avg_losses == 0:
            return 100.0
        
        rs = avg_gains / avg_losses
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def _calculate_macd(self, closes: np.ndarray) -> Tuple[float, float, float]:
        """Calculate MACD line, signal line, and histogram."""
        if len(closes) < self.macd_slow + self.macd_signal:
            return 0.0, 0.0, 0.0
        
        ema_fast = self._calculate_ema(closes, self.macd_fast)
        ema_slow = self._calculate_ema(closes, self.macd_slow)
        
        macd_line = ema_fast - ema_slow
        signal_line = self._calculate_ema(np.array([macd_line]), self.macd_signal)
        histogram = macd_line - signal_line
        
        return macd_line, signal_line, histogram
    
    def _calculate_ema(self, data: np.ndarray, period: int) -> float:
        """Calculate EMA."""
        if len(data) < period:
            return data[-1] if len(data) > 0 else 0.0
        
        alpha = 2 / (period + 1)
        ema = data[0]
        for price in data[1:]:
            ema = alpha * price + (1 - alpha) * ema
        return ema
    
    def _calculate_bollinger_bands(self, closes: np.ndarray) -> Tuple[float, float, float]:
        """Calculate Bollinger Bands."""
        if len(closes) < self.bb_period:
            middle = closes[-1] if len(closes) > 0 else 0.0
            return middle, middle, middle
        
        sma = np.mean(closes[-self.bb_period:])
        std = np.std(closes[-self.bb_period:])
        
        upper = sma + (self.bb_std * std)
        lower = sma - (self.bb_std * std)
        
        return upper, sma, lower
    
    def _calculate_volume_spike(self, volumes: np.ndarray) -> float:
        """Calculate volume spike ratio (current vs average)."""
        if len(volumes) < 20:
            return 1.0
        
        current_volume = volumes[-1]
        avg_volume = np.mean(volumes[-20:-1])
        
        if avg_volume == 0:
            return 1.0
        
        return current_volume / avg_volume
    
    def _detect_support_resistance(self, highs: np.ndarray, lows: np.ndarray, 
                                    closes: np.ndarray, lookback: int = 20) -> Tuple[float, float]:
        """Detect support and resistance levels."""
        if len(closes) < lookback:
            return closes[-1] * 0.95, closes[-1] * 1.05 if len(closes) > 0 else (0, 0)
        
        recent_highs = highs[-lookback:]
        recent_lows = lows[-lookback:]
        
        resistance = np.max(recent_highs)
        support = np.min(recent_lows)
        
        return support, resistance
    
    def analyze(self, klines: List[List]) -> Signal:
        """Generate trading signal from kline data."""
        if len(klines) < 50:
            return Signal(SignalType.HOLD, 0, [], 0.0, 0)
        
        # Parse klines: [timestamp, open, high, low, close, volume, ...]
        timestamps = np.array([k[0] for k in klines])
        opens = np.array([float(k[1]) for k in klines])
        highs = np.array([float(k[2]) for k in klines])
        lows = np.array([float(k[3]) for k in klines])
        closes = np.array([float(k[4]) for k in klines])
        volumes = np.array([float(k[5]) for k in klines])
        
        current_price = closes[-1]
        
        # Calculate indicators
        rsi = self._calculate_rsi(closes)
        macd_line, signal_line, macd_hist = self._calculate_macd(closes)
        bb_upper, bb_middle, bb_lower = self._calculate_bollinger_bands(closes)
        volume_spike = self._calculate_volume_spike(volumes)
        support, resistance = self._detect_support_resistance(highs, lows, closes)
        
        # Generate signals
        buy_signals = []
        sell_signals = []
        
        # RSI signals
        if rsi < 30:
            buy_signals.append("RSI_OVERSOLD")
        elif rsi > 70:
            sell_signals.append("RSI_OVERBOUGHT")
        
        # MACD signals
        if macd_hist > 0 and macd_hist > (macd_line * 0.1):  # Positive and growing
            buy_signals.append("MACD_BULLISH")
        elif macd_hist < 0:
            sell_signals.append("MACD_BEARISH")
        
        # Bollinger Band signals
        if current_price < bb_lower:
            buy_signals.append("BB_OVERSOLD")
        elif current_price > bb_upper:
            sell_signals.append("BB_OVERBOUGHT")
        
        # Volume spike
        if volume_spike > 2.0:
            if closes[-1] > closes[-2]:  # Price going up with volume
                buy_signals.append(f"VOLUME_SPIKE_{volume_spike:.1f}x")
            else:
                sell_signals.append(f"VOLUME_SPIKE_{volume_spike:.1f}x")
        
        # Support/Resistance bounce
        if current_price <= support * 1.02:  # Within 2% of support
            buy_signals.append("SUPPORT_BOUNCE")
        elif current_price >= resistance * 0.98:  # Within 2% of resistance
            sell_signals.append("RESISTANCE_REJECT")
        
        # EMA crossover (simple 9/21)
        ema_9 = self._calculate_ema(closes, 9)
        ema_21 = self._calculate_ema(closes, 21)
        if ema_9 > ema_21 * 1.005:  # Golden cross with buffer
            buy_signals.append("EMA_GOLDEN_CROSS")
        elif ema_9 < ema_21 * 0.995:
            sell_signals.append("EMA_DEATH_CROSS")
        
        # Determine final signal
        confidence = 0
        indicators = []
        signal_type = SignalType.HOLD
        
        if len(buy_signals) > len(sell_signals):
            confidence = min(len(buy_signals), 5)
            indicators = buy_signals
            signal_type = SignalType.BUY
        elif len(sell_signals) > len(buy_signals):
            confidence = min(len(sell_signals), 5)
            indicators = sell_signals
            signal_type = SignalType.SELL
        
        return Signal(
            type=signal_type,
            confidence=confidence,
            indicators=indicators,
            price=current_price,
            timestamp=int(timestamps[-1])
        )
    
    def get_indicator_values(self, klines: List[List]) -> Dict:
        """Get current indicator values for display."""
        if len(klines) < 50:
            return {}
        
        closes = np.array([float(k[4]) for k in klines])
        highs = np.array([float(k[2]) for k in klines])
        lows = np.array([float(k[3]) for k in klines])
        volumes = np.array([float(k[5]) for k in klines])
        
        return {
            "rsi": round(self._calculate_rsi(closes), 2),
            "macd": round(self._calculate_macd(closes)[0], 4),
            "macd_signal": round(self._calculate_macd(closes)[1], 4),
            "bb_upper": round(self._calculate_bollinger_bands(closes)[0], 2),
            "bb_middle": round(self._calculate_bollinger_bands(closes)[1], 2),
            "bb_lower": round(self._calculate_bollinger_bands(closes)[2], 2),
            "volume_spike": round(self._calculate_volume_spike(volumes), 2),
            "ema_9": round(self._calculate_ema(closes, 9), 2),
            "ema_21": round(self._calculate_ema(closes, 21), 2),
            "support": round(self._detect_support_resistance(highs, lows, closes)[0], 2),
            "resistance": round(self._detect_support_resistance(highs, lows, closes)[1], 2),
            "price": round(closes[-1], 2)
        }
