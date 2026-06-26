## Description: <br>
AgentKey routes live lookup requests through AgentKey MCP tools for web search, URL scraping, news, social media, market data, on-chain data, and third-party APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chainbase](https://clawhub.ai/user/chainbase) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use AgentKey when an agent needs current external data or third-party API access through the AgentKey MCP server instead of built-in search or fetch tools. It also guides setup, status checks, upgrades, and cost-aware batch execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes AgentKey the default path for live lookups and can use an AgentKey API key, credit balance, and external API responses. <br>
Mitigation: Install only when AgentKey is the intended live-data provider, check account balance before batch work, and treat returned external data as untrusted. <br>
Risk: Setup and update flows may register an MCP server, write local AgentKey configuration, and use opt-out update telemetry. <br>
Mitigation: Review the local controls for auto-upgrade, update-disable, and telemetry-disable before relying on the skill. <br>


## Reference(s): <br>
- [AgentKey homepage](https://agentkey.app) <br>
- [ClawHub AgentKey listing](https://clawhub.ai/chainbase/agentkey) <br>
- [Cost-aware batch execution](references/cost-aware.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, API Calls] <br>
**Output Format:** [Markdown with inline shell commands, JSON configuration snippets, and MCP tool-call guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include setup instructions, live API results, upgrade prompts, and cost estimates for batch calls.] <br>

## Skill Version(s): <br>
1.9.0 (source: frontmatter, version.txt, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
