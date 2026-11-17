## Description:

Bitrefill routes agents to browse or buy Bitrefill gift cards, mobile top-ups, and eSIMs through the best available channel: browser, MCP, CLI, or REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marcopesani](https://clawhub.ai/user/marcopesani)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to search Bitrefill catalog items, prepare purchases, and complete gift card, mobile top-up, or eSIM workflows with explicit spending safeguards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can initiate real-money purchases.

Mitigation: Use a dedicated low-balance account, require explicit confirmation before each purchase, and keep buy-products out of auto-approve settings.

Risk: API keys or purchase credentials could be exposed through unsafe configuration.

Mitigation: Prefer OAuth or bearer-token headers, avoid API keys in MCP URLs, and do not commit credentials to project files.

Risk: Recurring or automated purchases could continue beyond the user's intent.

Mitigation: Use explicit spending caps, expiration dates, recipient and SKU locks, plus a way to list and cancel recurring jobs.

Risk: Gift card codes, eSIM QR data, and redemption links are cash-like bearer secrets.

Mitigation: Deliver codes only in private text channels, avoid logs and shared documents, and advise prompt secure redemption.

## Reference(s):

- [Bitrefill Skill](https://clawhub.ai/marcopesani/skills/bitrefill)
- [Bitrefill Website](https://www.bitrefill.com)
- [Bitrefill Documentation](https://docs.bitrefill.com)
- [Bitrefill CLI Repository](https://github.com/bitrefill/cli)
- [Path: MCP](references/mcp.md)
- [Path: CLI](references/cli.md)
- [Path: REST API](references/api.md)
- [Path: Browse the Website](references/browse.md)
- [Spending Safeguards](references/safeguards.md)
- [Capability Matrix](references/capability-matrix.md)
- [Host: OpenClaw](references/host-openclaw.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline code blocks, shell commands, JSON/TOML configuration snippets, URLs, and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API calls or purchase steps; purchasing requires explicit user confirmation and secure handling of credentials and redemption codes.]

## Skill Version(s):

2.1.2 (source: server release metadata; artifact frontmatter says 2.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
