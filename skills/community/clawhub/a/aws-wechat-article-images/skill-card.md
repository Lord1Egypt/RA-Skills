## Description:

为微信公众号文章生成封面图和正文配图，根据文章标题与内容自动匹配画风，并支持一稿多方案和可复用风格预设。

This skill is ready for commercial/non-commercial use.

## Publisher:

[aiworkskills](https://clawhub.ai/user/aiworkskills)

### License/Terms of Use:

MIT-0

## Use Case:

External content editors, self-media operators, brand designers, and agents use this skill to plan and generate WeChat article cover images and inline illustrations from article content. It is intended for long-form article image workflows that need reusable visual styles, prompt files, generated image files, and insertion guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Article prompts and the image-model API key may be sent to a configurable external image endpoint.

Mitigation: Use a restricted, dedicated API key and configure only trusted HTTPS endpoints for image generation.

Risk: The skill can read article drafts, prompt files, configuration, and product image directories in the article workspace.

Mitigation: Install and run it only in a dedicated article workspace, and review prior-draft and product-image directories before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aiworkskills/skills/aws-wechat-article-images)
- [cover-method.md](references/cover-method.md)
- [image-method.md](references/image-method.md)
- [specs.md](references/specs.md)
- [cover-styles README](references/cover-styles/README.md)
- [image-styles README](references/image-styles/README.md)
- [prompt-construction.md](references/image-styles/prompt-construction.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands, prompt files, and generated image file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update image prompts, generated image files, optional image analysis notes, and article image references.]

## Skill Version(s):

1.0.24 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
