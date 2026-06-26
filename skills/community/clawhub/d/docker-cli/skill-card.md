## Description: <br>
Helper for using the Docker CLI to build, run, stop, inspect, and manage containers and images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlang-cn](https://clawhub.ai/user/openlang-cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill for Docker CLI tasks such as building images, running containers, checking logs, inspecting resources, and cleaning up local Docker state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Docker cleanup commands and remove operations can delete containers, images, volumes, or other local resources. <br>
Mitigation: Review proposed rm, rmi, prune, and volume commands before running them, and use destructive cleanup only when the intended resources are clear. <br>
Risk: Host volume mounts can expose sensitive local files to a container. <br>
Mitigation: Avoid mounting sensitive paths such as home directories, SSH keys, configuration folders, or the filesystem root; use read-only mounts with :ro when practical. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/openlang-cn/docker-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Markdown] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands should be reviewed before execution, especially cleanup operations, detached containers, port mappings, and host volume mounts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
