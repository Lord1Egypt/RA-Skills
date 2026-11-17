# Controls and economic dependencies

Map authority before ranking risks. For each material contract, retain address, chain, role, runtime identity, code/source correspondence, observation pin and how it relates to the target. Include the token, implementations, factory, fee/reward layer, treasury, locker, oracle and privileged callers that can change holder outcomes. Do not infer a deployed version from a website's current ABI.

## Capability and controller

Inspect the effective paths for issuance, balance changes, confiscation, transfer gating, buy/sell taxes, exemptions, freezes, arbitrary calls and delegatecall. Distinguish the rules active today from the authority to install different rules tomorrow. Record the actual controlling accounts or contracts, role administrators, multisig threshold and timelock delay/bypass paths. A renounced owner does not settle other roles or external controllers. Follow [OpenZeppelin's access-control model](https://docs.openzeppelin.com/contracts/5.x/access-control) as a reference, then verify the deployed implementation's behavior.

Resolve proxy implementation and beacon/admin state from the selected deployment. [ERC-1967](https://eips.ethereum.org/EIPS/eip-1967) defines common storage locations; empty slots do not rule out custom proxies, clones or other control mechanisms. Identical proxy runtimes can delegate to different logic and retain different state. Store those distinctions before reusing any analysis.

A nonzero `owner()` establishes an address, not its powers. Read which privileged functions exist in the deployed code and which are reachable from that account: minting, pausing, blacklisting, fee or tax changes, upgrades and principal withdrawal each need their own evidence. An externally owned owner that carries an [EIP-7702](https://eips.ethereum.org/EIPS/eip-7702) delegation designates code, so the authority surface can change with the delegation; record the current designator. Risk-scanner fields such as `mintable`, `owner` and `is_locked` are provider classifications: use them to choose what to verify, not as findings, and treat a blank field as unknown rather than clear.

Distinguish factory defaults for future deployments from callable powers over existing tokens. Trace each setter to its consumers: storing tax, admin or template defaults for clone initialization is not itself a demonstrated setter for a previously deployed token. Separately assess whether upgrades can expose otherwise dormant factory privileges, because absence of a forwarding path in today's implementation does not remove upgrade risk. Pin storage and call reads to a block, keep the raw slot or calldata beside each result, and never infer a function's return semantics from a selector guess without a verified ABI.

When source correspondence is uncertain, start with runtime, selectors, compiler metadata and available verified predecessors. Escalate to storage/history and narrow fork experiments only if needed to answer the question. Decompiler output remains a hypothesis until meaningful bytecode correspondence is established. Route broad exploit searches to a separately scoped protocol audit.

## What holders can actually claim

Identify the asset or right held and each conversion needed to reach the desired payout. Review eligibility, claim authority, collateral denomination, redemption queue/cap, fees, reserve availability and the administrator's ability to alter them. A treasury balance, synthetic reward or advertised buyback is not automatically a holder-enforceable claim. Trace any wrapper or quote asset to its own custody and exit dependencies.

For reward accounting, reconcile entitled, paid, unpaid and retained quantities by epoch and recipient. Check duplicate claims, caps, adjustments, prefunding and whether a stalled distributor can resume. Keep accounting solvency separate from processing liveness; both affect whether holders receive assets. Reuse the actual product's audited accounting model rather than assuming every vault follows ERC-4626.

Trigger deeper work when a material power, dependency or obligation remains unexplained. Stop once its executable scope and controller are evidenced or the missing evidence is explicit. Do not assign a clean result to an unreachable API or missing implementation.

Primary references reviewed 2026-09-06. These procedures do not certify a contract or administer its roles.
