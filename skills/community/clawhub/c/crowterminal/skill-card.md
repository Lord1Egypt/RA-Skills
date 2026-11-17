## Description:

CrowTerminal provides persistent, versioned memory and engagement analysis for AI agents supporting creators and influencers across social media platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[willnigri](https://clawhub.ai/user/willnigri)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to connect creator-support workflows to CrowTerminal's persistent memory, schema discovery, smart query, ingestion, webhook, and engagement-analysis APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Creator strategy, retention, watch-time, demographic, and webhook event data may be sensitive when sent to CrowTerminal.

Mitigation: Redact sensitive or personal data, use sandbox endpoints first, and confirm retention, deletion, and webhook security expectations before using real client data.

Risk: Installing SDKs or using API credentials introduces dependency and credential handling risk.

Mitigation: Pin SDK versions where installed and store CROWTERMINAL_API_KEY in environment variables or a secret manager rather than hardcoding it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/willnigri/skills/crowterminal)
- [Publisher Profile](https://clawhub.ai/user/willnigri)
- [API Key Registration](https://api.crowterminal.com/api/agent/register)
- [Full Docs](https://crowterminal.com/llms.txt)
- [MCP Manifest](https://crowterminal.com/.well-known/mcp.json)
- [OpenAPI](https://api.crowterminal.com/api/docs.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CROWTERMINAL_API_KEY for authenticated API calls; sandbox endpoints are available without authentication.]

## Skill Version(s):

2.3.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
