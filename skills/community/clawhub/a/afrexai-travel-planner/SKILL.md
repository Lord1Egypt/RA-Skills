---
name: afrexai-travel-planner
description: Complete travel planning system — from trip research to packing lists, budgets, itineraries, and travel hacks. Use when planning any trip (solo, family, business, group, international, road trip, or budget travel).
---

# Travel Planner Mastery

A complete system for planning trips that actually go smoothly — from first idea to post-trip review. Works for weekend getaways and month-long international journeys.

---

## Phase 1: Trip Discovery & Research

### Trip Brief Template

```yaml
trip:
  name: "[descriptive name]"
  type: solo | couple | family | group | business
  travelers:
    - name: "[name]"
      age: [age]
      needs: ["dietary restrictions", "mobility", "medications"]
  dates:
    departure: "YYYY-MM-DD"
    return: "YYYY-MM-DD"
    flexible: true | false
    flex_range: "[+/- N days]"
  destinations:
    - city: "[city]"
      country: "[country]"
      nights: [N]
      priority: must-visit | nice-to-have
      why: "[what you want to do/see here]"
  budget:
    total: [amount]
    currency: "[USD/GBP/EUR]"
    style: budget | mid-range | comfort | luxury
    includes_flights: true | false
  interests:
    - "[culture/history/food/adventure/beach/nature/nightlife/shopping/photography]"
  constraints:
    - "[visa restrictions, health conditions, kids ages, pet-friendly needed]"
  travel_style: slow | moderate | packed
```

### Destination Research Checklist

For each destination, research:

| Category | Questions | Source |
|----------|-----------|--------|
| Safety | Travel advisories? Common scams? Areas to avoid? | Gov travel sites (state.gov, gov.uk/foreign-travel) |
| Weather | Temperature range, rainy season, best months? | Web search "[city] weather [month]" |
| Visa | Visa required? Duration? Cost? Processing time? | Embassy websites |
| Health | Vaccinations needed? Travel insurance required? Tap water safe? | CDC, WHO |
| Money | Local currency? ATM availability? Card acceptance? Tipping culture? | Web search |
| Language | Primary language? English widely spoken? Key phrases? | Web search |
| Transport | Airport to city? Local transit? Uber/Grab available? Driving side? | Web search |
| Connectivity | SIM card or eSIM availability? WiFi reliability? | Web search |
| Culture | Dress code? Photography rules? Customs to respect? | Web search |
| Timing | Public holidays during visit? Major events? Ramadan? | Web search |

### Season & Timing Matrix

| Factor | Best | Acceptable | Avoid |
|--------|------|-----------|-------|
| Weather | Dry + comfortable temp | Shoulder season (cheaper, smaller crowds) | Monsoon, extreme heat/cold |
| Crowds | Off-season | Shoulder | Peak holiday / national events |
| Price | Off-peak (Jan-Mar, Sep-Nov for most) | Shoulder | Christmas, Easter, summer, Chinese New Year |
| Flights | Tue-Thu departures | Mon, Fri | Sun evening, holiday weekends |

**Pro tip:** The intersection of "good weather + low crowds + cheaper flights" is the sweet spot. Usually 2-4 weeks per destination per year.

---

## Phase 2: Budget Planning

### Budget Allocation by Travel Style

| Category | Budget (%) | Mid-Range (%) | Comfort (%) | Luxury (%) |
|----------|-----------|---------------|-------------|------------|
| Flights/Transport | 35-40 | 30-35 | 25-30 | 20-25 |
| Accommodation | 25-30 | 25-30 | 30-35 | 35-40 |
| Food & Drink | 15-20 | 15-20 | 15-20 | 15-20 |
| Activities | 10-15 | 10-15 | 10-15 | 10-15 |
| Buffer (emergencies) | 10 | 10 | 10 | 10 |

### Daily Budget Benchmarks (per person, USD)

| Region | Budget | Mid-Range | Comfort |
|--------|--------|-----------|---------|
| Southeast Asia | $30-50 | $50-100 | $100-200 |
| Eastern Europe | $40-60 | $70-120 | $120-250 |
| Western Europe | $60-100 | $120-200 | $200-400 |
| USA/Canada | $60-100 | $120-200 | $200-400 |
| Japan/Korea | $50-80 | $100-180 | $180-350 |
| Australia/NZ | $60-100 | $120-200 | $200-400 |
| Central/South America | $30-50 | $50-100 | $100-200 |
| Middle East | $40-70 | $80-150 | $150-350 |
| Africa (tourist areas) | $40-70 | $80-150 | $150-400 |

