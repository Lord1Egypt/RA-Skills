---
name: football-pilgrimage
description: |
  Generate a football pilgrimage guide for any team — stadium tours, football museums, fan pubs, and cultural landmarks. Each spot comes with deep storytelling (history, legends, anecdotes). Includes "On This Day" feature matching travel dates to historic football events, **live match detection during trip dates**, and **ticket search** (match tickets, attraction tickets via flyai).
  Use when: user asks for a football pilgrimage, stadium tour guide, fan culture trip, "pilgrimage guide" for a specific team, or wants to search for match/attraction tickets.
  Don't use when: user asks for match results, live scores, standings, or player stats (use football-data instead).
license: MIT
metadata:
  author: user-local
  version: "0.3.0"
---

# Football Pilgrimage Guide

Generate an emotionally resonant football pilgrimage guide. Input: a team name (+ optional travel dates). Output: a narrative-driven travel guide where **every spot tells a story**, enhanced with "On This Day" historic events, **automatic match detection during your trip**, and the team's official crest.

**Language rule**: Match the user's language. If the user writes in Chinese, output the entire guide in Chinese. If in English, output in English. Always mirror the user's input language — including the pre-check prompts, phase titles, spot stories, On This Day narratives, and all other text.

## Dependencies

- **ESPN API** (primary): Team info (team_id, name, crest URL) and match schedule — via ESPN's public REST API, no API key needed
- **Wikipedia** (via Web Search): Team history, stadium info, founding story, legends, honors — search `"{team_name} wikipedia history stadium legends"` to get Wikipedia content through search results, since `web_fetch` on Wikipedia may timeout
- **Web Search**: Stadium tours, museums, fan pubs, landmarks, **spot backstories**, **historic events** (On This Day)
- **flyai** (optional): Flight and hotel booking if user provides departure city

## ESPN API Reference

See [references/espn-api.md](references/espn-api.md) for full API documentation including base URL, league slugs, endpoints, response formats, team lookup guide, and common team IDs.

## Quick Start

User: "Generate an AC Milan football pilgrimage guide, departing April 15"

1. ESPN API: search teams in `ita.1` → find AC Milan (team_id=103), get crest URL (see [ESPN API Reference](references/espn-api.md))
2. Web search `"AC Milan wikipedia history stadium legends"` → founding story, stadium (San Siro), legends, honors
3. ESPN API: fetch schedule for team 103 → check for matches between April 15-19, extract stadium name
4. Web search for stadium tour, football museum, fan pubs — **and the story behind each spot**
5. Web search `"AC Milan history on this day April memorable moments"` → find historic events for the trip
6. Generate the pilgrimage guide with emotional narrative, spot stories, On This Day section, **and match alert if applicable**

## Commands

### generate_pilgrimage

Main command — generates a complete pilgrimage guide for a team.

- `team` (str, required): Team name (e.g., "AC Milan", "Liverpool", "Barcelona")
- `departure_city` (str, optional): User's departure city for travel planning (triggers flyai search)
- `departure_date` (str, optional): Travel date (YYYY-MM-DD) — also used for On This Day matching
- `duration` (str, optional): Trip duration in days (default: 3)

**Pre-check — if no team specified:**

If the user triggers a pilgrimage request without specifying a team (e.g., "I want a football pilgrimage guide", "plan a stadium trip for me"), do NOT guess. Instead:
1. Ask the user: "Which team is your heart's home? Tell me your club and I'll craft the perfect pilgrimage."
2. If the user is unsure or says "recommend one", suggest 3–5 iconic pilgrimage destinations based on popularity and experience richness:
   - 🏟️ **Liverpool** — Anfield, The Kop, Shankly Gates, "You'll Never Walk Alone"
   - 🏟️ **Barcelona** — Camp Nou (under renovation → Spotify Camp Nou), La Masia, Les Corts
   - 🏟️ **AC Milan / Inter Milan** — San Siro, shared cathedral of two rival faiths
   - 🏟️ **Real Madrid** — Santiago Bernabéu, the newly renovated galáctico temple
   - 🏟️ **Bayern Munich** — Allianz Arena, FC Bayern Museum, Säbener Straße
