## Description:

Generates AI images with 50+ models via SkillBoss API Hub, supporting text-to-image, image-to-image, inpainting, LoRA, editing, upscaling, and text rendering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alvisdunlop](https://clawhub.ai/user/alvisdunlop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to guide image generation through SkillBoss API Hub for AI art, product mockups, concept art, social media graphics, marketing visuals, and illustrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image prompts and supplied image URLs are sent to SkillBoss API Hub.

Mitigation: Avoid sending sensitive prompts or private image URLs unless the user has approved sharing them with SkillBoss.

Risk: The skill requires a SkillBoss_API_KEY credential.

Mitigation: Store the API key in a secret manager or environment variable and avoid printing, logging, or committing it.

Risk: Generated images and returned image URLs may need review before external or commercial use.

Mitigation: Review outputs for policy, quality, rights, and brand requirements before publication.

## Reference(s):

- [SkillBoss API Hub](https://api.SkillBoss.co)
- [ClawHub Skill Page](https://clawhub.ai/alvisdunlop/skills/alvis2-ai-image-generation)

## Skill Output:

**Output Type(s):** [text, markdown, code, API calls, guidance]

**Output Format:** [Markdown with Python code blocks and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may lead agents to produce SkillBoss API calls that return generated image URLs.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
