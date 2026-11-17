# Simulation record and recovery

## Required record

Record proposal identity and task mode; chain/block/hash/time; provider/tool/project; complete ordered `from`, `to`, `value`, `data`; quote/operation identity; real account prerequisites; artificial state and bypasses; per-call outcome; decoded asset and authority changes; gas; trace/log omissions; limits and next check. Redact secrets and signatures, never the recipient or target necessary to review the intent.

The optional helper accepts a smaller local record: proposal and simulation chain IDs; both transaction arrays; block number; `sequential` or `independent` mode; per-call statuses; declared asset/authority/trace coverage; overrides; truncation; and whether an asynchronous destination leg exists. Decimal `value` strings are wei. Full addresses and calldata are required. This diagnostic trusts its supplied evidence; ready-for-review means consistent complete declarations, never authenticated provider proof.

```bash
bun scripts/record.ts --help
bun scripts/record.ts scripts/example.json
```

Run from this skill's directory, or use its actual absolute path. No network or credential access occurs. Malformed records exit nonzero; a valid record with incomplete or reverted simulation returns its classification as JSON so automation can retain the findings.

## Stateful prerequisite

Synthetic proposal: approve 100 USDC to exact spender, then deposit 100 USDC. Both independent simulations start at allowance zero. Approval succeeds; deposit reverts. A provider's two success labels with no state-sharing guarantee still establish no sequential preflight. Required result: simulate the ordered bundle or verify real approval state before simulating the deposit. Do not submit an approval to repair a prepare-only test.

## Bypassed checks

Synthetic proposal: token transfer from account with zero balance. Provider credits it artificially and returns success. Required result: experiment-only, with the synthetic funding shown; the real missing balance remains. No unconditional execution recommendation follows.

## Stale sender

Synthetic proposal sender A; simulation sender B has a large allowance. Same calldata and token do not make the observations applicable to A. Classification: mismatched. Rerun using A and its current prerequisites.

## Complete source bridge preflight

Source deposit succeeds and effects show expected escrow on chain S. Destination is chain D with future solver processing. Record source-ready-for-review and destination not simulated; no delivered funds or successful destination call is established. After a separately authorized source write, persist its operation ID/hash and reconcile destination token, amount and recipient before any next leg.

## Historical replay

Record the original transaction hash and pre-state block. Reproducing its revert provides a diagnosis only. A changed allowance, storage override or timestamp is a new counterfactual run; compare it separately. Do not broadcast or resend to see whether the fix worked.
