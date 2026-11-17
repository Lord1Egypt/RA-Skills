## Description:

Converts Markdown content into GitHub-styled PNG or JPEG images with Chinese font support, emoji rendering, syntax highlighting, and line- or height-based pagination.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fried-avocado](https://clawhub.ai/user/fried-avocado)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to convert Markdown replies, technical notes, tables, and code-heavy content into shareable image files for messaging or chat surfaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted Markdown is rendered in an unsandboxed browser, and the inspected security evidence says documented path and size protections are not actually enforced.

Mitigation: Use trusted Markdown or run conversion in a contained environment without elevated privileges, and write to a dedicated output directory.

Risk: Debug mode can save intermediate HTML and pagination content that may contain private Markdown.

Mitigation: Keep debug mode off for private content and clean generated images and intermediate files after use.

## Reference(s):

- [auto-md2img ClawHub listing](https://clawhub.ai/fried-avocado/skills/auto-md2img)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Markdown, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; conversion output is PNG or JPEG image files and optional HTML image tags.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports line-based or height-based pagination, JPEG quality settings, and optional debug artifacts.]

## Skill Version(s):

1.3.1 (source: server release evidence, SKILL.md frontmatter, _meta.json, and CHANGELOG; package.json reports 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
