## Description:

AIUSD trading and account management skill for balance checks, trading, staking, withdrawals, gas top-up, and transaction history through authenticated MCP-backed tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chaunceyliu](https://clawhub.ai/user/chaunceyliu)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to let an assistant manage AIUSD account workflows, including balances, trades, staking, withdrawals, gas top-ups, deposits, authentication recovery, and transaction history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial trading, staking, withdrawals, gas top-ups, and account actions can affect user funds.

Mitigation: Require explicit user confirmation before trades, withdrawals, staking changes, gas top-ups, or other fund-moving actions.

Risk: Authentication and reauthentication flows can touch sensitive tokens or credential caches.

Mitigation: Use a dedicated account and environment, and require manual confirmation before reauthentication or credential deletion.

Risk: Self-extracting installers can unpack files and install dependencies from the current directory.

Mitigation: Review the unpacked package before installation and run installers only in a dedicated, low-risk directory.

## Reference(s):

- [ClawHub AIUSD Skill Page](https://clawhub.ai/chaunceyliu/skills/aiusd)
- [AIUSD Official Website](https://aiusd.ai)
- [AIUSD OAuth Login](https://mcp.alpha.dev/oauth/login)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with inline shell commands and structured tool results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses live tool schema lookup before account actions; financial and authentication actions should require explicit user confirmation.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
