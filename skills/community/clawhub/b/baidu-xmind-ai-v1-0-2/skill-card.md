## Description: <br>
Provides Baidu Intelligent Document Analysis API guidance and commands for document extraction, document parsing, PaddleOCR-VL parsing, document comparison, contract review, and document format conversion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wsxf](https://clawhub.ai/user/wsxf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document-processing teams use this skill to invoke Baidu cloud document AI services for extracting fields, parsing text and tables, comparing versions, reviewing contracts, and converting document formats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploaded documents may contain confidential, regulated, or customer data and are sent to Baidu cloud APIs for processing. <br>
Mitigation: Use only approved documents, avoid sensitive uploads without authorization, and confirm that Baidu processing is acceptable for the relevant data class. <br>
Risk: Baidu API keys can grant access to paid or sensitive document-processing services if exposed. <br>
Mitigation: Store credentials in environment variables or a protected local config file, keep them out of source control, logs, and shared terminals, and restrict file permissions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wsxf/skills/baidu-xmind-ai-v1-0-2) <br>
- [Baidu Intelligent Document Analysis](https://ai.baidu.com/tech/nlp/Textanalysis) <br>
- [Baidu Intelligent Document Analysis Console](https://console.bce.baidu.com/textmind/application/textExtract) <br>
- [Baidu API Documentation](https://ai.baidu.com/ai-doc/OCR/klzkwzdch) <br>
- [Document Extraction API Reference](references/doc_extract.md) <br>
- [Document Parsing API Reference](references/doc_parse.md) <br>
- [PaddleOCR-VL Parsing API Reference](references/doc_parse_vl.md) <br>
- [Document Comparison API Reference](references/doc_compare.md) <br>
- [Contract Review API Reference](references/contract_review.md) <br>
- [Document Conversion API Reference](references/doc_convert.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Python snippets, configuration examples, and JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May upload selected user documents to Baidu cloud APIs and may save JSON results to a user-specified output file.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
