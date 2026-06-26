## Description: <br>
Generates images from text prompts or one to eight reference image URLs using the BizyAir GPT_IMAGE_2 API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bozoyan](https://clawhub.ai/user/bozoyan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to generate images from prompts or transform one to eight reference images through BizyAir GPT_IMAGE_2. It helps an agent choose the text-to-image or image-to-image script, pass aspect ratio options, wait for remote generation, and report the saved image path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scripts print the first characters of BIZYAIR_API_KEY in command output. <br>
Mitigation: Remove or fully mask API-key logging before use, and avoid sharing logs from image-generation runs. <br>
Risk: Prompts and reference image URLs are sent to the third-party BizyAir API. <br>
Mitigation: Confirm user consent before sending private prompts or image URLs, and avoid using sensitive images unless approved. <br>
Risk: Local permissions and shell behavior are broader than necessary for a credentialed API integration. <br>
Mitigation: Narrow allowed shell permissions to the specific scripts and review commands before installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bozoyan/bozo-aigc) <br>
- [BizyAir OpenAPI task endpoint](https://api.bizyair.cn/w/v1/webapp/task/openapi/create) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with shell command invocations and generated image files saved under pic/] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BIZYAIR_API_KEY and may take 90 seconds to 10 minutes for remote image generation.] <br>

## Skill Version(s): <br>
2.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
