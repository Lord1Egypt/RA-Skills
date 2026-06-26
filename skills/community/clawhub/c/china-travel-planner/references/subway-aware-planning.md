# Subway-aware planning for domestic trips

Use this reference when the trip has **rail transit coverage constraints** or **hotel selection needs to consider metro access**.

## Supported planning ideas

### 1. Line coverage goal
Interpret requests like:
- 把长沙所有地铁线都坐到
- 每条线都要坐过
- 不要求每站打卡，只要线路覆盖

as:
- Each metro line must be ridden **at least once**.
- Do **not** assume every station must be visited unless the user explicitly says so.

### 2. Fixed hotel anchor
Interpret requests like:
- 酒店已经订在某站附近
- 住在黄土岭站附近

as:
- The hotel is a routing anchor.
- Prefer plans that start/end around the hotel area on most days.
- Evaluate convenience by transfer count and last-mile friction, not only geographic distance.

### 3. Metro-convenience hotel selection
If the user asks to choose a hotel by metro convenience, score candidates by:
1. near target line or target station
2. near interchange stations
3. easy access to railway station / airport / cross-city transit
4. low detour cost for the planned itinerary

## Data source strategy

### A. Metro / station network
Use AMap subway data when available.

Pattern:

```text
http://map.amap.com/service/subway?srhdata=<CITY_ID>_drw_<cityname>.json
```

Examples:
- Changsha: `4301_drw_changsha.json`
- Xiangtan: `4303_drw_xiangtan.json`

Expected structure:
- `l`: line list
- each line contains:
  - `ln`: line name
  - `la`: branch label if any
  - `st`: station list

### B. Travel products and hotel options
Use `flyai` for:
- hotel search
- attraction search
- broad travel discovery
- flight search when relevant

## Planning rules for metro-coverage trips

### Rule 1: Cover lines, not stations
When the user says all lines must be covered, optimize for:
- minimum unnecessary backtracking
- combining line coverage with actual sightseeing
- combining outer lines with day-trip direction when possible

### Rule 2: Treat short special lines separately
Airport / suburban / branch lines may be poor sightseeing matches.
Handle them as:
- transport mission segments
- arrival/departure-day coverage opportunities
- standalone short loops when needed

### Rule 3: Combine cross-city travel with network edges
If another city is reachable by rail transit, try to combine:
- line coverage requirement
- outbound day trip
- station-area sightseeing

### Rule 4: Hotel advice should be routing-aware
Do not just say "close to metro".
Explain:
- which line(s) the hotel benefits from
- whether it is near an interchange
- whether it helps day trips and return-at-night convenience

## Recommended output for transit-constrained trips

### Summary
- trip goal
- line coverage goal
- fixed anchors (hotel / booked train / must-visit cities)

### Network strategy
- list all lines that must be covered
- explain which day covers which lines
- identify any special handling line (airport / suburban / branch)

### Day plans
For each day include:
- start point
- which line(s) are being covered
- main attractions or city goal
- return logic

### Hotel / area assessment
If hotel is fixed, assess:
- nearest useful line
- interchange convenience
- late return convenience
- suitability for cross-city movement

If choosing hotels, recommend areas first, then hotels.
