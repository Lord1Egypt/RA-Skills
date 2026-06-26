#!/usr/bin/env python3
"""
AI Model Prediction Team
=======================
Multi-model协同预测系统：Kronos + Chronos-2 + TimesFM + FinBERT
对OKX加密货币进行多角度AI预测，输出综合意见
整合社会情绪分析：CryptoPanic + Reddit + RSS

P0/P2: 风险控制闸门强制执行，不可绕过

Usage:
  python3 model_team.py BTC-USDT-SWAP --signal-only
  python3 model_team.py CL-USDT-SWAP --models kronos,chronos-2 --social
  python3 model_team.py ETH-USDT-SWAP --full --social
"""

import sys, os, argparse, json
from datetime import datetime
from typing import List, Dict

# ============ MUST import config FIRST for fail-fast validation ============
AI_MODEL_TEAM_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Config validation happens on import (fail-fast)
try:
    from config import validate_config, ConfigValidationError
    # This will exit if config is invalid
    config_result = validate_config(fail_fast=True)
    print(f"✅ Config validated: env={config_result['config_summary']['app_env']}")
except ConfigValidationError as e:
    print(f"❌ Config Error: {e}")
    sys.exit(1)

# ============ Import Risk Control (MANDATORY) ============
from risk_control import RiskGate, check_trade_risk, get_risk_gate

# ============ Import Optional Modules ============
try:
    from social_sentiment_provider import get_social_sentiment
    SOCIAL_AVAILABLE = True
except ImportError:
    SOCIAL_AVAILABLE = False

OKX_BASE = "https://www.okx.com/api/v5"


def get_klines(symbol: str, bar: str = "4H", limit: int = 200):
    """Fetch K-line data (OKX for crypto, Yahoo Finance for stocks)"""
    from okx_data_provider import get_data
    try:
        df = get_data(symbol, bar=bar, limit=limit)
        return df.to_dict()
    except ValueError:
        return {}


def apply_risk_gate(
    fused_signal: Dict,
    current_equity: float = 10000.0,
    proposed_position_pct: float = 0.1
) -> Dict:
    """
    MANDATORY: Pass all signals through risk gate before outputting
    
    This function MUST be called for every prediction result.
    Risk gate is NON-BYPASSABLE.
    
    Args:
        fused_signal: Fused model signal (from fuse_signals)
        current_equity: Current account equity
        proposed_position_pct: Proposed position size
    
    Returns:
        Risk-checked result with risk_gate_passed and risk_details
    """
    gate = get_risk_gate()
    
    # Check through risk gate
    risk_result = gate.check(
        signal_confidence=fused_signal["confidence"] / 100.0,
        signal_direction=fused_signal["signal"],
        proposed_position_pct=proposed_position_pct,
        current_equity=current_equity
    )
    
    # Add risk gate result to signal
    result = fused_signal.copy()
    result["risk_gate_passed"] = not risk_result.blocked
    result["risk_gate_decision"] = risk_result.decision.value
    result["risk_gate_reason"] = risk_result.reason
    result["risk_gate_details"] = risk_result.details
    
    # Get current risk status
    result["risk_status"] = gate.get_status()
    
    return result


def print_risk_status(risk_status: Dict):
    """Print risk status in report"""
    state = risk_status.get("state", "unknown")
    emoji = "✅" if state == "normal" else "⚠️" if state == "warning" else "🔴"
    
    print(f"\n  {emoji} 风控状态: {state.upper()}")
    
    metrics = risk_status.get("metrics", {})
    if metrics:
        print(f"     ├─ 今日盈亏: {metrics.get('daily_pnl', 'N/A')}")
        print(f"     ├─ 回撤: {metrics.get('daily_drawdown', 'N/A')}")
        print(f"     ├─ 连亏: {metrics.get('consecutive_losses', 0)}次")
        print(f"     └─ 胜率: {metrics.get('win_rate', 'N/A')}")


