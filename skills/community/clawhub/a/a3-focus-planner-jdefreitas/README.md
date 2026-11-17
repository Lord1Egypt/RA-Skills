# Focus-gap planner

Original Assignment 3 skill: merge real busy intervals, detect overlaps, apply
meeting buffers, and suggest qualifying focus time without making bookings.

The skill works with an authorized calendar integration. The Assignment 3 adapter
is `openclaw:a3-google:a3_calendar_analyze`. Other assistants can use the included
portable offline Node helper with explicit offset-bearing event timestamps.

Example helper input:

```json
{"workStart":"2026-11-16T09:00:00-08:00","workEnd":"2026-11-16T17:00:00-08:00","events":[{"summary":"Fictional review","start":"2026-11-16T10:30:00-08:00","end":"2026-11-16T11:30:00-08:00"},{"summary":"Fictional study","start":"2026-11-16T10:45:00-08:00","end":"2026-11-16T11:15:00-08:00"}]}
```

Run `node scripts/plan.mjs` and provide the JSON on stdin. The helper has no network,
credentials, filesystem writes, or event mutation. Times are returned as UTC ISO
timestamps; the assistant renders them in the user's declared timezone. Convert
all-day events into explicit busy intervals before using this portable helper.

AI attribution: the initial skill and algorithm were drafted with Codex and tested
against independent overlap/gap expectations. Publication and a registry install
receipt are required before claiming the advanced-integration criterion complete.
