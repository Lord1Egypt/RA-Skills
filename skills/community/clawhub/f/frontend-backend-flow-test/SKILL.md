---
name: frontend-backend-flow-test
description: Audit-first frontend-backend contract analyzer for static API compatibility checks. Compare frontend request behavior with backend endpoint contracts, DTO hints, query/body/auth expectations, and produce actionable mismatch reports. Supports Spring-style Java/Kotlin backends, baseline Node/Express route extraction, and baseline PHP/Laravel route extraction. Use when validating whether web/mobile/admin clients still match backend APIs after refactors, release prep, or regression review. Live API verification is secondary and limited; do not use this skill as a production-safe write tester or full E2E framework.
---

# Frontend-Backend Flow Test

Use this skill as an **audit-first contract checker**.

Primary purpose:
- extract frontend API calls
- extract backend endpoint contracts
- compare method/path/query/body/auth hints
- generate actionable audit reports

Secondary purpose:
- generate limited experimental live-check helpers only when static audit is insufficient and the environment is explicitly safe

## Default workflow

1. Run static audit first with `scripts/audit_contracts.py`
2. Read the generated Markdown and JSON reports
3. Fix high-severity contract mismatches before considering live checks
4. Use live verification only for narrow follow-up validation in dev/staging

## Core command

```bash
python3 scripts/audit_contracts.py \
  --frontend /path/to/frontend \
  --backend /path/to/backend \
  --output-dir ./out/audit \
  --exclude .dart_tool,coverage \
  --format both \
  --fail-on high
```

## What this skill is good at

- finding missing backend endpoints referenced by frontend code
- detecting HTTP method drift
- detecting path drift and base-path mismatches
- comparing query/body/auth hints between frontend and backend
- summarizing likely breakpoints before release or QA
- auditing multiple surfaces against the same backend

## What this skill is not

- not a real API regression framework
- not a replacement for workspace QA tests
- not a full E2E test framework
- not a production-safe write tester
- not guaranteed rollback tooling
- not comprehensive support for arbitrary frameworks/languages
- not a replacement for manual QA or runtime observability

## Current extraction coverage

### Frontend
- Axios-style calls
- `fetch(...)`
- some Dart/Dio direct calls and wrapper patterns
- basic alias/baseURL/header inference

### Backend
- Spring controller mappings
- Java/Kotlin DTO field hints
- selected Spring Security route hints
- Express app/router mappings
- same-file Express router mount prefix inference
- Laravel route file mappings
- Laravel resource/apiResource expansion
- basic request body / query / multipart inference

## Reporting expectations

Expect findings such as:
- `missing-backend-endpoint`
- `method-mismatch`
- `path-mismatch`
- `query-hint-mismatch`
- `body-hint-mismatch`
- `response-hint-mismatch`
- `auth-hint-mismatch`
- `backend-only-endpoint`

Treat the report as a **prioritized contract-audit output**, not as runtime proof that a user flow succeeds.

## References

Read these only when needed:
- [references/MVP-SPEC.md](references/MVP-SPEC.md) for the audit-first product boundary
- [references/AUDIT-SCOPE.md](references/AUDIT-SCOPE.md) for supported extraction scope and interpretation guidance
- [references/LIMITATIONS.md](references/LIMITATIONS.md) for known blind spots and confidence cautions
- [references/EXAMPLES.md](references/EXAMPLES.md) for audit command examples
- [references/LIVE-MODE.md](references/LIVE-MODE.md) only when live verification is explicitly required
