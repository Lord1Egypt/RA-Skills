## Description:

Guides agents in using paid Blackwood State APIs for blockchain data, research, validation, finance, weather, and text utilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tgws-metal](https://clawhub.ai/user/tgws-metal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use the skill to retrieve onchain and financial data, research and validate information, check weather and time zones, and run text or media utilities through paid Blackwood State endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid requests can accumulate costs across multiple endpoint calls.

Mitigation: Review the endpoint catalog, agree on a total budget before paying, and enforce per-call payment caps; use a lightly funded dedicated wallet.

Risk: Submitted content may be shared with Blackwood State and its processing providers.

Mitigation: Send only content you are comfortable sharing with those parties.

Risk: Optional private-key signing gives the server access to a dedicated wallet key.

Mitigation: Enable private-key signing only if needed and use a dedicated, lightly funded wallet.

## Reference(s):

- [Blackwood State MCP documentation](https://github.com/Blackwood-State/mcp)
- [Blackwood State API OpenAPI specification](https://x402-gateway.blackwoodstate8.workers.dev/openapi.json)
- [Blackwood State service status](https://x402-gateway.blackwoodstate8.workers.dev/status.json)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Text, Markdown, JSON, Images, Audio]

**Output Format:** [API response data and generated content, including JSON, text, Markdown, images, and audio]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some endpoint results require asynchronous job polling; each paid call has a per-call price cap.]

## Skill Version(s):

0.2.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
