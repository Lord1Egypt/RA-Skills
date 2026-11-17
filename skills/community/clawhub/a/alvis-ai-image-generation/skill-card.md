## Description:

Generates AI images and image edits through SkillBoss API Hub using models such as FLUX, Gemini, Grok, Seedream, Reve, ImagineArt, and Topaz.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alvisdunlop](https://clawhub.ai/user/alvisdunlop)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent users use this skill to generate images, edit images, upscale images, and produce marketing visuals, mockups, concept art, illustrations, and social media graphics through the SkillBoss API Hub.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and input image URLs are sent to SkillBoss as a third-party image service.

Mitigation: Avoid submitting confidential prompts, private image URLs, regulated data, or secrets unless the user trusts SkillBoss's handling of that data.

Risk: The skill requires a SkillBoss API key for requests.

Mitigation: Store the API key in the SkillBoss_API_KEY environment variable and avoid exposing it in prompts, logs, or generated examples.

## Reference(s):

- [SkillBoss API Hub](https://api.SkillBoss.co)
- [ClawHub Skill Page](https://clawhub.ai/alvisdunlop/skills/alvis-ai-image-generation)
- [Publisher Profile](https://clawhub.ai/user/alvisdunlop)

## Skill Output:

**Output Type(s):** [Guidance, Code, API Calls, Configuration instructions]

**Output Format:** [Markdown guidance with Python code snippets and API response fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SkillBoss_API_KEY and returns image URLs from the third-party SkillBoss service.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
