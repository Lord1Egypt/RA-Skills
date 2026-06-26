---
name: china-travel-planner
description: Plan and optimize travel within China using flyai / Fliggy search capabilities plus public metro-network data when needed. Use when the user wants a domestic China trip plan, weekend getaway, city itinerary, family trip, holiday route, hotel recommendation, flight comparison, attraction shortlist, budget-based plan, or a practical travel guide that combines transportation, hotel, POI, and day-by-day scheduling for destinations inside mainland China. Also use when the trip has transit constraints such as covering every metro line at least once, choosing hotels by metro convenience, anchoring plans around a fixed hotel, or mixing city travel with nearby side trips.
---

# China Travel Planner

Plan practical domestic trips in China by combining itinerary design with real-time-ish search from `flyai`.

This skill is for **planning-first** travel help. Use it to turn a vague request like “清明去杭州玩两天怎么安排” into a usable plan with destination logic, transport suggestions, hotel area recommendations, attraction picks, and a day-by-day itinerary.

## Core workflow

1. **Clarify the trip frame**
   - Extract or ask for: departure city, destination, travel dates, duration, traveler type, budget, pace, and priorities.
   - Also detect hard constraints such as:
     - fixed hotel already booked
     - must-visit cities
     - every metro line must be ridden at least once
     - hotel must be close to a given metro line / station / interchange
   - If the user is vague, make reasonable assumptions and label them clearly.

2. **Pick the planning mode**
   - **Light plan**: quick destination ideas or a rough 1-3 day outline.
   - **Standard plan**: transport + hotel area + POIs + daily itinerary.
   - **Comparison plan**: compare 2-3 destinations, hotel zones, or transport options.
   - **Booking-oriented plan**: prioritize flight/hotel/ticket search and provide booking links.
   - **Transit-constrained plan**: optimize around metro-line coverage, fixed hotel anchors, or nearby side trips.

3. **Choose the right data source mix**
   - Use `flyai fliggy-fast-search` for broad natural-language discovery.
   - Use `flyai search-flight` for flight comparison when flights matter.
   - Use `flyai search-hotels` for hotel options near a city or POI.
   - Use `flyai search-poi` for attraction candidates inside the target city.
   - Use public metro data when the plan depends on line coverage, station lists, or metro-aware hotel selection.

4. **Turn results into a China-friendly plan**
   - Prefer practical advice over generic marketing copy.
   - For domestic travel, explicitly cover:
     - how to arrive: plane / high-speed rail / city transfer logic
     - where to stay: district / landmark / transport convenience
     - must-see vs optional POIs
     - crowd avoidance / holiday pressure / realistic pacing
     - budget bands
     - if transit constraints exist: which lines are covered on which days

5. **Produce a final answer that is actually usable**
   - Start with the recommendation.
   - Then give the itinerary and concrete options.
   - Keep it readable; do not dump raw JSON unless the user explicitly wants structured output.

6. **When the trip may become a web page or reusable artifact, also prepare structured data**
   - Prefer a stable JSON structure that can populate reusable cards and sections.
   - Align with a page-data model such as: `meta`, `hero`, `stats`, `hotels`, `metroCoverage`, `days`, `sideTrips`, `attractions`, `tips`.
   - Keep destination-specific wording in data values, not in page/template structure.
## Planning heuristics for domestic China trips

### Trip type presets

#### 1. Weekend / short break
- Default to **2D1N** or **3D2N**.
- Prefer compact cities or one core area.
- Avoid stuffing too many attractions into one day.
- Optimize for low transfer friction.

#### 2. Family trip
- Prefer fewer hotel changes.
- Reduce aggressive early departures.
- Prioritize stable meal / restroom / stroller / queue conditions when relevant.
- Recommend attractions with mixed-age tolerance.

#### 3. Holiday trip
- Warn about crowding, traffic, and price spikes.
- Suggest early/late entry windows and alternative districts.
- Offer a **mainstream plan** plus a **crowd-avoidance backup**.

#### 4. Budget trip
- Prioritize rail over flight where reasonable.
- Prefer transport-convenient hotel areas over luxury scenic isolation.
- Separate “must spend” from “optional upgrade”.

#### 5. Relaxed trip
- Limit major POIs per day.
- Add café / night walk / slow sightseeing blocks.
- Favor one scenic area plus one food/urban area per day.

## How to use flyai commands

### A. Broad discovery
Use when the user is still fuzzy, such as:
- “杭州三天怎么玩”
- “五一国内去哪儿适合亲子”
- “苏州周末度假住哪方便”

Command pattern:

```bash
flyai fliggy-fast-search --query "杭州三日游"
```

Use broad search first to collect candidate products, local experiences, hotel packages, or bundled travel ideas.

### B. Flight comparison
Use when the user is traveling farther or explicitly asks about flights.

Command pattern:

```bash
flyai search-flight --origin "北京" --destination "杭州" --dep-date 2026-04-04 --sort-type 3
```

