## Description:

YouTube channels, videos, transcripts, and comments for agents — no Google API key or daily quota to manage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[superagnt](https://clawhub.ai/user/superagnt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, marketing and research teams, and data teams can use the skill to search YouTube and retrieve video, channel, subtitle, recommendation, and comment data for research, monitoring, alerts, and analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requests send the SUPERAGNT_API_KEY to the external YouTube Data API service.

Mitigation: Use the skill only if you trust the service and are comfortable providing the key for these requests; keep the key private.

Risk: Channel email lookup returns creators’ business contact email addresses, which are personal contact data.

Mitigation: Use email results only for the user's stated purpose and never for bulk unsolicited outreach.

## Reference(s):

- [YouTube Data documentation](https://superagnt.com/r/ch-youtube-data-docs)
- [YouTube Data API](https://api.superagnt.com/v1/data/youtube)
- [YouTube Data MCP server](https://mcp.superagnt.com/mcp/youtube)
- [ClawHub listing](https://clawhub.ai/superagnt/skills/youtube-data)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Structured JSON API responses and Markdown usage guidance with inline curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live results depend on a valid SUPERAGNT_API_KEY and available account credits.]

## Skill Version(s):

2.0.14 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
