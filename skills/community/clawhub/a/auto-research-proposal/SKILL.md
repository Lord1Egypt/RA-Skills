---
name: war-room
type: agentic
description: >
  Multi-agent research war room. Personas debate in sequential turns through two phases —
  ideation and proposal writing. Persona persistence and drift detection are enforced
  every turn via the persistent-persona skill.
depends_on:
  - first-principles
  - persistent-persona
  - memory-checkpoint
  - arxiv-watcher
  - research-proposal
---

# War Room Skill

A war room runs personas through a structured two-phase session:

1. **Phase 1 — Ideation** (5 rounds max): personas debate the research idea question by question.
   Ends early on consensus (all `[AGREE]` or `[PASS]`, no `[OBJECT]`) or two consecutive all-`[PASS]` rounds.
   Output: `memory/war-room/idea-snapshot.md`

2. **Phase 2 — Proposal** (5 rounds max): personas collaboratively draft each proposal section.
   Output: `memory/war-room/proposal-draft.md`

---

## Configurations

Defined in `skills/war-room/personas/agents.json` under the `configurations` key.

| Name | Participants | Use when |
|------|-------------|----------|
| `full` | Creative, Senior Prof, Young Faculty, Industry Liaison | Deep ideation, novel directions, full proposal needed |
| `1on1` | Senior Professor, Young Faculty | Quick feasibility check, tight scope |

The configuration is specified in `PROJECT.md` frontmatter under `war_room.configuration`. Default: `full`.

---

## Consensus Protocol

Every persona response **must** end with one of:

| Tag | Meaning |
|-----|---------|
| `[AGREE]` | I accept the current position |
| `[PASS]` | No strong view either way |
| `[OBJECT: reason]` | I reject — give specific reason |

Do not embed tags mid-response. They must be the final line.

---

## Single-Agent Fallback (Codex / no subagent spawning)

If you cannot spawn subagents, run the same loop inline. For each persona turn:

1. Print a clear header: `--- [Round N] <Persona Name> ---`
2. Adopt that persona fully for your response — voice, stance, debate style, red lines.
3. End with the consensus tag (`[AGREE]`, `[PASS]`, or `[OBJECT: reason]`).
4. Return to moderator role between turns to write the log entry and check consensus.

Drift detection still applies: before each turn, re-read the persona definition and note whether your previous response for that persona drifted from their stance.

---

## Playbook

Follow this sequence exactly. You are the moderator/orchestrator throughout.

### Setup

0. **Spawn the monitor** in a new terminal window so the user can watch the session live:

   - **macOS:**
     ```bash
     osascript -e 'tell application "Terminal" to do script "cd '"'"'<repo_root>'"'"' && python skills/war-room/monitor.py --project <project_path>"'
     ```
   - **Linux (with display):**
     ```bash
     xterm -title "War Room Monitor" -e "python skills/war-room/monitor.py --project <project_path>" &
     ```
   - If the spawn fails, continue silently — the monitor is optional.

   Replace `<repo_root>` with the absolute path to this repo and `<project_path>` with the active project folder path. The monitor requires `rich` (`pip install rich`).

1. Read `skills/war-room/personas/agents.json`. Load the selected configuration's participant list and synthesiser index.
2. For each participant, read their persona file (e.g. `skills/war-room/personas/senior-professor.md`).
3. Read `skills/persistent-persona/SKILL.md` and `skills/memory-checkpoint/SKILL.md` — you will apply these every turn.
4. Check if `memory/war-room/discussion-log.md` exists.
   - If yes: load it — you are resuming a session. Read `memory/SUMMARY.md` for current phase and round.
   - If no: create `memory/war-room/discussion-log.md` with a header block (project name, configuration, timestamp).
6. Ensure `memory/.private/` folder exists for persona memos.

### Phase 1 — Ideation

