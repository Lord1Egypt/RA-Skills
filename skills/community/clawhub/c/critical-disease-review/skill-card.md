## Description: <br>
Assesses structured hospitalization records against 28 critical-disease insurance claim criteria and returns raw JSON plus a natural-language conclusion with supporting evidence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aaiccee](https://clawhub.ai/user/aaiccee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Insurance claims reviewers and claim automation agents use this skill to evaluate structured hospitalization records against supported critical-disease claim criteria and organize the resulting conclusion, reasons, and evidence. Its output is claim-assessment support, not medical diagnosis or treatment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Structured medical records may be sent to the configured assessment service, and the server security summary notes that the privacy claims do not match the code behavior. <br>
Mitigation: Use only with an organization-approved endpoint and real patient or claims data after confirming redaction, transfer, and privacy controls. <br>
Risk: Assessment outputs are saved to disk by default, which can retain medical or claims information after the run. <br>
Mitigation: Use controlled output paths, define retention and cleanup controls, and prefer a corrected release that makes persistence opt-in. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aaiccee/critical-disease-review) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands] <br>
**Output Format:** [Raw JSON response files and plain-text natural-language assessment summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports a disease selector, model type, timeout, input JSON path, and optional output paths.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
