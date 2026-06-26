## Description: <br>
Provides Docker container and image operations for creating, running, managing, and inspecting containers and images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[netium](https://clawhub.ai/user/netium) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill as an agent-facing Docker CLI reference for container lifecycle, image management, registry operations, cleanup, inspection, and system information tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Docker cleanup, removal, import, bind-mount, push, and login commands can affect local resources, credentials, registries, or sensitive filesystems. <br>
Mitigation: Review commands before execution, avoid production or sensitive hosts without explicit approval, prefer scoped filters and temporary empty directories, and use --password-stdin for credentials. <br>
Risk: The release security verdict is suspicious because the reference includes high-impact Docker examples without enough safety guardrails for agent use. <br>
Mitigation: Treat commands as proposals, require operator supervision for mutating actions, and scan or review the skill before deployment. <br>


## Reference(s): <br>
- [Docker Operations](https://clawhub.ai/netium/docker-operations) <br>
- [Container Lifecycle Commands](references/container-lifecycle.md) <br>
- [Container Interaction Commands](references/container-interaction.md) <br>
- [Container Listing Commands](references/container-listing.md) <br>
- [Image Operations Commands](references/image-operations.md) <br>
- [Image Inspection Commands](references/image-inspection.md) <br>
- [Registry Commands](references/registry.md) <br>
- [Cleanup Commands](references/cleanup.md) <br>
- [Docker Compose Commands](references/compose.md) <br>
- [System Information Commands](references/system-info.md) <br>
- [Advanced Image Operations](references/advanced-image-operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Docker command examples may mutate local containers, images, volumes, registries, and filesystems.] <br>

## Skill Version(s): <br>
0.0.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
