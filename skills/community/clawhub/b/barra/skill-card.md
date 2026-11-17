## Description:

Executes Bitcoin (BTC) spot buy orders on Binance using market or limit orders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[violetsakura-7](https://clawhub.ai/user/violetsakura-7)

### License/Terms of Use:

MIT-0

## Use Case:

External users who connect a Binance account use Barra to submit BTC spot buy orders from natural-language instructions and receive order execution details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can trigger real cryptocurrency buy orders without a documented final confirmation.

Mitigation: Require an explicit final confirmation before every trade and review the order details before execution.

Risk: Binance API credentials with broad permissions could expose funds if misused or leaked.

Mitigation: Use a tightly scoped API key with withdrawals disabled, spot trading only when needed, and IP restrictions enabled.

Risk: The permission metadata contains an invisible character that may confuse parsing.

Mitigation: Normalize and inspect the skill metadata before installation or deployment.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, API Calls, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with inline shell commands and trade-result text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Binance API credentials and account permissions configured outside the skill.]

## Skill Version(s):

0.1.4 (source: server evidence release; artifact frontmatter declares 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
