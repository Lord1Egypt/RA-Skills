## Description: <br>
Extracts text and structured birth medical certificate fields from local image or document files through the Sugon-Scnet OCR API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scnet-sugon](https://clawhub.ai/user/scnet-sugon) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to submit a specific birth medical certificate image, PDF, or archive to the Sugon-Scnet OCR API and receive structured certificate fields as JSON. It is intended for authorized OCR extraction of birth certificate details, not unrelated document processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Birth certificate images and extracted identity or medical details may be uploaded to a third-party OCR API. <br>
Mitigation: Use the skill only with explicit user intent, a specific authorized file path, and prior confirmation that Scnet is trusted to process the document. <br>
Risk: The skill requires a sensitive SCNET_API_KEY credential stored in configuration. <br>
Mitigation: Keep the API key out of chat transcripts, store it in a protected config/.env or environment variable, and rotate it if it is exposed or returns authorization errors. <br>
Risk: Using the skill for unrelated OCR tasks can route documents outside the intended birth certificate workflow. <br>
Mitigation: Restrict calls to the documented BIRTH_CERTIFICATE OCR type and reject unrelated document-processing requests. <br>


## Reference(s): <br>
- [Sugon-Scnet OCR API Documentation](references/api-docs.md) <br>
- [Birth Certificate Field Summary](assets/templates/fields-summary.md) <br>
- [Scnet](https://www.scnet.cn) <br>
- [ClawHub Skill Page](https://clawhub.ai/scnet-sugon/birth-medical-cert-ocr) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON data on standard output with human-readable error text on failure] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The script removes confidence fields from API results before printing the JSON payload.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter, skill.yaml, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
