## Description: <br>
Complex Math Tool provides AgentPMT-hosted math operations for percentages, ratios, rounding, random numbers, aggregates, and greatest common divisor calculations, returning both formatted and raw values. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call AgentPMT-hosted math utilities for business, finance, data analysis, testing, and everyday calculation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AgentPMT setup may involve account secrets, wallet material, signatures, or payment headers. <br>
Mitigation: Use the AgentPMT setup skill for credential handling and do not place secrets or wallet material in prompts or logs. <br>
Risk: Repeated automated calls can consume AgentPMT credits. <br>
Mitigation: Confirm credit costs and add workflow limits before allowing repeated unattended calls. <br>
Risk: Remote schema, parameters, examples, or endpoint behavior can change after the artifact update date. <br>
Mitigation: Fetch live schema or instructions before production integration when parameters, outputs, or examples are unclear. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/agentpmt/skills/complex-math-tool) <br>
- [AgentPMT Marketplace Page](https://www.agentpmt.com/marketplace/complex-math-tool) <br>
- [Action Schema](artifact/schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON responses with human-readable formatted calculation text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Remote AgentPMT tool calls require the configured AgentPMT MCP or REST setup; product actions are priced at 5 credits each in the artifact schema.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
