## Description: <br>
使用火山引擎豆包模型生成图片。通过火山引擎豆包图片生成 API 创建图片。支持自定义提示词、尺寸、模型等参数。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wanxing0724](https://clawhub.ai/user/wanxing0724) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and image-generation users can use this skill to create Doubao images from text prompts through the Volcengine API, with optional model, size, count, URL-only, and output-directory controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts are sent to Volcengine for image generation and may expose sensitive user or business information. <br>
Mitigation: Avoid placing secrets, personal data, or confidential business details in prompts. <br>
Risk: The skill requires a Volcengine API key and can consume API quota or incur billing. <br>
Mitigation: Install only when the Volcengine API key and expected usage are approved for the workspace. <br>
Risk: Generated images may be saved outside the expected directory when DOUBAO_IMAGE_OUTPUT_DIR is customized. <br>
Mitigation: Review DOUBAO_IMAGE_OUTPUT_DIR before running the skill and confirm the selected output location is appropriate. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wanxing0724/doubao-image-openclaw) <br>
- [Volcengine console](https://console.volces.com/) <br>
- [Volcengine image generation API endpoint](https://ark.cn-beijing.volces.com/api/v3/images/generations) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, configuration, guidance] <br>
**Output Format:** [Console text with URL or file-path markers and downloaded image files when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses VOLCENGINE_IMAGE_API_KEY for API access and DOUBAO_IMAGE_OUTPUT_DIR to customize saved image location.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
