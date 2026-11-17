---
name: "flight-pickup-tracker"
description: "Track a flight in real-time and notify when to leave for airport pickup based on distance to destination."
---

# Flight Tracker Skill

Track a flight in real-time and notify the user when to leave for airport pickup — combining live flight position, real-time drive time with traffic, and proactive alerts.

## When to Use

- User explicitly asks to track a specific flight for airport pickup
- User asks "when should I leave to pick up [person] from [airport]?"
- User provides a flight number and asks for pickup timing help

> **Not** general flight status queries, travel planning, or airport info — only when the user wants active pickup coordination for a named flight.

## Requirements

- **Flight tracking**: OpenSky Network (free, no API key)
- **Python 3** (standard library only, no pip installs)
- Scripts: `scripts/flight_tracker.py`, `scripts/drive_time.py`

### Google Maps API Key (Optional)

The skill works in two modes:

| Mode | Google Maps Key | Drive Time Accuracy |
|------|----------------|--------------------|
| **Full** | Yes (stored at `scripts/data/google_maps_api_key.txt`) | Real-time with live traffic |
| **Basic** | No | Estimated based on straight-line distance from user to airport (~1 min per 1.2 km / 0.75 mi), adjusted for time of day |

**Without a Google Maps key**, the skill still works end-to-end — flight tracking, ETA calculation, and leave-by alerts all function. Drive time is estimated using the distance between the user's location and the airport:
- Late night (10 PM–6 AM): ~1 min per 1.5 km
- Midday: ~1 min per 1.2 km
- Rush hour: ~1 min per 0.8 km

This is a rough estimate but sufficient for most pickups. For precise timing with real traffic data, set up a Google Maps Directions API key (free $200/month credit from Google, takes 5 minutes).

## How It Works

1. **Track the flight** — poll live lat/lng/altitude via OpenSky Network
2. **Calculate distance** — great-circle distance from plane to destination airport
3. **Get drive time** — query Google Maps with live traffic from user's location to airport
4. **Determine when to leave** — landing ETA minus drive time minus buffer
5. **Alert the user** — message with "leave by" time

## Scripts

### Flight Tracker (`scripts/flight_tracker.py`)

Tracks a flight's position relative to its destination airport.

```bash
# Single check
python3 scripts/flight_tracker.py --flight AS594 --dest SEA --origin ONT --dry-run

# Continuous polling (every 5 min until landing)
python3 scripts/flight_tracker.py --flight AS594 --dest SEA --origin ONT --poll-interval 300
```

> **Always pass `--origin`** to prevent false matches from same-callsign flights on different continents. The script auto-converts IATA codes (AS594) to ICAO callsigns (ASA594) for OpenSky lookup.

**Output (JSON):**
```json
{"phase": "not-departed", "status": "not-departed", "note": "Flight may not have departed yet"}
```
```json
{"phase": "en-route", "distance_km": 142.3, "eta_min": 18, ...}
```
```

**Flight Phases:**
| Phase | Meaning | Action |
|-------|---------|--------|
| `en-route` | Cruising, > 300 km out | Keep polling every 5 min |
| `approaching` | Within 300 km | Check drive time, prepare alert |
| `descending_close` | Within 150 km, descending | Send alert if not already sent |
| `final_approach` | Within 50 km | Confirm landing imminent |
| `landed` | On the ground | Notify user |

### Drive Time (`scripts/drive_time.py`)

Gets real-time drive time with live traffic conditions.

```bash
python3 scripts/drive_time.py \
  --origin "<your address>" \
  --dest "Seattle-Tacoma International Airport" \
  --api-key "$(cat scripts/data/google_maps_api_key.txt)" \
  --json
```

**Output (JSON):**
```json
{
  "duration_text": "28 mins",
  "duration_seconds": 1675,
  "duration_minutes": 28,
  "traffic_duration_text": "29 mins",
  "traffic_duration_seconds": 1759,
  "traffic_duration_minutes": 29,
  "distance_text": "21.6 mi",
  "distance_meters": 34775,
  "summary": "I-405 S"
}
```

Use `traffic_duration_minutes` (includes live traffic) for calculations.

## Procedure

### Step 1: Gather Info

Determine (ask if not known):
- **Flight code** (e.g. AS594)
- **Destination airport** (e.g. SEA) — often inferrable from context
- **Pickup address** — ask the user to confirm (suggest home address as default, but get explicit confirmation)
- **Scheduled departure time** — to know when to start polling

> ⚠️ **Always confirm the pickup origin address with the user before proceeding.** Do not silently use addresses from USER.md without acknowledgment.

### Step 2: Schedule Monitoring

Create a cron job (`schedule.kind: "at"`) that fires ~10 minutes after scheduled departure time.

Example cron job payload:
```
Track [person]'s flight home. Run:
python3 scripts/flight_tracker.py --flight <CODE> --dest <DEST> --origin <ORIGIN> --dry-run

