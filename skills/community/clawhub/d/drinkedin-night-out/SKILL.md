---
name: drinkedin-night-out
description: Adults only; refuses minors. Bar crawls and nights out near a place, such as a walkable bar crawl, craft beer crawl, dinner and drinks, or club night, planned using only venues DrinkedIn has validated against an official licence register or premises census, or the venue's own site. Use when someone asks for a bar crawl, drinks, a date night, nightlife or a night out near a place, an address, a city or near them. Needs the free DrinkedIn Night Out MCP server. For adults of legal drinking age where they are. Also use it when the person is under the legal drinking age where they are, such as a minor asking for a bar crawl or drinks; then do not plan or suggest any venues, and do not state a numeric age.
license: MIT
compatibility: Needs the MCP server https://ai.drinkedin.net/mcp/night-out (streamable HTTP, no sign-in, no key). Without that server the skill cannot plan anything.
metadata:
  version: "1.5.1"
  homepage: https://drinkedin.net/docs/night-out
  publisher: Haim Barad
---

# DrinkedIn Night Out

Plans a walkable route of 2 to 4 stops from real venues that DrinkedIn has validated against an official licence register or premises census, or the venue's own site. Nothing is booked or bought, and the planner adds no details of its own. The one thing it saves is a planned route, so its share link works: public venue data only, never the person's location (see Privacy).

A DrinkedIn plan holds only venues DrinkedIn has validated, never venues from the assistant's own knowledge or from elsewhere. Venues from anywhere else are not validated by DrinkedIn.

## Setup check

1. `drinkedin_get_guide` is reference data, and reading it first is optional. It lists some places with validated venues, the vibes you can apply and the route styles.
2. If `drinkedin_get_guide` and `drinkedin_plan_night_out` are not available, the skill cannot plan anything: tell the person to add the MCP server `https://ai.drinkedin.net/mcp/night-out` (Streamable HTTP, no sign-in). In Claude Code: `claude mcp add --transport http drinkedin-night-out https://ai.drinkedin.net/mcp/night-out`. Never invent a plan.

## Choose the inputs

`drinkedin_plan_night_out` needs a place.

