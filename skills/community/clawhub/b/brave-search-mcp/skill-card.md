## Description: <br>
Brave Search MCP Server connects AI agents to Brave Search for web, image, video, news, local point-of-interest search, and AI-powered summarization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BuddhaSource](https://clawhub.ai/user/BuddhaSource) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to add Brave-powered current-information search, media discovery, news lookup, local place search, and search-result summarization to MCP-capable agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries, precise locations, and other submitted content may be sent to Brave Search during use. <br>
Mitigation: Avoid sending secrets, confidential business data, or precise personal locations unless the user intends to share them with Brave Search. <br>
Risk: Installation may run npm packages or code from external sources. <br>
Mitigation: Confirm the npm package or repository is Brave-controlled and pin a known version before deployment. <br>
Risk: The skill requires a Brave API key. <br>
Mitigation: Use a dedicated key, store it in the MCP client's environment, and rotate it if exposed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/BuddhaSource/brave-search-mcp) <br>
- [Brave Search API](https://brave.com/search/api/) <br>
- [Brave Search](https://search.brave.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with search-result text, links, and inline configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BRAVE_API_KEY for live Brave Search API access] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
