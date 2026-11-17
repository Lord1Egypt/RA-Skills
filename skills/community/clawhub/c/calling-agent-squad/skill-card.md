## Description:

Activate a multi-agent team (the Squad) to manage complex projects, business tasks, or development workflows. The squad includes a Manager, Architect, Coder, Reviewer, and Observer. Use when the user wants to "call a squad", "start a project", or "deploy squad" with specialized roles and quality control loops.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arbiger](https://clawhub.ai/user/arbiger)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and project leads use this skill to coordinate specialized agent roles for complex projects, business tasks, or development workflows. It supports standard roleplay-style execution and a full mode that spawns separate OpenClaw sub-agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill grants broad persistent memory and personal-context access to bundled agent policies.

Mitigation: Require approval before agents read, create, or update memory and policy files, and disable persistent-memory sections when they are not required.

Risk: Full mode can spawn multiple agent sessions with separate workspaces.

Mitigation: Review spawned-agent permissions before use and require explicit user approval for session spawning in sensitive projects.

Risk: Bundled policies include heartbeat-driven operations and autonomous repository actions beyond the main skill description.

Mitigation: Remove or disable heartbeat and personal-assistant sections, and require explicit review before any git push or outbound communication.

## Reference(s):

- [Calling Agent Squad on ClawHub](https://clawhub.ai/arbiger/skills/calling-agent-squad)
- [Publisher profile: arbiger](https://clawhub.ai/user/arbiger)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and saved project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create structured project folders and agent workspaces when full mode is used.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
