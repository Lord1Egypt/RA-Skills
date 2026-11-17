# Xingzhe CLI Workflows

Use this reference for official Xingzhe OAuth, route-book queries, navigation
data, and GPX downloads through `cycling-health`.

## Boundary And Authentication

The adapter uses Xingzhe's official OpenAPI with read scope only. It can list
personal/collected routes, fetch raw navigation data, and download GPX. It does
not create routes, upload activities, request write scope, or upload a course
to Garmin.

Check the selected profile:

```bash
cycling-health --profile PROFILE xingzhe auth status --output json
```

For first-time setup, direct the user to the release archive's
`docs/xingzhe.md`. The Xingzhe application callback domain must be `localhost`;
the client secret should come from a local mode-0600 file or environment
variable, never chat or shell history. Browser authorization is:

```bash
cycling-health --profile PROFILE xingzhe \
  --client-id CLIENT_ID --client-secret-file SECRET_FILE \
  auth login --output json
```

The default callback is `http://localhost:8766/callback`; `--callback-port 0`
selects a free local port. `auth logout` previews local credential deletion and
requires `--confirm` for the actual deletion.

## Query Route Books

List routes created by or collected by the authenticated user:

```bash
cycling-health --profile PROFILE xingzhe route list \
  --collection mine --offset 0 --limit 20 --output json
cycling-health --profile PROFILE xingzhe route list \
  --collection collects --offset 0 --limit 20 --output json
```

The official API caps a page at 20 routes. Continue with offsets of 20 only
when more results are needed. List output can include route ID, title,
description, sport, distance, and create/update times.

Fetch one route when navigation, elevation, waypoint, POI, turn, polyline, or
climb data is needed:

```bash
cycling-health --profile PROFILE xingzhe route get \
  --route-id ROUTE_ID --output json
```

Analyze only fields actually returned. Route distance/elevation describes the
planned course, not a completed ride or achieved performance.

## Download GPX

Download only on an explicit request and use a user-approved destination:

```bash
cycling-health --profile PROFILE xingzhe route download \
  --route-id ROUTE_ID --path /absolute/path/route.gpx --output json
```

The destination is created with owner-only file permissions. Existing files
are rejected unless `--overwrite` is supplied; never add that flag without
explicit approval. Failed or empty downloads are removed. Report route ID,
absolute path, byte count, and whether the file was saved.

The resulting GPX can be imported through Garmin CN or the user's normal device
workflow. Do not claim that `route download` has uploaded or installed the
course on Garmin CN or a Garmin device.

## Failure Handling

- Missing app credentials: direct the user to `docs/xingzhe.md`; do not ask for
  the secret value.
- Expired access token with a refresh token: allow the CLI's automatic refresh
  and preserve any final OAuth error.
- Port conflict: retry login with `--callback-port 0`.
- Empty route page: report the selected profile, collection, and offset; do not
  treat it as an activity-data gap.
- Existing GPX destination: stop and ask whether to choose a new path or
  explicitly overwrite it.
