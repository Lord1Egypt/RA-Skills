"""可插拔策略框架 - 10 种策略 + 参数优化支持"""
from __future__ import annotations
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Type, Any
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)

@dataclass
class RawSignal:
    strategy_name: str
    direction: str
    confidence: float
    reason: str
    metadata: Dict = None
    def __post_init__(self):
        if self.metadata is None: self.metadata = {}

@dataclass
class StrategyParams:
    """策略参数基类"""
    vol_multiplier: float = 1.8
    rsi_threshold: int = 30
    ma_period: int = 20
    boll_squeeze_ratio: float = 0.95
    kdj_threshold: int = 50
    obv_ma_period: int = 5
    support_tolerance: float = 0.02
    momentum_period: int = 10

    def to_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}

_REGISTRY: Dict[str, Type["Strategy"]] = {}

def register(cls: Type["Strategy"]) -> Type["Strategy"]:
    _REGISTRY[cls.name] = cls; return cls

def get_all_strategies() -> List["Strategy"]:
    return [cls() for cls in _REGISTRY.values()]

def get_strategy(name: str) -> Optional["Strategy"]:
    cls = _REGISTRY.get(name); return cls() if cls else None

def get_strategy_names() -> List[str]:
    return list(_REGISTRY.keys())


class StrategyCalibrator:
    """策略参数校准器 - 基于历史K线自动搜索最优阈值"""

    # 各策略可校准参数及其搜索空间
    PARAM_SPACES = {
        "rsi_oversold": {
            "rsi_threshold": [20, 25, 28, 30, 33, 35, 40],
        },
        "kdj_cross": {
            "kdj_threshold": [30, 35, 40, 45, 50, 55, 60],
        },
        "ma_breakout": {
            "vol_multiplier": [1.2, 1.4, 1.6, 1.8, 2.0, 2.3],
        },
        "boll_squeeze": {
            "boll_squeeze_ratio": [0.90, 0.92, 0.94, 0.95, 0.97, 0.99],
        },
        "double_ma": {
            "vol_multiplier": [1.0, 1.2, 1.3, 1.5, 1.8],
        },
        "support_bounce": {
            "support_tolerance": [0.01, 0.015, 0.02, 0.025, 0.03],
        },
        "volume_shrink": {
            "vol_multiplier": [0.5, 0.6, 0.7, 0.8, 0.9],
        },
    }

    @staticmethod
    def calibrate(df: pd.DataFrame, strategy_name: str = None,
                  hold_days: int = 5, target_rate: float = 0.06,
                  stop_loss_rate: float = -0.04,
                  regime: str = None) -> Dict[str, Any]:
        """校准策略参数（支持按市场状态分别校准）

        Args:
            df: 历史K线数据（需含技术指标）
            strategy_name: 指定策略名，None则校准所有可校准策略
            hold_days: 持仓天数
            target_rate: 止盈率
            stop_loss_rate: 止损率
            regime: 市场状态(trend/range/volatile)，None则全量校准

        Returns:
            {strategy_name: {best_params, best_score, trials, regime}}
        """
        if len(df) < 150:
            return {}

        # 按市场状态切分数据
        if regime:
            df = StrategyCalibrator._filter_by_regime(df, regime)
            if len(df) < 100:
                return {}

        target_strategies = [strategy_name] if strategy_name else list(StrategyCalibrator.PARAM_SPACES.keys())
        results = {}

        for strat_name in target_strategies:
            if strat_name not in _REGISTRY or strat_name not in StrategyCalibrator.PARAM_SPACES:
                continue

            space = StrategyCalibrator.PARAM_SPACES[strat_name]
            strategy = _REGISTRY[strat_name]()
            best_score = -np.inf
            best_params = {}
            trials = []

            param_combos = StrategyCalibrator._generate_combos(space)

            for params in param_combos:
                score = StrategyCalibrator._evaluate_params(
                    strategy, df, params, hold_days, target_rate, stop_loss_rate
                )
                trials.append({"params": params, "score": score})
                if score > best_score:
                    best_score = score
                    best_params = params.copy()

            if best_score > 0:
                results[strat_name] = {
                    "best_params": best_params,
                    "best_score": round(best_score, 4),
                    "trials": len(trials),
                    "regime": regime or "all",
                }

        return results

    @staticmethod
    def _filter_by_regime(df: pd.DataFrame, regime: str) -> pd.DataFrame:
        """按市场状态过滤K线数据"""
        close = df["close"].astype(float)
        returns = close.pct_change().dropna()
        volatility = returns.rolling(20).std()
        ma20 = close.rolling(20).mean()
        ma60 = close.rolling(60).mean()

        mask = pd.Series(True, index=df.index)

        if regime == "trend":
            mask = (close > ma20) & (ma20 > ma60)
        elif regime == "range":
            vol_median = volatility.median()
            mask = volatility < vol_median
        elif regime == "volatile":
            vol_median = volatility.median()
            mask = volatility >= vol_median

        return df[mask].reset_index(drop=True)

    @staticmethod
    def calibrate_all_regimes(df: pd.DataFrame, **kwargs) -> Dict[str, Dict]:
        """校准所有市场状态的最优参数"""
        all_results = {}
        for regime in ["trend", "range", "volatile"]:
            results = StrategyCalibrator.calibrate(df, regime=regime, **kwargs)
            for strat_name, result in results.items():
                if strat_name not in all_results:
                    all_results[strat_name] = {}
                all_results[strat_name][regime] = result
        return all_results

    @staticmethod
    def apply_calibrated(df: pd.DataFrame) -> Dict[str, Dict]:
        """校准并应用最优参数到策略实例，返回校准结果"""
        cal_results = StrategyCalibrator.calibrate(df)
        applied = {}
        for strat_name, result in cal_results.items():
            strategy = get_strategy(strat_name)
            if strategy and result["best_score"] > 0.3:
                strategy.set_params(**result["best_params"])
                applied[strat_name] = result
        return applied

