## Description:

Creates 20 px SVG badges with labels, scores, and color-coded icon blocks for projects and skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT

## Use Case:

Developers and project maintainers use this skill to create small SVG badges showing a label and score for a project or agent skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running the badge generator can create or overwrite a local SVG despite documentation claiming no filesystem access.

Mitigation: Review the output path before running and point --out to an intended project location.

Risk: Untrusted badge text, icons, colors, or scores may produce unsafe SVG when embedded or published.

Mitigation: Use trusted inputs or sanitize the SVG before embedding or publishing it.

## Reference(s):

- [Badge Studio on ClawHub](https://clawhub.ai/zhaoxinghua09-cell/skills/badge-studio)

## Skill Output:

**Output Type(s):** [Files, Shell commands]

**Output Format:** [SVG badge file and a brief text confirmation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes to badge.svg by default or a selected --out path; existing files may be overwritten. Does not produce the JSON verdict described in its agent-facing documentation.]

## Skill Version(s):

1.0.0 (source: ClawHub release; artifact frontmatter says 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
