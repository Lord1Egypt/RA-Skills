## Description:

Use when the user wants to update Claude settings, hooks, permissions, MCP server toggles, or other JSON config safely and with scope awareness.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wimi321](https://clawhub.ai/user/wimi321)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to make scoped Claude settings, permission, hook, and MCP configuration changes while preserving valid JSON and unrelated settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Permission widening or hook automation can persist and affect future agent runs.

Mitigation: Review proposed permission and hook changes before applying them, especially broad automation or access changes.

Risk: Incorrect settings edits can break Claude configuration or change behavior at the wrong scope.

Mitigation: Read the current settings file first, apply the smallest valid JSON change, and verify the intended user, project, or local scope.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wimi321/skills/claude-code-claude-settings-editor)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Code]

**Output Format:** [Markdown with JSON snippets and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include explanations of settings scope, precedence, and risky configuration changes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
