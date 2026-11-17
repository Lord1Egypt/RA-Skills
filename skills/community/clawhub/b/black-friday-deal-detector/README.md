# Black Friday Deal Detector

**"60% OFF!" — off what, exactly?**

Retail's holiday playbook: inflate the anchor in October, discount off a
price nobody paid, and hide the honest price behind coupon mazes and
gift-card-back offers. This tool cuts through it by scoring every claim
against the only two numbers that matter — **today's street price** and the
**12-month low**.

```
Was $1,299  NOW $799  (38% off!)
  street today: $749   →  real discount: −7% (you'd LOSE money)
  12-month low: $699   →  sale is 14% above the annual floor
  VERDICT: PRICE THEATER
```

## What it detects

- **Fake-anchor MSRP** — discount claimed off a price never charged
- **October pre-inflation** — the step-up trackers see and shoppers don't
- **Derivative SKUs** — "exclusive" model numbers built to be incomparable
- **Gift-card-back pricing** — valued honestly at 50%, not face
- **Membership-gated floors** — membership cost amortized into the price
- **Category reality checks** — 10 category floors ("a real BF TV deal is
  ~30% below street; Apple cash discounts are ~10%; mattress '50% off' is
  everyday pricing")

## Verdicts

`PRICE THEATER` / `WAIT` / `OK DEAL` / `GREAT` — each with a one-line
strategy (including the alert price to set when waiting).

## Quick start

```bash
python3 scripts/deal_detector.py --msrp 1299 --sale 799 --street 749 --low 699 --category tv

# gift-card-back + membership-gated claim
python3 scripts/deal_detector.py --msrp 999 --sale 799 --street 829 --low 779 \
    --gift-card-back 100 --membership-cost 50

# head-to-head
python3 scripts/deal_detector.py --compare "TV-A:1299:799:749:699" "TV-B:1099:749:779:739"
```

## Who needs this

Anyone who shops sales — which is everyone. US holiday-season sales alone
run hundreds of billions of dollars, and price-anchor games are the
industry's core mechanism (the EU banned the trick outright with its 30-day
"was price" rule; the US hasn't).

## What's inside

- `SKILL.md` — the seven theater patterns, category floor table, scoring model
- `references/price-theater.md` — tells & counters, legal reference points
  (FTC, EU Omnibus Art. 6a, UK CMA), return-window traps
- `scripts/deal_detector.py` — stdlib-only CLI with JSON mode and head-to-head
  comparison

Stdlib Python only. No network, no tracking, no affiliate anything.

## License

MIT © Denis Voronin
