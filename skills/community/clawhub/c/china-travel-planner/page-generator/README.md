# travel-page-framework

A reusable travel itinerary web-page framework.

## Goal

Separate **travel content data** from **page presentation** so future destination pages can reuse:

- the same JSON schema
- the same card/component structure
- the same Tailwind page shell

## Structure

```text
travel-page-framework/
├── schema/
│   ├── trip-schema.json
│   └── trip-content-guidelines.md
├── templates/
│   └── trip-page-tailwind.html
└── examples/
    └── changsha-2026-03-31/
        ├── index.html
        └── data/trip-data.json
```

## Core idea

Future trip planners should output structured data first, then render UI from that data.

Recommended top-level sections:

- meta
- hero
- stats
- hotels
- metroCoverage
- days
- sideTrips
- attractions
- tips

## Quick Start

### 1. Open the example page locally

If you are already inside the repository root:

```bash
python3 -m http.server 8766 --directory examples/changsha-2026-03-31
```

Then open:

```text
http://127.0.0.1:8766
```

### 2. Edit trip data

Update:

```text
examples/changsha-2026-03-31/data/trip-data.json
```

Keep it aligned with:

```text
schema/trip-schema.json
```

### 3. Reuse for a new destination

Recommended flow:

1. copy `examples/changsha-2026-03-31/` to a new example folder
2. replace `data/trip-data.json` with the new trip data
3. keep the layout stable unless the schema evolves intentionally

## Card model examples

### Hotel card
- phase
- name
- dateRange
- station
- status
- price
- distanceToMetro
- image
- highlights[]

### Day plan card
- day
- date
- theme
- city
- hotel
- metroLines[]
- segments.morning[]
- segments.afternoon[]
- segments.evening[]
- note

### Attraction card
- name
- city
- type
- image
- description
- bestFor[]

## Notes

- Destination-specific wording belongs in JSON data files
- Presentation logic belongs in the page template
- Shared schema belongs in `schema/`
- Examples should be real trips, not abstract placeholders
- `trip-content-guidelines.md` defines how travel copy should be normalized into reusable card data
- Example pages should remain schema-driven so future destinations can swap data without rewriting layout
