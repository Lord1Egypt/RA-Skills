## Description:

Guides agents through MediaKit CLI image workflows for OCR, image erasure, background removal, enhancement, and quality evaluation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volcvnebot](https://clawhub.ai/user/volcvnebot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call MediaKit CLI image-domain tools for OCR, object or text erasure, background removal, image enhancement, and image quality scoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on MediaKit CLI cloud processing, which can upload local or remote images to MediaKit services.

Mitigation: Avoid sensitive or regulated images unless cloud processing and any local upload to MediaKit are acceptable for the deployment environment.

Risk: The skill requires a locally installed mediakit-cli binary and authenticated API configuration.

Mitigation: Confirm the MediaKit CLI package source is trusted, pin the npm package version where practical, and verify MEDIAKIT_API_KEY handling before use.

## Reference(s):

- [Image OCR Reference](reference/image-ocr.md)
- [Erase Image Reference](reference/erase-image.md)
- [Remove Image Background Reference](reference/remove-image-background.md)
- [Enhance Image Reference](reference/enhance-image.md)
- [Evaluate Image Quality Reference](reference/evaluate-image-quality.md)
- [MediaKit Shared Rules](reference/shared.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, JSON]

**Output Format:** [Markdown guidance with MediaKit CLI commands and JSON result handling]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires mediakit-cli and MEDIAKIT_API_KEY for cloud image processing.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
