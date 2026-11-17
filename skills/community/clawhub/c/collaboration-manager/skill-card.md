## Description:

A multi-agent collaboration manager for Feishu group chats that routes responses by mentions, keywords, task assignment, and pause/resume controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tazio7](https://clawhub.ai/user/tazio7)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workspace admins use this skill to coordinate multiple agents in Feishu group chats, routing work to named agents or keyword-matched roles while reducing duplicate replies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill text claims its group-chat routing rules take priority over AGENTS.md, which can confuse instruction hierarchy in shared workspaces.

Mitigation: Make the routing guidance explicitly subordinate to system, developer, workspace, authorization, and safety rules before shared use.

Risk: Broad keyword-based auto-routing can trigger agents that were not explicitly requested.

Mitigation: Narrow keyword triggers, cap automatic responders, or require explicit mentions for sensitive or high-noise channels.

Risk: Workspace task-state storage is described without access, retention, or deletion details.

Mitigation: Document what state is stored, who can access it, where it is kept, and how it can be deleted.

Risk: The included configuration assigns the same Feishu openId to multiple agents, which can prevent accurate mention targeting.

Mitigation: Configure distinct agent openIds or a reliable sender/application identifier mapping before operational deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tazio7/skills/collaboration-manager)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON examples, Feishu card payloads, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes mention-priority routing, keyword matching, task coordination, and pause/resume controls.]

## Skill Version(s):

1.0.0 (source: server release metadata and release changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
