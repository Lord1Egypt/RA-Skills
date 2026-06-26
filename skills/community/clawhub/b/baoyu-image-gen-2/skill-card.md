## Description: <br>
AI image generation with OpenAI, Google, OpenRouter, DashScope, Jimeng, Seedream, and Replicate APIs, supporting text-to-image, reference images, aspect ratios, and batch generation from saved prompt files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nengnengZ](https://clawhub.ai/user/nengnengZ) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to generate images from prompts or saved prompt files, optionally with reference images, model/provider selection, aspect ratio controls, and batch execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected reference images may be sent to external image-generation providers. <br>
Mitigation: Review the selected provider's data and billing policies, and avoid submitting sensitive inputs unless that provider is approved for the use case. <br>
Risk: Provider API credentials are required for normal operation. <br>
Mitigation: Use least-privilege, project-scoped API keys where possible and keep credentials out of prompts, source files, and shared configuration. <br>
Risk: Saved preferences can apply at project or user scope. <br>
Mitigation: Prefer project-scoped preferences when defaults should not affect other workspaces. <br>
Risk: The release evidence advises verifying that the runtime script is present before relying on the installed package. <br>
Mitigation: Confirm the installed package includes the referenced runtime script before using the skill in an agent workflow. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/nengnengZ/baoyu-image-gen-2) <br>
- [Project Homepage](https://github.com/JimLiu/baoyu-skills#baoyu-image-gen) <br>
- [First-Time Setup](references/config/first-time-setup.md) <br>
- [Qwen-Image API](https://help.aliyun.com/zh/model-studio/qwen-image-api) <br>
- [DashScope Text-to-Image Guide](https://help.aliyun.com/zh/model-studio/text-to-image) <br>
- [Qwen-Image Edit API](https://help.aliyun.com/zh/model-studio/qwen-image-edit-api) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Image files, JSON] <br>
**Output Format:** [Markdown guidance with shell commands; generated image files and optional JSON status output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a supported runtime and provider API credentials; batch mode can produce multiple image files.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
