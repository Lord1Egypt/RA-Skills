## Description:

Assesses and compares Uniswap and Aerodrome liquidity pools using read-only evidence of yield quality, position economics, and exit risks before capital is deployed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

Liquidity providers and analysts use this skill to compare candidate pools, distinguish fees from incentives, and evaluate token, contract, custody, and exit risks before choosing a pool. It produces research rather than transaction instructions or return guarantees.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stale or unverified pool data may misstate returns or hide exit constraints.

Mitigation: Verify pool identity and current on-chain state, date changing figures, and report missing reads as not assessable.

Risk: Optional external tools or automation may introduce fees, permissions, or wallet exposure.

Mitigation: Use external tools only when chosen, check current versions and fees, and keep wallet signing, approvals, and transactions outside this read-only skill.

Risk: LP contracts, tokens, hooks, or markets can fail and cause capital loss.

Mitigation: Review token, hook, custody, and full-exit gates; treat the result as research, not a return guarantee or execution authority.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/galleonlabs/skills/galleon-lp-analyze)
- [Uniswap v4 hooks documentation](https://developers.uniswap.org/docs/protocols/v4/concepts/hooks)
- [VFAT APR methodology](https://docs.vfat.io/aprs/)

## Skill Output:

**Output Type(s):** [Analysis, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dated pool identity and evidence, risk-gate verdicts, comparable fee and incentive estimates, exit assessment, and explicit unknowns; no transaction instructions.]

## Skill Version(s):

0.6.1 (source: ClawHub release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
