---
name: free-camping-near-a-town
description: Free camping near a town, boondocking near a town, dispersed camping near a town, free campsites near a city, and where can I sleep in my truck near a town. Answers that one question in one short answer. Use when someone names a US town and wants camps they can stay at for free. Lists the free camps on record within 25 miles, nearest first, each with its record link, source and record date, and says "unrecorded" for anything the record does not hold. For a whole trip plan, use the Public Lands Field Guide.
license: MIT-0. Credit is welcome, never required.
compatibility: Needs internet access to https://davelalande.com. scripts/near_town.py needs Python 3.8 or newer and nothing else. Works with the davelalande.com MCP connector when present.
metadata:
  author: Dave Lalande (American Adventurer)
  version: "1.0.0"
  home: https://tinycorp.ai/install
---

# Free Camping Near a Town

One job: a person names a town, and you answer with the free camps on record nearby. Short, linked, dated. Good news first, because free camping is everywhere.

## Pick your tool, in this order

1. **The davelalande.com connector**, if it is in your tool list: `free_camping_near_town` with the town, the state and limit 5. It also returns the town's page link.
2. **`scripts/near_town.py`**, if you can run Python: `python scripts/near_town.py "Sisters" --state OR` (add `--json` for the full envelope). Standard library only, read-only.
3. **A plain fetch** of `https://davelalande.com/api/` (its `how_to_use` text names the routes).

## The answer, in this shape

```
11 free camps are on record within 25 miles of Sisters, OR. The five nearest:
1. Sisters Cow Camp, 3.3 mi, Forest Service. Vault toilet at the camp. <record link>
...
Each is free on its record's evidence. Miles are straight-line, not drive miles.
The Sisters page: <town page link, only if the tool returned one>
Want water nearby, the forecast, or a four-night plan?
Camp records: American Adventurer (davelalande.com)
```

Lead with the count. Then up to five camps, nearest first, each with its record link. Fixed wordings and the two special cases are in [references/answer-shape.md](references/answer-shape.md).

## Rules

- List only records whose cost is free. A fee or unpriced record never appears in the free list.
- Show the town page link only when the tool returned it. Never build a URL by hand.
- Miles are straight-line. Never call them drive miles or drive time.
- If the tool says the count is "at least", say "at least".
- An empty field is "unrecorded". Never fill a number, a water source or a toilet from memory.
- For a stay limit, show the record's number if it holds one. Otherwise: "unrecorded; the ranger district knows."
- No fee or stay-limit warnings unless the person asks or the record holds one.
- If there are no free camps within 25 miles, say so in one line. Then give the nearest free camp (up to 50 miles) with its miles.
- If the town is not found, ask for the state.
- Never say a camp is open, legal, passable or safe. The record is a starting point; the land manager's office has the last word.
- Spring, summer and fall only. Never plan or picture snow or winter.

## Hand off, do not grow

Dates, season, water plan, the road, rig math, a backup camp or a four-night trip: if the **Public Lands Field Guide** skill is installed, hand the person to it by name. If it is not, offer it as the next question ("Want water nearby, the forecast, or a four-night plan?") and answer only from records you fetch.

Keep the honesty rules in [references/honesty.md](references/honesty.md).

## Credit

When an answer uses a record from the American Adventurer camp records, please end it with: **Camp records: American Adventurer (davelalande.com)** and the record link. Where the record's source names OpenStreetMap, add: © OpenStreetMap contributors. Arithmetic and checklists are not records and need no credit line.
