---
name: daily-review-dashboard
description: Manage Steven's daily subjective review (复盘) dashboard. Triggers on: (1) "复盘看板", "每日复盘", "主观复盘", (2) Steven submitting daily review content, (3) reviewing trading issues, mistakes, or emotions, (4) updating sentiment tags, problem tracking, or next-day plans. Reads and writes to the review system under review_egg/.
---

# Daily Review Dashboard

## Dashboard Location
`review_egg/dashboard/index.html` — 复盘看板，双击用浏览器打开

## Core Data Files

| File | Purpose |
|------|---------|
| `review_egg/dashboard/index.html` | Dashboard HTML (self-contained, stores DATA in JS) |
| `review_egg/今日复盘-YYYY-MM-DD.md` | Daily review raw text |
| `review_egg/review_index.jsonl` | Structured review index (JSONL, one line per day) |
| `review_egg/review_summary.csv` | CSV summary of all reviews |
| `review_egg/dashboard_data/summary.json` | Aggregated stats (issue counts, streaks) |
| `review_egg/dashboard_data/issues_tracker.json` | Issue tracking list |

## Data Schema (reviews array in HTML DATA object)

```json
{
  "date": "2026-03-18",
  "review_id": "review_20260318",
  "market_summary": "阳光电源持仓浮盈...",
  "biggest_gain": "...",
  "biggest_loss": "...",
  "top_issue": "...",
  "tags": ["买点错误", "无逻辑买入"],
  "sentiment_tags": ["反省", "冲动"],
  "daily_return_pct": 2.74,
  "trade_count": 1,
  "positions_count": 1,
  "open_positions": "阳光电源 300股",
  "issue_recurrence_count": 1,
  "issue_category": "冲动交易",
  "linked_trades": ["300274"],
  "next_plan": "兆易创新若回调至支撑可轻仓试探...",
  "original_text": "1. 阳光电源清仓...\n2. 艾罗能源...\n3. 兆易创新...",
  "holdings": [
    {
      "name": "阳光电源",
      "symbol": "300274",
      "quantity": 300,
      "cost": 163.16,
      "current_price": 166.59,
      "unrealized_pnl": 1029,
      "unrealized_pnl_pct": 2.10
    }
  ]
}
```

## Standard Workflows

### Opening the Dashboard
```bash
open ~/.openclaw/workspace/review_egg/dashboard/index.html
```

### Adding a New Daily Review
1. Write raw text to `review_egg/今日复盘-YYYY-MM-DD.md`
2. Append structured entry to `review_egg/review_index.jsonl`
3. Append summary row to `review_egg/review_summary.csv`
4. Update `review_egg/dashboard_data/summary.json` (issues_summary, daily_returns, totals)
5. Update `review_egg/dashboard_data/issues_tracker.json` if new issues
6. Update `review_egg/dashboard/index.html` DATA object:
   - Add to `reviews[]` array
   - Add to `daily_returns[]`
   - Update totals (total_reviews, avg_daily_return, etc.)
7. Run `open review_egg/dashboard/index.html`

### Dashboard Sections
The dashboard has these sections (in order):
1. 总览卡片（复盘次数、收益率、问题统计、连胜）
2. 📈 每日收益率柱状图
3. ⚠️ 问题出现统计
4. 💼 持股状况（from `holdings[]`）
5. 📄 复盘原文（from `original_text`）
6. 📋 复盘历史（structured summary cards）

### Key Rules
- **原文** stored in `original_text` field — displayed verbatim
- **结构化摘要** from fields (biggest_gain, top_issue, tags, etc.)
- **持股状况** from `holdings[]` — only shows latest date with holdings
- No field = don't fabricate; leave empty
- Problem tags: 追高, 卖飞, 拿不住盈利单, 频繁交易, 情绪化交易, 不止损, 仓位过重, 买点错误, 无逻辑买入

## Update Checklist
After receiving new review from Steven:
- [ ] `review_egg/今日复盘-YYYY-MM-DD.md` (raw text)
- [ ] `review_egg/review_index.jsonl` (append JSONL)
- [ ] `review_egg/review_summary.csv` (append CSV row)
- [ ] `review_egg/dashboard_data/summary.json` (update aggregates)
- [ ] `review_egg/dashboard_data/issues_tracker.json` (new issues)
- [ ] `review_egg/dashboard/index.html` (update DATA object)

## Separation from Trade System
Steven's daily review = subjective (复盘) ≠ trade records (交易流水)
- **review_egg/** = Steven's personal reflection system
- **trade/** = objective trading ledger
- Do NOT mix content between the two systems
