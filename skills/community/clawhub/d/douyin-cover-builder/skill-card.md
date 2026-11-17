## Description:

Helps Chinese-language creators draft image-generation prompts and art direction briefs for Douyin cover images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0x00000003](https://clawhub.ai/user/0x00000003)

### License/Terms of Use:

MIT-0

## Use Case:

Chinese-language content creators use this skill to plan consistent Douyin covers and prepare prompts for an image-generation model, using a topic, optional key points, a subject's pose, and a preferred aspect ratio.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A portrait supplied for consistent likeness may be uploaded to an image-generation service.

Mitigation: Only provide photos you are comfortable sharing with the chosen service.

Risk: An image model may return a cover with the wrong aspect ratio or dimensions.

Mitigation: Check the final image's pixel dimensions against the requested ratio and exact size; correct any mismatch before delivery.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/0x00000003/skills/douyin-cover-builder)
- [Examples and comparison images linked in skill documentation](https://github.com/0x00000003/douyin-cover-builder)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Markdown prompt and art direction brief]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Specifies target aspect ratio and dimensions; if an image is generated, its actual dimensions must be checked before delivery.]

## Skill Version(s):

3.1.3 (source: ClawHub release metadata and SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
