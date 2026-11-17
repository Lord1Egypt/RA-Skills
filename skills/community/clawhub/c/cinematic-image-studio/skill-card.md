## Description:

Builds cinematic image prompts from 75 reusable style cards and can generate images through a configured provider.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kongzichixiangjiao](https://clawhub.ai/user/kongzichixiangjiao)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creators use the skill to turn a subject or scene into a detailed image-generation prompt matched to a reusable visual style. They can optionally generate images through a configured image provider.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Provider credentials and image-generation charges may exceed the intended scope, and prompts or reference images are sent to the selected image processor.

Mitigation: Use an explicitly configured provider with a restricted key; check its privacy practices and any host-tool billing, and confirm the image count before generation.

Risk: Unchecked download URLs and file paths can reach beyond the intended project scope.

Mitigation: Validate download URLs and keep processed files within the project directory.

## Reference(s):

- [Cinematic Image Studio on ClawHub](https://clawhub.ai/kongzichixiangjiao/skills/cinematic-image-studio)
- [Film-style image standards](artifact/references/电影级画面规范.md)
- [Style card standards](artifact/references/风格卡规范.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Image files]

**Output Format:** [Structured image prompts in Markdown; optional generated image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompts combine style guidance with subject-specific scene details.]

## Skill Version(s):

2.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
