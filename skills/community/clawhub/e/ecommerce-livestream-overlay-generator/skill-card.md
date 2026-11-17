## Description:

Generates ecommerce livestream visual overlay packages from brand, product, promotion, and optional product-photo inputs, including backgrounds, title banners, host imagery, price cards, product shelves, benefits bars, transparent assets, previews, and packaged delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaoyuji12138](https://clawhub.ai/user/gaoyuji12138)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, livestream operators, and ecommerce teams use this skill to turn product and promotion details into a ready-to-use livestream overlay kit. The agent helps gather required campaign information, generate prompts, call the image generation API, remove green-screen backgrounds, compose a preview, and deliver local assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and product photos may be sent to Volcano Engine for image generation.

Mitigation: Use the skill only when that third-party processing is acceptable, and avoid uploading unreleased, confidential, or sensitive product imagery.

Risk: Python image-processing dependencies are installed and executed locally.

Mitigation: Install dependencies in a dedicated virtual environment before running the workflow.

Risk: Generated images are saved to local disk and may be placed in a desktop folder when direct file delivery is unavailable.

Mitigation: Review the output location and remove generated assets when they are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gaoyuji12138/skills/ecommerce-livestream-overlay-generator)
- [Volcano Engine Ark console](https://console.volcengine.com/ark)
- [Volcano Engine privacy policy](https://www.volcengine.com/docs/6369/71845)
- [Volcano Engine Ark image generation endpoint](https://ark.cn-beijing.volces.com/api/v3/images/generations)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands, Python snippets, image prompts, PNG assets, JPG preview, and optional ZIP package]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a fixed seven-file overlay package: six PNG assets and one JPG preview; prompts and optional product photos are sent to Volcano Engine under the user's API key, and generated assets are saved locally.]

## Skill Version(s):

2.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
