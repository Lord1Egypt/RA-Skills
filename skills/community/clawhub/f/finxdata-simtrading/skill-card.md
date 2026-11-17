## Description:

Uses FinXData's dedicated simulated-trading key to manage A-share and Hong Kong stock watchlists, simulated accounts, orders, positions, trades, cash ledgers, assets, and performance, with CNY T+1 behavior for A-share accounts and HKD T+0 behavior for Hong Kong accounts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[finxdata](https://clawhub.ai/user/finxdata)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to operate FinXData simulated-trading workflows for A-share and Hong Kong stock practice portfolios. It supports watchlist management, market-isolated account setup, simulated order entry and cancellation, and portfolio status review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Trading Key can authorize simulated-trading account actions.

Mitigation: Store the key in the environment, do not paste it into chat, and review write actions such as orders, cancellations, watchlist edits, account creation, and resets before execution.

Risk: A custom API base URL could receive the Trading Key.

Mitigation: Use the default FinXData endpoint unless the alternate endpoint is fully trusted.

Risk: Simulated trades and simplified fees may be mistaken for real holdings or investment advice.

Mitigation: Label results as simulated and avoid presenting positions, fills, or performance as real brokerage activity or recommendations.

## Reference(s):

- [FinXData A-share and Hong Kong Simulated Trading API](references/api.md)
- [Finxdata Simulated Trading on ClawHub](https://clawhub.ai/finxdata/skills/finxdata-simtrading)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands call the FinXData simulated-trading API and return JSON responses or JSON-formatted errors.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
