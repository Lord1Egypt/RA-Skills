## Description: <br>
Generate character design images, original character art, OC portraits, character sheets, and hero concept art. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[632657122](https://clawhub.ai/user/632657122) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, artists, and other external users use this skill to turn character requirements into structured prompts and generated character images, including portraits, character sheets, mascot concepts, and fantasy or sci-fi hero concepts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may write local .image-skills configuration files and can persist IMAGE_GEN_API_KEY in a plaintext .env file when setup is used. <br>
Mitigation: Review local configuration before installation, use least-privilege API credentials, and persist the key only when the environment requires it. <br>
Risk: Local reference images passed to image-to-image flows may be uploaded off-host through the WeryAI gateway. <br>
Mitigation: Avoid sensitive local images unless off-host upload is intended and approved for the use case. <br>
Risk: The security scan marks the release suspicious because local upload and setup behaviors are under-disclosed. <br>
Mitigation: Review the skill's safety scope and generated commands before deployment, especially in managed or sensitive workspaces. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/632657122/character-image-generator) <br>
- [First-Time Setup](references/config/first-time-setup.md) <br>
- [Preferences Schema](references/config/preferences-schema.md) <br>
- [Model Registry Schema](references/config/model-registry-schema.md) <br>
- [Style Presets](references/style-presets.md) <br>
- [Gateway Alignment Notes](references/weryai-platform.md) <br>
- [WeryAI API introduction](https://docs.weryai.com/en) <br>
- [WeryAI text-to-image endpoint](https://docs.weryai.com/api-reference/character-image-generator/submit-text-to-image-task) <br>
- [WeryAI image-to-image endpoint](https://docs.weryai.com/api-reference/character-image-generator/submit-image-to-image-task) <br>


## Skill Output: <br>
**Output Type(s):** [images, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with generated image files or image URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses IMAGE_GEN_API_KEY, may write output images and optional configuration under .image-skills/character-image-generator/ or the matching home directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; skill frontmatter reports 0.5.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
