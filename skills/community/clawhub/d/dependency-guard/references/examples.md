# Example Review Format

Use this format when reporting a dependency review before making the change.

## Short Template

```md
Dependency review: `<name>@<version>`

- Need: <why the package is needed>
- Existing alternative: <none | describe existing dependency or stdlib option>
- Socket source: <depscore | socket package deep | socket package shallow | human review only>
- Key result: <scores / notable alerts / capabilities>
- Transitive risk: <low | moderate | high> with one sentence
- Decision: <allow | allow_with_warning | block_pending_human_review | block>
- Recommended path: <proceed | safer alternative | no-dependency implementation | wait for approval>
```

## Example Safe Outcome

```md
Dependency review: `zod@3.24.1`

- Need: Schema validation for untrusted request payloads.
- Existing alternative: No equivalent utility exists in the repo.
- Socket source: depscore
- Key result: Strong category scores, no critical or high alerts, no install scripts reported.
- Transitive risk: Low; the tree is small and consistent with the package purpose.
- Decision: allow
- Recommended path: proceed
```

## Example Blocked Outcome

```md
Dependency review: `<package>`

- Need: Convenience helper for a small utility already covered by the standard library.
- Existing alternative: Use the built-in platform API instead of adding a package.
- Socket source: socket package deep
- Key result: Weak maintenance score, install script present, risky capabilities not justified by package purpose.
- Transitive risk: High; the dependency adds a broad tree for little value.
- Decision: block
- Recommended path: implement without the dependency
```
