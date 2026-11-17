## Description:

Cancel a task on OpenAnt and reclaim escrowed funds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ant-1984](https://clawhub.ai/user/ant-1984)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenAnt task creators use this skill to inspect a task they created, confirm whether it can be cancelled, cancel it through the OpenAnt CLI, and verify escrow refund status when applicable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a mutable CLI package for OpenAnt task inspection and cancellation.

Mitigation: Pin the CLI to a reviewed version where possible before installation or use.

Risk: Task cancellation is irreversible and may trigger escrow refund behavior.

Mitigation: Confirm the exact task title, status, and reward with the user before running the cancellation command.

Risk: Untrusted text could supply an unsafe or incorrect task ID.

Mitigation: Accept only task IDs that match the platform's expected format and verify the task with a read-only command before cancellation.

## Reference(s):

- [Cancel Task on ClawHub](https://clawhub.ai/ant-1984/skills/cancel-task)
- [Publisher Profile](https://clawhub.ai/user/ant-1984)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Text]

**Output Format:** [Markdown with inline bash commands and JSON command-output checks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user confirmation before running the cancellation command.]

## Skill Version(s):

0.1.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
