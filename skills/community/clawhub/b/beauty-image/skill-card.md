## Description:

Beauty Image is a commercial AI image-generation assistant with scene templates, style dictionaries, intent recognition, structured prompts, and routing across Wanx, Seedream 4, and Seedream 5 engines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yh22e](https://clawhub.ai/user/yh22e)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creators use this skill in OpenClaw to generate business cards, posters, avatars, product images, 3D-style objects, and other visual assets from natural-language prompts. The skill can apply templates, style dictionaries, size presets, optional structured fields, and engine routing before returning generated image URLs or saved image files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and any included personal or business text are sent to third-party image-generation services and optionally to DeepSeek for intent parsing.

Mitigation: Avoid secrets or regulated data in prompts, and use dedicated API keys for DashScope, Volcengine Ark, and DeepSeek.

Risk: Using the legacy SSL verification bypass can weaken transport security.

Mitigation: Keep certificate verification enabled and avoid the legacy --no-verify-ssl option.

Risk: Runtime dependency changes may affect sensitive deployments.

Mitigation: Pin dependencies and review the skill before deployment in sensitive environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yh22e/skills/beauty-image)
- [Project Homepage](https://github.com/xyva-yuangui/beauty-image)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Console text with MEDIA_URL lines, RESULT_JSON, optional local image files, and Markdown image-display guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated image URLs are described by the artifact as temporary; filename output saves the image locally when requested.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
