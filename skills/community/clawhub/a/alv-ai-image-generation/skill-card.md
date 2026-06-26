## Description: <br>
Generates AI images through SkillBoss API Hub across text-to-image, image-to-image, inpainting, editing, upscaling, LoRA, and text-rendering workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alvisdunlop](https://clawhub.ai/user/alvisdunlop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent for image-generation API examples and parameter guidance for artwork, product mockups, marketing visuals, illustrations, and upscaling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, image URLs, and related generation inputs are sent to SkillBoss for third-party processing. <br>
Mitigation: Avoid confidential prompts, private images, internal URLs, and sensitive visual material unless that processing is acceptable. <br>
Risk: The skill requires a sensitive SkillBoss API key. <br>
Mitigation: Use a scoped, revocable key stored in an environment variable or secret manager, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [SkillBoss API Hub](https://api.heybossai.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/alvisdunlop/alv-ai-image-generation) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, API calls, configuration] <br>
**Output Format:** [Markdown with Python code examples and JSON request bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY; API calls return image URLs or image result arrays from SkillBoss.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
