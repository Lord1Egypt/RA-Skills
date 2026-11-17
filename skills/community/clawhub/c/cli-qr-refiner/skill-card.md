## Description:

Professional utility to refine terminal-based ASCII QR code blocks into high-definition PNG images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jdchi](https://clawhub.ai/user/jdchi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to convert block-character QR codes captured from terminal output into scannable PNG image files, especially in headless or font-sensitive CLI environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: QR source text and generated PNG files can contain login, verification, or other sensitive data.

Mitigation: Use private temporary paths with restrictive permissions, share outputs only with intended recipients, and delete source and output files after use.

Risk: Unusually large QR inputs or scale values can create large images and consume excessive local resources.

Mitigation: Review input size and scale before rendering, and keep scale values within the practical range needed for scanning.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jdchi/skills/cli-qr-refiner)
- [Publisher profile](https://clawhub.ai/user/jdchi)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated PNG file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local PNG image files from text files containing terminal QR-code blocks.]

## Skill Version(s):

2.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
