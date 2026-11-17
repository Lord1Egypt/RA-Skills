## Description:

Skill lazy loading and search pack for on-demand SKILL.md loading and keyword-based skill search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[romainsantoli-web](https://clawhub.ai/user/romainsantoli-web)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to discover and load local skills on demand without pre-loading every SKILL.md file into memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on loader and search behavior that reads SKILL.md files from a local skills directory.

Mitigation: Install only when that local skill access is acceptable for the deployment environment.

Risk: The release declares a dependency on mcp-openclaw-extensions >= 3.0.0.

Mitigation: Review and trust the required dependency before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/romainsantoli-web/skills/firm-skill-loader-pack)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with YAML and inline tool command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires mcp-openclaw-extensions >= 3.0.0.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
