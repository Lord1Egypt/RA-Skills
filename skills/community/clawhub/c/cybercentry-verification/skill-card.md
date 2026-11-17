## Description:

Verify wallets, tokens, smart contracts, AI agents and web applications before trusting them, paying per call in USDC over x402

This skill is ready for commercial/non-commercial use.

## Publisher:

[cybercentry](https://clawhub.ai/user/cybercentry)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to request Cybercentry security checks before deciding whether to trust or interact with wallets, tokens, smart contracts, dApp frontends, AI agents, media, private data, or cryptographic material.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted addresses, URLs, source code, media, and other inputs are sent to Cybercentry's remote service for analysis.

Mitigation: Submit only content the user is comfortable sharing, and disclose the remote analysis behavior before use.

Risk: Paid verification tools cost $1.00 in USDC per call.

Mitigation: Use the free catalogue and recent-exploit tools first, then ask for explicit confirmation of the exact paid tool, price, and input before proceeding.

Risk: A clean verification result is not a guarantee that an asset or application is safe.

Mitigation: Report which checks ran and frame the result as decision support rather than a transaction approval.

Risk: Scanned third-party URLs may be hostile.

Mitigation: Render scanned URLs as plain text instead of clickable links.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cybercentry/skills/cybercentry-verification)
- [Cybercentry MCP server](https://centry.cybercentry.co.uk/api/mcp)
- [Cybercentry OpenAPI contract](https://centry.cybercentry.co.uk/openapi.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with service names, submitted inputs, verification summaries, and polling details when a check is asynchronous.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paid checks require explicit user confirmation and may use x402 or a subscription token; failed verification calls are disclosed as not charged.]

## Skill Version(s):

1.0.4 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