### Budget Tracker Template

```yaml
budget:
  total_allocated: [amount]
  currency: "USD"
  categories:
    flights:
      allocated: [amount]
      spent: 0
      items:
        - description: "[outbound flight]"
          amount: [cost]
          booked: true | false
          refundable: true | false
    accommodation:
      allocated: [amount]
      spent: 0
      items: []
    food:
      allocated: [amount]
      daily_target: [amount/day]
    activities:
      allocated: [amount]
      items: []
    transport_local:
      allocated: [amount]
    insurance:
      allocated: [amount]
    buffer:
      allocated: [amount]
  total_spent: 0
  remaining: [amount]
```

### Money-Saving Strategies (Ranked by Impact)

| Strategy | Typical Savings | Effort |
|----------|----------------|--------|
| Fly mid-week (Tue/Wed) | 15-30% on flights | Low |
| Book flights 6-8 weeks ahead (domestic) / 2-4 months (international) | 10-25% | Low |
| Stay in apartments with kitchen (cook breakfast/lunch) | 30-50% on food | Medium |
| Use Google Flights price tracking alerts | 5-20% | Low |
| Travel shoulder season | 20-40% on everything | Low |
| Use credit card with no foreign transaction fees | 3% saved on all spending | Low |
| Book accommodation with free cancellation, then price-match closer to date | 10-20% | Medium |
| Use local transit instead of taxis | 50-80% on transport | Medium |
| Get a local eSIM instead of roaming | 80-90% on data | Low |
| Book activities directly (not hotel/cruise) | 20-40% on activities | Medium |

---

## Phase 3: Itinerary Building

### Itinerary Architecture

```yaml
day:
  number: [N]
  date: "YYYY-MM-DD"
  location: "[city]"
  weather_expected: "[sunny, 25°C]"
  morning:
    activity: "[what]"
    time: "09:00-12:00"
    address: "[where]"
    cost: [amount]
    booking_needed: true | false
    booking_ref: "[ref]"
    notes: "[tips, what to bring]"
  lunch:
    restaurant: "[name or area]"
    cuisine: "[type]"
    budget: [amount]
    reservation: true | false
  afternoon:
    activity: "[what]"
    time: "14:00-17:00"
    address: "[where]"
    cost: [amount]
  evening:
    activity: "[dinner, show, walk, rest]"
    time: "19:00-22:00"
  transport:
    - from: "[A]"
      to: "[B]"
      method: "[walk/metro/taxi/bus]"
      duration: "[time]"
      cost: [amount]
  total_cost: [amount]
  notes: "[pack rain jacket, charge camera, early start]"
```

### Pacing Rules

| Travel Style | Activities/Day | Walk Distance | Rest Time |
|--------------|---------------|---------------|-----------|
| Packed | 3-4 major | 15-20km | Minimal |
| Moderate | 2-3 major | 10-15km | 1-2hr midday |
| Slow | 1-2 major | 5-10km | Generous |

**Adjustments:**
- With kids under 6: -50% activities, +100% buffer time
- With seniors: -30% walking, add rest stops
- In heat (>30°C): avoid 12-3pm outdoor, plan indoor for midday
- Jet lag: easy Day 1, no early starts for 2 days after long-haul

### The 3-2-1 Rule for Multi-City Trips

- **3 nights minimum** per city (less = too rushed, just surface)
- **2 "must-do" activities** per city (rest is flexible discovery)
- **1 rest day** per 5 travel days (no agenda, wander, recover)

### Transit Day Rules

- No activities planned on transit days (travel takes longer than expected)
- Allow 3 hours minimum for international connections
- Arrive at accommodation by 4pm if possible (check-in, orient, rest)
- Pre-download offline maps for every city before transit

---

## Phase 4: Flights & Transport

### Flight Search Strategy

1. **Set alerts** — Google Flights, Skyscanner, or Hopper for your routes
2. **Check flexible dates** — ±3 days can save 20-40%
3. **Compare airports** — nearby airports often have better deals
4. **Consider positioning flights** — sometimes a budget flight to a hub + long-haul from hub is cheaper
5. **Check airline directly** — after finding the deal on aggregator, sometimes cheaper on airline site

### Flight Booking Decision

