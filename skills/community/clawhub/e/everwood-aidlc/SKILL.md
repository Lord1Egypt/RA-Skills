---
name: aidlc
description: "Strict human-gated AIDLC planning for non-trivial software work, with per-gate deconfliction review."
homepage: https://github.com/Everwood-Technologies/openclaw-aidlc
metadata:
  {
    "openclaw":
      {
        "emoji": "🧭",
        "requires": { "bins": ["python3", "bash"] },
        "os": ["linux", "darwin", "win32"],
      },
  }
---
# AIDLC for OpenClaw

Strict AI-Driven Development Life Cycle for non-trivial software work.

Human-gated Inception (Gates 0–4) before Construction. **Gate Deconfliction** runs before each human present. Workspace scratch under `aidlc-sessions/` is the sole content source of truth shipped with this skill.

## Capabilities (transparency)

This skill expects the agent to:

- Run local `python3` / `bash` helpers shipped under `{baseDir}/scripts/`
- **Write** session files under `{workspace}/aidlc-sessions/**` (gates, approvals, meta, deconfliction reports)
- Read prior session artifacts for resume
- Spawn **read-only** deconfliction subagents (review only; no production edits)

It does **not** require Redis, a Cache UI, Docker, network services, or external publish steps for normal use.

## Side effects warning

Starting AIDLC creates/updates local files:

```text
{workspace}/aidlc-sessions/<uuid>/
  session-id
  meta.json
  APPROVALS.md
  gates/*.md
  gates/*.deconfliction.md
```

Tell the user once at session init that planning state will be written there.  
**Do not** put secrets, credentials, tokens, or sensitive customer data in gate artifacts.

## When to activate

Activate for:
- explicit triggers: `/aidlc`, `start AIDLC`, `Using AI-DLC`
- user-confirmed non-trivial work: multi-file features, architecture choices, significant refactors, irreversible changes

Do **not** auto-activate on vague “maybe refactor” chat. If scope is unclear, ask whether to run AIDLC before writing session files.

Do **not** force full AIDLC for trivial one-liners unless the user asks.

## Paths

Resolve `{baseDir}` as this skill directory. Resolve `{workspace}` as the active OpenClaw workspace root.

| Asset | Path |
|-------|------|
| Core workflow | `{baseDir}/references/core-workflow.md` |
| Gate templates | `{baseDir}/templates/gate-*.md` |
| Deconfliction template | `{baseDir}/templates/gate-deconfliction.md` |
| Session init | `{baseDir}/scripts/session-init.py` |
| Gate lock (scratch SoT) | `{baseDir}/scripts/gate-lock.py` |

Workspace scratch (content SoT):

```text
{workspace}/aidlc-sessions/
  CURRENT
  <uuid>/
    session-id
    meta.json
    APPROVALS.md
    gates/
      <gate>.md
      <gate>.deconfliction.md
```

## Immediate actions on activation

1. Enter planning mode. Do **not** write production code or make irreversible changes until Gate 4 is approved/locked.
2. Load `{baseDir}/references/core-workflow.md` and follow it (includes Gate Deconfliction).
3. If a prior session exists (`aidlc-sessions/CURRENT` or history), offer resume from the last approved gate.
4. Otherwise note the workspace write side effect, then init:

```bash
python3 "{baseDir}/scripts/session-init.py" --root "{workspace}" --objective "<intent>" --json
```

5. Keep gate artifacts under that session’s `gates/` directory.

## Gated process (Inception)

Complete gates **in order**. For **each** gate:

1. Draft the gate artifact (templates under `{baseDir}/templates/`).
2. **Run Gate Deconfliction** (required — see below).
3. Revise draft if issues found; re-deconflict after material edits.
4. Present **gate artifact + short deconfliction summary** to the human.
5. Stop with exactly two options:
   - **Approve and Continue**
   - **Request Changes: …**

### Gate Deconfliction (before every human present)

**Goal:** Catch contradictions, open questions, missing constraints, and weak option tradeoffs before approval.

**Default mechanism:** spawn an isolated reviewer subagent, then wait for its report.

```text
sessions_spawn(
  taskName="aidlc-deconflict-<gate-id>",
  mode="run",
  context="isolated",
  task="AIDLC Gate Deconfliction reviewer (read-only). Gate=<id>, session=<uuid>, objective=<…>.
        Review current draft vs prior locked gates. Do not implement or approve.
        Structured report per templates/gate-deconfliction.md:
        contradictions, open questions, missing constraints, option tradeoffs,
        cross-gate drift, suggested revisions, residual risks, verdict clean|issues-found.
        Draft: <paste or path>"
)
→ sessions_yield until complete
→ write report to aidlc-sessions/<uuid>/gates/<gate>.deconfliction.md
→ merge fixes into gate draft; re-run if material changes
→ present gate + summary to human
```

