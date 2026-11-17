## Description:

Calls the Volcengine Seedream image generation API to create images from text prompts and optional reference images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lamuier](https://clawhub.ai/user/lamuier)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate Seedream images from natural-language prompts, optionally using reference images, grouped image generation, or the Seedream web_search tool.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reference-image paths can upload any readable local file that is passed as an image input.

Mitigation: Pass only non-sensitive image files that are intended for Seedream processing; prefer vetted paths or URLs.

Risk: Prompts, reference images, URLs, and optional web_search requests are sent to an external Volcengine provider.

Mitigation: Avoid sensitive prompts or private files, and use only a Volcengine API key intended for Seedream usage.

Risk: Generated images are downloaded automatically by default and downloads are not constrained by the security evidence.

Mitigation: Review output locations and downloaded files before reuse, sharing, or execution in downstream workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lamuier/skills/doubao-seedream-skill)
- [Volcengine Seedream API endpoint](https://ark.cn-beijing.volces.com/api/v3/images/generations)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with Python and shell examples; generated image URLs and downloaded local image files at runtime]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires VOLCENGINE_API_KEY and sends prompts, reference images, URLs, and optional web_search requests to an external provider.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter says 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
