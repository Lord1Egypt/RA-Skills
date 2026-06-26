# Driftwatch

You wrote 25,000 characters in AGENTS.md. Your agent can only see 14,000 of them.

The truncation is invisible. Your agent doesn't know it's working with an incomplete picture of your instructions — and it won't tell you. It just silently misses the rules at the bottom of your file.

Driftwatch is an OpenClaw skill that checks your workspace for these problems before they cost you bad output.

---

## What It Checks

**Truncation** — Per-file and aggregate character counts against OpenClaw's bootstrap limits. Flags files where content is being cut off. Warning and danger callouts appear directly under each file's bar in the HTML report.

**Danger zone mapping** — For files approaching or exceeding the 20K limit, shows exactly which lines fall inside the truncation zone and what your agent *cannot see right now*.

**Compaction anchor health** — Checks whether AGENTS.md contains two recommended anchor sections (`## Session Startup` and `## Red Lines`). These are workspace conventions (not source-enforced) that ensure critical instructions are always present. Verifies each is present and within a 3,000-char budget.

**Hygiene** — Duplicate memory files, empty bootstrap slots, files you think are being loaded but aren't, and missing subagent files.

**Drift tracking** — Records scan results over time so you can see how fast your files are growing and how many days until you hit the limit.

**Cron alert mode** — Exit codes and one-line summaries designed for automated monitoring. Drop into crontab or CI pipelines.

---

## Install

```bash
openclaw skills install driftwatch
```

Or via ClawHub:

```bash
clawhub install driftwatch
```

Requires Python 3.9+. No other dependencies.

---

## Usage

Once installed, just say to your agent:

> "scan my config"

Also works: "check my bootstrap files", "analyze my workspace", "am I truncated", "workspace health check", "check for truncation".

Your agent runs the scanner and summarizes findings. Critical issues first, then warnings, then informational notes.

---

## HTML Report

Use `--html /path/report.html` to generate a shareable HTML report. It includes color-coded budget bars for every bootstrap file, inline truncation warnings, compaction health, hygiene findings, and trend data when history is available. The report works everywhere — including in-app viewers that don't run JavaScript.

Green = healthy. Amber = larger than typical. Red = approaching truncation. Files over 20K show a three-zone truncation view (HEAD 14K | cut content | TAIL 4K).

---

## Inline Truncation Warnings

The HTML report shows contextual warnings directly under each file's progress bar:

- **Warning (amber bar):** "Larger than typical — review for unnecessary content"
- **Danger (red bar, 18K–20K):** "Approaching truncation — trim now to avoid data loss"
- **Truncated (≥20K):** The bar transforms into a three-zone view showing HEAD 14K | ✂ cut chars | TAIL 4K, with "Lines X–Y are invisible to your agent right now"

---

## Drift Tracking

Every scan automatically records results so you can see how fast your files are growing over time. Run `--history` to surface trends:

The `--history` flag adds a `trends` section to the output:

```json
{
  "trends": {
    "scans_analyzed": 7,
    "files": [
      {
        "file": "AGENTS.md",
        "current_chars": 9200,
        "oldest_chars": 6800,
        "delta": 2400,
        "growth_rate_chars_per_day": 48,
        "days_to_limit": 224,
        "trend": "stable"
      }
    ]
  }
}
```

Your agent translates this into: "AGENTS.md has grown by 2,400 characters over the past week — about 48 chars per day. At that rate you have roughly 224 days before it hits the limit."

---

## Cron Integration

Drop Driftwatch into your daily cron for automated monitoring:

```bash
# In crontab (runs every morning at 8am)
0 8 * * * python3 ~/.openclaw/skills/driftwatch/scripts/scan.py --check --save
```

Exit codes:
- `0` — all healthy
- `1` — warnings present
- `2` — criticals present

One-line stdout output:
```
✓ All clear — 8 files healthy, 19% aggregate budget used
⚠ Warning — AGENTS.md at 82% of limit
✗ Critical — MEMORY.md TRUNCATED
```

**Note:** Non-zero exit codes are only produced in `--check` mode. Normal scans always exit 0 so agent-facing calls are never misread as script failures.

---

## Example Output

The scanner returns structured JSON. Here's the shape (abbreviated):

```json
{
  "summary": {
    "critical": 1,
    "warning": 3,
    "info": 2
  },
  "truncation": {
    "files": [
      {
        "file": "AGENTS.md",
        "char_count": 18500,
        "limit": 20000,
        "percent_of_limit": 93,
        "status": "warning"
      }
    ],
    "aggregate": { "percent_of_aggregate": 36, "aggregate_status": "ok" }
  },
  "compaction": {
    "anchor_sections": [
      { "heading": "Session Startup", "found": true, "status": "ok" },
      { "heading": "Red Lines", "found": false, "status": "critical" }
    ]
  },
  "simulation": {
    "files": [
      {
        "file": "AGENTS.md",
        "status": "at_risk",
        "danger_zone": {
          "start_char": 14000,
          "end_char": 14500,
          "chars_at_risk": 500,
          "sections_at_risk": [
            { "heading": "## QA Protocol", "line": 352, "chars_in_zone": 400 }
          ]
        }
      }
    ]
  }
}
```

Your agent translates this into plain language. You don't read JSON — you read: "AGENTS.md is at 93% of its limit and has content in the danger zone. Your Red Lines anchor section is missing entirely, that's a recommended convention for workspace health."

---

## Security

**This skill makes zero network calls.**

The scanner uses only Python standard library: `os`, `json`, `argparse`, `re`, `datetime`. No network requests, no external services, no data leaves your machine.

Verify yourself:

```bash
grep -rn 'import requests\|import urllib\|import http\|import socket' scripts/
```

That command should return nothing.

**What Driftwatch reads:**

| File | Why |
|------|-----|
| `AGENTS.md` | Truncation risk, compaction anchor health |
| `SOUL.md` | Truncation risk |
| `TOOLS.md` | Truncation risk |
| `IDENTITY.md` | Truncation risk |
| `USER.md` | Truncation risk |
| `HEARTBEAT.md` | Truncation risk |
| `BOOTSTRAP.md` | Truncation risk |
| `MEMORY.md` | Truncation risk, checks for duplicate memory files (MEMORY.md vs memory.md) |

History data (`~/.driftwatch/`) is stored locally and never transmitted.

---

## Built By

Dan and Bub (and a small AI team). Two people solving the same problem we kept running into ourselves.

Source: [github.com/DanAndBub/driftwatch-skill](https://github.com/DanAndBub/driftwatch-skill)

---

## License

MIT-0 — do whatever you want with it.
