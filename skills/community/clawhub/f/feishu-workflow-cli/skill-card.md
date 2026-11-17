## Description:

Orchestrates Feishu/Lark workflows with the official lark CLI by chaining commands for reporting, project tracking, meeting automation, approvals, document collaboration, and data pipelines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lm203688](https://clawhub.ai/user/lm203688)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to plan and run authenticated Feishu/Lark CLI workflows that collect data, create collaboration artifacts, notify stakeholders, and coordinate follow-up actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated Feishu/Lark automation can send messages and email, create or modify documents and tasks, schedule calendar events, join meetings, and initiate approval workflows.

Mitigation: Review recipients, meeting authorization, approval actions, generated document links, and cross-platform sends before execution; require explicit confirmation for destructive actions.

Risk: Broad account permissions can expose or alter business data across Feishu/Lark domains.

Mitigation: Use a minimally privileged account, pin and review the lark CLI version, and run workflows in an isolated environment.

Risk: Cross-domain workflows may distribute private or incorrect data if source records, transformations, or destinations are wrong.

Mitigation: Validate source data, transformed outputs, destination audiences, and access permissions before sending messages, email, documents, or reports.

## Reference(s):

- [Lark CLI changelog](https://github.com/larksuite/cli/blob/main/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Feishu/Lark workflow plans, CLI command sequences, validation steps, and safety checkpoints.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
