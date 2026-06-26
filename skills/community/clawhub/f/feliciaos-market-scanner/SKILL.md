---
name: market-scanner
description: Autonomous crypto market intelligence — macro read, technical analysis, pre-pump on-chain signals, risk management, and token watchlist. Built by FeliciaOS from Anambra, Nigeria.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - GROQ_API_KEY
    primaryEnv: GROQ_API_KEY
    envVars:
      - name: GROQ_API_KEY
        required: true
        description: Groq API key for LLaMA 3.3 70B inference.
    emoji: "📊"
    homepage: https://github.com/leodera-creator/feliciaos
---

# FeliciaOS Market Scanner

Performs deep crypto market intelligence analysis powered by LLaMA 3.3 70B.

## What it does
- Reads current market sentiment and BTC dominance
- Identifies key technical levels and trend direction
- Scans for pre-pump on-chain signals
- Provides stop-loss and position sizing guidance
- Returns 3-5 token watchlist with reasoning

## Usage
Install this skill, set your GROQ_API_KEY, then ask your agent:
- "Run a market scan"
- "Scan the market for BTC"
- "Give me a crypto market report"

## Output
Structured market intelligence report. Always ends with NFA disclaimer.

## Built by
Pascal Chidera (@chipasleo) — Anambra, Nigeria
Powered by FeliciaOS autonomous intelligence engine.
