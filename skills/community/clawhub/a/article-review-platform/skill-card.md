## Description:

Provides a usage guide for a local Article Review Platform that manages article listing, reading, creation, review status updates, publishing status sync, and role-specific review workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mayf3](https://clawhub.ai/user/mayf3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, writers, reviewers, and publishing agents use this skill to operate a local article review workflow from draft creation through review approval and multi-platform publishing updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes commands that create, update, publish, log, or delete article records in the local platform.

Mitigation: Require explicit user confirmation before running POST, PUT, publish-status update, publish-log write, or DELETE commands.

Risk: The DELETE example may permanently remove article records.

Mitigation: Use deletion only when the platform provides backup, soft delete, or recovery, and prefer non-destructive status updates when possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mayf3/skills/article-review-platform)
- [Publisher role guidance](artifact/references/role-publisher.md)
- [Reviewer role guidance](artifact/references/role-reviewer.md)
- [Writer role guidance](artifact/references/role-writer.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline bash commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands target a local service at http://localhost:3100 and may modify article workflow records.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
