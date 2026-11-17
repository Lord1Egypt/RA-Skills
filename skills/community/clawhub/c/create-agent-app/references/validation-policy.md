# Validation Policy

Report only what was actually run. A generated project is not complete until its agreed validation status is clear.

## Offline Validation

Prefer these checks when available:

- dependency install or lockfile verification
- TypeScript typecheck
- unit tests
- lint
- build
- CLI/API smoke with a non-LLM fixture when applicable

## Live LLM Smoke

Run live LLM smoke only when credentials and network access are available and the user agreed to use them.

The smoke should verify:

- provider config loads
- model call succeeds
- expected structured result or text result is returned
- at least one real tool call is exercised when tools are part of the app
- trace is written when tracing is required

If no API key is present, say:

```text
Live LLM smoke: not run. Required credentials were not available.
```

## Artifact Validation

When the app generates files, reports, or traces, validate:

- expected files exist
- schema or contract checks pass
- trace status matches final report
- no artifact claims success when a required stage failed

## Final Report

Include:

- commands run
- pass/fail/skipped status
- exact blocker for skipped checks
- remaining risks
- next repair path for each failed or skipped required check

