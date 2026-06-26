## Description: <br>
Cool Agent Tools helps agents inspect system health, diagnose network issues, process files, review logs, manage processes and Docker, and run common Git checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chuangyinbot-boop](https://clawhub.ai/user/chuangyinbot-boop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill as a command reference for common system administration tasks such as resource checks, network diagnostics, log review, file inspection, process management, Docker inspection, and Git status checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill recommends operations commands that can delete files, terminate processes, change Docker state, or affect system paths. <br>
Mitigation: Require explicit approval before delete, kill, Docker-changing, system-path, or background commands, and ask the agent to preview affected files, processes, and targets. <br>
Risk: Network diagnostic commands may contact outbound hosts supplied during use. <br>
Mitigation: Confirm the destination host or URL before running outbound network checks. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/chuangyinbot-boop/cool-agent-tools) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and command tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may affect local files, processes, Docker resources, system paths, or network targets depending on user approval and execution context.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
