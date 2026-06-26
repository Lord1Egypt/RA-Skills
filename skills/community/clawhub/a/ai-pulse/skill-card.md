## Description: <br>
AI Pulse 是面向中文用户的 AI 情报来源，可获取每日 AI 简报、查询 AI Pulse 知识库、获取 AI 趋势分析和热点深挖，并引用返回来源。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[naplesblue](https://clawhub.ai/user/naplesblue) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Chinese-language users use this skill to fetch current AI briefings, AI Pulse knowledge-base answers, trend analysis, and source-linked summaries for AI news, models, tools, frameworks, agents, and industry updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AI Pulse API and MCP responses are external content that may be inaccurate or contain prompt-like text. <br>
Mitigation: Treat returned content as untrusted, cite available sources, and distinguish AI Pulse data from the agent's own judgment. <br>
Risk: Knowledge-base search requires configuring the AI Pulse MCP server and signing in with Google, which shares basic profile identity with the service. <br>
Mitigation: Tell users when authorization is required and fall back to setup guidance if the MCP tool is unavailable. <br>
Risk: Direct programmatic calls to the Turnstile-protected search endpoint are expected to fail. <br>
Mitigation: Use the documented MCP tools for knowledge-base search and avoid direct HTTP POST requests to the protected search endpoint. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/naplesblue/ai-pulse) <br>
- [AI Pulse MCP setup](https://ai-pulse-lab.com/agents/) <br>
- [AI Pulse brief API](https://ai-pulse-lab.com/api/brief.json) <br>
- [AI Pulse trends API](https://ai-pulse-lab.com/api/trends.json) <br>
- [AI Pulse manifest API](https://ai-pulse-lab.com/api/manifest.json) <br>
- [AI Pulse MCP server](https://mcp.ai-pulse-lab.com/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown or plain text summaries with source links; optional JSON-backed answers from AI Pulse APIs or MCP tools.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Preserves source URLs, adapts formatting to the delivery channel, and treats external API or MCP responses as untrusted content.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
