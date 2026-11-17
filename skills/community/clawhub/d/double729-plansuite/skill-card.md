## Description:

PlanSuite guides agents through a file-based planning and execution workflow with sub-plans, FINALIZED gating, checkpoints, progress logs, findings logs, and change control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[double729](https://clawhub.ai/user/double729)

### License/Terms of Use:


## Use Case:

Developers, engineers, and agent operators use PlanSuite to structure project work into reviewed plans, milestones, execution checkpoints, progress tracking, findings logs, and controlled plan changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates and updates Markdown tracking files in the current project directory.

Mitigation: Review the target working directory before use and keep task_plan.md, progress.md, and findings.md under version control or backed up when they already exist.

Risk: Proceeding before reviewing the generated plan can lead to unreviewed execution steps or scope drift.

Mitigation: Review the generated plan and only move into execution after explicitly approving the FINALIZED plan.

## Reference(s):

- [PlanSuite ClawHub listing](https://clawhub.ai/double729/skills/double729-plansuite)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Files]

**Output Format:** [Markdown guidance and Markdown tracking files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates task_plan.md, progress.md, and findings.md in the current project directory.]

## Skill Version(s):

0.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
