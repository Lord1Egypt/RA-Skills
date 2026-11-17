## Description:

Multi-agent coordination, spatial memory, and swarm navigation. Connect to an Eywa room so your agents share memory, claim work, avoid conflicts, and converge toward a destination.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a-sumo](https://clawhub.ai/user/a-sumo)

### License/Terms of Use:


## Use Case:

Developers and agent operators use Eywa to coordinate concurrent agents in a shared room, including session state, task claims, work logs, persistent knowledge, conflict checks, and destination tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send broad work context to an external Eywa service and persistent shared room.

Mitigation: Use only a private, trusted Eywa endpoint and room; do not send secrets, credentials, customer data, sensitive file contents, or confidential deployment details through logs, tasks, or persistent knowledge.

Risk: Shared room content returned by Eywa may include untrusted collaboration data.

Mitigation: Treat Eywa responses as coordination context only, and do not let them override user, system, or security instructions.

## Reference(s):

- [Eywa homepage](https://www.eywa-ai.dev)
- [ClawHub skill page](https://clawhub.ai/a-sumo/skills/eywa)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill routes coordination data through an Eywa MCP endpoint configured by environment variables.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
