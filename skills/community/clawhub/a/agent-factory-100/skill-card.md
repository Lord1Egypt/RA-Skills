## Description: <br>
Rapidly spawns and configures specialized sub-agents, including Research, Coding, and Analysis templates, with workspace setup and instruction delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Keyserkazi1](https://clawhub.ai/user/Keyserkazi1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to scaffold specialized sub-agent folders, inbox/outbox communication directories, workspaces, and starter instructions for delegated coding, research, and analysis tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scaffold script uses the provided agent name to create local directories. <br>
Mitigation: Use simple agent names without slashes or path traversal and review generated paths before use. <br>
Risk: Role descriptions become part of the generated agent instructions. <br>
Mitigation: Review role descriptions before using generated sub-agents. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with a shell script that writes local skill files and folders] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local agent directories under agents/<name> with inbox, outbox, workspace, and SKILL.md files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
