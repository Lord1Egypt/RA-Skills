---
name: comfortable-roadtrip-planner
description: "Plan comfort-first multi-day self-drive road trips (自驾游/路书/行程规划) and a one-file interactive HTML route app with maps, swipeable stop photo galleries, A/B/C priority-ranked stops, weather, meals, restrooms, tickets, Apple/Google/Amap/Baidu Maps, and .ics calendar import. Use when hotels are already fixed, travelers have limited stamina (pregnant/elderly/kids), days must stay daylight-friendly, or the user wants skippable stops instead of a packed attraction list. Also trigger for 舒适自驾, 孕期旅行, 自驾路线, road trip itinerary, route tradeoffs, and calendar-ready itineraries. Do not use for flights, hotel booking engines, or generic city walking tours."
metadata:
  author: CrazyRiceMaker
  homepage: https://github.com/CrazyRiceMaker/comfortable-roadtrip-planner
  version: "1.1.0"
  openclaw:
    homepage: https://github.com/CrazyRiceMaker/comfortable-roadtrip-planner
---

# Comfortable Roadtrip Planner

## Core Workflow

1. **Extract fixed anchors first.** Capture home/start, final destination, fixed hotels, dates, check-in/check-out, traveler constraints, and must-see interests. Treat fixed hotels as immovable unless the user asks to reconsider.
2. **Refresh volatile facts.** Check current weather, road closures, event traffic, venue hours, ticket availability, parking/accessibility, and restaurant hours for the relevant dates. Prefer official sources for road, venue, and ticket facts.
3. **Build the route as a comfort-first chain.** Optimize for fewer backtracks, daylight driving, bathroom/meal/rest breaks, and short high-reward stops. For pregnant, elderly, or low-stamina travelers, favor indoor/flat/short-walk experiences and avoid sand, steep trails, long hikes, timed tours, or late-night arrivals.
4. **Convert attractions into decisions.** Do not list every good place. Mark stops as:
   - `A` keep if possible
   - `B` do if timing/body battery is good
   - `C` skip freely
   Include a one-line reason and a clear escape rule.
5. **Produce route artifacts.** The signature deliverable is a one-file interactive HTML route app: day cards with embedded maps, clickable ordered stops, flip-card detail panels, swipeable stop photo galleries, reasons/history/tips, meal plans, ticket links, multi-provider map choices (Apple Maps, Google Maps, Amap/高德, Baidu/百度), and downloadable `.ics` calendar events. Also provide Markdown or calendar notes when requested.
6. **Verify artifacts.** For generated HTML/maps, open locally and check that day cards render, links exist, no stale route points remain, and the route order matches the intended driving flow.

## When Detail Matters

Read `references/comfort-routing.md` when deciding what to keep/cut, ranking stops, handling low-stamina or pregnancy constraints, or explaining whether a scenic detour is worth it.

Read `references/artifact-patterns.md` when creating or updating HTML route cards, Markdown itinerary files, Apple Calendar/iCal notes, priority labels, or navigation/ticket link formats.

Read `references/interactive-html-artifact.md` when producing the final HTML route app, adding map cards, flip details, photos, or calendar import. Reuse `assets/interactive-route-map-template.html` as the starting point when creating a new HTML artifact.

Read `references/trip-data-contract.md` when filling structured trip data, source provenance, weather, images, tickets, cut rules, parking, or medical backup fields.

When adding photos, prefer user-provided images first. If the user asks the skill to find visuals, verify stable public/official sources and keep source links/credits, especially for hotels, starts, and “internet-famous” camera spots.

## Live-Data Rules

- Browse or otherwise verify anything likely to change: weather, road closures, venue hours, ticket prices/availability, restaurant hours, events, construction, and parking.
- Give absolute dates when the user says “today,” “tomorrow,” or “next week.”
- Mark weather and road facts with the date checked when they are embedded in a reusable artifact.
- If exact map traffic cannot be fetched, give ranges and state that traffic can change.
- For reusable HTML artifacts, record checked volatile facts in `sourceProvenance[]`.

## Quality Gates

- Validate HTML artifacts with `node scripts/validate-route-artifact.mjs <artifact.html>` when the repository scripts are available.
- Use `examples/california-coast-golden.html` as the regression example for signature output quality.
- Run `node scripts/run-trigger-eval.mjs` and `node scripts/run-output-eval.mjs examples/california-coast-golden.html` after changing routing language, artifact structure, or comfort-first requirements.

## Output Style

- Keep plans scannable. Prefer bullets by day, then brief stop-level reasons.
- Write like a trip companion, not a database. Explain why a stop feels worth it and what can be skipped without regret.
- Include multi-provider map choices for stops/routes, and official ticket/venue links where needed.
- Avoid exposing private addresses, hotel confirmations, medical details, or personal constraints in public artifacts unless the user explicitly wants that local/private output.