class Strategy(ABC):
    name: str = "base"
    description: str = ""
    default_params: StrategyParams = StrategyParams()

    def __init__(self):
        self.params = StrategyParams()
        self._custom_params: Dict[str, Any] = {}

    def set_params(self, **kwargs) -> "Strategy":
        for k, v in kwargs.items():
            if hasattr(self.params, k):
                setattr(self.params, k, v)
                self._custom_params[k] = v
        return self

    def get_params(self) -> Dict[str, Any]:
        return self.params.to_dict()

    def reset_params(self) -> "Strategy":
        self.params = StrategyParams()
        self._custom_params = {}
        return self

    @abstractmethod
    def evaluate(self, df: pd.DataFrame) -> Optional[RawSignal]: ...

    def evaluate_with_params(self, df: pd.DataFrame, params: Dict[str, Any]) -> Optional[RawSignal]:
        """使用指定参数评估策略"""
        original_params = self._custom_params.copy()
        self.set_params(**params)
        result = self.evaluate(df)
        self._custom_params = original_params
        for k, v in original_params.items():
            if hasattr(self.params, k):
                setattr(self.params, k, v)
        return result

@register
class MABreakoutStrategy(Strategy):
    name = "ma_breakout"
    description = "均线多头+放量突破"
    default_params = StrategyParams(vol_multiplier=1.8, ma_period=20)

    def evaluate(self, df):
        if len(df) < self.params.ma_period + 5:
            return None
        last, prev = df.iloc[-1], df.iloc[-2]
        close = float(last["close"])
        ma20 = float(last.get("ma20", 0))
        ma20_p = float(prev.get("ma20", 0))
        ma5 = float(last.get("ma5", 0))
        ma10 = float(last.get("ma10", 0))
        vol = float(last.get("volume", 0))
        vol_ma5 = float(last.get("vol_ma5", 1))
        high = float(last.get("high", close))
        low = float(last.get("low", close))

        trend_up = close > ma20 and ma20 > ma20_p
        vol_break = vol > vol_ma5 * self.params.vol_multiplier
        near_high = (high - close) / (high - low + 0.001) < 0.3

        if trend_up and vol_break and near_high:
            confidence = 0.75 if ma5 > ma10 > ma20 else 0.55
            return RawSignal(
                self.name, "BUY", confidence,
                f"站上20日线，成交量放大{vol / vol_ma5:.1f}倍",
                {"vol_ratio": vol / vol_ma5, "ma_alignment": ma5 > ma10 > ma20}
            )

        trend_down = close < ma20 and ma20 < ma20_p
        ma_death_cross = ma5 < ma10 < ma20
        if trend_down or ma_death_cross:
            confidence = 0.70 if ma_death_cross else 0.55
            return RawSignal(
                self.name, "SELL", confidence,
                f"跌破20日线，均线空头排列" if ma_death_cross else "MA20趋势转下",
                {"ma_alignment": ma_death_cross}
            )
        return None

