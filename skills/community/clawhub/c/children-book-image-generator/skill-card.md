## Description: <br>
Generate children's book illustrations, storybook images, picture-book scenes, and bedtime story art for kid-friendly storytelling workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[632657122](https://clawhub.ai/user/632657122) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creative agents use this skill to clarify a children's story moment, build an age-appropriate image prompt, choose a WeryAI image model, and generate storybook or picture-book artwork. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and reference images are sent to WeryAI during generation. <br>
Mitigation: Install and use the skill only when that data transfer is acceptable; avoid passing sensitive prompts or reference images. <br>
Risk: API key persistence and setup actions can write local configuration files. <br>
Mitigation: Prefer providing IMAGE_GEN_API_KEY through the runtime environment, and review setup actions before allowing persisted secrets or dependency installs. <br>
Risk: Web search and webhook callbacks can send data to additional destinations when enabled. <br>
Mitigation: Leave web search and webhook options disabled unless the destination and data flow are understood. <br>
Risk: Local reference-image paths may be uploaded by artifact behavior when used for image-to-image requests. <br>
Mitigation: Provide only reference images intended for upload and review paths before generation. <br>


## Reference(s): <br>
- [Skill listing](https://clawhub.ai/632657122/children-book-image-generator) <br>
- [Publisher profile](https://clawhub.ai/user/632657122) <br>
- [WeryAI API introduction](https://docs.weryai.com/en) <br>
- [WeryAI text-to-image API](https://docs.weryai.com/api-reference/children-book-image-generator/submit-text-to-image-task) <br>
- [WeryAI image-to-image API](https://docs.weryai.com/api-reference/children-book-image-generator/submit-image-to-image-task) <br>
- [First-time setup](references/config/first-time-setup.md) <br>
- [Model registry schema](references/config/model-registry-schema.md) <br>
- [Preferences schema](references/config/preferences-schema.md) <br>
- [Style presets](references/style-presets.md) <br>
- [WeryAI platform notes](references/weryai-platform.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands and generated image file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses IMAGE_GEN_API_KEY, Node/npm with bun or npx, WeryAI HTTPS calls, and local project or user configuration under .image-skills/children-book-image-generator/.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence; artifact frontmatter reports 0.5.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
