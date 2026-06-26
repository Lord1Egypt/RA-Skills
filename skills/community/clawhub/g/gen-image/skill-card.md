## Description: <br>
Generates images with SiliconFlow-hosted Kolors, FLUX, and Qwen-Image models using a SiliconFlow API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[duyiliu](https://clawhub.ai/user/duyiliu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to generate image assets from text prompts through SiliconFlow image-generation models. It is useful when an agent needs to provide shell commands, configuration guidance, or a generated image file path for downstream workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image prompts are sent to SiliconFlow and may contain sensitive or proprietary text. <br>
Mitigation: Avoid secrets, regulated data, and proprietary content in prompts before using the skill. <br>
Risk: Using the SiliconFlow API key can consume paid quota. <br>
Mitigation: Confirm the configured API key and quota policy before running generation commands. <br>
Risk: The helper script parses API responses with jq and will fail if jq is unavailable. <br>
Mitigation: Install jq alongside curl before using artifact/scripts/generate.sh. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/duyiliu/gen-image) <br>
- [SiliconFlow homepage](https://siliconflow.cn) <br>
- [SiliconFlow image generation API endpoint](https://api.siliconflow.cn/v1/images/generations) <br>
- [SiliconFlow model list API endpoint](https://api.siliconflow.cn/v1/models) <br>
- [SiliconFlow API key portal](https://cloud.siliconflow.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance and shell output that can include a generated image file path] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq for the helper script, and SILICONFLOW_API_KEY; may consume SiliconFlow paid quota.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
