# Forgejo Pull Request Review Workflow

This reference assumes `FORGEJO_URL` and `FORGEJO_TOKEN` are already set.

This workflow also requires a local git clone and a working `git` binary. If the
required bins, env vars, or `fj` setup are missing, return to `SKILL.md`
prerequisites, readiness checks, or troubleshooting before proceeding.

Use this workflow when the user asks for a review of a Forgejo pull request.

## Review goal

Prioritize behavioral risk over style. Focus first on security, correctness,
breaking changes, test gaps, and performance regressions. Treat readability and
convention issues as secondary unless they hide a real defect.

## Workflow

1. Inspect the current worktree before checking out the pull request.

```bash
git status --porcelain
```

If the worktree is dirty, warn the user before switching branches.

`fj pr checkout` will fail on uncommitted changes, so do not treat this as a
soft warning only.

2. Check out the pull request.

```bash
fj pr checkout <number>
```

3. Determine the actual base branch of the pull request.

Prefer `fj pr view <number>` if it exposes the base branch clearly. Otherwise use
the API:

```bash
curl -sS \
  -H "Authorization: token $FORGEJO_TOKEN" \
  -H "Accept: application/json" \
  "$FORGEJO_URL/api/v1/repos/$OWNER/$REPO/pulls/<number>" | jq -r '.base.ref, .head.ref, .head.sha, .mergeable, .draft, .merged'
```

The examples in this skill use the `Authorization: token ...` form. Forgejo also
accepts bearer-style authorization headers.

4. Compute the merge base against the real base branch.

```bash
BASE_BRANCH=<base-branch>
BASE_COMMIT=$(git merge-base HEAD "$BASE_BRANCH")
```

5. Inspect the diff.

Overview:

```bash
git diff --stat "$BASE_COMMIT"..HEAD
```

Per file:

```bash
git diff "$BASE_COMMIT"..HEAD -- path/to/file
```

If the diff is large, review file by file.

6. Analyze the changes using the review criteria below.

7. Post the review.

Global comment:

```bash
fj pr comment <number> "<review body>"
```

Some PR commands can infer the PR number from the current branch, but keeping the
number explicit is safer for review workflows.

Inline comments, if needed:
- Use `POST /repos/{owner}/{repo}/pulls/{index}/reviews`
- See `references/api-cheatsheet.md`
- Use `new_position` for added lines and `old_position` for removed lines when needed
- `COMMENT` reviews need a body or inline comments; `REQUEST_CHANGES` needs a body

8. Keep the final action separate:
- Post comments by default
- Approve only if the user explicitly asks for approval
- Merge only if the user explicitly asks for merge

Note: `forgejo-cli` currently exposes pull-request comments and merge flows, but
not a full approval-review command surface in the documented PR subcommands. This
skill keeps approval posting in the API/reference path because approval and merge
must remain conceptually separate.

## Review priorities

Prioritize findings in this order:

| Priority | Area | What to look for |
|---|---|---|
| 1 | Security | Injection, auth bypass, secret exposure, SSRF, XSS, path traversal, unsafe permission changes |
| 2 | Correctness | Nil or null access, wrong conditions, race conditions, broken error paths, resource leaks |
| 3 | Breaking changes | API contract drift, schema changes, config or env changes, backward-incompatible behavior |
| 4 | Tests and observability | Missing coverage, missing edge cases, broken assertions, absent logging or metrics around risky paths |
| 5 | Performance and operations | N+1 queries, quadratic behavior, blocking I/O, large allocations, retry storms, bad timeouts |
| 6 | Maintainability | Oversized functions, unclear ownership, duplicated logic, naming or comment issues that hide risk |

## Severity model

Use these severity labels in the final review:

| Severity | Meaning | Typical action |
|---|---|---|
| Blocking | Likely bug, security risk, data loss, or breaking change | Do not approve; ask for changes |
| Important | Real weakness or missing safety net, but not clearly blocking | Call out explicitly; approval depends on user intent and risk tolerance |
| Minor | Quality improvement with low immediate risk | Keep concise and avoid drowning out higher-risk findings |

If you are not sure a finding is real, lower confidence in the wording instead of
presenting speculation as fact.

## Language-specific hot spots

If the diff includes these languages, pay extra attention to:

- Go: `if err != nil`, goroutine leaks, `defer` ordering, nil handling
- JavaScript or TypeScript: async error handling, unhandled promises, XSS in templates, unsafe casts
- Python: mutable default arguments, exception specificity, resource management, typing gaps
- Rust: `unwrap()` or `expect()` in unsafe contexts, ownership mistakes, `unsafe` blocks
- C# or VB.NET: null handling, `IDisposable`, `async void`, deferred LINQ behavior

## Output format

Use this review structure when posting a summary comment:

```markdown
## Code Review - PR #<number>

**Base:** `<base branch>` <- `<head branch>`
**Files changed:** <count>
**Lines:** +<added> / -<removed>

### Summary
- <1-2 bullets on overall risk and scope>

### Blocking findings
- `<file>:<line>` - <description, risk, and concrete fix direction>

### Important suggestions
- `<file>:<line>` - <description>

### Minor improvements
- `<file>:<line>` - <description>

### Positive notes
- ...

### Verdict
**Recommendation:** Request Changes | Comment | Approve
**Why:** <1-2 sentences>
```

Only recommend `Approve` when no blocking issues remain and the user explicitly
asked for approval.

## Large diff strategy

If the diff exceeds roughly 500 changed lines:

1. List changed files with `git diff --name-only "$BASE_COMMIT"..HEAD`
2. Review business logic files first
3. Review tests next
4. Review config and docs last
5. Consolidate findings into one final review comment
6. If time or context limits prevented full coverage, say which files were not deeply reviewed

## Common pitfalls

- Reviewing style instead of behavior
- Assuming the base branch is `main` without checking PR metadata
- Missing removed-line comments that require `old_position` instead of `new_position`
- Approving by default instead of keeping approval separate from comments
- Overstating certainty when the evidence is incomplete
