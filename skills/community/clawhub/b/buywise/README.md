# BuyWise — Global Shopping Decision Assistant

> Should you buy it? Compare prices on 8+ platforms, detect fake discounts, analyze reviews, and get a clear Buy / Wait / Skip verdict.

[![clawhub](https://img.shields.io/badge/clawhub-buywise-blue)](https://clawhub.ai/skills/buywise)
[![version](https://img.shields.io/badge/version-1.5.5-green)](https://clawhub.ai/skills/buywise)
[![license](https://img.shields.io/badge/license-MIT--0-lightgrey)](LICENSE)

## What it does

BuyWise is an [OpenClaw](https://openclaw.ai) skill that answers the question you ask before every purchase: *is this actually a good deal?*

It navigates real product pages using your AI's browser tool — no fabricated prices — and returns a verdict with evidence.

**Price comparison** — Amazon, eBay, AliExpress, Temu, JD, Taobao, Tmall, smzdm in one report  
**Fake discount detection** — checks CamelCamelCamel and smzdm price history to expose "inflate then discount" tactics  
**Review analysis** — extracts top strengths, complaints, who it's for, and red flags  
**Alternatives** — recommends 2-3 better-value options with price ranges  
**Buy timing** — 🟢 Buy now / 🟡 Wait / 🔴 Skip verdict with reasoning  
**Coupon stacking** — hands off to [CouponClaw](https://github.com/jiajiaoy/CouponClaw) to stack promo codes + cashback on confirmed buys

## Price sources

| Platform | Region | Notes |
|---|---|---|
| Google Shopping (`?tbm=shop`) | Global | Aggregates Amazon, eBay, Walmart, Best Buy and dozens more |
| smzdm | China | Aggregates JD / Taobao / Tmall / Pinduoduo in one page |
| Amazon | US/Global | Cross-verified with Google Shopping |
| AliExpress | Global | Budget / wholesale reference |
| Temu | Global | Via web_search (no standard search URL) |
| CamelCamelCamel | Amazon history | All-time low, 90-day average, pre-sale spike detection |
| JD | China | Self-operated listings |

## Installation

```bash
openclaw install buywise
```

## Usage

```bash
# Full buying decision
openclaw run buywise advise "Sony WH-1000XM5"

# Price comparison only
openclaw run buywise compare "iPhone 16 Pro"

# Check if a sale is genuine
openclaw run buywise deal "Dyson V15 --price 399 --was 649"

# Review deep-dive
openclaw run buywise review "Kindle Paperwhite"
```

## Ecosystem

Part of the **OpenClaw Smart Consumer** skill suite:

| Skill | Description |
|---|---|
| [TrendRadar](https://github.com/jiajiaoy/TrendRadar) | Detect trending products → feed into BuyWise |
| **BuyWise** | Shopping decision ← you are here |
| [CouponClaw](https://github.com/jiajiaoy/CouponClaw) | Stack coupons + cashback after BuyWise confirms it's worth buying |
| [TravelHound](https://github.com/jiajiaoy/TravelHound) | Same logic applied to flights and hotels |
| [NewsToday](https://github.com/jiajiaoy/NewsToday) | Daily news including consumer/market trends |

## Keywords

price comparison · buy or wait · fake discount · Amazon price history · CamelCamelCamel · shopping assistant · deal checker · product review · is it worth buying · save money · buy timing · cross-border shopping · Black Friday · Cyber Monday

---

Built for [OpenClaw](https://openclaw.ai) · Published on [clawhub.ai/skills/buywise](https://clawhub.ai/skills/buywise)
