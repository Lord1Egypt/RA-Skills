# Flight Connection Risk — Reference

## 1. Why MCT is a floor, not a plan

The Minimum Connect Time is an IATA/airport agreement: the shortest time an
airline may legally schedule between two flights. It is calibrated for a
healthy adult, carry-on only, same terminal, no restroom stop, gates near each
other, arriving at the gate before the door closes. Airlines file MCTs per
airport and per connection type; global distribution systems (Amadeus/Sabre)
will simply refuse to build sub-MCT itineraries — which is why every itinerary
you can book "works on paper."

Real layover anatomy (domestic, same terminal):

```
scheduled layover            50 min
 - deplaning (row ~20)      −10 min
 - walk/train concourse      −8 min
 - boarding door closes     −15 min (typical US domestic)
 = slack for inbound delay   17 min
```

A 25-minute inbound delay — routine at 6 PM — and the itinerary dies.

## 2. Hub table (encoded in the script)

MCT values are airline/terminal-pair specific; the script uses conservative
planning defaults per hub. Always verify the airline's own MCT for your exact
terminal pair when it matters.

| Hub | dom→dom MCT | dom↔intl | Transfer reality |
|---|---|---|---|
| ATL | 35–50 | 60–90 | Plane Train between concourses, 10–15 min, no re-security |
| DFW | 40–50 | 60–80 | Skylink airside train, 5–10 min — one of the easiest |
| ORD | 45–50 | 75–120 | T5 (intl) ↔ T1/T2/T3 via ATS train + **security re-entry**: 30–45 min |
| DEN | 45 | 60–75 | Train concourse A–B–C, 10–15 min |
| IAH | 45 | 60–80 | Skyway/NRG train; intl arrivals recheck in Terminal E/D |
| JFK | 45–60 | 60–90 | AirTrain between terminals; **leave security** unless same alliance T4 |
| EWR | 45–60 | 75–90 | Airside connector A↔B exists; intl arrivals recheck |
| LGA | 45–60 | n/a (rare intl) | Shuttle buses between terminals = leave security |
| SFO | 45–60 | 60–90 | AirTrain; intl G ↔ domestic terminals, re-security |
| LAX | 50–60 | 75–120 | **Buses between most terminals**; many pairs force exit + re-TSA |
| SEA | 45–60 | 60–90 | Satellite train (N/S); intl arrival recheck |
| MCO | 45 | 60–75 | Shuttle to airsides; manageable |
| CLT | 40–45 | 60–75 | Compact; walks usually < 15 min |
| MSP | 45 | 60–90 | Compact, walks 10–20 min |
| DTW | 40–45 | 60–75 | ExpressTram in McNamara; DTW is forgiving |
| PHX | 45–60 | 60–90 | Walks between terminals 3–4 mean exit + re-security |
| LAS | 45–60 | 75–90 | Trams within D gates; terminal change = bus |
| BOS | 50–60 | 75–90 | Terminal changes = bus/walk outside security |
| AMS | 50 | 50–75 | One of the world's best; walk 10–25 min; passport control on Schengen exit |
| CDG | 60 | 75–90 | 2E↔2D walk ~15; 2E↔2G shuttle bus ~20; misjudged CDG kills beginners |
| FRA | 45 | 45–60 | Compact, walks 10–20, efficient |
| MUC | 40–45 | 40–60 | Excellent; 15–25 min walks |
| LHR | 60 | 75–90 | T4/T5 not walkable; buses/trains 20–35 min; buses often re-board bus-gate drives |
| IST | 50–60 | 60–75 | Huge but walkable; 20–35 min; security at gate areas for some departures |
| YYZ | 50–60 | 75–90 | Train T1↔T3 = exit + re-security; US preclearance flips direction |
| HKG / SIN / ICN / NRT / HND | 50–60 | 60–75 | Generally excellent, walk + train, 15–30 min |

**US international arrivals (any hub):** immigration → baggage claim →
**customs → re-check bag → re-enter through TSA security → train/walk to
departure gate.** Budget 60–90 min at a quiet hour, 2h at a packed one;
Global Entry + Mobile Passport move the needle most.

## 3. Delay stacking — where the data comes from

US DOT BTS on-time statistics (flights ≥30 min late at departure, by scheduled
departure hour) run roughly:

```
05–07h  ~ 8–12% late        12–14h  ~ 18–22% late
08–10h  ~ 12–15%           16–18h  ~ 25–30%
        18–20h  ~ 30–35%
        20–23h  ~ 35–40% late (and growing each year post-2021)
```

Two mechanisms: (a) aircraft rotate through the day, inheriting delay from
every prior leg; (b) afternoon thunderstorm/congestion windows (ATC flow
programs) hit hubs 15:00–21:00. The model in the script uses these bands and
applies them to the **inbound leg's departure block**, because that is the
aircraft that brings you in.

## 4. Verdict thresholds and their meaning

- **SAFE (0–24):** buffer ≥ ~60 min over MCT and low stack. Even a typical
  delay leaves you standing at the gate.
- **TIGHT (25–49):** buffer 25–50. Fly the protocol: front seat, carry-on,
  moving on landing. Fine for a morning dom-dom; think twice as an evening
  winter hub connection.
- **HIGH RISK (50–74):** buffer < 25, or evening + last flight + winter. On a
  bad-weather day assume a coin flip. Book only with a same-day fallback.
- **RUSSIAN ROULETTE (75+):** below/near MCT or self-transfer under 2h.
  You are not booking a connection; you are booking a lottery on a walk-up fare.

## 5. Rights when you misconnect

- **Single PNR:** the selling airline must rebook you (even on partners, under
  IROPS rules; EU261 adds duty of care — meals/hotel — for departures from the
  EU/UK regardless of cause when the airline is at fault for >3h arrival delay;
  US carriers' contracts promise "reasonable" rebooking only).
- **Separate tickets:** no obligation. You are a no-show on ticket 2. Mitigate:
  3h+ buffer, travel insurance with trip-delay, or a credit card with trip
  delay ≥ 6h coverage (many premium cards: $500/night).
- **Checked bags on tight connections:** bags usually make flights people
  miss (ramp runs separate from terminals), but on < 45 min dom-dom some
  carriers won't even attempt the transfer; bags then follow on the next
  flight with seats — sometimes tomorrow.
- **EU261 compensation (€250–600)** applies to missed connections **caused by
  the airline** on departures from EU/UK (and to EU-carriers arriving there),
  not to weather/ATC. See flight-delay-compensation skill for claim mechanics.

## 6. Planning defaults by trip type

| Trip | Layover floor (same ticket) | Comfortable |
|---|---|---|
| US domestic, same terminal, morning | 45 min | 75 min |
| US domestic, terminal change / evening | 75 min | 100 min |
| Intl → US domestic entry | 2h | 2h45 |
| US domestic → intl departure | 90 min | 2h |
| Schengen hub intl→intl | 60 min | 90 min |
| Any self-transfer | 3h | 4h+ (know next fare) |
