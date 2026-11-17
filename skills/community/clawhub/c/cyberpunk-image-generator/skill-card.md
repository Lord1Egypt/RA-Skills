## Description:

Generate cyberpunk style futuristic art for requests involving neon, sci-fi, dystopia, or cyberpunk cityscapes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[632657122](https://clawhub.ai/user/632657122)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate cyberpunk-styled images through a WeryAI gateway wrapper, including single-image, image-to-image, batch, and style-preset workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may persist an image generation API key in local configuration.

Mitigation: Use a restricted or disposable API key and avoid persisting it on shared machines.

Risk: The skill sends prompts and reference images to a third-party WeryAI gateway.

Mitigation: Review prompts, generated download URLs, and reference-image uploads before using sensitive material.

Risk: The runtime path may use `npx -y bun`, which can fetch tooling dynamically.

Mitigation: Prefer a locally installed trusted Bun runtime before running the skill.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/632657122/skills/cyberpunk-image-generator)
- [Publisher Profile](https://clawhub.ai/user/632657122)
- [WeryAI Platform Notes](references/weryai-platform.md)
- [First-Time Setup](references/config/first-time-setup.md)
- [Preferences Schema](references/config/preferences-schema.md)
- [Model Registry Schema](references/config/model-registry-schema.md)
- [Style Presets](references/style-presets.md)
- [WeryAI API Introduction](https://docs.weryai.com/en)
- [WeryAI API Keys](https://weryai.com/api/keys)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with CLI commands and generated image files or URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write generated image files and optional local configuration under project or user .image-skills directories.]

## Skill Version(s):

1.0.1 (source: server release evidence; source frontmatter reports 0.5.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
