# Black Friday Deal Detection — Reference

## 1. Price-theater taxonomy (with tells)

### Inflated anchor / phantom MSRP
- **Tell:** tracker history shows the "list price" was never charged, or was
  charged for < 30 days a year ago.
- **Counter:** recompute the discount from street price. A 60% anchor
  discount that is 7% off street is noise.

### October pre-inflation
- **Tell:** Keepa/camelcamelcamel shows a step-up 3–6 weeks before the sale
  event (late Sept–Oct for BF).
- **Counter:** anchor to the pre-step price. Several regulators (FTC pricing
  claims guidance; EU Omnibus Directive Art. 6a — "was" price must be the
  lowest 30-day price) have made this legally fraught in the EU; it remains
  endemic in the US.

### Derivative / exclusive SKUs
- **Tell:** model number differs from the standard lineup by a suffix/prefix
  (Samsung "D" retailer suffixes, "6000D" vs "6000"; LG C-level retailer
  variants; "Black Friday" laptop SKUs with last-gen CPUs).
- **Counter:** compare panel/engine/CPU specs, not names. Common derisks:
  fewer dimming zones, last-gen chip, 60Hz panel in a 120Hz family, half the
  RAM. Use RTINGS / notebookcheck class tables.

### Bundle-and-% maze
- **Tell:** discount computed against a bundle; or advertised price requires
  app + loyalty + store-card stack.
- **Counter:** compute the "walk-in price" — the price with zero of the maze.
  That is the honest comparable.

### Gift-card-back
- **Tell:** "$X back in gift cards."
- **Counter:** value at 50% face (or your honest probability of using it).
  Adjusted price = sale − 0.5 × card. Note it also locks the next purchase
  to the same retailer.

### Doorbuster unit economics
- Doorbusters are loss leaders in limited quantity. The realistic consumer
  EV of queuing for a $300-off TV with 8 units per store is poor unless you
  are first in line. Decide on EV, not on the sticker.

## 2. What "good" looks like per category (12-month low deltas)

Real BF floors, as typically observed on trackers:

- **TVs:** BF price ≈ 12-month low; model-year clearance (spring) can go
  5–10% lower on the outgoing model. If a BF TV price is > 5% above its
  tracked low, WAIT.
- **Apple hardware:** cash discounts 5–10% at resellers (Amazon, Walmart,
  BestBuy); Apple itself does gift cards. Education pricing stacks with some
  reseller sales in Sept.
- **Windows laptops:** 20–30% off street is a real BF deal; beware
  last-gen-CPU "exclusive" SKUs — verify the CPU generation.
- **SSD/RAM:** lows are cyclical (supply-driven); a "40% off" that merely
  returns to the spring low is neutral. Check the drive's controller/tier —
  sale units are sometimes the slower bin.
- **Small appliances (Ninja, Vitamix, Breville, KitchenAid):** BF is
  typically the genuine annual low; 35–50% off street is real.
- **Power tools:** two real windows — Father's Day (June) and BF. Bundled
  bare-tool kits effectively lower per-tool cost 25–40%. Wait for the window
  unless the tool is needed now.
- **Mattresses:** list prices are fiction (300%+ markups). The only
  comparable is the coupon-stacked floor across 3 brands in the same
  comfort tier. BF adds "freebies" (pillows/sheets) worth ~$100, not $400.
- **Toys:** the big-name items often hit lows in early December (retailers
  panic on stock); BF "toy deals" are frequently mid-tier items.

## 3. The 30-second field protocol

1. Pull out phone, open the product on 2 retailer apps → street price.
2. Open camelcamelcamel/Keepa → 12-month low + October step check.
3. Check model number letter-suffix against the manufacturer's site.
4. Run: `python3 scripts/deal_detector.py --msrp M --sale S --street T --low L`
5. Trust the verdict, not the strikethrough.

## 4. Legal reference points (for complaint-minded shoppers)

- **EU Omnibus Directive (2019/2161, Art. 6a):** any price reduction
  announcement must reference the lowest price in the prior 30 days. Makes
  October inflation legally risky in the EU.
- **US FTC:** "former price" claims must be bona fide, actual, and not
  inflated (FTC Guides Against Deceptive Pricing). Enforcement is sparse but
  the standard exists; state UDAP statutes also apply.
- **UK CMA pricing guidance:** similar "was" price expectations post-Brexit
  mirror EU rules in practice.

## 5. Return windows and warranty traps

- Holiday return extensions: many US retailers extend BF purchases to
  Jan 8–31 — VERIFY, don't assume; doorbusters and "Black Friday exclusive"
  SKUs are sometimes final-sale.
- Restocking fees: TVs > $500 sometimes 15% at some retailers unless
  defective.
- Warranty start date: usually purchase date, not gift date; a BF gift may
  burn 5 weeks of warranty before first use. Receipt keepers win.
