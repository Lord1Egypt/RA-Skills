## Description:

Publishes Obsidian notes or supplied text to dev-blog by converting Markdown to .mdoc, preparing image prompts, post-processing user-provided images, and deploying through preview approval before main deployment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sonim1](https://clawhub.ai/user/sonim1)

### License/Terms of Use:


## Use Case:

Developers and blog maintainers use this skill to prepare bilingual dev-blog posts, generate or collect supporting images, convert content into the expected .mdoc format, and publish through preview review before production.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can modify and push the dev-blog repository, including broad staging and force-pushing to the preview branch.

Mitigation: Use explicit file paths instead of git add -A, review the staged diff, require a clean working tree, and avoid force-push unless force-with-lease is explicitly confirmed.

Risk: Image prompts, generated images, and Telegram-transferred files may be shared with third-party services.

Mitigation: Keep secrets and sensitive drafts out of prompts and transferred files, strip image metadata when needed, and use restricted provider API keys.

## Reference(s):

- [Blog Format Reference](references/blog-format.md)
- [ClawHub Skill Page](https://clawhub.ai/sonim1/skills/blog-publisher)
- [Production Blog](https://sonim1.com)
- [Google Generative Language API Endpoint](https://generativelanguage.googleapis.com/v1beta/models)
- [OpenRouter Chat Completions API Endpoint](https://openrouter.ai/api/v1/chat/completions)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with frontmatter examples, shell command blocks, file path conventions, and generated or transformed blog/image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include .mdoc blog content, WebP image assets, image generation prompts, git commands, preview links, and deployment status notes.]

## Skill Version(s):

1.0.0 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
