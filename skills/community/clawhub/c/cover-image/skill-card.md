## Description: <br>
Generate article cover images with structured dimensions and bundled generation tooling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[632657122](https://clawhub.ai/user/632657122) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, writers, and content teams use this skill to turn article or blog topics into cover-image briefs, prompts, batch files, and generated banner-style images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner reports under-disclosed upload and network behavior for reference images and generation metadata. <br>
Mitigation: Use only public or intended-to-upload reference images, and avoid optional web search or webhook features unless they are specifically needed. <br>
Risk: The skill requires an image-generation API key and may persist it when setup is explicitly run with persistence enabled. <br>
Mitigation: Prefer providing IMAGE_GEN_API_KEY through the environment or a protected secret store instead of saving it to a project .env file. <br>


## Reference(s): <br>
- [Cover Image Dimensions](references/dimensions.md) <br>
- [Prompt Template](references/prompt-template.md) <br>
- [WeryAI Platform Notes](scripts/vendor/shared-image-generation/references/weryai-platform.md) <br>
- [WeryAI Text-to-Image API](https://docs.weryai.com/api-reference/image-generation/submit-text-to-image-task) <br>
- [WeryAI Image-to-Image API](https://docs.weryai.com/api-reference/image-generation/submit-image-to-image-task) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown prompts, JSON batch configuration, shell commands, and generated image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires IMAGE_GEN_API_KEY and local Node/npm with bun or npx; writes generated images and optional configuration under .image-skills/cover-image.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
