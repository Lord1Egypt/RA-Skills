---
name: travel-agent
description: Personal travel planning assistant. Requires a SerpAPI key (stored in ~/.serpapi_credentials). Searches real flights and hotels via Google (SerpAPI), checks the user's calendar, and builds fully costed itinerary options — including multi-stop trips across a country or region. Use when a user wants to plan a trip — whether they have dates and a destination, dates but no destination, or a destination but no dates. Handles single-destination and multi-stop itineraries, flight search, hotel search, internal transport, destination recommendations, seasonal timing advice, and calendar integration. NOT for booking (links to book externally).
metadata:
  clawdbot:
    emoji: "✈️"
    primaryEnv: "SERPAPI_KEY"
    requires:
      env:
        - SERPAPI_KEY
      bins:
        - python3
    configPaths:
      - "~/.serpapi_credentials"
      - "~/.travel_agent_config"
  openclaw:
    requires:
      credentials:
        - name: SERPAPI_KEY
          description: "SerpAPI key for Google Flights/Hotels/Directions search. Get one free at https://serpapi.com"
          paths:
            - "~/.serpapi_credentials"
            - "~/.travel_agent_config"
          required: true
      optional_skills:
        - name: google-calendar
          description: "Used to check the user's availability when dates are not specified (Mode C). If not installed, the skill falls back to asking the user directly."
        - name: outlook-calendar
          description: "Alternative calendar skill. Used for the same purpose as google-calendar if that is not installed."
    file_access:
      - path: "~/.serpapi_credentials"
        reason: "Read SERPAPI_KEY for flight and hotel searches"
      - path: "~/.travel_agent_config"
        reason: "Alternative location for SERPAPI_KEY"
    external_requests:
      - domain: "serpapi.com"
        reason: "Google Flights, Hotels, and Directions search via SerpAPI"
    notes: >
      This skill does NOT book travel — it provides search results and links only.
      All external calls go to serpapi.com using the user's own API key.
      The API key is loaded from the SERPAPI_KEY environment variable or credential files
      only — never passed as a CLI argument to avoid process listing exposure.
      Calendar skill access is optional and only triggered when the user has no
      fixed travel dates; no calendar skill is required for the core functionality.
---

# Travel Agent

## Setup — Credentials

**Requires:** A SerpAPI key. SerpAPI (serpapi.com) provides access to Google Flights, Google Hotels, and Google Maps Directions. A free tier is available with 100 searches/month. Sign up at: https://serpapi.com

Load the user's SerpAPI key before running any search. Check these locations in order:
- `~/.serpapi_credentials` → `SERPAPI_KEY=...`
- `~/.travel_agent_config` → `SERPAPI_KEY=...`

These are the **only** local files this skill reads. If neither file is found, ask the user where their SerpAPI key is stored, or whether they would like to create one at https://serpapi.com.

All flight, hotel, and transport searches are sent to `serpapi.com` using the user's own API key. This skill does not store, transmit, or proxy the key anywhere else.

## Step 1 — Gather Trip Details (always first)

Before searching anything, ask a small set of quick questions. Keep it conversational — one message, not a form. Tailor which questions to ask based on what the user hasn't already told you.

**Questions to ask (as needed):**
- 👥 How many people? (adults + children)
- ✈ Flying from which airport? (if no default configured)
- 💺 Cabin class? (Economy / Premium Economy / Business / First)
- 💰 Rough budget? (per person, or total — flights + hotel)
- 🏨 Hotel preferences? (e.g. beach, city centre, boutique, pool, specific star rating)
- 🎒 Trip vibe? (relaxing beach, city/culture, adventure, food-focused, nightlife, mix)
- 📍 **One place or travel around?** If moving around — roughly how many stops, or leave it to you?
- 🗓 Any flexibility on dates or duration?

Skip questions already answered. Keep to 4–6 questions max in a single message.

## Step 2 — Determine Mode

### Mode A: Dates ✅ + Destination ✅
- If **single stop** → go to Step 3
- If **multi-stop** → go to Step 2M

