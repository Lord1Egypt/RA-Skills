## Description:

Persistent project planning for AI agents. Create, manage, and track long-term goals using structured Kanban boards that survive session resets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[akievo](https://clawhub.ai/user/akievo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to give an OpenClaw agent persistent, human-editable Kanban planning for long-running goals, including task creation, progress tracking, dependencies, and status reporting across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and update Akievo boards through the configured API key, including boards used for business-critical planning.

Mitigation: Use an API key with the minimum required board scopes, avoid unrelated workspace access where possible, and review board activity after agent-managed changes.

## Reference(s):

- [Akievo skill page](https://clawhub.ai/akievo/skills/akievo)
- [Akievo publisher profile](https://clawhub.ai/user/akievo)
- [Akievo setup guide](https://akievo.com/openclaw-setup)
- [Akievo API documentation](https://akievo.com/api-docs)
- [Akievo MCP server](https://mcp.akievo.com)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with MCP tool calls and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AKIEVO_API_KEY and Akievo board access; performs remote board reads and writes when used.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, artifact/skill.yaml, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
