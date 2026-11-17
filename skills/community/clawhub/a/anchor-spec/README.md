# anchor-spec

**Tiered project anchors for AI coding agents — right-size your project memory, then let it maintain itself.**

> A drop-in skill/plugin for Claude Code, OpenClaw, and any agent that reads Markdown instructions. Zero dependencies, one optional Python script.

[简体中文说明](./README.zh-CN.md)

---

## The problem it solves

AI agents lose project context between sessions. Existing fixes fall into two camps:

- **Memory banks** (e.g. Cline Memory Bank): every project gets a full set of context files, and the agent must re-read *all of them* at the start of *every* task. Works — until you have 6 projects, the files bloat, and nobody ever deletes anything.
- **Spec-driven frameworks** (e.g. GitHub's spec-kit): excellent at *deciding what to build before you build it*, but they don't maintain living project state during execution.

anchor-spec occupies the empty slot: **project memory as a lifecycle** — how much you record matches how big the project is, and an automated doctor keeps the whole thing from rotting.

## Three mechanisms, one causal chain

**1. Tiering — right-size the investment (entry point)**

| Tier | When | What it costs |
|------|------|--------------|
| **T0** | One-shot task, single session | Zero. No anchor. Just do the work. |
| **T1** | Might span sessions, still light | One SEED card, **≤10 lines** (goal / outputs / next step / update counter) |
| **T2** | Real project (any of 4 promotion signals fires) | Full anchor: a README capped at **150 lines** + `tasks/` |

Promotion signals are explicit (project name appears ≥3 times across sessions; >5 files; referenced by other projects; still active after 2 weeks). **Upgrade only, never downgrade** — memory grows with the project, not ahead of it.

**2. The three-layer information model — *why* the README dares to stay thin (the enabling layer)**

Files are split not by topic but by **how their content changes**:

```
L3  Snapshot    README.md (≤150 lines)     status → overwritten, map → incremental,
                                            background → frozen, news → rolling window
L2  Decisions   EVOLUTION.md                append-only. "What we chose and why."
                                            Never rewritten; corrections are new entries.
L1  Raw log     daily memory / changelog    append-only
```

The status section can be brutally overwritten *because* an append-only layer beneath it guarantees no history is lost. That single invariant is what keeps the anchor permanently thin and permanently fresh — no periodic "documentation cleanup weekends".

**3. Lifecycle automation — still useful half a year later (the moat)**

`anchor-doctor.py` (read-only by default) continuously:

- **flags anchors untouched for 30 days** with a cold-storage banner ("verify facts before resuming")
- **archives at 90 days**
- **distills finished task anchors after 14 days** — durable "why" decisions are promoted into EVOLUTION, the task file itself is deleted
- detects orphan outputs, README bloat, and index drift

Anchors are an **asset, not a compliance ritual**: things enter, things leave.

**Bonus: the resume funnel (read protocol = token protocol)**

Instead of "read everything before every task" (that's a burn-money protocol), recovery is a 4-step funnel: README status (30 seconds to locate yourself) → map section (pull only the files you need) → EVOLUTION (decision context) → raw-log archaeology (only if still missing detail).

## Quick start

```bash
git clone https://github.com/<you>/anchor-spec.git
# Claude Code / OpenClaw:
cp -r anchor-spec/* ~/.claude/skills/anchor-spec/   # or your agent's skills dir
# That's it. The next time you say "new project" or "continue", the skill takes over.
```

Manual mode (no agent needed): copy the templates from `references/templates.md` into your project and follow `references/rules.md`.

## How is this different from …?

**Cline / Roo Memory Bank?** Memory Bank splits files *by topic* (brief / context / progress), mandates re-reading all files every task, and has no deletion path — the files only grow, which is exactly why its popular derivatives stalled. anchor-spec splits *by rate-of-change*, right-sizes by tier, and has an automated exit path. If you love Memory Bank, anchor-spec is the version that doesn't rot.

**GitHub spec-kit?** Complementary, not competing. spec-kit governs *what to build* (spec → plan → tasks); anchor-spec governs *where the project stands while you build it*. They compose cleanly — spec-kit artifacts slot straight into the anchor's map section.

**mem0 / Letta?** Those are memory *infrastructure* (vector stores, retrieval). anchor-spec is a documentation *protocol* — plain Markdown your agent and your future self both read. Use both if you like; they don't overlap.

## What's in the box

```
SKILL.md               the agent instruction (tiering + lifecycle + resume funnel)
references/
  templates.md         SEED card / T2 three-layer README / 3 task-anchor templates
  rules.md             the layer invariants + INDEX + distillation rules
  quality.md           self-check checklists + failure-mode table
doctor/
  anchor-doctor.py     read-only lifecycle auditor (cold banners, distillation
                       candidates, orphans, bloat, drift)
LICENSE                MIT
```

## FAQ

**Does it require Claude Code or OpenClaw?** No. It's plain Markdown + one optional Python script. Any LLM agent that can read files can run it; humans can too.

**What if my project outgrows T1?** The skill defines four explicit promotion signals and the upgrade path (SEED folds into the README background section). You never "migrate" — you grow.

**Is the doctor destructive?** Never on its own. It reports and proposes; all writes are opt-in (`--doctor` flag, dry-run by default).

## License

MIT — use it, fork it, ship it. If it saves your agent's memory, a star helps others find it.
