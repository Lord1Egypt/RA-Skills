## Description:

Curated image generation assistant covering characters, scenes, products, and style transformation for high-quality stylized 3D image generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ericn26-star](https://clawhub.ai/user/ericn26-star)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to route image-generation requests into curated styles for characters, scenes, products, and visual transformations. It helps produce stylized 3D image assets from user descriptions or reference images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may use web search to enrich prompts for public facts about places, brands, and movie scenes.

Mitigation: Review prompts and generated outputs for factual fit before external use.

Risk: Broad trigger keywords may cause the skill to activate more often than intended.

Mitigation: Use routing tests or narrower activation rules in workflows where image generation is optional.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ericn26-star/skills/christy-image-craft)
- [ClawHub publisher profile](https://clawhub.ai/user/ericn26-star)

## Skill Output:

**Output Type(s):** [Files, Guidance]

**Output Format:** [XML-style deliver_assets block with generated image file paths, plus concise selection UI text when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default image resolution is 1080x1080 unless a style specifies another aspect ratio.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
