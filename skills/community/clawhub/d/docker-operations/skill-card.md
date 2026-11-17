## Description:

Provides Docker container and image operations for creating, running, managing, and inspecting containers and images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[netium](https://clawhub.ai/user/netium)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to get Docker CLI guidance for container lifecycle, image management, registry operations, Compose workflows, inspection, interaction, and cleanup tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Docker cleanup and removal commands can delete containers, images, networks, or volumes.

Mitigation: Require explicit approval before prune, rm, rmi, compose down -v, force flags, or volume deletion commands.

Risk: Registry login and push workflows can expose credentials or publish to the wrong registry.

Mitigation: Use password-stdin or a credential helper, verify registry names, and require approval before push operations.

Risk: Running privileged containers or untrusted images can affect the host environment.

Mitigation: Prefer trusted, pinned images and require explicit approval before privileged execution.

## Reference(s):

- [Advanced Image Operations](references/advanced-image-operations.md)
- [Cleanup Commands](references/cleanup.md)
- [Docker Compose Commands](references/compose.md)
- [Container Interaction Commands](references/container-interaction.md)
- [Container Lifecycle Commands](references/container-lifecycle.md)
- [Container Listing Commands](references/container-listing.md)
- [Image Inspection Commands](references/image-inspection.md)
- [Image Operations Commands](references/image-operations.md)
- [Registry Commands](references/registry.md)
- [System Information Commands](references/system-info.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and command reference tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include destructive Docker operations and should be reviewed before execution.]

## Skill Version(s):

0.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
