## Description:

End-to-end plugin creation and publishing for Claude Code, Cowork, and OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autosolutionsai-didac](https://clawhub.ai/user/autosolutionsai-didac)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design, scaffold, package, and publish distributable Claude plugins, including marketplace structure, OpenClaw compatibility scripts, GitHub publication steps, and Cowork .plugin packaging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create repositories, commit, push, generate executable installers, and package plugin archives.

Mitigation: Require explicit human review and approval before any repo creation, commit, push, installer execution, or plugin package distribution.

Risk: Generated shell scripts may include plugin names or display text supplied during plugin creation.

Mitigation: Sanitize plugin names and display text before inserting them into generated shell scripts, and review scripts before execution.

Risk: The security verdict is suspicious due to high-impact publishing actions and weak confirmation boundaries.

Mitigation: Use the skill only in a controlled workspace with least-privilege credentials and review generated files before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/autosolutionsai-didac/skills/autosolutions-plugin-publisher)
- [Anthropic Marketplace Structure](references/marketplace-structure.md)
- [OpenClaw Deployment Template and Adaptation Rules](references/openclaw-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JSON, shell, and configuration snippets; may also produce plugin files and install scripts during agent execution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create or modify local files and package plugin archives when the host agent grants file-system access.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
