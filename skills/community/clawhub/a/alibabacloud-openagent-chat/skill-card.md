## Description:

Work with real Alibaba Cloud resources through OpenAgent conversations. Use for cloud inventory, permissions, security, architecture, costs, migration, and resource changes, including first-time connection and credential-source setup. Use it to list or inspect OpenAgent conversations, answer their questions, check task progress, cancel a task, or recover saved results. Prefer it for cloud tasks that need planning, user decisions, execution, and verification. General cloud explanations that need no account access do not require this skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to manage Alibaba Cloud work through OpenAgent conversations, including resource inspection or changes, connection setup, approvals, task recovery, and result verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud-side actions may exceed the user's intended resource scope.

Mitigation: Use narrowly scoped permissions and obtain authorization for the exact resource changes.

Risk: Secrets could be exposed in chat or handled through an unintended credential source.

Mitigation: Keep secrets out of chat and use only the selected official SDK credential source.

Risk: Stopping observation may leave cloud work running.

Mitigation: Use task cancellation when needed and verify the original task's status and outcome.

## Reference(s):

- [OpenAgent Skill connection setup](references/setup.md)
- [Tasks, conversations, and recovery](references/tasks.md)
- [OpenAgent client API permissions](references/ram-policies.md)
- [ClawHub skill release](https://clawhub.ai/sdk-team/skills/alibabacloud-openagent-chat)

## Skill Output:

**Output Type(s):** [Text, Guidance, API Calls, Shell commands, Configuration instructions]

**Output Format:** [Markdown with command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include verified cloud-task results and concise setup or authorization guidance.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
