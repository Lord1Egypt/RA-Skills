## Description:

Modify an existing image by instruction or mask, including object removal, replacement, recoloring, relighting, inpainting, and outpainting while preserving unchanged regions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runware](https://clawhub.ai/user/runware)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to route a provided image and edit instruction to an appropriate Runware image-editing model, including mask-driven removal, prompt-guided inpainting, or canvas extension.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided images or masks may be sent to Runware image models for editing.

Mitigation: Avoid using sensitive images unless sending them to Runware is acceptable for the user's data handling requirements.

Risk: Restoration wording is ambiguous for pure upscale, denoise, deblur, or old-photo repair tasks.

Mitigation: Use a restoration-focused skill for quality-only repair or enlargement tasks until the publisher clarifies the intended restore behavior.

Risk: Masked edits can fail or affect unintended regions when the mask dimensions or coverage are wrong.

Mitigation: Require masks to match the source image resolution exactly, then review the result and retry with a tighter mask or adjusted dilation when needed.

## Reference(s):

- [Edit image - worked recipes](artifact/references/examples.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, JSON]

**Output Format:** [Markdown guidance with JSON API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include model-routing recommendations, imageInference request payloads, mask requirements, and quality checks.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
