---
name: astronomy-data
description: "Research-grade astronomical data from NASA/JPL DE440 through the Astro Agents API: sunrise, sunset and twilight, altitude and azimuth, observation windows, Moon phase and distance, the day's sky for a place, planet positions, eclipses with local circumstances, planetary phenomena, seasons, celestial event calendars, longitude time series, time scales and coordinate conversion, for any date 1800-2200. Use it when a task needs exact astronomical times, positions or events instead of estimating them: every result is computed (no LLM) and SHA-256 verifiable."
license: MIT
compatibility: "Needs network access to https://astro-agent.dev (REST) or its remote MCP server https://astro-agent.dev/mcp. No install."
metadata:
  author: "Astro Agents"
  version: "1.10.0"
  homepage: "https://astro-agent.dev"
---

# Astronomical data with the Astro Agents API

Exact astronomical answers from the NASA/JPL DE440 ephemeris, for any date from 1800 to 2200. Call the API instead
of computing positions or times yourself: time zones, daylight saving of past years, Delta T, refraction and
eclipse geometry are where estimates go wrong. Every answer is computed (no language model), states its
conventions in `result.settings`, and carries `meta.result_sha256`, which `POST https://astro-agent.dev/v1/verify` (free)
recomputes.

## How to call it

- **REST:** `POST https://astro-agent.dev/v1/<route>` with a JSON body; the free catalog `GET https://astro-agent.dev/v1/catalog` lists every route
  with its input schema, price and an example.
- **MCP:** connect the remote server `https://astro-agent.dev/mcp` (Streamable HTTP); each route below is also an MCP tool.
- **Times and places:** give `datetime` in UTC (`Z`), with an offset, or as local clock time together with
  `latitude` and `longitude` (the historical time zone is resolved for you); a place-and-day route takes `date`.
- **Errors:** 400 with a `code` for invalid input (never charged); see https://astro-agent.dev/docs/errors.

## Paying for calls

