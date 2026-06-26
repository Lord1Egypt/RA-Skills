## Description: <br>
使用 DMXAPI 平台生成和编辑图片。支持 Gemini、Seedream（豆包即梦）、OpenAI 等多种模型。可进行文生图、图片编辑、多图融合、联网搜索增强生图。当用户需要生成图片、编辑图片、AI 绘图、多图融合时使用此技能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[onee-io](https://clawhub.ai/user/onee-io) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and agent users use this skill to generate images, edit images, fuse multiple input images, and build DMXAPI image-generation commands from natural-language requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends prompts and optional input images to DMXAPI and configured model providers. <br>
Mitigation: Use a dedicated revocable API key and avoid submitting private images or confidential prompts unless DMXAPI's data handling is acceptable. <br>
Risk: Generated images are written to local output directories and API usage may consume paid quota. <br>
Mitigation: Choose output directories deliberately and monitor DMXAPI quota or billing. <br>


## Reference(s): <br>
- [DMXAPI Console](https://www.dmxapi.cn/) <br>
- [ClawHub skill page](https://clawhub.ai/onee-io/dmxapi-image-generation) <br>
- [Publisher profile](https://clawhub.ai/user/onee-io) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown with inline shell commands and generated image file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 20+, the dmxapi-cli package, a DMXAPI API key, and deliberate output directory selection.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
