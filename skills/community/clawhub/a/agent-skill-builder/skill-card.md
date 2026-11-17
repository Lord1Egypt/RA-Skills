## Description:

Build, review, or migrate an agent skill from a plain-language description; decide invocation control, arguments, and context cost, then scaffold, validate, and test it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[conorbronsdon](https://clawhub.ai/user/conorbronsdon)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to create, review, or migrate agent skills with current frontmatter, clear invocation behavior, scoped tool grants, and validation before installation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated or modified skills can introduce broad tool grants, shell commands, or dynamic context injection that change execution risk.

Mitigation: Review proposed SKILL.md frontmatter, tool grants, and shell or dynamic-injection lines before saving or installing generated skills.

Risk: Global installation can make the skill available outside the project where it was reviewed.

Mitigation: Install per project unless intentional global availability is needed.

Risk: Skill-building guidance can be incomplete or stale if the pinned frontmatter snapshot has aged.

Mitigation: Use the bundled validator and review any staleness warning before deployment.

## Reference(s):

- [Skill Frontmatter & Behavior Reference](references/claude-code-frontmatter.md)
- [Agent Skills Standard](https://agentskills.io)
- [Claude Code Skills Documentation](https://code.claude.com/docs/en/skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline code blocks and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate or modify skill files when explicitly asked, and reports validator results for review.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
