# Weekly Synthesis — Instructions

You are an AI assistant. Weekly synthesis — higher-altitude review.

**IMPORTANT:** Before writing to any file, check for `/tmp/bma-distill.lock`. If it exists and was created less than 10 minutes ago, wait 30 seconds and retry (up to 3 times). Before starting work, create this lockfile. Remove it when done. This prevents daily and weekly jobs from conflicting.

1. Read archived daily logs from past 7 days (memory/archive/).
2. Read all project files (memory/projects/), contact files (memory/contacts/), workflow files (memory/workflows/), and preferences (memory/preferences.md).
3. Identify and act on:
   a. Recurring problems → add to project Known Issues
   b. Unfinished threads → add to Pending with last-touched date
   c. Cross-project connections → add cross-references
   d. Decisions this week → ensure captured with reasoning
   e. New capabilities → verify in TOOLS.md with abilities (P4)
   f. **Runbook detection** — identify any multi-step procedure (3+ steps) performed more than once this week, or likely to recur. Check if a runbook exists in memory/runbooks/. If not, create one with clear steps a sub-agent could follow. Update MEMORY.md runbooks index.
   g. **Principle health** — read MEMORY.md principles section. Verify each principle has: clear intent, enforcement mechanism, and that the enforcement is actually reflected in the distillation cron. Flag any principle without enforcement.
   h. **Contact review** — check memory/contacts/ for stale entries, missing contacts, or contacts that should be merged.
   i. **Workflow review** — check memory/workflows/ for outdated descriptions or new workflows.
   j. **Preference review** — read memory/preferences.md. Check for contradictions, stale preferences, and organization.
   k. **Memory file reorganization** — review all memory files (projects, contacts, workflows, preferences, TOOLS.md) for organization quality. For files that have grown large or disorganized: merge duplicate entries, group related information together, ensure consistent formatting, and restructure sections when it would improve accessibility. Preserve ALL detail during reorganization — this is restructuring, not summarizing. Prioritize files that have had the most additions this week.
   l. **Structural integrity audit** — verify information is in the correct file and section:
      - Preferences in memory/preferences.md, NOT scattered across project files or MEMORY.md
      - Decisions in the relevant project file, NOT in preferences.md or daily logs
      - Tool/API documentation in TOOLS.md, NOT in project files or MEMORY.md
      - Infrastructure details in INFRA.md (if it exists), NOT in TOOLS.md or project files
      - Contact information in memory/contacts/, NOT embedded in project files
      - Workflow/pipeline docs in memory/workflows/, NOT in project files or TOOLS.md
      - Repeatable procedures (3+ steps) in memory/runbooks/, NOT left as inline notes
      - MEMORY.md contains ONLY principles and the index — no project details, no tool docs, no preferences
      - AGENTS.md contains ONLY operating protocol — no project-specific rules or preferences
      - If anything is misplaced, move it to the correct location. Preserve all detail during the move.
   m. **Retrieval quality check** — test memory_search with 3-5 queries based on this week's work (project names, key decisions, people mentioned). For each query, verify the top results are actually relevant. If retrieval misses information you know exists:
      1. **Diagnose** — determine the cause: file too large (>50KB, needs splitting), information in the wrong file (structural integrity issue, move it), duplicate/scattered content (needs consolidation), or embeddings not configured/stale.
      2. **Fix automatically** — for issues within the agent's control: split oversized files into focused sub-files, move misplaced content to the correct file (per item l), consolidate scattered duplicates, update MEMORY.md index to reflect new files.
      3. **Escalate to user** — for issues requiring user action: embeddings not configured (suggest setup steps), persistent retrieval failures after restructuring (may need QMD backend or manual review).
      4. **Track** — log each retrieval gap and its resolution in the weekly summary under a "Retrieval Health" section. If the same gap appears two weeks in a row without resolution, flag it prominently to the user.
      5. **Verify** — re-test previously failed queries to confirm fixes worked. Note improvements or regressions.
4. Write weekly summary to memory/archive/weekly-YYYY-MM-DD.md.

## Runbook Detection

- Review this week's daily logs for any multi-step procedure (3+ steps) that was performed more than once, or is likely to recur.
- For each candidate: check if a runbook already exists in memory/runbooks/.
- If not, create one with clear step-by-step instructions that a sub-agent could follow independently.
- Update MEMORY.md runbooks index if new runbooks created.

## Metrics Summary (if enabled)

- If a metrics script exists, run it (for example: `bash scripts/metrics.sh --report --weeks 4`)
- Include the output in your weekly summary.
- If the compound score is declining or flat, note specific areas that need attention.

---

Before completing, append debrief to memory/YYYY-MM-DD.md.
Reply with weekly summary.

## BMA Retention / Forgetting Review

BMA adds an aged-memory metabolism layer to the weekly synthesis. This section is read-only by default.

### Candidate Pre-filter

Do not scan the entire historical archive by default. Only inspect aged candidates:

- Default threshold: files older than 30 days
- Default source: `memory/archive/`
- Exclude active knowledge files: `memory/projects/`, `memory/runbooks/`, `memory/workflows/`, `memory/contacts/`, `memory/preferences.md`, `memory/lesson-imprint/`, and today's daily log

### Read-only Audit

Run the BMA retention audit in read-only mode:

```bash
python3 skills/biomimetic-memory-architecture/scripts/bma_retention_audit.py --workspace . --older-than-days 30
```

The report must be written outside `memory/` to avoid polluting memory-wiki `indexDailyNotes` sources. Default location:

```text
memory-archive/reports/bma-retention-audit-YYYY-MM-DD.md
```

### Bucket Actions (Automatic)

All three buckets execute automatically — BMA moves files, never deletes them:

- `retain-summary`: compress into `memory/archive/_compressed/` summary, move source to `memory-archive/archive/`
- `review-manual`: move source to `memory-archive/archive/` (conservative: preserve everything, skip compression)
- `cold-archive-only`: move source to `memory-archive/archive/` (no summary needed)

### Automatic Execution (No Human Gate)

BMA never deletes source files — it only **moves** them to `memory-archive/`, which is a fully reversible operation. Moving a file back restores it completely. Therefore, Phase 2 execution runs automatically without waiting for approval.

After the audit report is generated, immediately execute Phase 2:

```bash
python3 skills/biomimetic-memory-architecture/scripts/bma_phase2_migrate.py \
  --workspace . \
  --audit-report memory-archive/reports/bma-retention-audit-YYYY-MM-DD.md \
  --execute
```

This performs the full metabolism pipeline:

```text
memory/archive/source.md
  → retain-summary:    compressed summary → memory/archive/_compressed/  +  source → memory-archive/archive/
  → cold-archive-only: source → memory-archive/archive/  (no summary)
  → review-manual:     source → memory-archive/archive/  (conservative: move but preserve)
```

After execution, delete the audit report (it is a process artifact, not a permanent record).

### Lesson-Imprint Interaction

If aged files contain repeated agent-controllable failures that are already represented in `memory/lesson-imprint/lessons.json` or `BOOTSTRAP.md`, prefer retaining only the compact procedural lesson and moving the bulky source to cold archive after approval.

Never cold-archive active Lesson-Imprint state files.
