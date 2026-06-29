## Description: <br>
Climate Environment And Land Data Hub lets agents query World Bank climate and environmental indicators for countries or regions through AgentPMT-hosted remote tool calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill to retrieve country or regional climate profiles, emissions trends, environmental compliance context, and resource or land assessments without working with World Bank indicator codes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tool queries leave the local agent boundary through AgentPMT-hosted remote calls. <br>
Mitigation: Keep requests limited to the country, environmental topic, and time period needed, and avoid including secrets or sensitive internal context. <br>
Risk: Separately installed AgentPMT setup skills handle account, MCP, REST, wallet, or credential configuration. <br>
Mitigation: Review the setup skills before use and follow their credential-handling guidance instead of placing account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs. <br>
Risk: Endpoint schemas, setup steps, or examples may become stale after publication. <br>
Mitigation: Refresh the skill when it is more than seven days past its last updated date, and fetch live schema or instructions before a new production integration. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/agentpmt/skills/climate-environment-and-land-data-hub) <br>
- [AgentPMT Marketplace Product](https://www.agentpmt.com/marketplace/climate-environmental-data) <br>
- [Generated Action Schema](artifact/schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, JSON] <br>
**Output Format:** [Markdown instructions with JSON request examples and remote JSON tool responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Remote lookup returns World Bank climate indicators, trends, global comparisons, and optional Paris Agreement and SDG context.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
