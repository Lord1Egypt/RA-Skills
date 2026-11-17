## Description: <br>
Docker核心操作免费版 helps agents generate and run core Docker commands for container lifecycle management, image operations, and basic debugging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to ask an agent for common Docker container, image, and debugging workflows. It is aimed at personal development, learning, and routine container operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead an agent to execute state-changing Docker commands such as removing containers or images, pruning resources, running containers with ports, or binding host directories. <br>
Mitigation: Review generated Docker commands before execution and require explicit user approval for destructive operations, bind mounts, exposed ports, and third-party image pulls or runs. <br>
Risk: ClawScan reports the release as suspicious because the skill describes executing Docker commands without clear confirmation or safety boundaries. <br>
Mitigation: Use it only in Docker environments where agent-assisted command execution is acceptable, and keep Docker Engine, images, credentials, and project directories scoped to the intended task. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/docker-essentials-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Docker shell commands and optional JSON-style status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose and execute Docker commands through an agent with read, exec, and write tool access.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence; artifact frontmatter reports 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
