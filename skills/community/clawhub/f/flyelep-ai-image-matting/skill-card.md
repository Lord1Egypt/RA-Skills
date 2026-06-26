## Description: <br>
Uses the Flyelep AI Tool API to remove image backgrounds from one or more public image URLs and return processed image URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flyelepai](https://clawhub.ai/user/flyelepai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill when a user asks to cut out a subject, remove an image background, extract a product subject, or create transparent-background assets. It is suitable for single-image or batch workflows where the input images are available as direct public URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user-provided image URLs to Flyelep's API with a user-supplied secretKey. <br>
Mitigation: Install only if you trust Flyelep with the submitted image URLs, provide the secretKey at runtime, and avoid storing the key in files or persistent configuration. <br>
Risk: Private, expired, or non-direct image links may fail or expose content through an unintended public URL workflow. <br>
Mitigation: Use only intended public direct image URLs and test with non-sensitive images before submitting sensitive or production assets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/flyelepai/flyelep-ai-image-matting) <br>
- [Flyelep open platform](https://www.flyelep.cn/controlboard) <br>
- [Flyelep AI image matting API endpoint](https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/aiTool/aiImageMatting) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with JSON and shell command examples; runtime results are image URLs returned by the API.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns one or more processed image URLs, comma-separated by the API for batch requests.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