| Factor | Choose This |
|--------|------------|
| Cheapest fare | Budget carrier if <4hr flight, tolerable seats |
| Long haul (>6hr) | Prioritize comfort — extra legroom worth it |
| Connections | Minimum 2hr domestic, 3hr international |
| Refundable? | Yes for uncertain plans; no for confirmed |
| Checked bags | Compare "basic fare + bag" vs "regular fare" total |

### Ground Transport Comparison

| Method | Best For | Typical Cost | Book When |
|--------|----------|-------------|-----------|
| Train | Europe, Japan, scenic routes | $$ | 1-3 months ahead for deals |
| Bus | Budget, Southeast Asia, Latin America | $ | 1-3 days ahead |
| Rental car | Road trips, rural areas, groups | $$-$$$ | 2-4 weeks ahead |
| Ride share | Airport transfers, short city hops | $$ | Day of |
| Domestic flight | Long distances, island hopping | $$-$$$ | 4-8 weeks ahead |

### Rental Car Checklist

- [ ] International driving permit needed?
- [ ] Drive on left or right?
- [ ] Book smallest car that fits luggage + passengers
- [ ] Decline CDW if credit card covers it (check BEFORE trip)
- [ ] Photo the car at pickup (all sides, existing damage)
- [ ] Full-to-full fuel policy preferred
- [ ] Download offline maps (Google Maps or Maps.me)
- [ ] Toll transponder needed?
- [ ] Parking strategy for each stop

---

## Phase 5: Accommodation

### Accommodation Decision Matrix

| Factor | Hotel | Airbnb/Apartment | Hostel |
|--------|-------|-----------------|--------|
| Best for | Business, short stays, luxury | Families, long stays, self-catering | Solo, budget, social |
| Book when | 2-4 weeks ahead | 1-3 months ahead (popular areas) | 1-2 weeks ahead |
| Check | Free cancellation, breakfast included | Kitchen, washer, WiFi speed, check-in time | Locker, reviews, location |

### Accommodation Quality Checklist

Score each option 1-5:

| Criteria | Weight | Score |
|----------|--------|-------|
| Location (walkable to key sites + transit) | 5x | |
| Reviews (4.0+ overall, read recent negatives) | 4x | |
| Price vs budget | 3x | |
| Amenities match needs (kitchen, AC, WiFi, laundry) | 3x | |
| Cancellation flexibility | 2x | |
| Check-in flexibility | 1x | |

**Total = weighted sum. Compare options numerically, not emotionally.**

### Location Priority Order

