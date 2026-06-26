"""
Chronos adapter for AI Model Team
Chronos: Amazon's T5-based time series foundation model
"""
import sys, os, pandas as pd, numpy as np, torch
from datetime import timedelta
from typing import Dict

# 使用新的 OKX 数据提供模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from okx_data_provider import OKXDataProvider, get_klines, get_data

# 信号阈值配置（可调）
BULLISH_THRESHOLD = 2.0
BEARISH_THRESHOLD = -2.0

MODEL_CONFIGS = {
    "chronos-2": {
        "hf": "amazon/chronos-2", "params": "~120M",
        "institution": "Amazon", "desc": "Chronos-2 (最新模型)"
    },
    "chronos-t5-small": {
        "hf": "amazon/chronos-t5-small", "params": "~20M",
        "institution": "Amazon", "desc": "Chronos T5 Small (轻量通用)"
    },
    "chronos-t5-base": {
        "hf": "amazon/chronos-t5-base", "params": "~200M",
        "institution": "Amazon", "desc": "Chronos T5 Base (通用)"
    },
}


class ChronosAdapter:
    """Chronos T5-based time series model"""
    _models = {}

    def __init__(self, variant: str = "chronos-t5-base"):
        self.variant = variant
        cfg = MODEL_CONFIGS.get(variant, MODEL_CONFIGS["chronos-t5-base"])
        self.name = cfg["hf"].split("/")[1]
        self.institution = cfg["institution"]
        self.params = cfg["params"]
        self.hf_name = cfg["hf"]
        self.specialty = "通用时序"
        self._pipeline = None

    def load(self):
        if self.variant not in ChronosAdapter._models:
            if self.hf_name == "amazon/chronos-2":
                from chronos import Chronos2Pipeline
                ChronosAdapter._models[self.variant] = Chronos2Pipeline.from_pretrained(
                    self.hf_name,
                    device_map='cpu',
                )
            else:
                from chronos import ChronosPipeline
                ChronosAdapter._models[self.variant] = ChronosPipeline.from_pretrained(
                    self.hf_name,
                )
        return ChronosAdapter._models[self.variant]

    def predict(self, symbol: str, bar: str = "4H",
                 lookback: int = 128, pred_len: int = 24) -> Dict:
        try:
            pipeline = self.load()
            df = get_data(symbol, bar=bar, limit=lookback + pred_len + 50)
            df = df.tail(lookback + pred_len).reset_index(drop=True)

            context = df["close"].values[-lookback:].tolist()

            # Chronos prediction - returns list of tensors or single tensor
            # chronos-t5-base: list of (n_quantiles, pred_len) tensors
            # chronos-2: list of (1, 21, 24) tensors (batch=1, n_quantiles=21, pred_len=24)
            forecast = pipeline.predict([torch.tensor(context)], prediction_length=pred_len)

            # Get first forecast item
            if isinstance(forecast, list):
                forecast_item = forecast[0]
            else:
                forecast_item = forecast

            if isinstance(forecast_item, torch.Tensor):
                forecast_arr = forecast_item.cpu().numpy()
            elif isinstance(forecast_item, np.ndarray):
                forecast_arr = forecast_item
            else:
                forecast_arr = np.array(forecast_item)

            # Handle different output shapes:
            # - chronos-2: (1, 21, 24) -> median over axis=1 -> (1, 24) -> flatten
            # - chronos-t5: (21, 24) or (20, 24) -> median over axis=0 -> (24,)
            if forecast_arr.ndim == 3:
                # chronos-2: (batch=1, n_quantiles, pred_len) -> median over quantiles axis=1
                median_fcast = np.median(forecast_arr[0], axis=1).flatten()  # Shape: (pred_len,)
            elif forecast_arr.ndim == 2:
                # chronos-t5: (n_quantiles, pred_len) -> median over axis=0
                median_fcast = np.median(forecast_arr, axis=0)
            else:
                # Already 1D
                median_fcast = np.atleast_1d(forecast_arr).flatten()
            
            if len(median_fcast) == 0:
                return self._error_result("Empty forecast")

            cur = float(df["close"].iloc[-1])
            mean_fcast = float(np.mean(median_fcast))
            pct = (mean_fcast / cur - 1) * 100

            std = float(np.std(median_fcast))
            conf = max(30, min(95, 50 + abs(pct) * 3))

            if pct > BULLISH_THRESHOLD:
                direction = "bullish"
            elif pct < BEARISH_THRESHOLD:
                direction = "bearish"
            else:
                direction = "neutral"

            up = sum(1 for p in median_fcast if p > cur)
            trend = abs(up / len(median_fcast) - 0.5) * 200

            return {
                "model": self.name,
                "institution": self.institution,
                "params": self.params,
                "specialty": self.specialty,
                "signal": direction,
                "confidence": round(conf, 1),
                "trend_strength": round(float(trend), 1),
                "current_price": cur,
                "forecast_price": round(mean_fcast, 2),
                "price_change_pct": round(pct, 2),
                "forecast_low": round(float(np.min(median_fcast)), 2),
                "forecast_high": round(float(np.max(median_fcast)), 2),
                "up_bars": int(up),
                "total_bars": int(len(median_fcast)),
                "reasoning": f"Chronos({self.name})预测: ${cur:.2f}→${mean_fcast:.2f} ({pct:+.2f}%), 趋势强度{trend:.0f}/100"
            }
        except Exception as e:
            import traceback
            return self._error_result(f"{str(e)[:100]}\n{traceback.format_exc()[:200]}")

    def _error_result(self, msg: str) -> Dict:
        return {
            "model": self.name,
            "institution": self.institution,
            "params": self.params,
            "specialty": self.specialty,
            "signal": "neutral",
            "confidence": 30,
            "trend_strength": 0,
            "current_price": 0,
            "forecast_price": 0,
            "price_change_pct": 0,
            "forecast_low": 0,
            "forecast_high": 0,
            "up_bars": 0,
            "total_bars": 0,
            "reasoning": f"Chronos预测出错: {str(msg)[:120]}"
        }
