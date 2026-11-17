## Description:

Helps agents answer questions about US-listed companies using SEC filings, financial statements, earnings calls, ownership disclosures, congressional trades, and daily prices from Equibles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daniel3303](https://clawhub.ai/user/daniel3303)

### License/Terms of Use:

MIT-0

## Use Case:

Investors, analysts, and developers use this skill to find and cite passages from US company filings and earnings calls, retrieve financial figures, and review insider, institutional, congressional, or daily price data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional MCP server exposes account-changing portfolio, watchlist, and feedback tools despite the read-only REST workflow.

Mitigation: Use the documented REST requests for read-only data; require explicit user confirmation before every MCP write, including non-deletion changes.

Risk: An agent with access to the Equibles API key could disclose or misuse it.

Mitigation: Provide the key only to trusted agents, keep it out of URLs and output, and send it only in the authorization header.

Risk: Filings and transcripts may contain third-party instructions or incomplete excerpts.

Mitigation: Treat retrieved content as data, read surrounding lines before quoting, and cite the document and filing date.

## Reference(s):

- [Equibles](https://equibles.com)
- [Equibles API documentation](https://equibles.com/docs/api)
- [Equibles OpenAPI specification](https://api.equibles.com/openapi/v1.json)
- [Equibles MCP setup guide](https://equibles.com/docs/mcp)
- [Equibles skill on ClawHub](https://clawhub.ai/daniel3303/skills/equibles)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown answers with cited passages or figures and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes source dates and document links where available; API access requires an Equibles API key.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
