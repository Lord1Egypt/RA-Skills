## Description: <br>
Extracts structured fields from Chinese driver license main and secondary pages using the Sugon-Scnet OCR API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scnet-sugon](https://clawhub.ai/user/scnet-sugon) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to submit local driver license images or PDFs to Scnet's OCR service and receive extracted identity, license, archive, validity, and record fields. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload sensitive driver-license images or PDFs to an external OCR API. <br>
Mitigation: Confirm the exact file path and document type before each run, and use it only when sending the document to Scnet's OCR service is acceptable. <br>
Risk: The skill requires an SCNET_API_KEY credential. <br>
Mitigation: Store the key in a local configuration file with restrictive permissions and avoid pasting credentials into chat. <br>
Risk: Broad auto-trigger guidance could cause unintended files to be processed. <br>
Mitigation: Require explicit user confirmation of the target document path before invoking the OCR command. <br>


## Reference(s): <br>
- [Sugon-Scnet OCR API Documentation Summary](references/api-docs.md) <br>
- [Driver License OCR Field Summary](assets/templates/fields-summary.md) <br>
- [Scnet Website](https://www.scnet.cn) <br>
- [ClawHub Skill Page](https://clawhub.ai/scnet-sugon/driver-license-ocr) <br>
- [Publisher Profile](https://clawhub.ai/user/scnet-sugon) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [JSON on standard output with text error messages on failure] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The JSON data contains OCR recognition results and field-level confidence information where returned by the API.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, skill.yaml, changelog, and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
