## Description:

Local-first execution queue for OpenClaw agents that turns promises into executable tasks, lets agents pick work during heartbeat, maintains a queue inside each workspace, and can dispatch work to another registered agent workspace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoujiejun](https://clawhub.ai/user/zoujiejun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to turn conversational follow-up commitments into workspace-local executable tasks, claim queued work during heartbeat, and explicitly dispatch tasks to other registered OpenClaw agent workspaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent heartbeat or hook automation can queue or trigger agent work across workspaces without much containment.

Mitigation: Enable heartbeat and OpenClaw hooks only in trusted workspaces, review generated HEARTBEAT.md changes before using --write, and avoid setup-heartbeat --all unless every discovered workspace should be affected.

Risk: Workspace-local task files may contain source identifiers, task context, and generated report text from conversations or forum replies.

Mitigation: Keep workspace access restricted, review queued tasks before dispatch or report generation, and avoid enabling automatic reply-to-task hooks where untrusted reply content is expected.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zoujiejun/skills/agent-todo)
- [README](artifact/README.md)
- [Specification](artifact/SPEC.md)
- [OpenClaw Hooks Integration Guide](artifact/references/openclaw-hooks.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Plain text and Markdown command output with workspace-local JSON task storage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write .agent-todo/tasks.json task queues and managed HEARTBEAT.md blocks when write-oriented commands or hooks are enabled.]

## Skill Version(s):

1.2.1 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
