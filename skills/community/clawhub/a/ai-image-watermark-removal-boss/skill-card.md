## Description:

Guides agents through locating and covering corner watermarks on AI-generated images, then checking the edited region for remaining bright pixels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lingyu9495-source](https://clawhub.ai/user/lingyu9495-source)

### License/Terms of Use:

MIT-0

## Use Case:

Users and image-editing agents can follow this workflow to edit authorized AI-generated images with corner watermarks and check the resulting region for bright-pixel remnants.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Removing a watermark can erase attribution, provenance, authenticity, copyright, or platform markings without authorization.

Mitigation: Edit only images you own or are authorized to modify; do not remove protected or provenance-related markings.

Risk: A bright-pixel count alone may mistake image content for watermark residue or miss edits outside the selected region.

Mitigation: Check the target region and edited image visually as well as reviewing the verification result; do not treat the script as a complete editing pipeline.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/lingyu9495-source/skills/ai-image-watermark-removal-boss)
- [ClawHub publisher profile](https://clawhub.ai/user/lingyu9495-source)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Markdown guidance and text verification results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled script checks bright-pixel counts in original and edited images; it does not perform the edit.]

## Skill Version(s):

1.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