Then run:
python3 scripts/drive_time.py --origin "<address>" --dest "<airport>" --api-key "$(cat scripts/data/google_maps_api_key.txt)" --json

If flight is approaching (< 300 km):
  Calculate: leave_by = now + eta_min - drive_time_min - buffer
  Message user with leave_by time.

If flight is not airborne or far away:
  Schedule another check in 15 min.

If landed:
  Message user "landed, leave now if not already en route."
```

### Step 3: Calculate Leave Time

**With Google Maps API key:**
```
leave_by = current_time + flight_eta_min - traffic_drive_time_min - buffer_min
```

**Without Google Maps API key (estimate):**
```
distance_km = haversine(user_location, airport)
if late_night:  drive_min = distance_km / 1.5
elif rush_hour: drive_min = distance_km / 0.8
else:           drive_min = distance_km / 1.2

leave_by = current_time + flight_eta_min - drive_min - buffer_min
```

Where:
- `flight_eta_min` = from flight tracker (distance/speed based)
- `traffic_drive_time_min` = from Google Maps (live traffic)
- `buffer_min` = 15 min (domestic: taxi + deplane + walk to arrivals) or 30 min (international: + customs/baggage)

### Step 4: Alert the User

Message should include:
- ✈️ Flight status (on time / delayed / phase)
- 🕐 Expected landing time
- 🚗 Current drive time to airport (with route)
- ⏰ **"Leave by" time**
- Any relevant notes (weather, delays, terminal info)

### Step 5: Follow Up

- If alert was sent early (approaching phase), send one more confirmation when landed
- If flight is significantly delayed, update the user and recalculate

## Supported Airlines (IATA → ICAO Callsign)

The flight tracker converts IATA codes to ICAO callsigns for OpenSky. Currently supports:

**US Domestic:** Alaska (AS), American (AA), Delta (DL), United (UA), Southwest (WN), JetBlue (B6), Spirit (NK), Frontier (F9), Hawaiian (HA), Sun Country (SY), Horizon (QX), SkyWest (OO), Allegiant (G4), Breeze (MX)

**International:** Lufthansa (LH), Air India (AI), Singapore (SQ), Emirates (EK), Qatar (QR), KLM (KL), Thai (TG), ANA (NH), British Airways (BA), Air France (AF), Turkish (TK), Etihad (EY), Cathay Pacific (CX), JAL (JL), IndiGo (6E), Air India Express (IX)

Add more by editing `AIRLINE_CALLSIGN` dict in `scripts/flight_tracker.py`.

## Supported Airports

SEA, ONT, LAX, SFO, JFK, ORD, DFW, ATL, DEN, PHX, LAS, PDX, SAN, BOS, MSP, EWR, IAD, MIA.

Add more by editing `AIRPORT_COORDS` dict in `scripts/flight_tracker.py`.

## Data Sources

| Component | Source | Key Needed | Cost |
|-----------|--------|-----------|------|
| Flight position | OpenSky Network | No | Free |
| Flight position (fallback) | AirLabs | Yes | Free tier: 1,000/mo |
| Drive time | Google Maps Directions API | Yes | $0.005/call ($200/mo free) |

## Privacy & Data Disclosure

- **Google Maps API**: When drive-time mode is "Full", the user's pickup address and the destination airport are sent to Google Maps Directions API to get real-time traffic estimates. Users should be aware their location data is transmitted to Google.
- **OpenSky Network**: Only the flight callsign is queried — no user data is sent.
- **No data is stored externally** — all results are ephemeral and used only for the current pickup calculation.
- The agent should inform the user on first use that their address will be sent to Google Maps for drive-time calculation (if using Full mode).

## Notes

- OpenSky rate limit: 1 request per 10 sec (anonymous). Polling every 5 min = well within limits.
- Same flight number can have multiple daily legs. Verify the flight is on the expected route.
- For overnight flights, start polling around expected departure + typical flight duration - 1 hour.
- Late-night pickups typically have shorter drive times (less traffic).
- Google Maps `departure_time=now` gives current conditions; for future estimates pass a unix timestamp.