3. Wait for the user to choose before proceeding with the workflow.

**Pre-check — if no departure date specified:**

If the user provides a team but no departure date, recommend the best travel date within the **next 30 days** by combining match schedule and On This Day events:
1. Fetch the team's upcoming fixtures via ESPN API (see [Get team schedule](references/espn-api.md#get-team-schedule-upcoming-fixtures))
2. Filter for **home matches** within the next 30 days — a home match is the #1 factor for choosing a date
3. Search On This Day events for dates around those home matches: `"{team_name} on this day {month} {day}"` — find dates with rich historical significance
4. Recommend the best departure date with reasoning, e.g.:
   - 🔥 "I recommend departing **April 15** — on April 17, {team} has a home match vs {opponent}, AND on April 16, back in {year}, {historic_event}. This gives you the perfect combination of live football and historical resonance!"
   - If no home match in the next 30 days: "No home matches in the next 30 days, but I recommend **{date}** — on this day in {year}, {historic_event}. You can still enjoy the stadium tour and city pilgrimage!"
5. Ask the user to confirm or adjust the recommended date before generating the full guide.

**Workflow:**

> ⚡ **Concurrency strategy**: Steps 1 is sequential (needed by later steps). Steps 2–5 should run **in parallel** to minimize latency. Within each step, all searches should also be parallel.

