## Description:

Agent Starter Kit provides OpenClaw templates and customization guidance for creating agent workspaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hirofumiko](https://clawhub.ai/user/hirofumiko)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to scaffold OpenClaw agent workspaces with starter files for identity, operating principles, workspace rules, user context, and heartbeat tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Default template rules allow persistent memory and memory review, which can retain sensitive user context.

Mitigation: Edit the templates before use so memory files are treated as untrusted notes, secrets are excluded, and MEMORY.md is loaded only in appropriate private sessions.

Risk: The workspace rules direct an agent to follow and delete BOOTSTRAP.md and include broad 'do not ask permission' language.

Mitigation: Remove or gate bootstrap-following behavior and require explicit confirmation for ambiguous, destructive, or externally visible actions.

Risk: Heartbeat guidance encourages proactive checks of email, calendar, social notifications, weather, project state, and repository activity.

Mitigation: Make each heartbeat integration opt-in, limit credentials until boundaries are explicit, and require confirmation before commits, pushes, messages, or other external actions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hirofumiko/skills/fumi-agent-starter-kit)
- [README](artifact/README.md)
- [Skill Definition](artifact/SKILL.md)
- [Changelog](artifact/CHANGELOG.md)
- [Workspace Rules Template](artifact/templates/AGENTS.md)
- [Heartbeat Template](artifact/templates/HEARTBEAT.md)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown templates with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces starter templates for SOUL.md, IDENTITY.md, AGENTS.md, USER.md, and HEARTBEAT.md.]

## Skill Version(s):

1.0.0 (source: release evidence, frontmatter, changelog, and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
