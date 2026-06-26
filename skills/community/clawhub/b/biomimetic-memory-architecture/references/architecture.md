# BMA Architecture Reference

BMA includes the complete OpenCortex-style memory foundation and adds two biomimetic evolution layers:

1. **Retention / forgetting** — aged declarative memory is compressed, cited, and eventually moved to cold storage.
2. **Lesson-Imprint procedural learning** — repeated failures become compact safeguards instead of bulky narrative memory.

## Why This Exists

Default OpenClaw memory is a flat MEMORY.md that grows unbounded. Context fills up, compaction loses information, and the agent forgets what it learned. The OpenCortex foundation solves this with:

1. **Separation of concerns** — different files for different purposes
2. **Nightly distillation** — raw daily logs → permanent structured knowledge
3. **Weekly synthesis** — pattern detection across days
4. **Principles** — enforced habits that prevent knowledge loss (P0 for custom, P1-P8 managed)
5. **Sub-agent debrief loop** — delegated work feeds back into memory

BMA keeps that foundation and adds:

6. **Aged retention / forgetting** — old raw memory shrinks into compressed summaries and cold source archives
7. **Procedural learning** — repeated agent-controllable failures become Lesson-Imprint safeguards
8. **Wiki hygiene** — `memory/` remains the active memory source for memory-wiki; metabolized sources move to `memory-archive/`

## File Purposes

