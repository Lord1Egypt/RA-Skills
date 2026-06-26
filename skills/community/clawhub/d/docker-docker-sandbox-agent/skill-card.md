## Description: <br>
A generic skill that provides a secure, temporary Docker sandbox for executing generated code such as Python, Node.js, and shell scripts so agents can verify code without compromising the host machine. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[newtonfrank](https://clawhub.ai/user/newtonfrank) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to run generated Python, Node.js, shell, or other Docker-supported code in temporary containers before presenting results. It is intended for code verification workflows that need host isolation, resource limits, and controlled network access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Containers may expose sensitive host data if broad or sensitive directories are mounted. <br>
Mitigation: Mount only a temporary task folder or another minimal task-specific directory; avoid paths such as /, /etc, and ~/.ssh. <br>
Risk: Executed code may initiate unwanted network access when networking is enabled. <br>
Mitigation: Keep Docker networking disabled with --network none unless network access is required for the specific verification task. <br>
Risk: Unbounded or privileged containers can affect host stability or weaken isolation. <br>
Mitigation: Use CPU and memory limits, avoid privileged containers, and clean up containers after execution. <br>


## Reference(s): <br>
- [ClawHub release page: Docker Sandbox](https://clawhub.ai/newtonfrank/docker-docker-sandbox-agent) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Docker; examples use temporary mounts, container removal, CPU and memory limits, and disabled networking where appropriate.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
