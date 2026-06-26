## Description: <br>
AI tool marketplace via AgentForge for discovering, comparing, and executing tools with automatic billing and trust scoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Paparusi](https://clawhub.ai/user/Paparusi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External agents and developers use this skill to discover marketplace tools, inspect schemas, compare price and trust signals, check balance, and execute single or batch tool calls through AgentForge. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paid marketplace tool execution can create unintended spend, especially for batch calls. <br>
Mitigation: Before execution, ask the agent to show the selected tool, provider, schema, exact input, price, and maximum total cost. <br>
Risk: Inputs may be sent to third-party tools selected from the marketplace. <br>
Mitigation: Avoid sending sensitive data unless you understand the destination tool's handling terms. <br>


## Reference(s): <br>
- [A2A Marketplace on ClawHub](https://clawhub.ai/Paparusi/a2a-marketplace) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, JSON] <br>
**Output Format:** [Markdown instructions with JSON examples and tool-call guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May trigger paid third-party tool execution and batch calls through the installed plugin.] <br>

## Skill Version(s): <br>
2.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
