## Description: <br>
AutoGrind directs an agent to keep working through repeated autonomous planning, execution, validation, reflection, and pause cycles until the user gives an explicit stop signal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ttttonyhe](https://clawhub.ai/user/ttttonyhe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, writers, and other agent users use AutoGrind when they want an agent to continue improving a project autonomously across repeated cycles until an explicit stop signal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to continue acting autonomously and may keep working longer than intended. <br>
Mitigation: Set a maximum runtime or cycle count, define the exact stop phrase, and require confirmation for actions outside the approved scope before invoking the skill. <br>
Risk: Autonomous operation with broad permissions can modify sensitive files, accounts, or services. <br>
Mitigation: Restrict allowed directories, commands, network access, and external services; avoid sensitive repositories or accounts with broad write privileges. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ttttonyhe/autogrind) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/ttttonyhe) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown progress updates, task plans, code or file changes, and shell command invocations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs repeated autonomous cycles with a 60-second inter-cycle pause until an explicit stop signal.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
