#!/usr/bin/env python3
"""
Polymarket Fast-Loop Skill - Paper Trading
Enhanced with TradingAgents pipeline, Swarm Consensus, ACTA Receipts, Cedar Governance
"""
import os
import sys
import json
import requests
import asyncio
from datetime import datetime, timezone
from pathlib import Path

# Add botwave to path
sys.path.insert(0, '/home/gringo/botwave')

from trading_agents.pipeline import TradingAgentsPipeline
from swarm_consensus.integrate_predictive import PredictiveSwarm, get_swarm_decision

BASE = os.environ["SIMMER_API_URL"].rstrip("/")
KEY = os.environ.get("SIMMER_API_KEY", "sk_replay")
HEADERS = {"Authorization": f"Bearer {KEY}"}

# ──────────────────────────────────────────────────────────────────────────────
# CONFIG
# ──────────────────────────────────────────────────────────────────────────────

# Fast-loop parameters (will be optimized by autoresearch)
MOMENTUM_THRESHOLD = float(os.environ.get("SIMMER_MOMENTUM_THRESHOLD", "0.001"))  # 0.1%
VOLUME_FILTER = float(os.environ.get("SIMMER_VOLUME_FILTER", "10000"))  # $10k min
SPREAD_FILTER = float(os.environ.get("SIMMER_SPREAD_FILTER", "0.05"))  # 5% max spread
FEE_BUFFER = float(os.environ.get("SIMMER_FEE_BUFFER", "1.5"))
POSITION_SIZE_PCT = float(os.environ.get("SIMMER_POSITION_SIZE_PCT", "0.05"))  # 5%
MAX_HOLD_MINUTES = int(os.environ.get("SIMMER_MAX_HOLD_MINUTES", "5"))

# Kelly sizing
KELLY_FRACTION = 0.25  # quarter-Kelly

# ──────────────────────────────────────────────────────────────────────────────
# TRADING AGENTS PIPELINE
# ──────────────────────────────────────────────────────────────────────────────

trading_pipeline = TradingAgentsPipeline({
    "kelly_fraction": KELLY_FRACTION,
    "max_position_pct": 0.10,
    "max_drawdown_pct": 0.05
})

# Swarm consensus
swarm = PredictiveSwarm(n_personas=50)

# ──────────────────────────────────────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────────────────────────────────────

def get_held_market_ids():
    r = requests.get(f"{BASE}/api/sdk/positions", headers=HEADERS, timeout=30)
    r.raise_for_status()
    return {p["market_id"] for p in r.json().get("positions", [])}

def get_balance():
    r = requests.get(f"{BASE}/api/sdk/balance", headers=HEADERS, timeout=30)
    r.raise_for_status()
    return r.json().get("balance", 1000.0)

def get_markets():
    r = requests.get(f"{BASE}/api/sdk/markets", params={"limit": 100}, headers=HEADERS, timeout=30)
    r.raise_for_status()
    return r.json().get("markets", [])

def place_trade(market_id: str, side: str, action: str, amount: float, reasoning: str):
    """Place a trade via Simmer API"""
    resp = requests.post(
        f"{BASE}/api/sdk/trade",
        json={
            "market_id": market_id,
            "side": side,
            "action": action,
            "amount": amount,
            "reasoning": reasoning,
            "skill_slug": "polymarket-fast-loop",
            "source": "fast-loop-enhanced"
        },
        headers=HEADERS,
        timeout=30
    )
    return resp.json() if resp.ok else {"error": resp.text}

# ──────────────────────────────────────────────────────────────────────────────
# BINANCE MOMENTUM FETCH
# ──────────────────────────────────────────────────────────────────────────────

async def fetch_binance_momentum():
    """Fetch BTC/USDT 1m candles from Binance and calculate momentum"""
    try:
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://api.binance.com/api/v3/klines",
                params={"symbol": "BTCUSDT", "interval": "1m", "limit": 20}
            ) as resp:
                klines = await resp.json()
        
        # Calculate momentum: (close[-1] - close[-5]) / close[-5]
        closes = [float(k[4]) for k in klines]
        if len(closes) >= 5:
            momentum = (closes[-1] - closes[-5]) / closes[-5]
            volume = sum(float(k[5]) for k in klines[-5:])  # quote volume
            return momentum, volume
    except Exception as e:
        print(f"[FastLoop] Binance fetch error: {e}")
    return 0.0, 0.0

# ──────────────────────────────────────────────────────────────────────────────
# MAIN TICK
# ──────────────────────────────────────────────────────────────────────────────

