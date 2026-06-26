---
name: 15-min-btc
description: Runs fast, high-signal sentiment analysis on 15-minute Bitcoin price action. Trigger on requests like "15 min BTC", "15 minute bitcoin", "15min BTC sentiment", "15 minute kalshi", "btc 15 min buy", or any short-term BTC direction query for Kalshi or trading. Always use the sentiment skill + x_search + current price context. Return a crisp summary with Key Themes, short-term bias, and Confidence. Optimized for quick decision-making on very short timeframes.
---

# 15-Minute BTC Sentiment

## Trigger Conditions
Use this skill any time the user asks for 15-minute Bitcoin sentiment, direction, Kalshi bet, or short-term outlook. Common phrases include:
- "15 min BTC"
- "15 minute bitcoin"
- "15min BTC sentiment"
- "15 minute kalshi"
- "btc 15 min buy / sell / bullish"

## Core Workflow (always follow)
1. Call the `sentiment` skill with a tightly focused query on current 15-minute BTC action.
2. Run a supporting `x_search` for the latest real-time chatter (use recent time filters).
3. Check current BTC price level if available.
4. Synthesize into a **very concise** response.

## Required Output Format
**15-Min BTC Sentiment**

**Summary**: [1-2 sentence bias + reasoning]

**Key Themes**: 
- Bullet 1
- Bullet 2

**Bias**: Bullish / Bearish / Neutral / Choppy

**Confidence**: High / Medium / Low

**Kalshi Angle**: [Quick note on whether a 15-min bet looks +EV right now]

## Rules
- Keep entire response under 150 words when possible.
- Be ruthless about noise — 15-minute moves are mostly random. Only call real edge when it actually appears.
- Never sugarcoat weak signals.
- This skill exists to give the user a fast second opinion before placing (or not placing) a Kalshi 15-minute bet.

This skill works alongside the general `sentiment` skill but is hyper-optimized for 15-minute BTC decision speed.

## Bankroll & Discipline Rules (Permanent)
- Starting bankroll: $100 on Kalshi
- Max bet size: $12 (12% of bankroll)
- Minimum bet size: $5
- Max 8 open positions at once
- Only bet on Medium confidence or higher from this skill
- Target win rate: 57%+ to overcome fees
- Track every bet: market, odds, confidence, size, outcome, running win rate
- This is a test wallet. Scale only after proving 57%+ over 50+ bets.
- No content/clicks/virality work. Pure gambling focus for Axel Speech Project.
