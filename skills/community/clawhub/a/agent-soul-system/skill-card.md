## Description:

Create, manage, and validate SOUL.md personality files for multi-agent systems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adamwgp](https://clawhub.ai/user/adamwgp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to create SOUL.md templates, audit existing agent personality files, and define collaboration protocols for multi-agent teams.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated SOUL.md files can persist agent personality and collaboration settings that may not match the user's intended hierarchy.

Mitigation: Review each generated SOUL.md before agents use it and replace the hardcoded reporting hierarchy with the user's own structure.

Risk: Unsafe path handling in soul-create.py can create files in unintended locations if an untrusted or path-like agent name is supplied.

Mitigation: Use trusted simple agent names until path validation is added.

## Reference(s):

- [Agent Soul System on ClawHub](https://clawhub.ai/adamwgp/skills/agent-soul-system)
- [SOUL.md Template](references/soul-template.md)
- [Personality Library](references/personality-library.md)
- [Multi-Agent Collaboration Protocol](references/collaboration-protocol.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated SOUL.md files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or inspects files under ~/.openclaw/agents when the bundled scripts are run.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
