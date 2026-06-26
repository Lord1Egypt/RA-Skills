---
name: active-self-improvement
version: 1.2.0
description: Active self-improvement loop that reads learnings, errors, batch outputs, and memory — detects patterns — and UPDATES skills/protocols/behavior automatically. Use when the agent should get smarter without being prompted. Different from passive logging — this ACTS on what it learns. Triggers after Recorder at end of sessions, after batch processing, after project milestones, on explicit "improve" or "what have we learned" prompts, or on a weekly cron schedule.
---

# Auto-Improve

Reads logs, detects patterns, rewrites the playbook. Not passive logging — this ACTS on what it learns.

```
SCAN (read logs) ──► PROPOSE (specific edits) ──► APPLY (low-risk auto, high-risk flag)
```

## Input Sources

| Source | What It Contains |
|--------|-----------------|
| `.learnings/ERRORS.md` | What broke and how it was fixed |
| `.learnings/LEARNINGS.md` | Corrections, insights, knowledge gaps, batch outcomes |
| `workspace/OUTSTANDING.md` | Ranked ideas and opportunities |
| `memory/permanent/*.md` | Current knowledge state |
| `workspace/DELEGATION_PLAN.md` | Atom timing data (if delegation was used) |

## Step 1: SCAN

Detect:
- **Repeated errors** — same mistake 3+ times → needs a prevention rule
- **Repeated corrections** — user keeps fixing the same thing → behavior change needed
- **Emerging patterns** — 3+ items connecting → thesis forming
- **Stale knowledge** — facts in permanent memory contradicted by recent sessions
- **Unused wins** — high-value items that haven't been acted on

## Step 2: PROPOSE

For each detected pattern:

```
PROPOSAL: [short title]
EVIDENCE: [file#line references]
CHANGE: [exact edit — old text → new text]
RISK: [low/medium/high]
REVERSIBLE: [yes/no]
Pattern-Key: [hash(error+fix) for dedup]
```

| Pattern Type | Action | Target File |
|-------------|--------|-------------|
| Repeated error | Add prevention rule | relevant skill's `## Learned` section |
| Repeated correction | Update behavior guideline | `SOUL.md` or `AGENTS.md` |
| Emerging thesis | Write thesis + next steps | `OUTSTANDING.md` |
| Stale knowledge | Update the fact | `memory/permanent/*.md` |
| Unused win | Create ticket or reminder | `NEXT_TICKET.md` or cron |

## Step 3: APPLY

- **Low risk + reversible**: Apply immediately. Log the change.
- **Medium risk**: Apply but notify user on next interaction.
- **High risk**: Write to `OUTSTANDING.md` and wait for approval.
- **Dry-run mode** (`--dry-run`): Propose all changes but apply none. Output a report.

Use 3-occurrence threshold before proposing pattern-based changes. Track recurrence with `Pattern-Key` and `Recurrence-Count`.

## Error→Skill Feedback Loop

After SCAN, for each error in ERRORS.md:
1. Extract the `Context` column value
2. Match against skill names (fuzzy: "SiteBlitz CSS" → `webdev-sop`)
3. If match found and skill doesn't already have the fix in `## Learned`:
   ```markdown
   ## Learned
   - [date] [error summary] → [fix]. Source: .learnings/ERRORS.md#L[N]
   ```
4. Use `Pattern-Key: hash(error+fix)` to prevent duplicates

Skills self-heal: every failure improves the relevant skill.

## Delegation Feedback

After delegation plan completes:
1. Read atom timing data from DELEGATION_PLAN.md
2. Atom actual time > 2× estimated → flag estimation drift
3. Atom model upgraded (flash→sonnet) → update routing suggestion in MODEL_ROUTING_PROTOCOL.md
4. Append summary to `.learnings/LEARNINGS.md`
