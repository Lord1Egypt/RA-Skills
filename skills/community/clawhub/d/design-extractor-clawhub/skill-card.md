## Description:

Extract design tokens from existing code and generate DESIGN.md with awesome-design-md comparison.

This skill is ready for commercial/non-commercial use.

## Publisher:

[html1602](https://clawhub.ai/user/html1602)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to scan project style files, extract colors, typography, spacing, effects, and component patterns, and generate design-system documentation with awesome-design-md comparison.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running mutable external code while scanning a project can affect local files or expose workspace context.

Mitigation: Use a pinned, reviewed package version or commit in a low-privilege workspace without sensitive environment variables.

Risk: Automatic conversion into `.claude/skills` creates a persistent agent-skill entry.

Mitigation: Avoid automatic conversion unless that persistent entry is explicitly intended, and review generated files before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/html1602/skills/design-extractor-clawhub)
- [Project homepage](https://github.com/moyubox/design-extractor)
- [awesome-design-md](https://github.com/VoltAgent/awesome-design-md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown design documentation with JSON analysis data and optional shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces DESIGN.md or DESIGN-EXTRACTED.md and Docs/Design/extracted-analysis.json when run against a project.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
