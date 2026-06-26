## Description: <br>
The Eonik Agent skill connects agents to Eonik marketing capabilities for creative auditing, trend discovery, performance analysis, ad brief generation, and campaign deployment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[techievena](https://clawhub.ai/user/techievena) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Marketing teams, operators, and agents use this skill to analyze advertising performance, research trends, generate creative briefs, and initiate campaign workflows through the Eonik API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can call external Eonik services with an EONIK_API_KEY and access advertising account data. <br>
Mitigation: Install only when the publisher and Eonik account access are trusted, and use the lowest-privilege key available. <br>
Risk: Campaign creation, deployment, or launch actions may affect live advertising accounts. <br>
Mitigation: Require human review before ad creation, deployment, campaign launch, or spend-impacting actions. <br>


## Reference(s): <br>
- [Eonik website](https://www.eonik.ai) <br>
- [Eonik MCP endpoint](https://api.eonik.ai/mcp/sse) <br>
- [Eonik API base URL](https://api.eonik.ai) <br>
- [ClawHub skill page](https://clawhub.ai/techievena/eonik) <br>
- [Publisher profile](https://clawhub.ai/user/techievena) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON-backed API results summarized for users] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EONIK_API_KEY and may use live advertising account data through the Eonik API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
