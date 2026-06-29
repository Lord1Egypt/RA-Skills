## Description: <br>
Complex Mathematics Engine evaluates mathematical expressions using SymPy for symbolic math, NumPy for numerical work, and SciPy for scientific computing through AgentPMT-hosted remote tool calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to submit mathematical expressions for arithmetic, calculus, algebra, linear algebra, statistics, equation solving, and scientific-computing tasks. It is appropriate when the agent should route a math expression to AgentPMT and consume the returned JSON result. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mathematical expression text is sent to AgentPMT for remote processing. <br>
Mitigation: Send only the expression needed for the calculation and exclude secrets, wallet data, credentials, and unrelated private content. <br>
Risk: Broad activation terms could cause an agent to invoke the skill on generic calculation requests. <br>
Mitigation: Narrow local activation behavior or require an explicit user confirmation before sending content to AgentPMT. <br>
Risk: Using the remote calculate action may spend AgentPMT credits. <br>
Mitigation: Confirm the intended AgentPMT account, enabled tool, and credit impact before production use. <br>


## Reference(s): <br>
- [Complex Mathematics Engine schema](artifact/schema.md) <br>
- [Complex Mathematics Engine marketplace page](https://www.agentpmt.com/marketplace/complex-mathematics-engine) <br>
- [Complex Mathematics Engine on ClawHub](https://clawhub.ai/agentpmt/complex-mathematics-engine) <br>
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup) <br>
- [What AgentPMT is](https://clawhub.ai/agentpmt/what-is-agentpmt) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands, API calls, JSON] <br>
**Output Format:** [Markdown instructions with JSON request and response shapes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces AgentPMT invocation guidance for a single calculate action; tool responses include the original expression, engine used, execution time, result, result string, and metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
