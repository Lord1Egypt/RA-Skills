---
name: container-update-advisor
description: Check running Docker containers for newer image versions and generate a prioritized update report. Fetches release notes and flags breaking changes vs safe updates. Use when asked about container updates, docker updates, outdated containers, update check, what needs updating, are my containers up to date, or any request to review Docker image versions.
---

# Container Update Advisor

Check all running Docker containers against Docker Hub for newer versions, fetch changelogs, and output a prioritized markdown report with risk flags.

## Scripts

All scripts live in `scripts/` relative to this file. Run from that directory.

| Script | Purpose |
|---|---|
| `scan_containers.py` | List running containers + image tags (outputs JSON) |
| `check_updates.py` | Query Docker Hub for newer versions (stdin/file → JSON) |
| `fetch_changelog.py` | Fetch GitHub release notes for updated images (stdin/file → JSON) |
| `format_report.py` | Render prioritized markdown report (stdin/file → stdout) |

## Full Pipeline

```bash
python3 scan_containers.py \
  | python3 check_updates.py \
  | python3 fetch_changelog.py \
  | python3 format_report.py
```

To save intermediate output for debugging, pass each script's output as a file argument to the next:
```bash
python3 scan_containers.py > /tmp/c.json
python3 check_updates.py /tmp/c.json > /tmp/u.json
python3 fetch_changelog.py /tmp/u.json > /tmp/ch.json
python3 format_report.py /tmp/ch.json
```

## Risk Assessment Logic

- **Major version bump** → 🔴 review first
- **Minor version bump** → 🔴 review first (may have API changes)
- **Changelog mentions "breaking"** → 🔴 review first
- **Patch bump only, no breaking keywords** → 🟢 safe to update

## What Gets Skipped

- Containers using `latest` tag (no version to compare)
- Digest-pinned images (`sha256:...` tags)
- Non-Docker Hub registries (GHCR, ECR, etc.)
- Private images (401/403 → skipped gracefully)
- Non-semver tags (e.g. `alpine`, `focal`, `slim`)

## GitHub Token (Optional)

Set `GITHUB_TOKEN` env var to increase GitHub API from 60 → 5,000 req/hr:
```bash
export GITHUB_TOKEN=ghp_yourtoken
```

## Reference

See `references/setup-guide.md` for scheduling, rate limits, and how image matching works.
