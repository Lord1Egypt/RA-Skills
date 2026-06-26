## Description: <br>
Supports OCR for education certificates and extracts fields such as holder name, certificate number, major, school name, and graduation date. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scnet-sugon](https://clawhub.ai/user/scnet-sugon) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to send a local education certificate image or PDF to Scnet's OCR API and receive structured certificate fields for review or downstream processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Certificate images or PDFs may contain personal or sensitive education records and are sent to Scnet's remote OCR service. <br>
Mitigation: Use the skill only for documents that are appropriate to share with Scnet, minimize unnecessary personal data, and review the provider's privacy, retention, and compliance terms before use. <br>
Risk: The skill requires a sensitive API credential. <br>
Mitigation: Store SCNET_API_KEY in the configured environment or local config file with restricted permissions, and do not paste the key into chat transcripts or shared logs. <br>
Risk: OCR results may be incomplete or incorrect for low-quality scans or unsupported files. <br>
Mitigation: Review extracted fields against the source document before using them for records, decisions, or automated workflows. <br>


## Reference(s): <br>
- [Sugon-Scnet OCR API docs](references/api-docs.md) <br>
- [Scnet website](https://www.scnet.cn) <br>
- [ClawHub skill page](https://clawhub.ai/scnet-sugon/education-certificate-ocr) <br>
- [Publisher profile](https://clawhub.ai/user/scnet-sugon) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, configuration guidance] <br>
**Output Format:** [Pretty-printed JSON data from the OCR response, with human-readable error text on failure.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local certificate file path, an OCR type, and SCNET_API_KEY credentials; the script removes the top-level confidence field from each result item before printing.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
