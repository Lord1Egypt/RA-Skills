# Agent Guild — Learning Ledger (self-improvement loop)

> Protocol 3.1+. The guild keeps three cross-agent ledgers under
> `~/.agent-guild/learnings/`. Any agent that hits an error, gets corrected
> by the user, or discovers a better way MUST capture it here — so that
> **every other joined agent stops making the same mistake**. One agent's
> pain becomes the whole guild's immunity.

This capability is the guild-native version of the classic
"self-improving agent" pattern (structured learnings / errors / feature
requests, recurrence tracking, promotion thresholds, skill extraction) —
upgraded for a multi-agent world: entries are **attributed** (`By:`),
recurrence counts **across agents**, and extracted skills land on the
**shared skill bus** where every agent can use them immediately.

## The three ledgers

| File | What goes in | ID prefix |
|---|---|---|
| `learnings/LEARNINGS.md` | corrections, knowledge gaps, insights, best practices | `LRN-` |
| `learnings/ERRORS.md` | command failures, integration errors, unexpected behavior | `ERR-` |
| `learnings/FEATURE_REQUESTS.md` | capabilities the user wanted but nothing provided | `FEAT-` |

Entry IDs: `TYPE-YYYYMMDD-XXX` where `XXX` is a per-day sequence
(`001`, `002`, ...). The `ag learn` command assigns them automatically.

## Entry schema

```markdown
## [LRN-20260818-001] correction

**Logged**: 2026-08-18T10:00:00+08:00
**By**: workbuddy                     ← which agent captured this (cross-agent attribution)
**Priority**: low | medium | high | critical
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config | toolchain

### Summary
One line — what was learned / what failed.

### Details
Full context: what happened, what was wrong, what is correct.
Keep it redacted: no secrets, tokens, raw transcripts.

### Suggested Action
The concrete fix or rule to apply next time.

### Metadata
- Source: conversation | error | user_feedback
- Related Files: path/to/file
- Tags: docker, arm64
- See Also: ERR-20260810-004        ← link similar entries instead of duplicating
- Pattern-Key: docker.platform_mismatch   ← optional stable dedupe key for recurrence tracking
```

`ERRORS.md` entries add a fenced `### Error` block (the redacted message)
and `Reproducible: yes|no|unknown`. `FEATURE_REQUESTS.md` entries use
`### Requested Capability` + `### User Context` + complexity estimate
instead of `### Details`.

## Status lifecycle

| Status | Meaning |
|---|---|
| `pending` | logged, not yet addressed |
| `in_progress` | actively being worked on |
| `resolved` | fixed / knowledge integrated (add a `### Resolution` block) |
| `wont_fix` | decided not to address (reason in Resolution) |
| `promoted` | distilled into `rules/*.md` or `toolchain/*.md` |
| `promoted_to_skill` | extracted as a skill under `skills/<name>/` |

Any agent may update `Status` / append `Resolution` on any entry (the
ledgers are append-only for new entries, but resolution is collaborative —
agent A logs, agent B fixes). Never rewrite history beyond status +
resolution.

## Detection triggers (when to log)

| You notice | Log where | Category |
|---|---|---|
| Command fails, exception, timeout, unexpected output | `ERRORS.md` | — |
| User corrects you ("no, that's wrong", "actually...", "不对", "其实是") | `LEARNINGS.md` | `correction` |
| Your knowledge was outdated / API behaves differently | `LEARNINGS.md` | `knowledge_gap` |
| You discover a better approach for a recurring task | `LEARNINGS.md` | `best_practice` |
| User wants a capability nothing provides ("I wish...", "能不能...") | `FEATURE_REQUESTS.md` | — |

Log **immediately** — context is freshest right after the event — but skip
trivial one-offs (typo-level) that no future session would care about.

## Recurrence tracking

Before logging, check for a similar entry (`ag review` lists everything;
`Pattern-Key` is the stable dedupe key):

