# California Coast Golden Example

This is a脱敏 fixture for regression checks, not a live travel recommendation.

## What It Covers

- 3-day California coast self-drive route.
- Fixed public hotel-area anchors without booking confirmations or private addresses.
- Low-stamina comfort profile: late starts, daylight driving, meal/rest protection, and clear cut rules.
- Multi-provider map chooser: Apple Maps, Google Maps, Amap / 高德, Baidu / 百度.
- A/B/C priority badges separated from stop names.
- Swipeable stop galleries with captions, credits, and source links.
- Hotel/start/final anchors with `imageQuery` placeholders when no exact public image is embedded.
- Weather, road, ticket, restaurant, and image source provenance records.
- `.ics` calendar generation through the shared template runtime.

## Commands

```bash
node scripts/validate-route-artifact.mjs examples/california-coast-golden.html
node scripts/run-output-eval.mjs examples/california-coast-golden.html
```

## Fixture Rules

- Refresh all weather, road, ticket, restaurant, parking, and image facts before using this as a real itinerary.
- Keep public examples free of home addresses, traveler names, hotel confirmation details, private calendar names, personal medical status, emails, phone numbers, and payment details.
- If a visual source is uncertain, prefer a `Visual reference` link and `imageQuery` placeholder over embedding a questionable image.
