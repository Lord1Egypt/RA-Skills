## Description: <br>
This skill helps an agent call Flyelep's product replacement API to replace a product in an image while preserving the original scene, background, lighting, and composition. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flyelepai](https://clawhub.ai/user/flyelepai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to submit product-image replacement requests to Flyelep with a source image URL, optional replacement product image URL, model choice, and prompt constraints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Flyelep secretKey is required for API authentication and could expose account access or billing if stored or shared improperly. <br>
Mitigation: Provide the secretKey only at runtime in the request header, avoid committing it to files or persistent configuration, and rotate it if exposure is suspected. <br>
Risk: Source and replacement image URLs, plus prompts, are sent to a third-party service. <br>
Mitigation: Confirm trust in Flyelep before use and avoid submitting private or sensitive images unless the user accepts Flyelep's data handling and billing terms. <br>
Risk: Requests can fail when image URLs are not public direct links, credentials are invalid, the modelType is outside 0 or 1, or long generations time out. <br>
Mitigation: Validate inputs before calling the API, use only public direct image URLs, pass modelType 0 or 1, and allow a 120-300 second timeout for generation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/flyelepai/flyelep-product-replace) <br>
- [Flyelep product replacement API endpoint](https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/aiTool/productReplace) <br>
- [Flyelep control board](https://www.flyelep.cn/controlboard) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with JSON and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The downstream API returns a generated image URL; the skill instructs agents to show that URL directly rather than reading back image contents.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
