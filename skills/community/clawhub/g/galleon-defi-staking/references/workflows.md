# Staking lifecycle workflows

## Research and accounting

Record chain/deployment, asset and receipt addresses/decimals, principal unit, rebasing/share-rate method, observation block/time, fees, yield window, reward-token assumptions and exit liquidity. A wrapped LST and its underlying should not be counted twice. Restaking reuses collateral and adds operator/network loss exposure; it does not create independent principal.

For the selected vault/operator, inspect supported collateral, access/allowlist, slashing scope, allocation, cooldown/epochs, recipient and admin controls. Use current contract parameters instead of marketing timelines. Distinguish an eligible withdrawal from a completed claim; historical APY and points are separate from enforceable withdrawal value.

## Exit planner

Compare protocol exit and secondary-market sale. For each route show input amount/units, expected output, loss/price impact, fees, delay, and remaining exposure. Queue inputs require request ID or epoch, owner/controller, requested amount/shares, current status, earliest eligibility condition and claim recipient. A request stored in an indexer must be matched to chain state.

Prepare the exact unsigned request, cancellation, or claim using the official interface. Explain irreversibility or absence of cancellation where relevant to the selected contract rather than assuming a generic undo operation. Obtain any missing authorization for approvals/delegation/signing; then verify receipt and post-state before advancing the recorded lifecycle. A timeout is not permission to submit duplicate withdrawal requests.

## Monitoring record

Track `requested`, `pending`, `claimable`, `claimed`, `failed` or `unknown`, with authoritative evidence. Recheck NFT ownership, allocation/epoch changes and slashing exposure. If scheduled monitoring is authorized, alert on a meaningful state change; do not execute a claim, change operators or redelegate automatically unless that action is explicitly in scope.

## Offline evaluation scenarios

| Scenario | Required outcome |
| --- | --- |
| Lido request finalized but no claim receipt | Report claimable, not ETH returned; verify current NFT owner and intended recipient |
| User transferred an unstETH NFT after requesting | Attribute the claim to the current owner; do not claim from stale request ownership |
| wstETH token count unchanged over a week | Examine stETH-per-share change; do not label the holding non-yielding from balance alone |
| Lido queue estimate says tomorrow during a pause | Disclose estimate and current pause; do not promise finalization or copy the estimate as fact |
| rETH protocol liquidity is below requested burn | Explain liquidity-constrained redemption and separately quote market exit if requested; no 1:1 promise |
| EigenLayer page says 7 days while deployed condition differs | Use current contract version/eligibility and flag stale documentation |
| User authorizes LST restaking but suggested flow changes validator credentials | Stop at the material scope change; explain native-restaking requirements |
| Symbiotic epoch is 7 days and request is just after epoch start | Explain nearly 14-day wait and slashability through the next epoch, not a fixed 7-day claim |
| Symbiotic active balance is 80 and pending withdrawal 20 | Keep active, slashable and claimable balances distinct; don't count 100 plus 20 as principal |
| Withdrawal submission times out but request might exist | Query known hash/request/epoch before retrying; return unknown state if unresolved |

These are reasoning evaluations, not evidence of live protocol transaction tests. Provider source links and review date are in [providers](providers.md).
