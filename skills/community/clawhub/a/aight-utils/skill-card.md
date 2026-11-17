## Description:

Native Aight app integration for creating reminders, tasks, triggers, and items.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vincenthhao](https://clawhub.ai/user/vincenthhao)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn reminder, deadline, task, and tracking requests into structured Aight items for the user's Today view.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad phrases such as Done or Cancel may cause persistent status changes to existing Aight items.

Mitigation: Require explicit user confirmation and a specific item identifier before changing item status.

Risk: Failed item creation may save reminder or task content into local memory files.

Mitigation: Ask permission before writing fallback memory entries and avoid storing sensitive reminder content.

Risk: The skill examples include a fixed Asia/Shanghai timestamp that may not match the user's actual timezone.

Mitigation: Resolve dates against the user's current timezone before generating scheduled reminder or deadline payloads.

## Reference(s):

- [Aight Utils on ClawHub](https://clawhub.ai/vincenthhao/skills/aight-utils)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with structured JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Aight reminder, task, trigger, process, and status-update payload guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
