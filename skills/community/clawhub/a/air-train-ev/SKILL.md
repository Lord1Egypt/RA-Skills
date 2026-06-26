---
name: air-train-ev
description: Unified travel + mobility skill: (1) flight pricing with Amadeus (flight offers), (2) public transport/train journey planning with Navitia (journeys, departures), and (3) find nearby EV charge points using Open Charge Map. Use when Alessandro asks for flight prices, train itineraries/schedules, or EV charging stations.
---

# Air + Train + EV

## Credentials (env)
Do not hardcode keys in scripts.

### Flights (Amadeus)
- `AMADEUS_CLIENT_ID`
- `AMADEUS_CLIENT_SECRET`
- Optional: `AMADEUS_HOST` (default `https://api.amadeus.com`)

### Trains / public transport (Navitia)
- `NAVITIA_TOKEN`
- Optional: `NAVITIA_HOST` (default `https://api.navitia.io`)
- Optional: `NAVITIA_COVERAGE` (default `sandbox`)

### EV charge points (Open Charge Map)
- `OPENCHARGEMAP_API_KEY`
- Optional: `OPENCHARGEMAP_HOST` (default `https://api.openchargemap.io`)

## Flights — quick usage
```bash
python3 skills/air-train-ev/scripts/flight_offers.py \
  --origin ZRH --destination IST \
  --departure 2026-03-10 \
  --adults 1 --travel-class ECO \
  --non-stop true \
  --included-airlines PC,VF,TK \
  --max 6
```

Output formatting is fixed:
- Dates/times: `DD/MM/YY HH:MM`
- EUR prices use `€`

## Train journeys — quick usage
```bash
python3 skills/air-train-ev/scripts/navitia.py coverage
python3 skills/air-train-ev/scripts/navitia.py places --q "Strasbourg"
python3 skills/air-train-ev/scripts/navitia.py journeys --from "Strasbourg" --to "Rennes" --datetime "2026-03-07T08:00:00" --count 5
```

## EV charge points — quick usage
```bash
python3 skills/air-train-ev/scripts/ev_charge_points.py \
  --lat 48.5839 --lon 7.7455 \
  --km 5 --max 10
```

Notes:
- This uses Open Charge Map `GET /v3/poi/`.
- Returned results include operator/title, address, distance (when available), connector types, and coordinates.
