## Description: <br>
Generate 3D rendered art and icons. Use when the user asks for 3D graphics, claymorphism, octane render, or blender 3d style. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[632657122](https://clawhub.ai/user/632657122) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creative users use this skill to generate 3D-rendered images, icons, and image variations through a WeryAI-backed image generation workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send prompts and selected reference images to WeryAI. <br>
Mitigation: Use only prompts and reference images that are acceptable to share with WeryAI; avoid sensitive local images unless upload is intended. <br>
Risk: The skill can persist IMAGE_GEN_API_KEY in a plaintext local environment file during setup. <br>
Mitigation: Prefer environment variables or a managed secret store, and persist a local environment file only when that storage is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/632657122/3d-image-generator) <br>
- [WeryAI platform contract](artifact/references/weryai-platform.md) <br>
- [Style presets](artifact/references/style-presets.md) <br>
- [First-time setup](artifact/references/config/first-time-setup.md) <br>
- [Model registry schema](artifact/references/config/model-registry-schema.md) <br>
- [Preferences schema](artifact/references/config/preferences-schema.md) <br>
- [WeryAI API keys](https://weryai.com/api/keys) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples, configuration notes, and generated image files from the runtime workflow] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated image files may be written locally, and dry runs can return JSON request previews.] <br>

## Skill Version(s): <br>
2026.3.23 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
