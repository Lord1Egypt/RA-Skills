## Description:

Transform your agent from chatbot to copilot with context persistence, proactive anticipation, and opinionated help across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to make assistant interactions feel continuous across sessions by maintaining local project, priority, decision, and preference context. It guides agents to read and update local state, provide opinionated help, and use screenshots or proactive checks only when useful.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages broad cross-session memory about projects, people, decisions, work habits, screenshots, messaging, calendar, and operational context.

Mitigation: Configure a private storage path, avoid storing secrets or regulated data, and periodically review or delete the local copilot state directory.

Risk: Proactive checks or screenshots can expose sensitive user or workplace information if used without clear consent.

Mitigation: Require explicit user approval before screenshots or email, Slack, calendar, and DevOps access, and fall back to user-provided descriptions when access is denied.

## Reference(s):

- [Copilot Skill on ClawHub](https://clawhub.ai/ivangdavila/skills/copilot)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with state-file templates, interaction patterns, and suggested commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local files under a user-configured copilot state directory and may suggest optional screenshot, calendar, messaging, or DevOps checks when explicitly authorized.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
