## Description:

EchoSync helps agents authenticate to echosync.io, manage Hyperliquid copy-trade configurations, query market data, and submit trading actions through its Node.js helper.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ly95](https://clawhub.ai/user/ly95)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use EchoSync to connect an echosync.io account, inspect wallet and Hyperliquid market data, and request copy-trading or trading operations from an agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access EchoSync account data and saved OAuth credentials.

Mitigation: Use OAuth sign-in only through the provided flow, avoid printing raw tokens unless absolutely necessary, and log out when access is no longer needed.

Risk: The skill can submit orders, update leverage, cancel orders, and change copy-trade settings that may affect real funds.

Mitigation: Independently confirm wallet, coin, side, size, order type, leverage, cancellation ID, and copy-trade settings before allowing those commands.

Risk: Endpoint overrides could route requests away from the expected EchoSync services.

Mitigation: Do not enable endpoint override environment variables unless the target service is trusted and intentionally configured.

## Reference(s):

- [EchoSync Skill on ClawHub](https://clawhub.ai/ly95/skills/echosync)
- [OpenClaw](https://openclaw.ai/)
- [Node.js](https://nodejs.org)
- [Hyperliquid Info API](https://api.hyperliquid.xyz/info)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or plain text with shell commands and JSON-like command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and local credentials stored under ~/.echosync after OAuth sign-in.]

## Skill Version(s):

1.0.0 (source: release evidence; artifact frontmatter: 0.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
