# Review and Handoffs

## Review-First Output

For review tasks, findings come before summary:
- rank by severity
- cite concrete files
- call out likely regressions and missing tests
- keep the overview brief

If there are no findings, say that explicitly and still note residual risk.

## PR-Ready Handoff

A good Codex handoff should answer:
- what changed
- what checks ran
- what failed or was skipped
- what assumptions remain open
- what the next safe step is

## Structured Final Output

When another system needs machine-readable output, use a schema:

```bash
codex exec --output-schema final-schema.json ...
```

This is better than post-processing vague prose after the fact.

## Recovery Handoff

When interrupted, leave a minimal checkpoint:
- repo and branch
- files touched
- commands that passed
- commands that failed
- next best move

That makes `resume` or human takeover possible without starting over.
