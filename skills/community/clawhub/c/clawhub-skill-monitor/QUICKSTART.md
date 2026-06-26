# ClawHub Skill Monitor - Quick Start

## One-line summary
Query the public skills published by a ClawHub user and export their public metadata.

## Install
```bash
cp -r clawhub-skill-monitor ~/.openclaw/skills/
```

## Basic usage
```bash
# Default table output
python scripts/clawhub_monitor.py <username>

# JSON output
python scripts/clawhub_monitor.py <username> --format json

# CSV export
python scripts/clawhub_monitor.py <username> --export skills.csv

# Wider public scan if needed
python scripts/clawhub_monitor.py <username> --max-pages 50 --page-size 50
```

## Typical use cases
- list a user's public ClawHub skills
- export public skill metadata
- compare version changes over time
- track created/updated timestamps

## Important limitation
This skill currently does **not** provide:
- installs
- downloads
- rating / stars
- reviews

Reason: the current public ClawHub API used by this skill does not expose those metrics.

## Main script
| Script | Purpose |
|------|------|
| `clawhub_monitor.py` | Main real-API entrypoint |

## Status
Ready for real public-metadata queries.
