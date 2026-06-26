#!/usr/bin/env python3
"""Earnings call processor: Whisper transcription + stock analysis → Feishu document."""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

import pandas as pd


# ---------------------------------------------------------------------------
# 1. Whisper transcription
# ---------------------------------------------------------------------------

def transcribe_audio(audio_path: str, output_dir: str, model: str = "turbo") -> str:
    """Run Whisper on the audio file and return the transcript text."""
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    cmd = [
        "whisper",
        str(audio_path),
        "--model", model,
        "--output_format", "txt",
        "--output_dir", str(out_path),
    ]
    print(f"[whisper] Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[whisper] stderr: {result.stderr}", file=sys.stderr)
        raise RuntimeError(f"Whisper failed with exit code {result.returncode}")

    # Whisper writes <basename>.txt next to the audio or in output_dir
    audio_stem = Path(audio_path).stem
    transcript_file = out_path / f"{audio_stem}.txt"
    if not transcript_file.exists():
        # fallback: look for any .txt in output_dir
        txts = list(out_path.glob("*.txt"))
        if txts:
            transcript_file = txts[0]
        else:
            raise FileNotFoundError(f"No transcript file found in {out_path}")

    transcript = transcript_file.read_text(encoding="utf-8").strip()
    # also save a canonical copy
    canonical = out_path / "transcript.txt"
    canonical.write_text(transcript, encoding="utf-8")
    print(f"[whisper] Transcript saved to {canonical} ({len(transcript)} chars)")
    return transcript


# ---------------------------------------------------------------------------
# 2. Stock price analysis
# ---------------------------------------------------------------------------

def analyze_stock(csv_path: str, symbol: str) -> dict:
    """Load stock CSV and compute key financial indicators."""
    df = pd.read_csv(csv_path)
    df["Date"] = pd.to_datetime(df["Date"])

    close_col = [c for c in df.columns if "Close" in c or "close" in c]
    if not close_col:
        raise ValueError(f"No Close column found in {csv_path}. Columns: {list(df.columns)}")
    close = df[close_col[0]]

    volume_col = [c for c in df.columns if "Volume" in c or "volume" in c]
    volume = df[volume_col[0]] if volume_col else pd.Series(dtype=float)

    high_col = [c for c in df.columns if "High" in c and "Adj" not in c]
    low_col = [c for c in df.columns if "Low" in c and "Adj" not in c]
    high = df[high_col[0]] if high_col else close
    low = df[low_col[0]] if low_col else close

    # Daily returns
    daily_returns = close.pct_change().dropna()

    indicators = {
        "symbol": symbol,
        "period_start": str(df["Date"].min().date()),
        "period_end": str(df["Date"].max().date()),
        "trading_days": len(df),
        "price_start": round(float(close.iloc[0]), 2),
        "price_end": round(float(close.iloc[-1]), 2),
        "price_high": round(float(high.max()), 2),
        "price_low": round(float(low.min()), 2),
        "price_change_pct": round(float((close.iloc[-1] / close.iloc[0] - 1) * 100), 2),
        "avg_daily_volume": round(float(volume.mean()), 0) if len(volume) else None,
        "volatility_daily_pct": round(float(daily_returns.std() * 100), 4),
        "max_drawdown_pct": round(float(((close / close.cummax()) - 1).min() * 100), 2),
        "sharpe_ratio_annualized": round(
            float(daily_returns.mean() / daily_returns.std() * (252 ** 0.5)), 4
        ) if len(daily_returns) > 1 else None,
    }

    # Direction distribution
    if "direction" in df.columns:
        dir_counts = df["direction"].value_counts().to_dict()
        indicators["direction_distribution"] = dir_counts

    # Moving average vs close at end
    if "mavg" in df.columns:
        indicators["mavg_end"] = round(float(df["mavg"].iloc[-1]), 2)
        indicators["close_vs_mavg_pct"] = round(
            float((close.iloc[-1] / df["mavg"].iloc[-1] - 1) * 100), 2
        )

    # Bollinger band position at end
    if "up" in df.columns and "dn" in df.columns:
        band_up = float(df["up"].iloc[-1])
        band_dn = float(df["dn"].iloc[-1])
        band_width = band_up - band_dn
        if band_width > 0:
            indicators["bollinger_position"] = round(
                float((close.iloc[-1] - band_dn) / band_width * 100), 1
            )

    return indicators


# ---------------------------------------------------------------------------
# 3. Feishu structured document generation
# ---------------------------------------------------------------------------

