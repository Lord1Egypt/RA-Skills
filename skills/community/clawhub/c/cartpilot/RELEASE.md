# CartPilot Release Notes

## Short Description

Calculate the best final ordering path for a cart: whether to split the order, which coupon is worth using, whether a threshold discount should be chased, and how the cheapest, easiest, and fastest routes compare.

## Marketplace Card Copy

Title:
- CartPilot

Alternate title:
- Checkout Tactician

Short description:
- Calculate the optimal checkout path: split orders, coupon choice, threshold logic, and cheapest-versus-fastest tradeoffs

Install hook:
- Not a price comparer. A checkout decision layer.

## Announcement Copy

CartPilot is not another shopping skill that only finds cheaper items.

It solves a more realistic last-mile problem:
- should this order be split
- which coupon is actually worth using
- whether the threshold discount should be chased
- whether a small savings gap is worth the extra hassle
- how the cheapest, easiest, and fastest routes differ

In one line:

It is not a comparison tool. It is a checkout decision layer.

## Suggested Tags

- latest
- shopping
- checkout
- cart-optimization
- coupon
- threshold
- split-order
- ecommerce
- meituan
- jd
- taobao
- pdd

## Suggested Repo Name

- `openclaw-skill-cartpilot`

## Preflight

```bash
cd /absolute/path/to/cartpilot
clawhub whoami
bash /absolute/path/to/codex/tmp/validate_clawhub_skill_dir.sh .
```

## Publish Command

### One command

```bash
cd /absolute/path/to/cartpilot
sh scripts/publish.sh
```

### Manual command

```bash
clawhub publish /absolute/path/to/cartpilot \
  --slug cartpilot \
  --name "CartPilot" \
  --version "1.0.0" \
  --changelog "Launch CartPilot, a checkout-path optimization skill that decides split-order strategy, coupon placement, threshold tradeoffs, and the best final ordering path." \
  --tags "latest,shopping,checkout,cart-optimization,coupon,threshold,split-order,ecommerce,meituan,jd,taobao,pdd"
```
