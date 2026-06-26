# ClawHub Skill Monitor - Design

## Goal

Provide a reality-based monitor for a ClawHub author's **publicly visible skill metadata**.

## Input
- ClawHub username / `ownerHandle`

## Output
Publicly available package metadata for that author's skills, including:
- skill name
- display name
- owner handle
- latest version
- summary
- created / updated timestamps
- official flag
- executes-code flag
- CSV / JSON / text export

## Explicit non-goals
The current version does **not** promise these fields because the current public API used by the skill does not expose them:
- installs
- downloads
- star rating
- review count

## Current data source

Primary public endpoints used by the repaired implementation:
- `/api/v1/packages?family=skill`
- `/api/v1/packages/search?...`
- `/api/v1/packages/{name}`

## Data strategy

Because the current public package list endpoint does not provide a reliable public ownerHandle filter for this use case, the script:
1. paginates public skill packages,
2. filters locally by `ownerHandle`,
3. returns matched public skills,
4. reports scan depth honestly.

## Main script

```bash
python scripts/clawhub_monitor.py <username>
python scripts/clawhub_monitor.py <username> --format json
python scripts/clawhub_monitor.py <username> --format text
python scripts/clawhub_monitor.py <username> --export skills.csv
python scripts/clawhub_monitor.py <username> --max-pages 50 --page-size 50
```

## Behavior design

### When matches are found
Return matched public skills and metadata.

### When no matches are found
Return an honest “not found within scanned public results” message, plus scan counters.

### When the API fails
Return a clear error instead of fake fallback data.

## File structure

```text
clawhub-skill-monitor/
├── SKILL.md
├── README.md
├── QUICKSTART.md
├── INSTALL.md
├── DESIGN.md
└── scripts/
    └── clawhub_monitor.py
```

## Release standard
This skill is publishable only as a **public metadata monitor**.
Any future claim about installs/downloads/stars/reviews must first be backed by a verified public or authorized API source.
