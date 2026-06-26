## Description: <br>
Essential Docker commands and workflows for container management, image operations, and debugging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a2mus](https://clawhub.ai/user/a2mus) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill as a concise Docker command reference for container lifecycle tasks, image management, debugging, Docker Compose workflows, networking, volumes, and system cleanup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Some referenced Docker commands can remove containers, images, networks, volumes, or other local Docker resources if run carelessly. <br>
Mitigation: Review container, image, network, and volume names before running destructive commands such as prune, rm, rmi, or compose down -v. <br>
Risk: Commands that mount host paths, push images, or open root shells can expose local files, publish unintended images, or alter container state. <br>
Mitigation: Verify host mount paths, registry targets, and shell user context before executing these examples. <br>


## Reference(s): <br>
- [Docker Documentation](https://docs.docker.com/) <br>
- [Dockerfile Reference](https://docs.docker.com/engine/reference/builder/) <br>
- [Compose File Reference](https://docs.docker.com/compose/compose-file/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown with inline bash and Dockerfile code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Docker for command execution; examples should be reviewed before running against local containers, images, networks, volumes, or registries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
