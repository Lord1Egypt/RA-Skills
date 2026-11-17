# iGPSPORT CLI Workflows

Use this reference for profile-isolated iGPSPORT CN account queries and FIT
analysis through `cycling-health`.

## Boundary

- This is a personal, read-only adapter to the unsupported private iGPSPORT CN
  web API. Authentication and response behavior can change without notice.
- The CLI never writes remote iGPSPORT data. It does store local credentials,
  account metadata, and downloaded FIT files per profile.
- A profile can represent a different person. Preserve the selected
  `--profile` and its description, and do not combine its rides with Garmin or
  Intervals.icu until identity and duplication are explicitly established.

## Authentication And Accounts

Check the intended profile without exposing its token:

```bash
cycling-health igpsport auth status --output json
cycling-health --profile PROFILE igpsport auth status --output json
cycling-health igpsport account list --output json
cycling-health --profile PROFILE igpsport account get --output json
```

When login is needed, let the user enter the password interactively in their
local terminal:

```bash
cycling-health --profile PROFILE igpsport auth login \
  --username USERNAME --description "ACCOUNT PURPOSE"
```

The password is not stored. Do not request it in chat or place it directly on
the command line. For automation, the user can pipe it through
`--password-stdin` locally. `auth logout` only previews token deletion until
`--confirm` is supplied. Account descriptions can be changed with:

```bash
cycling-health --profile PROFILE igpsport account update \
  --description "ACCOUNT PURPOSE" --output json
```

## Activity Collection

Start with a bounded list and metadata detail:

```bash
cycling-health --profile PROFILE igpsport activity list \
  --start YYYY-MM-DD --end YYYY-MM-DD --page 1 --per-page 20 --output json
cycling-health --profile PROFILE igpsport activity get \
  --activity-id RIDE_ID --output json
```

Use `activity get --raw` only when a required metadata field is absent. The
detail endpoint normally supplies distance, duration, speed, ascent, title,
start time, and device metadata.

For one selected ride, add FIT-derived data only as needed:

```bash
cycling-health --profile PROFILE igpsport activity analyze \
  --activity-id RIDE_ID --output json
cycling-health --profile PROFILE igpsport activity streams \
  --activity-id RIDE_ID \
  --channels speed,heart_rate,cadence,elevation,power \
  --resolution 10s --max-points 5000 --output json
```

Supported stream channels are `speed`, `heart_rate`, `cadence`, `elevation`,
`power`, `gps`, `temperature`, and `distance`. Request only the channels needed
for the question. Use downsampled streams for pacing, drift, cadence, climbing,
or sensor-quality questions rather than returning every FIT point.

Export only when the user needs the file:

```bash
cycling-health --profile PROFILE igpsport activity export \
  --activity-id RIDE_ID --format fit --path ACTIVITY.fit --output json
```

The CLI caches downloaded FIT files per profile. `analyze`, `streams`, and
`export` reuse that cache; add `--refresh` only when the remote activity has
changed or the cache is suspected stale. An explicit export path can replace
an existing file, so check the destination and obtain approval before using an
occupied path.

## Analysis And Failure Handling

- Label all results as iGPSPORT CN and include the profile/description.
- Separate activity metadata from FIT sensor observations.
- A missing FIT channel usually means the bike computer or paired sensor did
  not record it; do not invent values or call it an API failure.
- Report truncation when stream output reaches `--max-points`.
- On expired authentication, direct the user to rerun interactive login for
  the same profile.
- On signing, endpoint, or payload errors, identify the integration as an
  unsupported private API and preserve the exact CLI error.
- Do not expose local credential paths or cached FIT contents unless they are
  necessary for an explicitly requested troubleshooting step.
