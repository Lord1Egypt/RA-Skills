---
name: daily-options-plays-top-2-picks
description: Build a simple stock-options watchlist and paper-trade plan after the first 15 minutes of the market session. Use when the user wants a 9:45 AM ET scan, only the top 2 stock plays, clear entry/stop/target levels, 1-2 week near-the-money contract guidance, hourly check-in logic, or a no-hype paper-trading workflow with explicit risks and no guarantees.
---

# Daily Options Plays — Top 2 Picks

## Overview

Create a simple, disciplined options watchlist for beginners. Keep the output narrow: scan after 9:45 AM ET, rank setups, give only the best 2 plays, and translate each idea into a paper-trade plan with entry, stop, target, contract guidance, and a short plain-English thesis.

## Workflow

1. Run only on U.S. stock market trading days. Skip weekends and market holidays when the market is closed.
2. Wait until at least 9:45 AM ET for same-day trade ideas. Do not issue opening-drive signals in the first 15 minutes.
3. Review the user’s stock universe or use a small liquid default list if none is provided.
3. Score setups using price action, volume, trend, support/resistance, catalyst context, and market tone.
4. Return only the top 2 plays. Fewer is better if conviction is weak.
5. For each play, provide:
   - ticker and direction
   - entry
   - stop / invalidation
   - first target and stretch target when useful
   - confidence from 1-10
   - short rationale with key risk
   - 1-2 week near-the-money options guidance
6. Default to paper-trade-first language unless the user explicitly asks for live execution framing.
7. Re-check the watchlist roughly once per hour, not every few minutes, unless the user requests a live drill-down.

## Output Rules

- Keep the writeup concise and easy to scan.
- Prefer liquid large-cap names and obvious levels over exotic setups.
- Avoid more than 2 trade ideas in the final answer.
- If the market is messy, say no clean setup instead of forcing picks.
- Never promise outcomes. Use probability language.
- Explicitly mention that this is educational planning, not guaranteed financial advice.

## Contract Guidance

Translate the stock setup into beginner-friendly options guidance:

- Prefer calls for bullish ideas and puts for bearish ideas.
- Prefer near-the-money strikes.
- Prefer expirations about 1-2 weeks out.
- Avoid very short-dated contracts unless the user knowingly wants faster decay and higher risk.
- If implied volatility or liquidity looks problematic, say so and reduce confidence.

## Monitoring Philosophy

Use an hourly monitoring mindset by default:

- Check whether price is holding above/below the planned entry zone.
- Check whether stop or invalidation is close.
- Check whether the thesis still matches market tone and news.
- If price hits target 1, discuss partial-profit logic or stop tightening.
- If the thesis breaks, say exit or stand aside. Do not rationalize a bad setup.

## Recommended Response Shape

Use this structure when generating the watchlist:

- Market tone: 1-3 bullets
- Macro / News Context: explicitly say if it is an FOMC day, CPI day, earnings-heavy day, major geopolitical/world-event day, or if there is no major market-moving news
- Play 1
- Play 2
- No-trade note or risk note
- Paper-trade reminder

## References

Read `references/watchlist-framework.md` when you need the exact scan checklist, ranking criteria, or an example output format.