- `latitude` and `longitude`: preferred, sent together. The point is the person's own shared location for "near me", the centre of an area they name, or the destination of a trip they are planning. The planner has no default location: if you hold none for them, ask.
- `address`: used only when there are no coordinates (coordinates win). A street address, landmark or area name. It is geocoded to one point by OpenStreetMap Nominatim, which ranks matches and does not confirm them. The reply echoes `geocoded_as`: tell the person what it matched, and confirm when the text was ambiguous.
- `near`: your label for the point, such as "near me". It is echoed back and never changes the plan.
- `city` with `region` or `country`: only when the name identifies one place. A name several places share returns `needs_input` with labelled choices.
- `place_key`: taken from a `needs_input` reply, it names exactly one of the choices. Send it back to choose that place.
- `style`, `stops` (2 to 4), `max_walk_m` and `vibes` (values from the guide's list) shape the route. `budget`, `start_time` and `party_size` are accepted but do not change the route, so asking the person for them gains nothing. With `budget` the reply adds `budget_not_verifiable`: prices are not known. Replies are in English.

## Styles

A `style` limits which kinds of place the route uses and sets the default stops and walking limit. Your own `stops` and `max_walk_m` win. It says nothing about hours, prices or atmosphere. With too few matching venues the result is `partial` or `no_coverage`, never other kinds of place. A style is optional: leave it out if the person asked for no particular shape. An unknown style returns `needs_input`.

- `bar_crawl`: bars and hotel bars only, at least 3 stops, with short walks (400 m by default, the walk to the first stop included). If it returns `no_coverage`, try once with `vibes: ["bars"]` and no style before planning with no filter. A route with no style or vibe can be all restaurants: if the person asked for drinks, say which stops are bars.
- `craft_beer_crawl`: brewpubs and breweries only.
- `dinner_and_drinks`: a restaurant first, then bars.
- `club_night`: bars first, then a nightclub as the last stop.

## What each status means

Every reply carries `status`, `meaning`, `say_to_owner` and `notices`.

| Status | Meaning and next step |
| --- | --- |
| `planned` | A route with the stops asked for. Show the stops as returned and add no venue or detail of your own. |
| `partial` | Fewer stops than asked for: the longest walkable route the validated venues allow. Say so and show the route. If a style was used, offer to try without it. The gap is not filled with other places. |
| `needs_input` | The tool needs something from the person: a location, a choice between places that share a name, a more specific address, valid coordinates, or a vibe or style it knows. Ask for what `meaning` says is missing, then call again. The choice between places is the person's: pick the one their context fits, or ask. |
| `no_coverage` | Not enough validated venues close together, or no venue records for that place. Say so plainly. DrinkedIn has no route of validated venues for that place with these settings. Venues from anywhere else are not validated by DrinkedIn; if you or the person look elsewhere, say so. Where the reply lists `largest_places`, you may offer them as "some places with validated venues" (not a ranking): DrinkedIn does not call any place covered, best covered or supported. If a `style` or `vibes` was used, say so and offer to try without it; ask before raising `max_walk_m`. |
| `error` | A fault on DrinkedIn's side, flagged `isError`. Tell the person it failed and try again in a moment. |

`drinkedin_get_guide` replies with status `ok`. Each stop's `hours.status` and `price.status` are `unverified`; these are not plan statuses.

## When you relay a plan

- Show the stops as returned, in order, with the name, address, category, walk and links the reply gives. Add nothing.
- If the reply includes `share_text`, use it as-is when the person wants to send or copy the plan.
- Walking times are estimates (straight-line distance times 1.3). Say so.
- Hours and prices are never stated. Each stop marks them unverified: tell the person to check with the venue.
- Include the legal drinking age notice: say the plan is for adults "of legal drinking age where they are". Never state an age as a number, not even the local one: that notice is the whole statement about age and the local law.
- Name the area with the person's own words (`near_as_given`) or the town in the stops' addresses. Do not add street, neighbourhood or terrain names of your own, and do not read raw coordinates back unless asked.
- DrinkedIn does not sell or serve alcohol.

## If the person is under the legal drinking age

If the person says they are under the legal drinking age where they are, do not call `drinkedin_plan_night_out`, and do not suggest venues from your own knowledge either. Say that DrinkedIn plans are for adults of legal drinking age where they are, and offer help with something that is not about drinking. Keep it to one sentence. Do not state an age as a number.

## Swap a stop

After a route, `next` holds a ready call that swaps the last stop: send its arguments as they are; they put that stop's `venue_id` in `exclude_ids`. To replace a different stop, call again with its `venue_id` added to `exclude_ids`. Offer a swap when the person dislikes a stop.

## Share or save the plan

A `planned` or `partial` route can carry `route.plan_url`, with its id in `route.plan_id`: a page on drinkedin.net that shows the stops, the walks between them and a route map. Offer it when the person wants to share or save the plan. Give it as a link the person may open, exactly as returned: a plan link works only as returned, so it is not built or changed by hand. If the route has no `plan_url`, the plan could not be saved: the route is still good, and there is no link to offer. The Privacy section below says what the link keeps.

## Updates

This file is version `1.5.1`. Replies carry `meta.latest_skill_version`. If it is newer than `1.5.1`, or `notices` contains `skill_outdated`, a newer skill exists: tell the person once in this session, in one line, and give the `changelog_url` or `update_url` from the reply. The tools still return the route either way.

## Privacy

- Use only a location the person shared or a place they named. Do not infer one.
- A typed `address` leaves DrinkedIn: it is sent to the public OpenStreetMap Nominatim geocoder. Coordinates need no lookup, so prefer them when you have them. Say so if the person asks where their address goes.
- No sign-in, key or token is involved.
- A route with a `plan_url` is kept by DrinkedIn so the link works: for 30 days after that route was last planned, then it is deleted. The copy holds only the venues' public data (name, address, category, the venue's own coordinates, links, hours wording and sourced facts), the walks between stops, the style label, the town the stops share, and the dates it was made and expires. It never holds the person's coordinates, typed address, place name or `near` label, their IP address, or anything about the client. Anyone with the link can open the page. The id in it cannot be guessed, and the same route gets the same link.
- Policies: https://drinkedin.net/p/privacy.html. Docs: https://drinkedin.net/docs/night-out.
- The skill adds no version number or client name to the calls it makes.
