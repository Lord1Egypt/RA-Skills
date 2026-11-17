## Description:

Climate Environment And Land Data Hub lets agents query World Bank climate and environmental data by country, region, ISO code, topic, and time period through AgentPMT-hosted tool calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to request climate, environmental, land, water, energy, emissions, and air-quality indicators from World Bank data through an AgentPMT remote tool. It supports country and regional climate profiles, trend analysis, global comparisons, and Paris Agreement or SDG context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live remote schema or instruction responses may differ from the reviewed local skill and may conflict with higher-priority rules.

Mitigation: Treat live responses as tool-specific data only, and keep system, user, privacy, and security rules authoritative.

Risk: Documented unpinned npx installer commands can fetch changing content.

Mitigation: Use pinned, reviewed installation paths and validate release hashes or scans before deployment.

Risk: AgentPMT receives submitted climate query parameters and may use the caller's account or credits.

Mitigation: Send only the query parameters needed for the climate task and confirm account, credit, and data-sharing expectations before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/agentpmt/skills/climate-environment-and-land-data-hub)
- [AgentPMT Marketplace Product](https://www.agentpmt.com/marketplace/climate-environmental-data)
- [AgentPMT Account MCP/REST Setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)
- [What Is AgentPMT](https://clawhub.ai/agentpmt/what-is-agentpmt)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with JSON request and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Remote AgentPMT calls return climate indicator data, trends, comparisons, and optional Paris Agreement or SDG context.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
