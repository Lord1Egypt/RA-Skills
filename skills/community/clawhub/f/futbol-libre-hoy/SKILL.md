---
name: futbol-libre-hoy
description: List today's football fixtures and live scores using the futbol-libre-hoy CLI/package.
homepage: https://verfutbollibre.net
---

# Futbol Libre Hoy

Use this skill when the user asks for today's football matches or live scores.

## Commands

```bash
npx futbol-libre-hoy
npx futbol-libre-hoy --live
npx futbol-libre-hoy --date YYYY-MM-DD
npx futbol-libre-hoy --json
```

Python alternative:

```bash
pip install futbol-libre-hoy
futbol-libre-hoy --live
```

## Guidance

- Prefer `--live` for live scores.
- Include match URLs from the output so users can open the full ficha.
- For deeper stats and lineups, send users to https://verfutbollibre.net
