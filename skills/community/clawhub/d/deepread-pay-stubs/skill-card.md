## Description: <br>
Extracts structured data from pay stubs and earnings statements, including employer, employee, pay period, gross and net pay, taxes, deductions, and year-to-date totals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[uday390](https://clawhub.ai/user/uday390) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Lenders, tenant-screening teams, payroll auditors, and benefits reviewers use this skill to extract income-verification fields from pay stubs and earnings statements as structured JSON. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pay stubs can contain highly sensitive payroll, tax, identity, and banking information that may be sent to DeepRead for extraction. <br>
Mitigation: Review DeepRead's privacy and data-retention terms before use, and only send documents when that handling is acceptable for the workflow. <br>
Risk: The skill claims PII redaction is built in, but the security evidence says the claim is not sufficiently explained for highly sensitive payroll documents. <br>
Mitigation: Do not rely on built-in redaction until the publisher documents what is redacted, when redaction occurs, and whether it happens before external upload. <br>
Risk: Extracted income fields may affect lending, rental, benefits, or payroll decisions. <br>
Mitigation: Use the per-field needs_review flags and manually review flagged values before relying on the extraction. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/uday390/deepread-pay-stubs) <br>
- [DeepRead homepage](https://www.deepread.tech) <br>
- [DeepRead dashboard](https://www.deepread.tech/dashboard) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown instructions with JSON examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DEEPREAD_API_KEY and sends documents to the DeepRead API for extraction.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
