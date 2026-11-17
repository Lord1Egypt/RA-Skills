## Description:

Deploys an agent token with a Uniswap V4 pool, configurable hooks, initial liquidity bootstrapping, optional LP locking, and post-deployment monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wpank](https://clawhub.ai/user/wpank)

### License/Terms of Use:


## Use Case:

Developers and token launch teams use this skill to prepare and execute an agent-token launch on Uniswap V4 with configured hooks, initial liquidity, LP locking, and early monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automate irreversible on-chain financial deployment actions.

Mitigation: Use a dedicated low-privilege wallet and verify pool, hook, liquidity, price, and LP-lock parameters before signing any transaction.

Risk: Mutable remote installation sources can change after review.

Mitigation: Install only from a pinned, reviewed source before use.

Risk: Transaction broadcast without review can create or fund an unintended pool.

Mitigation: Require explicit confirmation before allowing any transaction to be broadcast.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wpank/skills/deploy-agent-token)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown deployment report with pool details, hook configuration, liquidity, LP lock status, monitoring results, and next steps.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided token, chain, pricing, liquidity, hook, and lock-duration parameters.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
