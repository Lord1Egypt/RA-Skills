#!/usr/bin/env python3
"""
AI Model Team - 1H × 24 统一预测
All three models predict 24 hours ahead (24 × 1H bars) for direct comparison.
- Chronos: 1H × 24 (24hr continuous forecast)
- TimesFM: 1H × 24 (24hr continuous forecast)
- Kronos: 1H × 24 (24hr continuous forecast)
All models reference the SAME current price for % calculation.
"""
import subprocess, sys, os

# 使用环境变量或默认路径
AI_MODEL_TEAM_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AI_HEDGE = os.environ.get('AI_HEDGE_PATH', os.path.join(os.path.expanduser('~'), '.agents/skills/ai-hedge-fund-skill'))
OBSIDIAN_VAULT = os.environ.get('OBSIDIAN_VAULT', os.path.join(os.path.expanduser('~'), 'Obsidian/我的远程库'))

TIMESFM_VENV = os.path.join(AI_MODEL_TEAM_DIR, "timesfm_only", "bin", "python3")
CHRONOS_VENV = os.path.join(AI_MODEL_TEAM_DIR, ".venv", "bin", "python3")

# 信号阈值配置（可调）
BULLISH_THRESHOLD = 2.0
BEARISH_THRESHOLD = -2.0


def get_cur(symbol="BTC-USDT-SWAP"):
    import requests
    url = "https://www.okx.com/api/v5/market/history-candles"
    try:
        r = requests.get(url, params={"instId": symbol, "bar": "4H", "limit": 5}, timeout=30)
        r.raise_for_status()
        d = r.json()
        if d.get("code") == "0" and d.get("data"):
            return float(d["data"][-1][4])  # close price
    except requests.RequestException:
        pass
    return None


def get_data(bar, limit):
    """获取OKX K线数据"""
    import requests, pandas as pd
    url = "https://www.okx.com/api/v5/market/history-candles"
    try:
        r = requests.get(url, params={"instId": "BTC-USDT-SWAP", "bar": bar, "limit": limit}, timeout=30)
        r.raise_for_status()
        d = r.json()
        cols = ["ts","open","high","low","close","vol","vol2","vol3","confirm"]
        df = pd.DataFrame(d["data"], columns=cols)
        df['close'] = pd.to_numeric(df['close'])
        df = df.sort_values("ts").reset_index(drop=True)
        return df["close"].values.astype("float32")
    except requests.RequestException:
        return None


cur_price = get_cur()
if cur_price is None:
    print("❌ 无法获取当前价格")
    sys.exit(1)

print(f"[统一参考价] BTC-USDT-SWAP 1H收盘: ${cur_price:.2f}")
print()

results = {}

# ── Chronos-2 (1H - 24hr continuous) ──
print("▶ Chronos-2  [1H×24 24小时连续 — 宏观周期]...", flush=True)
chr_code = f"""
import numpy as np, chronos, torch, requests, pandas as pd

BULLISH_THRESHOLD = {BULLISH_THRESHOLD}
BEARISH_THRESHOLD = {BEARISH_THRESHOLD}

def get_data(bar, limit):
    url = "https://www.okx.com/api/v5/market/history-candles"
    r = requests.get(url, params={{"instId": "BTC-USDT-SWAP", "bar": bar, "limit": limit}}, timeout=30)
    d = r.json()
    cols = ["ts","open","high","low","close","vol","vol2","vol3","confirm"]
    df = pd.DataFrame(d["data"], columns=cols)
    df['close'] = pd.to_numeric(df['close'])
    df = df.sort_values("ts").reset_index(drop=True)
    return df["close"].values.astype("float32")

prices = get_data('1H', 100)
cur = float(prices[-1])
ctx = [torch.tensor(prices[-64:], dtype=torch.float32)]
pipeline = chronos.Chronos2Pipeline.from_pretrained('amazon/chronos-2', device_map='cpu', dtype=torch.float32)
forecast = pipeline.predict(ctx, prediction_length=24)[0]  # (1, 21, 24)
# quantiles: [0.01, 0.05, ..., 0.5, ..., 0.95, 0.99]; q50=index10
fcast = forecast[0, 10, :].numpy()  # median quantile
avg_f = float(np.mean(fcast))
pct = (avg_f/cur-1)*100
direction = 'bullish' if pct>BULLISH_THRESHOLD else 'bearish' if pct<BEARISH_THRESHOLD else 'neutral'
up = sum(1 for p in fcast if p>cur)
print(f"RESULT:chr:{{direction}}:{{pct:.2f}}:{{cur:.2f}}:{{avg_f:.2f}}:{{up}}")
"""
out = subprocess.run([CHRONOS_VENV, "-c", chr_code], capture_output=True, text=True, timeout=300)
for line in out.stdout.strip().split("\n"):
    if line.startswith("RESULT:chr:"):
        _, _, d, p, c, a, u = line.split(":")
        results["Chronos-t5-large"] = {
            "direction": d, "pct": float(p), "cur": float(c), "avg": float(a), "up": int(u),
            "bar": "1H×24", "model": "Chronos-2", "inst": "Amazon",
            "params": "710M", "spec": "泛领域宏观周期(数学)"
        }
        print(f"  {d} {float(p):+.2f}%  ref=${float(c):.2f} → ${float(a):.2f}  [{u}/24 周期看涨]")
        break

