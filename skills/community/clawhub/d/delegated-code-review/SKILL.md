---
name: delegated-code-review
description: Perform a single review with a fresh, read-only subagent, then verify findings and apply accepted fixes.
license: MIT-0
---

# Delegated Code Review

## Review

1. Start one fresh subagent with `fork_turns: "none"` and `$review-agent`. The reviewer may inspect code, tests, and call sites, but must only review. Wait patiently for its conclusion; unless the reviewer is confirmed to be in an abnormal state, do not send prompts to rush or wrap up the review.
2. Ask the reviewer to focus on Critical, Important, and clearly worthwhile issues. Record Minor issues as non-blocking. Every finding must include:
   - Issue
   - File/line number
   - Reason
   - Recommendation
3. Close the subagent after its report. If there are no findings, only Minor findings, or all findings are not accepted, finalize. Otherwise, verify each finding yourself:
   - Record invalid or unaccepted findings as `Not accepted` with the reason.
   - If an implementation subagent owns the change, delegate accepted fixes to it; otherwise fix them yourself. In either case, rerun the relevant tests after each fix.

## Finalize

Summarize the implementation, findings and decisions, fixes, verification results, unverified items, and remaining risks.
