## Description:

Unified real-time search MCP server supporting general web search, vertical domain search, parallel batch search, and full-page URL content extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anysearch-ai](https://clawhub.ai/user/anysearch-ai)

### License/Terms of Use:

Apache 2.0

## Use Case:

External developers and agent users use this skill to connect agents to AnySearch for real-time web search, vertical domain search, batch search, and page content extraction. It supports anonymous access with lower rate limits and optional API-key configuration for higher limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AnySearch may receive search queries, extracted URLs, and any email provided for account creation.

Mitigation: Use anonymous access when appropriate, confirm before creating an account, and avoid submitting sensitive queries, URLs, or personal data unless that data sharing is acceptable.

Risk: API keys can be exposed through shell history, logs, or committed configuration files.

Mitigation: Store API keys in environment variables or local ignored files, keep them out of command history and logs, and rotate keys if exposure is suspected.

Risk: Unpinned npx proxy commands may execute newer proxy package versions than the user reviewed.

Mitigation: Prefer native Streamable HTTP mode where supported, or pin and review proxy package versions before use.

## Reference(s):

- [AnySearch MCP ClawHub page](https://clawhub.ai/anysearch-ai/skills/anysearch-mcp)
- [AnySearch publisher profile](https://clawhub.ai/user/anysearch-ai)
- [AnySearch API keys console](https://anysearch.com/console/api-keys)
- [mcp-remote proxy](https://github.com/geelen/mcp-remote)
- [supergateway proxy](https://github.com/supercorp-ai/supergateway)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON configuration examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API key setup guidance, MCP transport configuration, search results, extracted page content, and user-facing error handling guidance.]

## Skill Version(s):

2.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
