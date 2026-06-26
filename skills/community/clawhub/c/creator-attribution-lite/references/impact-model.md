# Lightweight Impact Model

Use 0-100 composite scoring.

`impact_score = (engagement_quality * 0.35) + (intent_signal * 0.30) + (conversion_signal * 0.35)`

## Inputs
- engagement_quality: watch %, saves, shares
- intent_signal: profile clicks, link clicks, comments with purchase intent
- conversion_signal: leads, checkouts, GMV events

## Decision bands
- 75-100: scale
- 50-74: optimize and retest
- <50: pause or redesign
