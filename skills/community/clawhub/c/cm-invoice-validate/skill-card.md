## Description: <br>
Helps users validate Chinese invoice authenticity from invoice fields or supported invoice files through the ClawMate invoice validation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lijianhu1](https://clawhub.ai/user/lijianhu1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to check invoice authenticity, review returned invoice details, and summarize single or batch validation results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Invoice files and validation results may contain sensitive invoice contents, tax identifiers, bank details, and API-key-backed usage data. <br>
Mitigation: Use narrow invoice-only folders, review batch lists before validation, and remove saved Markdown result files when they are no longer needed. <br>
Risk: The documented manual update command downloads and unzips code that can overwrite an installed agent skill. <br>
Mitigation: Run update commands only after verifying the downloaded ZIP through a trusted channel. <br>
Risk: The skill requires a ClawMate API key and sends invoice data to ClawMate for validation. <br>
Mitigation: Install and use the skill only where ClawMate is trusted to process the invoice data involved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lijianhu1/cm-invoice-validate) <br>
- [ClawMate API key page](https://www.clawmate.net/user) <br>
- [ClawMate invoice validation endpoint](https://www.clawmate.net/server/test/Api/InvoiceValidate) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, API Calls, Files, Guidance] <br>
**Output Format:** [Markdown summaries, terminal text, optional JSON API responses, and saved Markdown batch reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and CLAWMATE_API_KEY; batch validation may save timestamped Markdown result files.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and skill source) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
