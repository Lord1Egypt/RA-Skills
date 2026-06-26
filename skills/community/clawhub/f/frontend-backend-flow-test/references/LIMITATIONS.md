# Limitations

This skill is an **audit-first static analyzer** with optional live follow-up tooling.
Understand these limits before trusting a result too much.

## Static audit limits

### 1. Pattern-dependent extraction
The auditor only sees what its extractors can recognize.
If a project hides API calls behind unusual wrappers, generated SDK layers, or string-building helpers, coverage drops.

### 2. Dynamic paths reduce confidence
Template strings, concatenation, and computed routes can still be matched, but confidence is lower and some calls may remain ambiguous.

### 3. Hints are not full schemas
`query/body/auth` comparison is hint-based.
It can reveal likely drift, but it does not yet prove exact runtime serialization, validation, or response-shape correctness.

### 4. Response-side coverage is still limited
The current MVP is stronger on request contracts than on response contracts.
Indirect field usage and transformed response access may be missed.

### 5. Framework coverage is intentionally narrow
Current strength is frontend JS/TS/Dart patterns plus Spring-style backends and baseline Express routing.
This is not yet a universal contract analyzer.

### 6. Express support is useful but still shallow
Express extraction is strongest when routes are declared with recognizable `app/router` calls and mounted in the same file.
Cross-file router assembly, decorator wrappers, generated route registries, and highly dynamic middleware composition can still reduce confidence.

### 7. Laravel support is useful but still shallow
Laravel extraction is strongest when routes live in standard `routes/*.php` files and point to conventional controller actions.
Nested groups, route macros, package-provided registries, invokable classes, closures with complex request shaping, and custom FormRequest/resource transformations can still reduce confidence.

## Live mode limits

Live tooling is secondary and intentionally conservative.
It is useful only for narrow follow-up checks in safe environments.

Do not rely on it for:
- production write validation
- guaranteed rollback
- full user-flow verification
- comprehensive QA
- external side-effect containment
- replacing a real regression suite such as workspace-based API tests

## Confidence guidance

Prefer this interpretation model:
- `missing-backend-endpoint` / `method-mismatch`: usually the strongest signals
- `path-mismatch`: often useful, but verify prefixes and dynamic parameters
- `query/body/auth hint mismatch`: good investigation leads, not absolute proof
- `backend-only-endpoint`: may be genuine dead code or simply missed frontend extraction

## Recommended usage discipline

1. run audit first
2. fix or review high-severity findings
3. re-run audit
4. use live verification only for the unresolved or highest-risk paths
