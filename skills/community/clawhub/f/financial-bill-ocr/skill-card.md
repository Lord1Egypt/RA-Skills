## Description: <br>
Financial Bill Ocr sends user-selected financial bill images or documents to the Scnet OCR API and returns structured recognition results for drafts, checks, receipts, deposit slips, transfer vouchers, payment vouchers, and mobile payment statements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scnet-sugon](https://clawhub.ai/user/scnet-sugon) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to extract structured fields from supported financial bills by providing an OCR type and local file path. Users should treat uploads as sensitive financial documents and confirm that Scnet's data handling terms fit their requirements before use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/scnet-sugon/financial-bill-ocr) <br>
- [Scnet Publisher Profile](https://clawhub.ai/user/scnet-sugon) <br>
- [Sugon-Scnet OCR API Documentation Summary](references/api-docs.md) <br>
- [Supported Financial Bill Fields](assets/templates/fields-summary.md) <br>
- [Scnet Website](https://www.scnet.cn) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Text, Shell commands, Configuration] <br>
**Output Format:** [Structured JSON on standard output with user-facing error text on failure] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SCNET_API_KEY and uploads the selected local document to Scnet's remote OCR service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release, frontmatter, changelog, skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
