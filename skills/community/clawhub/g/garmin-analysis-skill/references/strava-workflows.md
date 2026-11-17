# Strava CLI Workflows

Use this reference for official Strava OAuth and personal read-only athlete,
activity, route, gear, and API rate-limit queries through `cycling-health`.

## Authentication

Check the selected profile without exposing OAuth tokens:

```bash
cycling-health --profile PROFILE strava auth status --output json
```

For first-time setup, direct the user to the release archive's
`docs/strava.md`. The Strava application callback domain must be `localhost`;
the client secret should come from a local protected file or environment
variable, never chat or a command-line argument. The adapter accepts only
read-only scopes.

The default callback is `http://localhost:8765/callback`. Use
`--callback-port 0` when the port is occupied. Access tokens are refreshed and
saved automatically. Profiles isolate credentials for different accounts.

Authorization revocation is preview-first:

```bash
cycling-health --profile PROFILE strava auth revoke --output json
cycling-health --profile PROFILE strava auth revoke --confirm --output json
```

The confirmed command deauthorizes the application remotely and deletes local
credentials. Run it only after explicit user authorization.

## Athlete And Zones

```bash
cycling-health --profile PROFILE strava athlete get --output json
cycling-health --profile PROFILE strava athlete zones --output json
```

Use athlete details for account/profile context and zones for the user's
configured heart-rate and power boundaries. Do not infer missing zones or
replace source-specific Garmin/Intervals zones silently.

## Cycling Activities

Start with a bounded date range:

```bash
cycling-health --profile PROFILE strava activity list \
  --start YYYY-MM-DD --end YYYY-MM-DD --page 1 --per-page 100 --output json
```

Filter returned records to cycling types relevant to the question. Fetch one
activity and add laps or streams only when needed:

```bash
cycling-health --profile PROFILE strava activity get \
  --activity-id ACTIVITY_ID --output json
cycling-health --profile PROFILE strava activity laps \
  --activity-id ACTIVITY_ID --output json
cycling-health --profile PROFILE strava activity streams \
  --activity-id ACTIVITY_ID \
  --keys time,distance,heartrate,cadence,watts --output json
```

Use activity detail for summary metrics, laps for structured sections, and
streams for pacing, heart-rate drift, cadence, or power questions. Request
only necessary stream keys. Missing heart rate, cadence, or watts normally
means the activity lacks that sensor stream; report that separately from API
errors.

## Routes And Gear

```bash
cycling-health --profile PROFILE strava route list \
  --page 1 --per-page 100 --output json
cycling-health --profile PROFILE strava route get \
  --route-id ROUTE_ID --output json
cycling-health --profile PROFILE strava route streams \
  --route-id ROUTE_ID --output json
cycling-health --profile PROFILE strava gear get \
  --gear-id GEAR_ID --output json
```

Use route metadata before requesting route streams. Route distance and
elevation describe a planned route, not a completed performance. Gear IDs from
activities can be resolved with `gear get`; do not assume gear ownership or
usage when the activity does not reference it.

## Rate Limits And Boundaries

```bash
cycling-health --profile PROFILE strava rate-limit --output json
```

Every Strava API response includes observed rate-limit headers. Query
`rate-limit` before a large paginated request or when the API returns 429. The
CLI uses official read-only endpoints and does not create, update, delete,
upload, synchronize, compare, or cache Strava data.

## Failure Handling

- Missing credentials: direct the user to local OAuth setup; never request the
  client secret or token in chat.
- Missing scopes: identify the required read-only scope and let the user
  reauthorize the same profile locally.
- HTTP 401 after refresh: report the profile and direct the user to login again.
- HTTP 429: report returned short-term/daily usage and stop until the limit
  resets; do not scrape or bypass the official API.
- Empty activity or route page: report the exact profile, date range/page, and
  filters before widening the query.
- Missing streams: distinguish absent sensor data from endpoint failure.
