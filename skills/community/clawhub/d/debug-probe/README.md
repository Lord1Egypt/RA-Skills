# Debug Probe — Hypothesis-Driven Runtime Debugging

A Claude Code agent skill for systematic debugging. When reading code isn't enough to find a bug, Debug Probe guides you through a 6-phase loop: **hypothesize → instrument → reproduce → converge → fix → clean up**.

## How It Works

```
[Hypothesize] → [Instrument] → [Collect] → [Converge] → [Fix] → [Clean Up]
     ↑                                                         │
     └────────────────── if fix fails ─────────────────────────┘
```

1. **Hypothesize** — Read source, generate 2-4 falsifiable hypotheses (not guesses)
2. **Instrument** — Insert 2-4 precise log points per hypothesis, tagged for cleanup
3. **Collect** — Build, reproduce the bug, export buffered logs
4. **Converge** — Match log evidence to hypotheses, confirm or refute
5. **Fix** — Minimal fix targeting the confirmed root cause
6. **Clean Up** — Remove ALL instrumentation, verify build passes

## Installation

```bash
# Clone the skill
git clone https://github.com/YOUR_USERNAME/debug-probe.git

# Install to Claude Code (project-level)
cp -r debug-probe .claude/skills/

# Or install globally
cp -r debug-probe ~/.claude/skills/
```

Or install directly:

```bash
npx skills add YOUR_USERNAME/debug-probe -g -y
```

## What's Included

| File | Purpose |
|------|---------|
| `SKILL.md` | Main skill file — 6-phase workflow and rules |
| `TEMPLATES.md` | Diagnostic buffer code templates for TypeScript, Python, and Go |

## When Claude Uses This Skill

The skill triggers automatically when Claude encounters:
- Bug reports, crashes, or unexpected behavior
- "Debug this", "diagnose", "investigate", "why is X broken"
- Situations where static code reading can't find the root cause

## Example

```
User: The login button does nothing in production but works fine locally

Claude (using Debug Probe):
  [H1] API URL mismatch between envs → log baseUrl and resolved endpoint
  [H2] Auth token not persisted in prod → log token presence and expiry

  *instruments 3 points, user reproduces, exports logs*

  Logs show: [DIAG][H1] baseUrl=https://api.prod.example.com /login
             [DIAG][H2] token=null

  → H2 confirmed. Root cause: token storage key differs between envs.
  → Fix: align storage key. Verified. Cleaned up.
```

## Anti-Patterns (What NOT to Do)

- ❌ Skip hypotheses, jump straight to "fixing"
- ❌ Sprinkle 10+ log points — 2-4 per hypothesis is the sweet spot
- ❌ Dump entire objects into logs — `key=value` pairs only
- ❌ Leave instrumentation code after fixing — Phase 6 is mandatory
- ❌ Claim "fixed" without user verification

## License

MIT
