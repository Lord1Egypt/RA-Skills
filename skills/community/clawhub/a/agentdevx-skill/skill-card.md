## Description: <br>
Agentdevx Skill lets agents register and call APIs through the AgentDevX gateway with Ed25519 identity, encrypted credential injection, rate limiting, and audit logging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mirajmahmudul](https://clawhub.ai/user/mirajmahmudul) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to give agents access to registered APIs through a hosted gateway with agent identity, credential routing, rate limiting, and audit logging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automatically registers the agent with AgentDevX and sends outbound requests to a third-party hosted gateway. <br>
Mitigation: Install only where automatic third-party registration is acceptable, and review the AgentDevX dashboard and revocation process before use. <br>
Risk: API calls, credentials stored in the vault, and memory contents may route through AgentDevX. <br>
Mitigation: Avoid sensitive APIs or production credentials until the service trust boundary, dashboard controls, and account deletion process are reviewed. <br>


## Reference(s): <br>
- [AgentDevX Gateway](https://agentdevx.onrender.com) <br>
- [Smithery AgentDevX Server](https://smithery.ai/server/io.github.mirajmahmudul/agentdevx) <br>
- [AgentDevX SDK](https://github.com/mirajmahmudul/agentdevx-sdk) <br>
- [AgentDevX npm Package](https://www.npmjs.com/package/@agentdevx/install) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks; API responses depend on registered APIs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Routes requests through a third-party gateway; API response shape depends on the registered OpenAPI spec.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release metadata; artifact frontmatter says 1.0.6) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
