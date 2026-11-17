## Description:

Debug running Docker containers and Compose services. Use when inspecting container logs, exec-ing into running containers, diagnosing networking issues, checking resource usage, debugging multi-stage builds, troubleshooting health checks, or fixing Compose service dependencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gitgoodordietrying](https://clawhub.ai/user/gitgoodordietrying)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to debug Docker containers and Compose services by inspecting logs, entering containers, diagnosing networking issues, checking resource usage, debugging builds, troubleshooting health checks, and reviewing Compose service dependencies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Container debugging commands can provide powerful access to running containers, host namespaces, network traffic, and cleanup operations.

Mitigation: Require explicit approval before running nsenter, namespace-sharing debug containers, tcpdump sidecars, root exec, or any docker prune command; avoid these commands on production or sensitive containers unless an authorized operator has reviewed the exact command.

Risk: Helper images used for debugging can introduce supply-chain or trust risk.

Mitigation: Pin and verify helper images before use.

## Reference(s):

- [Container Debug on ClawHub](https://clawhub.ai/gitgoodordietrying/skills/container-debug)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown with inline bash, Dockerfile, and YAML code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Docker command-line access; proposed commands may inspect or modify running containers, images, networks, volumes, and host namespaces.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
