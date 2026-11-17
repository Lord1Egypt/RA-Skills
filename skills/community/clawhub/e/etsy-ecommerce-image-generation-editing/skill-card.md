## Description:

Creates and edits Etsy listing images for handmade, vintage, and personalized products, including scale, material, maker-process, customization, and gift-packaging visuals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, Etsy sellers, and agents use this skill to generate or edit listing visuals that preserve product authenticity, scale, materials, customization options, process views, and packaging details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials can be sent to a configured base URL, including an untrusted host if the user changes --base-url or AI_HIVE_BASE_URL.

Mitigation: Use only the trusted AI Hive endpoint, avoid untrusted base URLs, and keep ~/.ai-hive/config.json protected.

Risk: Product or customer images uploaded for listing generation may contain sensitive or personal data.

Mitigation: Upload only images intended for AI Hive processing and avoid sensitive product or customer information unless that use is approved.

Risk: Generated listing visuals may misrepresent handmade, vintage, personalization, scale, or packaging details.

Mitigation: Use seller-provided references and review outputs against Etsy listing policies and the skill's authenticity checks before publishing.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/wubin1836/skills/etsy-ecommerce-image-generation-editing)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key page](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, image files]

**Output Format:** [Markdown guidance with bash commands and generated image files from API tasks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports reference images, batch generation, task polling, and local configuration for AI Hive API access.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
