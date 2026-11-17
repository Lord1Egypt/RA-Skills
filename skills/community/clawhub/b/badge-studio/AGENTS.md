# AGENTS.md — badge-studio

Machine-readable entry for AI agents.

## Purpose
One-command badge generator, LGD VERIFIED style.

## Invocation
```bash
python scripts/badge_studio.py --label LGD --score 90/100 [--color 2563eb] [--out out.svg]
```

## Output contract
- Structured JSON available via `--json` (fields: verdict, score, sha256_8, hits).
- Exit code: 0 = PASS, 1 = FAIL (fail-closed).

## Rules
- Static analysis only; never executes external commands.
- FAIL verdict requires human decision before proceeding.
- No placeholders in outputs.
