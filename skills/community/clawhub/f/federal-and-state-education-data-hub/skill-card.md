## Description: <br>
Provides a natural-language interface for querying World Bank education statistics by country or region, education level, time period, and optional equity or capacity indicators. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill to call an AgentPMT-hosted education data tool for country, regional, literacy, enrollment, gender parity, completion, pupil-teacher ratio, and SDG 4 analysis workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Calls use an external hosted AgentPMT service and may consume credits. <br>
Mitigation: Confirm trust in AgentPMT before installation and use the recommended setup flow so credentials and payment material are not placed in prompts or logs. <br>
Risk: Education data availability varies by country and indicator, and the most recent values may lag the current year. <br>
Mitigation: Check returned metadata, available flags, and timestamps before using results for policy, benchmarking, or reporting decisions. <br>
Risk: Country or region names that cannot be resolved cause the tool call to fail. <br>
Mitigation: Use plain-English country or region names, preserve request parameters on failure, and fetch the live schema or instructions before retrying unclear requests. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/agentpmt/skills/federal-and-state-education-data-hub) <br>
- [AgentPMT Marketplace Product](https://www.agentpmt.com/marketplace/education-statistics-literacy) <br>
- [Generated Action Schema](artifact/schema.md) <br>
- [AgentPMT Account MCP/REST Setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup) <br>
- [What AgentPMT Is](https://clawhub.ai/agentpmt/what-is-agentpmt) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, JSON, configuration] <br>
**Output Format:** [Markdown instructions with JSON request and response structures] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces tool-call guidance for a hosted AgentPMT education data service; calls may consume credits and require account setup.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
