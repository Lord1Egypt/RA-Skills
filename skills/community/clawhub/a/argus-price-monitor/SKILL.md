---
name: Price Monitor & Daily Excel Report Bot
description: Monitors product prices across e-commerce sites daily, detects price drops, and emails a formatted Excel report automatically every morning.
version: 1.0.2
tags: [python, scraping, automation, excel, email, selenium, pandas]
author: neo1307
requires: [python3, selenium, webdriver-manager, pandas, openpyxl, chromium]
---

# Price Monitor & Daily Excel Report Bot

## Overview
Automated price tracking system that monitors products across competitor websites,
detects price drops, and delivers a formatted Excel report via email every morning at 8 AM.
Saves 3+ hours of manual work per day.

## What It Does
- Scrapes prices from target URLs using Selenium (handles JavaScript-rendered pages)
- Compares against previous day's prices automatically
- Highlights price drops >5% in red, increases in green inside Excel
- Emails formatted report to specified recipients on schedule
- Logs all runs with timestamps for auditing

## Required Environment Variables
Set these in OpenClaw's Secrets manager before running:

| Variable | Description | Example |
|----------|-------------|---------|
| `SMTP_HOST` | SMTP server hostname | `smtp.gmail.com` |
| `SMTP_PORT` | SMTP port number | `587` |
| `SMTP_USER` | Sender email address | `bot@gmail.com` |
| `SMTP_PASS` | Email password or app-specific password | `xxxx xxxx xxxx xxxx` |
| `REPORT_RECIPIENT` | Where to send the daily report | `manager@company.com` |

## Setup
1. Add target product URLs to `config/urls.txt` (one URL per line)
2. Set all environment variables above in OpenClaw Secrets
3. Set run schedule in OpenClaw: `daily at 08:00`
4. Chromium must be available on the host for Selenium headless mode

## Usage
> "Start monitoring prices for these URLs and email me a report every morning"
> "Check competitor prices and send Excel summary to manager@company.com"
> "Run price tracker now and show me today's drops"
> "Add this product URL to the monitoring list"

## Output
- `price_report_YYYY-MM-DD.xlsx` — color-coded Excel report
- Email with report attached sent to configured recipient
- Console summary: total products, drops found, errors

## Rules
- Never send more than 1 request per second to any domain
- Always save raw scraped data before processing (in `data/raw/`)
- If email delivery fails, save report to `data/reports/` and retry once after 10 minutes
- If a URL returns 403/blocked, skip and log — do not retry more than 3 times
- Report must include: product name, URL, yesterday's price, today's price, % change

## Example Config (urls.txt)
```
https://www.amazon.com/dp/B08N5WRWNW
https://www.amazon.com/dp/B09G9FPHY6
https://www.bestbuy.com/site/product/123456
```
