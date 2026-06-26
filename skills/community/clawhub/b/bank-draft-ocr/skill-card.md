## Description: <br>
Bank Draft OCR identifies bank draft documents and extracts key fields such as issue date, payee, paying bank, and draft amount. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scnet-sugon](https://clawhub.ai/user/scnet-sugon) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external users use this skill to submit local bank draft images or PDFs to Scnet OCR and receive structured recognition results for downstream review or processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends selected bank draft images or PDFs to Scnet's remote OCR API, which may expose sensitive financial document contents to a third party. <br>
Mitigation: Use the skill only for documents you are authorized to transmit to Scnet, and confirm organizational data handling requirements before use. <br>
Risk: The skill requires a Scnet API key for authentication. <br>
Mitigation: Store the key locally in the configured environment or config file and do not paste API keys into chat. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/scnet-sugon/bank-draft-ocr) <br>
- [Scnet Website](https://www.scnet.cn) <br>
- [Sugon-Scnet OCR API Documentation Summary](references/api-docs.md) <br>
- [Bank Draft Field Summary](assets/templates/fields-summary.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, API Calls, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Structured JSON recognition results with setup and command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SCNET_API_KEY and sends the selected document file to Scnet's remote OCR API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, skill frontmatter, skill.yaml, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
