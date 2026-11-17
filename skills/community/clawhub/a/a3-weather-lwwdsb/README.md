# a3-weather

An OpenClaw skill that returns a daily forecast plus a short day plan:

- conditions, high/low, precipitation chance, wind, UV index
- tips: umbrella (≥40% precipitation), sunscreen (UV ≥ 6), layers (large temperature swing), heat/cold
- the best 3-hour dry, comfortable outdoor window between 08:00 and 20:00

Zero dependencies; requires Node ≥ 18. No API key.

```
node scripts/a3-weather.mjs --city Seattle --date tomorrow --units metric
node scripts/a3-weather.mjs --lat 34.05 --lon -118.24 --name "Los Angeles" --json
```

Exit codes: `0` ok, `2` invalid input, `3` data unavailable (the skill never fabricates a forecast).

Tests: `node --test test/*.test.mjs` (they use a local fake API; no network needed).

## Examples

```
a3-weather --city "Los Angeles"                       # today, imperial units
a3-weather --city Tokyo --date tomorrow --units metric
a3-weather --city London --date 2026-11-20 --json     # up to 7 days ahead
```

## Version

1.0.0 — first public release. Publish with `clawhub skill publish ./skills/a3-weather --version 1.0.0`.

## Data attribution

Weather and geocoding data by [Open-Meteo.com](https://open-meteo.com/), licensed under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Open-Meteo's free API is for
non-commercial use.

## License

MIT — original work written for USC CSCI 599 Assignment 3.
