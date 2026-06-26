# CouponClaw — Find Coupons & Stack Cashback Worldwide

> Never pay full price — find every coupon code and stack it with cashback. China · US · UK · Australia · Southeast Asia · DTC brands.

[![clawhub](https://img.shields.io/badge/clawhub-couponclaw-blue)](https://clawhub.ai/skills/couponclaw)
[![version](https://img.shields.io/badge/version-1.1.5-green)](https://clawhub.ai/skills/couponclaw)
[![license](https://img.shields.io/badge/license-MIT--0-lightgrey)](LICENSE)

## What it does

CouponClaw is an [OpenClaw](https://openclaw.ai) skill that runs a **3-layer savings strategy** on any product or store:

1. **Layer 1 — Coupon codes**: real-time browser search across region-specific coupon sites
2. **Layer 2 — Cashback stacking**: compares rates across Rakuten, TopCashback, ShopBack, 返利网 — and checks if they stack with the coupon
3. **Layer 3 — DTC brand check**: detects first-order discounts and newsletter signup offers on brand official sites

Also generates a daily deals briefing surfacing the hottest community-verified deals from smzdm, Slickdeals, HotUKDeals, OzBargain, and ShopBack each morning.

## Coverage

| Region | Coupon sources | Cashback |
|---|---|---|
| 🇨🇳 China | 什么值得买, 京东领券, 淘宝聚划算, 折800 | 返利网, 什么值得买返利 |
| 🌏 Chinese overseas | Dealmoon | Rakuten |
| 🇺🇸 US | RetailMeNot, Slickdeals, Amazon Coupons | Rakuten, TopCashback |
| 🇬🇧 UK | VoucherCodes, HotUKDeals, MyVoucherCodes | TopCashback |
| 🇦🇺 Australia | OzBargain, Cashrewards | ShopBack |
| 🌏 Southeast Asia | ShopBack, iPrice | ShopBack |
| 🏷️ DTC brands | Official site popup detection, newsletter offers | Rakuten / TopCashback |

## Installation

```bash
openclaw install couponclaw
```

## Usage

```bash
# Find all coupons for a product or store
openclaw run couponclaw find "Nike" --region us

# Compare cashback rates across platforms
openclaw run couponclaw cashback "Booking.com" --spend 300

# Today's top deals briefing
openclaw run couponclaw daily-deals --region all --lang en

# All regions, both languages
openclaw run couponclaw find "AirPods Pro" --region all --lang en
```

## Ecosystem

Part of the **OpenClaw Smart Consumer** skill suite:

| Skill | How it connects |
|---|---|
| [BuyWise](https://github.com/jiajiaoy/BuyWise) | Calls CouponClaw after confirming a product is worth buying |
| [TravelHound](https://github.com/jiajiaoy/TravelHound) | Calls CouponClaw for Booking.com, Agoda, Trip.com promo codes |
| [TrendRadar](https://github.com/jiajiaoy/TrendRadar) | Calls CouponClaw for surging products before prices spike |
| **CouponClaw** | Coupon + cashback layer ← you are here |

## Keywords

coupon code · promo code · discount code · cashback · cashback stacking · RetailMeNot · Slickdeals · Rakuten · TopCashback · ShopBack · OzBargain · HotUKDeals · VoucherCodes · Amazon coupon · DTC discount · never pay full price · 优惠券 · 优惠码 · 返利 · 省钱 · 领券 · Black Friday · Cyber Monday

---

Built for [OpenClaw](https://openclaw.ai) · Published on [clawhub.ai/skills/couponclaw](https://clawhub.ai/skills/couponclaw)
