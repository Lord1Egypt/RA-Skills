## Description: <br>
image-clarity-enhance helps an agent call Flyelep's image clarity enhancement API for one or more public image URLs and return the enhanced image URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flyelepai](https://clawhub.ai/user/flyelepai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they want an agent to enhance the clarity of single or batch image URLs through Flyelep's HTTP API, choosing light, standard, or strong enhancement strength. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user-provided image URLs to Flyelep's image enhancement API. <br>
Mitigation: Submit only image URLs that users are comfortable sharing with Flyelep, and avoid private or sensitive images unless Flyelep's privacy and retention practices are acceptable. <br>
Risk: The API requires a secretKey for requests. <br>
Mitigation: Provide the secretKey at runtime, keep it out of skill files and persistent configuration, and rotate it if it is exposed. <br>
Risk: The API expects public direct image links and specific image constraints. <br>
Mitigation: Confirm that submitted URLs are direct public JPG, PNG, or BMP links within the documented size, dimension, and aspect-ratio limits before calling the API. <br>


## Reference(s): <br>
- [image-clarity-enhance on ClawHub](https://clawhub.ai/flyelepai/flyelep-image-clarity-enhance) <br>
- [Flyelep Open Platform](https://www.flyelep.cn/controlboard) <br>
- [Flyelep Image Clarity Enhance API](https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/aiTool/imageClarityEnhance) <br>
- [Skill Definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text responses with optional HTTP request examples and enhanced image URLs returned by the API.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs can include selected enhancement strength, API response status, error guidance, and comma-split enhanced image URLs.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