# ── TimesFM (1H - generic trend rhythm, 24hr continuous) ──
print("▶ TimesFM-2.5-200M  [1H×24 24小时连续 — 通用节奏]...", flush=True)
tfm_code = f"""
import numpy as np, requests, pandas as pd
from timesfm import TimesFM_2p5_200M_torch, ForecastConfig

BULLISH_THRESHOLD = {BULLISH_THRESHOLD}
BEARISH_THRESHOLD = {BEARISH_THRESHOLD}

def get_data(bar, limit):
    url = "https://www.okx.com/api/v5/market/history-candles"
    r = requests.get(url, params={{"instId": "BTC-USDT-SWAP", "bar": bar, "limit": limit}}, timeout=30)
    d = r.json()
    cols = ["ts","open","high","low","close","vol","vol2","vol3","confirm"]
    df = pd.DataFrame(d["data"], columns=cols)
    df['close'] = pd.to_numeric(df['close'])
    df = df.sort_values("ts").reset_index(drop=True)
    return df["close"].values.astype("float32")

prices = get_data('1H', 200)
cur = float(prices[-1])
tfm = TimesFM_2p5_200M_torch.from_pretrained('google/timesfm-2.5-200m-pytorch', proxies=None)
fc = ForecastConfig(max_context=512, max_horizon=128, per_core_batch_size=4)
tfm.compile(forecast_config=fc)
fcast = tfm.forecast(horizon=24, inputs=[prices[-200:]])[0][0]
avg_f = float(np.mean(fcast))
pct = (avg_f/cur-1)*100
direction = 'bullish' if pct>BULLISH_THRESHOLD else 'bearish' if pct<BEARISH_THRESHOLD else 'neutral'
up = sum(1 for p in fcast if p>cur)
print(f"RESULT:tfm:{{direction}}:{{pct:.2f}}:{{cur:.2f}}:{{avg_f:.2f}}:{{up}}")
"""
out = subprocess.run([TIMESFM_VENV, "-c", tfm_code], capture_output=True, text=True, timeout=300)
for line in out.stdout.strip().split("\n"):
    if line.startswith("RESULT:tfm:"):
        _, _, d, p, c, a, u = line.split(":")
        results["TimesFM-2.5-200M"] = {
            "direction": d, "pct": float(p), "cur": float(c), "avg": float(a), "up": int(u),
            "bar": "1H×24", "model": "TimesFM-2.5-200M", "inst": "Google",
            "params": "200M", "spec": "通用时序节奏"
        }
        print(f"  {d} {float(p):+.2f}%  ref=${float(c):.2f} → ${float(a):.2f}  [{u}/24 周期看涨]")
        break

# ── Kronos (1H - crypto K-line specialist, 24hr continuous) ──
print("▶ Kronos-base  [1H 24小时连续 — K线形态]...", flush=True)

sys.path.insert(0, AI_HEDGE)
sys.path.insert(0, f"{AI_HEDGE}/Kronos")
import requests as _req, pandas as _pd, numpy as _np
from datetime import timedelta as _td

def _get_ohlcv(symbol, bar, limit):
    url = 'https://www.okx.com/api/v5/market/history-candles'
    r = _req.get(url, params={'instId': symbol, 'bar': bar, 'limit': limit}, timeout=30)
    d = r.json()
    cols = ['ts','open','high','low','close','vol','vol2','vol3','confirm']
    df = _pd.DataFrame(d['data'], columns=cols)
    for c in ['open','high','low','close','vol']: df[c] = _pd.to_numeric(df[c])
    df['ts'] = _pd.to_datetime(df['ts'].astype(float), unit='ms')
    return df.sort_values('ts').reset_index(drop=True)

df_kr = _get_ohlcv('BTC-USDT-SWAP', '1H', 300)
kr_cur = float(df_kr['close'].iloc[-1])
kr_ts = df_kr['ts'].iloc[-1]

from kronos_distilled import load_kronos_predictor as _load_kp
_predictor = _load_kp()

_kr_df = df_kr.rename(columns={'ts':'timestamps','vol':'volume'})
_kr_df['amount'] = _kr_df['volume'] * _kr_df['close']
_x_ts = _kr_df['timestamps'].reset_index(drop=True)
_x_df2 = _kr_df[['open','high','low','close','volume','amount']].reset_index(drop=True)

_pred_len = 24
_future_ts = _pd.date_range(start=kr_ts + _td(hours=1), periods=_pred_len, freq='1h')
_y_ts = _pd.Series(_future_ts, name='timestamps')

