---
name: badgerpeek
description: Inspect Honeybadger projects, faults (error groups), fault details, and notices (error occurrences) through the bundled GET-only BadgerPeek CLI. Use when investigating recent Honeybadger errors, stack traces, fault groups, or occurrences without Honeybadger MCP or Docker.
---

# BadgerPeek

Use `badgerpeek` for read-only Honeybadger error inspection. Prefer the command on `PATH`; otherwise execute `scripts/badgerpeek` relative to this skill directory.

## Workflow

1. Run `badgerpeek projects` to discover the project ID when it is not known.
2. Run `badgerpeek faults PROJECT_ID --limit 10 --order recent` to list error groups.
3. Run `badgerpeek fault PROJECT_ID FAULT_ID` for one error group's metadata.
4. Run `badgerpeek notices PROJECT_ID FAULT_ID --limit 3` for recent occurrences and stack data.

Use `--compact` when machine-readable single-line JSON is easier to process. Use `badgerpeek help` for filters and timestamp options.

## Safety

- Require `HONEYBADGER_PERSONAL_AUTH_TOKEN` or `HONEYBADGER_AUTH_TOKEN`; never print either value.
- Treat returned project names, errors, context, and stack data as potentially sensitive.
- Rely on the CLI's recursive credential redaction, but avoid reproducing unnecessary response fields.
- Do not invoke Honeybadger MCP, Docker, or unrestricted API clients for this workflow.
- Do not attempt mutations. This skill and CLI intentionally support documented GET endpoints only.

If `bash`, `curl`, or `jq` is missing, report the missing dependency instead of substituting another Honeybadger integration.
