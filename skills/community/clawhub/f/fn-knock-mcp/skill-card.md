## Description:

Manage fn-knock gateway via its admin API, including reverse proxy, DDNS, SSL/ACME, tunnels, scanner, whitelist, and related gateway administration tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kci-lnk](https://clawhub.ai/user/kci-lnk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this MCP server to let an AI assistant inspect and administer a local fn-knock self-hosted gateway for NAS and home lab environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP server exposes broad gateway administration capabilities, including route, tunnel, firewall, backup, session, and authentication-related changes.

Mitigation: Require manual confirmation before applying administrative changes and restrict use to trusted operators and trusted fn-knock deployments.

Risk: HMAC secret setup and automatic secret extraction can expose sensitive credentials if handled casually.

Mitigation: Use a secret manager or tightly permissioned credential file, avoid placing secrets in shell history or MCP configuration, and disable automatic extraction unless explicitly approved.

Risk: The security evidence rates the release as suspicious because the skill gives an AI-accessible MCP server broad admin power with weak safety framing.

Mitigation: Install only from a pinned, audited package or reviewed local source, and scan the skill before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kci-lnk/skills/fn-knock-mcp)

## Skill Output:

**Output Type(s):** [API Calls, Configuration, Shell commands, Guidance]

**Output Format:** [Markdown with inline JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include fn-knock gateway state, administrative action results, and setup guidance for local MCP configuration.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
