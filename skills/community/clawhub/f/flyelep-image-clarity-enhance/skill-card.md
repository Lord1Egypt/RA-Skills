## Description:

通过 Flyelep AI 工具接口增强单张或批量图片的清晰度。

This skill is ready for commercial/non-commercial use.

## Publisher:

[flyelepai](https://clawhub.ai/user/flyelepai)

### License/Terms of Use:

MIT-0

## Use Case:

面向需要提升单张或批量图片清晰度的用户；技能通过 Flyelep AI 服务处理图片并返回结果链接。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Images are sent to Flyelep for processing; the security assessment was partial and noted that the cleanup command's relationship to the main function was unclear.

Mitigation: Use only images you are comfortable sending to Flyelep, provide the API key at runtime, and review cleanup behavior before execution.

## Reference(s):

- [Flyelep image clarity enhancement API](https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/aiTool/imageClarityEnhance)
- [Flyelep file upload API](https://www.flyelep.cn/prod-api/poster-design/api/v1/file/upload)
- [Flyelep Open Platform (API key access)](https://www.flyelep.cn/controlboard)
- [ClawHub skill release](https://clawhub.ai/flyelepai/skills/flyelep-image-clarity-enhance)

## Skill Output:

**Output Type(s):** [API Calls, Text, URLs]

**Output Format:** [JSON API result summarized as image URLs and status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Batch results may contain fewer image URLs than inputs when individual images fail.]

## Skill Version(s):

1.0.5 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
