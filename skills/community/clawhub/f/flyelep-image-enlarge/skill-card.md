## Description: <br>
Image Enlarge helps an agent upscale one or more publicly accessible image URLs through the Flyelep AI image-enlargement API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flyelepai](https://clawhub.ai/user/flyelepai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they need an agent to upscale or enhance clarity for single images or batches of product images by calling Flyelep with user-provided image URLs and a runtime API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected image URLs are sent to Flyelep for processing. <br>
Mitigation: Use only image links that are approved for Flyelep processing, and avoid private or sensitive image URLs unless Flyelep is approved for that data. <br>
Risk: The Flyelep secretKey is required to call the API. <br>
Mitigation: Provide the secretKey only at runtime and avoid storing it in shared files, chats, examples, or persistent configuration. <br>


## Reference(s): <br>
- [Flyelep Image Enlarge API Endpoint](https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/aiTool/enlarge) <br>
- [Flyelep Controlboard](https://www.flyelep.cn/controlboard) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with request JSON, optional curl commands, and returned image URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns comma-separated enhanced image URLs from the API; the agent should split and present them individually.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