1. Near public transit (metro/tram stop within 5 min walk)
2. Safe neighborhood (check reviews + safety maps)
3. Near at least one key attraction
4. Grocery store / restaurants within walking distance
5. Quiet at night (not above a bar/club unless that's your thing)

---

## Phase 6: Packing

### Universal Packing List

**Documents (carry-on ONLY):**
- [ ] Passport (valid 6+ months beyond trip end)
- [ ] Visa (printed if required)
- [ ] Travel insurance docs (printed + digital)
- [ ] Flight confirmations (printed + digital)
- [ ] Accommodation confirmations
- [ ] Vaccination records (if needed)
- [ ] Driver's license + international permit
- [ ] Emergency contacts card
- [ ] 2x passport photos (spare, for emergency visa)
- [ ] Copies of all documents (separate from originals)

**Tech:**
- [ ] Phone + charger
- [ ] Power adapter (destination-specific)
- [ ] Portable battery pack (10,000+ mAh)
- [ ] Headphones
- [ ] Camera + charger + SD cards
- [ ] Laptop/tablet (if needed)
- [ ] eSIM or local SIM plan confirmed

**Health & Safety:**
- [ ] Medications (prescription in carry-on, letter from doctor)
- [ ] First aid basics (band-aids, pain relief, anti-diarrheal, antihistamine)
- [ ] Sunscreen
- [ ] Insect repellent (tropical destinations)
- [ ] Hand sanitizer
- [ ] Face masks (2-3)
- [ ] Water bottle (refillable)

**Clothing Formula:**
Use the **5-4-3-2-1 rule** for 1-2 week trips:
- 5 tops (mix casual + 1 nice)
- 4 bottoms (2 pants/shorts + 1 nice + 1 active)
- 3 pairs of shoes (walking, nice, flip-flops/sandals)
- 2 outerwear (jacket + light layer)
- 1 formal outfit (if needed)

**Laundry hack:** Pack for 5-7 days max regardless of trip length. Do laundry.

### Carry-On vs Check Rules

**Always carry-on:**
- Documents, valuables, medications, 1 change of clothes, phone/charger, entertainment
- Why: if luggage is lost, you survive Day 1

**Check:**
- Liquids >100ml, bulky items, anything you wouldn't cry about losing

### Packing by Climate

| Climate | Add |
|---------|-----|
| Tropical | Quick-dry everything, insect repellent, rain poncho, waterproof phone case |
| Cold | Thermal base layer, down jacket (compresses small), warm hat + gloves, lip balm |
| Desert/Dry | Wide-brim hat, SPF 50+, light long sleeves, extra water bottle |
| Rainy | Waterproof jacket (not umbrella — hands free), quick-dry shoes, dry bags for electronics |
| Mixed/Urban | Layers, versatile shoes (walking-friendly but restaurant-appropriate) |

---

## Phase 7: Travel Day Logistics

### Airport Checklist

**Before leaving:**
- [ ] Online check-in (24hr before)
- [ ] Boarding pass saved offline
- [ ] Passport + documents in accessible pocket
- [ ] Snacks packed (airport food is expensive)
- [ ] Accommodation address saved offline
- [ ] Offline maps downloaded
- [ ] Transport from destination airport planned

**Timing:**
- Domestic: arrive 1.5-2hr before departure
- International: arrive 2.5-3hr before
- First time at this airport: add 30 min buffer

### Transit Day Survival Kit (in personal bag)

- Passport + boarding pass
- Phone + portable charger
- Headphones
- Snacks + empty water bottle (fill after security)
- Neck pillow (long flights)
- Pen (immigration forms)
- 1 change of clothes in carry-on (long-haul or connections)

---

## Phase 8: During the Trip

### Daily Routine

**Morning:**
1. Check weather forecast → adjust plans if needed
2. Confirm any reservations/tickets for today
3. Charge all devices
4. Pack day bag (water, snacks, sunscreen, battery pack, camera)

**Evening:**
1. Back up photos (cloud or external drive)
2. Update budget tracker
3. Review tomorrow's plan
4. Charge everything overnight

### Eating Strategy

| Approach | Best For | How |
|----------|----------|-----|
| Cook breakfast | Budget, families | Stay in apartments with kitchen |
| Lunch as main meal | Europe, Asia | Lunch menus/set meals are 30-50% cheaper than dinner |
| Street food | Southeast Asia, Mexico, India | Follow locals, busy stalls = fresh, avoid raw |
| Grocery + picnic | Scenic destinations | Buy local cheese, bread, fruit — eat in parks |
| Splurge dinner | Special occasions | Book 1 nice restaurant per city, skip the rest |

### Safety Essentials

1. **Share itinerary** with someone not on the trip
2. **Register with embassy** for high-risk destinations
3. **Split cash and cards** — don't carry everything in one place
4. **Use hotel safe** for passport (carry a photocopy)
5. **Trust your gut** — if something feels wrong, leave
6. **Emergency numbers** saved in phone contacts: local police, embassy, insurance hotline, emergency contact back home

### Photo & Memory Strategy

- Take photos at the START of the day (fresh energy, good light)
- One "postcard shot" per major site, then put camera away and experience it
- Video: 10-30 second clips, not minutes-long recordings
- Daily: write 3 bullet points about the day (you'll forget details in weeks)
- Backup: upload to cloud every evening

---

## Phase 9: Post-Trip

### Post-Trip Checklist

- [ ] Back up all photos/videos to cloud + local drive
- [ ] Submit travel insurance claims (if any)
- [ ] Submit expense reports (business trips)
- [ ] Leave reviews (accommodation, activities — while fresh)
- [ ] Update budget with final totals
- [ ] Cancel any local SIM/subscriptions
- [ ] Unpack and launder immediately (jet lag makes this harder each day)
- [ ] Send thank-you notes (hosts, guides)

### Trip Review Template

```yaml
trip_review:
  name: "[trip name]"
  dates: "[when]"
  destinations: ["[list]"]
  total_spent: [amount]
  budget_variance: "[over/under by X%]"
  highlights:
    - "[best experience]"
    - "[best meal]"
    - "[best surprise]"
  lessons:
    - "[what would you do differently]"
    - "[what worked perfectly]"
  recommendations:
    - "[for others visiting same place]"
  would_return: true | false
  rating: [1-10]
```

---

## Phase 10: Specialized Trip Types

### Business Travel

- Book refundable fares and flexible accommodation
- Pack 2 complete outfits per day (backup for spills/weather)
- Arrive day before meetings (never morning-of for important ones)
- Hotel near meeting venue > cheaper hotel far away
- Keep all receipts (photo + email to self = backup)
- Travel insurance with trip interruption + electronics coverage

### Family Travel (with kids)

- **Under 2:** Bring car seat adapter for flights, pack triple the diapers you think you need, book accommodation with crib + washing machine
- **2-5:** Max 2 activities/day, always have snacks, midday nap/rest is non-negotiable, kid-friendly restaurant = one with a garden/terrace
- **6-12:** Involve them in planning (pick 1 activity per day), bring card games, activity books for transit, walking tours > museum tours
- **Teens:** Let them plan 1 full day, give them photo challenges, budget exercise (here's $X for souvenirs — your choice)

### Solo Travel

- Stay in social accommodation (hostels, guesthouses with common areas)
- Join walking tours (free ones are good for orientation + meeting people)
- Eat at bar seats / communal tables
- Share location with someone back home
- Trust instincts about people and situations
- Solo dining tip: bring a book or journal — you'll feel less self-conscious

### Road Trips

- Plan max 4-5 hours driving per day (more = exhausting)
- Stop every 2 hours
- Download offline music/podcasts before departure
- Pre-book first and last night accommodation, leave middle flexible
- Fill gas at half tank (not when empty)
- Pack a cooler (saves money + time on food stops)

---

## Phase 11: Travel Hacks & Tips

### Top 20 Travel Hacks (Ranked by Impact)

| # | Hack | Why |
|---|------|-----|
| 1 | Get a no-foreign-transaction-fee credit card | Saves 3% on everything abroad |
| 2 | Always get local eSIM/SIM | 10x cheaper than roaming, essential for maps/translation |
| 3 | Download offline maps for every city | Works without data, saves battery vs live maps |
| 4 | Book accommodation with free cancellation | Lock in prices, refine later |
| 5 | Pack half of what you first think | You will NEVER regret packing light |
| 6 | Use Google Translate camera mode | Point at menus/signs — instant translation |
| 7 | Arrive early at popular sites (opening time) | 50% fewer crowds, better photos, cooler temps |
| 8 | Eat where locals eat (away from tourist streets) | Better food, lower prices, authentic |
| 9 | Carry a photocopy of passport | Accepted most places, protects original |
| 10 | Use ATMs for foreign currency (not exchange bureaus) | Better rates, lower fees |
| 11 | Reconfirm flights 24hr before | Catch schedule changes early |
| 12 | Keep a daily expense note | Prevents budget surprise at the end |
| 13 | Wear your bulkiest clothes on the plane | Saves luggage space and weight |
| 14 | Screenshot all confirmations | Works offline when you need them |
| 15 | Learn 5 phrases in local language | "Hello, please, thank you, sorry, how much" = respect |
| 16 | Use laundry services (or laundromats) instead of packing more | Worth the $5-10 |
| 17 | Book tours/activities through local operators (not hotel desk) | 20-50% cheaper |
| 18 | Get travel insurance (seriously) | One medical emergency can cost $50K+ |
| 19 | Set up banking notifications | Know instantly if card is charged unexpectedly |
| 20 | Use packing cubes | Organization + compression = more space |

---

## Natural Language Commands

- "Plan a trip to [destination] for [dates]" → Generate trip brief + research checklist + budget estimate
- "Build an itinerary for [N] days in [city]" → Day-by-day plan with timing, costs, and transport
- "What should I pack for [destination] in [month]?" → Climate-appropriate packing list
- "Create a budget for [trip type] in [region]" → Budget allocation with daily estimates
- "Compare [destination A] vs [destination B] for [dates]" → Side-by-side on weather, cost, activities
- "What do I need to know about [country]?" → Research checklist filled in (visa, safety, money, transport)
- "Plan a road trip from [A] to [B]" → Route, stops, drive times, accommodation suggestions
- "Help me save money on [trip]" → Ranked money-saving strategies specific to that trip
- "Review my itinerary" → Pacing analysis, gap identification, cost check, logistics review
- "Create a family travel plan for [destination] with [kids ages]" → Age-adjusted itinerary with family tips
- "What's the best time to visit [destination]?" → Season matrix with weather, crowds, and pricing
- "Post-trip review for [trip]" → Review template with budget analysis
