## Description: <br>
Recognizes degree certificates and extracts the certificate holder name, degree type, issuing institution, and grant date. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scnet-sugon](https://clawhub.ai/user/scnet-sugon) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Employees, external users, and developers use this skill to run OCR on degree certificate images or PDFs and receive structured fields for document review or data entry. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Degree certificate images or PDFs and extracted OCR data are sent to Scnet's remote API. <br>
Mitigation: Use the skill only when third-party handling of the documents is acceptable for privacy, compliance, and organizational requirements. <br>
Risk: The skill requires a sensitive SCNET_API_KEY credential. <br>
Mitigation: Store the key in an environment variable or protected config file and avoid pasting it into chats or logs. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/scnet-sugon/degree-certificate-ocr) <br>
- [scnet-sugon publisher profile](https://clawhub.ai/user/scnet-sugon) <br>
- [Sugon-Scnet OCR API docs summary](references/api-docs.md) <br>
- [Degree certificate OCR field summary](assets/templates/fields-summary.md) <br>
- [Scnet website](https://www.scnet.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [JSON on stdout, with text error guidance on failure] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SCNET_API_KEY; sends selected degree certificate files to Scnet's remote OCR API.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, changelog, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
