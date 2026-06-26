# Container Update Advisor — Setup Guide

## Table of Contents
1. [Quick Start](#quick-start)
2. [Full Pipeline](#full-pipeline)
3. [Configuration](#configuration)
4. [How Image Matching Works](#how-image-matching-works)
5. [Scheduling](#scheduling)
6. [Rate Limits](#rate-limits)
7. [Limitations](#limitations)

---

## Quick Start

```bash
cd ~/.openclaw/workspace/skills/container-update-advisor/scripts/

# Full pipeline: scan → check → fetch changelogs → report
python3 scan_containers.py \
  | python3 check_updates.py \
  | python3 fetch_changelog.py \
  | python3 format_report.py
```

Or save intermediate steps for debugging:

```bash
python3 scan_containers.py > /tmp/containers.json
python3 check_updates.py /tmp/containers.json > /tmp/updates.json
python3 fetch_changelog.py /tmp/updates.json > /tmp/changelogs.json
python3 format_report.py /tmp/changelogs.json > report.md
```

---

## Full Pipeline

| Script | Input | Output | Purpose |
|---|---|---|---|
| `scan_containers.py` | — | JSON | Running containers with image/tag info |
| `check_updates.py` | scan JSON | JSON | Docker Hub tag comparison, update status |
| `fetch_changelog.py` | update JSON | JSON | GitHub release notes per updated image |
| `format_report.py` | changelog JSON | Markdown | Prioritized report with risk flags |

---

## Configuration

### GitHub Token (optional but recommended)

GitHub's unauthenticated API allows 60 requests/hour. With a token: 5,000/hour.

```bash
export GITHUB_TOKEN=ghp_yourtoken
python3 scan_containers.py | python3 check_updates.py | python3 fetch_changelog.py | python3 format_report.py
```

Generate a token at: https://github.com/settings/tokens (no scopes needed for public repos).

### Docker Hub credentials

Not required. The Docker Hub v2 API is public for checking tags on public images. Private images are skipped gracefully.

---

## How Image Matching Works

### Tag parsing

The scanner parses image strings into components:

```
nginx:1.25.3              → namespace=library, repo=nginx, tag=1.25.3
myuser/app:2.0            → namespace=myuser, repo=app, tag=2.0
docker.io/myuser/app:2.0  → same as above
ghcr.io/org/app:1.0       → registry=ghcr.io (skipped — not Docker Hub)
```

### Version comparison

Tags are compared using semver-style parsing:
- `1.25.3` < `1.25.4` (patch)
- `1.25.3` < `1.26.0` (minor)
- `1.25.3` < `2.0.0` (major)
- Non-semver tags (e.g. `slim`, `alpine`, `edge`) are not compared

Tags pinned to `latest` are skipped — there's no way to know if `latest` changed.

### Why some containers are skipped

| Reason | What to do |
|---|---|
| Tag is `latest` | Pin to a specific version tag |
| Tag is a sha256 digest | Use a version tag instead |
| Registry is GHCR/ECR/etc. | Only Docker Hub is supported without auth |
| Private image | Image namespace is still checked; 401/403 = skipped |
| No versioned tags on Hub | Docker Hub may use non-semver tags only |

### GitHub source discovery

`check_updates.py` fetches the Docker Hub repository description and scans for `github.com/` links. If found, `fetch_changelog.py` uses that URL for the releases API. For official images (namespace=`library`), it tries `docker-library/{repo}` on GitHub.

---

## Scheduling

Run nightly via cron and save the report to the workspace:

```bash
# Edit crontab: crontab -e
0 7 * * * cd ~/.openclaw/workspace/skills/container-update-advisor/scripts && python3 scan_containers.py | python3 check_updates.py | python3 fetch_changelog.py | python3 format_report.py > ~/container-updates-$(date +\%Y-\%m-\%d).md 2>&1
```

Or save to Obsidian vault:

```bash
0 7 * * * cd ~/.openclaw/workspace/skills/container-update-advisor/scripts && python3 scan_containers.py | python3 check_updates.py | python3 fetch_changelog.py | python3 format_report.py > ~/.openclaw/workspace/vault/container-updates/$(date +\%Y-\%m-\%d).md 2>&1
```

---

## Rate Limits

| API | Unauthenticated | Authenticated |
|---|---|---|
| Docker Hub | ~100 req/hr (unofficial) | 200/hr with free account |
| GitHub | 60 req/hr | 5,000/hr with token |

The scripts insert delays between requests to avoid 429s. With many containers (>20), consider running during off-peak hours or setting `GITHUB_TOKEN`.

---

## Limitations

- **Only Docker Hub public images** are checked for updates. GHCR, ECR, GCR, and private registries are skipped.
- **Non-semver tags** (e.g. `focal`, `bullseye`, `latest-alpine`) cannot be compared.
- **Digest-pinned images** cannot be checked.
- **GitHub changelog** requires the Docker Hub image to link to a public GitHub repo, or the namespace to match a GitHub org/user.
- **Rate limits** may cause incomplete results if many containers are running. Set `GITHUB_TOKEN` for best results.
