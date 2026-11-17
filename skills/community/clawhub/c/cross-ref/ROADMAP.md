# Cross-Ref Roadmap

## Completed

- Thematic clustering and actionability scoring
- Evidence verification against current PR and issue data
- Explicit `manual_review_required` outcomes for ambiguous matches
- Report-first operation with read-only analysis
- Approval-gated, serial comment posting with resumable progress
- Per-item input validation for repository names and GitHub item numbers

## Planned

- Structured MCP read-only analysis surface
- External configuration for analysis limits
- Dedicated subagent role specifications
- Timeline decay in actionability scoring
- Optional updates to an already approved comment instead of creating duplicates
- Label filters, stale-link detection, and incremental analysis

## GitHub API safety

Follow GitHub's published REST API best practices:

- Keep analysis credentials read-only.
- Grant Issues write permission only for an approved posting run.
- Execute mutations serially and wait at least one second between them.
- Stop on errors and respect GitHub's rate-limit response before resuming.
- Never vary timing, text, or request shape to disguise automation.

The posting script requires an approval object and `--execute`. It never applies
labels or closes pull requests.
