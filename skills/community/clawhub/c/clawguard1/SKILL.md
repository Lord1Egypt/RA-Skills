---
name: clawguard
description: "ClawGuard governance layer that must run before any SQL, file-system, or API write. Use evaluate_action(action_type, justification, risk_level) to log/authorize actions and get_audit_report(limit) to review the SQLite-based audit ledger. Blocks risk_level >= 4 automatically."
---

# ClawGuard Governance Skill

ClawGuard enforces a universal audit and approval layer for any potentially destructive or high-impact change. It persists all intents to `clawguard.db` and automatically blocks actions when `risk_level >= 4`.

## Tools

- `evaluate_action(action_type, justification, risk_level)`
  - Logs the requested action to the `audit_ledger` table and returns `{ allowed: boolean, message: string }`.
  - Risk levels:
    - 1 = negligible (read-only, cosmetic)
    - 2 = low (single-record updates, reversible)
    - 3 = medium (bulk updates, config tweaks)
    - 4 = high (privileged file writes, schema changes, secrets)
    - 5 = critical (system-wide deletions, irreversible ops)
  - Any level `>= 4` is blocked automatically—handle accordingly.

- `get_audit_report(limit)`
  - Fetches the most recent `limit` rows (default 5) from `audit_ledger`, ordered by newest first.

## Workflow

1. **Classify the action** — Determine `action_type`, craft a concise `justification`, and score `risk_level`.
2. **Call `evaluate_action` BEFORE executing** any SQL statement, file mutation, or write-capable API request. (See `GUIDANCE.md`.)
3. **Honor the result** — If `allowed` is `false`, stop immediately and surface the block reason.
4. **Execute the operation** only after an approved response.
5. **Audit** as needed with `get_audit_report(limit)` when preparing reports or debugging governance outcomes.

## Additional Notes

- `audit_ledger` schema: `(id INTEGER PK, action_type TEXT, justification TEXT, risk_level INTEGER, status TEXT, ts DATETIME DEFAULT CURRENT_TIMESTAMP)`.
- The ledger is persistent; repeated approvals accumulate chronological history.
- Keep justifications specific (who/what/why) to maintain a high-quality audit trail.
