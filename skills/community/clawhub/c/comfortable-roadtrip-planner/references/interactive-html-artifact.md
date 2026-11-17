# Interactive HTML Route App Reference

Use this when the user wants the final trip artifact, a visual route map, previous-style HTML output, flip-card details, image-rich stop cards, or one-click calendar import.

## Product Promise

The finished HTML should feel like a small personal travel app, not a printed itinerary. It should answer four questions at a glance:

- Where do we drive today?
- Which stops matter, and which can be skipped?
- What does each place look/feel like?
- How do I navigate, buy tickets, eat, or add this day to my calendar?

## Required Features

- One static HTML file that works from `file://` when possible.
- One card per day with:
  - date, origin, destination, and one-sentence strategy
  - weather in the user’s preferred unit
  - total drive time/distance/difficulty and fatigue warning
  - embedded mini map with numbered markers and route polyline
  - ordered stop list that opens a multi-provider map chooser
  - distinct `A/B/C` priority badges beside stop names when priorities are present
  - route chooser matching the same stop order
  - leg-by-leg navigation for multi-stop days
  - per-day “Add to Calendar” `.ics` download
- Card interaction:
  - clicking anywhere on the card opens the day detail panel
  - links and map controls remain clickable without opening the panel
  - detail panel uses a flip or reveal motion, blurred/dimmed backdrop, close button, outside-click close, and Escape close
  - respect `prefers-reduced-motion`
- Detail panel:
  - swipeable stop image gallery when multiple images are available
  - per-image title/caption/source so visual references can distinguish classic views, “网红机位”, low-effort viewpoints, hotel exteriors, or backup indoor angles
  - why this stop is worth it compared with alternatives
  - short background/history when useful
  - comfort note for low-stamina/pregnancy/elderly/family travelers
  - map chooser links for Apple Maps, Google Maps, Amap / 高德地图, and Baidu Maps / 百度地图
  - links for tickets, official page, parking, restaurants, or visual references
  - meal/rest strategy and cut rules
- Calendar import:
  - generate `.ics` files in the browser via Blob downloads
  - include `SUMMARY`, `DTSTART`, `DTEND`, `LOCATION`, `DESCRIPTION`, and `URL` when available
  - include map/ticket links in `DESCRIPTION`
  - offer all-day events by default unless the user provides exact times
  - set a stable filename such as `day-3-san-francisco.ics`

## Data Model

Prefer a structured JavaScript array. Keep route order and display order explicit:

For reusable artifacts, follow `references/trip-data-contract.md` and `schemas/trip-data.schema.json`.

```js
const tripDays = [
  {
    id: "day-1",
    title: "Day 1 | 6/15 | City A to City B",
    date: "2026-06-15",
    color: "#2d7f9f",
    strategy: "Main idea for the day.",
    weather: ["City A 24/16°C", "City B 28/17°C"],
    drive: {
      summary: "About 4-5 hr / 280 mi",
      difficulty: "Medium",
      note: "Main fatigue source."
    },
    stops: [
      {
        name: "Stop name",
        lat: 37.0,
        lng: -122.0,
        address: "Stop address or map query",
        priority: "A keep",
        tag: "low-effort high-reward",
        why: "Why this stop earns a place in the day.",
        history: "One short background sentence.",
        tip: "Comfort/safety note.",
        imageQuery: "Search query to use if photos still need to be filled.",
        imageNote: "Optional note for missing hotel/start/anchor photos.",
        images: [
          {
            src: "https://example.com/image.jpg",
            alt: "Image alt text",
            title: "Classic viewpoint",
            caption: "Why this visual angle matters or when to skip it.",
            credit: "Source or photographer",
            link: "https://example.com/source"
          }
        ],
        links: [
          ["Official", "https://..."],
          ["Tickets", "https://..."]
        ]
      }
    ],
    meals: [
      {
        label: "Lunch",
        text: "Where and why.",
        links: [["Restaurant", "https://..."]]
      }
    ]
  }
];
```

## Route Rules

- Main route points should be the actual driving chain.
- Optional after-check-in stops may be shown in details, but do not force them into the main route if they distort the map.
- Route links must use the same order as the map polyline.
- Stop lists, route buttons, and marker popups should open the shared map chooser instead of hard-coding one provider.
- Include Apple Maps, Google Maps, Amap / 高德地图, and Baidu Maps / 百度地图 for every stop.
- Prefer Google Maps for full multi-stop routes. Include Apple/Amap/Baidu first-to-last route links and leg-by-leg route links because provider URI support differs by device and waypoint behavior.
- For China-mainland trips, verify local POI names and coordinate systems before embedding the artifact. Baidu URI links should specify `coord_type` when using non-Baidu coordinates. Amap marker links can declare `coordinate=wgs84`; Amap route URI works best when coordinates are verified for the target region.
- Do not include private home addresses or personal medical details in public examples.

## Image Sourcing Rules

- Use user-provided images, URLs, hotel links, booking-site public pages, or official venue pages when available.
- If the user asks the skill to find visuals, browse/search for stable public or official sources and record source/credit/link on each image.
- For attractions, prefer 2-4 images that help a traveler choose a camera spot: classic frame, easy/low-walk angle, indoor/rain backup, or optional “internet-famous” shot.
- For hotels, starts, airports, rental-car points, and final anchors, fill images when the exact public place is known. If only a private address is known, avoid exposing it in a public artifact.
- If image rights or hotlink reliability are uncertain, do not embed the image; add an outbound `Visual reference` link and leave an `imageQuery` placeholder.
- Caption photos honestly when a shot is hard to recreate, requires a long walk, poor parking, night driving, or body-battery risk.

## Template

Start from `assets/interactive-route-map-template.html` for new HTML artifacts. Replace `tripDays` first, then tune visual styling only if the user asks for a different mood.

## Verification Checklist

- Open the HTML locally.
- Confirm every day card appears.
- Confirm maps are nonblank and fit bounds correctly.
- Confirm route and stop map choosers open from card buttons, ordered stop links, detail stop buttons, and map marker popups.
- Confirm priority labels render as separate badges and do not blend into stop names.
- Confirm multi-image stop galleries swipe/scroll horizontally and captions/credits are readable.
- Confirm missing hotel/start/anchor images show the search/fill placeholder instead of an empty gray box.
- Confirm Google full-route links contain the intended driving order.
- Confirm Apple Maps, Amap, and Baidu links open reasonable first-to-last or leg-by-leg routes.
- Confirm card click opens the flip detail panel, close button works, outside click works, and Escape works.
- Confirm `.ics` downloads open/import in Apple Calendar or another calendar app.
- Confirm links are clickable on mobile-sized viewport.
- Confirm no private addresses, names, hotel confirmations, or medical details appear in a public artifact unless explicitly requested.
- Run `node scripts/validate-route-artifact.mjs <artifact.html>` when working inside this repository.
- Run `node scripts/run-output-eval.mjs examples/california-coast-golden.html` after artifact-shape changes.
