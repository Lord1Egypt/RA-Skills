# Improve (Self-Improving Loop)

Analyze session episodic data (mistakes, hook/skill behavior, repeated patterns) and improve the system.

## When to Use

- `/claudify improve` — direct invocation
- `/cleanup run` Step 2 — automatic as part of session cleanup

## Workflow

### A. Retrospect (Mistake Analysis)

Scan conversation for mistake signals and record to feedback memory + failed-attempts.md.

**Signals**:

| Signal | Example |
|--------|---------|
| User correction | "no, not that", "you didn't even verify?" |
| Wrong judgment | Model declared absent, guessed separate issue |
| Ignored artifacts | Existing plan/research files not checked |
| Repeated mistake | Same correction 2+ times |
| Rule violation | Performed prohibited action from rules |

**Per mistake**:
1. Analyze root cause (Why 1-3 minimum)
2. Draft feedback memory entry (rule + Why + How to apply)
3. Collect for Phase 2 AskUserQuestion

**FA Prune**: After recording, if failed-attempts.md has 5+ sections, run [fa-prune.md](../cleanup/fa-prune.md) automatically.

**Skip condition**: No mistakes/corrections in conversation.

### B. Automation Review (Hook + Skill Check)

#### Hook Review

1. Collect registered hooks from settings.json
2. **File existence check**: Extract script paths → verify files exist → classify missing as "ghost hooks"
3. Check each hook's session behavior:
   - Triggered + acted on → "OK"
   - Triggered + **ignored** → "Ignored" (most critical)
   - Triggered + error → record error
   - Not triggered → "Not triggered"
   - File missing → "Ghost"
4. **Ignored output detection**: Search for `<skill-trigger>`, `BUILD_COMPLETED`, `AUTO_AGENTIFY_CANDIDATE:` markers
5. Summary report (immediate output):

```
**Hook summary**: 16 registered / 10 OK / 6 not triggered / 0 ignored / 0 error
```

**Skip condition**: None — always run if any hooks registered.

#### Skill Check

1. Collect skills invoked via `Skill()` during session
2. Post-execution self-heal checklist per skill:
   - Did trigger fire correctly?
   - Was correct topic selected?
   - Was procedure complete? (no manual correction needed?)
   - Were outputs complete?
3. Malfunctions → collect for Phase 2 AskUserQuestion

**Skip condition**: No skills invoked, or all skills worked correctly.

### C. Pattern Detect (Automation Candidate Discovery)

**Always run — no skip.**

1. Analyze conversation context for automatable repeated patterns
2. On candidate discovery:
   - Maps to existing rule/skill → suggest upgrade in Phase 2
   - **New pattern that fits nowhere → invoke `/skill-kit route`** → auto-chain to upgrade/writer
3. Collect candidates for Phase 2 AskUserQuestion

## Ralph Mode

**Detection**: see SKILL.md "Ralph Mode" — `.ralph/` directory + `RALPH_LOOP=1` env var, both required.

A-C: detect + record to `.ralph/improvements.md` only. No direct modifications.

## Phase 2 Integration

This topic does NOT call AskUserQuestion directly. All findings are returned to the caller (cleanup run.md) for batch Phase 2 confirmation.

**Return format** (internal):
```
{
  retrospect: [{ label, description }],
  hooks: { summary, issues: [{ label, description }] },
  skills: [{ label, description }],
  patterns: [{ label, description, needsRoute: bool }]
}
```
