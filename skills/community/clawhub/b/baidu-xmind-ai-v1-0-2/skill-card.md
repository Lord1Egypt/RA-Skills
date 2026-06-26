## Description: <br>
百度智能文档分析平台API调用技能，支持文档抽取、文档解析、PaddleOCR-VL 文档解析、文档比对、合同审查和文档格式转换。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wsxf](https://clawhub.ai/user/wsxf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call Baidu Document AI services for extracting fields from documents, parsing text and tables, comparing document versions, reviewing contracts for risks, and converting document formats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected documents are sent to Baidu cloud services for processing. <br>
Mitigation: Use only when the user or organization is permitted to send the chosen documents to Baidu, and avoid confidential, regulated, privileged, or highly sensitive documents without approval. <br>
Risk: Baidu API credentials and access tokens are sensitive. <br>
Mitigation: Store credentials in environment variables or a secret manager, avoid plaintext dotfiles when possible, never commit credentials, and avoid exposing access tokens in browser-visible URLs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wsxf/baidu-xmind-ai-v1-0-2) <br>
- [Baidu Document Extraction API](https://ai.baidu.com/ai-doc/OCR/klzkwzdch) <br>
- [Baidu Document Parsing API](https://ai.baidu.com/ai-doc/OCR/llxst5nn0) <br>
- [Baidu PaddleOCR-VL Parsing API](https://ai.baidu.com/ai-doc/OCR/3mi73at9o) <br>
- [Baidu Document Comparison API](https://ai.baidu.com/ai-doc/OCR/Glqd7jgmf) <br>
- [Baidu Contract Review API](https://ai.baidu.com/ai-doc/OCR/olqc085rg) <br>
- [Baidu Document Conversion API](https://ai.baidu.com/ai-doc/OCR/Elf3sp7cz) <br>
- [Document Extraction Reference](artifact/references/doc_extract.md) <br>
- [Document Parsing Reference](artifact/references/doc_parse.md) <br>
- [PaddleOCR-VL Parsing Reference](artifact/references/doc_parse_vl.md) <br>
- [Document Comparison Reference](artifact/references/doc_compare.md) <br>
- [Contract Review Reference](artifact/references/contract_review.md) <br>
- [Document Conversion Reference](artifact/references/doc_convert.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Python examples, and JSON-oriented API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Baidu API credentials and may write result JSON files when an output path is provided.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
