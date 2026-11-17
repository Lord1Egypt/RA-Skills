---
name: flight-connection-risk-analyzer
description: "Use when booking or sweating a connecting flight: computes true connection budget from minimum-connect-time by airport/terminal, transfer logistics (trains, security re-entry), time-of-day delay stacking, and last-flight-of-day exposure. Verdicts SAFE / TIGHT / HIGH RISK plus a survive-the-layover protocol and rebooking rights."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [flights, layover, connection, MCT, travel, airline, delay-risk]
---

# Flight Connection Risk Analyzer

## Overview

Every traveler eventually stares at a booking screen asking: *is a 45-minute
connection at O'Hare insane, or fine?* Airlines will happily sell it — they
compute against the **legal minimum connect time (MCT)**, the fastest possible
wheel-stop-to-departure a marathon runner with no bag could achieve. MCT is not
a plan; it's a floor. What actually decides whether you make a connection:

1. **Buffer above MCT** — scheduled time minus the legal minimum.
2. **Terminal transfer reality** — some airports require a train, a bus, or
   exiting and re-clearing security (international arrivals into the US always
   do: customs + bag recheck + TSA again).
3. **Delay stacking** — on-time performance collapses through the day. A 6 AM
   flight departs on time ~90% of the time; the 7 PM departure of the same
   route inherits every delay of the aircraft's previous legs (~65–70%).
4. **Consequence asymmetry** — miss the last flight of the day and the
   "inconvenience" is a hotel you pay for; on a **self-transfer (separate
   tickets)** the airline owes you nothing and you buy a new walk-up fare.

This skill turns those four factors into a 0–100 risk score, a verdict, and a
protocol. It does not book anything and never claims real-time data — it is a
planning instrument used *before* you click purchase.

## When to Use

- Booking any itinerary with a connection and judging whether the layover is sane
- Deciding between "1h05 at hub X" vs "2h40 at hub Y" vs paying more for nonstop
- Self-transfer itineraries (separate tickets / budget-carrier hops) — the 3-hour doctrine
- International arrivals into the US (customs + recheck + re-security math)
- Already booked a tight connection and wanting the survive-it protocol
- "What happens if I miss it?" — same-ticket protection vs separate-ticket ruin

**Don't use for:** real-time "will my flight make it today" (check the airline
app / FlightAware), or visa/transit-permit questions (see border-buddy).

## The Four-Factor Model

### 1. Connection buffer (the floor)

```
buffer = layover_minutes − MCT(airport, itinerary type)
```

MCT varies by airport AND by itinerary type (domestic→domestic, dom→intl,
intl→dom, intl→intl) AND sometimes by terminal pair. Typical legal minimums:

| Pattern | Typical MCT | Notes |
|---|---|---|
| Domestic → domestic, same terminal | 30–40 min | DL@ATL 35, AA@DFW 40, UA@ORD/DEN 45 |
| Domestic → domestic, terminal change | 45–60 min | JFK T2→T4 style |
| Domestic → international | 60–90 min | Boarding closes earlier; docs check |
| International → domestic (US entry) | 90–120 min | Customs + bag recheck + TSA |
| International → international (same alliance, sterile transit) | 50–75 min | AMS/MUC/IST efficient |
| **Self-transfer (separate tickets)** | **no MCT protection** | Plan ≥ 3h; first ticket's delay is your problem |

### 2. Terminal transfer time

The script carries a per-hub table (walk / train / bus / re-security) for ~25
major hubs. Examples baked in: ATL concourse train 10–15 min; ORD Terminal 5
(intl) ↔ Terminals 1–3 via ATS train 25–40 min **plus security re-entry**;
JFK AirTrain between terminals 20–45 min; LHR T4↔T5 not walkable (~25–35 min);
CDG 2E↔2G shuttle bus ~20 min; IST, MUC, AMS walkable 15–30 min.

### 3. Time-of-day delay stacking (US DOT on-time curves)

Approximate departure on-time rates by scheduled departure block:

| Departure block | On-time (≈) | Delay inheritance |
|---|---|---|
| 05:00–07:00 | 88–92% | aircraft usually fresh |
| 08:00–11:00 | 84–88% | |
| 12:00–15:00 | 78–84% | |
| 16:00–19:00 | 70–78% | cascading |
| 20:00–23:59 | 62–72% | worst stack + overnight risk if missed |

