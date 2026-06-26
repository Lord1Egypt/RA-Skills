## Description: <br>
Generates images and videos through the BigModel CogView and CogVideoX API for creative visuals such as covers, product images, social media assets, and short videos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[156554395](https://clawhub.ai/user/156554395) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, creators, and developers use this skill to call BigModel for prompt-driven image, batch image, and video generation. It supports scripts and Python APIs for social media assets, covers, product images, posters, and short videos. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and referenced image URLs are transmitted to BigModel for generation. <br>
Mitigation: Avoid sensitive prompts or private URLs, and require explicit confirmation before external generation calls. <br>
Risk: The skill requires a BigModel API key. <br>
Mitigation: Use scoped API keys and prefer session-only secret storage or a secrets manager. <br>
Risk: Broad activation language may trigger external generation when visual creation is only implied. <br>
Mitigation: Confirm user intent, model choice, and cost-sensitive settings before making API calls. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/156554395/bigmodel-image-video) <br>
- [BigModel Open Platform](https://open.bigmodel.cn/) <br>
- [BigModel API Base](https://open.bigmodel.cn/api) <br>
- [Skill README](README.md) <br>
- [Skill Instructions](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown guidance with Python and shell command snippets; API calls return JSON objects containing generated media URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BIGMODEL_API_KEY; generated prompts and optional image URLs are sent to BigModel.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
