---
name: ecommerce-ad-copy-generator-free
description: Free basic version of ecommerce ad copy generator. Generates 3 ad copies from product info, and reserves premium upgrade hooks for 10-copy batch generation and A/B variants.
---

# Ecommerce Ad Copy Generator (Free)

## Value

- Free tier: generate 3 ad copies for Facebook/Google/TikTok.
- Premium tier (reserved): 10-copy batch, multi-language output, and A/B variants.

## Input

- `user_id`
- `product_name`
- `selling_points` (list or delimited string)
- `target_audience`
- optional `tier` (`free`/`premium`)

## Run

```bash
python3 scripts/ecommerce_ad_copy_generator_free.py \
  --user-id user_001 \
  --product-name "CloudBoost" \
  --selling-points 智能出价 多平台同步 分钟级报表 \
  --target-audience "跨境电商运营"
```

## Tests

```bash
python3 -m unittest scripts/test_ecommerce_ad_copy_generator_free.py -v
```

## Freemium Strategy

- Free tier is fully available now.
- Premium API hook is reserved and returns upgrade guidance with payment link.
