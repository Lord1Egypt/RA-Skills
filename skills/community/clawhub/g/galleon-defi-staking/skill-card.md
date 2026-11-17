## Description:

Guides source-backed planning for liquid staking, restaking, delegation, and queued withdrawals across Lido, Rocket Pool, EigenLayer, and Symbiotic.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

People researching or managing DeFi staking positions use this skill to compare routes, prepare unsigned plans, and track withdrawal eligibility and claims without granting transaction authority by default.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stale protocol conditions or quotes can misstate liquidity, withdrawal timing, or slashing exposure.

Mitigation: Verify current deployed contracts and state, identify observation time, and treat delays as estimates until eligibility is confirmed.

Risk: Approvals, staking, delegation, or claims can move funds or expand authority beyond the user's request.

Mitigation: Keep wallet secrets out of the agent and require explicit review of exact terms before any signing or scheduled monitoring.

Risk: A withdrawal request or indexer estimate may be mistaken for settled funds, and an uncertain submission could be retried twice.

Mitigation: Check current owner, request identity, on-chain eligibility, and claim receipt; reconcile uncertain transactions before retrying.

## Reference(s):

- [Provider mechanics and source links](references/providers.md)
- [Staking lifecycle workflows](references/workflows.md)
- [Task examples and user configuration](references/task-examples.md)
- [Lido withdrawal queue](https://docs.lido.fi/contracts/withdrawal-queue-erc721/)
- [EigenLayer unstaking and withdrawal](https://docs.eigencloud.xyz/eigenlayer/restakers/restaking-guides/restaking-user-guide/liquid-restaking/withdraw-from-eigenlayer)
- [Symbiotic epochs and delays](https://docs.symbiotic.fi/learn/mechanics/epochs-and-delays)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Unsigned transaction plans]

**Output Format:** [Markdown text with source-backed comparisons and lifecycle status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes chain and source time, asset units, liquidity, withdrawal status, and authorization scope when relevant.]

## Skill Version(s):

0.2.1 (source: skill metadata and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
