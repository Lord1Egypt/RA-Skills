## Description:

AI image generation with OpenAI GPT Image 2, Azure OpenAI, Google, OpenRouter, DashScope, Z.AI GLM-Image, MiniMax, Jimeng, Seedream and Replicate APIs, supporting text-to-image, reference images, aspect ratios, and batch generation from saved prompt files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jimliu](https://clawhub.ai/user/jimliu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and content-production agents use this skill to generate images from prompts, prompt files, and reference images across configurable image providers. It is also useful for repeated or multi-image workflows where saved prompts should be generated in batch.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project-local settings can redirect API-keyed requests through provider base URL configuration.

Mitigation: Use the skill only in trusted directories, review project `.baoyu-skills/.env` files before running, and avoid combining global API keys with project-defined `*_BASE_URL` settings.

Risk: The runtime fallback can download unpinned code when using `npx` to obtain Bun.

Mitigation: Prefer a preinstalled trusted Bun binary and use the `npx` fallback only after reviewing the execution environment.

Risk: Prompts, prompt files, reference images, and remote reference URLs may be sent to the selected external provider.

Mitigation: Treat all generation inputs as provider-bound data and avoid including sensitive or confidential material unless the selected provider and account controls are appropriate.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jimliu/skills/baoyu-imagine)
- [Project homepage](https://github.com/JimLiu/baoyu-skills#baoyu-imagine)
- [Usage examples](references/usage-examples.md)
- [First-time setup](references/config/first-time-setup.md)
- [Preferences schema](references/config/preferences-schema.md)
- [Codex OAuth vs OpenAI API key](references/codex-oauth-vs-openai-api-key.md)
- [Codex Image2 fallback](references/codex-image2-fallback.md)
- [DashScope provider guide](references/providers/dashscope.md)
- [MiniMax provider guide](references/providers/minimax.md)
- [OpenRouter provider guide](references/providers/openrouter.md)
- [Replicate provider guide](references/providers/replicate.md)
- [Z.AI provider guide](references/providers/zai.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands, configuration instructions, optional JSON status, and generated image files from the selected provider.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports single-image and batch workflows, provider-specific model selection, reference-image inputs where supported, and configurable output paths.]

## Skill Version(s):

1.117.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
