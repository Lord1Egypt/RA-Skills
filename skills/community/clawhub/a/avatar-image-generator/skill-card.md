## Description: <br>
Generate avatars, profile pictures, PFPs, social media headshots, gaming avatars, and portrait icons. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[632657122](https://clawhub.ai/user/632657122) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to produce profile-picture style avatar images for social profiles, creator or founder portraits, gaming icons, stylized self-portraits, and team member profile images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send prompts, generated tasks, and image inputs to a WeryAI-backed image-generation API. <br>
Mitigation: Use it only for data approved for that provider and avoid private photos or sensitive personal details unless upload is intended. <br>
Risk: The broader runtime supports local file upload behavior beyond a narrowly scoped avatar helper. <br>
Mitigation: Prefer public HTTPS reference images for avatar work and review any local reference path before execution. <br>
Risk: Optional webhook callbacks and web search can disclose task context to additional network endpoints. <br>
Mitigation: Avoid arbitrary webhook URLs and keep web search disabled unless it is explicitly needed for the request. <br>
Risk: The setup flow can persist IMAGE_GEN_API_KEY into project or home .env files. <br>
Mitigation: Prefer environment variables or managed secret storage, and persist credentials only in trusted workspaces. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/632657122/avatar-image-generator) <br>
- [First-Time Setup](references/config/first-time-setup.md) <br>
- [Preferences Schema](references/config/preferences-schema.md) <br>
- [Model Registry Schema](references/config/model-registry-schema.md) <br>
- [Style Presets](references/style-presets.md) <br>
- [WeryAI Platform](references/weryai-platform.md) <br>
- [WeryAI API introduction](https://docs.weryai.com/en) <br>
- [WeryAI text-to-image API](https://docs.weryai.com/api-reference/avatar-image-generator/submit-text-to-image-task) <br>
- [WeryAI image-to-image API](https://docs.weryai.com/api-reference/avatar-image-generator/submit-image-to-image-task) <br>
- [WeryAI task status API](https://docs.weryai.com/api-reference/tasks/query-task-details) <br>


## Skill Output: <br>
**Output Type(s):** [Images, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Generated image files or URLs with concise Markdown status and setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses IMAGE_GEN_API_KEY, WeryAI image generation APIs, 1:1 avatar defaults, optional reference images, optional web search, and optional webhook callbacks.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata; artifact frontmatter reports 0.5.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
