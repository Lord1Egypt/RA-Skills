---
name: financial-market-risk-analysis
description: "Analyze financial markets, FX, investments, macro context, and risk with concise uncertainty-aware framing."
license: "MIT"
---

# Financial Market Risk Analysis

Use for investment, FX, cryptocurrency, Chile-market, macro, S&P 500, financial-news, or portfolio-risk analysis.

## Core Workflow

1. Identify asset, market, horizon, currency, and risk tolerance.
2. Pull current data when the question depends on price, news, rates, laws, or market state.
3. Separate facts, scenarios, and judgment.
4. Frame conclusions as risk/reward, not certainty.
5. Keep output concise unless detail is requested.

## Required Context

- Chile macro: use `mindicador.cl/api` as quick context when relevant.
- Chile official series: search the BCCh/SI3 catalog if available; prefer official sources for conclusions.
- USD/CLP: check observed dollar, SII, trend/history, projections, and local/global event risk.
- News: include public or authorized content from FT, WSJ, Bloomberg, Diario Financiero, and El Mercurio Inversiones when relevant.
- Markets: include Chile/IPSA and S&P 500 as local/global risk context when relevant.

## Guardrails

- Never guarantee returns, timing, or "best entry".
- Use staged-buying language for timing calls: partial buys, tranches, watch zones.
- Do not bypass paywalls.
- State source limits, stale data, and uncertainty.

## Bilingual Output

- Match the user's language.
- If asked for bilingual output, provide Spanish first, then English.

## References

Load `references/methodology.md` for detailed source and signal rules.
