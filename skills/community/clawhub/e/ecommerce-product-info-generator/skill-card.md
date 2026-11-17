## Description:

Generates ecommerce product selling-point summaries, a high-fidelity product layer image, and structured base-layer data for localized short-video workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bstory28](https://clawhub.ai/user/bstory28)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ecommerce content teams use this skill to turn product images and product details into structured selling points, localized base-image design guidance, a product layer image, and downstream inputs for video-script and video-generation skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can send product images and product details to the disclosed external image API.

Mitigation: Avoid sending confidential product images unless the external service is approved for the intended use.

Risk: The release evidence notes missing scripts and dependency hygiene concerns.

Mitigation: Review or obtain the referenced scripts before execution, use a virtual environment, and pin dependency versions where possible.

Risk: The skill requires API credentials for AIGC_APP_KEY, AIGC_APP_SECRET, and SUDOCODE_API_KEY.

Mitigation: Confirm why each credential is required and provide secrets only through approved environment-variable or secret-management paths.

## Reference(s):

- [Server-resolved source repository](https://github.com/BStory28/ecommerce-product-info-generator)
- [ClawHub skill page](https://clawhub.ai/bstory28/skills/ecommerce-product-info-generator)
- [Downstream video script generator repository](https://github.com/BStory28/ecommerce-video-script-generator)
- [External image API base URL](https://aigc.hkttok.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Files, Shell commands, Configuration guidance]

**Output Format:** [Markdown plus generated PNG and JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can save product_layer.png, base_layers.json, selling_points.json, and image_analysis.json to an output directory for downstream skills.]

## Skill Version(s):

0.1.5 (source: server release metadata; artifact frontmatter reports 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
