## Description: <br>
AI-optimized web search via Bailian(Alibaba ModelStdio) API. Returns multisourced, concise web search results for LLMs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krisyejh](https://clawhub.ai/user/krisyejh) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to run Bailian/DashScope web searches from an agent workflow and return concise, multi-source search results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to Bailian/DashScope and may include sensitive user or business information. <br>
Mitigation: Avoid submitting secrets or confidential business data in queries, and install only if the deployment trusts Bailian/DashScope for search processing. <br>
Risk: The skill uses a DashScope API key and may affect quota or billing. <br>
Mitigation: Use a dedicated DashScope API key where possible and monitor quota and billing for the account. <br>


## Reference(s): <br>
- [Bailian WebSearch MCP Marketplace Page](https://bailian.console.aliyun.com/cn-beijing?tab=app#/mcp-market/detail/WebSearch) <br>
- [DashScope WebSearch MCP Endpoint](https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp) <br>
- [ClawHub Skill Page](https://clawhub.ai/krisyejh/bailian-web-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell command examples and JSON-formatted API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires bash, curl, jq, and the DASHSCOPE_API_KEY environment variable; accepts a query and optional result count with a default of 5 and maximum of 20.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
