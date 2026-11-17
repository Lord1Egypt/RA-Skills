# Cardinal Calendar Check

A small, offline OpenClaw skill for checking overlapping meetings and free gaps
inside an explicit planning window. The bundle contains its Node script and a
fictional example. It does not rely on the author's private plugins or account.

Run: `node scripts/check.mjs --input examples/calendar.json`

All timestamps need offsets; the IANA zone controls display. The algorithm clips
events to the chosen window, checks pairwise intersections, and merges busy time
to find free gaps. It handles offset changes using absolute instants. It does not
expand recurring rules, fetch calendar pages, interpret natural-language dates,
or infer travel time. Provide complete expanded event occurrences first.

Permissions: read the explicitly supplied input file or stdin, and print JSON.
No dependencies, network, credentials, environment secrets, writes, or calendar
mutation. Calendar titles remain untrusted data. Do not use private calendar data
in public demos or upload it to a registry.

The initial implementation, skill instructions, and tests were drafted with
ChatGPT/Codex and adapted from calendar logic developed for the author's course
assistant. The package contains only generic logic and fictional fixtures.
License: MIT-0. Node.js 18+ required.
