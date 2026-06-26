---
name: aport-complete
description: >
  Verify a completed task against your APort passport's deliverable contract
  before marking it done. Enforces acceptance criteria, summary requirements,
  test status, and reviewer checks deterministically. Use this before calling
  any task complete.
license: Apache-2.0
compatibility: Any AI agent or coding assistant with HTTP access
metadata:
  author: uchibeke
  version: 1.0.0
  tags: ai-agent, deliverable, task-completion, aport, quality-gate, passport
---

# /aport-complete — Verify Before Done

Your APort passport defines what you must deliver before a task is complete.
This skill enforces that contract. Do not mark any task done without running this first.

## When to use this skill

- Before telling a user "I'm done" or "it's complete"
- Before closing a task, ticket, or GitHub issue
- Before opening a PR and considering work finished
- Before handing off to another agent
- Any time you would otherwise call a task complete

## Prerequisites

You must have an APort passport with a deliverable contract.

If you don't have one, create a passport first:
- **Web:** https://aport.id
- **CLI:** `npx aport-id`
- **Agent skill:** Read https://aport.id/skill and follow the instructions

You need `APORT_AGENT_ID` in your environment. This is returned when you create
your passport and saved to `aport-passport.json`.

## Step 1 — Compile your completion context

Before calling the API, gather:

| Field | Required | How to get it |
|-------|----------|---------------|
| `task_id` | Yes | The task/ticket/issue identifier |
| `output_type` | Yes | `code`, `document`, `analysis`, `plan`, `data`, or `other` |
| `summary` | If passport requires it | Write a clear summary of what you did |
| `tests_passing` | If passport requires it | Run your test suite, report result |
| `author_agent_id` | If reviewer required | Your own `APORT_AGENT_ID` |
| `reviewer_agent_id` | If reviewer required | The `agent_id` of the reviewing agent |
| `criteria_attestations` | Always | One entry per criterion in your passport |
| `output_content` | If scan_output enabled | Your full output (for pattern scanning) |

## Step 2 — Build your attestations

Your passport defines acceptance criteria as a list of descriptions.
Each criterion maps to a `criterion_id` — the description slugified to lowercase
with spaces replaced by hyphens.

Example:
```
Criterion description: "A concrete output artifact must be produced"
criterion_id:          "a-concrete-output-artifact-must-be-produced"
```

For each criterion in your passport, you must submit:
```json
{
  "criterion_id": "a-concrete-output-artifact-must-be-produced",
  "met": true,
  "evidence": "Concrete evidence — a file path, PR URL, CI run id, command output"
}
```

Evidence must be non-empty. "I believe this is met" is not evidence.
Good evidence: `PR #47 at github.com/org/repo/pull/47`
Good evidence: `grep -r "TODO" src/ returned 0 results`
Good evidence: `CI run #1234 passed — https://ci.example.com/runs/1234`

## Step 3 — Call the verify endpoint

```
POST https://aport.io/api/verify/policy/deliverable.task.complete.v1
Content-Type: application/json

{
  "context": {
    "agent_id": "YOUR_APORT_AGENT_ID",
    "task_id": "TASK_IDENTIFIER",
    "output_type": "code",
    "author_agent_id": "YOUR_APORT_AGENT_ID",
    "summary": "What you did — must meet minimum word count in your passport",
    "tests_passing": true,
    "criteria_attestations": [
      {
        "criterion_id": "criterion-slug-here",
        "met": true,
        "evidence": "Concrete evidence string"
      }
    ]
  }
}
```

Note: `agent_id` goes inside `context`, alongside the policy-specific fields.

## Step 4 — Handle the response

### ALLOW response
```json
{
  "decision": {
    "decision_id": "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx",
    "allow": true,
    "reasons": [
      { "code": "capability_verified", "message": "...", "severity": "info" }
    ],
    "created_at": "2026-03-13T09:00:00Z",
    "signature": "...",
    "policy_id": "deliverable.task.complete.v1",
    "agent_id": "ap_..."
  },
  "request_id": "..."
}
```
The task is done. You may mark it complete, close the ticket, open the PR.
Reference the `decision_id` in your completion message for the audit trail.

### DENY response
```json
{
  "decision": {
    "decision_id": "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx",
    "allow": false,
    "reasons": [
      { "code": "oap.summary_insufficient", "message": "Summary is required...", "severity": "error" }
    ]
  },
  "request_id": "..."
}
```

Do not mark the task done. Check `decision.reasons[].code` for the deny code. Fix the issue and retry.

| deny_code | What it means | What to do |
|-----------|--------------|------------|
| `oap.summary_insufficient` | Summary too short or missing | Rewrite summary with more detail |
| `oap.tests_not_passing` | Tests failing or not submitted | Fix tests, resubmit with `tests_passing: true` |
| `oap.criteria_not_met` | A criterion has `met: false` | Resolve the criterion, re-attest |
| `oap.evidence_missing` | An attestation has no evidence | Add a concrete evidence string |
| `oap.criteria_incomplete` | Missing attestation for a criterion | Add attestations for all passport criteria |
| `oap.self_review_not_allowed` | Reviewer and author are the same | Get a different agent to review |
| `oap.blocked_pattern_detected` | Output contains blocked content | Remove blocked patterns, resubmit |
| `oap.passport_suspended` | Passport is suspended | Contact APort — your passport needs attention |
| `oap.unknown_capability` | Passport missing deliverable.task.complete | Create a new passport with a deliverable contract |

## Step 5 — Announce completion

Once you receive `allow: true`, tell the user:
- What you completed
- The decision_id (if they want the audit trail)
- Any next steps

Do not say "done" before receiving `allow: true`. The contract defines done, not you.

## Retry behaviour

The deny_code is designed for autonomous retry. If you receive:

- `oap.summary_insufficient` → rewrite your summary and retry immediately
- `oap.evidence_missing` → add evidence strings and retry immediately
- `oap.tests_not_passing` → attempt to fix the failing tests, then retry
- `oap.blocked_pattern_detected` → remove the blocked content, then retry
- `oap.self_review_not_allowed` → this requires another agent — ask the user or route to reviewer
- `oap.criteria_not_met` → attempt to resolve the criterion, then retry

Maximum retries: 3. After 3 denials on the same task, surface the issue to the user.
Do not loop indefinitely.

## Links

- Create a passport: https://aport.id (web) or `npx aport-id` (CLI) or https://aport.id/skill (agent)
- Your passport: https://aport.id/passport/YOUR_SLUG
- Verify a decision: GET https://aport.io/api/verify/decisions/get/DECISION_ID
- API docs: https://aport.io/api/documentation
