# Review Process Reference

Use this when a review is broad, high-risk, or ambiguous.

## Discovery

Identify:

- languages and frameworks
- package managers and lockfiles
- build/test commands
- application entry points
- routes/controllers/consumers/jobs
- database schemas and migrations
- messaging contracts
- auth/security boundaries
- observability setup

## Evidence Standards

Prefer findings backed by direct code evidence. Use lower confidence when a finding depends on production data, deployment configuration, middleware not present in the repository, or undocumented operational assumptions.

## Stable IDs

Within a run, assign IDs by category and order:

- `BUG-001`
- `SEC-001`
- `ARCH-001`
- `SMELL-001`
- `PAT-001`
- `PERF-001`
- `TEST-001`
- `OBS-001`

IDs only need to be stable within the execution folder. Do not reuse an ID for a different finding in the same run.

## Dedupe Rules

If the same root cause appears in many files, create one finding with representative locations and list affected files. If multiple risks share a location but have different impacts, split them.

## Reporting Empty Categories

If no material finding exists in a category, write:

```text
No findings in the reviewed scope.
```

Mention limitations if the scope was narrow.
