## Description: <br>
Provides DingTalk-based web search and real-time information retrieval with keyword search, freshness filters, custom result counts, and optional JSON output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[breath57](https://clawhub.ai/user/breath57) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search current web information through a DingTalk MCP endpoint. It supports technical research, current-event lookup, time-filtered queries, and JSON-formatted search results for follow-on analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local search helper can persist MCP connection settings for later use. <br>
Mitigation: Use explicit invocation, avoid saving tokens or private server URLs, and review or remove the saved configuration after setup. <br>
Risk: The skill runs a local shell helper to contact an external MCP search endpoint. <br>
Mitigation: Review the helper script before deployment and run connectivity checks before using it for search tasks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/breath57/dingtalk-ai-web-search) <br>
- [Publisher profile](https://clawhub.ai/user/breath57) <br>
- [DingTalk MCP configuration page](https://mcp.dingtalk.com/#/detail?detailType=instanceMcpDetail&instanceId=78440) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and optional JSON search results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports result count and freshness filters; JSON output includes title, URL, snippet, site, published date, and source when available.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
