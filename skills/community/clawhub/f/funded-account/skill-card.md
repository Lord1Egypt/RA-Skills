## Description:

Interact with the Hyperscaled funded trading platform to check trading accounts, positions, orders, balances, rules, miners, registration, KYC status, and configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[taoshidev1](https://clawhub.ai/user/taoshidev1)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading agents use this skill to operate Hyperscaled funded accounts through CLI commands or SDK scripts. It supports account review, trading-rule checks, positions and orders, registration, KYC, payouts, miner browsing, and configuration tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install the Hyperscaled package without pinning a reviewed version.

Mitigation: Install a reviewed pinned package version in an isolated environment before using the skill.

Risk: The skill can support high-impact account actions such as purchases, KYC, configuration changes, order cancellation, and trade submission.

Mitigation: Require explicit user confirmation before every purchase, KYC step, config change, cancellation, or trade, and validate trading rules before submitting orders.

Risk: Private keys or wallet credentials could be exposed if handled directly on the command line.

Mitigation: Use narrowly scoped credentials and environment variables where possible, and do not display, log, or pass private keys on the command line.

Risk: Funded-account trading can approach drawdown or leverage limits.

Mitigation: Review account type, intraday drawdown, EOD drawdown, and current portfolio leverage before acting on trade guidance.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/taoshidev1/skills/funded-account)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and optional Python code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include account and risk summaries, CLI command proposals, configuration guidance, validation results, and confirmation prompts for high-impact actions.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
