## Description: <br>
Automates programming tasks with the Claude Code CLI, including code generation, bug fixing, project creation, and validation steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wenlavril](https://clawhub.ai/user/wenlavril) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers use this skill to delegate implementation, bug fixing, and project creation tasks to Claude Code CLI while tracking progress and validation results in TASKS.md. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs agents to run Claude Code CLI with approval safeguards bypassed during broad programming tasks. <br>
Mitigation: Use only in trusted repositories, remove or avoid the approval-bypass flag where possible, verify the local claude binary, and require explicit confirmation before file edits, command execution, server starts, or Git commits. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown status summaries with inline shell commands and generated code or file changes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify files, run validation commands, start development servers, and summarize test results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
