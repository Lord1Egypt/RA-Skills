## Description:

Reviews an agent workspace boot files against registry-backed context notes and produces concise audits, refactor recommendations, and optional staged rewrite drafts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gregtysick](https://clawhub.ai/user/gregtysick)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent maintainers use this skill to audit bootstrap files for structure, redundancy, reference integrity, context alignment, and length discipline before making agent context changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed to read agent boot files and registry-listed personal or workspace context.

Mitigation: Use it only when that review is intended, and keep registry entries limited to context that should be part of the audit.

Risk: Registry edits, staged drafts, or live boot-file rewrites could change an agent setup if approved without review.

Mitigation: Review proposed registry changes and draft replacements before approval; allow live rewrites only when they match the intended agent setup.

## Reference(s):

- [Boot File Review Skill](references/why-this-skill.md)
- [Bootstrap Review on ClawHub](https://clawhub.ai/gregtysick/skills/bootstrap-review)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance, files]

**Output Format:** [Markdown audit text with optional staged markdown file drafts and registry JSON guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default workflow is audit and recommendations; staged drafts or in-place rewrites require explicit user request.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
