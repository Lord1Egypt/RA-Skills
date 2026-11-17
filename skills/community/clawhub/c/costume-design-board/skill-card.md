## Description:

Generates standardized stage costume design board collages and PDFs from full-body costume images, detail references, character information, and design notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trumcy9987](https://clawhub.ai/user/trumcy9987)

### License/Terms of Use:

MIT-0

## Use Case:

External designers, production teams, and agents preparing stage-costume materials use this skill to assemble named costume views and detail shots into a consistent review board for print or PDF handoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency behavior may vary if Pillow is installed without a pinned version.

Mitigation: Install in an isolated Python environment and pin Pillow for reproducible runs.

Risk: User-provided character and version values influence output filenames.

Mitigation: Use simple character and version values without slashes, `..`, drive prefixes, or absolute paths, and review output paths before running.

## Reference(s):

- [舞台服装设计板参数规范（V9.1 验证版）](references/v9.1-layout-spec.md)
- [ClawHub skill page](https://clawhub.ai/trumcy9987/skills/costume-design-board)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Files]

**Output Format:** [Markdown guidance with bash command examples; generated PNG and PDF files when the script is run.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 and Pillow; expects a source directory with nine named costume images.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
