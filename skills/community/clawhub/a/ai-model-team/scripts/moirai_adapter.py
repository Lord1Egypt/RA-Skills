"""
MOIRAI adapter for AI Model Team
MOIRAI: Salesforce's large-scale time series foundation model
"""
import sys, os, requests, pandas as pd, numpy as np
from typing import Dict

# 使用环境变量或默认路径
AI_HEDGE_FUND = os.environ.get('AI_HEDGE_PATH', os.path.join(os.path.expanduser('~'), '.agents/skills/ai-hedge-fund-skill'))
sys.path.insert(0, AI_HEDGE_FUND)

OKX_BASE = "https://www.okx.com/api/v5"

# 信号阈值配置（可调）
BULLISH_THRESHOLD = 2.0
BEARISH_THRESHOLD = -2.0


def get_klines(symbol: str, bar: str = "4H", limit: int = 500) -> pd.DataFrame:
    for inst in [symbol, f"{symbol}-SWAP"]:
        url = f"{OKX_BASE}/market/history-candles"
        try:
            r = requests.get(url, params={"instId": inst, "bar": bar, "limit": limit}, timeout=30)
            r.raise_for_status()
            d = r.json()
            if d.get("code") == "0" and d.get("data"):
                cols = ["ts", "open", "high", "low", "close", "vol", "vol2", "vol3", "confirm"]
                df = pd.DataFrame(d["data"], columns=cols)
                for c in ["open", "high", "low", "close", "vol"]:
                    df[c] = pd.to_numeric(df[c])
                df["ts"] = pd.to_datetime(df["ts"].astype(float), unit="ms")
                df = df.sort_values("ts").reset_index(drop=True)
                return df
        except requests.RequestException:
            continue
    raise ValueError(f"Cannot fetch data for {symbol}")


class MOIRAIAdapter:
    """MOIRAI 1.1-R time series model from Salesforce"""
    _pipeline = None

    name = "MOIRAI-1.1-R-small"
    institution = "Salesforce"
    params = "~50M"
    specialty = "多变种时序预测"
    hf_name = "Salesforce/moirai-1.1-R-small"

    def load(self):
        if MOIRAIAdapter._pipeline is None:
            from uni2ts.model.moirai import MOIRAI
            from uni2ts.model.builder import model_builder

            MOIRAIAdapter._pipeline = model_builder(
                [
                    "Salesforce/MOIRAI-1.1-R-small",
                ]
            )
        return MOIRAIAdapter._pipeline

    def predict(self, symbol: str, bar: str = "4H",
                lookback: int = 256, pred_len: int = 24) -> Dict:
        try:
            import torch
        except ImportError:
            return self._error_result("torch not available")

        df = get_klines(symbol, bar=bar, limit=lookback + pred_len + 50)
        df = df.tail(lookback).reset_index(drop=True)

        prices = df["close"].values.astype(np.float32)
        cur = float(prices[-1])

        try:
            # MOIRAI requires specific data format
            # (patch_size, individual_series, dim)
            # Simplified: use last lookback points
            from uni2ts.model.moirai import MOIRAI
            import torch

            model = MOIRAI(
                module="Salesforce/MOIRAI-1.1-R-small",
                device="cpu",
                dtype=torch.float32,
            )

            # MOIRAI prediction
            prediction = model(
                patch_size=32,
                context_length=lookback,
                prediction_length=pred_len,
                freq_mapping={"4H": 6, "1H": 5, "1D": 7}.get(bar, 6),
                value=torch.from_numpy(prices).unsqueeze(0).unsqueeze(-1),
            )

            fcast = prediction.mean(dim=1).squeeze().numpy()
            avg_fcast = float(np.mean(fcast))
            pct = (avg_fcast / cur - 1) * 100

            if pct > BULLISH_THRESHOLD:
                direction, conf = "bullish", min(95, 50 + abs(pct) * 3)
            elif pct < BEARISH_THRESHOLD:
                direction, conf = "bearish", min(95, 50 + abs(pct) * 3)
            else:
                direction, conf = "neutral", 50

            up = sum(1 for p in fcast if p > cur)
            trend = abs(up / len(fcast) - 0.5) * 200

            return {
                "model": self.name, "institution": self.institution,
                "params": self.params, "specialty": self.specialty,
                "signal": direction, "confidence": round(conf, 1),
                "trend_strength": round(float(trend), 1),
                "current_price": cur, "forecast_price": round(avg_fcast, 2),
                "price_change_pct": round(pct, 2),
                "forecast_low": round(float(np.min(fcast)), 2),
                "forecast_high": round(float(np.max(fcast)), 2),
                "up_bars": int(up), "total_bars": int(len(fcast)),
                "reasoning": f"MOIRAI预测: ${cur:.2f}→${avg_fcast:.2f} ({pct:+.2f}%), "
                             f"趋势强度{trend:.0f}/100"
            }
        except Exception as e:
            return {
                "model": self.name, "institution": self.institution,
                "params": self.params, "specialty": self.specialty,
                "signal": "neutral", "confidence": 30,
                "trend_strength": 0, "current_price": cur, "forecast_price": cur,
                "price_change_pct": 0, "forecast_low": cur, "forecast_high": cur,
                "up_bars": 0, "total_bars": 0,
                "reasoning": f"MOIRAI预测出错: {str(e)[:120]}"
            }

    def _error_result(self, msg: str) -> Dict:
        return {
            "model": self.name, "institution": self.institution,
            "params": self.params, "specialty": self.specialty,
            "signal": "neutral", "confidence": 30,
            "trend_strength": 0, "current_price": 0, "forecast_price": 0,
            "price_change_pct": 0, "forecast_low": 0, "forecast_high": 0,
            "up_bars": 0, "total_bars": 0,
            "reasoning": f"MOIRAI加载失败: {msg}"
        }
