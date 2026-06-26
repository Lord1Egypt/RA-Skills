## Description: <br>
Generate high-quality anime style illustrations. Use when the user asks for anime, light novel covers, or japanese animation style art. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[632657122](https://clawhub.ai/user/632657122) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creative users use this skill to generate anime-style illustrations, light novel cover art, and Japanese animation style image assets through a WeryAI-backed image generation workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and referenced images are sent to WeryAI for generation. <br>
Mitigation: Use the skill only with prompts and images intended for that third-party service; avoid private reference images unless upload is expected. <br>
Risk: The skill depends on IMAGE_GEN_API_KEY and can persist local setup state. <br>
Mitigation: Prefer an environment variable or a gitignored local secret file, and never echo or commit the API key. <br>
Risk: Setup may request runtime or package installation before generation. <br>
Mitigation: Review installation requests before approving them, especially in shared or production workspaces. <br>
Risk: Security evidence flagged setup and upload behavior as requiring review. <br>
Mitigation: Review the skill behavior and generated commands before deployment, with particular attention to uploads, local config writes, and package installation. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/632657122/anime-image-generator) <br>
- [WeryAI platform notes](references/weryai-platform.md) <br>
- [Style presets](references/style-presets.md) <br>
- [First-time setup](references/config/first-time-setup.md) <br>
- [Model registry schema](references/config/model-registry-schema.md) <br>
- [Preferences schema](references/config/preferences-schema.md) <br>
- [WeryAI API keys](https://weryai.com/api/keys) <br>
- [WeryAI call history](https://weryai.com/api/history) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with CLI commands, local configuration updates, generated image files, and optional JSON task summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires IMAGE_GEN_API_KEY and local Node/npm plus either bun or npx; image generation sends prompts and referenced images to WeryAI.] <br>

## Skill Version(s): <br>
2026.3.23 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
