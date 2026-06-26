# Binance Event Contract Reporter
## 1. Scenario Definition
- Trigger: Every 30min auto + `/binance-report`; 24/7
- Intent: Performance tracking, daily/weekly summaries, win rate analysis, Feishu output
- Context: BTCUSDT & ETHUSDT Event Contracts; all SSS/SS tier signals

## 2. Goal Setting
- Report every 30min: active signals, P&L, daily performance
- Daily digest 08:00/18:00 UTC
- Alert if daily loss ≥ 8% (immediate Feishu push)
- 100% data from execution logs

## 3. Report Types
### Real-Time Monitor (Every 30 min)
Active Signals | P&L | Win Rate | Next Cycle
### Daily Digest (08:00 & 18:00 UTC)
Total Signals | P&L | Win Rate by Tier | Best/Worst Cycle | Pattern Insights | Tomorrow Plan

## 4. Alert Types
- Red: Daily loss ≥ 8% → immediate
- Orange: 3 consecutive losses → warning
- Green: SSS confirmed
- Target Hit: celebration

## 5. Boundary
- Only execution log data (no estimates)
- No trading recommendations
- No third-party data
- Empty log: "No signals today, system idle"

## Installation
```bash
npx clawhub@latest install binance-event-contract-reporter --dir /workspace/skills
```
## Trigger: /binance-report