| File | Loaded at boot? | Purpose | Size target |
|------|-----------------|---------|-------------|
| MEMORY.md | Yes | Principles + index only | < 3KB target |
| TOOLS.md | Yes | Tool/API catalog with abilities | Grows with tools |
| INFRA.md | Yes | Infrastructure reference | Grows with infra |
| SOUL.md | Yes | Identity, personality | < 1KB target |
| AGENTS.md | Yes | Operating protocol | < 1KB target |
| USER.md | Yes | Human's preferences/profile | < 1KB target |
| BOOTSTRAP.md | Yes | Session startup checklist | < 0.5KB target |
| memory/projects/*.md | On demand / wiki source | Per-project knowledge | Any |
| memory/contacts/*.md | On demand / wiki source | Per-person/org knowledge | Any |
| memory/workflows/*.md | On demand / wiki source | Per-workflow/pipeline knowledge | Any |
| memory/preferences.md | On demand / wiki source | Cross-cutting user preferences by category | Any |
| memory/runbooks/*.md | On demand / wiki source | Procedures for sub-agents | Any |
| memory/lesson-imprint/*.json/md | Boot / procedural layer | Compact repeated-failure safeguards | Small, curated |
| memory/YYYY-MM-DD.md | Current day | Working log | Any |
| memory/archive/*.md | Via search / weekly review | Downranked historical logs | Any |
| memory-archive/** | Cold storage | Metabolized source files and BMA reports | Any |

## Baseline Runtime Stack

BMA is designed to work with:

- QMD search/indexing
- LCM / lossless-claw for lossless conversation recall
- active-memory for runtime recall
- memory-wiki with `indexDailyNotes=true` and `indexDreamReports=false`
- memory-core dreaming light/rem enabled; deep promotion disabled

Recommended memory-wiki bridge settings:

```json
{
  "indexDailyNotes": true,
  "indexDreamReports": false,
  "indexMemoryRoot": true,
  "followMemoryEvents": false
}
```

## Distillation Routes

The nightly cron reads daily logs and routes each piece of information:

| Information type | Destination |
|-----------------|-------------|
| Project work, features, bugs | memory/projects/{project}.md |
| New tool descriptions and capabilities | TOOLS.md (sensitive values → vault reference) |
| Infrastructure changes | INFRA.md (only when infra collection is enabled) |
| People and organizations mentioned | memory/contacts/{name}.md |
| Workflows and pipelines described | memory/workflows/{name}.md |
| Stated preferences and opinions | memory/preferences.md (categorized) |
| Decisions and architectural directions | Relevant project file or MEMORY.md index |
| New principles | MEMORY.md P0 section |
| Agent-controllable repeated failures | memory/lesson-imprint/lessons.json |
| Objective external/system errors | Daily/archive log only unless operationally reusable |
| User info and communication style | USER.md / memory/VOICE.md when enabled |
| Scheduled job changes | MEMORY.md jobs table |
| Repeatable procedures | memory/runbooks/ |

After distillation, processed daily logs move to `memory/archive/`. This is the first downranking step, not final forgetting.

## Preference Categories

Preferences in `memory/preferences.md` are organized by category:

| Category | Examples |
|----------|----------|
| Communication | "No verbose explanations", "Direct messages only" |
| Code & Technical | "Detailed commit messages", "Prefer TypeScript" |
| Workflow & Process | "Check for messages before pushing", "Batch commits" |
| Scheduling & Time | "Don't schedule before 9 AM", "Prefer async" |
| Tools & Services | "Use VS Code over Vim", "Prefer Brave over Chrome" |
| Content & Media | "720p minimum", "No dubbed content" |
| Environment & Setup | "Dark mode everywhere", "Dual monitor layout" |

Format: `**Preference:** [what] — [context/reasoning] (date)`

Preferences are auto-captured from conversation when the user says "I prefer", "always do", "I don't like", etc. Contradicted preferences are updated, not duplicated.

## Lesson-Imprint Procedural Memory

Lesson-Imprint is not a separate integration layer in BMA. It is BMA's procedural memory component.

It turns repeated agent-controllable failures into compact behavioral safeguards stored under:

```text
memory/lesson-imprint/lessons.json
memory/lesson-imprint/config.json
memory/lesson-imprint/BOOTSTRAP.md
```

Minimal lesson schema:

```json
{
  "key": "report_unverified_completion",
  "key_type": "behavior",
  "triggers": ["completion", "verification"],
  "mistake": "Reported completion before verifying the actual result.",
  "correct_action": "Before reporting completion, independently verify the actual result.",
  "count": 11
}
```

Rules:

- Daily distillation is the intended writer.
- Raw failures/corrections remain in daily/archive logs.
- Only repeated lessons are promoted into `BOOTSTRAP.md`.
- Inject `correct_action`, not the whole failure story.
- Never cold-archive active Lesson-Imprint state files.

This models procedural memory: repeated mistakes become habits/reflexes instead of remaining bulky episodic records.

## BMA Retention / Forgetting

OpenCortex-style archive is only downranking. BMA adds the next stage: aged forgetting.

Default retention flow:

```text
memory/archive/source.md
  → aged candidate filter (default >30 days)
  → value assessment
  → compressed active residue with citation
  → source moved to memory-archive/archive/source.md
```

Retention rules:

- Do not scan the full history by default.
- Start with files older than 30 days.
- Write audit reports outside `memory/`, under `memory-archive/reports/`.
- Do not move/delete/rewrite source files without explicit user approval.
- Keep source citations after compression.
- Prefer preserving lasting meaning over raw detail.

Suggested buckets:

| Bucket | Meaning |
|--------|---------|
| retain-summary | Keep a compressed active summary and cite the cold source |
| review-manual | Ambiguous; requires human or stronger-model review |
| cold-archive-only | Move to cold archive with no active residue after approval |

## Declarative vs Procedural Memory

BMA uses two complementary loops:

```text
Declarative memory:
raw archive → aged candidate filter → value assessment → compressed residue → cold source archive

Procedural memory:
repeated failure → lesson extraction → threshold promotion → compact bootstrap safeguard
```

Human-memory analogy:

- Old episodic details fade into compressed semantic memory.
- Repeated mistakes become procedural safeguards.
- Full details remain retrievable from cold records when needed.

## Compounding Effect

```text
Week 1:  Agent knows basics, asks lots of questions
Week 4:  Agent has project history, knows tools, follows decisions, remembers preferences
Week 12: Agent has deep institutional knowledge, patterns, runbooks, contact history
Week 52: Agent knows more about the setup than most humans would remember
```

The key insight: **daily distillation + weekly synthesis + decision/preference capture + Lesson-Imprint + aged forgetting** means the agent gets better while avoiding unbounded historical bloat.

## Common Customizations

### Adding delegation tiers
Edit MEMORY.md P1 to adjust which capability tier handles what complexity. P1 is model-agnostic and works with whatever models are configured.

### Changing distillation schedule
Use OpenClaw cron management to edit the Daily Distillation schedule.

### Adding custom principles
All custom principles go in P0 as sub-principles (P0-A, P0-B, P0-C, etc.). P1-P8 are managed by the memory architecture and should not be modified casually.

Before adding a principle, check whether the request is better suited as:

- preference
- decision
- runbook
- workflow
- Lesson-Imprint safeguard

### Write-ahead durability
When the user states a preference, makes a decision, gives a deadline, or corrects the agent, write it to the relevant memory file before composing the response. This prevents context loss if the session ends or compacts mid-conversation.

### Memory health monitoring
Weekly synthesis maintains memory quality through:

- Structural integrity audit
- Memory file reorganization
- Retrieval quality testing
- Stale content cleanup
- Runbook detection
- Lesson-Imprint validation
- BMA retention report review

### Multi-bot setups
Each bot can have its own BMA install. Share knowledge via:

- common git repo
- shared read-only reference docs
- primary bot propagation workflow
- carefully scoped memory-wiki sources

## Safety Model

Phase 1: read-only audit.  
Phase 2: compress and stage migration proposals.  
Phase 3: move source files to cold storage only after explicit approval.

Do not publish private memory examples, user IDs, emails, local paths, tokens, or real logs in public BMA templates.

## Attribution

BMA is inspired by and compatible with OpenCortex. OpenCortex is MIT licensed. Public BMA releases should preserve upstream attribution and clearly state which components are derived, adapted, or reimplemented.
