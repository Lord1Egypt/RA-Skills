## Description: <br>
Runs a cost-benefit audit workflow that collects full-scope costs, estimates benefits, compares inputs and outputs, simulates sensitivity, and prepares an audit report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rc17777](https://clawhub.ai/user/rc17777) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and audit practitioners use this skill to run a structured cost-benefit audit workflow for a named project, including cost collection, benefit measurement, comparative analysis, sensitivity analysis, and final report generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Project-local operator and development workflows can affect real users or production data when run with authenticated admin credentials. <br>
Mitigation: Install only for intended ClawHub operator or development workflows, and review affected maintenance, moderation, content-rights, and migration actions before use. <br>
Risk: High-impact actions are available in the skill bundle but are gated by explicit user control. <br>
Mitigation: Require explicit operator approval before executing workflow steps that send email, change production data, or affect user-facing records. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rc17777/audit-cost-benefit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and workflow configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a staged audit workflow and final cost-benefit analysis report; requires project context such as project name, implementing unit, and evaluation period.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
