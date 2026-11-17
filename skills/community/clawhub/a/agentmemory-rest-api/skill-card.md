## Description:

The agentmemory HTTP REST API surface is the primary protocol for talking to the memory server when calling agentmemory over HTTP, using MCP fallback, or integrating a host that does not speak MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rohitg00](https://clawhub.ai/user/rohitg00)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call an agentmemory REST service over HTTP for memory liveness, save, recall, and related operations when MCP is unavailable or an HTTP integration is needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local REST service is open by default on localhost and may expose stored memory to other local processes or shared environments.

Mitigation: Enable AGENTMEMORY_SECRET for shared or sensitive environments, keep the service bound to localhost, and avoid storing secrets or private data unless access to the memory server is understood.

## Reference(s):

- [Server-resolved source import](https://github.com/rohitg00/agentmemory/tree/main/plugin/skills/agentmemory-rest-api)
- [ClawHub skill page](https://clawhub.ai/rohitg00/skills/agentmemory-rest-api)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes HTTP endpoint conventions and authentication guidance for localhost agentmemory REST calls.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
