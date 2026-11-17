## Description:

Retrieve rich metadata for a specific Art Blocks token using artblocks-mcp.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryley-o](https://clawhub.ai/user/ryley-o)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve complete metadata for a known Art Blocks token, including traits, media URLs, owner address, listing information, and project context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Token lookups can expose public blockchain and marketplace metadata, including owner addresses, listings, prices, and Art Blocks media links.

Mitigation: Treat returned ownership and listing data as public metadata, and avoid presenting it as private, verified identity, or financial advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ryley-o/skills/get-token-metadata)
- [Publisher profile](https://clawhub.ai/user/ryley-o)

## Skill Output:

**Output Type(s):** [guidance, API calls, text]

**Output Format:** [Markdown guidance describing a get_token_metadata tool call and expected structured token, media, and project fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a full token ID and optionally a chain ID for Ethereum, Arbitrum, or Base.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
