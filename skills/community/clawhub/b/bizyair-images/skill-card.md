## Description: <br>
基于 BizyAir 异步 API 的模块化图片生成助手，支持多工作流模板（web_app_id）动态切换与自定义传参。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bozoyan](https://clawhub.ai/user/bozoyan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, creators, and external users use this skill to submit BizyAir image-generation jobs from text prompts, choose workflow templates, set dimensions and batch size, and retrieve generated image URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image prompts and generation settings are sent to BizyAir. <br>
Mitigation: Do not include confidential or regulated information in prompts unless the user trusts BizyAir's handling of that data. <br>
Risk: The skill relies on BIZYAIR_API_KEY for authenticated network calls. <br>
Mitigation: Keep BIZYAIR_API_KEY out of chat messages, logs, and generated output. <br>
Risk: Generated images may be downloaded to local storage. <br>
Mitigation: Save images only to intended folders after checking the final path. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bozoyan/bizyair-images) <br>
- [BizyAir create task API endpoint](https://api.bizyair.cn/w/v1/webapp/task/openapi/create) <br>
- [BizyAir output query API endpoint](https://api.bizyair.cn/w/v1/webapp/task/openapi/outputs?requestId=) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown with inline shell commands and image-result tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses BIZYAIR_API_KEY, submits asynchronous BizyAir tasks, returns request IDs, status guidance, and generated image URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
