## Description:

Agent Recruitment guides OpenClaw operators through requirements intake, isolated workspace creation, model configuration, Feishu route binding, and delivery checklist generation for new or updated agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[usewild2026](https://clawhub.ai/user/usewild2026)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to create or update OpenClaw agents with isolated workspaces, model bindings, optional Feishu routing, and a clear handoff checklist.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Feishu group routing may cause a bot to process and answer every group message without explicit mention-based activation or clear consent.

Mitigation: Review routes before installation, prefer @mention-only activation by default, notify group members that messages may be processed, and define who can authorize, disable, and retain data from routes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/usewild2026/skills/agent-recruitment)
- [Publisher profile](https://clawhub.ai/user/usewild2026)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown checklist with paths, model bindings, route details, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include absolute workspace paths, Feishu route identifiers, agent identities, and role-boundary notes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
