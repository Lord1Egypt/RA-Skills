## Description: <br>
Automated development workflow with task board management, code quality checks, and continuous improvement for scheduled auto-coding projects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lgugeng](https://clawhub.ai/user/lgugeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to run scheduled, task-board-driven repository improvement cycles. The workflow reads TASKS.md, selects one pending task, edits code, runs quality checks and tests, commits or pushes changes, and reports the result. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The default workflow can discard local repository changes during forced synchronization. <br>
Mitigation: Use it only in disposable or well-backed-up repositories, require a clean working tree or backup branch, and remove or gate any git reset --hard step before unattended runs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lgugeng/easyclass-auto-improve) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown status reports with code, shell command, and configuration changes as needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires git and python3; designed for bounded runs that handle one task and up to four file changes per cycle.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
