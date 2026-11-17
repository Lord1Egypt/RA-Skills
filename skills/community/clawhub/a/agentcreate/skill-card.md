## Description:

Creates or uninstalls isolated OpenClaw agents with independent workspaces, optional channel bindings such as Feishu or WeChat, and model selection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xf9070](https://clawhub.ai/user/xf9070)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to create separate agent workspaces, bind optional channel accounts, select models, and remove agents when they are no longer needed. It is intended for administrative agent lifecycle tasks where the operator can verify targets and configuration changes before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Full uninstall can delete OpenClaw agents, workspaces, bindings, and channel accounts.

Mitigation: Verify the exact agent and channel account, refuse operations on the main agent, require explicit confirmation, and back up OpenClaw configuration before removal.

Risk: The documented account-removal path directly rewrites a live OpenClaw configuration file.

Mitigation: Prefer a supported deletion method when available; otherwise review the edit, back up the config first, and validate agents and bindings after the change.

Risk: Channel credentials such as Feishu app IDs and secrets may be exposed if pasted into shared chats or logs.

Mitigation: Avoid sharing secrets in chat transcripts or logs, redact credentials from summaries, and use existing configured accounts where possible.

## Reference(s):

- [Agent creation workflow](references/create.md)
- [Agent uninstall workflow](references/delete.md)
- [ClawHub skill page](https://clawhub.ai/xf9070/skills/agentcreate)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask for operator confirmation before administrative create, bind, unbind, or uninstall actions.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