def generate_feishu_content(transcript: str, indicators: dict) -> str:
    """Build a structured Feishu-ready markdown document from transcript + indicators.

    This is the function that was previously incomplete — it now produces a full
    structured document with:
      - Title and metadata header
      - Financial indicators section (table + narrative)
      - Earnings call transcript section
      - Key takeaways / summary section
    """
    symbol = indicators.get("symbol", "N/A")
    period_start = indicators.get("period_start", "N/A")
    period_end = indicators.get("period_end", "N/A")
    trading_days = indicators.get("trading_days", "N/A")
    price_start = indicators.get("price_start", "N/A")
    price_end = indicators.get("price_end", "N/A")
    price_high = indicators.get("price_high", "N/A")
    price_low = indicators.get("price_low", "N/A")
    price_change_pct = indicators.get("price_change_pct", "N/A")
    avg_vol = indicators.get("avg_daily_volume", "N/A")
    volatility = indicators.get("volatility_daily_pct", "N/A")
    max_dd = indicators.get("max_drawdown_pct", "N/A")
    sharpe = indicators.get("sharpe_ratio_annualized", "N/A")
    mavg_end = indicators.get("mavg_end", "N/A")
    close_vs_mavg = indicators.get("close_vs_mavg_pct", "N/A")
    bollinger = indicators.get("bollinger_position", "N/A")
    direction_dist = indicators.get("direction_distribution", {})

    # Format volume
    if isinstance(avg_vol, (int, float)) and avg_vol:
        avg_vol_str = f"{avg_vol:,.0f}"
    else:
        avg_vol_str = str(avg_vol)

    # Direction summary line
    dir_parts = [f"{k}: {v}天" for k, v in direction_dist.items()] if direction_dist else []
    dir_line = "、".join(dir_parts) if dir_parts else "N/A"

    # Build narrative
    trend_word = "上涨" if isinstance(price_change_pct, (int, float)) and price_change_pct > 0 else "下跌"
    trend_emoji = "📈" if trend_word == "上涨" else "📉"

    narrative = (
        f"{symbol} 在 {period_start} 至 {period_end} 期间共交易 {trading_days} 天，"
        f"收盘价从 {price_start} {trend_word}至 {price_end}，"
        f"涨跌幅 {price_change_pct}%。{trend_emoji}"
    )

    if isinstance(max_dd, (int, float)):
        narrative += f"\n期间最大回撤 {max_dd}%，"

    if isinstance(sharpe, (int, float)):
        narrative += f"年化夏普比率 {sharpe}。"

    if isinstance(close_vs_mavg, (int, float)):
        mavg_dir = "高于" if close_vs_mavg > 0 else "低于"
        narrative += f"期末收盘价{mavg_dir}移动均线 {abs(close_vs_mavg)}%。"

    if isinstance(bollinger, (int, float)):
        narrative += f"布林带位置 {bollinger}%（0=下轨，100=上轨）。"

    # Transcript preview (first 2000 chars, full version in appendix)
    transcript_preview = transcript[:2000]
    if len(transcript) > 2000:
        transcript_preview += "\n\n... (完整转录见下方附录) ..."

    # Key takeaways extraction (simple heuristic: first 3 non-empty lines)
    lines = [l.strip() for l in transcript.split("\n") if l.strip()]
    key_lines = lines[:5] if lines else ["（转录内容为空）"]
    takeaways = "\n".join(f"- {l}" for l in key_lines)

    # Assemble full document
    doc = f"""# {symbol} 财报电话会总结

## 基本信息

- 标的：{symbol}
- 数据区间：{period_start} ~ {period_end}
- 交易日数：{trading_days}

## 股价关键指标

| 指标 | 数值 |
|------|------|
| 期初收盘价 | {price_start} |
| 期末收盘价 | {price_end} |
| 区间最高价 | {price_high} |
| 区间最低价 | {price_low} |
| 区间涨跌幅 | {price_change_pct}% |
| 日均成交量 | {avg_vol_str} |
| 日波动率 | {volatility}% |
| 最大回撤 | {max_dd}% |
| 年化夏普比率 | {sharpe} |
| 期末移动均线 | {mavg_end} |
| 收盘vs均线偏离 | {close_vs_mavg}% |
| 布林带位置 | {bollinger}% |
| 涨跌方向分布 | {dir_line} |

## 走势概述

{narrative}

## 电话会要点摘录

{takeaways}

## 电话会转录（节选）

{transcript_preview}

## 附录：完整转录

{transcript}
"""

    return doc


# ---------------------------------------------------------------------------
# 4. Main pipeline
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Earnings call processor")
    parser.add_argument("--audio", required=True, help="Path to earnings call audio file")
    parser.add_argument("--stock-csv", required=True, help="Path to stock price history CSV")
    parser.add_argument("--symbol", required=True, help="Stock ticker symbol (e.g. AAPL)")
    parser.add_argument("--output-dir", default="/tmp/earnings_output", help="Output directory")
    parser.add_argument("--whisper-model", default="turbo", help="Whisper model name")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Step 1: Transcribe
    print("=" * 60)
    print("Step 1: Transcribing audio with Whisper")
    print("=" * 60)
    transcript = transcribe_audio(args.audio, str(output_dir), model=args.whisper_model)

    # Step 2: Analyze stock
    print("\n" + "=" * 60)
    print("Step 2: Analyzing stock price data")
    print("=" * 60)
    indicators = analyze_stock(args.stock_csv, args.symbol)
    indicators_path = output_dir / "financial_indicators.json"
    indicators_path.write_text(json.dumps(indicators, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[analysis] Indicators saved to {indicators_path}")
    print(json.dumps(indicators, indent=2, ensure_ascii=False))

    # Step 3: Generate Feishu content
    print("\n" + "=" * 60)
    print("Step 3: Generating Feishu structured document")
    print("=" * 60)
    feishu_md = generate_feishu_content(transcript, indicators)
    feishu_path = output_dir / "feishu_content.md"
    feishu_path.write_text(feishu_md, encoding="utf-8")
    print(f"[feishu] Content saved to {feishu_path} ({len(feishu_md)} chars)")

    print("\n✅ Pipeline complete. Files in output directory:")
    for f in sorted(output_dir.iterdir()):
        print(f"  {f.name} ({f.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
