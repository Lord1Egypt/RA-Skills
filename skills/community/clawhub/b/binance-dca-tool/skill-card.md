## Description:

Binance Dollar-Cost Averaging (DCA) tool for planning recurring crypto purchases, checking balances and trade history, and placing manual or scheduled spot buys on Binance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fpsjago](https://clawhub.ai/user/fpsjago)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to plan Binance DCA strategies, inspect account balances and trade history, and execute or schedule recurring spot purchases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place real-money Binance spot buy orders when signed API credentials are available.

Mitigation: Use Binance testnet first, require explicit confirmation before live buys or recurring schedules, and set clear spending limits.

Risk: Binance API credentials could grant more authority than the DCA workflow needs.

Mitigation: Use minimum-permission API keys with withdrawals disabled and IP allowlisting enabled.

Risk: Inline cron secrets or unattended schedules could expose credentials or trigger unintended purchases.

Mitigation: Avoid placing secrets directly in cron entries and review every scheduled buy configuration before enabling it.

## Reference(s):

- [Binance API base URL](https://api.binance.com)
- [Binance Spot Testnet](https://testnet.binance.vision)
- [ClawHub skill page](https://clawhub.ai/fpsjago/skills/binance-dca-tool)
- [Publisher profile](https://clawhub.ai/user/fpsjago)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and plain-text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call Binance public or signed API endpoints through the bundled shell script when the user supplies credentials and chooses an action.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
