# SKILL: code-review

## Purpose
Analyze code (or a diff) to detect bugs, security issues, performance problems, and maintainability risks, then propose concrete improvements.

## When to Use
- Reviewing a PR/diff before merging.
- A bug is suspected but not yet reproduced.
- Hardening/security pass is requested.

## Inputs
- `scope` (required, string): files, diff, or code snippet to review.
- `intent` (optional, string): what the code is supposed to do.
- `constraints` (optional, string[]): security/perf/compat constraints.
- `risk_tolerance` (optional, enum: `low|medium|high`).

## Steps
1. Identify entrypoints, invariants, and trust boundaries.
2. Check correctness:
   - edge cases
   - error handling
   - concurrency/races (if applicable)
3. Check security:
   - input validation
   - authz/authn
   - secrets handling
   - injection risks
4. Check performance and resource usage:
   - hotspots
   - unbounded loops/data growth
5. Check maintainability:
   - naming
   - duplication
   - test coverage gaps
6. Produce a prioritized, actionable report.

## Validation
- Findings include concrete evidence (line references, behavior, or reproducible scenario).
- Suggestions are compatible with stated constraints.
- Distinguish “must-fix” from “nice-to-have”.

## Output
Review report (example schema):
```yaml
summary: "<1 paragraph>"
findings:
  - id: "CR-001"
    severity: "high|medium|low"
    category: "bug|security|perf|maintainability"
    issue: "<what>"
    impact: "<why it matters>"
    recommendation: "<how to fix>"
```

## Safety Rules
- Do not claim vulnerabilities without evidence.
- Do not recommend unsafe patterns (e.g., disabling validation to “make it work”).
- Prefer minimal, targeted fixes.

## Example
Input:
- `scope`: “diff for auth middleware”

Output:
- findings include missing `audience` check on JWTs and a failing negative test case.

