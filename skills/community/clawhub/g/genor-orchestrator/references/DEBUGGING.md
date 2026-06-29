# Debugging Guide

## Diagnose Protocol
1. Build feedback loop (failing test, curl, CLI, screenshot)
2. Reproduce the bug
3. Hypothesise (3-5 ranked causes)
4. Instrument (one variable at a time)
5. Fix + regression test
6. Cleanup debug logs

## Common Error Recovery
| Error | Fix |
|---|---|
| Build fails | Read error, fix, rebuild |
| Test fails | Read output, fix code |
| Package missing | `npm install` / equivalent |
| Git conflict | `git stash`, rebase, pop |
| No internet | Use local fallbacks |
| Model timeout | Retry, then fallback model |
| Rate limited | Wait, then retry with different model |

## Quality Gates
```
[Build passes] → [Tests pass] → [Lint clean] → [Types check]
```
If any fails → Diagnose → Fix → Retry.

For UI:
```
[Screenshot] → [Vision analysis] → [Fix issues]
```

Post-ship:
```
[Log session] → [Log decisions] → [Update STATE.md] → [Update roadmap]
```
