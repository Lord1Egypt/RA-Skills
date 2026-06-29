## Description: <br>
Corecoder guides coding agents through precise code edits, parallel file handling, subtask delegation, hazardous-command checks, and local task logging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paudyyin](https://clawhub.ai/user/paudyyin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use Corecoder to structure code-writing, bug-fixing, refactoring, review, and project-analysis workflows with scoped edits, validation, and task logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may run commands, edit workspace files, and spawn subagents as part of normal coding workflows. <br>
Mitigation: Review proposed edits and commands before execution, keep work scoped to the active workspace, and run available tests or validation checks after changes. <br>
Risk: The skill documents local dated memory logs that may contain file paths, bug details, or code-change rationale. <br>
Mitigation: Review, disable, or routinely clean local memory logging when those details are sensitive in the deployment environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/paudyyin/corecoder) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/paudyyin) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code and shell-command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose workspace edits, command execution, subagent tasks, and local memory log entries.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
