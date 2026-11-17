## Description:

Connect to 100+ third-party APIs, including Google Workspace, Microsoft 365, GitHub, Notion, Slack, Airtable, and HubSpot, through Maton-managed OAuth connections.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kenswj](https://clawhub.ai/user/kenswj)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to call native endpoints on connected business, file, admin, messaging, and financial services after configuring Maton API-key authentication and per-service OAuth authorization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent broad API-level authority across connected business, file, admin, messaging, and financial services.

Mitigation: Use least-privileged OAuth/API-key connections and require explicit approval before writes, deletes, admin changes, public messages, or financial operations.

Risk: The documented troubleshooting command can print MATON_API_KEY to the terminal.

Mitigation: Use a presence-only environment check instead of printing the secret value.

Risk: Gateway calls depend on external services, network availability, active connections, and target API rate limits.

Mitigation: Validate active connections before use, handle passthrough API errors, and respect the documented 10 requests-per-second account limit plus target-service limits.

## Reference(s):

- [Maton](https://maton.ai)
- [Maton API Reference](https://www.maton.ai/docs/api-reference)
- [API Gateway Skill Definition](artifact/SKILL.md)
- [Slack Routing Reference](artifact/references/slack/README.md)
- [Gmail Routing Reference](artifact/references/google-mail/README.md)
- [GitHub Routing Reference](artifact/references/github/README.md)
- [Notion Routing Reference](artifact/references/notion/README.md)
- [Notion MCP Routing Reference](artifact/references/notion-mcp/README.md)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown with inline code examples and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and explicit per-service OAuth authorization through Maton's connect flow.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
