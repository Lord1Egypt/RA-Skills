## Description:

AI图像生成-免费版 helps agents generate images from text prompts with multiple aspect ratios and standard resolutions for personal creative workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, developers, and automation users can use this skill to turn prompt text into generated images for avatars, social media covers, concept visualization, and lightweight creative assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The trigger language is broader than image generation and could route unrelated prompts to an external API.

Mitigation: Use the skill only for explicit image-generation requests and review the requested action before any external API call.

Risk: Prompts may be sent to an external image-generation provider.

Mitigation: Avoid confidential, regulated, or sensitive prompt text and verify the external API provider before use.

Risk: The artifact references a generation script that is not present in the submitted files.

Mitigation: Confirm the required generation script or equivalent implementation exists in the runtime environment before relying on the skill.

Risk: The skill requires an API key for image generation.

Mitigation: Keep API keys in environment variables or managed secrets and out of source-controlled files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/ai-image-gen-tool-free)
- [Publisher profile](https://clawhub.ai/user/thcjp)
- [Gemini image API endpoint referenced by artifact](https://code.newcli.com/gemini)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides an agent through API-key configuration, model selection, prompt construction, and saving generated image files.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
