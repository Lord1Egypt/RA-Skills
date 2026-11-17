## Description:

AI image generation with OpenAI GPT Image 2, Azure OpenAI, Google, OpenRouter, DashScope, Z.AI GLM-Image, MiniMax, Jimeng, Seedream, Replicate and Agnes APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jimliu](https://clawhub.ai/user/jimliu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to generate images from prompts, prompt files, reference images, aspect ratios, provider-specific options, and batch payloads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and reference images may be sent to the selected image provider.

Mitigation: Use providers whose data handling is acceptable for the input, and avoid sending confidential prompts or images unless that provider is approved.

Risk: The optional codex-cli provider can launch a Codex subprocess with broad local execution authority.

Mitigation: Use codex-cli only for trusted prompts and repositories, and prefer direct provider APIs when local execution authority is not needed.

Risk: Project-local configuration can redirect provider choices and sensitive execution settings.

Mitigation: Review project-local .baoyu-skills configuration and .env files before running the skill in an unfamiliar workspace.

Risk: The npx bun fallback can fetch tooling at runtime.

Mitigation: Prefer a pinned, trusted Bun installation over the npx fallback for repeatable or security-sensitive use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jimliu/skills/baoyu-image-gen)
- [Project homepage](https://github.com/JimLiu/baoyu-skills#baoyu-image-gen)
- [Usage Examples](references/usage-examples.md)
- [First-Time Setup](references/config/first-time-setup.md)
- [Preferences Schema](references/config/preferences-schema.md)
- [Codex OAuth vs OpenAI API Key](references/codex-oauth-vs-openai-api-key.md)
- [Codex Image2 Fallback](references/codex-image2-fallback.md)
- [Codex CLI Provider](references/providers/codex-cli.md)
- [DashScope Provider](references/providers/dashscope.md)
- [OpenRouter Provider](references/providers/openrouter.md)
- [Replicate Provider](references/providers/replicate.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON batch payloads, configuration snippets, and generated image file paths or structured errors.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can call external image provider APIs and save generated images to user-specified paths.]

## Skill Version(s):

2.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
