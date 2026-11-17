## Description:

Provides color code conversion, contrast calculation, palette recommendation, and optional HTML preview generation for UI design and accessibility workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ldxs001](https://clawhub.ai/user/ldxs001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and accessibility reviewers use this skill to convert colors, compare contrast with WCAG/APCA and color-difference metrics, generate palettes from descriptions, and create preview artifacts for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HTML preview generation may write files to unsafe or unintended paths.

Mitigation: Write previews only into a disposable directory, avoid elevated privileges, and prefer a fixed version that confines output to a safe directory with overwrite protection.

Risk: Generated HTML previews may include unescaped text from color descriptions or preview titles.

Mitigation: Use trusted color descriptions and preview titles, review generated HTML before sharing, and prefer a fixed version that escapes HTML text.

## Reference(s):

- [Color Toolkit Turn ClawHub Page](https://clawhub.ai/ldxs001/skills/color-toolkit-turn)
- [Output Examples](references/examples.md)
- [FAQ](references/faq.md)
- [Permissions](references/permissions.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or JSON summaries, with optional generated HTML files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preview generation may write HTML files to a caller-selected output path.]

## Skill Version(s):

3.4.1 (source: ClawHub release metadata; artifact frontmatter and _meta.json report 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
