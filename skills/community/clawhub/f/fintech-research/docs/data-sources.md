# Data Sources

All data sources are 100% free with zero subscription required.

## P0 — Core (Implemented)

### yfinance
- **Source**: Yahoo Finance public data via yfinance Python library
- **Free basis**: Open-source library (MIT) accessing publicly available market data
- **Coverage**: Global equities, including `.HK` suffix for HKEX-listed stocks
- **Rate limit**: Reasonable frequency; no hard limit
- **Cache**: SQLite, 1h (price) to 24h (fundamentals) TTL
- **HK support**: Yes — all HKEX stocks via `.HK` suffix

### HKEX Disclosure
- **Source**: HKEX News (www1.hkexnews.hk)
- **Free basis**: Official exchange disclosure platform, public access
- **Coverage**: All HKEX company announcements, filings, circulars
- **Rate limit**: 2s between scrape requests
- **Cache**: 4h TTL
- **HK support**: Yes — primary HK regulatory data

## P1 — Macro (Implemented)

### FRED (Federal Reserve Economic Data)
- **Source**: fred.stlouisfed.org
- **Free basis**: Free official API provided by the Federal Reserve Bank of St. Louis
- **Coverage**: US interest rates, FX rates, inflation, employment, GDP
- **Rate limit**: 120 requests per minute
- **Cache**: 24h TTL
- **HK support**: N/A — macro data is country-level; HK macro via HKMA

### HKMA (Hong Kong Monetary Authority)
- **Source**: hkma.gov.hk
- **Free basis**: Public statistics published by HKMA
- **Coverage**: HK base rate, aggregate balance, FX reserves, HKD money supply
- **Rate limit**: 2s between requests
- **Cache**: 24h TTL
- **HK support**: Yes — HK-specific monetary data

## P2 — Enhancement

### NewsAPI
- **Source**: newsapi.org
- **Free basis**: Free tier (100 requests per day)
- **Coverage**: Global English-language news headlines
- **Rate limit**: 100/day on free tier
- **Cache**: 30min TTL
- **HK support**: Yes — covers HK financial news in English

### RSS Feeds
- **Source**: Public financial RSS feeds (e.g., Reuters, Bloomberg, HKEX)
- **Free basis**: RSS is an open web standard
- **Coverage**: Breaking news, earnings announcements, regulatory updates
- **Rate limit**: Respectful polling (5-15 min intervals)
- **Cache**: 15min TTL
- **HK support**: Yes — HKEX and local financial RSS feeds supported

## P3 — Fallback

### East Money (东方财富)
- **Source**: eastmoney.com
- **Free basis**: Public web data
- **Coverage**: A-share and HK stock data, research reports
- **Rate limit**: 2s between requests
- **Cache**: 1h TTL
- **HK support**: Yes — HK stock pages available
- **Status**: Fallback only — scraping resilience not guaranteed

### Sina Finance
- **Source**: finance.sina.com.cn
- **Free basis**: Public web data
- **Coverage**: HK stock quotes, A+H spreads, news
- **Rate limit**: 2s between requests
- **Cache**: 1h TTL
- **HK support**: Yes — HK real-time quotes available
- **Status**: Fallback only — scraping resilience not guaranteed

## Data Coverage Matrix

| Capability | US | HK | Source |
|------------|----|----|--------|
| Price/Quote | Yes | Yes | yfinance |
| Fundamentals | Yes | Yes | yfinance |
| Filings/Announcements | SEC EDGAR | HKEX News | Free official APIs |
| Macro (Rates/FX/GDP) | Yes | Limited | FRED + HKMA |
| News Headlines | Yes | Yes | NewsAPI + RSS |
| AH Spread | N/A | Yes | yfinance (dual-listed) |
| Short Interest | Yes | Yes | yfinance (where available) |
| Ownership/Connect Flow | No | Yes | HKEX News |
| Earnings Calendar | Yes | Limited | yfinance + fiscal_calendar |
| Historical Dividends | Yes | Yes | yfinance |