The **inbound aircraft's** departure block matters more than yours: a 9 PM
connection usually rides an aircraft that has flown 4–6 legs already.

### 4. Consequence modifiers

- **Last flight of the day to destination** → miss = overnight (add +15 risk)
- **Winter season (Dec–Feb) at northern hubs** (ORD, DTW, DEN, MSP, JFK) → +10
- **Self-transfer** → +25 and no protection; budget a walk-up-fare disaster cost
- **Same PNR (one ticket)** → airline must rebook you; risk is hours, not dollars
- **International departure missed** → often next-day + visa/hotel cascade

## Scoring & Verdicts

```
risk = base(buffer) + tod_penalty + last_flight + season + self_transfer
  buffer ≥ 60 min  → base 5      buffer 40–59 → 20
  buffer 25–39     → base 40     buffer 10–24 → 60
  buffer < 10 or < MCT → base 85
```

| Score | Verdict | Meaning |
|---|---|---|
| 0–24 | **SAFE** | book it; normal ops you make it with time to eat |
| 25–49 | **TIGHT** | workable, fly the protocol below |
| 50–74 | **HIGH RISK** | only if no alternative; assume realistic 20–30% miss on bad days |
| 75+ | **RUSSIAN ROULETTE** | do not book; you are planning to miss it |

## Survive-a-Tight-Connection Protocol

1. **Seat near the front** of the inbound aircraft (rows within first ~10);
   deplaning last from row 38 costs 10–15 minutes.
2. **Carry-on only.** A checked bag on a <60 min domestic connection is a
   coin-flip on some airlines' ramp handling.
3. Know the **terminal map before landing** (the script prints transfer steps).
4. Tell the flight attendant on approach — they can radio ahead / hold 2 min.
5. On landing, **do not stop**; gates close 10–15 min before departure.
6. If you miss it: same ticket → get in rebooking line **and** open the airline
   app simultaneously (app often rebooks faster than the queue).
7. Self-transfer missed → you are a no-show; buy the next fare and file travel
   insurance / credit-card trip-delay claim if covered.

## Using the Script

```bash
# Domestic connection at ATL, 50 min layover, departing 18:40, not last flight
python3 scripts/connection_scorer.py --airport ATL --layover 50 \
    --type dom-dom --dep-block 16-20

# International arrival into the US connecting at ORD, 1h50, evening
python3 scripts/connection_scorer.py --airport ORD --layover 110 \
    --type intl-dom --dep-block 16-20 --season winter --last-flight

# Separate tickets (self-transfer) through LHR
python3 scripts/connection_scorer.py --airport LHR --layover 165 \
    --type intl-intl --self-transfer --dep-block 12-16

# List the hub knowledge base
python3 scripts/connection_scorer.py --list-hubs
```

Output: MCT used, transfer-time estimate, effective buffer, risk score,
verdict, and a situation-specific protocol list.

## Common Pitfalls

1. **Trusting "legal connection" labels.** Booking sites show itineraries at
   MCT + 0; legal ≠ sane. MCT assumes no line anywhere.
2. **Forgetting US international arrivals re-clear security.** 1h30 at ORD
   from an international arrival is a sprint with a re-TSA line.
3. **Reading the layover as door-to-door.** Deplaning (10–15 min) and boarding
   close (10–15 min) eat 20–30 minutes of every layover before you move.
4. **Self-transfers priced like connections.** Kiwi-style "connections" on
   separate tickets carry no protection — 3 hours minimum, and know the next
   fare.
5. **Evening hub connections in winter.** Stack two risk factors and a
   "workable" 50 minutes becomes a planned overnight.
6. **Connecting to the last flight.** The cheapest itineraries often are;
   multiply the miss cost by "is there a 6 AM flight tomorrow?"

## Verification Checklist

- [ ] Itinerary type matches (dom-dom / dom-intl / intl-dom / intl-intl / self-transfer)
- [ ] Airport hub entry exists in the table (else use generic MCT bands + manual transfer estimate)
- [ ] Departure block of the **inbound** leg used for delay stacking
- [ ] Last-flight-of-day and season flags set when true
- [ ] Verdict ≤ TIGHT before booking; if HIGH RISK, a fallback flight identified
- [ ] Self-transfer: ≥ 3h layover and next-fare price known before booking
