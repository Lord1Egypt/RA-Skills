## Description: <br>
Manage Docker containers, images, volumes, networks, and Docker Compose projects for listing, control, logs, image builds, cleanup, compose authoring, and debugging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ericlooi504](https://clawhub.ai/user/ericlooi504) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, DevOps engineers, and Docker operators use this skill to inspect, operate, troubleshoot, and clean up Docker environments and to draft Docker Compose configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can affect local containers, images, volumes, networks, and services when the user approves stop, remove, or prune commands. <br>
Mitigation: Review exact resource names before approval, and avoid cleanup on important or production Docker hosts unless backups and rollback plans exist. <br>
Risk: Generated Docker Compose files may expose ports, mount volumes, or set image and environment choices that are unsuitable for a deployment. <br>
Mitigation: Review compose YAML, image tags, volume mounts, exposed ports, health checks, and secrets handling before applying generated configuration. <br>
Risk: Docker logs, inspect output, and debugging commands may surface sensitive runtime information. <br>
Mitigation: Inspect output before sharing it and redact credentials, tokens, internal hostnames, or sensitive file paths. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ericlooi504/eric-docker-helper) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and YAML configuration blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Docker and Docker Compose binaries; destructive cleanup and removal commands require user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release.version and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
