---
name: debug-probe
version: 1.0.0
description: Hypothesis-driven runtime debugging with precise instrumentation. Use when debugging bugs, anomalies, or unexpected behavior where static code analysis is insufficient. 6-phase loop: hypothesize → instrument → reproduce → converge → fix → clean up. Triggers on: debug, diagnose, broken, bug, not working, unexpected behavior, investigate, root cause, probe.
---

# Debug Probe

## Quick Start

When you hit a bug that reading code can't resolve:

1. **Hypothesize** — Read source, generate 2-4 falsifiable hypotheses
2. **Instrument** — Insert minimal logging (2-4 points per hypothesis), tag `[DIAG_<topic>]`
3. **Collect** — Build → user reproduces → user exports logs
4. **Converge** — Match logs to hypotheses → confirm root cause
5. **Fix** — Minimal fix → verify with user
6. **Clean up** — Remove ALL instrumentation, confirm build passes

Never skip to fixing. Always clean up after.

## The 6 Phases

### Phase 1: Hypothesize

Read relevant source code. Generate 2-4 testable hypotheses:

```
[H1] Root cause may be X → if true, log would show Y
[H2] Root cause may be Z → if true, log would show W
```

Share hypotheses with user before touching code.

### Phase 2: Instrument

**Rules:**
- Only instrument to test hypotheses — no fishing expeditions
- Tag format: `[DIAG_<topic>]` (short topic like `auth`, `render`, `state`)
- 2-4 instrumentation points per hypothesis
- Mark ALL temporary code: `// DIAG: remove after debug` (adapt comment syntax to language)
- Set up a diagnostic buffer (pick from [TEMPLATES.md](TEMPLATES.md))

Use `diagLog('H1', 'key=val', ...)` — outputs to both console and an in-memory buffer so users can export all logs at once after reproducing the bug.

### Phase 3: Collect

1. Build & deploy
2. User reproduces the bug
3. User exports logs (dump function, console output, log file, etc.)
4. Group logs by hypothesis tag (`[DIAG][H1]`, `[DIAG][H2]`)
5. If expected paths aren't hit → is instrumentation on the right branch? → adjust and rebuild

### Phase 4: Converge

| Situation | Action |
|-----------|--------|
| Logs confirm a hypothesis | Confirmed root cause → Phase 5 |
| All hypotheses refuted | New hypotheses from log clues → Phase 2 |
| Insufficient data | More precise instrumentation → Phase 2 |

Max 2-3 iterations before escalating.

### Phase 5: Fix & Verify

1. Minimal fix targeting confirmed root cause
2. Build → user verifies fix works
3. Fix fails → keep key instrumentation, return to Phase 1
4. Fix works → Phase 6

### Phase 6: Clean Up

**Mandatory.** Search for `DIAG: remove after debug` and:
1. Remove all temporary instrumentation code
2. Remove all diagnostic imports
3. Remove diagnostic buffer file if no longer referenced
4. Build to confirm compilation passes
5. Tell user: instrumentation removed, only fix remains

## Anti-Patterns

- ❌ Skip hypotheses, jump straight to "fixing"
- ❌ Instrument 10+ points — precision beats coverage
- ❌ Dump entire objects — signal drowns in noise
- ❌ Forget Phase 6 cleanup — instrumentation rots
- ❌ Claim "done" without user verification
- ❌ Use raw `console.log` / `print` — use the diag buffer pattern
