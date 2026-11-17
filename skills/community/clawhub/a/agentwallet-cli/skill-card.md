## Description:

Create and manage non-custodial smart wallets on Base and Solana with gasless transactions, spending limits, and passkey-based human control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xartex](https://clawhub.ai/user/0xartex)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to create agent-controlled wallets, configure human-approved spending limits, run wallet CLI commands, and integrate Base or Solana transaction flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned wallet CLI execution is used for private-key and financial operations.

Mitigation: Review the `@agntos/agentwallet` package source before installation and pin a specific trusted version.

Risk: Private keys or signing data could be exposed in logged agent sessions, CI, chat, or source control.

Mitigation: Avoid generating or displaying private keys in logged environments, keep keys in encrypted storage or a secrets manager, and do not log signing data.

Risk: Funding the wrong wallet address or setup URL can cause irreversible loss or unsafe authorization.

Mitigation: Verify wallet addresses and setup URLs before funding, and prefer managed wallets with passkey-based human oversight.

Risk: Solana spending limits may be weak if valuation inputs can be supplied or understated by the agent.

Mitigation: Treat Solana spending limits as uncertain unless the deployed program proves that valuations cannot be supplied or understated by the agent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/0xartex/skills/agentwallet-cli)
- [Publisher profile](https://clawhub.ai/user/0xartex)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell command, JSON, and TypeScript code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes wallet creation, transaction, limit-management, status, and emergency-pause guidance; CLI commands can emit JSON with --json.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
