## Description:

DuckDuckGo搜索服务 provides DuckDuckGo web search and webpage content fetching through a model context protocol server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to route natural-language search or webpage-fetch requests to the provided search and fetch tools, then summarize the returned raw results for the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search and fetch requests are handled through a third-party XiaoBenYang MCP proxy rather than a direct DuckDuckGo-only implementation.

Mitigation: Review the proxy relationship before use and avoid submitting private URLs, secrets, or confidential search queries.

Risk: The required XiaoBenYang API key may be persisted in a local .env file.

Mitigation: Use a limited, revocable API key and ensure .env is protected and excluded from version control.

Risk: The security summary notes branding and configuration inconsistencies that require review.

Mitigation: Verify the publisher, endpoint, MCP IDs, and expected tool behavior before relying on results.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/alinklab/skills/ddg-search)
- [Publisher Profile](https://clawhub.ai/user/alinklab)
- [XiaoBenYang API Key Site](https://xiaobenyang.com)
- [XiaoBenYang MCP Endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Markdown or text summaries derived from JSON tool responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tool responses include success, raw, and message fields; the agent is expected to present raw results clearly to the user.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
