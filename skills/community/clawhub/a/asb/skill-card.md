## Description: <br>
Agent Service Bus provides ASB orchestration and collaboration capabilities through an MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qiyueqiu](https://clawhub.ai/user/qiyueqiu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to connect an agent to Agent Service Bus capabilities for service discovery, service composition, governance, LLM calls, message sending, and task orchestration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill delegates runtime behavior to an external Python package. <br>
Mitigation: Review and trust the upstream Agent-Service-Bus package before installing or enabling the MCP server. <br>
Risk: LLM calls and message sending may be outbound depending on the configured providers and destinations. <br>
Mitigation: Avoid sending sensitive data until providers, destinations, and runtime configuration are understood. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qiyueqiu/asb) <br>
- [Agent Service Bus repository](https://github.com/qiyueqiu/Agent-Service-Bus) <br>
- [Agent Service Bus documentation](https://github.com/qiyueqiu/Agent-Service-Bus/tree/main/docs) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with JSON, Python, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill delegates runtime behavior to the external agent-service-bus Python package.] <br>

## Skill Version(s): <br>
0.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
