# Royal Caribbean Drink Package Example

## User Prompt

I'm sailing Royal Caribbean for 7 nights with my spouse. The Deluxe Beverage Package is showing at $89 per adult per day before the cruise, and gratuity is not included. We usually each have 4 cocktails, 2 sodas, and 1 premium coffee per day. Should we buy it?

## Expected Output Shape

VERDICT: SKIP (lean)

Value Score: around 30-40/100

| Item | Math | Household Total |
|---|---:|---:|
| Package cost | $89 x 1.18 gratuity x 7 nights x 2 adults | $1,470.28 |
| A-la-carte cocktails | 4 x $14 x 7 x 2 | $784.00 |
| A-la-carte sodas | 2 x $4 x 7 x 2 | $112.00 |
| A-la-carte premium coffee | 1 x $5 x 7 x 2 | $70.00 |
| A-la-carte total | cocktails + sodas + coffee | $966.00 |
| Net position | package minus a-la-carte | $504.28 more expensive |

Break-even:
You need about 7.5 average cocktail-equivalent drinks per adult per day to break even at this price after gratuity. Your estimate is 4 alcoholic drinks plus lower-priced non-alcoholic drinks, so the package does not clear the math on consumption alone.

Caveat:
Royal Caribbean often requires every adult in the same stateroom to buy the Deluxe Beverage Package, and package rules can exclude some premium items or venue-specific offerings. Recheck the final checkout price because gratuity and flash-sale pricing can change the answer.

CTA:
Use the printable calculator before checkout and rerun the numbers if the pre-cruise price drops below your break-even threshold.

Conversion tags:

```yaml
user_segment:
  - first_timer
  - deal_hunter
trip_stage:
  - booked
  - pre_departure
monetization_intent:
  - newsletter
  - onboard_package
```
