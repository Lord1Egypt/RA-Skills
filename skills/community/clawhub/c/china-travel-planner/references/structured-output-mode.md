# Structured Output Mode

Use this reference when the travel plan is expected to feed a reusable web page, shareable itinerary page, or downstream automation.

## Goal

Produce two synchronized outputs:

1. **Readable itinerary summary** for chat
2. **Structured trip data** aligned with the travel-page-framework schema

The readable summary is for humans.
The structured trip data is for rendering and reuse.

## Recommended top-level keys

Use these sections when possible:

- `meta`
- `hero`
- `stats`
- `hotels`
- `metroCoverage`
- `days`
- `sideTrips`
- `attractions`
- `tips`

## Required mindset

### Do
- keep section names stable
- keep field meanings stable
- put destination-specific details into data values
- prefer concise card text over long essay paragraphs
- make sure the human-readable plan and structured data do not contradict each other

### Don't
- invent ad-hoc top-level sections unless truly needed
- put raw HTML into data fields
- mix CSS classes into structured data
- produce unbounded freeform blobs when card fields can express the same thing

## Section guidance

### meta
Use for document/page identity.

Fields:
- `title`
- `subtitle`
- `description`

### hero
Use for first-screen messaging.

Fields:
- `title`
- `subtitle`
- `dateRange`
- `tags`
- `summary`
- optional `heroImage`

### stats
Use short dashboard values.
Example:
- 出发
- 返程
- 时长
- 已定酒店
- 推荐后半程
- 轨交目标

### hotels
Each hotel card should answer:
- which phase it belongs to
- why it is included
- what transport advantage it has

Recommended fields:
- `phase`
- `name`
- `dateRange`
- `station`
- `status`
- `price`
- `distanceToMetro`
- `image`
- `highlights`

### metroCoverage
Use for transit constraints and line allocations.

Recommended fields:
- `goal`
- `lines[]`
  - `name`
  - `day`
  - `status`

### days
Each day should be operationally useful.

Recommended fields:
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

### sideTrips
Use for out-of-core-city or nearby city modules.

Recommended fields:
- `name`
- `date`
- `role`
- `description`
- optional `image`

### attractions
Use short, reusable attraction cards.

Recommended fields:
- `name`
- `city`
- `type`
- `image`
- `description`
- `bestFor`

### tips
Use concise operational reminders.

## Output workflow

When generating a plan in structured mode:

1. Identify constraints
2. Draft itinerary logic
3. Draft hotel logic
4. Draft transit/metro logic
5. Build card-friendly content blocks
6. Assemble the readable summary
7. Assemble the structured sections with the same facts

## Best practice

If the user asks for both a plan and a web page, think in this order:
- produce the trip logic first
- normalize that logic into structured card data
- let the page render from the structured layer
