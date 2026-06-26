# ClawHub Skill Monitor - Installation Guide

## What this skill does

This skill queries **public ClawHub skill metadata** for a given user (`ownerHandle`).

Reliable public fields today:
- skill name / display name
- owner handle
- latest version
- created / updated timestamps
- summary
- official flag
- executes-code flag

Not publicly exposed by the current ClawHub API:
- installs
- downloads
- rating / stars
- review count

This skill does **not** fabricate those missing metrics.

## Install

### Option 1: copy into OpenClaw skills directory
```bash
cp -r clawhub-skill-monitor ~/.openclaw/skills/
```

### Option 2: install from a packaged bundle
```bash
openclaw skills install clawhub-skill-monitor.skill
```

## CLI usage

```bash
cd ~/.openclaw/skills/clawhub-skill-monitor

# Table output
python scripts/clawhub_monitor.py <username>

# JSON output
python scripts/clawhub_monitor.py <username> --format json

# Text output
python scripts/clawhub_monitor.py <username> --format text

# CSV export
python scripts/clawhub_monitor.py <username> --export skills.csv

# Scan more public pages when needed
python scripts/clawhub_monitor.py <username> --max-pages 50 --page-size 50
```

## Recommended entrypoint

Use `scripts/clawhub_monitor.py` as the primary entrypoint.

The older helper/demo scripts in `scripts/` are historical artifacts and should **not** be used as the main published behavior reference.

## Output behavior

### Success with results
Returns one or more public skills for the target user.

### Success with zero results
The script honestly reports that no public skills were found **within the scanned public result window**.
That may mean:
- the user has no public skills,
- the user's skills were not reached within the current scan depth,
- or the public index changed.

### API/network failure
Returns an error JSON object in JSON mode, or a clear text error in CLI output.

## Notes

- ClawHub currently exposes public package metadata via public API endpoints.
- It does not currently expose installs/downloads/stars/reviews in the public package API used by this skill.
- If ClawHub adds those fields later, this skill can be extended.
