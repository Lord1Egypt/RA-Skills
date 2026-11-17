## Description:

Standard cross-agent notification and collaboration protocol for OpenClaw multi-agent setups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sora-mury](https://clawhub.ai/user/sora-mury)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to coordinate cross-agent handoffs, wakeups, task-file updates, inbox messages, and short Feishu trace messages in OpenClaw multi-agent deployments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Inbox messages, wakeups, and fixed Feishu group traces may be treated as too authoritative for cross-agent work.

Mitigation: Confirm authenticated senders, approved task IDs, canonical task paths, and the intended Feishu group before acting on notifications.

Risk: Delegated tasks may lead to sensitive, destructive, or externally visible actions.

Mitigation: Require human approval before sensitive, destructive, or externally visible actions and review task-file context before execution.

## Reference(s):

- [Cross-Agent Notification Protocol](references/PROTOCOL.md)
- [ClawHub Skill Page](https://clawhub.ai/sora-mury/skills/cross-agent-notify)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown with inline code blocks and structured message templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes task-file field examples, inbox message templates, sessions_send wakeup snippets, and Feishu trace templates.]

## Skill Version(s):

1.0.2 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