def print_social_sentiment(symbol: str):
    """Print social sentiment analysis"""
    if not SOCIAL_AVAILABLE:
        print("\n⚠️  社会情绪模块未安装 (pip install feedparser)")
        return
    
    currency = symbol.split("-")[0] if "-" in symbol else symbol
    
    print(f"\n📊 社会情绪分析 ({currency})")
    print(f"{'━' * 62}")
    
    try:
        sentiment = get_social_sentiment(currency)
        
        overall = sentiment.get("overall_sentiment", "neutral")
        score = sentiment.get("sentiment_score", 0)
        
        emoji = {"bullish": "🟢", "bearish": "🔴", "neutral": "⚪"}
        s_emoji = emoji.get(overall, "⚪")
        
        print(f"  {s_emoji} 综合情绪: {overall.upper()} (得分: {score:+.3f})")
        
        breakdown = sentiment.get("breakdown", {})
        print(f"     ├─ 新闻情绪: {breakdown.get('news_sentiment', 0):+.3f}")
        print(f"     └─ Reddit情绪: {breakdown.get('reddit_sentiment', 0):+.3f}")
        
        stats = sentiment.get("statistics", {})
        print(f"\n  📈 数据统计:")
        print(f"     ├─ 新闻: {stats.get('news_positive', 0)}+ / {stats.get('news_negative', 0)}- / {stats.get('news_neutral', 0)}=")
        print(f"     └─ Reddit: {stats.get('reddit_posts', 0)} 帖分析")
        
        hot_topics = sentiment.get("hot_topics", [])
        if hot_topics:
            print(f"\n  🔥 热门话题:")
            for topic in hot_topics[:2]:
                print(f"     • {topic.get('title', '')[:50]}... (👍{topic.get('score', 0)})")
        
    except Exception as e:
        print(f"  ❌ 获取失败: {str(e)[:50]}")
    
    print(f"{'━' * 62}")


def fuse_signals(results: List[Dict]) -> Dict:
    """投票融合多模型信号"""
    bullish = sum(1 for r in results if r["signal"] == "bullish")
    bearish = sum(1 for r in results if r["signal"] == "bearish")
    neutral = sum(1 for r in results if r["signal"] == "neutral")
    total = len(results)

    avg_conf = sum(r["confidence"] for r in results) / total
    avg_pct = sum(r["price_change_pct"] for r in results) / total

    if bullish >= 3:
        fused = "bullish"
        conf = min(95, int(avg_conf * (bullish / total) * 1.2))
    elif bearish >= 3:
        fused = "bearish"
        conf = min(95, int(avg_conf * (bearish / total) * 1.2))
    elif bullish > bearish:
        fused = "bullish"
        conf = int(avg_conf * 0.8)
    elif bearish > bullish:
        fused = "bearish"
        conf = int(avg_conf * 0.8)
    else:
        fused = "neutral"
        conf = int(avg_conf * 0.7)

    all_lows = [r["forecast_low"] for r in results if r["forecast_low"] > 0]
    all_highs = [r["forecast_high"] for r in results if r["forecast_high"] > 0]

    support = max(all_lows) if all_lows else 0
    resistance = min(all_highs) if all_highs else 0

    return {
        "signal": fused, "confidence": conf,
        "avg_price_change_pct": round(avg_pct, 2),
        "support": round(support, 2), "resistance": round(resistance, 2),
        "vote": f"{bullish}🔴 {neutral}⚪ {bearish}🟢",
        "details": {"bullish": bullish, "neutral": neutral, "bearish": bearish}
    }


