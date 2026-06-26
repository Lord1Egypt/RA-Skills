## Description: <br>
Unified planning and execution workflow that creates a file-based plan with sub-plans, freezes it as FINALIZED, and executes in a separate session with checkpoints and progress and findings logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[double729](https://clawhub.ai/user/double729) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and project maintainers use PlanSuite to create structured implementation plans, freeze approved milestones, and track execution progress, findings, validation steps, and rollback notes across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PlanSuite creates and updates task_plan.md, progress.md, and findings.md in the active working directory, which may conflict with existing files of the same names. <br>
Mitigation: Check the working directory for existing planning files before use and review generated updates before relying on them. <br>
Risk: Planning and progress files may contain project-sensitive context if users include secrets, credentials, or private implementation details. <br>
Mitigation: Do not place secrets or credentials in the generated planning files, and review the files before sharing or publishing the workspace. <br>


## Reference(s): <br>
- [PlanSuite on ClawHub](https://clawhub.ai/double729/double729-plansuite) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Configuration] <br>
**Output Format:** [Markdown planning files and concise agent guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or maintains task_plan.md, progress.md, and findings.md in the active working directory.] <br>

## Skill Version(s): <br>
0.2.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
