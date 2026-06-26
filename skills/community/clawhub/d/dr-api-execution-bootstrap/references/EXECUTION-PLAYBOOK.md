# Execution playbook

## Goal
Run API work fast, directly, and with minimal user friction.

## Direct-first runtime
- Execute API calls in the current session by default.
- Do not spawn subagents for normal API workflows unless the user explicitly asks.
- Keep the chain inside one run whenever tools and auth are already available.

## Fast mode single-run chain
Use this default sequence:
1. Load required tenant, auth, and endpoint constants.
2. Run one preflight only:
   - token present or refreshable
   - app code / function key present
   - one sanity endpoint returns expected auth/result shape
3. If preflight passes, execute the remaining API calls continuously.
4. Verify final state with the minimum readback needed.

Do not repeat token checks, config checks, or sanity probes before every call unless the API actually starts failing.

## Bulk read strategy
- Prefer one broad list call over many per-item reads when the payload contains enough fields.
- Build local lookup maps by id, title, or external key before writes.
- Filter in memory when cheaper than extra network round-trips.

## Bulk write strategy
- For many similar writes, keep the payload template fixed and vary only the changing fields.
- Serialize writes unless the API is clearly safe for concurrency.
- Use small pauses only when the API shows rate or stability issues.
- After bulk writes, do one summary verification pass instead of many redundant reads when possible.

## Approval flow for writes
For PUT/POST/DELETE operations:
- show a concise change preview
- wait for approve/reject in chat
- after approval, execute the whole write batch continuously
- do not ask for approval item-by-item when one batch preview is enough

## Failure handling
- Stop and surface the blocker when auth, endpoint shape, or payload contract is wrong.
- For bulk jobs, continue past isolated per-item failures only when safe, then return a created/updated/failed summary.
- Preserve enough detail to resume from the failed subset.

## Resume pattern
When a batch partially succeeds, report:
- attempted
- succeeded
- failed
- identifiers for failed items

Then resume only the failed subset if the user asks.

## Progress style
- Default: no per-call chatter.
- Acceptable: one short progress note for long-running batches.
- Always keep the final report concise and numeric.

## Verification checklist
After execution, verify only what matters:
- target object exists or was updated
- changed fields match expectation
- summary counts are correct
- failures are enumerated if any
