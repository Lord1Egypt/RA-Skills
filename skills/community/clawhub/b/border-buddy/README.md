# Border Buddy 🛂

**Pre-trip border intelligence: visas, passport validity, transit rules, vaccination certificates, customs limits, and the Schengen 90/180 calculator.**

## The Problem

Every international trip begins with three questions people answer badly:

1. **"Do I need a visa?"** — The answer depends on nationality × destination × purpose, and travelers routinely discover the answer at the airport check-in counter, where they're denied boarding. Airlines pay the fine for improperly documented passengers, so they deny boarding aggressively.
2. **"How long can I stay?"** — The Schengen Area's **90/180 rolling-window rule** defeats manual counting. Visit Europe in March (60 days) and again in July (40 days)? That's 100 days in one rolling window — a 10-day overstay. Consequences: 5-year entry bans, visa annulment, fingerprint flags.
3. **"Is my passport valid enough?"** — "Valid" isn't enough. China wants 6 months validity. Schengen wants 3 months beyond departure AND issuance within 10 years. Airlines enforce their own stricter reading of both.

On top of that: transit visas for layovers (a 3-hour London Heathrow layover requires a Direct Airside Transit Visa for many nationalities), yellow fever certificates when arriving from endemic countries, and cash-declaration thresholds (€10,000 in the EU — an offense to exceed undeclared).

Border rules also **change constantly** — visa-free pilots launch and expire, ETA schemes roll out (UK ETA, US ESTA expansions), reciprocity rules flip (Brazil ↔ US eVisa requirements changed in 2025). Generic AI answers go stale silently.

## What It Does

`border-buddy` combines an embedded rules snapshot (~20 major destinations, nationality-group policies, passport validity rules, health and customs data) with a **precise date-arithmetic engine** for the Schengen window. It produces entry-readiness reports *before* you book non-refundable tickets, and always names the official authority to verify with.

```bash
# Entry report: Brazilian to Portugal via Frankfurt, 42 days
python3 scripts/border_buddy.py check --nationality BR --destination PT \
  --transit DE --stay-days 42 --passport-expiry 2027-03-01 --entry-date 2026-09-01

# Schengen 90/180: how many days do I have left? When can I next enter?
python3 scripts/border_buddy.py schengen --visits my_visits.json --on 2026-09-15 --plan-days 30

# Raw rule snapshot for a country
python3 scripts/border_buddy.py rules --destination JP

# End-to-end demo with sample data
python3 scripts/border_buddy.py demo
```

Example output:

```
ENTRY READINESS - Portugal (PT) for BR nationals [group: SOUTH_AMERICA]
  Visa:         NOT REQUIRED (Schengen 90/180 window) [✓]
                └ shared 90/180 Schengen pool - budget across ALL Schengen states
  Passport:     ✓ - Schengen rule: expiry >= departure+3mo = 2027-01-11
  Transit DE:   NO VISA (airside transit visa-free)
  Yellow fever: not required (not arriving from an endemic country)
  Customs:      1L spirits + 4L wine + 200 cig. Cash >= EUR 10,000 declare.
  VERIFY WITH:  sef.pt / vistos.mne.gov.pt
```

## The Schengen Calculator

The crown jewel. Feed it your visit history, it computes the rolling 180-day window for any date, flags overstays, tells you exactly when old days fall out of the window, and finds the **next safe entry date** for a desired stay length:

```
SCHENGEN 90/180 - as of 2026-08-18
  window:       2026-02-20 -> 2026-08-18
  days used:    48 / 90
  remaining:    42
  next safe entry for a 20-day stay: 2026-08-18 (uses 49/90 on final day)
```

Correct conventions matter: entry day counts, exit day doesn't; presence is area-wide; the window moves daily. Manual counting gets these wrong constantly — which is how 5-year bans happen.

## Who Needs This

- **Frequent Schengen travelers** (digital nomads, retirees wintering in Spain, business travelers) — the rolling window is genuinely hard to track by hand across multiple trips
- **Anyone booking flights with connections** — transit visa surprises are the #1 avoidable travel disaster
- **Travel planners and agents** — first-pass screening before routing clients
- **AI agents** helping users plan trips — a structured, verifiable answer instead of a hallucinated "I think you're fine"

## Honest Limitations (by design)

This is a **snapshot**, not a live feed. Immigration law changes weekly somewhere. Every report prints `as_of` and the exact authority to verify with. The skill's own instructions tell the agent to present the snapshot answer *plus* a live verification pointer — never as a guarantee. It's trip-planning intelligence, not legal advice.

## Testing

```bash
python3 scripts/test_border_buddy.py   # 26 assertions: date math, rules, CLI
```

Covers the off-by-one traps (entry/exit day conventions), window expiry, overstay detection, passport rule boundaries, and CLI end-to-end runs.

## License

MIT © 2026 Denis Voronin
