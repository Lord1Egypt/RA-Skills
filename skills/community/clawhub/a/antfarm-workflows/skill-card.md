## Description: <br>
Antfarm Workflows provides multi-agent workflow orchestration for OpenClaw feature development, bug fixes, security audits, and workflow lifecycle commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YonghaoZhao722](https://clawhub.ai/user/YonghaoZhao722) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to run autonomous OpenClaw workflow pipelines for feature development, bug fixing, security auditing, and workflow management. It helps agents install workflows, start runs with acceptance criteria, inspect status and logs, resume failed runs, and manage dashboard access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install and run persistent autonomous cron-driven workers through a local Antfarm CLI. <br>
Mitigation: Review the existing Antfarm CLI, cron jobs, dashboard port, database location, and agent workspaces before running install. <br>
Risk: Workflow task text and agent outputs may expose sensitive information in local state or logs. <br>
Mitigation: Avoid putting secrets in workflow task text or agent outputs, and monitor workflow logs while runs are active. <br>
Risk: Uninstall commands may remove workflow state and background jobs. <br>
Mitigation: Use uninstall commands deliberately, confirm the target workflow or all-workflow scope, and preserve needed state before removal. <br>


## Reference(s): <br>
- [Antfarm Workflows on ClawHub](https://clawhub.ai/YonghaoZhao722/antfarm-workflows) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should include clear task scope and acceptance criteria before starting workflow runs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
