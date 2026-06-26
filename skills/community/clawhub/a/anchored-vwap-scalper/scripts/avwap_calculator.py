#!/usr/bin/env python3
import json
import pandas as pd
from datetime import datetime
import os

STATE_FILE = os.path.join(os.path.dirname(__file__), "../state/avwap_state.json")
os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"anchor_ts": None, "cum_pv": 0.0, "cum_vol": 0.0, "last_bar_ts": None}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

def calculate_avwap(candles: list[dict], symbol: str, new_anchor_ts: str = None):
    state = load_state()
    df = pd.DataFrame(candles)
    df['ts'] = pd.to_datetime(df['timestamp'], unit='ms')
    df['typical'] = (df['high'] + df['low'] + df['close']) / 3
    df['pv'] = df['typical'] * df['volume']

    # Handle new anchor
    if new_anchor_ts:
        anchor_idx = df[df['ts'] >= pd.to_datetime(new_anchor_ts)].index[0]
        state["anchor_ts"] = new_anchor_ts
        state["cum_pv"] = float(df.loc[anchor_idx:, 'pv'].sum())
        state["cum_vol"] = float(df.loc[anchor_idx:, 'volume'].sum())
    else:
        # Incremental update
        if state["last_bar_ts"]:
            last_ts = pd.to_datetime(state["last_bar_ts"])
            new_bars = df[df['ts'] > last_ts]
            if not new_bars.empty:
                state["cum_pv"] += float(new_bars['pv'].sum())
                state["cum_vol"] += float(new_bars['volume'].sum())
        else:
            state["cum_pv"] = float(df['pv'].sum())
            state["cum_vol"] = float(df['volume'].sum())

    state["last_bar_ts"] = str(df['ts'].iloc[-1])
    avwap = state["cum_pv"] / state["cum_vol"] if state["cum_vol"] > 0 else float(df['close'].iloc[-1])
    save_state(state)
    return float(avwap)