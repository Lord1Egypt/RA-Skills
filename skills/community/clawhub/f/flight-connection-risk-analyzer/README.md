# Flight Connection Risk Analyzer

**Is that 50-minute layover sane — or a planned overnight?**

Airlines sell connections down to the legal *Minimum Connect Time* — the
fastest possible wheel-stop-to-departure for a marathon runner with no bags.
MCT is a floor, not a plan. This tool scores any connecting itinerary on what
actually decides whether you make it:

| Factor | What it captures |
|---|---|
| **Buffer above MCT** | Scheduled time minus the legal minimum for that airport + connection type |
| **Terminal transfer reality** | Trains, buses, security re-entry (US intl arrivals = customs + bag recheck + TSA again) |
| **Delay stacking** | On-time rates collapse from ~90% at 6 AM to ~65% by 9 PM; the inbound aircraft carries every earlier delay |
| **Consequence asymmetry** | Last flight of the day, winter at ORD/DTW/MSP, and the unprotected self-transfer |

## Verdicts

`SAFE` → `TIGHT` → `HIGH RISK` → `RUSSIAN ROULETTE`, each with a
survive-the-layover protocol: front-of-plane seating, carry-on doctrine,
radio-ahead tactics, and exactly what to do the moment you miss it (same
ticket = rebooking rights; separate tickets = you bought a new fare).

## Quick start

```bash
# 50 min at ATL, domestic, evening inbound
python3 scripts/connection_scorer.py --airport ATL --layover 50 --type dom-dom --dep-block 16-20

# 1h50 intl arrival into ORD, winter, last flight
python3 scripts/connection_scorer.py --airport ORD --layover 110 --type intl-dom \
    --dep-block 16-20 --season winter --last-flight

# Self-transfer (separate tickets) at LHR
python3 scripts/connection_scorer.py --airport LHR --layover 165 --type intl-intl --self-transfer

python3 scripts/connection_scorer.py --list-hubs   # 29-hub knowledge base
```

Example verdict (ORD, 110 min, intl→dom, evening, winter, last flight):

```
Working buffer:   -5 min  →  RISK 92/100  RUSSIAN ROULETTE
```

The same 110 minutes at DFW domestic morning = SAFE. The tool explains why.

## Who needs this

- Anyone booking a connection who can read a risk score — hundreds of millions
  of connecting itineraries are sold annually at MCT + 5 minutes
- Self-transfer bookers (Kiwi/budget hops): the 3-hour doctrine, priced
- Travelers into US hubs from abroad (customs/recheck/TSA math)
- Travel-department folk deciding whether the cheap 45-min connection is
  actually cheap after the missed-connection hotel and the walk-up fare

## What's inside

- `SKILL.md` — the four-factor model, scoring bands, survive protocol, pitfalls
- `references/connection-model.md` — hub transfer table (29 hubs), DOT delay
  curves, misconnection rights (single PNR vs separate tickets, EU261)
- `scripts/connection_scorer.py` — stdlib-only CLI, JSON output mode, no network

Stdlib Python only. No API keys, no network calls, no data collection.
Planning instrument — not real-time flight status.

## License

MIT © Denis Voronin