def run_model(model_name: str, symbol: str, bar: str) -> Dict:
    """Run a single model and return result"""
    try:
        if model_name == "kronos":
            from kronos_adapter import KronosAdapter
            adapter = KronosAdapter()
            return adapter.predict(symbol, bar=bar, lookback=400, pred_len=24)
        elif model_name == "chronos-base":
            from chronos_adapter import ChronosAdapter
            adapter = ChronosAdapter("chronos-t5-base")
            return adapter.predict(symbol, bar=bar, lookback=128, pred_len=24)
        elif model_name == "chronos-2":
            from chronos_adapter import ChronosAdapter
            adapter = ChronosAdapter("chronos-2")
            return adapter.predict(symbol, bar=bar, lookback=512, pred_len=24)
        elif model_name == "chronos-small":
            from chronos_adapter import ChronosAdapter
            adapter = ChronosAdapter("chronos-t5-small")
            return adapter.predict(symbol, bar=bar, lookback=64, pred_len=24)
        elif model_name == "timesfm":
            from timesfm_adapter import TimesFMAdapter
            adapter = TimesFMAdapter("timesfm-2.5-200m")
            return adapter.predict(symbol, bar=bar, lookback=256, pred_len=24)
        elif model_name == "timesfm-fin":
            from timesfm_adapter import TimesFMAdapter
            adapter = TimesFMAdapter("timesfm-1.0-200m-fin")
            return adapter.predict(symbol, bar=bar, lookback=256, pred_len=24)
        elif model_name == "moirai":
            from moirai_adapter import MOIRAIAdapter
            adapter = MOIRAIAdapter()
            return adapter.predict(symbol, bar=bar, lookback=256, pred_len=24)
        elif model_name == "finbert":
            from finbert_adapter import FinBERTAdapter
            adapter = FinBERTAdapter("finbert-base")
            return adapter.predict(symbol, bar=bar, lookback=24, pred_len=24)
        elif model_name == "finbert-crypto":
            from finbert_adapter import FinBERTAdapter
            adapter = FinBERTAdapter("finbert-crypto")
            return adapter.predict(symbol, bar=bar, lookback=24, pred_len=24)
        else:
            return {
                "model": model_name, "signal": "neutral", "confidence": 30,
                "reasoning": f"Unknown model: {model_name}",
                "current_price": 0, "forecast_price": 0, "price_change_pct": 0
            }
    except Exception as e:
        return {
            "model": model_name, "signal": "neutral", "confidence": 30,
            "reasoning": f"Error: {str(e)[:100]}",
            "current_price": 0, "forecast_price": 0, "price_change_pct": 0,
            "trend_strength": 0, "forecast_low": 0, "forecast_high": 0,
            "up_bars": 0, "total_bars": 0
        }


