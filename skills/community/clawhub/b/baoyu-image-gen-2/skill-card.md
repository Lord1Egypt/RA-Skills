## Description:

AI image generation with OpenAI, Google, OpenRouter, DashScope, Jimeng, Seedream and Replicate APIs, supporting text-to-image, reference images, aspect ratios, and batch generation from saved prompt files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nengnengz](https://clawhub.ai/user/nengnengz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to generate images from prompts, prompt files, and optional reference images across multiple image-generation providers. It supports single-image work as well as batch generation when prompts are already saved.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use an unpinned `npx -y bun` runtime fallback.

Mitigation: Prefer installing and using a trusted local `bun` binary before running the skill.

Risk: Persistent preferences can affect generation behavior across projects when saved outside the project.

Mitigation: Use project-scoped preferences unless cross-project defaults are intentional.

Risk: Configured providers may receive prompts, API keys, and reference images needed for generation.

Mitigation: Verify which provider, model, API keys, and reference images are selected before generation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nengnengz/skills/baoyu-image-gen-2)
- [Project Homepage](https://github.com/JimLiu/baoyu-skills#baoyu-image-gen)
- [First-Time Setup](references/config/first-time-setup.md)
- [Qwen-Image API](https://help.aliyun.com/zh/model-studio/qwen-image-api)
- [Text-to-Image Guide](https://help.aliyun.com/zh/model-studio/text-to-image)
- [Qwen-Image Edit API](https://help.aliyun.com/zh/model-studio/qwen-image-edit-api)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration, JSON]

**Output Format:** [Image files with optional JSON status output and Markdown/shell guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports single-image generation and batch generation from saved prompt files; provider, model, quality, aspect ratio, size, and reference images can be configured.]

## Skill Version(s):

0.1.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
