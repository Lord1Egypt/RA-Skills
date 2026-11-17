## Description:

Use when the user wants to update Claude settings, hooks, permissions, MCP server toggles, or other JSON config safely and with scope awareness.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wimi321](https://clawhub.ai/user/wimi321)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to make scoped Claude settings changes, including permissions, hooks, local overrides, and MCP server toggles, while preserving unrelated configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent Claude settings changes can broaden permissions or automation hooks beyond the intended scope.

Mitigation: Review proposed edits before applying them, choose the narrowest appropriate scope, validate JSON, and preserve unrelated settings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wimi321/skills/claude-settings-editor)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown with JSON configuration snippets and concise change notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include risk notes for permission, hook, and automation changes.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
