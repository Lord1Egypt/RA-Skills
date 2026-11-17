## Description:

基于 BizyAir 异步 API 的模块化图片生成助手，支持多工作流模板（web_app_id）动态切换与自定义传参。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bozoyan](https://clawhub.ai/user/bozoyan)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to create BizyAir image-generation tasks from text prompts, choose workflow templates and dimensions, and retrieve generated image URLs when a request completes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-controlled prompts, custom parameters, or request IDs may be assembled into shell curl commands, creating local command-execution or malformed-request risk.

Mitigation: Run the skill in a sandbox, validate and quote shell inputs, and avoid accepting custom parameters or request IDs from untrusted users.

Risk: Prompts and generated-image requests are sent to the BizyAir API with a bearer token.

Mitigation: Use only non-sensitive prompts and a minimally scoped BizyAir API key.

Risk: Optional local downloads can create path traversal or overwrite risk if arbitrary save paths are accepted.

Mitigation: Allow downloads only when the runner enforces safe path validation and overwrite controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bozoyan/skills/bizyair-images)
- [BizyAir create task API](https://api.bizyair.cn/w/v1/webapp/task/openapi/create)
- [BizyAir task outputs API](https://api.bizyair.cn/w/v1/webapp/task/openapi/outputs?requestId=)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance]

**Output Format:** [Markdown with inline shell commands and image-result tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BIZYAIR_API_KEY and curl; generated images are returned as remote object URLs.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
