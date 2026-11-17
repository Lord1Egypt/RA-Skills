## Description:

Use Beecli to interact with the Beetrade platform for authentication, market data, bot/strategy operations, alerts, accounts, and portfolio workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[htranbee](https://clawhub.ai/user/htranbee)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to run or troubleshoot Beetrade CLI workflows for authentication, market data, portfolios, bots, strategies, alerts, brokerages, accounts, and trading-client operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release installs an unpinned financial-trading CLI.

Mitigation: Review the skill before installing, use an isolated environment, and verify or pin the exact @beelabs/beetrade-cli version.

Risk: Command patterns can expose Beetrade passwords or brokerage API credentials if secrets are passed directly in arguments or displayed in output.

Mitigation: Do not put Beetrade passwords or brokerage API secrets directly in command arguments, and redact tokens, API keys, secrets, and passwords from outputs.

Risk: Live trading, deletion, scheduling, and credential-update commands can affect real accounts or execution state.

Mitigation: Require explicit human approval before live trading, delete, schedule, or credential-update operations, and prefer read-only, paper, or backtest commands first.

## Reference(s):

- [Beecli Command Reference](references/commands.md)
- [ClawHub Beetrade Skill](https://clawhub.ai/htranbee/skills/beetrade)
- [htranbee Publisher Profile](https://clawhub.ai/user/htranbee)
- [Beetrade CLI npm Package](https://www.npmjs.com/package/@beelabs/beetrade-cli)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Configuration]

**Output Format:** [Markdown with inline shell commands and JSON result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill expects credential redaction, confirmation before live trading or destructive actions, and JSON output handling for most command actions.]

## Skill Version(s):

0.1.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
