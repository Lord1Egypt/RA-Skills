# Garage Sale Pricer

**Every garage sale dies the same two deaths: everything overpriced so nothing sells, or decision fatigue so the $200 treadmill leaves for $10 at 8 AM. 300 items need 300 prices — and nobody has a system.**

This is the system: a knowledge base of what things **actually sell for at garage sales** (not marketplace prices — garage-sale reality runs 30–50% lower) with condition multipliers and negotiation floors, plus the operational layer everyone forgets: the change float sized from your expected gross, signage counts and ordinance warnings, the 7:00–8:30 AM pro-buyer window that carries 40% of revenue, and a leftover router that schedules the donation truck BEFORE the sale so your garage doesn't become storage again.

## What it does
- `price --category tools_power --condition B --retail 200` → tag, floor, day-2 price with the reasoning shown.
- `add` + `list` → priced inventory with **printable two-column tag sheet** (name / price / after-noon price).
- `plan --items 120 --avg-price 6` → expected gross band, exact change float denomination stack, signage plan, timing doctrine, payment-QR reminder, never-sell list.
- `leftovers` → routes unsold items to **consign / donate / curb-alert / re-list** by category value, with the donation-pickup-before-the-sale rule.

## Example
```
$ python3 scripts/garage_sale.py price --category furniture_upholstered --condition C --retail 900
furniture_upholstered (condition C, retail $900):
  TAG  $70   (13% of retail $900 x 0.7, clamped to band; band $11-$95)
  negotiation floor $42 · day-2 $35 · last hour: fill-a-bag or donate

$ python3 scripts/garage_sale.py plan --items 120 --avg-price 6
EXPECTED GROSS: $360-$504 (50-70% of tag total; best 90 min = ~40% of it)
CHANGE FLOAT (get FRIDAY at the bank): $154
  $40 in $1s · $25 in $5s · $30 in $10s · 1 quarter roll ($10) · 1x $20 buffer
```

Stdlib-only Python; inventory is a local JSON file.

## License
MIT
