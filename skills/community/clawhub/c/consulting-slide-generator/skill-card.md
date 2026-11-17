## Description:

Generates consulting-style business slide diagrams as HTML and Tailwind templates, then converts them to fixed-size PNG images with headless Chrome.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mtdnot](https://clawhub.ai/user/mtdnot)

### License/Terms of Use:

MIT-0

## Use Case:

Business users, consultants, and agents use this skill to draft Japanese consulting-style proposal and presentation slides, including problem, solution-flow, matrix, comparison, and process-style visuals. It is intended to produce reusable HTML slide files and PNG exports for business communication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Rendered slides load live third-party JavaScript and fonts, which can be risky for confidential or client-sensitive slide content.

Mitigation: Bundle Tailwind CSS and fonts locally, disable outbound network access during Chrome rendering, or avoid sensitive content until live CDN dependencies are removed.

Risk: The skill references a process slide template that is not included in the artifact.

Mitigation: Review available templates before use and add or substitute a process template before relying on that slide type.

## Reference(s):

- [Design Principles for Consulting Slides](references/design-principles.md)
- [ClawHub Skill Page](https://clawhub.ai/mtdnot/skills/consulting-slide-generator)

## Skill Output:

**Output Type(s):** [text, code, shell commands, files, guidance]

**Output Format:** [Markdown guidance with HTML/Tailwind code, shell commands, and generated HTML/PNG slide files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Targets 1200 x 675 px PNG output through Chrome headless.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
