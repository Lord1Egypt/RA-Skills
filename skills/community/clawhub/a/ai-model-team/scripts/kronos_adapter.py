"""
Kronos adapter for AI Model Team
Kronos: K-line specialist, pre-trained on 1.2B K-line records
"""
import sys, os, pandas as pd, numpy as np
from datetime import timedelta
from typing import Dict, Optional

# 使用新的 OKX 数据提供模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from okx_data_provider import OKXDataProvider, get_klines, get_data

# 使用环境变量或默认路径
AI_HEDGE_FUND = os.environ.get('AI_HEDGE_PATH', os.path.join(os.path.expanduser('~'), '.agents/skills/ai-hedge-fund-skill'))
sys.path.insert(0, f"{AI_HEDGE_FUND}/Kronos")
sys.path.insert(0, AI_HEDGE_FUND)

MODEL_DIR = f"{AI_HEDGE_FUND}/models/kronos-base"
TOKENIZER_DIR = f"{AI_HEDGE_FUND}/models/kronos-tokenizer"


class KronosAdapter:
    name = "Kronos-base"
    institution = "NeoQuasar"
    params = "102M"
    specialty = "K线/金融"
    _predictor = None

    def load(self):
        """加载Kronos模型（带错误处理）"""
        if self._predictor is None:
            try:
                from model import Kronos, KronosTokenizer, KronosPredictor
                print("  加载 Kronos 模型...", end=" ", flush=True)
                tokenizer = KronosTokenizer.from_pretrained(
                    "NeoQuasar/Kronos-Tokenizer-base", cache_dir=TOKENIZER_DIR)
                model = Kronos.from_pretrained(
                    "NeoQuasar/Kronos-base", cache_dir=MODEL_DIR)
                self._predictor = KronosPredictor(model, tokenizer, device="cpu", max_context=512)
                print("✅")
            except Exception as e:
                print(f"❌ {str(e)[:50]}")
                raise RuntimeError(f"Kronos模型加载失败: {str(e)[:200]}")
        return self._predictor

    def predict(self, symbol: str, bar: str = "4H", lookback: int = 400,
                 pred_len: int = 24) -> Dict:
        """Kronos预测（带完整错误处理）"""
        try:
            predictor = self.load()
            
            # 获取数据（智能检测股票/加密货币）
            try:
                df = get_data(symbol, bar=bar, limit=lookback + 50)
            except Exception as e:
                return self._error_result(f"无法获取{symbol}数据: {str(e)[:100]}")
            
            if df is None or len(df) == 0:
                return self._error_result(f"获取到的{df}为空或None")
            
            df = df.rename(columns={"ts": "timestamps"})  # 兼容新数据模块
            
            if len(df) < lookback:
                return self._error_result(f"数据不足 ({len(df)} < {lookback})")
            
            df_in = df.tail(lookback).reset_index(drop=True)
            last_ts = df_in["timestamps"].iloc[-1]

            freq_map = {"1H": 1, "4H": 4, "1D": 24, "30m": 0.5, "15m": 0.25, "5m": 0.083, "1m": 0.0167}
            fh = freq_map.get(bar, 4)
            future_ts = pd.date_range(start=last_ts + timedelta(hours=fh),
                                       periods=pred_len, freq=f"{fh}h")
            y_ts = pd.Series(future_ts, name="timestamps")

            x_df = df_in[["open", "high", "low", "close", "vol"]].copy()
            x_df = x_df.rename(columns={"vol": "volume"})
            x_df["amount"] = x_df["volume"] * x_df["close"]

            try:
                pred = predictor.predict(
                    df=x_df, x_timestamp=df_in["timestamps"],
                    y_timestamp=y_ts, pred_len=pred_len,
                    T=1.0, top_p=0.9, sample_count=1, verbose=False
                )
            except Exception as e:
                return self._error_result(f"Kronos预测失败: {str(e)[:100]}")

            cur = float(df_in["close"].iloc[-1])
            fcast = pred["close"].values
            avg_fcast = float(np.mean(fcast))
            pct = (avg_fcast / cur - 1) * 100

            if pct > 2:
                direction, conf = "bullish", min(95, 50 + abs(pct) * 3)
            elif pct < -2:
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
                "reasoning": f"Kronos预测: ${cur:.2f}→${avg_fcast:.2f} ({pct:+.2f}%), "
                             f"趋势强度{trend:.0f}/100"
            }
            
        except Exception as e:
            return self._error_result(str(e))

    def _error_result(self, msg: str) -> Dict:
        """生成错误结果（用于优雅降级）"""
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
            "reasoning": f"Kronos错误: {str(msg)[:100]}"
        }
