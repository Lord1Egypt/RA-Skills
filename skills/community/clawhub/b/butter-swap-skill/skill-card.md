## Description:

ButterSwap helps agents get cross-chain token swap quotes, route transaction data, and cross-chain routing information through the Butter Router API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivanmacaron](https://clawhub.ai/user/ivanmacaron)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to inspect supported chains and tokens, compare cross-chain swap routes, and prepare transaction data for user review and wallet signing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prepared transaction data could be signed without adequate review.

Mitigation: Treat outputs as transaction preparation only and verify token contracts, chains, amounts, recipients, refund addresses, slippage, fees, bridge assumptions, calldata, value, and wallet details before signing.

Risk: Wallet addresses and swap intent may be sent to the Butter Router API.

Mitigation: Use the skill only when comfortable sharing those addresses and transaction parameters with the Butter Router service.

Risk: Routes may be unavailable or unsuitable because of liquidity, fees, slippage, or chain/token selection.

Mitigation: Compare returned routes and fees, handle no-route or insufficient-liquidity responses, and ask the user to choose among multiple route options before preparing swap transaction data.

## Reference(s):

- [Butter API Docs](https://docs.butternetwork.io/butter-swap-integration/integration-guide)
- [Butter Router API Base URL](https://bs-router-v3.chainservice.io)
- [ClawHub Skill Page](https://clawhub.ai/ivanmacaron/skills/butter-swap-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with API examples, route summaries, transaction fields, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API response fields, route options, fees, slippage values, token and chain identifiers, and transaction calldata for user review.]

## Skill Version(s):

1.0.0 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
