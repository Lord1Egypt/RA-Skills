# autoresearch-loop

A bounded modify-verify-decide loop for agents working toward a measurable goal.

You give it a goal, a metric, verification commands, scope, rollback rules, and an iteration cap. It makes one atomic change at a time, verifies the result, keeps improvements, discards failures, and stops when the approved contract says to stop.

This is not a silent background coding daemon. Foreground review is the default. Background or unattended operation requires explicit approval, a fixed scope, a rollback strategy, and an iteration cap.

---

## What it does

- Runs a tight modify-verify-keep/discard loop toward a measurable target
- Separates **Verify** (did the metric improve?) from **Guard** (did anything else break?)
- Requires an approved run contract before edits begin
- Keeps edits inside approved files/directories
- Uses version-control snapshots or commits so failures can be discarded cleanly
- Escalates intelligently: REFINE after 3 failures, PIVOT after 5, ask before external research unless pre-approved, soft blocker after repeated dead ends
- Extracts lessons after kept iterations and pivots
- Prevents context drift on long runs by re-reading instructions every 10 iterations
- Works for anything with a number: test coverage, type errors, lint warnings, performance, research quality, translation completeness

---

## Safety Model

Before the loop starts, the agent must confirm:

- goal, metric, baseline, and target
- exact verify and guard commands
- allowed edit scope and forbidden paths
- rollback strategy
- foreground or explicitly approved background mode
- iteration cap
- whether external search is allowed
- private-data boundary

The loop must stop instead of improvising when the metric cannot be measured, scope is unclear, guard files need changing, rollback is unsafe, or external research would expose private material.

---

## Installation

### OpenClaw

Add your workspace skills directory to `openclaw.json`:

```json
{
  "skills": {
    "load": {
      "extraDirs": ["/path/to/your/skills"]
    }
  }
}
```

Clone into that directory:

```bash
git clone https://github.com/LeoStehlik/autoresearch-loop.git /path/to/your/skills/autoresearch-loop
```

### Codex / Claude Code / other agents

Copy `SKILL.md` and the `references/` folder into your project's skills directory (`.agents/skills/autoresearch-loop/`), then invoke with `$autoresearch-loop`.

---

## Usage

Say what you want in one sentence:

```text
$autoresearch-loop
Reduce TypeScript `any` types in src/**/*.ts without breaking tests.
```

The agent will confirm a run contract before making edits:

1. Goal and target metric
2. Verify command
3. Guard command
4. Edit scope and forbidden paths
5. Rollback strategy
6. Foreground/background mode
7. Iteration cap
8. External research policy

The loop starts only after you approve the contract and say go.

---

## The Loop

```text
read contract + state + lessons
pick ONE hypothesis
make ONE scoped atomic change
snapshot or commit
run VERIFY
run GUARD
keep / discard / rework
log result
check escalation and safety gates
repeat only within approved cap
```

---

## Escalation Ladder

| Trigger | Action |
|---------|--------|
| 3 consecutive discards | REFINE - adjust within current strategy |
| 5 consecutive discards | PIVOT - fundamentally different approach |
| 2 PIVOTs without improvement | Ask before external research unless pre-approved |
| 3 PIVOTs without improvement | Soft blocker - stop and report to human |

A single successful keep resets all counters.

---

## What's Inside

```text
autoresearch-loop/
├── SKILL.md                          Core loop rules + decision protocol
└── references/
    ├── loop-protocol.md              Full iteration spec + results log format
    ├── pivot-protocol.md             REFINE/PIVOT/soft-blocker escalation
    └── lessons-protocol.md           Cross-run learning + lesson format
```

---

## Inspiration

Inspired by Karpathy's autoresearch and codex-autoresearch. Built as our own clean, agent-agnostic implementation.

---

## License

MIT - see [LICENSE](LICENSE)