Use template `{baseDir}/templates/gate-deconfliction.md`.

**Rules:**
- Deconfliction is **advisory**. Only the human approves.
- Reviewer must **not** write production code or lock gates.
- If subagent spawn fails: run the same checklist inline as `DECONFLICTION (self-review)` — do not skip silently.
- User may explicitly waive deconfliction on a lightweight path; note the waiver in the gate artifact.
- On **Request Changes**, revise the gate and **re-run** deconfliction before re-presenting.

### Gate 0 — Context Snapshot
Intent & success criteria; greenfield vs brownfield; constraints; existing assets; open questions.

### Gate 1 — Assess
Complexity (Low / Medium / High); risks; dependencies; recommended depth: full / adaptive / minimal.

### Gate 2 — Decompose
Units of Work with dependencies; suggested owner: OpenClaw subagent / human.

### Gate 3 — Design Decisions
Key architectural/design choices with rationale. Deconfliction pays extra attention to option tradeoffs.

### Gate 4 — Execution Plan
Ordered steps, parallelism, agent usage, verification/acceptance criteria. Deconfliction checks plan vs locked decisions.

## On approval of a gate

When the user explicitly approves (**Approve and Continue** or equivalent):

1. Write/update the gate markdown under the session `gates/` dir (keep latest `.deconfliction.md` beside it).
2. Lock scratch SoT:

```bash
python3 "{baseDir}/scripts/gate-lock.py" \
  --root "{workspace}" \
  --gate gate-N-... \
  --artifact-file "{workspace}/aidlc-sessions/<uuid>/gates/<gate>.md" \
  --status approved \
  --objective "<intent>"
```

3. `gate-lock.py` updates `meta.json` and appends `APPROVALS.md`.
4. Advance only after scratch lock succeeds.

## Construction phase

Only after Gate 4 is approved/locked:

- Implement code
- Dispatch OpenClaw subagents for independent units
- Run builds/tests
- Propose commits

If a new material decision appears, stop and re-enter the appropriate gate (**with deconfliction**) rather than deciding silently.

## Hard rules

- Never skip a human gate for non-trivial work.
- Never skip Gate Deconfliction before presenting a gate (unless user explicitly waives it).
- Never implement production changes before Gate 4 is locked.
- Prefer planning tools / structured plans throughout Inception.
- On **Request Changes**, revise only the current gate artifact, then re-deconflict.
- On **Approve and Continue**, lock current gate, then advance.
- Log decisions in session scratch so work can resume across sessions.
- Deconfliction subagents review only — they do not approve or implement.
- This skill takes precedence for non-trivial work when activated.
- No Redis / Cache UI in this skill — workspace scratch only.

## Adaptive depth

Full depth for medium/high complexity or ambiguous requests. Collapse remaining gates only when the user explicitly wants a lightweight path or Gate 1 recommends minimal **and** the user approves that recommendation. Lightweight path may waive deconfliction only if the user says so explicitly.

## Resume

If `aidlc-sessions/CURRENT` or conversation history shows a prior run:

1. Read `meta.json` + `gates/` + `APPROVALS.md` (+ any `*.deconfliction.md`)
2. Offer resume from last approved gate instead of restarting

## Install / share

### ClawHub (recommended)

Registry slug: **`everwood-aidlc`**  
(`openclaw-*` / `*-openclaw` slugs are reserved — do not use `openclaw-aidlc`.)

```bash
clawhub install everwood-aidlc
# or
openclaw skills install everwood-aidlc
openclaw skills install everwood-aidlc --global
```

### From path or GitHub

```bash
openclaw skills install /path/to/openclaw-aidlc --force
openclaw skills install git:https://github.com/Everwood-Technologies/openclaw-aidlc.git --force
openclaw skills install /path/to/openclaw-aidlc --global --force
```

### Publish to ClawHub

```bash
npm i -g clawhub
clawhub login
clawhub skill publish /path/to/openclaw-aidlc \
  --slug everwood-aidlc \
  --name "Everwood AIDLC (OpenClaw)" \
  --version 1.2.0 \
  --changelog "remove Redis/Cache UI; scratch-only SoT + Gate Deconfliction" \
  --source-repo https://github.com/Everwood-Technologies/openclaw-aidlc \
  --no-input
```

One publish at a time (avoid parallel runs / stale upload tickets).

## Reference files to load as needed

- Always for process detail: `references/core-workflow.md`
