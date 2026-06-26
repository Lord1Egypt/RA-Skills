---
id: 'einstein-research-ftd'
name: 'Follow-Through Day (FTD) Detector'
description: "Detects Follow-Through Day (FTD) signals for market bottom confirmation using William O'Neil's methodology. Dual-index tracking (S&P 500 + NASDAQ) with state machine for rally attempt, FTD qualification, and post-FTD health monitoring. Use when user asks about market bottom signals, follow-through days, rally attempts, re-entry timing after corrections, or whether it's safe to increase equity exposure. Complementary to market-top-detector (defensive) - this skill is offensive (bottom confirmation)."
version: '1.0.0'
author: 'DaVinci'
last_amended_at: null
trigger_patterns: []
pre_conditions:
  git_repo_required: false
  tools_available: []
expected_output_format: 'natural_language'
---

# Follow-Through Day (FTD) Detector

**Goal Chain**: L0 Medici Enterprises → L1 Einstein Research → L2 Market Timing

## Purpose

Detects Follow-Through Day (FTD) signals for market bottom confirmation using William O'Neil's methodology. This skill helps identify when it's safer to increase equity exposure after a market correction. It is the offensive counterpart to the defensive `market-top-detector` skill.

## How It Works

This skill implements a state machine that tracks the S&P 500 (SPY) and NASDAQ (QQQ) for signs of a market bottom.

**State Machine:**
1.  **Correction:** The market is in a downtrend. The skill is looking for a potential bottom.
2.  **Rally Attempt:** A significant up-day occurs after a new low, initiating a "rally attempt". The skill starts a day count.
3.  **FTD Watch:** Between days 4 and 10 of the rally attempt, the skill looks for a Follow-Through Day.
4.  **FTD Confirmed:** A valid FTD occurs. The market is considered to be in a "confirmed uptrend".
5.  **Post-FTD Monitoring:** The skill monitors the health of the confirmed uptrend for signs of failure (e.g., immediate sharp reversals).

## FTD Rules (O'Neil Methodology)

-   **Rally Attempt Start (Day 1):** The index closes higher after a new low, or holds above the low for a second day.
-   **FTD Qualification (Day 4-10):** A major index (SPY or QQQ) must close up **>1.5%** on higher volume than the previous day.
-   **Confirmation:** Both SPY and QQQ should ideally confirm the FTD within a day or two of each other for the strongest signal.
-   **Failure:** An FTD is considered failed if the index undercuts the low of the rally attempt day.

## Usage

This skill is run via a CLI tool, typically as part of a daily market analysis cron job.

```bash
# Run the FTD analysis for the latest market data
einstein-research ftd

# Output (example)
{
  "status": "FTD_CONFIRMED",
  "details": "Follow-Through Day confirmed on 2026-03-14 for SPY.",
  "spy": {
    "state": "FTD_CONFIRMED",
    "rally_attempt_start_date": "2026-03-10",
    "day_count": 5,
    "ftd_date": "2026-03-14",
    "ftd_price_change_pct": 1.8,
    "ftd_volume_change_pct": 25.1
  },
  "qqq": {
    "state": "FTD_WATCH",
    "rally_attempt_start_date": "2026-03-11",
    "day_count": 4,
    "ftd_date": null
  },
  "recommendation": "Market in confirmed uptrend. Consider increasing equity exposure cautiously. Monitor for confirmation on QQQ."
}
```

## Data Sources

-   **yfinance:** Daily OHLCV data for SPY and QQQ.
-   **Local Cache:** Data is cached locally to avoid redundant downloads.

## Integration

-   **Daily Cron:** Run `einstein-research ftd` after market close each day.
-   **Alerting:** If `status` changes to `RALLY_ATTEMPT` or `FTD_CONFIRMED`, send a notification to Omer.
-   **DaVinciOS Dashboard:** The output of this skill can be used to update a market-timing indicator on the main dashboard.

## When to Use

-   After a market correction of 10% or more.
-   When looking for a signal to start buying stocks again.
-   To confirm if a recent market bounce has strength.

This skill should be used in conjunction with other indicators (like market breadth, sentiment, and the `market-top-detector`) for a complete picture.
