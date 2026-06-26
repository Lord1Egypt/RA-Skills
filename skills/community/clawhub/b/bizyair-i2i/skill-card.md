## Description: <br>
BizyAir 图生图（Image-to-Image）助手 uploads a local reference image to BizyAir and uses a prompt plus optional aspect ratio to create an image-to-image generation task. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bozoyan](https://clawhub.ai/user/bozoyan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, creators, and developers use this skill to upload a local image as a reference, submit an image-to-image prompt to BizyAir, and retrieve generated image URLs from the task result. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uploads the selected image, filename, prompt, and generated-task data to BizyAir and Alibaba OSS. <br>
Mitigation: Use it only with images and prompts that are acceptable to share with those services; avoid sensitive, private, or proprietary content. <br>
Risk: BizyAir credentials are required to run the upload and generation workflow. <br>
Mitigation: Keep the BizyAir API key in the BIZYAIR_API_KEY environment variable and avoid embedding it in prompts, logs, or shared command history. <br>
Risk: The workflow depends on Python packages and network services outside the skill artifact. <br>
Mitigation: Review unpinned Python dependencies before installation and expect failures when BizyAir or Alibaba OSS endpoints are unavailable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bozoyan/bizyair-i2i) <br>
- [BizyAir task creation endpoint](https://api.bizyair.cn/w/v1/webapp/task/openapi/create) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown status messages and result tables with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include BizyAir request IDs, task status, generated image URLs, and upload or API error messages.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
