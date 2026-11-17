## Description:

USDC wallet operations for OpenClaw agents via Circle Developer-Controlled Wallets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eltontay](https://clawhub.ai/user/eltontay)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to create Circle developer-controlled wallets, check USDC balances, request sandbox testnet funds, and send USDC across supported chains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can initiate USDC transfers.

Mitigation: Require manual review and explicit approval before any send operation, especially on mainnet or production credentials.

Risk: Circle API keys and entity secrets are stored under ~/.openclaw/circle-wallet/.

Mitigation: Restrict filesystem permissions on that directory and rotate Circle credentials if they may have appeared in shell history, process logs, or overly readable config files.

Risk: Commands may be run against production or mainnet environments.

Mitigation: Use sandbox/testnet first and avoid production credentials unless the execution environment and operator workflow are trusted.

## Reference(s):

- [Circle Developer Docs](https://developers.circle.com)
- [Circle Console](https://console.circle.com)
- [ClawHub skill page](https://clawhub.ai/eltontay/skills/circle-wallet)
- [Publisher profile](https://clawhub.ai/user/eltontay)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions and CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call Circle APIs and write wallet configuration under ~/.openclaw/circle-wallet/.]

## Skill Version(s):

1.0.17 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
