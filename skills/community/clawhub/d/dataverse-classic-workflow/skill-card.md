## Description: <br>
Read, analyze, compare, edit, copy, and publish Microsoft Dataverse Classic Workflows, including WF4/XAML workflow files, custom workflow activity scaffolding, and PAC CLI publishing guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rwilson504](https://clawhub.ai/user/rwilson504) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Dataverse administrators use this skill to inspect, modify, compare, copy, and publish Classic Workflow XAML from Dataverse solutions while preserving workflow designer metadata and reviewing environment-changing commands before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incorrect workflow XAML or logic changes could alter Dataverse automation behavior. <br>
Mitigation: Review every proposed XAML diff before applying changes and preserve workflow designer metadata during edits. <br>
Risk: Publishing, importing, activating, deactivating, Run As, and Scope changes can affect the wrong Dataverse environment or production records. <br>
Mitigation: Confirm the target environment and review every PAC command before execution, with extra caution for production operations. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/rwilson504/dataverse-classic-workflow) <br>
- [Project homepage](https://github.com/rwilson504/agent-skills/tree/main/dataverse-classic-workflow) <br>
- [Microsoft Learn: Classic Dataverse workflows](https://learn.microsoft.com/power-automate/workflow-processes) <br>
- [XAML Anatomy](reference/xaml-anatomy.md) <br>
- [Activity Type Catalog](reference/activity-types.md) <br>
- [Trigger, Scope, Mode, and Run-As Reference](reference/trigger-types.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with XML/XAML, C#, and shell command blocks when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local file edits and Dataverse PAC CLI commands; environment-changing commands require user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
