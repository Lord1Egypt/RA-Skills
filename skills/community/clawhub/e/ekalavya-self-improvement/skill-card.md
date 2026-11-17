## Description:

Enforce execution discipline for ongoing work after the user has already approved direction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[21f2000735](https://clawhub.ai/user/21f2000735)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to keep an assistant focused on visible approved work, maintain a clean execution queue, adapt around blockers, and promote repeated workflow lessons into durable rules or skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages quieter, more autonomous work after a direction is approved, which may reduce opportunities for user checkpoints on sensitive tasks.

Mitigation: Ask for explicit checkpoints for commits, durable rule changes, skill edits, project-document changes, or other sensitive and high-impact work.

Risk: Autonomous follow-through can continue down an approved path even when a blocker or product decision should be surfaced.

Mitigation: Keep blockers in a separate lane and require user input when credentials, approvals, product choices, or broken environments prevent meaningful progress.

## Reference(s):

- [Execution Queue Protocol](references/execution-queue.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration]

**Output Format:** [Markdown instructions and operating rules]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code, tool calls, credentials, or external services are defined by the artifact.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
