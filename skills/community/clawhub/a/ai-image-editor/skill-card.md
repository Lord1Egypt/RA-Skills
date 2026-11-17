## Description:

Edit images with plain-language instructions via PopNow: change backgrounds, outfits, lighting or text, combine several photos, restyle or extend a picture using Nano Banana, GPT Image, Seedream, FLUX or Qwen edit models. Exact USD quote before every edit. Use when the user wants to modify, retouch or combine existing images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyuminjo](https://clawhub.ai/user/kyuminjo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use the skill to edit, retouch, restyle, extend or combine existing images with text instructions through PopNow image models. Each paid edit is quoted for approval before creation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and reference media are sent to PopNow and the generation provider; provider privacy practices were not tested.

Mitigation: Only share images and prompts suitable for those services, avoid sensitive personal data, and use images you have rights to submit.

Risk: Image generation is paid from a separate prepaid API balance.

Mitigation: Review and explicitly approve each quoted maximum price; use a dedicated API key with restricted models and spending caps.

Risk: Command arguments may be retained in host or agent logs.

Mitigation: Keep the API key in secret or environment settings and never pass it as a command argument.

## Reference(s):

- [PopNow image models](https://popnow.ai/image)
- [PopNow task API documentation](https://popnow.ai/docs/tasks)
- [PopNow privacy policy](https://popnow.ai/privacy)

## Skill Output:

**Output Type(s):** [Image links, Text]

**Output Format:** [Generated image URLs with concise text for quoted cost and task status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper returns output links and does not download image files.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
