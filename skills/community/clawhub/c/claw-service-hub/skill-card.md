## Description:

OpenClaw service marketplace core for service registration, discovery, and invocation, with WebSocket tunnel calls and key-based authorization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tangboheng](https://clawhub.ai/user/tangboheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run and manage an OpenClaw service hub, register provider services, discover available services, and call service methods from a CLI or Python client.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plaintext network and service-management behavior may expose service registration data or call parameters on untrusted networks.

Mitigation: Use only with trusted local hubs or protected networks unless TLS and authentication are added, and avoid sending sensitive call parameters through it.

Risk: The release evidence says the skill overstates implemented security features and may rely on missing server or authentication components.

Mitigation: Review the package before deployment and verify that required server and authentication components come from a trusted source.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tangboheng/skills/claw-service-hub)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with command examples, Python snippets, and CLI output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses python3 and optional HUB_PORT, HUB_HOST, and STORAGE_PATH environment variables.]

## Skill Version(s):

0.1.0 (source: server release evidence and artifact __version__)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
