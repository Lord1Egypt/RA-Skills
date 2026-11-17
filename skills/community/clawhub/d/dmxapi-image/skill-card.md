## Description:

使用 MiniMax (image-01) 和其他模型生成图片，支持文生图和图片编辑，并提示用户配置 DMXAPI_API_KEY 环境变量。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoliang1319-cloud](https://clawhub.ai/user/xiaoliang1319-cloud)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide agents in generating or editing images with MiniMax-compatible image-generation APIs from text prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and credentials may be sent to an external MiniMax-compatible image-generation service.

Mitigation: Confirm the service and data-handling terms are acceptable before use, provide credentials through an environment variable, and avoid sending sensitive prompts.

Risk: The artifact uses mildly inconsistent API key naming between the description and code example.

Mitigation: Use the documented DMXAPI_API_KEY value consistently and verify the credential format against the target service before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaoliang1319-cloud/skills/dmxapi-image)

## Skill Output:

**Output Type(s):** [Guidance, Code, Configuration]

**Output Format:** [Markdown with JavaScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a MiniMax-compatible API key and sends prompts to an external image-generation service.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
