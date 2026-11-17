## Description:

Backtest and deploy trading strategies on Superior Trade's managed cloud.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mmmmssss8899](https://clawhub.ai/user/mmmmssss8899)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create, backtest, and manage DEX trading strategies through Superior Trade. It can create and start live trading deployments only after explicit user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Superior Trade API key can create and manage deployments that may trade real funds.

Mitigation: Store the key securely, keep it scoped to the intended account, and require explicit review of every live deployment summary before approval.

Risk: Deployment deletion or cleanup actions can close positions and orders.

Mitigation: Confirm cleanup actions with the user before deleting deployments or changing live trading status.

## Reference(s):

- [Superior Trade Account Portal](https://account.superior.trade)
- [ClawHub Skill Page](https://clawhub.ai/mmmmssss8899/skills/ai-agent-trading-on-dex)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with API request examples, strategy code, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include live deployment summaries requiring explicit user confirmation before execution.]

## Skill Version(s):

3.0.10 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
