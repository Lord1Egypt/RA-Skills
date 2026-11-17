## Description:

Guides Uniswap v3 liquidity-position decisions, including tick selection, fee collection, adding or removing liquidity, and range changes, with an unsigned action plan.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

Liquidity providers and developers use this skill to assess a Uniswap v3 NFT position, compare holding with liquidity changes, and prepare an unsigned, evidence-backed action sequence. It does not cover Uniswap v4 or gauge-held positions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An incorrect chain, manager, pool, or token order could produce an unsafe liquidity plan.

Mitigation: Verify the chain, manager contract, pool identity, and token order from authoritative deployments and live read-only state before wallet handoff.

Risk: Incorrect slippage bounds, deadlines, or unverified calldata could lead to unexpected financial outcomes.

Mitigation: Review bounds and deadlines, simulate the final action from the actual owner, and require explicit wallet approval; installation alone grants no trade or signing authority.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/galleonlabs/skills/galleon-uniswap-v3-liquidity)
- [Protocol recipes and sources](references/recipes.md)
- [Uniswap deployments](https://developers.uniswap.org/deployments)
- [Uniswap v3 position minting](https://developers.uniswap.org/docs/sdks/v3/guides/managing-liquidity/position-minting)
- [Uniswap v3 liquidity modification](https://developers.uniswap.org/docs/sdks/v3/guides/managing-liquidity/modifying-position)
- [Uniswap v3 fee collection](https://developers.uniswap.org/docs/protocols/v3/guides/managing-liquidity/collect-fees)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Shell commands]

**Output Format:** [Markdown with an unsigned action sequence and optional read-only commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes position and pool identity, proposed usable ticks, inventory and fee accounting, cost comparison, and required simulation or receipt evidence. No signing is included.]

## Skill Version(s):

0.6.1 (source: skill metadata and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