Prefer sorting by:
- `3` for lowest price
- `8` for direct-priority
- `4` for shortest duration

For domestic planning, mention whether high-speed rail may be more sensible if flight transfer friction is high.

### C. Hotel search
Use when deciding where to stay, especially around scenic areas or transit hubs.

Command pattern:

```bash
flyai search-hotels --dest-name "杭州" --poi-name "西湖" --check-in-date 2026-04-04 --check-out-date 2026-04-06 --sort rate_desc
```

Hotel guidance:
- If the user values convenience, recommend by **area first**, hotel second.
- Explain why the area works: near metro / scenic area / food street / station.
- When budget is unclear, give 3 price bands if possible.

### D. POI search
Use when building the daily route.

Command pattern:

```bash
flyai search-poi --city-name "杭州" --keyword "西湖"
```

Group POIs into:
- must-see
- optional swap-ins
- niche / backup choices

## Output rules

- Always return a **curated plan**, not raw command output.
- If flyai returns image URLs, place the image line before the booking link.
- If flyai returns booking/detail URLs, include them when helpful.
- Mention that recommendations are **based on fly.ai / Fliggy results** when using those results.
- In Feishu chats, prefer bullets over markdown tables unless the comparison truly benefits from a table.

## Recommended answer structure

### Fast recommendation
- Who this plan is for
- Why this destination / route fits
- Budget feel: economical / moderate / comfortable

### Trip snapshot
- Duration
- Best departure method
- Suggested stay area
- Top highlights

### Day-by-day itinerary
For each day include:
- morning
- lunch suggestion area
- afternoon
- evening
- pacing note / transfer note

### Hotel suggestion
- best area to stay
- 2-3 hotel choices if available
- who each option suits

### Transport suggestion
- plane vs rail judgment if relevant
- arrival/departure advice
- local transport note

### Notes
- booking tips
- crowd avoidance
- weather / season / holiday reminders if obvious from context

## Structured output mode for reusable web pages

When the user wants a web page, reusable framework, shareable itinerary page, or future automation, also organize the content into stable sections.

Recommended top-level keys:
- `meta`
- `hero`
- `stats`
- `hotels`
- `metroCoverage`
- `days`
- `sideTrips`
- `attractions`
- `tips`

### What to produce

Whenever possible, produce two synchronized layers:

1. **Readable itinerary summary**
2. **Structured trip data**

The readable summary should be easy to read in chat.
The structured layer should be easy to feed into `travel-page-framework`.

### Card conventions

#### Hotel cards
Use fields such as:
- `phase`
- `name`
- `dateRange`
- `station`
- `status`
- `price`
- `distanceToMetro`
- `image`
- `highlights`

#### Day cards
Use fields such as:
- `day`
- `date`
- `theme`
- `city`
- `hotel`
- `metroLines`
- `segments.morning`
- `segments.afternoon`
- `segments.evening`
- `note`

#### Attraction cards
Use fields such as:
- `name`
- `city`
- `type`
- `image`
- `description`
- `bestFor`

Keep structured card text concise and web-friendly.

### Working rule

If the user explicitly wants a web page, page framework, reusable travel card layout, or future rendering, read `references/structured-output-mode.md` and organize the plan so the text layer and structured layer remain consistent.
## Page generation pipeline

Use this when the user wants a **shareable web page**, standalone HTML itinerary, or asks for a "travel page" / "行程页面". The pipeline turns a travel plan into a static HTML page powered by the `travel-page-framework`.

### Flow

```
plan (chat) → structured trip-data.json → tpf-generate → tpf validate → tpf build → dist/index.html
```

### Step-by-step

1. **Plan the trip** using the normal planning workflow above.
2. **Generate structured JSON** from a natural-language prompt:

```bash
python3 skills/china-travel-planner/page-generator/scripts/tpf-generate.py \
  "杭州3天2晚，西湖+灵隐寺，住湖滨，预算2000" \
  --with-metro --with-images --pretty \
  -o data/trip-data.json
```

Options:
- `--with-metro`: auto-fetch metro/subway data for the city
- `--with-images`: auto-search Wikimedia Commons for attraction images
- `--from-file prompt.txt`: read prompt from a file instead of CLI arg
- `--output` / `-o`: output path (default: `trip-data.json`)
- `--pretty`: pretty-print the JSON

3. **Review and refine** the generated `trip-data.json`. The auto-generated skeleton is a starting point — fill in richer descriptions, swap placeholder images, and adjust day-by-day segments as needed. Follow the content guidelines in `page-generator/schema/trip-content-guidelines.md`.

4. **Validate** the data against the schema:

```bash
cd <project-dir>   # must contain data/trip-data.json
python3 skills/china-travel-planner/page-generator/scripts/tpf-cli.py validate
```

5. **Build** the static site:

```bash
python3 skills/china-travel-planner/page-generator/scripts/tpf-cli.py build
```

This produces `dist/index.html` + `dist/trip-data.json`. Preview with:

