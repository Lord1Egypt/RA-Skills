---
name: ecommerce-ad-copy-generator
description: Generate paid ecommerce ad copy in batch with SkillPay billing. Use when the user needs 5 ready-to-use ad copies from product name, selling points, and target audience; charge 0.10 USDT per request via /billing/charge; return payment_url when balance is insufficient; and enforce strict input validation plus error handling.
---

# Ecommerce Ad Copy Generator

## Overview

Generate 5 conversion-focused ad copies for `Facebook` / `Google` / `TikTok` from structured product input. Charge `0.10 USDT` per run before content generation.

## Workflow

1. Parse and validate input fields:
   - `user_id`
   - `product_name`
   - `selling_points` (list or delimited string)
   - `target_audience`
2. Call SkillPay `POST /billing/charge` with amount `0.10 USDT`.
3. If billing succeeds, generate exactly 5 platform-adapted ad copies.
4. If billing returns insufficient balance, return `INSUFFICIENT_BALANCE` with `payment_url`.
5. Return structured JSON output for downstream use.

## Run

- Core script: `scripts/ecommerce_ad_copy_generator.py`
- Test script: `scripts/test_ecommerce_ad_copy_generator.py`

Run with direct arguments:

```bash
python3 scripts/ecommerce_ad_copy_generator.py \
  --user-id user_001 \
  --product-name "CloudBoost 智能投放器" \
  --selling-points 智能出价 多平台同步 分钟级报表 \
  --target-audience "跨境电商运营团队"
```

Run with JSON file:

```bash
python3 scripts/ecommerce_ad_copy_generator.py --input-file ./payload.json
```

Run tests:

```bash
python3 -m unittest scripts/test_ecommerce_ad_copy_generator.py -v
```

## Output Contract

Success:
- `success: true`
- `pricing.amount: "0.10"`
- `pricing.currency: "USDT"`
- `copies`: exactly 5 items, each containing:
  - `platform`
  - `headline`
  - `body`
  - `cta`

Billing failure:
- `VALIDATION_ERROR` for invalid input
- `INSUFFICIENT_BALANCE` and `payment_url` when top-up is required
- `BILLING_ERROR` for non-balance billing failures

## Environment Variables

- `SKILLPAY_CHARGE_ENDPOINT` (default: `https://skillpay.me/billing/charge`)
- `SKILLPAY_API_KEY` (optional bearer token)
- `SKILLPAY_PAYMENT_URL_TEMPLATE` (optional; supports `{user_id}`)
- `SKILLPAY_TOPUP_BASE_URL` (default: `https://skillpay.me/pay`)

## References

- SkillPay request/response assumptions and fallback behavior: `references/skillpay-api-contract.md`
