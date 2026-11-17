## Description:

Brave Search MCP Server connects agents to Brave Search for web, image, video, news, and local point-of-interest search with API-backed summarization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[buddhasource](https://clawhub.ai/user/buddhasource)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to connect agents to Brave Search for web, image, video, news, local point-of-interest search, fact checking, research, and content discovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install path can run mutable external npm or GitHub code.

Mitigation: Pin the MCP package version or Git commit, avoid auto-fetching latest code with npx on each run, and review updates before deployment.

Risk: Search queries and local search locations are sent to Brave's API.

Mitigation: Avoid sending sensitive searches or precise locations unless that data sharing is acceptable for the deployment.

Risk: The MCP server requires an API key at runtime.

Mitigation: Store BRAVE_API_KEY in the MCP client's secret or environment management system and run the server with least privilege.

## Reference(s):

- [Brave Search API](https://brave.com/search/api/)
- [Official Brave Search MCP Server](https://github.com/brave/brave-search-mcp-server)
- [Brave Search](https://search.brave.com)
- [ClawHub Skill Page](https://clawhub.ai/buddhasource/skills/brave-search-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Brave Search API key for runtime use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
