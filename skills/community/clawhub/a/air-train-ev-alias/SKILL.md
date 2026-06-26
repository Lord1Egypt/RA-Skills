---
name: air_train_ev
description: Alias of air-train-ev. Unified travel + mobility skill: (1) flight pricing with Amadeus (flight offers), (2) public transport/train journey planning with Navitia (journeys, departures), and (3) find nearby EV charge points using Open Charge Map. Use when Alessandro asks for flight prices, train itineraries/schedules, or EV charging stations.
---

# Alias — air_train_ev → air-train-ev

This skill is an **alias** for the canonical skill:
- `skills/air-train-ev/SKILL.md`

Use the same scripts (do not duplicate logic):
- Flights (Amadeus): `skills/air-train-ev/scripts/flight_offers.py`
- Train/PT (Navitia): `skills/air-train-ev/scripts/navitia.py`
- EV charge points (Open Charge Map): `skills/air-train-ev/scripts/ev_charge_points.py`

## Credentials (env)
Same as `air-train-ev`:
- `AMADEUS_CLIENT_ID`, `AMADEUS_CLIENT_SECRET`
- `NAVITIA_TOKEN`
- `OPENCHARGEMAP_API_KEY`