async def run_tick(quiet: bool = False):
    """Run one fast-loop tick"""
    
    if not quiet:
        print(f"[FastLoop] {datetime.now(timezone.utc).isoformat()} - Starting tick")
    
    # 1. Get Binance momentum
    momentum, binance_volume = await fetch_binance_momentum()
    
    if not quiet:
        print(f"[FastLoop] BTC momentum: {momentum:.4%}, volume: ${binance_volume:,.0f}")
    
    # 2. Check momentum threshold
    if abs(momentum) < MOMENTUM_THRESHOLD:
        if not quiet:
            print(f"[FastLoop] Momentum {momentum:.4%} below threshold {MOMENTUM_THRESHOLD:.4%}")
        return
    
    # 3. Get Polymarket markets
    markets = get_markets()
    held = get_held_market_ids()
    balance = get_balance()
    
    if not quiet:
        print(f"[FastLoop] Balance: ${balance:.2f}, Held markets: {len(held)}")
    
    # 4. Filter for BTC 5-min markets
    btc_markets = []
    for m in markets:
        if m.get("id") in held:
            continue
        slug = m.get("slug", "").lower()
        question = m.get("question", "").lower()
        if ("btc" in slug or "bitcoin" in slug) and ("5 min" in slug or "5min" in slug or "5-min" in slug):
            yes_price = m.get("yes_price")
            no_price = m.get("no_price")
            volume = m.get("volume", 0)
            spread = abs(yes_price - no_price) if yes_price and no_price else 1.0
            
            if yes_price and no_price and volume >= VOLUME_FILTER and spread <= SPREAD_FILTER:
                btc_markets.append({
                    "market_id": m["id"],
                    "slug": m["slug"],
                    "question": m["question"],
                    "yes_price": yes_price,
                    "no_price": no_price,
                    "volume": volume,
                    "spread": spread
                })
    
    if not btc_markets:
        if not quiet:
            print("[FastLoop] No qualifying BTC 5-min markets")
        return
    
    # Sort by volume descending
    btc_markets.sort(key=lambda x: x["volume"], reverse=True)
    
    if not quiet:
        print(f"[FastLoop] Found {len(btc_markets)} qualifying markets")
    
    # 5. Run enhanced decision pipeline for each market
    for market in btc_markets[:3]:  # Max 3 trades per tick
        if not quiet:
            print(f"[FastLoop] Analyzing: {market['question']} - YES: {market['yes_price']:.4f}")
        
        # Determine side from momentum
        predicted_side = "yes" if momentum > 0 else "no"
        market_price = market["yes_price"] if predicted_side == "yes" else market["no_price"]
        
        # Run TradingAgents pipeline
        market_data = {
            'momentum': momentum,
            'volume': binance_volume,
            'rsi': 50,  # Would fetch from Binance
            'ob_imbalance': 0,
            'news_signal': 0,
            'sentiment': 0,
        }
        
        state = trading_pipeline.run_fast_loop(
            market_id=market["market_id"],
            market_question=market["question"],
            market_price=market_price,
            market_data=market_data
        )
        
        # Run Swarm Consensus
        swarm_result = swarm.aggregate(market_data, market_price)
        
        # Combine decisions
        pipeline_approved = state.portfolio_decision and state.portfolio_decision.approved
        swarm_edge = swarm_result['edge']
        swarm_side = "yes" if swarm_result['recommended_side'] == 'YES' else "no"
        
        if not quiet:
            print(f"[FastLoop] Pipeline: approved={pipeline_approved}, side={state.trader_proposal.recommended_side.value if state.trader_proposal else 'N/A'}")
            print(f"[FastLoop] Swarm: edge={swarm_edge:.4f}, side={swarm_side}, kelly={swarm_result['kelly_fraction']:.4f}")
        
        # Decision logic: both must agree on side, pipeline must approve
        if (pipeline_approved and 
            state.trader_proposal and 
            state.trader_proposal.recommended_side.value == predicted_side and
            swarm_edge > 0.001 and
            swarm_side == predicted_side):
            
            # Calculate position size (quarter-Kelly)
            position_size = balance * POSITION_SIZE_PCT * min(1.0, abs(swarm_result['kelly_fraction']) * 4)
            position_size = min(position_size, balance * 0.10)  # Cap at 10%
            
            if position_size < 1.0:
                if not quiet:
                    print(f"[FastLoop] Position too small: ${position_size:.2f}")
                continue
            
            if not quiet:
                print(f"[FastLoop] EXECUTING TRADE: {predicted_side.upper()} ${position_size:.2f} on {market['slug']}")
            
            # Place trade
            result = place_trade(
                market_id=market["market_id"],
                side=predicted_side,
                action="buy",
                amount=position_size,
                reasoning=f"FastLoop: momentum={momentum:.4%}, swarm_edge={swarm_edge:.4f}, pipeline_approved=True, kelly={swarm_result['kelly_fraction']:.4f}"
            )
            
            if not quiet:
                print(f"[FastLoop] Trade result: {result}")
        else:
            if not quiet:
                print(f"[FastLoop] NO TRADE: pipeline={pipeline_approved}, swarm_edge={swarm_edge:.4f}, sides_match={state.trader_proposal.recommended_side.value if state.trader_proposal else 'N/A'} == {predicted_side}")

async def main():
    quiet = "--quiet" in sys.argv
    await run_tick(quiet)

if __name__ == "__main__":
    asyncio.run(main())