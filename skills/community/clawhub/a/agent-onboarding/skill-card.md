## Description:

A quick-start guide for onboarding new agents into Meeting or project group chats by helping them update AGENTS.md, create group notes, follow speaking norms, and build memory routines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[biociao](https://clawhub.ai/user/biociao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to onboard agents into group-chat projects with consistent participation rules, project notes, and checkpoint practices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead an agent to update AGENTS.md and persistent memory files in a workspace.

Mitigation: Invoke it intentionally and review proposed file changes before keeping them.

Risk: Group-chat notes can accidentally mix private long-term memory into shared conversation context.

Mitigation: Keep MEMORY.md out of group-chat notes and review notes for sensitive content before sharing or committing them.

## Reference(s):

- [Group Chat Guide](references/group-chat-guide.md)
- [Project Notes Template](references/project-notes-template.md)
- [ClawHub skill page](https://clawhub.ai/biociao/skills/agent-onboarding)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration]

**Output Format:** [Markdown guidance with reusable note and checkpoint templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose updates to local AGENTS.md and memory files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