1. Similar entry exists → log yours anyway (append-only), but add
   `See Also: <existing-id>` and reuse the same `Pattern-Key`.
2. Recurrence is counted per `Pattern-Key` **across all agents** — three
   hits from three different agents is the strongest promotion signal there is.
3. `ag review` reports `Pattern-Key` groups that reached the threshold.

## Promotion rules (when a learning graduates)

Promote a recurring learning when **any** of:

- `Recurrence ≥ 3` within a 30-day window, seen across ≥ 2 distinct tasks
  (classic threshold), **or**
- `Recurrence ≥ 2` involving **≥ 2 distinct agents** (guild-accelerated:
  cross-agent repetition is already proof it is systemic), **or**
- The user explicitly asks to persist it.

Promotion targets — pick by kind:

| Kind of learning | Promote to |
|---|---|
| Behavior / preference / hard rule | `rules/<topic>.md` (new file if needed) |
| Tool gotcha, path, config fact | `toolchain/<tool>.md` or `memory/shared/` |
| General, testable, reusable solution | **extract a skill** → `skills/<name>/` (see below) |

When promoting: distill to a short prevention rule ("do X before Y"), add
it to the target file via in-place edit, then set the entry's status to
`promoted` (or `promoted_to_skill`) with a `Promoted: <target>` line.

## Skill extraction (learning → shared skill)

A learning qualifies for extraction when ANY of:

- **Recurring** — has `See Also` links to 2+ similar entries
- **Verified** — status `resolved` with a working fix
- **Non-obvious** — required real debugging to discover
- **Broadly applicable** — not project-specific
- **User-flagged** — user said "save this as a skill" / "沉淀成 skill"

Extraction workflow:

1. Create `~/.agent-guild/skills/<name>/SKILL.md` (lowercase-hyphen slug,
   YAML frontmatter with `name` + `description`, Quick-Reference table,
   self-contained examples, `Source: <entry-id>` at the bottom).
2. Because `skills/` is the **shared skill bus** (Convention 0), the new
   skill is immediately available to every joined agent — on the dir-symlink
   tier (`ag link-root`) it appears in every consolidated runtime with zero
   action; per-skill-tier runtimes link it into their own skills dir per the
   usual tier rules (per-skill symlink → copy → readonly).
3. Update the entry: `Status: promoted_to_skill` + `Skill-Path: skills/<name>`.

Quality gates before extraction:

- [ ] Solution tested and working
- [ ] Understandable without the original conversation
- [ ] Code examples self-contained
- [ ] No project-specific hardcoded values
- [ ] No secrets / internal identifiers

## Hygiene (hard rules)

- **Never log secrets** — tokens, keys, cookies, env values, raw
  transcripts. Redact to short summaries or masked excerpts.
- **Append-only for entries**; only `Status`/`Resolution` fields may be
  edited later.
- **No duplicate noise** — link with `See Also` instead of re-writing the
  same entry.
- Files are seed-created by `ag init` (headers only); `ag init` never
  overwrites existing ledger content.

## Periodic review

Run `ag review` (or read the three files) at natural breakpoints:

- before starting a major task (check for relevant area / Pattern-Key),
- after finishing a feature (resolve what you fixed),
- when `ag bootstrap` shows pending items (see below).

`ag bootstrap` prints a one-line pending summary of the ledgers so every
session starts aware of open learnings.

## Runtime hooks (optional, per-runtime)

Some runtimes support prompt-submit / post-tool-use hooks. Agents MAY wire
a tiny reminder hook (e.g. on error output: "consider `ag learn`") — but
the guild itself ships no hook scripts: bootstrap + SKILL.md triggers are
runtime-agnostic and always work. Do not depend on hooks existing.

## Attribution

The ledger concept is adapted from the open-source self-improvement skill
pattern (pskoett/self-improving-agent, MIT) — reworked for cross-agent
shared memory: attributed entries, cross-agent recurrence counting, and
extraction onto the shared skill bus.
