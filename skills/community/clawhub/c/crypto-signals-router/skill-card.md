## Description:

Routes crypto trade signal, market data, news sentiment, Telegram publishing, x402 wallet, signal performance, and health-check requests to the appropriate crypto-signals-plugin agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vizionik25](https://clawhub.ai/user/vizionik25)

### License/Terms of Use:

MIT-0

## Use Case:

External operators and developers use this skill to coordinate a multi-agent crypto signals operation across market data collection, news analysis, signal generation, x402 payment handling, Telegram publishing, and watchdog checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to enable persistent automated execution with wallet and Telegram credentials.

Mitigation: Review the actual scripts and service files before installation, protect secrets with restrictive permissions or a secret manager, and keep Telegram publishing and payments disabled until manually tested.

Risk: Automated x402 wallet payments can spend funds during market-data, news, or publishing workflows.

Mitigation: Use a low-balance dedicated wallet, set conservative spend caps, and monitor spend logs before increasing operational limits.

Risk: The optional systemd setup can introduce root-level persistence if installed without review.

Mitigation: Prefer a user-level scheduler and avoid the sudo systemd path unless the service contents are fully understood and trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vizionik25/skills/crypto-signals-router)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with routing tables, shell command examples, scheduler examples, and configuration variables.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces routing guidance and operational instructions for crypto signals agents; it does not itself provide verified financial advice.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
