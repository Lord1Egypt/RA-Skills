# Country Holiday Data

This directory contains public holiday data used by the FIDIC Deadline Calculator.

## Bundled data

Only **Singapore** (`SG.json`) is bundled and maintained by the skill author, verified against the MOM gazette and eGazette.

## Other jurisdictions

For any non-Singapore seat, users must supply their own holiday file via `--holidays-file`. See `docs/holiday-file-format.md` for the JSON schema, a worked example, and source recommendations.

## File naming

`<ISO-3166-1-alpha-2>.json` — e.g. `SG.json`

## Refresh procedure

Check annually (typically Q4 when MOM publishes next year's gazette) for updated Singapore holidays. Update `SG.json`, run tests, and bump the skill version.

## Why only Singapore?

Holiday calendars vary by sub-jurisdiction (Malaysian state, UK constituent country, individual emirate), shift by moon-sighting, and are gazetted by each government's authoritative source. Rather than ship best-effort data that users might rely on without verification, we provide a clean extension mechanism and let users bring verified data from their own jurisdiction's gazette.