1. **Discover team info** via ESPN API + Wikipedia (sequential — needed by all later steps):
   - Determine the ESPN league slug (e.g., `ita.1` for Serie A) — see [League Slugs](references/espn-api.md#league-slugs). If unsure, try the most likely league for the team name
   - Search the teams list to find team_id and crest URL — see [Search team](references/espn-api.md#search-team--list-all-teams-in-a-league)
   - ⚠️ The team profile endpoint does NOT return venue info. Stadium name comes from the **schedule endpoint** — see step 2 and [ESPN API notes](references/espn-api.md#get-team-profile)
   - **Search Wikipedia** for team background: Web search `"{team_name} wikipedia history stadium legends honors"` — extract founding year, stadium name, city, honors, legendary players, club motto, and key historical moments from search results. Do NOT use `web_fetch` on Wikipedia (it times out). This is the primary source for storytelling content in the guide
   - Extract: team_id, crest URL, city from ESPN; founding story, legends, stadium history from Wikipedia
   - If team name is ambiguous (e.g., "Inter" could be Inter Milan or Inter Miami), try multiple league slugs or confirm with the user

**── After step 1 completes, launch steps 2–5 in parallel ──**

2. **Check schedule + get stadium info** via ESPN API 🔀 (see [ESPN API Reference](references/espn-api.md) for curl commands and response format):
   - Fetch past results and upcoming fixtures via the schedule endpoints
   - **Extract stadium**: From any home match, get `venue.fullName` and `venue.address.city`
   - **Check for trip matches** (if departure_date and duration provided): Filter events where date falls within trip dates
   - For each match found, extract: opponent name, home/away, kickoff time
   - **If home match found**: 🔥 This is the highlight of the pilgrimage! Adjust the itinerary to make this the "Stadium Day". Use flyai to search match tickets and recommend to user
   - **If away match found**: Still worth noting — user might want to watch at a fan pub
   - **If no match found**: Note it and suggest checking for schedule updates closer to the trip

3. **Research pilgrimage spots with stories** 🔀 — launch 3 web_search calls in one batch (merged queries for speed):
   - web_search: `"{stadium_name} history legends stadium tour"` — stadium origin, iconic moments, tour info
   - web_search: `"{city} {team_name} fan pubs landmarks statues monuments"` — pubs, landmarks, statues and their stories
   - web_search: `"{city} {team_name} football museum shops merchandise"` — museum exhibits, shops, memorabilia
   - ⚠️ Do NOT search for ticket prices, flight prices, or hotel prices via Web Search. Use **flyai** for all ticket/pricing queries
   - After spots are identified, use flyai to search attraction tickets (stadium tour, museum, etc.) and include ticket info in the guide

4. **Research On This Day events** 🔀 — **only 1 web_search call** for the entire trip:
   - web_search: `"{team_name} history on this day {month} memorable moments"` (use the departure month)
   - From the search results, pick events whose dates fall within the trip dates. Assign each matching event to the corresponding trip day
   - If no events match the trip dates, that's fine — simply omit On This Day sections from the guide
   - **⚠️ Anti-fabrication rules:**
     - **ONLY use events that appear in Web Search results** — never generate events from memory or training data
     - If no events found for a specific day, **skip that day entirely** — do NOT output any On This Day section for that day. No placeholder text, no filler quotes. Simply omit
     - Prefer well-documented events (league matches, cup finals, official transfers) over vague anecdotes

5. **Ticket search** via flyai 🔀:
   - **Match tickets** (if home match found in step 2): `flyai search-tickets --event "{team_name} vs {opponent}" --date "{match_date}" --city "{city}"`
   - **Attraction tickets**: `flyai search-tickets --attraction "{stadium_name} tour" --date "{date}" --city "{city}"` (stadium tour, museum, etc.)

**── After all parallel steps complete, generate the guide ──**

6. **Generate the guide** with emotional narrative structure (see Guide Structure reference)

7. **Ask about flights & hotels** — after the guide is generated, ask the user:
   - "Need me to search for flights and hotels? Just tell me your departure city and I'll find the best options for you! ✈️🏨"
   - If user says yes and provides departure city, use flyai:
     - `flyai search-flight --origin "{departure_city}" --destination "{city}" --dep-date "{date}"`
     - `flyai search-hotels --city "{city}" --check-in "{date}" --nights {duration}`
   - If user already provided departure_city in the initial request, still ask to confirm before searching

### get_stadium_info

Get detailed stadium information for pilgrimage planning.

- `team` (str, required): Team name

Returns: stadium name, capacity, address, tour availability, ticket prices, visiting hours, **plus the stadium's origin story and legendary moments**.

### get_pilgrimage_spots

Get a curated list of pilgrimage spots for a team's city. **Each spot includes a backstory.**

- `team` (str, required): Team name
- `spot_type` (str, optional): Filter by type — "museum", "pub", "landmark", "shop", "all"

Returns: list of spots with name, description, address, significance, **story** (historical background, legendary events, famous anecdotes tied to this spot).

### get_on_this_day

Get historic football events that match the user's trip dates.

- `team` (str, required): Team name
- `departure_date` (str, required): Trip start date (YYYY-MM-DD)
- `duration` (int, optional): Trip duration in days (default: 3)

**Workflow:**
1. Web search `"{team_name} history on this day {month} memorable moments"` (use the departure month) — **only 1 search**
2. From results, filter events whose calendar date (month + day) falls within the trip dates
3. Assign each matching event to the corresponding trip day
4. For days with no matching event, simply omit — do NOT invent an event

**⚠️ Critical**: Every event in the output MUST come from a Web Search result. If you cannot point to a specific search result that contains the event, do not include it.

### get_trip_matches

Check if the team has any matches during the user's trip dates.

- `team` (str, required): Team name
- `departure_date` (str, required): Trip start date (YYYY-MM-DD)
- `duration` (int, optional): Trip duration in days (default: 3)

**Workflow:**
1. Determine ESPN league slug and team_id (see [Finding a Team](references/espn-api.md#finding-a-team))
2. Fetch past results and upcoming fixtures via schedule endpoints (see [ESPN API Reference](references/espn-api.md))
3. Merge both results, filter events where date falls within [departure_date, departure_date + duration - 1]
4. For each match found, extract: home/away, opponent, kickoff time, status
5. Return matches sorted by date, with home matches highlighted

**Output guidance:**
- 🔥 **Home match**: "Lucky you! During your trip, {team} will face {opponent} at {stadium}!" + flyai ticket search results
- ⚽ **Away match**: "During your trip, {team} has an away match (vs {opponent}) — you can watch the live broadcast at a local fan pub!"
- 😢 **No match**: "Match schedule during your trip — please check the team's official website before departure"

### get_travel_plan

Generate travel plan (flights + hotels) for the pilgrimage.

- `team` (str, required): Team name
- `departure_city` (str, required): Departure city
- `departure_date` (str, required): Travel date (YYYY-MM-DD)
- `nights` (int, optional): Number of nights (default: 3)

## Team Crest (Logo)

The team's official crest is obtained from ESPN API responses:

1. **Primary source** — ESPN teams list or team profile → `team.logos[0].href` returns a URL like `https://a.espncdn.com/i/teamlogos/soccer/500/{team_id}.png`
2. **Direct construction** — If you know the team_id, the crest URL follows a predictable pattern: `https://a.espncdn.com/i/teamlogos/soccer/500/{team_id}.png`
3. **Fallback** — If crest URL is missing, search `"{team_name} official logo png"` via Web Search

- **Usage**: Display in the guide header and anywhere the team identity is shown
- **Rendering**: Use `![{team_name} crest]({crest_url})` in Markdown
- **Fallback**: If crest URL is missing, use a text-based team badge with team colors

## Guide Structure (Emotional Arc)

See [references/guide-structure.md](references/guide-structure.md) for the full 5-phase narrative arc (Pre-departure → Arrival → Stadium Day → Deep Experience → Departure), spot storytelling format, match day itinerary, and optional travel & stay section.

## Data Sources

| Source | What it provides |
|--------|-----------------|
| ESPN API | Team ID, name, crest URL, match schedule, stadium info (from schedule endpoint). See [ESPN API Reference](references/espn-api.md) |
| Wikipedia (via Web Search) | Team history, founding story, legends, honors, stadium background |
| Web Search | Stadium tours, museums, fan pubs, landmarks, **spot backstories**, **On This Day events** |
| flyai | Flights, hotels, **and match tickets** (when departure city provided or user asks for pricing) |

## Examples

See [references/examples.md](references/examples.md) for 3 complete examples: basic pilgrimage, pilgrimage with travel + On This Day + match detection, and standalone On This Day query.

## Error Handling

- **If no team specified**: Ask the user which team they support. If they're unsure, recommend 3–5 iconic pilgrimage destinations and wait for their choice. Never guess or pick a team on their behalf
- If ESPN API returns no matching team or the team name is ambiguous (e.g., "Inter" could be Inter Milan or Inter Miami), try multiple league slugs or ask user to clarify
- If stadium tour info is unavailable, note it and suggest checking the official website
- If flyai returns no flights, suggest alternative dates or nearby airports
- If no On This Day events found for a specific day, try broadening the search (league-level, city-level). If still nothing, **omit the On This Day section for that day entirely** — no placeholder text, no filler. **Never fabricate events to fill gaps**
- If crest URL is missing, use a text-based badge with team colors as fallback
- If ESPN API returns an error or is unreachable, fall back to Web Search for team info and skip match detection with a note to the user
- Never surface raw errors to the user — provide clean, human-readable messages

## Common Mistakes

- Don't confuse team names — always confirm with search results
- Don't hallucinate stadium tour details — only use verified info from search
- Don't skip the emotional narrative — this is not a dry travel guide, it's a pilgrimage
- **Don't list spots without stories** — every spot must have its backstory. If you can't find a story, search harder
- **Don't fabricate On This Day events** — this is the #1 risk of this skill. Rules:
  - Every event MUST come from a Web Search result — never from LLM memory or training data
  - If search returns nothing for a day, **omit the On This Day section for that day entirely** — a gap is better than a lie
  - Don't "improve" search results — if the search says "Milan beat Juventus 2-1", don't change the score or add details not in the source
  - Prefer official match records (scores, dates, competitions) over vague anecdotes that can't be verified
  - When in doubt, do a verification search: `"{team} {opponent} {date} {year}"` to confirm the event
- **Don't only search one day for On This Day** — search **every day** of the trip (departure_date through departure_date + duration - 1), so each Phase has its own historic event
- **Don't forget the team crest** — it should appear in the guide header
- **Don't forget to check for matches** — when departure_date and duration are provided, always query ESPN schedule API to check for matches during the trip. A home match is the ultimate pilgrimage moment
- **Don't assume match day = tour day** — stadium tours are usually closed on match days. If there's a match, schedule the tour for the day before
