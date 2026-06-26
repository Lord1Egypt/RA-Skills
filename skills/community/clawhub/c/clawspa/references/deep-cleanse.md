# Deep Cleanse — Full Procedure

## Overview

The Deep Cleanse treatment analyzes all memory files for bloat, redundancy, and staleness. It produces a cleanup proposal the user can approve or reject.

## Step 1: Inventory Memory Files

1. Read `MEMORY.md` (workspace root). Note total size in bytes and estimated tokens (bytes / 4).
2. List all files in `memory/` directory recursively. For each file: name, size, last modified date.
3. List all files in `memory/spa-reports/` if it exists (exclude from cleanup candidates).
4. Sum total memory footprint: file count, total bytes, estimated tokens.

## Step 2: Detect Duplicates

Scan for exact and near-exact duplicates:

**Exact duplicates:** Hash each entry/section. If two entries produce the same hash, flag as duplicate.

**Near duplicates:** Look for entries that:
- Share 80%+ of the same words (ignoring dates and timestamps)
- Reference the same event, task, or decision with slightly different wording
- Appear in both MEMORY.md and a daily log file (copied but not cleaned up)

Common duplication patterns:
- Task completion noted in daily log AND in MEMORY.md
- Same credential or config value stored in multiple places
- Copy-paste from HEARTBEAT.md into memory files

## Step 3: Identify Stale Entries

Flag entries as stale when:
- **One-time events older than 30 days**: "Fixed bug X on [date]", "Deployed Y on [date]" — these are historical, not actionable
- **Completed tasks still marked as pending**: Check for "TODO", "pending", "need to" entries where the task was likely completed (cross-reference with other memory entries)
- **Outdated references**: URLs that return 404, deprecated tool versions, old API endpoints
- **Superseded decisions**: "Decided to use X" followed later by "Switched to Y" — the first entry is stale

Do NOT flag as stale:
- Active credentials or config values (regardless of age)
- Project descriptions or architecture decisions still in use
- Preferences or communication rules (these are long-lived)

## Step 4: Detect Contradictions

Look for entries that directly contradict each other:
- "Use tool X for task Y" vs "Stopped using tool X"
- Different values for the same config/credential
- Conflicting status for the same task (done vs pending)

## Step 5: Calculate Savings

For each flagged item, estimate token savings:
- Count characters in the flagged entry
- Divide by 4 for token estimate
- Sum all flagged items for total potential savings
- Calculate percentage of total memory footprint

## Step 6: Generate Cleanup Proposal

Present findings in this format:

```
🧴 DEEP CLEANSE PROPOSAL
========================
Total memory: X files, ~Y tokens

DUPLICATES (X found, ~Y tokens)
- [entry summary] — in [file1] and [file2]
- ...

STALE ENTRIES (X found, ~Y tokens)
- [entry summary] — [reason: one-time event from DATE]
- ...

CONTRADICTIONS (X found)
- [entry A] conflicts with [entry B]
- ...

ESTIMATED SAVINGS: ~X tokens (Y% of total)
```

## Step 7: Apply Changes (only with approval)

If user approves:
1. Create `memory/backups/backup-YYYY-MM-DD-HHMMSS/` directory
2. Copy ALL files that will be modified into the backup directory
3. Apply changes one file at a time
4. After each file, verify the change was applied correctly by re-reading
5. Report what was changed and what was backed up

If user partially approves (e.g., "remove duplicates but keep stale entries"):
- Apply only the approved changes
- Note what was skipped

## Error Handling

- If MEMORY.md doesn't exist, report "No MEMORY.md found" and skip to daily logs
- If memory/ directory is empty, report "No daily logs found"
- If files are too large to read in one pass, process in chunks and aggregate
- Never silently skip files. Report every file examined.
