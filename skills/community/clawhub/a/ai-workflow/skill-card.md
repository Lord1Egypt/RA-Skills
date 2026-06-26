## Description: <br>
Auto Workflow helps agents define and run multi-step automation workflows for file operations, data conversion, HTTP requests, shell commands, backups, and related repeatable tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yofoan](https://clawhub.ai/user/yofoan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to automate repeatable local workflows such as backups, file handling, data conversion, HTTP calls, and scripted multi-step jobs. It is best suited for reviewed workflow definitions in controlled workspaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workflow files can exercise broad command, file, network, and environment-variable access. <br>
Mitigation: Review workflow definitions like code before execution, run only trusted workflows, and limit execution to a restricted directory or sandbox. <br>
Risk: Workflow runs may expose more environment data than intended through variable expansion or shell commands. <br>
Mitigation: Provide only the environment variables required for the workflow and avoid running workflows with broad credentials in the process environment. <br>
Risk: Dry-run behavior is documented but should not be assumed to prevent side effects unless verified. <br>
Mitigation: Validate workflows separately and test them in a disposable workspace before using them on important files or systems. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yofoan/ai-workflow) <br>
- [Publisher profile](https://clawhub.ai/user/yofoan) <br>
- [Example backup workflow](examples/backup-workflow.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON workflow examples, shell commands, and Python code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces workflow definitions and command guidance for agent execution; actual workflow runs may create, modify, download, archive, delete, or log files depending on the reviewed workflow.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
