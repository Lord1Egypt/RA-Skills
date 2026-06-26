---
name: early_setup_finder
description: Pre-pump fingerprint scanner. Identifies assets showing accumulation signals before a price move using the 8-signal framework.
version: 0.1.0
license: MIT-0
metadata:
  author: 0xzahra
  keywords: [trading, crypto, pre-pump, analysis, on-chain, accumulation, signals]
---

# Early Setup Finder

This skill scans for assets exhibiting pre-pump accumulation signals using the 8-signal fingerprint framework developed from tracking ZEC, TAO, HYPE, and other breakout candidates.

## When to use this skill

Use `early_setup_finder` when a user asks for early-stage trading setups, pre-pump candidates, or wants to run the fingerprint check on a specific token.

## The 8-Signal Pre-Pump Fingerprint

1. **Volume accumulation without price explosion** — volume rising while price stays flat
2. **Higher lows on weekly, no fanfare** — structure improving silently
3. **Low social noise but rising on-chain activity** — the gap between narrative and reality
4. **Smart money wallets quietly building positions** — whale accumulation detected
5. **Exchange supply declining week over week** — tokens moving off exchanges
6. **RSI resetting from oversold on the daily** — momentum resetting
7. **Quiet catalyst sitting offscreen** — upgrade, listing, partnership not yet priced in
8. **DEX bid depth thinning relative to 30-day average** — liquidity compression means path of least resistance is up

## Instructions

1. Ask the user for the token name/contract and chain, or offer to scan the current market.
2. For each signal, gather data:
   - Volume: compare 7-day average to 30-day average
   - Structure: check weekly chart for higher lows
   - Social vs on-chain: compare CT/social mentions to on-chain transaction count
   - Smart money: check top holder changes on block explorer
   - Exchange supply: check exchange inflow/outflow data
   - RSI: check daily RSI position
   - Catalysts: search for upcoming events (upgrades, listings, partnerships)
   - DEX liquidity: check bid depth relative to 30-day average (ratio below 0.5 = compression)
3. Score: count how many of 8 signals are active (5+ = strong setup)
4. Return the analysis in this format:

**Token:** [name]
**Signal Score:** X/8
**Active Signals:** (list which ones)
**Key Level:** (entry zone if identifiable)
**Risk Note:** (one specific risk for this setup)
**Psychology Trap:** (one cognitive bias to watch for this specific trade)

5. Always end with: **NFA — probabilistic only.**

## Important Rules

- Never skip the risk note or psychology trap
- Always include signal 8 (DEX liquidity) — it was identified as a critical missing signal by @cicadafinanceintern on Moltbook
- If fewer than 3 signals are active, clearly state the setup is weak
- Do not fabricate on-chain data — if you cannot verify a signal, state it as unconfirmed
