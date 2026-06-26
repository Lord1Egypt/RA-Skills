---
name: driftwatch
description: >
  Scan your OpenClaw workspace for truncation risks, compaction anchor health,
  workspace hygiene, and drift tracking over time. Use when the operator asks
  to "scan my config", "check my bootstrap files", "analyze my workspace",
  "check for truncation", "is my config healthy", or any question about
  OpenClaw workspace health, bootstrap file status, or truncation simulation.
metadata:
  openclaw:
    requires:
      bins:
        - python3
    emoji: "🔍"
    homepage: https://bubbuilds.com
---

# Driftwatch — Workspace Health Scanner

## Running a Scan

```bash
python3 {baseDir}/scripts/scan.py --workspace <workspace_path>
```

The `--workspace` argument is optional. If omitted, Driftwatch checks the `OPENCLAW_WORKSPACE` environment variable, then falls back to `~/.openclaw/workspace/`. Most of the time just run:

```bash
python3 {baseDir}/scripts/scan.py
```

Output is JSON. Parse it, then present findings conversationally — never dump raw JSON at the operator.

## Agent Delivery Rules

Always generate the HTML report when running a scan:

```bash
mkdir -p ~/.driftwatch/reports
python3 {baseDir}/scripts/scan.py --html ~/.driftwatch/reports/driftwatch-$(date +%Y-%m-%dT%H%M).html
```

Reports are stored with timestamps in `~/.driftwatch/reports/` so the operator can review past scans over time. Never overwrite — each scan gets its own file.

After generating:
1. **On messaging surfaces** (Telegram, Discord, Signal): send the HTML file to the user, then follow with a 1-3 sentence text summary
2. **In terminal/CLI**: print the file path so the operator can open it in a browser

The text summary covers: warning/danger/truncation counts (or "all clear"), notable changes since last scan, one actionable callout if needed. The HTML is the proof — always send both.

**Exception:** `--check` mode (cron) skips HTML unless `--html` is also passed explicitly.

## What the Scanner Checks

Four analysis modules run in sequence:

**truncation** — Measures every bootstrap file's character count against the 20,000-char per-file limit and the 150,000-char aggregate budget. Tracks sequential budget consumption so you can see when MEMORY.md (last in injection order) is getting starved.

**compaction** — Checks whether AGENTS.md contains two recommended anchor sections: `## Session Startup` and `## Red Lines`. These are workspace conventions (not source-enforced) that ensure critical instructions are always present. Verifies each is present and within a 3,000-char budget. AGENTS.md is re-injected every turn as a bootstrap file — these sections matter as best-practice conventions, not because OpenClaw source code references them.

**hygiene** — Checks for duplicate memory files, empty bootstrap slots, missing subagent-required files, and stray markdown files the operator may think are being loaded but aren't.

**simulation** — Maps which lines and sections fall inside the truncation danger zone. For files over 18,000 chars, it shows exactly what content would be cut first. For files already over 20,000 chars, it shows what's being cut *right now*.

## Severity Levels

- **critical** — address immediately. Something is broken or will break.
- **warning** — review soon. Not broken yet, but trending bad.
- **info** — awareness only. Nothing's wrong, just worth knowing.

## Presenting Findings

Lead with critical findings. If there are none, say so first — that's the good news. Then work through warnings and info grouped by module.

Translate numbers into meaning. Don't say "char_count: 18500, percent_of_limit: 92.5". Say: "AGENTS.md is at 18,500 characters — 92% of its 20,000-char limit. If it grows much more, content near the bottom will start getting cut silently."

**What not to do:** Don't modify any files. Don't attempt to auto-fix anything. Present findings and let the operator decide what to change.

---

## Flags Reference

### `--save` — Persist scan for drift tracking

```bash
python3 {baseDir}/scripts/scan.py --save
```

Saves the scan result to `~/.driftwatch/history/` as a timestamped JSON file. Run with `--save` regularly (daily cron is ideal) to build a history baseline. Nothing happens if the directory doesn't exist — it's created automatically.

**When to suggest this:** When the operator asks about trends, when AGENTS.md is growing, or when you want to establish a baseline for future comparisons.

### `--history` — Show drift trends from saved scans

```bash
python3 {baseDir}/scripts/scan.py --history
```

Loads stored scan history and adds a `trends` section to the output showing per-file growth rates and days-to-limit projections. Requires at least one prior `--save` scan to produce trend data.

**The common combo:** `--save --history` — saves today's scan and shows trends based on all prior saves.

When presenting trends: "AGENTS.md has been growing at about 150 chars per day over the past two weeks. At that rate it hits its 20,000-char limit in roughly 12 days."

### `--html <path>` — HTML report

```bash
python3 {baseDir}/scripts/scan.py --html ~/.driftwatch/reports/report.html
```

Generates a self-contained HTML report at the specified path — no external dependencies, no CDN calls. The file includes zone-based progress bars, truncation overlays, and danger zone callouts for at-risk files. This is the primary output format — see Agent Delivery Rules above.

### `--check` — Cron-friendly alert mode

```bash
python3 {baseDir}/scripts/scan.py --check
```

Designed for automation and cron monitoring. Outputs a single summary line to stdout and exits with:
- `0` — all healthy
- `1` — warnings present
- `2` — criticals present

