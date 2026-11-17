## Description:

Provides an OpenClaw workspace template for command-line tool development, emphasizing CLI user experience, documentation-first work, and test-driven development.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hirofumiko](https://clawhub.ai/user/hirofumiko)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create an OpenClaw workspace scaffold for building CLI tools with clear command design, error handling, testing, documentation, and packaging practices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The included workspace instructions encourage persistent memory writes and autonomous edits to agent configuration files.

Mitigation: Review and constrain memory and configuration-write behavior before installing or reusing the templates.

Risk: Heartbeat activity can prompt background checks and workspace changes without an explicit request.

Mitigation: Make heartbeat behavior read-only unless specific file changes are deliberately approved.

Risk: The templates include Japanese-language documentation and placeholders that may be missed by some reviewers.

Mitigation: Localize or complete placeholders during setup and verify the resulting workspace instructions before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hirofumiko/skills/fumi-cli-tool-template)
- [README](artifact/README.md)
- [Changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [Markdown, Configuration, Guidance, Shell commands]

**Output Format:** [Markdown templates and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces reusable workspace template files for CLI development agents.]

## Skill Version(s):

1.0.0 (source: frontmatter, release evidence, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
