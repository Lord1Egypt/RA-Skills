## Description: <br>
Uses the Flyelep AI Tool API to identify products in images and generate new images with changed product colors while keeping the product otherwise unchanged. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flyelepai](https://clawhub.ai/user/flyelepai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they need an agent to recolor a product image through Flyelep's HTTP API while preserving product identity, material appearance, logos, background, lighting, and composition. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Flyelep secretKey could be exposed if hard-coded, logged, or stored in generated files. <br>
Mitigation: Collect the secretKey at runtime, pass it only in the HTTP request header, and avoid persisting it in skill files, examples, repositories, or durable configuration. <br>
Risk: Product images and prompts are sent to Flyelep's service for processing. <br>
Mitigation: Use only product images and prompts that the user is comfortable sharing with Flyelep. <br>
Risk: Color-change results may alter unintended regions or drift from the requested appearance when prompts or source images are unclear. <br>
Mitigation: Use clear product image URLs and prompts that specify the target color and any elements to preserve, such as logos, background, materials, lighting, and composition. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/flyelepai/flyelep-product-color-change) <br>
- [Flyelep Product Color Change API Endpoint](https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/aiTool/productColorChange) <br>
- [Flyelep Open Platform](https://www.flyelep.cn/controlboard) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Text] <br>
**Output Format:** [Markdown with JSON and shell command examples, plus a resulting image URL when the API call succeeds] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a runtime Flyelep secretKey, a public image URL, a color-change prompt, and modelType 0 or 1.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
