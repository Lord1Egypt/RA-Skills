## Description: <br>
Extracts structured data from PDFs, images, and Word documents with layout analysis, table recognition, OCR, seal detection, and directory extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ankylala](https://clawhub.ai/user/ankylala) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document-workflow users use this skill to parse PDFs, scanned images, and Word files into structured JSON or Markdown for downstream review, extraction, and automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Parsed files may be uploaded to a configured remote document-parsing service, exposing document contents or metadata. <br>
Mitigation: Use only a trusted HTTPS endpoint, avoid confidential or regulated documents unless you control or trust the service and its retention policy, and protect API keys through environment variables or config.json. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/ankylala/document-parser) <br>
- [README](README.md) <br>
- [Skill instructions](SKILL.md) <br>
- [ClawHub package configuration](clawhub.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, files] <br>
**Output Format:** [Structured JSON and optional Markdown saved to a parsed result file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include parsed pages, document elements, table content, OCR text, seal detections, formulas, table-of-contents entries, and task status responses.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
