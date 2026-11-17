## Description:

Beautify FACS gating plots for publication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill as a local command-line helper for FACS gating plot styling workflows, selecting contour, density, or dot styles for an input FCS path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The current artifact may not generate a publication plot despite the skill description.

Mitigation: Validate expected plot output before relying on the skill, and treat current behavior as draft placeholder output until plotting is implemented.

Risk: Future versions that write files could save outputs in unexpected locations or overwrite existing files.

Mitigation: Review output paths and overwrite behavior before deployment, especially when processing workspace files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/facs-gating-viz-style)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and plain-text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local FCS path and a style choice of contour, density, or dot. Current script prints status messages rather than writing a plot file.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
