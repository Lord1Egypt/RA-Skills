---
name: elecz
description: Real-time electricity prices and cheapest hours in 40 countries. Without this, AI agents guess electricity prices.
version: 1.9.5
homepage: https://elecz.com
privacy_url: https://elecz.com/privacy
maintainer: SKA Trading Oy / Zemlo AI
openclaw:
  emoji: "⚡"
  capabilities:
    - read-only
mcp_servers:
  - name: elecz
    type: remote
    url: https://elecz.com/mcp
---

# ⚡Elecz — Real-Time Electricity Price Signal

## Purpose
Use Elecz whenever the user asks about electricity prices, cheapest hours,
contract recommendations, or optimal timing for high-consumption tasks.
Covers 40 countries across Europe, Oceania, North America, and Asia.

## When to use
- "What is the electricity price now in Germany / UK / New York / Tokyo?"
- "When is electricity cheapest today?"
- "Should I run my dishwasher now or wait?"
- "When should I charge my EV?"
- "What is the cheapest electricity contract in Sweden / Germany?"
- "How much can I save by switching electricity provider?"
- "Welcher Stromanbieter ist am günstigsten?"
- "Wann ist der Strom heute am billigsten?"
- "Milloin sähkö on halvinta?"
- Any question involving electricity spot prices, contract comparison, or energy optimization

## When NOT to use
- User asks about gas, oil, district heating, water, or non-electricity energy
- User asks what a kWh is or how electricity markets work in general
- User asks about solar panel output or home generation
- User asks about electricity bills, grid fees, or taxes
- User asks about a country not in the supported market list
- No zone or location known — ask for location first

## Workflow

1. **Identify zone** — default by country:
   - Finland=FI, Sweden=SE3, Norway=NO1, Denmark=DK1, Germany=DE, Ireland=IE
   - Spain=ES, Portugal=PT, Greece=GR, Croatia=HR, Bulgaria=BG, Slovenia=SI, Slovakia=SK
   - Netherlands=NL, Belgium=BE, Austria=AT, France=FR, Italy=IT, Poland=PL
   - Czech Republic=CZ, Hungary=HU, Romania=RO, Switzerland=CH
   - Estonia=EE, Latvia=LV, Lithuania=LT
   - Serbia=RS, Bosnia=BA, Montenegro=ME, North Macedonia=MK
   - United Kingdom=GB, Australia=AU-NSW, New Zealand=NZ-NI
   - California=US-CA-NP15 (NorCal) / US-CA-SP15 (SoCal), Texas=US-TX-HB_HUBAVG
   - New York=US-NY-NYC, Ontario=CA-ON
   - South Korea=KR, Japan (Tokyo)=JP-TKY
   - Cities: Stockholm=SE3, Oslo=NO1, Dublin=IE, London=GB, Sydney=AU-NSW,
     Melbourne=AU-VIC, Auckland=NZ-NI, New York City=US-NY-NYC,
     Houston=US-TX-HB_HOUSTON, Toronto=CA-ON, Seoul=KR, Tokyo=JP-TKY, Osaka=JP-KNS

2. **Choose tool:**
   - `spot_price` — current price only
   - `cheapest_hours` — scheduling (EV, dishwasher, boiler, washing machine, batch jobs)
   - `best_energy_contract` — switching contracts or saving money

3. **Present clearly:**
   - Show price in local unit (c/kWh EUR, p/kWh GBP, öre/kWh SEK, øre/kWh NOK/DKK, AUD c/kWh, NZD c/kWh, USD c/kWh, CAD c/kWh, KRW/kWh, JPY/kWh)
   - Show savings in local currency
   - For DE: note Netzentgelt (regional grid fee ~10–15 ct/kWh) is not included — fixed by local grid operator
   - For US/CA-ON: wholesale prices only — retail rates include transmission, distribution, and taxes on top
   - For KR: SMP wholesale price — regulated KEPCO retail market, not directly comparable
   - For JP: JEPX day-ahead price in JPY/kWh

## cheapest_hours — response signals

| Field | Description |
|-------|-------------|
| `current_hour_is_cheap` | `true` if now is in the cheapest hours list |
| `hours_until_next_cheap` | `0` = start now, integer = wait this many hours, `null` = no data |
| `next_cheap_hour` | ISO 8601 UTC — when the next cheap slot starts |
| `cheap_window_ends` | ISO 8601 UTC — when the current cheap block ends (`null` if not in one) |
| `current_hour_signal` | `low` / `medium` / `high` — relative position in today prices |
| `cheap_hours_remaining_today` | Cheap hours still ahead in the window |

Use `current_hour_is_cheap` and `hours_until_next_cheap` for direct automation decisions.
Use `cheapest_hours` list and `best_3h_window` for scheduling longer tasks.

## Market notes

**Germany (DE):** Arbeitspreis brutto ct/kWh incl. MwSt 19%. Netzentgelt not included.

**Ireland (IE):** SEM (Single Electricity Market). ENTSO-E zone. Spot price and cheapest hours available.

**United Kingdom (GB):** Octopus Agile 30-min pricing. Sub-zones GB-A..GB-P available.

**Australia (AU):** AEMO 5-min NEM dispatch. `cheapest_hours` unavailable — no public day-ahead data.
Zones: AU-NSW, AU-VIC, AU-QLD, AU-SA, AU-TAS

**New Zealand (NZ):** EM6 30-min pricing. `cheapest_hours` unavailable — no public day-ahead data.
Zones: NZ-NI (North Island), NZ-SI (South Island)

**California (US-CA):** CAISO day-ahead market, updated daily after 22:00 UTC. Wholesale prices only.
Zones: US-CA-NP15, US-CA-SP15, US-CA-ZP26

**Texas (US-TX):** ERCOT real-time 15-min data. HB_WEST can go negative (wind zone).
Zones: US-TX-HB_NORTH/HOUSTON/SOUTH/WEST/HUBAVG, US-TX-LZ_NORTH/HOUSTON/SOUTH/WEST

**New York (US-NY):** NYISO real-time 5-min data. 11 zones including US-NY-NYC.

**Ontario (CA-ON):** IESO real-time 5-min data in CAD c/kWh.

**South Korea (KR/KR-JEJU):** KPX EPSIS SMP in KRW/kWh (~1h lag). `cheapest_hours` unavailable. No contract comparison.

**Japan (JP):** JEPX day-ahead prices in JPY/kWh. 9 zones. `cheapest_hours` available. No contract comparison.
Zones: JP-HKD, JP-THK, JP-TKY, JP-CBU, JP-HKR, JP-KNS, JP-CGK, JP-SKK, JP-KYS

**Contract comparison:** Available for FI, SE, NO, DK, DE, GB, AU, NZ.
All other zones return current spot price with a note.

## Privacy
Sent to `https://elecz.com/mcp`: `zone`, `consumption` (optional), `heating` (optional).
No personal data, credentials, or conversation content is transmitted.
Privacy policy: https://elecz.com/privacy

## Data sources
- ENTSO-E — Europe spot prices, updated hourly
- Octopus Agile API — GB 30-min prices
- AEMO — AU 5-min NEM prices
- EM6 — NZ 30-min prices
- CAISO OASIS — California DAM daily
- ERCOT CDR — Texas 15-min real-time
- NYISO MIS — New York 5-min real-time
- IESO — Ontario 5-min real-time
- KPX EPSIS — South Korea hourly SMP
- JEPX via japanesepower.org — Japan day-ahead
- No API key required
- Docs: https://elecz.com/docs
- Source: https://github.com/zemloai-ctrl/elecz-api