@register
class MACDCrossStrategy(Strategy):
    name = "macd_cross"
    description = "MACD金叉"
    default_params = StrategyParams(momentum_period=10)

    def evaluate(self, df):
        if len(df) < 30:
            return None
        last, prev = df.iloc[-1], df.iloc[-2]
        dif = float(last.get("dif", 0))
        dea = float(last.get("dea", 0))
        macd = float(last.get("macd", 0))
        dif_p = float(prev.get("dif", 0))
        dea_p = float(prev.get("dea", 0))
        macd_p = float(prev.get("macd", 0))

        if dif > dea and dif_p <= dea_p and macd > 0 and macd_p <= 0:
            return RawSignal(
                self.name, "BUY", 0.65,
                "MACD金叉，柱状线由负转正",
                {"dif": dif, "dea": dea, "macd": macd}
            )

        if dif > dea and macd > macd_p and macd > 0:
            lookback = min(self.params.momentum_period, len(df) - 1)
            p5 = df.iloc[-lookback - 1] if len(df) > lookback else prev
            if float(p5.get("macd", 0)) < 0:
                return RawSignal(
                    self.name, "BUY", 0.55,
                    "MACD柱状线连续放大",
                    {"macd_trend": "increasing"}
                )

        if dif < dea and dif_p >= dea_p:
            return RawSignal(
                self.name, "SELL", 0.65,
                "MACD死叉，DIF下穿DEA",
                {"dif": dif, "dea": dea, "macd": macd}
            )

        if dif < dea and macd < macd_p and macd < 0:
            return RawSignal(
                self.name, "SELL", 0.55,
                "MACD柱状线持续缩小",
                {"macd_trend": "decreasing"}
            )
        return None

@register
class BollingerSqueezeStrategy(Strategy):
    name = "boll_squeeze"
    description = "布林带收口突破"
    default_params = StrategyParams(boll_squeeze_ratio=0.95)

    def evaluate(self, df):
        if len(df) < 25:
            return None
        last, prev = df.iloc[-1], df.iloc[-2]
        close = float(last["close"])
        mid = float(last.get("boll_mid", 0))
        upper = float(last.get("boll_upper", 0))
        lower = float(last.get("boll_lower", 0))
        mid_p = float(prev.get("boll_mid", 0))
        upper_p = float(prev.get("boll_upper", 0))
        lower_p = float(prev.get("boll_lower", 0))

        if mid == 0 or mid_p == 0:
            return None

        bw = (upper - lower) / mid
        bw_p = (upper_p - lower_p) / mid_p

        if close > mid and float(prev["close"]) <= mid_p and bw < bw_p * self.params.boll_squeeze_ratio:
            return RawSignal(
                self.name, "BUY", 0.60,
                f"布林带收口(bw={bw:.3f})后突破中轨",
                {"bandwidth": bw, "bandwidth_prev": bw_p, "squeeze_ratio": bw / bw_p}
            )

        if close < lower and float(prev["close"]) >= lower_p and lower > 0:
            return RawSignal(
                self.name, "SELL", 0.60,
                f"跌破布林下轨(bw={bw:.3f})",
                {"bandwidth": bw, "break_lower": True}
            )
        return None