def print_report(symbol: str, bar: str, results: List[Dict], fused: Dict, 
                 prices: Dict, show_social: bool = False, show_risk: bool = True):
    """Print full team report with MANDATORY risk gate status"""
    emoji = {"bullish": "🟢", "bearish": "🔴", "neutral": "⚪"}
    f_emoji = emoji.get(fused["signal"], "⚪")

    print("=" * 62)
    print(f"🤖 AI 模型预测团队报告 — {symbol} ({bar})")
    print(f"   生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 62)

    print(f"\n【综合信号】{f_emoji} {fused['signal'].upper()} | 置信度: {fused['confidence']}/100")
    print(f"【模型投票】{fused['vote']}")
    print(f"【平均预测变化】{fused['avg_price_change_pct']:+.2f}%")
    print(f"【关键价位】支撑: ${fused['support']} | 阻力: ${fused['resistance']}")

    # ============ MANDATORY RISK GATE STATUS ============
    if show_risk and "risk_status" in fused:
        print_risk_status(fused["risk_status"])
        
        # Show risk gate decision
        if not fused.get("risk_gate_passed", True):
            print(f"\n  🔴 风控闸门: 阻止交易")
            print(f"     原因: {fused.get('risk_gate_reason', 'Unknown')}")

    # Social sentiment
    if show_social:
        print_social_sentiment(symbol)

    print(f"\n{'━' * 62}")
    print(f"{'模型':<25} {'机构':<12} {'信号':<10} {'置信度':<8} {'预测变化'}")
    print(f"{'━' * 62}")
    for r in results:
        m_emoji = emoji.get(r["signal"], "⚪")
        pct = r.get("price_change_pct", 0)
        cur = r.get("current_price", 0)
        fcast = r.get("forecast_price", 0)
        chg = f"{pct:+.2f}%" if cur and fcast else "N/A"
        print(f"{r['model']:<25} {r.get('institution',''):<12} "
              f"{m_emoji}{r['signal']:<8} {r['confidence']:>5}/100  {chg}")

    print(f"\n{'━' * 62}")
    print("【各模型详细意见】")
    for r in results:
        m_emoji = emoji.get(r["signal"], "⚪")
        print(f"\n  {m_emoji} {r['model']} ({r.get('institution','')}, {r.get('params','')})")
        print(f"     信号: {r['signal']} ({r['confidence']}/100)")
        print(f"     {r.get('reasoning', 'N/A')[:100]}")

    print(f"\n{'=' * 62}")
    print("⚠️  仅供参考，不构成投资建议。模型预测存在不确定性。")
    print("=" * 62)


def main():
    parser = argparse.ArgumentParser(description="AI Model Prediction Team")
    parser.add_argument("symbol", help="交易对，如 BTC-USDT-SWAP")
    parser.add_argument("--timeframe", "--tf", default="4H", help="周期 (默认: 4H)")
    parser.add_argument("--models", default="kronos,chronos-base,chronos-small,timesfm",
                        help="逗号分隔的模型列表")
    parser.add_argument("--signal-only", "-s", action="store_true", help="只输出信号")
    parser.add_argument("--json", "-j", action="store_true", help="JSON格式输出")
    parser.add_argument("--social", action="store_true", help="显示社会情绪分析")
    parser.add_argument("--equity", type=float, default=10000.0, help="当前资金 (默认: 10000)")
    parser.add_argument("--position", type=float, default=0.1, help="建议仓位百分比 (default: 0.1)")
    args = parser.parse_args()

    model_list = [m.strip() for m in args.models.split(",")]

    # Get current prices
    import requests
    for inst in [args.symbol, f"{args.symbol}-SWAP"]:
        url = f"{OKX_BASE}/market/ticker"
        r = requests.get(url, params={"instId": inst}, timeout=10)
        d = r.json()
        if d.get("code") == "0" and d.get("data"):
            current_price = float(d["data"][0]["last"])
            break
    else:
        current_price = 0

    print(f"\n🔄 运行AI模型团队 ({len(model_list)}个模型)...")
    results = []
    for mn in model_list:
        print(f"  ▶ {mn}...", end=" ", flush=True)
        r = run_model(mn, args.symbol, args.timeframe)
        results.append(r)
        status = "✅" if "Error" not in r.get("reasoning","") else "❌"
        print(f"{status} {r['signal']} ({r['confidence']}%)")

    # ============ MANDATORY: Fuse signals ============
    fused = fuse_signals(results)
    
    # ============ MANDATORY: Apply risk gate ============
    # ALL signals MUST pass through risk gate
    fused_with_risk = apply_risk_gate(
        fused_signal=fused,
        current_equity=args.equity,
        proposed_position_pct=args.position
    )

    if args.json:
        output = {
            "symbol": args.symbol, "timeframe": args.timeframe,
            "timestamp": datetime.now().isoformat(),
            "fused": fused_with_risk,  # Already includes risk gate result
            "models": results,
            "current_price": current_price,
            "risk_gate_passed": fused_with_risk["risk_gate_passed"],
            "risk_gate_decision": fused_with_risk["risk_gate_decision"],
            "risk_gate_reason": fused_with_risk["risk_gate_reason"]
        }
        if args.social and SOCIAL_AVAILABLE:
            currency = args.symbol.split("-")[0] if "-" in args.symbol else args.symbol
            try:
                output["social_sentiment"] = get_social_sentiment(currency)
            except Exception as e:
                output["social_sentiment"] = {"error": str(e)}
        print(json.dumps(output, ensure_ascii=False, indent=2))
    elif args.signal_only:
        emoji = {"bullish": "🟢", "bearish": "🔴", "neutral": "⚪"}
        f_emoji = emoji.get(fused_with_risk["signal"], "⚪")
        risk_status = "🔴" if not fused_with_risk["risk_gate_passed"] else "✅"
        print(f"\n{f_emoji} 综合: {fused_with_risk['signal']} ({fused_with_risk['confidence']}/100)")
        print(f"   投票: {fused_with_risk['vote']}")
        print(f"   {risk_status} 风控: {fused_with_risk['risk_gate_decision']}")
        if not fused_with_risk["risk_gate_passed"]:
            print(f"   原因: {fused_with_risk['risk_gate_reason']}")
        for r in results:
            m_e = emoji.get(r["signal"], "⚪")
            print(f"   {m_e} {r['model']}: {r['signal']} ({r['confidence']}%)")
    else:
        print_report(args.symbol, args.timeframe, results, fused_with_risk,
                    {"current": current_price}, show_social=args.social, show_risk=True)


if __name__ == "__main__":
    main()
