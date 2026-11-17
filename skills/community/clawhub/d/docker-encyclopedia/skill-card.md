## Description:

Docker Encyclopedia gives agents a documentation-first workflow for Docker-specific questions, troubleshooting, command planning, builds, runtime operations, Compose, networking, volumes, registries, and diagnostics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kklouzal](https://clawhub.ai/user/kklouzal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when an agent needs grounded Docker help, including command planning, Dockerfile and BuildKit work, Compose review, runtime troubleshooting, and Docker environment diagnostics. The skill directs the agent to prefer cached or freshly consulted official Docker documentation and to record useful workspace-local operational notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may save persistent workspace-local Docker notes that could accidentally include secrets, private registry credentials, tokens, or private URLs.

Mitigation: Keep notes high-level and redact or omit credentials, tokens, private URLs, and other secret material before writing to .Docker-Encyclopedia/.

Risk: Docker operations proposed through the workflow can affect running containers, volumes, networks, registries, credential paths, or daemon configuration.

Mitigation: Review proposed Docker commands and configuration changes before execution, consult the relevant official Docker documentation, and inspect current state before high-impact changes.

Risk: Cached documentation and local observations can become stale or be mistaken for official behavior.

Mitigation: Distinguish official documentation, observed local state, and inference in answers or notes, and refresh official Docker docs when syntax, feature boundaries, or version-sensitive behavior matters.

## Reference(s):

- [Docker Documentation](https://docs.docker.com/)
- [Docker Encyclopedia Workflow](references/workflow.md)
- [Docker Encyclopedia Cache Layout](references/cache-layout.md)
- [Docker Topic Map](references/topic-map.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with inline code and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create workspace-local Docker documentation cache and operational note files under .Docker-Encyclopedia/.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
