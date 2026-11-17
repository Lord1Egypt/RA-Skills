## Description:

调用百度 Unlimited-OCR API 解析 PDF、Word、PPT、图片等文档，并返回适合复杂表格、多段落、多结构文档的 Markdown 结构化结果。

This skill is ready for commercial/non-commercial use.

## Publisher:

[maglanyulan](https://clawhub.ai/user/maglanyulan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to submit documents or document URLs to Baidu Unlimited-OCR, poll for task completion, and retrieve Markdown parsing results for downstream review, knowledge-base ingestion, or document conversion workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send full document contents or document URLs to Baidu for OCR processing.

Mitigation: Use it only after explicit user agreement that the selected document or URL may be sent to Baidu, and avoid confidential, regulated, or internal documents unless that data flow is approved.

Risk: Baidu API credentials are required and the artifact documents both environment variables and plaintext agent configuration as setup options.

Mitigation: Prefer environment variables or a managed secret store, and avoid storing API keys or secret keys in plaintext agent configuration files.

Risk: The client can automatically download Markdown and parse-result URLs returned by the OCR service.

Mitigation: Consider disabling automatic result downloads or validating returned URLs against expected Baidu domains before retrieval.

## Reference(s):

- [API Parameters Reference](artifact/references/parameters.md)
- [Error Codes Reference](artifact/references/error_codes.md)
- [API Key Configuration Guide](artifact/references/apikey-fetch.md)
- [Baidu Unlimited-OCR Official API Documentation](https://cloud.baidu.com/doc/OCR/s/fmr1p39gb)
- [Baidu OCR Free Test Resources](https://cloud.baidu.com/doc/OCR/s/fk3h7xu7h)
- [Baidu OCR Pricing](https://cloud.baidu.com/doc/OCR/s/Fls06fa15)
- [Baidu AI Console](https://console.bce.baidu.com/ai/)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON returned from Baidu OCR APIs, with command-line usage and configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses asynchronous task submission and polling; Markdown and parse-result URLs returned by the service are documented as valid for 30 days.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
