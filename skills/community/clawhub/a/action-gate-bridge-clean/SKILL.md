---
name: action-gate-bridge
description: Route risky communications next steps through a typed action-intent bridge so external writes, bookings, settings changes, public posts, and spend decisions require explicit policy and approval handling instead of informal reasoning.
---

# Action Gate Bridge

Use this skill when a communications workflow moves from analysis into a possible external action.

## Core workflow

1. Read `references/action-bridge.md` first.
2. Read `references/approval-matrix.md` before proposing any action.
3. Pick the narrowest typed action that fits the next step.
4. Create a proposal or route the write intent through the sidecar.
5. Interpret the result as `allowed`, `needs_approval`, `blocked`, or `accepted`.
6. Decide what to show the user; do not silently execute a risky action.

## Helpers

Use the bundled scripts when the host environment supports them:

```bash
node scripts/propose-action.js communications send_email target@example.com "Subject" "Summary" "Program"
node scripts/route-http-write.js communications api-target "Summary" /path '{"hello":"world"}' "Program" "credentials-ref"
```

## Safety

- Red actions require explicit user approval.
- Do not send, post, submit, confirm, or spend by default.
- If policy, scope, approval, or reversibility is unclear, escalate instead of acting.
