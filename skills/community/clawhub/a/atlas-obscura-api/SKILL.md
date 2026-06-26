---
name: atlas-obscura-api
description: Query Atlas Obscura places for weird/obscure location inspiration. Use when you need nearby curiosities by coordinates, place lookup by ID, or global place coordinates for creative prompt spice and worldbuilding.
---

Use this skill to pull Atlas Obscura data through the `atlas-obscura-api` JavaScript library.

## Setup

From this skill directory:

- `npm install`

This installs the `atlas-obscura-api` dependency used by the helper script.

## Fast path commands

Run from `skills/atlas-obscura-api/`.

- Nearby search by coordinates:
  - `node scripts/atlas_obscura.js search --lat 44.4759 --lng -73.2121 --limit 5`
- Place details by ID (short):
  - `node scripts/atlas_obscura.js place-short --id 4654`
- Place details by ID (full):
  - `node scripts/atlas_obscura.js place-full --id 4654`
- Raw place coordinate index:
  - `node scripts/atlas_obscura.js places-all --limit 10`

## Output usage guidance

When sharing results:

1. Prefer 1–3 top places unless user asks for more.
2. Include: title, location, short subtitle/description, and canonical URL.
3. For creative workflows, extract one “spice line” (e.g., architectural mood, local oddity, folklore angle) for prompt context.

## Troubleshooting

- `ERR_MODULE_NOT_FOUND` for `atlas-obscura-api`: run `npm install` in this skill directory.
- Empty search: broaden location radius by changing coordinates slightly or run a different query seed.
- Site/library drift: return partial data and clearly note field gaps.
