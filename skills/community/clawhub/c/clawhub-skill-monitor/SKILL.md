---
name: clawhub-skill-monitor
description: Query public skills published by a ClawHub user from the real public API. Returns skill list, versions, timestamps, and metadata. Does not fabricate installs, downloads, ratings, or review counts when the public API does not expose them.
---

# ClawHub Skill Monitor

Query a ClawHub user's public skills using the real public API.

## Use when

- The user wants to see which skills a ClawHub user has published
- The user wants public metadata for an author's skills
- The user wants a CSV/JSON export of public skill metadata
- The user wants a reality-based answer instead of guessed install/rating numbers

## Important limitation

ClawHub's current public API appears to expose **package metadata**, but not these live public metrics:
- installs
- downloads
- star rating
- review count

So this skill must **never invent those values**.

## Commands

```bash
python scripts/clawhub_monitor.py <username>
python scripts/clawhub_monitor.py <username> --format json
python scripts/clawhub_monitor.py <username> --format text
python scripts/clawhub_monitor.py <username> --export skills.csv
python scripts/clawhub_monitor.py <username> --max-pages 50 --page-size 50
```

## Output

Returns:
- skill name
- display name
- owner handle
- latest version
- summary
- created / updated timestamps
- official / executes_code flags
- package URL hint

For installs/downloads/stars/reviews, return unavailable/null when not exposed by the public API.
