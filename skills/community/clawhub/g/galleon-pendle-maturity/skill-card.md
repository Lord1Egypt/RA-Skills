## Description:

Guides evaluation of Pendle PT and YT positions, including maturity holds, early exits, and redemption.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

DeFi users and analysts compare holding Pendle PT to maturity, selling early, and redeeming PT or YT on a specified chain and market. The skill prepares an evidence-backed decision record and, when requested, an unsigned transaction sequence for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An incorrect chain, market, token address, or stale quote could misstate proceeds or route funds incorrectly.

Mitigation: Verify chain, market, token addresses, exact-size quotes, and route simulations before signing any transaction.

Risk: Disclosing wallet secrets or mistaking research for signing authorization could expose assets.

Mitigation: Never provide private keys or seed phrases; review unsigned transactions and sign only after explicit authorization.

## Reference(s):

- [Pendle decision worksheet](references/recipe.md)
- [Pendle FAQ](https://docs.pendle.finance/pendle-v2/FAQ)
- [Pendle PT, YT and LP guide](https://docs.pendle.finance/pendle-academy/cheatsheet-for-the-impatient/pt-yt-lp-cheatsheet)
- [Pendle API schema](https://api-v2.pendle.finance/core/docs)
- [Pendle core interfaces](https://github.com/pendle-finance/pendle-core-v2-public)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown decision record]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes chain, market, block time, observed units, assumptions, costs, and missing reads; may include a simulated unsigned transaction sequence.]

## Skill Version(s):

0.2.1 (source: ClawHub release and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
