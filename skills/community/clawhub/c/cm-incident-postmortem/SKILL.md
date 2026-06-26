---
name: incident-postmortem
description: Generate structured, blame-free incident postmortem reports from logs, timeline data, and incident metadata. Produces root cause analysis, impact assessment, timeline reconstruction, lessons learned, and action items. Supports log parsing (syslog, JSON, Apache/Nginx, Python tracebacks), timeline JSON input, blame-free language checking, and multiple output formats (markdown, HTML, JSON). Use when asked to create a postmortem, write an incident report, document an outage, generate a post-incident review, analyze incident timeline, check postmortem language for blame, create RCA (root cause analysis), or produce an after-action report. Triggers on "postmortem", "incident report", "outage report", "post-incident", "root cause analysis", "RCA", "after-action", "blameless review", "incident review".
---

# Incident Postmortem

Generate structured, blame-free incident postmortem reports with timeline reconstruction, log analysis, and action item tracking.

## Quick Start

```bash
# Create a postmortem from scratch (fills in template sections)
python3 scripts/generate_postmortem.py --title "Database outage" --severity P1

# Parse logs to auto-extract timeline events
python3 scripts/generate_postmortem.py --title "API latency" --log /var/log/app.log --since 2h

# Load a complete incident from JSON
python3 scripts/generate_postmortem.py --from incident.json --output html -o postmortem.html

# Combine logs + manual timeline
python3 scripts/generate_postmortem.py --title "Deploy failure" --log /var/log/deploy.log --timeline events.json

# Check existing document for blameful language
python3 scripts/generate_postmortem.py --check-blame existing-report.md
```

## Features

1. **Log parsing** — Auto-detects syslog, JSON, Apache/Nginx, Python tracebacks, Docker, generic timestamped formats. Extracts errors, warnings, and notable events into a timeline.
2. **Timeline reconstruction** — Merges log-extracted events with manual timeline JSON. Sorted chronologically with event type labels (detection, action, escalation, resolution).
3. **Blame-free language** — Built-in checker scans for blameful patterns and suggests alternatives. Use `--check-blame` on any document.
4. **Severity classification** — P0 (critical) through P3 (low) with appropriate descriptions.
5. **Multiple outputs** — Markdown (default), HTML (styled), JSON (structured).
6. **CI-friendly exit codes** — 0 (clean), 1 (errors found), 2 (critical severity).
7. **Template sections** — Summary, impact, timeline, root cause, detection, resolution, lessons learned, action items.

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `--title` | required | Incident title |
| `--severity` | P2 | P0, P1, P2, or P3 |
| `--date` | today | Incident date |
| `--duration` | TBD | How long it lasted |
| `--summary` | — | Brief summary text |
| `--log` | — | Log file path (repeatable) |
| `--since` | all | Time filter for logs (1h, 24h, 7d) |
| `--timeline` | — | Timeline JSON file |
| `--from` | — | Load full incident from JSON |
| `--output` | markdown | Output format: markdown, html, json |
| `-o` | stdout | Output file path |
| `--check-blame` | — | Check file for blameful language |

## Workflow

### After an Incident

1. Gather logs: `--log /var/log/app.log --log /var/log/nginx/error.log --since 4h`
2. Generate draft: `python3 scripts/generate_postmortem.py --title "..." --severity P1 --log ... -o draft.md`
3. Fill in template sections (summary, root cause, impact, resolution)
4. Run blame check: `--check-blame draft.md`
5. Add action items and share

### From Structured Data

1. Create `incident.json` with full details (see `references/templates.md` for schema)
2. Generate: `--from incident.json --output html -o postmortem.html`

### Periodic Review

Use JSON output to track action item completion across multiple postmortems.

## References

- **templates.md** — Full JSON schema, timeline event types, blame-free language guide with replacements
