## Description: <br>
Generates foundational product selling-point information for an international e-commerce video pipeline from product images and catalog details, producing a product layer image and structured selling-point data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bstory28](https://clawhub.ai/user/bstory28) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, e-commerce operators, and automation agents use this skill to analyze product imagery and product details, extract concise selling points, and prepare localized base assets for a downstream short-form commerce video pipeline. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may send product images or extracted product text to the documented AIGC service using configured API credentials. <br>
Mitigation: Confirm the data-sharing path and credential use are acceptable before running the skill. <br>
Risk: The skill may create local output files in a default Desktop folder. <br>
Mitigation: Use a controlled --output path and review generated PNG and JSON files before using them downstream. <br>
Risk: SUDOCODE_API_KEY is listed as a required credential without a documented purpose in the evidence. <br>
Mitigation: Treat it as an unexplained credential requirement unless the publisher documents why it is needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bstory28/skills/ecommerce-product-info-generator) <br>
- [Server-resolved GitHub provenance](https://github.com/BStory28/ecommerce-product-info-generator) <br>
- [Downstream ecommerce video script generator](https://github.com/BStory28/ecommerce-video-script-generator) <br>
- [AIGC service endpoint](https://aigc.hkttok.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown chat summary plus PNG and JSON output files, with shell commands for downstream pipeline handoff.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates product_layer.png, base_layers.json, selling_points.json, and image_analysis.json; defaults to a Desktop output folder unless --output is set.] <br>

## Skill Version(s): <br>
0.1.5 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
