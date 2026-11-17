## Description:

Uses Alibaba Cloud Model Studio Qwen VL models for image Q&A, visual analysis, OCR-like extraction, chart and table reading, and screenshot understanding workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to send image-and-text prompts to Alibaba Cloud Model Studio Qwen VL models for image understanding, structured extraction, and operational analysis tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Caller-supplied request data can route the DashScope API key and image payload to an unintended endpoint.

Mitigation: Use only trusted request JSON and remove or restrict the base_url override before deployment.

Risk: Images, screenshots, or documents may contain sensitive, secret, or regulated information that would be sent to Alibaba Cloud for processing.

Mitigation: Avoid sending sensitive or regulated data unless the workflow has explicit approval and appropriate data handling controls.

Risk: Unpinned dependencies or latest model aliases can reduce reproducibility for production workflows.

Mitigation: Pin Python dependencies and use snapshot model IDs when stable behavior is required.

## Reference(s):

- [Qwen VL API Reference Notes](references/api_reference.md)
- [Source List](references/sources.md)
- [Invoice Schema Example](references/examples/invoice.schema.json)
- [Alibaba Cloud DashScope Model List](https://help.aliyun.com/zh/model-studio/models)
- [Alibaba Cloud Qwen VL Usage](https://help.aliyun.com/zh/model-studio/qwen-vl?spm=a2c4g.11186623.help-menu-search-2400256.d_5_0_9_0.6dc14095CSwPw2)
- [Alibaba Cloud Model Rate Limits](https://help.aliyun.com/zh/model-studio/rate-limit)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON request and response examples plus optional saved JSON analysis output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save normalized results, usage data, prompts, and input image references to output/aliyun-qwen-vl/ for traceability.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