@register
class RSIOversoldStrategy(Strategy):
    name = "rsi_oversold"
    description = "RSI超卖反弹"
    default_params = StrategyParams(rsi_threshold=30)

    def evaluate(self, df):
        if len(df) < 20:
            return None
        rsi = float(df.iloc[-1].get("rsi", 50))
        rsi_p = float(df.iloc[-2].get("rsi", 50))

        threshold = self.params.rsi_threshold
        if rsi_p < threshold and rsi > threshold and rsi > rsi_p:
            confidence = 0.55 + (threshold - rsi_p) / 100
            return RawSignal(
                self.name, "BUY", min(confidence, 0.75),
                f"RSI从{rsi_p:.1f}超卖反弹至{rsi:.1f}",
                {"rsi": rsi, "rsi_prev": rsi_p, "threshold": threshold}
            )

        overbought = 100 - threshold
        if rsi_p > overbought and rsi < overbought and rsi < rsi_p:
            confidence = 0.55 + (rsi_p - overbought) / 100
            return RawSignal(
                self.name, "SELL", min(confidence, 0.75),
                f"RSI从{rsi_p:.1f}超买回落至{rsi:.1f}",
                {"rsi": rsi, "rsi_prev": rsi_p, "overbought": overbought}
            )
        return None

@register
class KDJCrossStrategy(Strategy):
    name = "kdj_cross"
    description = "KDJ超卖区金叉"
    default_params = StrategyParams(kdj_threshold=50)

    def evaluate(self, df):
        if len(df) < 15:
            return None
        last, prev = df.iloc[-1], df.iloc[-2]
        k = float(last.get("k", 50))
        d = float(last.get("d", 50))
        k_p = float(prev.get("k", 50))
        d_p = float(prev.get("d", 50))

        if k > d and k_p <= d_p and k < self.params.kdj_threshold:
            confidence = 0.55 + (self.params.kdj_threshold - k) / 200
            return RawSignal(
                self.name, "BUY", min(confidence, 0.70),
                f"KDJ金叉 K={k:.1f} D={d:.1f}",
                {"k": k, "d": d, "threshold": self.params.kdj_threshold}
            )

        overbought = 100 - self.params.kdj_threshold
        if k < d and k_p >= d_p and k > overbought:
            confidence = 0.55 + (k - overbought) / 200
            return RawSignal(
                self.name, "SELL", min(confidence, 0.70),
                f"KDJ死叉 K={k:.1f} D={d:.1f} 超买区",
                {"k": k, "d": d, "overbought": overbought}
            )
        return None

@register
class VolumeShrinkStrategy(Strategy):
    name = "volume_shrink"
    description = "上升趋势缩量回调"
    default_params = StrategyParams(vol_multiplier=0.7)

    def evaluate(self, df):
        if len(df) < 30:
            return None
        last = df.iloc[-1]
        close = float(last["close"])
        ma20 = float(last.get("ma20", 0))
        vol = float(last.get("volume", 0))
        vol_ma5 = float(last.get("vol_ma5", 1))
        ma5 = float(last.get("ma5", 0))

        if ma5 > ma20 > 0 and vol < vol_ma5 * self.params.vol_multiplier and 0 < (close - ma20) / ma20 < 0.03:
            return RawSignal(
                self.name, "BUY", 0.50,
                f"缩量回调，成交量仅为5日均量的{vol / vol_ma5 * 100:.0f}%",
                {"vol_ratio": vol / vol_ma5, "ma_trend": "up"}
            )

        if ma5 < ma20 and vol > vol_ma5 * 1.5 and close < ma20:
            return RawSignal(
                self.name, "SELL", 0.55,
                f"放量下跌，成交量放大{vol / vol_ma5:.1f}倍",
                {"vol_ratio": vol / vol_ma5, "ma_trend": "down"}
            )
        return None