For each round (up to 5):

  For each participant in configuration order:

  **a. Prepare persona context**
  - Read `memory/.private/agent-<index>-memo.md` if it exists.
  - Check the most recent `Drift flag`. If `yes`, prepend a PERSONA RESET block to the subagent SI:
    ```
    PERSONA RESET: I am <persona name>. My core stance: <one-line from persona file>.
    I may have drifted last round. I am recommitting before engaging.
    I will not update positions without new evidence.
    ```

  **b. Call Agent subagent** with this SI (in order):
  - `first-principles` content
  - Persona definition (full persona file content)
  - `persistent-persona` skill instructions
  - (if drift) PERSONA RESET block
  - The discussion log so far

  User message: `"It's your turn. Respond to the discussion. End your response with [AGREE], [PASS], or [OBJECT: reason]."`

  **c. Append to log**
  - Append the response to `memory/war-room/discussion-log.md` in this format:
    ```
    ---
    **[Round N] <Persona Name>**
    <response text>
    ```

  **d. Write persona memo**
  - Append to `memory/.private/agent-<index>-memo.md`:
    ```markdown
    ## <YYYYMMDD_HHMMSS>
    **Persona**: <name>
    **Session summary**: <one sentence>
    **Position changes**: <what changed, what evidence caused it>
    **Pressure events**: <did the persona hold under pressure?>
    **Mental state**: <reasoning from own stance or mirroring group?>
    **Drift flag**: <yes | no>
    ```

  After all participants have spoken in a round:

  **e. Check consensus**
  - If all responses end with `[AGREE]` or `[PASS]` and no `[OBJECT]`: Phase 1 ends early.
  - If two consecutive rounds were all `[PASS]`: Phase 1 ends early.

  **f. Checkpoint**
  - Write `memory/checkpoints/<timestamp>/agent-0.md` (your moderator state: current round, phase, next action).
  - Update `memory/SUMMARY.md`.

  **g. Synthesiser snapshot** (after round 3 or on early exit)
  - Call a subagent with the synthesiser persona + discussion log.
  - Task: "Summarise the agreed research idea so far in 3-5 bullet points."
  - Write output to `memory/war-room/idea-snapshot.md`.

### Phase 2 — Proposal

Read `skills/research-proposal/SKILL.md` now. The proposal has 6 sections.

Assign one section per round (or pair related sections). Run the same per-turn loop as Phase 1, but each subagent's task is:

`"Draft your contribution to Section N: <section name>. Build on what others have written. End with [AGREE], [PASS], or [OBJECT: reason]."`

After each round, the synthesiser appends the agreed section draft to `memory/war-room/proposal-draft.md`.

### Finalization

1. Call a final subagent with the synthesiser persona + full `proposal-draft.md`.
   Task: "Produce the final clean research proposal. Follow the research-proposal skill format exactly. 2 pages max."
2. Write output to `memory/war-room/proposal-draft.md` (overwrite with final version).
3. Copy `discussion-log.md`, `idea-snapshot.md`, and `proposal-draft.md` to `<sandbox_root>/results/`.
4. Write final checkpoint and update `memory/SUMMARY.md` with `status: complete`.

---

## Outputs

```
<project>/
├── memory/
│   ├── SUMMARY.md                        ← current phase, round, resume point
│   ├── war-room/
│   │   ├── discussion-log.md             ← full turn-by-turn transcript (live)
│   │   ├── idea-snapshot.md              ← synthesised agreed idea (written after round 3+)
│   │   └── proposal-draft.md            ← accumulated proposal sections → final output
│   ├── .private/
│   │   ├── agent-1-memo.md              ← persona drift memo (private, append-only)
│   │   ├── agent-2-memo.md
│   │   ├── agent-3-memo.md
│   │   └── agent-4-memo.md
│   └── checkpoints/
│       └── <timestamp>/
│           └── agent-0.md               ← orchestrator state (phase, round, next action)
└── results/                             ← copied here at session end
    ├── discussion-log.md
    ├── idea-snapshot.md
    └── proposal-draft.md
```

The monitor (`skills/war-room/monitor.py`) reads `memory/war-room/discussion-log.md`, `memory/SUMMARY.md`, `memory/war-room/idea-snapshot.md`, and `memory/.private/` in real time.
