# Apartment Scorecard — Compare Rentals Like an Analyst

**The problem.** Renting is most people's largest single expense, yet the
decision is made emotionally: five tours in an afternoon, the nice lobby
wins, and the true cost — fees, parking, pet rent, utilities, an
uncounted commute — surfaces only when the first month's auto-pay hits.
Six months later you're white-knuckling a lease you can barely afford
in an apartment whose "charming neighborhood" turns out to mean bass
until 2am.

**What this is.** A decision system for renters:

- **Hard-constraint screening first**: budget, commute ceiling, bedrooms,
  pets, move date. Listings that fail don't get scored — or toured.
- **Weighted scoring on 16 criteria** (price, commute, noise, light,
  safety, kitchen, neighbors, laundry, transit, …) with weights you set
  to YOUR life — a remote worker and a daily commuter should never use
  the same weights, and now they don't.
- **True all-in monthly cost**: every fee, broker fee amortized over the
  lease, pet rent, parking, utilities, insurance, lost deposit interest,
  and your commute valued at your own $/minute (a $0.50/min valuation
  makes a 20-minute-farther apartment cost ~$433/month more — usually
  more than the rent gap people agonize over).
- **Affordability math**: the 30/33/50% rules, the 3×-income approval
  standard landlords actually use, and the 2.5-3.5× front-costs warning
  for signing day.
- **Head-to-head compare** with the exact right question: "you'd pay
  $301/month more for the higher-scoring place — worth it?"
- **A negotiation plan built from leverage**: vacancy math, comparable
  listings, lease-length trades, with a specific anchoring script (ask
  7% under, walk away at 3% under — on a $1,850 unit that's up to
  $1,554/year for one conversation).

## Quick start

```bash
python3 scripts/apartment_scorecard.py example        # full pipeline demo
python3 scripts/apartment_scorecard.py budget         # what can you afford
python3 scripts/apartment_scorecard.py criteria       # the 16 criteria
python3 scripts/apartment_scorecard.py screen --file apartments.json
python3 scripts/apartment_scorecard.py compare "Maple St 2BR" "Oak Rd Garden"
python3 scripts/apartment_scorecard.py negotiate "Maple St 2BR" \
    --vacant-days 30 --lease-offer 18 --facts comparables
```

Listing/weights formats and the 30-minute tour protocol (including the
photos-that-save-your-deposit trick) are in
`references/listing-format.md`.

## Tests

```bash
python3 scripts/test_apartment_scorecard.py    # 29 assertions, pure stdlib
```

MIT License — see LICENSE. Pure Python stdlib, JSON/CSV input, no
network calls, nothing leaves your machine.
