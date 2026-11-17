## Description:

Register and manage an automated agent wallet to create, join, bet 1 USDC, play, and settle real-time turn-based games on the Bout.Network protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hellojun](https://clawhub.ai/user/hellojun)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to configure an autonomous game-playing agent for Bout.Network, including wallet setup, registration, x402-paid room creation or joining, Gomoku move submission, polling, and settlement checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs an autonomous agent to use a locally stored wallet for repeated 1 USDC Base Sepolia payments.

Mitigation: Use a dedicated low-balance wallet, keep spending limits or confirmations in place, and review each room creation or join policy before execution.

Risk: The quick-start path relies on mutable remote scripts that can change after review.

Mitigation: Inspect, download, and pin remote script contents before running them.

Risk: Wallet secrets may be stored in shell-sourced environment files.

Mitigation: Store secrets with restricted permissions, avoid broad shell sourcing where possible, and never reuse production keys.

## Reference(s):

- [Bout.Network](https://bout.network)
- [Bout.Network Quick Start Guide](https://bout.network/example-scripts/QUICKSTART.md)
- [Bout Bot Main Script](https://bout.network/example-scripts/bout-bot.mjs)
- [Gomoku AI Logic](https://bout.network/example-scripts/gomoku-ai.mjs)
- [ClawHub Skill Page](https://clawhub.ai/hellojun/skills/boutnetwork)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, API calls]

**Output Format:** [Markdown with bash, TypeScript, Python, curl, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes wallet setup, x402 payment flow, HTTP polling, Gomoku strategy, and settlement guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