### Mode B: Dates ✅ + Destination ❓
1. Read `references/seasonal-destinations.md`
2. Suggest 3–4 destination options that match the dates (season fit) and the user's vibe
3. For each option, include: why it's good then, rough flight time, vibe summary, and whether it suits single or multi-stop
4. Wait for user to choose, then return to Mode A or 2M

### Mode C: Destination ✅ + Dates ❓
1. Check for an installed calendar skill — try `google-calendar`, `outlook-calendar`, or any other calendar skill available. This is an **optional** convenience: it checks the user's calendar for free windows to suggest good travel dates. If no calendar skill is found (or the user prefers not to use it), fall back to asking the user directly for their available date windows. **Never access calendar data without the user's awareness.**
2. Read `references/seasonal-destinations.md` for best time to visit that destination
3. Recommend 2–3 date windows ranked by: season fit + calendar availability
4. Present clearly: "Window 1: [dates] — great timing (dry season), you're free. Window 2: ..."
5. Wait for user to confirm dates, then go to Mode A or 2M

---

## Step 2M — Multi-Stop Itinerary Planning

Use when the user wants to travel around a country or region rather than stay in one place.

### 2M-1: Propose a Route
1. Read `references/multi-stop-routes.md` for regional route suggestions
2. Based on total duration, vibe, and number of stops, propose a day-by-day route:
   - Suggest how many nights per stop (balance: enough time to explore, not rushed)
   - Recommend a logical geographic order (minimise backtracking)
   - Note highlight of each stop (what it's known for)
3. Present as a clear itinerary skeleton, e.g.:
   ```
   Days 1–3: Tokyo (arrive, recover, explore)
   Days 4–6: Kyoto (temples, geisha district, day trip to Nara)
   Days 7–9: Osaka (food scene, day trip to Hiroshima)
   Day 10: Fly home from Osaka (KIX)
   ```
4. Invite the user to adjust: swap stops, add/remove places, change durations

### 2M-2: Confirm the Route
Once the user is happy with the skeleton, confirm:
- All stop names and exact dates
- Which city to fly into (may differ from first stop)
- Which city to fly home from (may differ from last stop — open-jaw flights)
- Preferred transport between stops (flight / train / bus / hire car)

### 2M-3: Search All Legs
Run searches for each component in this order:

**Flights:**
- Inbound: home airport → first city
- Between stops: if flying (run `search_flights.py` per leg)
- Outbound: last city → home airport
- Note: for open-jaw (fly into City A, home from City B), search each leg as one-way

**Hotels:**
- Run `search_hotels.py` for each stop with correct check-in/check-out dates

**Internal transport between stops — run BOTH scripts in parallel:**

```bash
# Ground transport (trains, buses, ferries)
python3 scripts/search_transport.py \
  --from "City A, Country" --to "City B, Country" \
  --key $SERPAPI_KEY

# Domestic flights
python3 scripts/search_flights.py \
  --from [IATA_A] --to [IATA_B] --date YYYY-MM-DD \
  --adults N --class economy --currency GBP \
  --key $SERPAPI_KEY
```

Present all options in a single combined comparison, grouped by type:
- ✈ Flights — fastest door-to-door if airports convenient; include airport transfer time in assessment
- 🚄 Train — usually best for city centre → city centre under ~4h; no airport faff
- 🚌 Bus — cheapest, good for budget travellers
- ⛴ Ferry — if applicable (islands, coastal routes)

For each option show: operator, duration, price, booking link.
**Recommend the best option** based on journey time including transfers, price, and convenience — don't just list them.
Note when advance booking is essential (e.g. Trenitalia, Eurostar, Renfe, Shinkansen).

Present the full itinerary in one structured summary — see Step 5M.

---

## Step 3 — Search Flights (single destination)

Run `scripts/search_flights.py`:
```bash
python3 scripts/search_flights.py \
  --from [IATA] --to [IATA] \
  --date YYYY-MM-DD [--return-date YYYY-MM-DD] \
  --adults N [--children N] \
  --class economy|premium_economy|business|first \
  --currency GBP \
  --key $SERPAPI_KEY
```

For round trips, also run the return leg separately for more options.

**Present results as 3–4 options:**
- 💰 Cheapest — lowest price, even if slower
- ⚡ Fastest — fewest stops / shortest duration
- ⭐ Best value — balance of price, airline quality, legroom
- 👑 Premium — best class/airline if budget allows

For each option show: airline + flight number, depart/arrive times, duration, stops, price, aircraft, legroom, any delay warnings.

## Step 4 — Search Hotels (single destination)

Run `scripts/search_hotels.py`:
```bash
python3 scripts/search_hotels.py \
  --location "[CITY] [preference]" \
  --check-in YYYY-MM-DD --check-out YYYY-MM-DD \
  --adults N [--children N] \
  [--stars N] [--amenities "pool,beach"] \
  --sort highest_rating \
  --currency GBP \
  --key $SERPAPI_KEY
```

**Present results as 3 tiers:**
- 🎒 Budget — good rating, lower price
- 🏨 Mid-range — solid choice, best balance
- 🌟 Splurge — top rated, premium amenities

For each: name, stars, rating, price/night, total cost, key amenities, location notes, booking link.

## Step 5 — Iterate (single destination)

After presenting options, invite refinement:
- "Swap to the BA flight instead?"
- "Find something closer to the beach?"
- "What's available in business class?"
- "Show me budget hotels only?"

Re-run the relevant script with adjusted parameters.

## Step 5M — Present Full Multi-Stop Itinerary

Once all flights and hotels are searched, present a complete trip summary:

```
🌍 [TRIP NAME] · [DATE RANGE] · [N] people

DAY 1–3 | CITY A
✈ [Inbound flight] | [time] → [time] | £XX
🏨 [Hotel name] ★★★★ | £XX/night | £XX total

[Train/bus to City B — Xh, book via Trainline: URL]

DAY 4–6 | CITY B
🏨 [Hotel name] ★★★★ | £XX/night | £XX total

✈ [Internal flight if applicable]

DAY 7–9 | CITY C
🏨 [Hotel name] ★★★ | £XX/night | £XX total

✈ [Outbound flight] | [time] → [time] | £XX

💰 TOTAL ESTIMATED COST: £XX
   Flights: £XX | Hotels: £XX | (Transport: £XX est.)
```

Invite iteration on any leg:
- "Upgrade the hotel in City B"
- "Find a cheaper internal flight"
- "Swap City C for City D"
- "Add an extra night in City A"

## Step 6 — Lock In & Calendar

Once the user confirms everything:
1. Summarise full trip with all costs
2. Ask if they'd like the dates blocked in their calendar
3. If yes: check which calendar skill the user has installed (e.g. `google-calendar`, `outlook-calendar`, or any other calendar skill) and use that. Do not assume Google Calendar. This access is **explicitly user-requested** at this step — the user has just asked to add events to their calendar.
   - If no calendar skill is found, offer to generate an `.ics` file the user can import into any calendar app (Google, Apple, Outlook, etc.)
4. Create events for **each** component:
   - Each flight leg: departure datetime → arrival datetime, airline + flight number in title
   - Each hotel stay: check-in → check-out date, hotel name + address
   - Spanning "Trip to [destination]" event across full duration
5. Include booking links in all event descriptions

## Notes
- Always show prices in the user's preferred currency (default GBP if not set)
- SerpAPI free tier = 100 searches/month — multi-stop trips use more quota; heads up if >10 searches in one session
- Open-jaw flights (fly into A, out of B) often work out cheaper than returning to origin — suggest when relevant
- See `references/serpapi.md` for full API reference (flights, hotels, transport/directions)
- See `references/seasonal-destinations.md` for destination/timing guidance
- See `references/multi-stop-routes.md` for regional itinerary templates
