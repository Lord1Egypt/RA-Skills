## Description:

Helper for using the Docker CLI to build, run, stop, inspect, and manage containers and images. Use when the user wants to perform container-related tasks from the command line, such as building images, running services, cleaning up resources, or checking logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlang-cn](https://clawhub.ai/user/openlang-cn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to get Docker CLI guidance for building images, running containers, inspecting Docker resources, viewing logs, troubleshooting common issues, and cleaning up resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Docker run commands can mount host paths, expose ports, or run third-party images with local permissions.

Mitigation: Review image sources, volume mounts, port mappings, and runtime flags before approving execution.

Risk: Cleanup commands such as docker rm, docker rmi, docker volume rm, and docker system prune can delete containers, images, volumes, networks, or cached build resources.

Mitigation: Use read-only inspection commands first and require explicit confirmation before destructive cleanup.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/openlang-cn/skills/docker-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Docker commands are user-reviewed suggestions before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
