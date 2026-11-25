## Description:

YouTube channels, videos, transcripts, and comments for agents — no Google API key or daily quota to manage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[superagnt](https://clawhub.ai/user/superagnt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and research or marketing teams can search YouTube and retrieve channel and video details, subtitles, comments, recommendations, and trending content for creator research, monitoring, and analytics. The documented channel email lookup can return business contact addresses, which should be used only for the stated purpose and not for bulk unsolicited outreach.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requests send an API credential to an external service.

Mitigation: Provide the key only for requests to the documented superagnt API, and store it as a secret environment variable rather than placing it in prompts or shared files.

Risk: The channel email lookup can return creators’ business contact addresses.

Mitigation: Use returned contact details only for the user's stated purpose and avoid bulk unsolicited outreach.

## Reference(s):

- [YouTube Data documentation](https://superagnt.com/r/ch-youtube-data-docs)
- [YouTube Data MCP endpoint](https://mcp.superagnt.com/mcp/youtube)
- [API key and account](https://superagnt.com/r/ch-youtube-data-key)
- [ClawHub listing](https://clawhub.ai/superagnt/skills/youtube-data)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [Structured JSON results and Markdown instructions with curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live results require the documented API credential or scoped MCP sign-in and depend on available account credits.]

## Skill Version(s):

2.0.19 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
