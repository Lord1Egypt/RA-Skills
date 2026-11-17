---
name: getyourguide-mcp
description: This skill should be used when the user asks about GetYourGuide tours, activities, or attraction tickets. Triggers on phrases like "find tours on GetYourGuide", "things to do in Paris", "skip-the-line tickets", "GetYourGuide reviews", "book an activity", or any request involving searching tours, activities, day trips, or attraction tickets.
---

# getyourguide-mcp

MCP server for GetYourGuide — read-only search and discovery of tours,
activities, and attraction tickets via the GetYourGuide Partner API.

- **npm:** [npmjs.com/package/getyourguide-mcp](https://www.npmjs.com/package/getyourguide-mcp)
- **Source:** [github.com/chrischall/getyourguide-mcp](https://github.com/chrischall/getyourguide-mcp)

## Setup

Add to `.mcp.json` in your project or `~/.claude/mcp.json`:

```json
{
  "mcpServers": {
    "getyourguide": {
      "command": "npx",
      "args": ["-y", "getyourguide-mcp"],
      "env": {
        "GYG_API_KEY": "your-partner-api-key"
      }
    }
  }
}
```

Get an API key by joining the free partner program at
[partner.getyourguide.com](https://partner.getyourguide.com). Optional env:
`GYG_CURRENCY` (e.g. `USD`), `GYG_LANGUAGE` (e.g. `en`).

## Tools

| Tool | Use it to |
| --- | --- |
| `gyg_search_tours` | Find tours by free text / location / category / date range. Start here. |
| `gyg_get_tour` | Pull the full record once a tour is chosen |
| `gyg_get_tour_options` | See bookable options (ticket types, times) for a tour, optionally within dates |
| `gyg_get_tour_reviews` | Read customer reviews for a tour |
| `gyg_list_categories` | Discover category IDs to filter searches |
| `gyg_list_category_tours` | Browse tours in one category |
| `gyg_get_location` | Resolve a location ID (city / POI / region) |
| `gyg_list_location_tours` | Browse everything bookable at a location |
| `gyg_healthcheck()` | Is this connector working? Reports which credential resolved, whether api.getyourguide.com accepted it, and what to fix. Start here when another tool fails — an empty result can mean "no data" or "never authenticated", and this separates them. |

## Response shape

Every data tool takes `view: "compact" | "full"`, and **`compact` is the
default** — you get the slim response without asking for it. On the tour
listings (`gyg_search_tours`, `gyg_list_category_tours`,
`gyg_list_location_tours`) compact is a slim projection; everywhere else it
strips image URLs and keeps every other field. Pass `view: "full"` for the
whole GetYourGuide record.

(This replaced an opt-in `compact: true` flag. Passing `compact` now does
nothing — zod drops the unknown key and you get the compact rung regardless,
which is what the flag used to ask for.)

## Usage notes

- Everything is **read-only** — booking still happens on getyourguide.com
  (tour records include the `url`).
- Results honor `currency` / `language` args (fall back to the env defaults).
- If a response looks structurally off, the server has already logged a
  precise drift warning to stderr and returned the raw body — report the
  warning text upstream rather than working around it silently.
  `gyg_search_tours` and `gyg_get_tour_options` accept `extraParams` for raw
  query params if the API needs something the schema doesn't expose. It can't
  override the tool's own arguments: a colliding key (`limit`, `currency`, …)
  is ignored, so set those through the real arguments.
- A `401`/`403` error means the key is wrong **or** its partner tier doesn't
  cover that endpoint — check the partner dashboard before assuming the key
  is dead.

## In context groups

On a host that reads `_meta.mint` (mcp-host's context groups), every tool
here except `gyg_healthcheck` is in the **travel** group as a `lookup`, with
aliases in the words people say ("things to do", "day trips", "reviews",
"when can i go", …).

There is **no canonical read**: GetYourGuide's Partner API is a public
catalogue with nothing that is the person's own — no bookings, no saved
tours — so nothing here answers "what's new / due / on" for them, and no
tool names a subject. A compound ask such as *"what's on this weekend in
travel, and any good day trips from Lisbon?"* is answered by the group's
other members for the first half; the second half is an ordinary lookup
here (`gyg_search_tours` with `q: "lisbon day trip"`, or
`gyg_list_location_tours`).

This server calls the Partner API directly with an API key — it is not
browser-bridged, so it never answers "needs your browser open".
