---
name: tennis-grand-slam-planner
description: >-
  When a user mentions watching tennis, Grand Slam travel, or planning a trip
  to the Australian Open, French Open (Roland Garros), Wimbledon, or US Open,
  activate this skill. It combines the Grand Slam calendar with flyai travel
  APIs to generate a complete "match-chasing" itinerary — including flights,
  hotels near the venue, local attractions, and event tickets — all organized
  around the tournament schedule. Not for general travel planning without a
  tennis event context.
version: 1.0.0
---

# Tennis Grand Slam Planner — Chase the Match Calendar

Plan a complete trip around any of the four tennis Grand Slam tournaments.
This skill turns a simple intent like "I want to watch Wimbledon" into a
fully structured itinerary with flights, stadium-adjacent hotels, match-day
schedules, and pre/post-tournament sightseeing.

## Prerequisites

- **flyai CLI** must be installed: `npm i -g @fly-ai/flyai-cli`
- Verify with: `flyai keyword-search --query "tennis"`

## Workflow

### Step 1 — Identify the target Grand Slam

Ask the user which tournament they want to attend (or infer from context).
Read `references/grand-slam-calendar.md` to get:
- Exact tournament dates, city, venue, and nearby landmarks
- Which rounds fall on which days (so the user can pick specific matches)

If the user only says "the next Grand Slam", use `date +%Y-%m-%d` to determine
the current date and find the nearest upcoming tournament from the calendar.

### Step 2 — Determine trip parameters

Collect (ask if missing):

| Parameter         | Example              | Required |
|-------------------|----------------------|----------|
| Departure city    | "Shanghai" / "Beijing" | Yes    |
| Which rounds      | "Quarter-finals and on" | No (default: full tournament) |
| Budget tier       | "mid-range" / "luxury" | No (default: mid-range) |
| Extend for tourism| "Yes, 2 extra days"  | No (default: no extension) |

Map budget tier to price caps per `references/travel-tips.md`.

### Step 3 — Search flights

Read `references/flyai-commands.md` for exact CLI syntax, then run:

```bash
flyai search-flight \
  --origin "{departure_city}" \
  --destination "{slam_city}" \
  --dep-date {arrive_date} \
  --back-date {leave_date} \
  --sort-type 3
```

**Arrival rule**: Plan arrival **1 day before** the user's first target round.
**Departure rule**: Plan departure **1 day after** the user's last target round
(or after the tourism extension).

### Step 4 — Search hotels

Prioritize proximity to the venue. Run:

```bash
flyai search-hotel \
  --dest-name "{slam_city}" \
  --poi-name "{venue_name}" \
  --check-in-date {arrive_date} \
  --check-out-date {leave_date} \
  --sort distance_asc \
  --max-price {budget_cap}
```

### Step 5 — Search event tickets and local experiences

```bash
flyai keyword-search --query "{slam_name} tickets {year}"
flyai keyword-search --query "{slam_city} tennis experience"
```

### Step 6 — Search nearby attractions (if tourism extension)

```bash
flyai search-poi --city-name "{slam_city}" --category "{category}"
```

Select categories appropriate to the city from `references/grand-slam-calendar.md`.

### Step 7 — Assemble the itinerary

Use the template in `assets/itinerary-template.md` to produce the final output.
Read `references/travel-tips.md` for city-specific advice (transport, food,
visa, weather gear) to include as practical tips.

**The itinerary must follow this structure:**

1. Trip overview (tournament, dates, total budget estimate)
2. Flight options (table with price, duration, airline)
3. Hotel recommendations (top 3, with images and booking links)
4. Day-by-day schedule (match days + rest/tourism days)
5. Ticket and experience booking links
6. Practical tips (visa, weather, transport, etiquette)
7. Source attribution: "Based on fly.ai real-time results"

## Output rules

- All output in valid Markdown
- Hotel images: `![hotel]({mainPic})`
- Attraction images: `![attraction]({picUrl})`
- Booking links: `[Book now]({jumpUrl})` or `[Book now]({detailUrl})` for hotels
- Use tables for multi-option comparisons (flights, hotels)
- Day-by-day schedule in chronological order
- Emphasize key facts: dates, prices, distances to venue

## Error handling

- If no flights found for exact dates, widen the search window by +/- 1 day
- If hotel results are sparse, remove `--max-price` and retry
- If ticket search returns empty, suggest the user check the official tournament
  website and still complete the rest of the itinerary
