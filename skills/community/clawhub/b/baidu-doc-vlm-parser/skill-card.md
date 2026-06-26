## Description: <br>
调用百度 PaddleOCR-VL API 将 PDF、Office 文档和图片解析为 Markdown、JSON 和结构化版面结果。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maglanyulan](https://clawhub.ai/user/maglanyulan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to submit documents or document URLs to Baidu's PaddleOCR-VL service, poll asynchronous parsing tasks, and retrieve Markdown or JSON document-analysis results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected documents, document URLs, and parsing results are sent to Baidu for cloud processing. <br>
Mitigation: Use only documents approved for this external service, and avoid confidential or regulated content unless the use case has been reviewed. <br>
Risk: The skill requires Baidu API keys or secret keys. <br>
Mitigation: Store credentials outside source control in environment variables or an approved secret store, and rotate them if exposed. <br>
Risk: Returned markdown_url and parse_result_url values may expose parsed document content during their 30-day lifetime. <br>
Mitigation: Treat result links as sensitive, limit sharing, and avoid persisting them longer than necessary. <br>


## Reference(s): <br>
- [Baidu PaddleOCR-VL API documentation](https://ai.baidu.com/ai-doc/OCR/3mi73at9o) <br>
- [Baidu API key and secret key guide](https://ai.baidu.com/ai-doc/REFERENCE/Ck3dwjhhu#1-获取aksk) <br>
- [Baidu intelligent document analysis platform](https://ai.baidu.com/solution/intelligent-document-analysis) <br>
- [Baidu free test resource guide](https://ai.baidu.com/ai-doc/OCR/dk3iqnq51) <br>
- [API Key configuration guide](references/apikey-fetch.md) <br>
- [API parameters](references/parameters.md) <br>
- [Error codes](references/error_codes.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash examples and a Python parser that returns JSON plus Markdown/JSON result links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Baidu API credentials; parsing is asynchronous and returned result links are valid for 30 days.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