@register
class VolumePriceDivergenceStrategy(Strategy):
    name = "vol_price_divergence"
    description = "量价背离（真正背离检测）"
    default_params = StrategyParams(momentum_period=10)

    def evaluate(self, df):
        if len(df) < 30:
            return None
        period = self.params.momentum_period

        close = df["close"].astype(float)
        volume = df["volume"].astype(float)

        price_slope = self._calc_slope(close.tail(period))
        vol_slope = self._calc_slope(volume.tail(period))

        price_new_low = close.iloc[-1] <= close.tail(period * 2).min() * 1.01
        price_new_high = close.iloc[-1] >= close.tail(period * 2).max() * 0.99

        # 底背离：价格创新低或下行，但成交量/OBV上行（量能背离）
        if price_slope < 0 and vol_slope > 0:
            last = df.iloc[-1]
            if float(last["close"]) > float(last["open"]):
                return RawSignal(
                    self.name, "BUY", 0.60,
                    f"底背离: 价跌量增(price_slope={price_slope:.3f}, vol_slope={vol_slope:.3f})",
                    {"price_slope": price_slope, "vol_slope": vol_slope, "divergence": "bullish"}
                )

        # 顶背离：价格创新高或上行，但成交量下行
        if price_slope > 0 and vol_slope < 0:
            last = df.iloc[-1]
            if float(last["close"]) < float(last["open"]):
                return RawSignal(
                    self.name, "SELL", 0.60,
                    f"顶背离: 价涨量缩(price_slope={price_slope:.3f}, vol_slope={vol_slope:.3f})",
                    {"price_slope": price_slope, "vol_slope": vol_slope, "divergence": "bearish"}
                )

        # OBV背离检测
        obv_signal = self._check_obv_divergence(df, period)
        if obv_signal:
            return obv_signal

        return None

    @staticmethod
    def _calc_slope(series: pd.Series) -> float:
        """计算序列线性回归斜率（标准化）"""
        if len(series) < 3:
            return 0.0
        x = np.arange(len(series))
        y = series.values.astype(float)
        if np.std(y) == 0:
            return 0.0
        slope = np.polyfit(x, y, 1)[0]
        return slope / (np.mean(np.abs(y)) + 1e-10)

    @staticmethod
    def _check_obv_divergence(df: pd.DataFrame, period: int) -> Optional[RawSignal]:
        """检测OBV与价格的背离"""
        close = df["close"].astype(float)
        volume = df["volume"].astype(float)

        obv = [0.0]
        for i in range(1, len(df)):
            c = float(df.iloc[i]["close"])
            cp = float(df.iloc[i - 1]["close"])
            v = float(df.iloc[i]["volume"])
            obv.append(obv[-1] + v if c > cp else obv[-1] - v if c < cp else obv[-1])
        obv_series = pd.Series(obv)

        recent_close = close.tail(period)
        recent_obv = obv_series.tail(period)

        price_trend = 1 if recent_close.iloc[-1] > recent_close.iloc[0] else -1
        obv_trend = 1 if recent_obv.iloc[-1] > recent_obv.iloc[0] else -1

        if price_trend < 0 and obv_trend > 0:
            return RawSignal(
                "vol_price_divergence", "BUY", 0.55,
                "OBV底背离: 价跌但OBV上升",
                {"divergence": "obv_bullish"}
            )
        if price_trend > 0 and obv_trend < 0:
            return RawSignal(
                "vol_price_divergence", "SELL", 0.55,
                "OBV顶背离: 价涨但OBV下降",
                {"divergence": "obv_bearish"}
            )
        return None