```bash
cd dist && python3 -m http.server 8080
```

6. **(Optional) Deploy** to GitHub Pages:

```bash
python3 skills/china-travel-planner/page-generator/scripts/tpf-cli.py deploy --to gh-pages
```

### Schema and content guidelines

- JSON schema: `page-generator/schema/trip-schema.json`
- Content writing guide: `page-generator/schema/trip-content-guidelines.md`
- Required top-level keys: `meta`, `hero`, `stats`, `hotels`, `metroCoverage`, `days`, `sideTrips`, `attractions`, `tips`

### When to use tpf-generate vs manual JSON

- **tpf-generate**: quick scaffolding from a one-liner prompt. Good for getting the structure right fast.
- **Manual JSON**: when you already have a detailed plan from the chat workflow and want precise control over every field.

In practice, generate the skeleton first, then hand-edit or have the agent refine it.

## When information is missing

If critical info is missing, ask at most the smallest set of questions needed. Prioritize:
1. 出发地
2. 日期 / 天数
3. 预算
4. 几个人、什么类型（情侣 / 亲子 / 家庭 / 独自）

If the user just wants a quick answer, do not block on questions. State assumptions and give a draft plan.

## Scripts

### `scripts/fetch_subway_data.py`
Use this script when the plan depends on metro / subway line coverage or station lists.

Examples:

```bash
python3 skills/china-travel-planner/scripts/fetch_subway_data.py 长沙 --pretty
python3 skills/china-travel-planner/scripts/fetch_subway_data.py changsha --stations-only --pretty
python3 skills/china-travel-planner/scripts/fetch_subway_data.py 湘潭 --pretty
```

Behavior:
- reads the AMap subway city index
- resolves the city by Chinese name / pinyin / city id
- fetches line + station data
- outputs JSON for downstream planning

Use the result to:
- count how many lines a city has
- list line names
- see station lists for each line
- support "every line must be ridden once" planning

### `scripts/metro_hotel_match.py`
Use this script to rank hotels by metro convenience.

Examples:

```bash
python3 skills/china-travel-planner/scripts/metro_hotel_match.py \
  --subway changsha-subway.json \
  --hotels hotels.json \
  --target-line "1号线" \
  --target-station "黄土岭" \
  --pretty
```

Behavior:
- reads subway JSON and hotel JSON
- scores hotels by target station / line mentions plus transit-convenience hints
- returns a ranked list with reasons

### `scripts/coverage_plan_notes.py`
Use this script to generate lightweight notes for line-coverage planning.

Examples:

```bash
python3 skills/china-travel-planner/scripts/coverage_plan_notes.py \
  --subway changsha-subway.json \
  --hotel-station "黄土岭" \
  --pretty
```

Behavior:
- summarizes each line
- notes whether the hotel anchor lies on that line
- gives rough planning hints for route design

### `page-generator/scripts/wikimedia_image_search.py`
Use this script to find free-license images from Wikimedia Commons for attractions, landmarks, or city scenes. Use it when populating `image` fields in structured trip data.

**Keyword search:**

```bash
python3 skills/china-travel-planner/page-generator/scripts/wikimedia_image_search.py "橘子洲 长沙" --limit 3 --pretty
```

**Category browse:**

```bash
python3 skills/china-travel-planner/page-generator/scripts/wikimedia_image_search.py --category "Orange Isle" --limit 5 --pretty
```

**Batch mode** (read a JSON file with multiple search specs):

```bash
python3 skills/china-travel-planner/page-generator/scripts/wikimedia_image_search.py \
  --batch landmarks.json --output results.json --pretty
```

Batch input format (`landmarks.json`):
```json
[
  {"name": "五一广场", "query": "Changsha Wuyi Square"},
  {"name": "橘子洲", "category": "Orange Isle"},
  {"name": "岳阳楼", "query": "Yueyang Tower Hunan"}
]
```

Options:
- `--limit` / `-n`: number of results (default: 5)
- `--width` / `-w`: thumbnail width in pixels (default: 1200)
- `--output` / `-o`: write results to file instead of stdout
- `--pretty`: pretty-print JSON

Output: JSON array of `{title, url, thumbUrl, width, height, license, description}`. All images carry free licenses (CC / Public Domain).

## References

Read these only when needed:
- `../flyai/references/fliggy-fast-search.md` for broad natural-language search
- `../flyai/references/search-flight.md` for flight parameters and output fields
- `../flyai/references/search-hotels.md` for hotel filters and fields
- `../flyai/references/search-poi.md` for attraction filters and fields
- `references/subway-aware-planning.md` for metro-line coverage, fixed-hotel anchors, and metro-aware hotel selection
- `references/domestic-planning-prompts.md` for common domestic trip phrasing and default itinerary patterns
- `references/structured-output-mode.md` for producing reusable structured trip data alongside readable itinerary text
- `page-generator/schema/trip-content-guidelines.md` for reusable travel-page content structure and card-writing conventions
