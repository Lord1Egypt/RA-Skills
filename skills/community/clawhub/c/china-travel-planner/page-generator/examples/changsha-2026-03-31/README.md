# changsha-2026-03-31

A real example page for the travel-page-framework.

## Scenario

- 7-day Changsha trip
- metro-line coverage goal
- fixed hotel anchor for the first 3 nights
- recommended second hotel for the last 3 nights
- side trips to Xiangtan, Zhuzhou, and Yueyang

## Files

- `data/trip-data.json` — structured trip content
- `index.html` — example page rendering this content

## How to preview

From the framework root:

```bash
python3 -m http.server 8766 --directory examples/changsha-2026-03-31
```

Then open:

```text
http://127.0.0.1:8766
```

## Notes

This example is intended to validate:
- the shared trip schema
- card structure reusability
- itinerary-to-page conversion flow
- destination data replacement without rewriting the page layout
