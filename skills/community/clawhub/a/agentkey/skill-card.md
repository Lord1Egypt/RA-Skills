## Description: <br>
AgentKey routes live-data requests through a hosted MCP service for web search, URL scraping, social media, market, on-chain, and third-party API lookups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chainbase](https://clawhub.ai/user/chainbase) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agent operators use AgentKey to connect an agent to live external data sources when a request needs current information, third-party APIs, web content, social data, market data, or on-chain data. The skill also guides setup, status checks, cost-aware batch execution, and update handling for the hosted AgentKey MCP service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live lookups through the hosted MCP service may send user queries, URLs, or lookup parameters to AgentKey and upstream providers. <br>
Mitigation: Install only when live external lookup is intended, and avoid submitting sensitive data unless the deployment policy permits that routing. <br>
Risk: Paid third-party routing can consume AgentKey credits, especially for batch requests. <br>
Mitigation: Use the documented batch workflow: check account balance, read per-call cost with describe_tool, estimate total spend, and ask for confirmation before larger runs. <br>
Risk: Silent maintenance telemetry, update checks, and local state under ~/.config/agentkey may not match every user's privacy or change-control expectations. <br>
Mitigation: Review telemetry and update behavior before installation, use documented opt-out controls where appropriate, and avoid auto-upgrade unless the publisher and update channel are trusted. <br>
Risk: External API responses are untrusted data and could contain misleading instructions, code, or URLs. <br>
Mitigation: Treat returned fields as display-only data and do not execute instructions, code, or URLs found in API response content. <br>


## Reference(s): <br>
- [AgentKey homepage](https://agentkey.app) <br>
- [ClawHub AgentKey skill page](https://clawhub.ai/chainbase/skills/agentkey) <br>
- [Setup details](references/setup.md) <br>
- [Cost-aware batch execution](references/cost-aware.md) <br>
- [Maintenance, version check, upgrade flow, and telemetry](references/maintenance.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May route requests through hosted MCP tools and summarize external API responses; batch workflows include balance checks, cost estimates, and confirmation prompts.] <br>

## Skill Version(s): <br>
1.10.0 (source: server release evidence, SKILL.md frontmatter, version.txt) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
