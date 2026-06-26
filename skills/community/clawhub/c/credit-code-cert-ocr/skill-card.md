## Description: <br>
Extracts text and structured fields from document images, especially Unified Social Credit Code certificates, by calling Scnet's OCR API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scnet-sugon](https://clawhub.ai/user/scnet-sugon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to OCR local images or PDFs containing Unified Social Credit Code certificates and receive structured extracted fields for downstream review or processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected images or PDFs are sent to Scnet's OCR service. <br>
Mitigation: Use the skill only for documents approved for this provider and avoid sensitive files unless organizational data-handling requirements are met. <br>
Risk: The Scnet API key could be exposed if pasted into chat or stored loosely. <br>
Mitigation: Store SCNET_API_KEY in config/.env or the environment with restrictive permissions and do not paste credentials into conversations. <br>
Risk: High request volume can trigger API rate limits. <br>
Mitigation: Call the skill serially and retry later when 429 responses occur. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/scnet-sugon/credit-code-cert-ocr) <br>
- [Publisher profile](https://clawhub.ai/user/scnet-sugon) <br>
- [Sugon-Scnet OCR API documentation summary](references/api-docs.md) <br>
- [OCR field summary](assets/templates/fields-summary.md) <br>
- [Scnet website](https://www.scnet.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration guidance] <br>
**Output Format:** [JSON on stdout with friendly error text for failures] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local file path, ocrType UNIFIED_SOCIAL_CREDIT_REG, and SCNET_API_KEY; OCR results include recognized fields and confidence where returned by the API.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
