## Description:

Uses Nano Banana 2 through AI Hive to create reusable e-commerce product hero images from SKU truth tables for white-background, lifestyle, kit, variant, and promotion-space views.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Marketplace operators, designers, and listing teams use this skill to turn approved SKU photos and SKU truth tables into channel-ready product image prompts and AI Hive image generation commands. It is intended for product identity, quantity, variant, included-item, and layout consistency checks before publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected product images and prompts are sent to AI Hive for generation.

Mitigation: Use only images the merchant is comfortable sharing with AI Hive, and avoid highly sensitive unreleased assets unless the service is trusted for that use.

Risk: The script stores an AI Hive API key locally or reads it from the environment.

Mitigation: Use a dedicated API key, keep the generated config file permission-restricted, and rotate the key if it may have been exposed.

Risk: The script trusts service-provided upload and download URLs without destination allowlists or maximum download sizes.

Mitigation: Run it in a controlled environment, use a virtual environment for dependencies, and monitor output downloads and destination paths.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ecommerce-main-image)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates AI Hive image tasks, can upload reference images, query task status, and download image outputs to a local directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