- **First try:** every client gets 1 free call on the $0.01-0.02 routes, without a key.
- **A key** (free plan: an email, no card; paid plans by card on https://astro-agent.dev/pricing) or **prepaid credits**: send it
  in the `X-Credits-Token` header (REST, or the MCP client's headers). Credits are bought in USDC at
  `POST https://astro-agent.dev/v1/credits/topup` and each call spends its listed price.
- **Pay per call (x402):** without a key, a paid call answers HTTP 402 with an x402 offer (USDC on Base or
  Solana) in the body and the `PAYMENT-REQUIRED` header; an x402 client signs it and retries with
  `PAYMENT-SIGNATURE`. Over MCP the offer is in the tool result and the payment goes in `_meta["x402/payment"]`.

## Routes and prices (per call)

| Route | MCP tool | Price | What it returns |
|---|---|---|---|
| `POST /v1/astronomy/positions` | `body_positions` | $0.01 | Ecliptic longitude and latitude, daily speed, retrograde flag and distance of the Sun, the Moon, Mercury..Pluto and the lunar nodes, for any moment 1800-2200. |
| `POST /v1/astronomy/sky` | `sky_now` | $0.01 | The sky at a moment: planetary positions, which planets are retrograde, the Moon's phase and illumination, and the exact times of the next stations, lunations and separations. |
| `POST /v1/astronomy/rise-set` | `rise_set_times` | $0.01 | Rise, transit and set of the Sun, Moon and planets for a place and local day, with civil, nautical and astronomical twilight, day length, golden hour and blue hour. |
| `POST /v1/astronomy/altaz` | `altitude_azimuth` | $0.01 | Where the Sun, Moon and planets are in the sky from a place at a moment: altitude, azimuth, compass point, topocentric right ascension and declination, distance, elongation, illumination and magnitude. |
| `POST /v1/astronomy/visibility` | `observation_windows` | $0.02 | When each planet and the Moon can be observed from a place during a night: windows above a minimum altitude while the sky is dark, with the best time, altitude, azimuth and magnitude. |
| `POST /v1/astronomy/moon` | `moon_details` | $0.01 | The Moon at a moment: phase name and angle, illuminated fraction, age, lunation number, distance and apparent size, the next new, first quarter, full and last quarter Moons, and the next perigee and apogee. |
| `POST /v1/astronomy/day` | `day_summary` | $0.02 | One call for a day at a place: sunrise, sunset, twilight, day length, golden and blue hour; the Moon's phase, illumination, rise and set; the planets observable that night; the next lunations, planetary stations and eclipse. |
| `POST /v1/astronomy/seasons` | `seasons` | $0.01 | The year's equinoxes and solstices and Earth's perihelion and aphelion to the second; optionally the Sun day by day: sunrise, sunset, day length, solar noon, declination and equation of time. |
| `POST /v1/astronomy/time` | `time_scales` | $0.01 | One moment in every astronomical time scale: UTC, unix time, Julian day (UTC, UT1, TT, TDB), MJD, Julian centuries, Delta T, TAI-UTC, UT1-UTC, Greenwich and local mean and apparent sidereal time. |
| `POST /v1/astronomy/convert` | `convert_coordinates` | $0.01 | Convert one direction on the sky between equatorial (J2000 and of date), ecliptic (J2000 and of date), galactic and, with a moment and a place, horizontal coordinates. |
| `POST /v1/astronomy/phenomena` | `planetary_phenomena` | $0.10 | Every conjunction with the Sun (inferior / superior for Mercury and Venus), opposition, greatest elongation, conjunction between two planets, perihelion and aphelion between two dates, to the second. |
| `POST /v1/astronomy/eclipse-local` | `local_eclipse` | $0.10 | For a place: every solar and lunar eclipse between two dates with its local circumstances: whether and how it is seen, contact times, magnitude, obscuration, duration and the Sun's or Moon's altitude. |
| `POST /v1/astronomy/solunar` | `solunar_periods` | $0.01 | The day's solunar periods for a place: major periods centred on the Moon's upper and lower meridian transits, minor periods centred on moonrise and moonset, with the Moon's phase. |
| `POST /v1/astronomy/angles` | `angular_separations` | $0.02 | Pairs of bodies whose ecliptic separation is within a tolerance of 0, 60, 90, 120 or 180 degrees (or any angle you choose), with the deviation; optionally equal and opposite declinations. |
| `POST /v1/astronomy/events` | `celestial_events` | $0.25 | Solar and lunar eclipses, planetary stations, lunations, separations, longitude crossings and declination events between two dates (1800-2200), to the minute. |
| `POST /v1/astronomy/longitude-series` | `longitude_series` | $0.20 | Ecliptic longitudes of the planets at one moment or as a time series (1 hour to 1 week steps), geocentric and heliocentric, with optional angle offsets, multi-body averages and declinations. |
| `POST /v1/astronomy/sky-analogues` | `similar_skies` | $0.25 | The past or future dates whose planetary positions best match a reference sky, ranked by a stated angular distance. |
| `POST /v1/astronomy/local-time` | `resolve_local_time` | $0.01 | Local time + place -> exact UT, historical UTC offset, Delta T, Local Mean Time, true solar time. |

## Examples

### `POST /v1/astronomy/rise-set`

```bash
curl -s -X POST https://astro-agent.dev/v1/astronomy/rise-set -H 'Content-Type: application/json' \
  -H "X-Credits-Token: $ASTRO_AGENTS_KEY" -d '{"date": "2026-06-21", "latitude": 37.7749, "longitude": -122.4194}'
```

Real answer (excerpt):

```json
{
  "endpoint": "astronomy/rise-set",
  "result": {
    "subject": {
      "timezone": "America/Los_Angeles"
    },
    "sun": {
      "sunrise": "2026-06-21T05:48:05-07:00",
      "sunset": "2026-06-21T20:35:02-07:00",
      "civil_dusk": "2026-06-21T21:06:23-07:00"
    }
  },
  "meta": {
    "result_sha256": "c8d49c7a3abf5cc266183675922a069e3b235fd88aeb43faf48bb6c40b709ca8"
  }
}
```

### `POST /v1/astronomy/moon`

```bash
curl -s -X POST https://astro-agent.dev/v1/astronomy/moon -H 'Content-Type: application/json' \
  -H "X-Credits-Token: $ASTRO_AGENTS_KEY" -d '{"datetime": "2026-12-24T20:00:00Z"}'
```

Real answer (excerpt):

```json
{
  "endpoint": "astronomy/moon",
  "result": {
    "phase": {
      "name": "full moon",
      "phase_angle": 191.0345,
      "illuminated_fraction": 0.99009,
      "waxing": false,
      "age_days": 15.7973,
      "lunation": 1286
    },
    "distance": {
      "km": 356875.0,
      "earth_radii": 55.9529,
      "angular_diameter_arcmin": 33.473
    }
  },
  "meta": {
    "result_sha256": "4b78be831030c902599a54299cd6a5a9a6416687baf005a9583ebc878bb9cfd9"
  }
}
```

### `POST /v1/astronomy/events`

```bash
curl -s -X POST https://astro-agent.dev/v1/astronomy/events -H 'Content-Type: application/json' \
  -H "X-Credits-Token: $ASTRO_AGENTS_KEY" -d '{"start": "2026-01-01", "end": "2026-12-31", "include": ["eclipse"]}'
```

Real answer (excerpt):

```json
{
  "endpoint": "astronomy/events",
  "result": {
    "events": [
      {
        "kind": "solar",
        "eclipse_type": "annular",
        "exact_utc": "2026-02-17T12:12Z"
      },
      {
        "kind": "lunar",
        "eclipse_type": "total",
        "exact_utc": "2026-03-03T11:34Z"
      },
      {
        "kind": "solar",
        "eclipse_type": "total",
        "exact_utc": "2026-08-12T17:46Z"
      },
      {
        "kind": "lunar",
        "eclipse_type": "partial",
        "exact_utc": "2026-08-28T04:13Z"
      }
    ]
  },
  "meta": {
    "result_sha256": "dea24206e4ce197479f00f08252f3df7323ec8abf6bff92f9f91bfa2e50f857f"
  }
}
```

## Good practice

- Quote values as returned and keep `meta.result_sha256` with them; do not recompute or round them.
- For a place, pass coordinates; the result gives local times with their UTC offset and the UTC instant.
- Long ranges: the event calendar takes up to a year per call; page year by year and de-duplicate on `key`.
- Data only: no predictions, never a signal or forecast.

Docs: https://astro-agent.dev/docs · Reference: https://astro-agent.dev/llms-full.txt · Engine 1.10.0
