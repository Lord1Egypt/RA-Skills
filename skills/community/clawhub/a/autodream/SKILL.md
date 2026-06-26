---
name: autodream
description: >-
  Automatic memory consolidation for OpenClaw agents. Analyzes daily memory files,
  removes duplicates, prunes stale entries, normalizes dates, and builds a clean
  MEMORY.md index. Like REM sleep for AI memory. Triggers on "consolidate memory",
  "dream", "clean up memory", "organize memory", "memory maintenance".
metadata:
  openclaw:
    emoji: "🌙"
    requires:
      anyBins: ["node"]
---

# Autodream — Memory Consolidation

Consolidates scattered daily memory files into a clean, organized `MEMORY.md`.

## When to Use

- **Manually**: User says "consolidate memory", "dream", "clean up memory", "organize my memories"
- **Via heartbeat**: Periodically check if consolidation is needed (24h+ since last run AND 5+ new files)
- **After major events**: Big refactor, project changes, many new daily files

## Quick Start

```bash
# Check if consolidation is needed
node /path/to/openclaw-autodream/bin/autodream.js {{workspace}} --stats

# Run consolidation (dry run first!)
node /path/to/openclaw-autodream/bin/autodream.js {{workspace}} --dry-run --verbose

# Run for real
node /path/to/openclaw-autodream/bin/autodream.js {{workspace}} --verbose

# Force full reconsolidation
node /path/to/openclaw-autodream/bin/autodream.js {{workspace}} --force --verbose
```

Replace `{{workspace}}` with your actual workspace path (e.g., `~/.openclaw/workspace`).

## If Installed Globally

```bash
# npm install -g openclaw-autodream
autodream ~/.openclaw/workspace --stats
autodream ~/.openclaw/workspace --verbose
autodream ~/.openclaw/workspace --dry-run
```

## What It Does (4 Phases)

### Phase 1: Orientation
- Reads existing `MEMORY.md` (if any)
- Scans `memory/` for daily files
- Identifies files changed since last consolidation

### Phase 2: Gather Signal
- Extracts structured entries from each daily file
- Classifies into categories: People, Projects, Preferences, Technical Decisions, Events, Lessons
- Scores importance of each entry

### Phase 3: Consolidation
- Removes exact duplicates (hash-based)
- Removes fuzzy duplicates (similarity > 75%)
- Prunes stale entries (completed tasks, old debugging notes)
- Normalizes relative dates ("yesterday" → "2026-03-24")

### Phase 4: Prune & Index
- Enforces max line limit (default: 200 lines)
- Prioritizes by importance × recency
- Writes clean `MEMORY.md` with category sections
- Backs up previous `MEMORY.md` to `memory/.autodream-backups/`

## Heartbeat Integration

Add to your `HEARTBEAT.md`:

```markdown
## Memory Consolidation Check
- Run `autodream <workspace> --stats` to check if consolidation is needed
- If "Would trigger: ✅ yes", run `autodream <workspace> --verbose`
- Only run consolidation during quiet hours (not while human is actively chatting)
```

## Configuration

Create `.autodream.json` in workspace root to customize:

```json
{
  "maxLines": 200,
  "lookbackDays": 30,
  "categories": [
    "People & Relationships",
    "Projects & Work",
    "Preferences & Style",
    "Technical Decisions",
    "Important Events",
    "Lessons Learned"
  ],
  "preservePatterns": ["⚠️", "IMPORTANT", "NEVER", "ALWAYS"],
  "triggerThreshold": {
    "minHoursSinceLastRun": 24,
    "minNewFiles": 5
  }
}
```

## Safety

- **Non-destructive**: Always backs up existing `MEMORY.md` before modifying
- **Backups**: Stored in `memory/.autodream-backups/`
- **Reports**: Consolidation reports in `memory/.autodream-reports/`
- **Dry run**: Always available with `--dry-run`
- **Protected entries**: Entries with ⚠️, IMPORTANT, NEVER, ALWAYS are never pruned

## Output Format

```markdown
# Long-Term Memory
<!-- Last consolidated: 2026-03-25T17:00:00Z | Files processed: 31 | Entries: 47 -->

## People & Relationships
- **Bob Smith** — Team Lead test run passed (2026-03-25)

## Projects & Work
- **Acme Corp** — Q1 review: 30.1% margin, targeting 40% (2026-03-25)

## Preferences & Style
- Values precision and factual accuracy (2026-02-01)

## Technical Decisions
- Using Supabase + Vercel for Project Alpha (2026-03-18)

## Lessons Learned
- Always backup before modifying production data (2026-02-15)
```
