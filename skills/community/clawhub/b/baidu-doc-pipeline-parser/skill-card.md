## Description: <br>
调用百度文档解析API解析文档，支持PDF、Word、Excel、PPT、图片等18+格式，并提取文本、表格、版面分析、OCR识别及RAG文档分块。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maglanyulan](https://clawhub.ai/user/maglanyulan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and document-processing teams use this skill to submit documents to Baidu's document parsing API for OCR, text and table extraction, layout analysis, Markdown conversion, and RAG-oriented chunking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documents selected for parsing are sent to Baidu's document parsing service. <br>
Mitigation: Use only with documents that policy permits Baidu to process; avoid confidential, regulated, or secret material unless approved. <br>
Risk: The skill requires Baidu API credentials. <br>
Mitigation: Use a dedicated limited-quota API key and keep BAIDU_DOC_AI_API_KEY and BAIDU_DOC_AI_SECRET_KEY out of source control. <br>
Risk: Returned markdown_url and parse_result_url links may expose parsed document content during their 30-day lifetime. <br>
Mitigation: Treat result links as private and avoid sharing or logging them in public channels. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/maglanyulan/baidu-doc-pipeline-parser) <br>
- [Baidu document parsing API documentation](https://ai.baidu.com/ai-doc/OCR/llxst5nn0) <br>
- [Baidu Intelligent Document Analysis Platform](https://ai.baidu.com/solution/intelligent-document-analysis) <br>
- [Baidu API key setup documentation](https://ai.baidu.com/ai-doc/REFERENCE/Ck3dwjhhu#1-获取aksk) <br>
- [API key configuration guide](references/apikey-fetch.md) <br>
- [Parameter reference](references/parameters.md) <br>
- [Error code reference](references/error_codes.md) <br>


## Skill Output: <br>
**Output Type(s):** [API calls, JSON, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [JSON API responses with optional downloaded parse-result JSON and Markdown result links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses asynchronous task submission and polling; returned markdown_url and parse_result_url links are documented as private and valid for 30 days.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
