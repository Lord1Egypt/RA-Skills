## Description: <br>
Extract structured data from W-2s, 1099s, 1040s, and other tax forms into typed JSON with per-field confidence flags and PII redaction guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[uday390](https://clawhub.ai/user/uday390) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and business users use this skill to extract typed JSON from tax forms for tax preparation, lending or underwriting, accounting intake, payroll audits, and related income verification workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tax forms and related personal or financial information are sent to DeepRead's API. <br>
Mitigation: Use the skill only when that data transfer is approved, request only needed fields, and follow the redaction guidance to limit sensitive data exposure. <br>
Risk: The skill requires a DeepRead API key. <br>
Mitigation: Store DEEPREAD_API_KEY securely and avoid sharing it in prompts, logs, or committed files. <br>
Risk: Extracted tax data may include fields that need human review before use in filings or income calculations. <br>
Mitigation: Check the per-field needs_review flags and review flagged values before relying on the output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/uday390/deepread-tax-forms) <br>
- [DeepRead homepage](https://www.deepread.tech) <br>
- [DeepRead dashboard](https://www.deepread.tech/dashboard) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with cURL commands, JSON schemas, and JSON extraction examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DEEPREAD_API_KEY; instructs agents to send user-provided tax documents to DeepRead's API and review per-field needs_review flags.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