_kr_pred = _predictor.predict(df=_x_df2, x_timestamp=_x_ts, y_timestamp=_y_ts,
    pred_len=_pred_len, T=1.0, top_p=0.9, sample_count=1, verbose=False)
_kr_fcast = _kr_pred['close'].values
_kr_avg = float(_np.mean(_kr_fcast))
_kr_pct = (_kr_avg/kr_cur-1)*100
_kr_up = int(sum(1 for p in _kr_fcast if p>kr_cur))
_kr_dir = 'bullish' if _kr_pct>BULLISH_THRESHOLD else 'bearish' if _kr_pct<BEARISH_THRESHOLD else 'neutral'

results["Kronos-base"] = {
    "direction": _kr_dir,
    "pct": float(_kr_pct),
    "cur": kr_cur,
    "avg": _kr_avg,
    "up": _kr_up,
    "bar": "1H×24",
    "model": "Kronos-base",
    "inst": "NeoQuasar",
    "params": "102M",
    "spec": "加密K线专精(庄家行为/洗盘)"
}
d = _kr_dir; p = _kr_pct; c = kr_cur; a = _kr_avg
u = _kr_up
print(f"  {d} {p:+.2f}%  ref=${c:.2f} → ${a:.2f}  [{u}/24 周期看涨]")

# ── Weighted Ensemble ──
print()
print("=" * 60)
print(f"  🎯 三模型分工分析 — BTC-USDT-SWAP")
print(f"  统一参考价: ${cur_price:.2f}")
print("=" * 60)

for name, r in results.items():
    emoji = "🟢" if r["direction"]=="bullish" else "🔴" if r["direction"]=="bearish" else "⚪"
    bar = r.get("bar","?")
    spec = r.get("spec","")
    print(f"  {emoji} {r['model']:<22} [{bar}]  {r['direction']:>8} {r['pct']:+.2f}%")
    print(f"     ref=${r['cur']:.2f} → ${r['avg']:.2f}  [{r['up']}/24涨]  {spec}")

# Weighted voting: Kronos=40%, Chronos=30%, TimesFM=30%
weights = {"Kronos-base": 0.4, "Chronos-t5-large": 0.3, "TimesFM-2.5-200M": 0.3}
bullish_w = sum(weights[n] for n,r in results.items() if r["direction"]=="bullish")
bearish_w = sum(weights[n] for n,r in results.items() if r["direction"]=="bearish")

avg_pct_w = sum(weights[n]*r["pct"] for n,r in results.items())
avg_conf = sum(50+abs(r["pct"])*3 for r in results.values()) / 3
conf = min(95, avg_conf)

if bullish_w >= 0.5: fused, femoji = "bullish 🟢", "🟢"
elif bearish_w >= 0.5: fused, femoji = "bearish 🔴", "🔴"
else: fused, femoji = "neutral ⚪", "⚪"

print()
print(f"  ── 加权投票 ──")
print(f"  Kronos(1H×24)×40% {'✅' if 'Kronos-base' in results else '❌'}  Chronos(1H×24)×30%  TimesFM(1H×24)×30%")
print(f"  看多权重: {bullish_w*100:.0f}%  |  看空权重: {bearish_w*100:.0f}%")
print()
print(f"  🏛️ 综合信号: {fused}  |  置信度: {conf:.0f}/100")
print(f"  📊 加权平均变化: {avg_pct_w:+.2f}%")
print("=" * 60)
print("⚠️ 仅供参考，不构成投资建议")

# ── Auto-write to Obsidian ──
NOTE = os.path.join(OBSIDIAN_VAULT, "投资分析", "AI-Model-Team-Runs.md")

from datetime import datetime
now = datetime.now().strftime("%Y-%m-%d %H:%M")

lines = [
    f"## {now}  — BTC-USDT-SWAP",
    f"**统一参考价:** ${cur_price:.2f}  **综合信号:** {fused}  **置信度:** {conf:.0f}/100  **加权变化:** {avg_pct_w:+.2f}%",
    "",
    "| 模型 | 时间帧 | 信号 | 变化 | 周期看涨 | 权重 | 备注 |",
    "|------|---------|------|------|---------|------|------|",
]
weight_map = {"Kronos-base": "40%", "Chronos-t5-large": "30%", "TimesFM-2.5-200M": "30%"}
for name, r in results.items():
    emoji = "🟢" if r["direction"]=="bullish" else "🔴" if r["direction"]=="bearish" else "⚪"
    w = weight_map.get(r["model"], "—")
    lines.append(f"| {emoji} {r['model']} | {r['bar']} | {r['direction']} | {r['pct']:+.2f}% | {r['up']}/24 | {w} | {r['spec']} |")

lines.append("")

# 确保目录存在
os.makedirs(os.path.dirname(NOTE), exist_ok=True)
try:
    with open(NOTE, "a", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"\n✅ 已写入 Obsidian: {NOTE}")
except Exception as e:
    print(f"\n⚠️ Obsidian写入失败: {e}")
