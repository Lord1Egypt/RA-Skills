## Description: <br>
Provides AI agents with instructions for retrieving current air quality, pollutant, pollen forecast, historical trend, and map data through AgentPMT-hosted remote tool calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to guide agents that check air quality and pollen conditions, compare locations, plan outdoor activity, assess travel destinations, and generate short-lived environmental map outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Location requests can send addresses or coordinates to AgentPMT, including potentially sensitive home, workplace, or travel locations. <br>
Mitigation: Use only the location precision needed for the task, avoid precise sensitive places unless necessary, and confirm users are comfortable sharing the requested locations. <br>
Risk: Generated map URLs are stored for 7 days and may expose requested environmental overlays for the selected locations. <br>
Mitigation: Share map links only with intended recipients and avoid generating maps for sensitive locations unless the persistence window is acceptable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/agentpmt/skills/air-quality-pollen-information) <br>
- [AgentPMT Marketplace Page](https://www.agentpmt.com/marketplace/air-quality-pollen-information) <br>
- [Generated Action Schema](artifact/schema.md) <br>
- [AgentPMT Account MCP/REST Setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Configuration] <br>
**Output Format:** [Markdown instructions with JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides AgentPMT-hosted remote calls that return JSON data and 7-day map download URLs when map generation is requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
