## Description:

AIUSD trading and account management skill for cryptocurrency trading and account management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chaunceyliu](https://clawhub.ai/user/chaunceyliu)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to let an OpenClaw or ClawdBot assistant check AIUSD balances, query account data, execute crypto trades, stake or unstake AIUSD, withdraw stablecoin, and guide deposits through AIUSD services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place trades, stake assets, withdraw funds, and otherwise affect real crypto balances.

Mitigation: Require clear user intent for fund-moving actions, review live tool schemas before calls, and confirm trade, staking, and withdrawal details before execution.

Risk: Setup and reauthentication can read local authentication tokens and delete shared authentication state.

Mitigation: Use a dedicated environment for installation, keep credential backups, and avoid running it where unrelated MCP credentials are present unless that risk is accepted.

Risk: The provided self-extracting installers run package extraction and npm dependency installation under the current user account.

Mitigation: Review the decoded package and dependencies before running installers or npm install.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chaunceyliu/skills/aiusd-skill-agent)
- [AIUSD official website](https://aiusd.ai)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with inline shell commands, configuration guidance, and tool result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke MCP-backed account, trading, staking, withdrawal, gas, transaction, recharge, and authentication workflows when used by an agent.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
