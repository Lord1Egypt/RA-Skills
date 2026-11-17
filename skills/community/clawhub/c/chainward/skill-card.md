## Description:

Monitor AI agent wallets on Base. Register wallets, check health scores, view transactions, manage alerts, and watch live feeds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[saltxd](https://clawhub.ai/user/saltxd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use ChainWard to monitor autonomous AI agent wallets on Base, register wallets, review transactions and health, and configure operational alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an external ChainWard CLI installed from npm.

Mitigation: Review the @chainward/cli package and version before installation and install it only in environments where ChainWard is trusted.

Risk: The ChainWard CLI uses CHAINWARD_API_KEY and stores local configuration that may include sensitive alert or account settings.

Mitigation: Limit the API key to ChainWard use, protect the key in the agent environment, and review ~/.chainward/config.json and alert delivery channels for sensitive values.

## Reference(s):

- [ChainWard website](https://chainward.ai)
- [ChainWard ClawHub listing](https://clawhub.ai/saltxd/skills/chainward)
- [saltxd ClawHub profile](https://clawhub.ai/user/saltxd)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance assumes the ChainWard CLI, CHAINWARD_API_KEY, and Base-only wallet monitoring described by the artifact.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
