## Description: <br>
使用火山引擎豆包模型生成图片，通过火山引擎豆包图片生成 API 创建图片，并支持自定义提示词、尺寸、模型等参数。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wanxing0724](https://clawhub.ai/user/wanxing0724) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to generate images from text prompts with Volcengine Doubao models, including control over model, image size, and image count. It requires the user's own Volcengine image API key and writes generated images to local storage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and generation settings are sent to Volcengine using the user's API key. <br>
Mitigation: Use only prompts and settings that are acceptable to share with Volcengine, and configure VOLCENGINE_IMAGE_API_KEY with an appropriate account and permissions. <br>
Risk: Generated images are written to local storage, and the artifact currently contains a hard-coded Windows output directory. <br>
Mitigation: Review or change the output directory before use so generated files are saved to an intended, portable location. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wanxing0724/doubao-image) <br>
- [Publisher profile](https://clawhub.ai/user/wanxing0724) <br>
- [Volcengine console](https://console.volces.com/) <br>
- [Volcengine Ark image generation endpoint](https://ark.cn-beijing.volces.com/api/v3/images/generations) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Generated image file with console status text and setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires VOLCENGINE_IMAGE_API_KEY; supports prompt, model, size, and image count parameters; saves generated images locally.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
