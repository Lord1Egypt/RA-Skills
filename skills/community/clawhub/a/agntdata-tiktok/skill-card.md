## Description:

Public TikTok creator profiles for agents — follower, video, and like counts as structured JSON, with no TikTok key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[superagnt](https://clawhub.ai/user/superagnt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and research or marketing teams use the skill to retrieve TikTok creator profiles, video details, account and video search results, and related content for creator research, monitoring, and analytics workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill's documented features include video and search access in addition to creator statistics.

Mitigation: Review the documented endpoint scope and use the skill only when those data features fit the task.

Risk: The service receives the SUPERAGNT_API_KEY used for API requests.

Mitigation: Use the skill only if you trust the external service to handle the key, and keep the key in the designated environment variable.

## Reference(s):

- [TikTok Data documentation](https://superagnt.com/r/ch-tiktok-data-docs)
- [TikTok Data MCP server](https://mcp.superagnt.com/mcp/tiktok)
- [TikTok Data on ClawHub](https://clawhub.ai/superagnt/skills/tiktok-data)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [Structured JSON returned by TikTok data endpoints, with Markdown instructions and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live API access requires SUPERAGNT_API_KEY and available service credits.]

## Skill Version(s):

2.0.14 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
