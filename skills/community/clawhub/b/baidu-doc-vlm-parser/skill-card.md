## Description:

调用百度PaddleOCR-VL大模型API解析文档，支持PDF、Word、PPT、图片等格式，并可识别印刷文本、手写文本、表格、公式、图表、印章和复杂版面元素。

This skill is ready for commercial/non-commercial use.

## Publisher:

[maglanyulan](https://clawhub.ai/user/maglanyulan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-processing teams use this skill to submit documents or document URLs to Baidu PaddleOCR-VL and retrieve structured parsing results such as Markdown, JSON, layout elements, tables, images, coordinates, and task status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send full documents, document URLs, and Baidu API credentials to external Baidu Cloud services.

Mitigation: Use it only with documents approved for Baidu Cloud processing, store credentials through controlled environment configuration, and avoid confidential, regulated, customer, legal, financial, or identity documents unless organizational policy permits that processing.

Risk: Returned Baidu result links may expose parsed Markdown or JSON output while they remain valid.

Mitigation: Treat result links as sensitive, limit sharing, and disable automatic result downloading when local retention is not needed.

Risk: The authoritative security summary reports one unsafe result-download pattern.

Mitigation: Review downloaded parse-result content before downstream use and run the skill in an environment with appropriate network, credential, and data-handling controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maglanyulan/skills/baidu-doc-vlm-parser)
- [Baidu PaddleOCR-VL API documentation](https://cloud.baidu.com/doc/OCR/s/3mi73at9o)
- [Baidu OCR pricing and purchasing](https://cloud.baidu.com/doc/OCR/s/Fls06fa15#%E6%96%87%E6%A1%A3%E8%A7%A3%E6%9E%90%EF%BC%88paddleocr-vl%EF%BC%89)
- [Baidu OCR error codes](https://cloud.baidu.com/doc/OCR/s/dk3iqnq51)
- [API Key configuration guide](references/apikey-fetch.md)
- [API parameters](references/parameters.md)
- [Error codes](references/error_codes.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, shell command examples, and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can return Baidu-hosted Markdown and JSON result URLs, downloaded parse results, task IDs, status messages, and error details.]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