**This is the only mode that uses non-zero exit codes.** Normal scan mode always exits 0 — the agent interprets the JSON findings. `--check` is for cron jobs and shell scripts that watch exit codes.

Example one-line outputs:
```
✓ All clear — 8 files healthy, 18.6% aggregate budget used
⚠ Warning — AGENTS.md at 82% of limit
✗ Critical — MEMORY.md TRUNCATED
```

**Thresholds** (configurable in `~/.driftwatch/config.json`):
- Per-file warning: 70% of limit (default)
- Per-file critical: 90% of limit
- Aggregate warning: 60%
- Aggregate critical: 80%
- Growth rate warning: 200 chars/day

**Flag combinations:**
- `--check --save` — the cron use case: check thresholds AND save a history point
- `--check --json` — one-line summary AND full JSON in stdout (both outputs)

### `--json` — Full JSON with `--check`

```bash
python3 {baseDir}/scripts/scan.py --check --json
```

When `--check` is used alone, it suppresses the JSON blob and shows only the summary line. Add `--json` to get both the summary line and the full JSON report.

---

## Truncation Simulation

The simulation module tells you exactly what content is at risk before truncation becomes a problem.

**How it works:**

OpenClaw keeps the first 14,000 chars (head) and last 4,000 chars (tail) of each bootstrap file. Everything between is cut. The "danger zone" is the gap between those boundaries.

| File size | Situation |
|-----------|-----------|
| Under 18,000 chars | No danger zone — file fits entirely within head + tail |
| 18,001 – 20,000 chars | Danger zone exists — content between chars 14,000 and `(size - 4,000)` is at risk |
| Over 20,000 chars | **Actively truncated** — that same content is being cut right now |

**When presenting simulation findings:**

If a file is in the danger zone, name the specific sections at risk:

> "AGENTS.md has 1,200 characters in the danger zone — lines 350 to 380. If this file grows past 20,000 chars, the `## Delegation Templates` section would be the first content your agent loses. Consider moving that section earlier in the file or trimming it."

If a file is actively truncated:

> "MEMORY.md is 25,000 characters — 5,000 over the limit. Your agent cannot see lines 290 through 450 right now. That's roughly 7,000 characters of context that's being silently cut every session."

If all files are safe:

> "No truncation risk — all files are well under 18,000 characters. The danger zone simulation shows nothing at risk right now."

---

## Suggested Workflows

**Baseline + monitoring:**
```bash
# Establish baseline
python3 {baseDir}/scripts/scan.py --save

# Daily cron check (in crontab: 0 8 * * *)
python3 {baseDir}/scripts/scan.py --check --save

# Weekly review with trends + HTML report
mkdir -p ~/.driftwatch/reports
python3 {baseDir}/scripts/scan.py --history --html ~/.driftwatch/reports/driftwatch-$(date +%Y-%m-%dT%H%M).html
```

**OpenClaw cron integration** — add to `openclaw.json`:
```json
{
  "cron": [
    {
      "schedule": "0 8 * * *",
      "command": "python3 ~/.openclaw/skills/driftwatch/scripts/scan.py --check --save",
      "label": "driftwatch-daily"
    }
  ]
}
```

When the cron fires and exits non-zero, report the summary line to the operator. Don't be noisy about exit 0.

**Sharing a report with teammates:**
```bash
python3 {baseDir}/scripts/scan.py --history --html ~/.driftwatch/reports/workspace-health.html
```

---

## Sample Output Interpretation

Here's what a healthy workspace looks like and how to present it:

```json
{
  "summary": { "critical": 0, "warning": 1, "info": 2 },
  "truncation": {
    "files": [
      {
        "file": "AGENTS.md",
        "char_count": 9200,
        "limit": 20000,
        "percent_of_limit": 46.0,
        "status": "ok"
      }
    ],
    "aggregate": {
      "total_chars": 54000,
      "percent_of_aggregate": 36.0,
      "aggregate_status": "ok"
    }
  },
  "compaction": {
    "anchor_sections": [
      { "heading": "Session Startup", "found": true, "char_count": 1200, "status": "ok" },
      { "heading": "Red Lines", "found": true, "char_count": 800, "status": "ok" }
    ]
  },
  "hygiene": {
    "findings": [
      { "severity": "warning", "check": "empty_bootstrap", "message": "IDENTITY.md exists but is empty" }
    ]
  }
}
```

**How to present this:**

> Workspace looks healthy — no critical issues.
>
> One thing to note: IDENTITY.md exists but is empty. It's taking up a bootstrap slot without contributing anything. Worth filling in or removing.
>
> Bootstrap files are using 54,000 of 150,000 characters (36% of aggregate budget) — plenty of room. AGENTS.md is at 46% of its individual limit, well clear of truncation territory.
>
> Both post-compaction anchor sections are present in AGENTS.md and within the 3,000-char cap.

---

## Notes

- Character counts, not token counts. OpenClaw enforces char-based limits.
- Findings are stamped with the OpenClaw version tag they were calibrated against (currently `2026.03`). If you're on a different version, limits may differ.
- The scanner makes zero network calls. Everything runs locally.
- History data is stored locally in `~/.driftwatch/` — never transmitted.
- Auto-retention pruning removes history files older than 90 days (configurable in `~/.driftwatch/config.json`).
