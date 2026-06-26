---
description: Generate a weekly marketing performance report from Search Console, Analytics, and ad platform data. User pastes CSV exports or Claude pulls via computer use.
disable-model-invocation: true
---

# Weekly Marketing Report

Read the user's business profile for average job size (used to calculate dollar value of ranking changes).

## Data sources
Ask the user to paste data, or offer to pull it via computer use:
- Google Search Console: Performance > Last 7 days > Export CSV
- Google Analytics 4: Reports > Acquisition > Traffic acquisition > Last 7 days > Export
- Meta Ads Manager: Campaigns > Last 7 days > Performance and Clicks > Export CSV
- Google Ads: Campaigns > Last 7 days > Download CSV

## Report format

### 3 Things That Matter This Week
Only genuinely important changes. If nothing moved: "Steady week, nothing to act on."

### Traffic
| Metric | This Week | Last Week | Change |
Clicks, impressions, CTR, avg position. Sessions, users, bounce rate.

### SEO
**Keyword Winners** (improved 3+ spots): keyword, position, change, clicks, opportunity
**Keyword Losers** (dropped 3+ spots): keyword, position, change, what happened (diagnose why)
**Striking Distance** (positions 4-10): keyword, position, specific action to take

### Ads (if data provided)
| Metric | This Week | Last Week | Target |
Spend, leads, CPL, jobs booked, revenue, ROAS

**Creative scorecard:** each ad with spend, leads, CPL, CTR, verdict (SCALE/KEEP/KILL/TEST)

### This Week's To-Do
3 specific tasks ranked by impact. Name the page, the keyword, and what to change.

## Rules
- Never pad with filler. Short weeks get short reports.
- Never report impressions unless asked.
- Calculate dollar value: "(ranking improvement for [keyword]) could mean X additional clicks/mo at your $Y avg job size = $Z potential revenue"
- Flag ROAS below 3x for 2 consecutive weeks.
