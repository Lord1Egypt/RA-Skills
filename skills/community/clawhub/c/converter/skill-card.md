## Description:

A local-first conversion router and format strategist that identifies safe local paths for document, image, audio, video, archive, and data transformations while prioritizing fidelity and privacy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agisearch](https://clawhub.ai/user/agisearch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other external users use this skill to plan and run local file conversions across documents, images, audio, video, archives, office files, and data formats. It helps choose an available local toolchain, explain fidelity tradeoffs, and provide commands or fallback guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local conversion commands may process or overwrite files selected by the user, especially during batch workflows.

Mitigation: Confirm matched files and run batch commands in the intended folder or on copies when source files matter.

Risk: Conversion quality can be lossy, partially reconstructed, unsupported, or dependent on missing local binaries.

Mitigation: Review the route analysis, fidelity notes, and execution status before running commands; use fallback guidance when required tools are unavailable.

Risk: Some conversion requests may require external services or involve protected files.

Mitigation: Keep conversions local by default, require explicit consent before any external route, and do not bypass DRM, crack passwords, or decrypt protected files without authorization.

## Reference(s):

- [Converter ClawHub skill page](https://clawhub.ai/agisearch/skills/converter)
- [AGIsearch publisher profile](https://clawhub.ai/user/agisearch)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown route analysis with inline shell commands and fallback guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on host-available local binaries such as ffmpeg, pandoc, magick, soffice, and 7z.]

## Skill Version(s):

2.0.0 (source: skill frontmatter, skill.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
