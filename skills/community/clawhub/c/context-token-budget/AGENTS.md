# AGENTS.md — context-token-budget

Machine-readable entry for AI agents.

## Purpose
Estimate tokens, enforce a budget, fail closed before overspend.

## Invocation
```bash
python scripts/budget.py <file-or-text> [--limit N] [--json]
```

## Output contract
- Structured JSON available via `--json` (fields: verdict, score, sha256_8, hits).
- Exit code: 0 = PASS, 1 = FAIL (fail-closed).

## Rules
- Static analysis only; never executes external commands.
- FAIL verdict requires human decision before proceeding.
- No placeholders in outputs.