@register
class OBVTrendStrategy(Strategy):
    name = "obv_trend"
    description = "OBV趋势确认"
    default_params = StrategyParams(obv_ma_period=5)

    def evaluate(self, df):
        if len(df) < 30:
            return None

        obv = [0.0]
        for i in range(1, len(df)):
            c = float(df.iloc[i]["close"])
            cp = float(df.iloc[i - 1]["close"])
            v = float(df.iloc[i]["volume"])
            obv.append(obv[-1] + v if c > cp else obv[-1] - v if c < cp else obv[-1])

        s = pd.Series(obv)
        ma_period = self.params.obv_ma_period
        ma5 = s.rolling(ma_period).mean()
        ma10 = s.rolling(ma_period * 2).mean()

        if float(ma5.iloc[-1]) > float(ma5.iloc[-2]) and float(ma5.iloc[-1]) > float(ma10.iloc[-1]):
            if float(df.iloc[-1]["close"]) > float(df.iloc[-1].get("ma20", 0)):
                return RawSignal(
                    self.name, "BUY", 0.50,
                    "OBV持续上升，资金流入确认",
                    {"obv_trend": "up", "price_above_ma": True}
                )

        if float(ma5.iloc[-1]) < float(ma5.iloc[-2]) and float(ma5.iloc[-1]) < float(ma10.iloc[-1]):
            if float(df.iloc[-1]["close"]) < float(df.iloc[-1].get("ma20", 0)):
                return RawSignal(
                    self.name, "SELL", 0.50,
                    "OBV持续下降，资金流出确认",
                    {"obv_trend": "down", "price_below_ma": True}
                )
        return None

@register
class DoubleMAStrategy(Strategy):
    name = "double_ma"
    description = "双均线金叉放量"
    default_params = StrategyParams(vol_multiplier=1.3)

    def evaluate(self, df):
        if len(df) < 25:
            return None
        last, prev = df.iloc[-1], df.iloc[-2]
        ma5 = float(last.get("ma5", 0))
        ma20 = float(last.get("ma20", 0))
        ma5_p = float(prev.get("ma5", 0))
        ma20_p = float(prev.get("ma20", 0))
        vol = float(last.get("volume", 0))
        vol_ma5 = float(last.get("vol_ma5", 1))

        if ma5 > ma20 and ma5_p <= ma20_p and vol > vol_ma5 * self.params.vol_multiplier:
            return RawSignal(
                self.name, "BUY", 0.60,
                f"MA5/MA20金叉，成交量放大{vol / vol_ma5:.1f}倍",
                {"vol_ratio": vol / vol_ma5, "golden_cross": True}
            )

        if ma5 < ma20 and ma5_p >= ma20_p:
            return RawSignal(
                self.name, "SELL", 0.60,
                "MA5/MA20死叉，趋势转空",
                {"death_cross": True}
            )
        return None

@register
class SupportBounceStrategy(Strategy):
    name = "support_bounce"
    description = "支撑位反弹"
    default_params = StrategyParams(support_tolerance=0.02)

    def evaluate(self, df):
        if len(df) < 30:
            return None
        last, prev = df.iloc[-1], df.iloc[-2]
        close = float(last["close"])
        prev_low = float(prev["low"])
        prev_close = float(prev["close"])
        ma60 = float(last.get("ma60", 0))
        boll_lower = float(last.get("boll_lower", 0))

        tol = self.params.support_tolerance
        touched = (abs(prev_low - ma60) / ma60 < tol and ma60 > 0) or \
                  (abs(prev_low - boll_lower) / boll_lower < tol and boll_lower > 0)

        if touched and close > prev_close and close > float(last["low"]) * 1.01:
            support_name = "MA60" if abs(prev_low - ma60) / ma60 < tol else "布林下轨"
            return RawSignal(
                self.name, "BUY", 0.55,
                f"触及{support_name}支撑后反弹",
                {"support_type": support_name, "bounce_strength": (close - prev_low) / prev_low}
            )

        if ma60 > 0 and close < ma60 * (1 - tol) and prev_close >= ma60 * (1 - tol):
            return RawSignal(
                self.name, "SELL", 0.60,
                "跌破MA60支撑位",
                {"support_break": "MA60"}
            )
        if boll_lower > 0 and close < boll_lower * (1 - tol) and prev_close >= boll_lower * (1 - tol):
            return RawSignal(
                self.name, "SELL", 0.55,
                "跌破布林下轨支撑",
                {"support_break": "布林下轨"}
            )
        return None
