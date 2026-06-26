# Knowledge Bundle

This directory ships domain reference data used by the skill scripts.

For the initial public release we keep only the schema / placeholder files
here so the bundle stays small and reviewable. Full reference tables (ICD-10
master, drug aliases, LOINC mapping, industry medians, curriculum codes,
symbol libraries, etc.) can be added incrementally via subsequent releases
without breaking the published API.

Add your own data by dropping CSV/JSON files into this directory and
pointing the relevant environment variable in `SKILL.md` to override the
bundled defaults.
