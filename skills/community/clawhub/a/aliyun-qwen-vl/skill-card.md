## Description: <br>
Uses Alibaba Cloud Model Studio Qwen VL models for image Q&A, visual analysis, OCR-like extraction, chart and table reading, and screenshot understanding workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to route image understanding tasks through Alibaba Cloud Model Studio Qwen VL, including visual Q&A, screenshot understanding, chart/table reading, and structured extraction from images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted images, prompts, and local outputs may contain sensitive data and are sent to Alibaba Cloud for processing. <br>
Mitigation: Use only data approved for Alibaba Cloud processing, redact sensitive content before submission, and manage local output retention. <br>
Risk: The helper script can send the Alibaba Cloud API key, prompt, and image content to a request-specified server instead of only DashScope. <br>
Mitigation: Use trusted request JSON only and do not pass a base_url override unless that endpoint is intentionally trusted with the API key and submitted content. <br>


## Reference(s): <br>
- [Qwen VL API Reference Notes](references/api_reference.md) <br>
- [Invoice Extraction Schema Example](references/examples/invoice.schema.json) <br>
- [Source List](references/sources.md) <br>
- [Alibaba Cloud DashScope model list](https://help.aliyun.com/zh/model-studio/models) <br>
- [Alibaba Cloud Qwen VL usage](https://help.aliyun.com/zh/model-studio/qwen-vl?spm=a2c4g.11186623.help-menu-search-2400256.d_5_0_9_0.6dc14095CSwPw2) <br>
- [Alibaba Cloud model rate limits](https://help.aliyun.com/zh/model-studio/rate-limit) <br>
- [ClawHub release page](https://clawhub.ai/cinience/aliyun-qwen-vl) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON request/response examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can save normalized JSON model responses and extraction results to output/aliyun-qwen-vl/ for traceability.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
